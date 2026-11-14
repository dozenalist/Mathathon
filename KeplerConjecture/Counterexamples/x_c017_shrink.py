#!/usr/bin/env python3
"""Bounded rational-size reduction of X-C017.  Reproduces X_C017_small.json exactly.

Why the stored triple is 10 KB.  `both_sides_gmargin.py` rounds the float SDP solution to
denominators <= 1e8 and then solves the 12 linear constraints *exactly* for the columns that
SymPy's rref picked.  Those columns form a dense 12x12 block, so the solved entries carry its
determinant: 281-digit numerators.

The constraint.  With d_k(M) = sum_{i+j=k} M_ij,
    v(w/S)^T M v(w/S) = sum_k d_k(M) (w/S)^k ,
so the identity  v^T A v + w v^T B v = Fourier(P),  P = -(s-4) v(s/S)^T G v(s/S),  is
*linear* in (G,A,B): it is  L p = 0  for a 12 x 126 rational matrix L.  Row k of L touches
only A-entries on anti-diagonal k, B-entries on anti-diagonal k-1, and G-entries on two
adjacent anti-diagonals.

Two choices make the reduction work.
 1. Pivot ONE A column per row k <= 10 and one B column at k = 11.  The pivot block is then
    diagonal with entries -(1 or 2) S^-k, so no determinant enters.  (rref's dense block is
    what produced the 281-digit numerators.)
 2. Round to the dyadic grid 2^-m, not to 10^-m.  First attempt with 10^-m gave 122-digit
    entries even with the diagonal pivot block: each row-sum term has a <= 17-digit
    denominator, the terms' denominators are mutually coprime, and the lcm of 21 of them is
    118 digits.  Denoms of powers of two share the factor 2, so no lcm is taken.

What is *not* claimed.  This is a different certificate: the density moves in the 8th decimal.
Coarser grids fail because the SDP forced A, B >= 1e-6 I and a grid coarser than 1e-6
destroys that margin; G survives coarser grids because it was given eps_G = 1e-2.  The digit
count also has a floor: S^11 = 8.6e9 appears whenever a pivot coefficient S^-k is inverted,
so ~10 digits are structural and no 5-digit certificate exists in this basis.

Run: python3 x_c017_shrink.py        (writes X_C017_small.json, ~5 s)
"""
import json, sys
import sympy as sp
from sympy import Rational as R
import ce_exact_gauss as G

m, S = 5, 8
N = 2*m+1
GRID = 24                      # 2^-24: the finest grid at which the stored A stays PSD
v = lambda x: sp.Matrix([x**i for i in range(m+1)])

# ---- exact constraint matrix L (12 x 126), same construction as both_sides_gmargin.build
rows = G.fourier_map_matrix(N)
polys = []
for nn in range(N+1):
    e = sp.expand(rows[nn]); sy = e.free_symbols
    polys.append(sp.Poly(e, list(sy)[0] if sy else sp.Symbol('w')))
Ml = []
for k in range(N+1):
    row = []
    for nn in range(N+1):
        if polys[nn].free_symbols:
            c = polys[nn].coeff_monomial(sp.Symbol('w')**k); row.append(R(0) if c is None else R(c))
        else:
            row.append(R(polys[nn].as_expr()) if k == 0 else R(0))
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

piv = [([n+ei for ei,(a,b) in enumerate(ent) if a+b == k] if k <= 2*m
        else [2*n+ei for ei,(a,b) in enumerate(ent) if a+b == k-1]) for k in range(N+1)]

def digits(q): return max(len(str(abs(q.p))), len(str(abs(q.q))))
def ldl(Mx):
    cur = Mx[:,:]; nn = Mx.rows
    for k in range(nn):
        dd = cur[k,k]
        if dd < 0: return False
        if dd == 0:
            if any(cur[k,j] != 0 for j in range(k,nn)): return False
            continue
        for i in range(k+1,nn):
            f = cur[i,k]/dd
            for j in range(k,nn): cur[i,j] -= f*cur[k,j]
    return True

d = json.load(open('X_C017_certificate.json'))
x0 = [None]*(3*n)
for ei,(a,b) in enumerate(ent):
    x0[ei] = R(d['G'][a][b]); x0[n+ei] = R(d['A'][a][b]); x0[2*n+ei] = R(d['B'][a][b])
print("stored certificate: max |L p| = %s" % max(abs(t) for t in Lm*sp.Matrix(x0)))

D0 = 2**GRID
x = [R(int(sp.floor(q*D0 + R(1,2))), D0) for q in x0]
for k, cols in enumerate(piv):
    jb = max(cols, key=lambda j: abs(x[j]))
    s = sum((Lm[k,j]*x[j] for j in range(3*n) if j != jb and Lm[k,j] != 0), sp.Integer(0))
    x[jb] = R(R(-s)/R(Lm[k,jb]))

assert all(t == 0 for t in Lm*sp.Matrix(x)), "identity L p = 0 failed"
Gm = sp.zeros(m+1); Am = sp.zeros(m+1); Bm = sp.zeros(m+1)
for ei,(a,b) in enumerate(ent):
    Gm[a,b] = Gm[b,a] = x[ei]; Am[a,b] = Am[b,a] = x[n+ei]; Bm[a,b] = Bm[b,a] = x[2*n+ei]
P = sp.expand(-(G.s_-4)*sp.expand((v(G.s_/S).T*Gm*v(G.s_/S))[0]))
P0 = P.subs(G.s_, 0); Q0 = Am[0,0]
assert P0 > 0 and Q0 > 0 and ldl(Gm) and ldl(Am) and ldl(Bm), "certificate invalid"
dens = float(R(4,3)/sp.sqrt(sp.pi)*R(P0)/R(Q0))
blob = json.dumps({"m":m, "S":S,
    "G":[[str(Gm[i,j]) for j in range(m+1)] for i in range(m+1)],
    "A":[[str(Am[i,j]) for j in range(m+1)] for i in range(m+1)],
    "B":[[str(Bm[i,j]) for j in range(m+1)] for i in range(m+1)],
    "P_over_Q":str(R(P0)/R(Q0)), "density":dens})
json.dump(json.loads(blob), open('X_C017_small.json','w'), indent=1)
print("grid 2^-%d: max digits %d, %d bytes, density %.12f (stored %.12f)"
      % (GRID, max(digits(q) for q in x), len(blob), dens, d['density']))
print("wrote X_C017_small.json")
