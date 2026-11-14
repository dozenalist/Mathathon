#!/usr/bin/env python3
"""AUDIT of Main's REPAIRED CUT_FLOW_THEOREM.md (main tip 9d6414d, file repaired at aa52147).

Everything here is written from the theorem's *statement*, not from Main's or C's code.
Three independent objects are compared on the same instances:

  (C)   the cut condition      : for every U subset F, sum_U b <= cap(U).
  LP    direct linear feasibility of {A phi >= b on F, |phi_e| <= Phi_e}
        (scipy HiGHS, floats; only used on small integer data where it is decisive).
  t*    the document's threshold formula (uniform Phi):
              +inf   if some U subset F has delta^+(U) = empty and sum_U b > 0,
              max(0, sup over delta^+(U) != empty of sum_U b/|delta^+(U)|)  else.

Theorem 1 (finite, free boundary) predicts  (C)  <=>  LP feasible  <=>  Phi >= t*(G,b).
Theorem 2 (infinite) is not testable numerically; its hypotheses are audited by reading.

Exit 0 iff every check passes.  Run:  python3 Reviews/audit_cutflow_repair.py
"""
import itertools, sys
from fractions import Fraction as F

def ck(name, cond, detail=""):
    global FAIL
    print("  [%s] %-58s %s" % ("PASS" if cond else "FAIL", name, detail))
    if not cond: FAIL.append(name)
FAIL = []

# ---------------------------------------------------------------- graphs
def edges_of(G):                     # G: list of neighbour lists
    return sorted({(min(u,v), max(u,v)) for u in range(len(G)) for v in G[u]})
def nbrs(G):
    N = {u: set() for u in range(len(G))}
    for u,v in edges_of(G): N[u].add(v); N[v].add(u)
    return N
def delta_plus(G, U):
    S = set(U)
    return [e for e in edges_of(G) if (e[0] in S) != (e[1] in S)]
def cap(G, U, Phi):
    return sum(Phi[e] for e in delta_plus(G, U))
def cut_holds(G, b, Fset, Phi):
    bad = []
    for k in range(1, len(Fset)+1):
        for U in itertools.combinations(sorted(Fset), k):
            if sum(b[v] for v in U) > cap(G, U, Phi): bad.append(U)
    return (not bad), bad
def threshold(G, b, Fset, Phi=1):
    """The document's formula, verbatim, with uniform Phi factored out."""
    sup = F(0); closed_pos = False
    for k in range(1, len(Fset)+1):
        for U in itertools.combinations(sorted(Fset), k):
            s = sum(b[v] for v in U)
            d = len(delta_plus(G, U))
            if d == 0:
                if s > 0: closed_pos = True          # branch 1 -> +infinity
            else:
                sup = max(sup, F(s, d))
    return None if closed_pos else max(F(0), sup)     # None == +infinity

# ---------------------------------------------------------------- direct LP
def lp_feasible(G, b, Fset, Phi):
    import numpy as np
    from scipy.optimize import linprog
    E = [e for e in edges_of(G) if e[0] in Fset or e[1] in Fset]
    if not E: return all(b[v] <= 0 for v in Fset)
    idx = {e:i for i,e in enumerate(E)}
    rows, rhs = [], []
    for v in sorted(Fset):
        row = [0.0]*len(E)
        for e in E:
            if e[1] == v: row[idx[e]] = 1.0        # phi(v,w) with v the second endpoint
            elif e[0] == v: row[idx[e]] = -1.0     # -> use antisymmetry phi(v,w) = -phi(w,v)
        rows.append([-x for x in row]); rhs.append(-float(b[v]))   # -A phi <= -b
    caps = [float(Phi[e]) for e in E]
    r = linprog([0.0]*len(E), A_ub=np.array(rows), b_ub=np.array(rhs),
                bounds=[(-c, c) for c in caps], method="highs")
    return r.status == 0

# ---------------------------------------------------------------- graphs used
def star(k):
    G = [[1,2,3][:k]] + [[0] for _ in range(k)] if k == 3 else None
    # centre 0, leaves 1..k
    G = [[] for _ in range(k+1)]
    for i in range(1, k+1): G[0].append(i); G[i].append(0)
    return G
def path(n):
    G = [[] for _ in range(n)]
    for i in range(n-1): G[i].append(i+1); G[i+1].append(i)
    return G
def two_edges():                      # two disjoint single edges: 0-1 and 2-3
    return [[1],[0],[3],[2]]

