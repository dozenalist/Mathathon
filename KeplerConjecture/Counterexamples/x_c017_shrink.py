#!/usr/bin/env python3
"""Bounded rational-size reduction of X-C017, with no loss of structure.

Why the stored triple is 10 KB.  `both_sides_gmargin.py` rounds the float SDP solution to
denominators <= 1e8 and then solves the 12 linear constraints *exactly* for the columns that
SymPy's rref chose.  Those columns form a dense 12x12 block, so the solved entries carry the
determinant of that block: 281-digit numerators.  The free entries are fine (<= 8 digits).

What is actually forced.  Write v(x) = (1,x,...,x^5), S = 8, and let
    d_k(M) = sum_{i+j=k} M_ij            (the k-th anti-diagonal sum, 0 <= k <= 10).
Then  v(w/S)^T M v(w/S) = sum_k d_k(M) (w/S)^k, so
    Q(w) = sum_k [ S^-k d_k(A) + S^-(k-1) d_k(B) ] w^k ,
and H (hence P and Q) depends on G only through d_0(G),...,d_10(G).  The constraint that
v^T A v + w v^T B v equals the exact Fourier map of P = -(s-4)H is *linear* in
(G,A,B) -- it is the 12 x N matrix L of `both_sides_gmargin.build`, and the condition is
simply
    L p = 0 ,   p = (G_ij , A_ij , B_ij) .
Row k of L touches only the A-entries with i+j=k and the B-entries with i+j=k-1, plus
G-entries on two adjacent anti-diagonals.  So choosing ONE A-column per row k <= 10 and one
B-column at k = 11 gives a *diagonal* pivot block whose determinant is +-2^a 8^-b: tiny.
Everything else can stay at a coarse rational approximation.

Consequence: the same construction certifies a density at 1e-9 of the stored one, with every
entry a rational of <= D digits.  This script searches the denominator cap D, verifies the
result exactly (L p = 0, rational LDL on G,A,B, P0,Q0 > 0) and writes X_C017_small.json.

Run: python3 x_c017_shrink.py
"""
import json, sys
import sympy as sp
from sympy import Rational as R
import ce_exact_gauss as G

m, S = 5, 8
N = 2*m+1
v = lambda x: sp.Matrix([x**i for i in range(m+1)])

# ---- exact constraint matrix L (12 x 126), same construction as both_sides_gmargin.build
rows = G.fourier_map_matrix(N)
polys = []
for n in range(N+1):
    e = sp.expand(rows[n]); sy = e.free_symbols
    polys.append(sp.Poly(e, list(sy)[0] if sy else sp.Symbol('w')))
Ml = []
for k in range(N+1):
    row = []
    for n in range(N+1):
        if polys[n].free_symbols:
            c = polys[n].coeff_monomial(sp.Symbol('w')**k); row.append(R(0) if c is None else R(c))
        else:
            row.append(R(polys[n].as_expr()) if k == 0 else R(0))
    Ml.append(row)
ent = [(i,j) for i in range(m+1) for j in range(i,m+1)]; n = len(ent)
Lm = sp.zeros(N+1, 3*n)
for k in range(N+1):
    for nidx in range(N+1):
        c = Ml[k][nidx]
        if c == 0: continue
        for mult, off in ((R(4), 0), (R(-1), 1)):
            j = nidx - off
            if j < 0 or j > 2*m: continue
            for ei,(a,b) in enumerate(ent):
                if a+b == j: Lm[k,ei] += c*mult*(1 if a == b else 2)*R(S)**(-j)
    if k <= 2*m:
        for ei,(a,b) in enumerate(ent):
            if a+b == k: Lm[k,n+ei] -= (1 if a == b else 2)*R(S)**(-k)
    if 1 <= k <= 2*m+1:
        for ei,(a,b) in enumerate(ent):
            if a+b == k-1: Lm[k,2*n+ei] -= (1 if a == b else 2)*R(S)**(-(k-1))

# ---- pivot columns: one per row, so the pivot block is diagonal
piv = []
for k in range(N+1):
    if k <= 2*m:
        cand = [(abs(0), n+ei) for ei,(a,b) in enumerate(ent) if a+b == k]   # A block
        key = 'A'
    else:
        cand = [(abs(0), 2*n+ei) for ei,(a,b) in enumerate(ent) if a+b == k-1]
        key = 'B'
    piv.append((key, [ci for _, ci in cand]))