print("="*86); print("A. Regression witnesses W1-W6 (W6 restated: my REVIEW_0353 row was wrong)"); print("="*86)
S3 = star(3)
cases = [
 ("W1 star b=(3,-1,-1,-1) F=V, Phi=1",      S3, [3,-1,-1,-1], {0,1,2,3}, 1, True,  F(1)),
 ("W1' same at Phi=0",                      S3, [3,-1,-1,-1], {0,1,2,3}, 0, False, F(1)),
 ("W2 star b=(4,-1,-1,-1) F=V, Phi=1e6",    S3, [4,-1,-1,-1], {0,1,2,3}, 10**6, False, None),
 ("W2' same at Phi=0",                      S3, [4,-1,-1,-1], {0,1,2,3}, 0, False, None),
 ("W3 star b=(4,-1,-1,-1) F={a}, Phi=4/3",  S3, [4,-1,-1,-1], {0},   F(4,3), True,  F(4,3)),
 ("W3' same at Phi=1",                      S3, [4,-1,-1,-1], {0},   F(1),   False, F(4,3)),
 ("W4 path4 b=(1,0,0,-1) Phi=1",            path(4), [1,0,0,-1], {0,1,2,3}, 1, True, F(1)),
 ("W5 single edge b=(1,-1) Phi=1/2",        path(2), [1,-1], {0,1}, F(1,2), False, F(1)),
 ("W6 two edges b=(1,-1)|(2,-2) Phi=2",     two_edges(), [1,-1,2,-2], {0,1,2,3}, 2, True,  F(2)),
 ("W6' same at Phi=3/2",                    two_edges(), [1,-1,2,-2], {0,1,2,3}, F(3,2), False, F(2)),
]
for name, G, b, Fset, Phi, want_feas, want_t in cases:
    uPhi = {e: F(Phi) for e in edges_of(G)}
    ok, bad = cut_holds(G, b, Fset, uPhi)
    lp = lp_feasible(G, b, Fset, uPhi)
    t  = threshold(G, b, Fset)
    good = (ok == want_feas == lp) and (t == want_t)
    ck(name, good, "C=%s LP=%s t*=%s (want C=%s t*=%s)" % (ok, lp, "inf" if t is None else t, want_feas, want_t))

print("="*86); print("B. The two threshold branches on ONE instance (Main's 'try to break' request)"); print("="*86)
# isolated vertex 0 with b=+1, disjoint star 1<-2,3,4 with b=(4,-4/3,-4/3,-4/3)
G = [[] for _ in range(5)]
G[1] = [2,3,4]
for i in (2,3,4): G[i] = [1]
G[0] = []
b = [1, 4, F(-4,3), F(-4,3), F(-4,3)]
t = threshold(G, b, {0,1,2,3,4})
ck("isolated +1 component forces t*=+inf", t is None, "t*=%s" % ("inf" if t is None else t))
ok, bad = cut_holds(G, b, {0,1,2,3,4}, {e: F(10**6) for e in edges_of(G)})
ck("and (C) fails at Phi=1e6 (branch 1 is capacity-free)", (not ok) and (0,) in bad,
   "violating U=%s" % (bad[:1],))
# the finite branch alone would have said 4/3: report it
print("        finite-branch sup alone = 4/3; answer is +inf, so both branches are needed.")
# max(0,.) branch: everything negative
G2, b2 = path(2), [-1, -2]
ck("all-negative b: t*=0 (max(0,.) is needed)", threshold(G2, b2, {0,1}) == 0,
   "t*=%s" % threshold(G2, b2, {0,1}))
ck("all-negative b: feasible at Phi=0", cut_holds(G2, b2, {0,1}, {e: F(0) for e in edges_of(G2)})[0])

print("="*86); print("C. Section 5 worked examples, recomputed from the formula"); print("="*86)
ex = [("5(a) b=(1,-1/3,-1/3,-1/3) F=V", S3, [1,F(-1,3),F(-1,3),F(-1,3)], {0,1,2,3}, F(1,3)),
      ("5(b') b=(4,-4/3,-4/3,-4/3) F=V", S3, [4,F(-4,3),F(-4,3),F(-4,3)], {0,1,2,3}, F(4,3)),
      ("5(c) path4 b=(1,0,0,-1)", path(4), [1,0,0,-1], {0,1,2,3}, F(1))]
for name, G, b, Fset, want in ex:
    t = threshold(G, b, Fset)
    ok, _ = cut_holds(G, b, Fset, {e: want for e in edges_of(G)})
    ok2, _ = cut_holds(G, b, Fset, {e: want - F(1,1000) for e in edges_of(G)})
    ck(name, t == want and ok and not ok2, "t*=%s (want %s); tight: fails just below" % (t, want))