print("pivot rows: " + ", ".join("%d:%s" % (k, p[0]) for k, p in enumerate(piv)))

# ---- load the stored certificate
d = json.load(open('X_C017_certificate.json'))
def pack(d):
    x = [None]*(3*n)
    for ei,(a,b) in enumerate(ent):
        x[ei] = R(d['G'][a][b]); x[n+ei] = R(d['A'][a][b]); x[2*n+ei] = R(d['B'][a][b])
    return x
p0 = pack(d)
ok0 = Lm*sp.Matrix(p0)
print("stored certificate: max |L p| = %s" % max(abs(t) for t in ok0))

def digits(q): return max(len(str(abs(q.p))), len(str(abs(q.q))))

def rebuild(x):
    Gm = sp.zeros(m+1); Am = sp.zeros(m+1); Bm = sp.zeros(m+1)
    for ei,(a,b) in enumerate(ent):
        Gm[a,b] = Gm[b,a] = x[ei]
        Am[a,b] = Am[b,a] = x[n+ei]
        Bm[a,b] = Bm[b,a] = x[2*n+ei]
    return Gm, Am, Bm

def ldl_ok(M):
    nn = M.rows; cur = M[:,:]
    for k in range(nn):
        dd = cur[k,k]
        if dd < 0: return False, k
        if dd == 0:
            if any(cur[k,j] != 0 for j in range(k,nn)): return False, k
            continue
        for i in range(k+1,nn):
            f = cur[i,k]/dd
            for j in range(k,nn): cur[i,j] -= f*cur[k,j]
    return True, None

print("\ncap        maxdigits  bytes   P0/Q0                          density        LDL")
results = []
for cap in (10**8, 10**6, 10**4, 10**3, 500):
    x = [R(sp.Rational(p0[j]).limit_denominator(cap)) for j in range(3*n)]
    # one exact solve per row: the pivot column of that row is the only unknown of its row
    for k, (key, cols) in enumerate(piv):
        jbest = max(cols, key=lambda j: abs(x[j]))
        s = sum(Lm[k,j]*x[j] for j in range(3*n) if j != jbest)
        x[jbest] = sp.nsimplify(-s/Lm[k,jbest]) if False else R(-s/Lm[k,jbest])
    res = max(abs(t) for t in Lm*sp.Matrix(x))
    Gm, Am, Bm = rebuild(x)
    g_ok, _ = ldl_ok(Gm); a_ok, _ = ldl_ok(Am); b_ok, _ = ldl_ok(Bm)
    Hb = sp.expand((v(G.s_/S).T*Gm*v(G.s_/S))[0]); P = sp.expand(-(G.s_-4)*Hb)
    P0 = P.subs(G.s_, 0); Q0 = Am[0,0]
    rq = R(P0)/R(Q0); dens = float(R(4,3)/sp.sqrt(sp.pi)*rq)
    md = max(digits(q) for q in x)
    blob = json.dumps({"m":m,"S":S,
        "G":[[str(Gm[i,j]) for j in range(m+1)] for i in range(m+1)],
        "A":[[str(Am[i,j]) for j in range(m+1)] for i in range(m+1)],
        "B":[[str(Bm[i,j]) for j in range(m+1)] for i in range(m+1)],
        "P_over_Q":str(rq),"density":dens})
    print("%-10d %-10d %-7d %-30.20s %.12f  G=%s A=%s B=%s  [Lp=%s]"
          % (cap, md, len(blob), str(rq)[:30], dens, g_ok, a_ok, b_ok, res == 0))
    results.append((cap, md, len(blob), dens, g_ok and a_ok and b_ok and res == 0 and P0 > 0 and Q0 > 0, x, blob, rq))

good = [r for r in results if r[4] and r[3] < 0.783097911]
if good:
    best = min(good, key=lambda r: (r[2], r[0]))
    print("\nsmallest passing: cap=%d, max digits=%d, %d bytes, density=%.12f"
          % (best[0], best[1], best[2], best[3]))
    json.dump(json.loads(best[6]), open('X_C017_small.json','w'), indent=1)
    print("wrote X_C017_small.json")
    print("stored (original): 10056 bytes, 281-digit entries, density 0.782267220")
    print("reduction factor in bytes: %.1fx" % (10056.0/best[2]))
else:
    print("\nNO passing reduction found"); sys.exit(1)