print("="*86); print("D. Randomised cross-check: (C) <=> LP <=> Phi >= t*"); print("="*86)
import random
random.seed(20261114)
bad_n = 0; n = 0
for trial in range(120):
    k = random.choice([3,4,5,6])
    G = [[] for _ in range(k)]
    for i, j in itertools.combinations(range(k), 2):
        if random.random() < 0.45: G[i].append(j); G[j].append(i)
    b = [random.randint(-2, 2) for _ in range(k)]
    Fset = set(range(k)) if random.random() < 0.6 else {i for i in range(k) if random.random() < 0.6}
    if not Fset: continue
    Phi = random.choice([0, 1, 2, 3])
    uPhi = {e: F(Phi) for e in edges_of(G)}
    ok, _ = cut_holds(G, b, Fset, uPhi)
    lp = lp_feasible(G, b, Fset, uPhi)
    t = threshold(G, b, Fset)
    pred = (t is not None) and (F(Phi) >= t)
    n += 1
    if not (ok == lp == pred):
        bad_n += 1
        print("    mismatch:", G, b, sorted(Fset), Phi, "C=%s LP=%s pred=%s t*=%s" % (ok, lp, pred, t))
ck("120 random instances: C == LP == (Phi >= t*)", bad_n == 0, "%d/%d mismatches" % (bad_n, n))


# ---------------------------------------------------------------- exact feasibility (no floats)
def fm_feasible(G, b, Fset, Phi, cap_cons=3000):
    """Decide {A phi >= b on F, |phi_e| <= Phi_e} in EXACT rational arithmetic by
    Fourier-Motzkin elimination.  No LP solver, no tolerance, no float anywhere.

    A constraint is (coeffs: dict var->Fraction, rhs: Fraction), meaning
        sum coeffs[i]*x_i >= rhs .
    The variable to eliminate is chosen to minimise |pos|*|neg| (a min-cost order keeps the
    constraint count from exploding; with a fixed order n = 6 ran out of memory).  None means
    "undecided" (the blow-up guard fired), and callers must skip it rather than count it.
    """
    E = [e for e in edges_of(G) if e[0] in Fset or e[1] in Fset]
    if not E:
        return all(b[v] <= 0 for v in Fset)
    cons = []
    for v in sorted(Fset):                       # div_phi(v) >= b(v),  x_e = phi(e0,e1)
        d = {e: (F(1) if e[0] == v else F(-1)) for e in E if v in e}
        cons.append((d, F(b[v])))
    for e in E:                                  # -Phi <= x <= Phi
        cons.append(({e: F(1)}, -F(Phi[e])))
        cons.append(({e: F(-1)}, -F(Phi[e])))
    left = set(E)
    while left:
        best = None
        for k in left:
            npos = sum(1 for (c, _) in cons if c.get(k, F(0)) > 0)
            nneg = sum(1 for (c, _) in cons if c.get(k, F(0)) < 0)
            if best is None or npos*nneg < best[0]: best = (npos*nneg, k)
        _, k = best
        pos = [(c, r) for (c, r) in cons if c.get(k, F(0)) > 0]
        neg = [(c, r) for (c, r) in cons if c.get(k, F(0)) < 0]
        newc = [(c, r) for (c, r) in cons if c.get(k, F(0)) == 0]
        for (cp, rp) in pos:
            ap = cp[k]
            for (cn, rn) in neg:
                bn = cn[k]
                r = (-bn)*rp + ap*rn          # (-b)(a x + P >= A) + a(b x + Q >= B)
                c = {}                        #   =>  (-b)P + aQ >= (-b)A + aB
                for i in set(cp) | set(cn):
                    if i == k: continue
                    val = (-bn)*cp.get(i, F(0)) + ap*cn.get(i, F(0))
                    if val != 0: c[i] = val
                if not c:
                    if r > 0: return False    # unconditional contradiction
                else:
                    newc.append((c, r))
                if len(newc) > cap_cons: return None
        cons = newc
        left.discard(k)
    return all(r <= 0 for (c, r) in cons)

print("="*86); print("E. The same instances, decided in exact arithmetic (Fourier-Motzkin)"); print("="*86)
bad_n, n, und = 0, 0, 0
for trial in range(300):
    k = random.choice([3,4,5,6])
    G = [[] for _ in range(k)]
    for i, j in itertools.combinations(range(k), 2):
        if random.random() < 0.45: G[i].append(j); G[j].append(i)
    b = [random.randint(-2, 2) for _ in range(k)]
    Fset = set(range(k)) if random.random() < 0.6 else {i for i in range(k) if random.random() < 0.6}
    if not Fset: continue
    Phi = random.choice([0, 1, 2, 3])
    uPhi = {e: F(Phi) for e in edges_of(G)}
    ok, _ = cut_holds(G, b, Fset, uPhi)
    ex = fm_feasible(G, b, Fset, uPhi)
    if ex is None: und += 1; continue
    n += 1
    if ok != ex:
        bad_n += 1
        print("    mismatch:", G, b, sorted(Fset), Phi, "cut=%s FM=%s" % (ok, ex))
ck("300 random instances (n<=6): exact FM == cut condition", bad_n == 0,
   "%d/%d mismatches, %d undecided (guard)" % (bad_n, n, und))

print("="*86)
print("RESULT:", "ALL PASS" if not FAIL else "FAILURES: %s" % FAIL)
sys.exit(0 if not FAIL else 1)
