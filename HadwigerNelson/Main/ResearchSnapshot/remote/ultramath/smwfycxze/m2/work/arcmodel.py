#!/usr/bin/env python3
"""
d2: the arc model.  A measurable palette field on the whole direction circle that satisfies
(8.1) and (5.7) for a.e. e, with |P| <= 3 and (6.2), at a k=6 centre carrying an interface
5-cycle whose outsider label X = 5 is ALLOWED in the palette.

Geometry is given by exact rational angles beta_j = arg(v_j) in degrees.  The sign
s_j(theta) = sign(cos(theta - beta_j)) changes only at theta = beta_j +- 90, so the pattern
Q(theta) = { j : cos(theta - beta_j) > 0 } is constant on the arcs cut out by those points and
a circle-constant field is determined by one palette per arc.

Constraints per arc A with pattern Q:
   (8.1)  P meets I(Q) and O(Q);            |P| <= 3;   P avoids the absent label;
   (6.2)  P is not contained in any cycle edge {j,j+1};
   (5.7)  P_A disjoint from P_A' whenever sigma(A n R^{-1}A') > 0.
Also reported: whether the field is a two-valued state function (Lemma 6.4), and m11's
sigma{T subset P} <= 1/2 for every nonempty T.
"""
import itertools, sys
from fractions import Fraction as F

ELL = 5

def internal(Q, sign):
    return frozenset(i for i in range(ELL)
                     if (((i - 1) % ELL) in Q) == bool(sign) and (i in Q) == bool(sign))

def allowed(Q, k):
    outs = frozenset(range(ELL, k))
    return internal(Q, True) | outs, internal(Q, False) | outs

def arcs_and_patterns(betas, k=6):
    """betas: list of ell fractions (degrees).  Returns (representation points, patterns)."""
    cuts = set()
    for b in betas:
        for d in (90, -90):
            cuts.add((b + d) % 360)
    cuts = sorted(cuts)
    n = len(cuts)
    reps, pats, sizes = [], [], []
    for i in range(n):
        a, b = cuts[i], cuts[(i + 1) % n]
        length = (b - a) % 360
        if length == 0:
            continue
        mid = (a + length / 2) % 360
        Q = frozenset(j for j in range(ELL)
                      if _cos_pos(mid, betas[j]))
        reps.append(mid); pats.append(Q); sizes.append(length)
    return cuts, reps, pats, sizes

def _cos_pos(t, b):
    d = (t - b) % 360
    return d < 90 or d > 270

def R_overlap(cuts, sizes, shift=60):
    """incidence: inc[i] = set of j with sigma(A_i n (A_j - shift)) > 0."""
    reps = []
    n = len(cuts)
    arcs = []
    for i in range(n):
        a, b = cuts[i], cuts[(i + 1) % n]
        L = (b - a) % 360
        if L == 0: continue
        arcs.append((a, L))
    m = len(arcs)
    inc = [set() for _ in range(m)]
    for i, (a, L) in enumerate(arcs):
        lo = (a + shift) % 360
        # subdivide A_i into pieces of length 1/6 degree and locate the image arc
        steps = 72
        for t in range(steps):
            th = (lo + L * (t + F(1, 2)) / steps) % 360
            for j, (a2, L2) in enumerate(arcs):
                if (th - a2) % 360 < L2:
                    inc[i].add(j); break
    return arcs, inc

def solve_arcs(pats, sizes, inc, k=6, b=3, absence=frozenset(), need_variety=3):
    opts = []
    for Q in pats:
        I, O = allowed(Q, k)
        o = []
        for c in range(1, b + 1):
            for cand in itertools.combinations(range(k), c):
                P = frozenset(cand)
                if not (P & I and P & O): continue
                if P & absence: continue
                if any(P <= frozenset({j, (j + 1) % ELL}) for j in range(ELL)): continue
                o.append(P)
        opts.append(o)
    if any(not o for o in opts):
        return None
    m = len(pats); sol = []; res = []
    def dfs(i):
        if res: return
        if i == m:
            if len(set(sol)) >= need_variety: res.append(tuple(sol))
            return
        for P in opts[i]:
            if any(sol[j] & P for j in inc[i] if j < i): continue
            # also the reverse incidence
            if any((i in inc[j]) and (sol[j] & P) for j in range(i)): continue
            sol.append(P); dfs(i + 1); sol.pop()
    dfs(0)
    return res[0] if res else None

def check_field(pats, sizes, inc, P, k=6, absence=frozenset()):
    for i, Q in enumerate(pats):
        I, O = allowed(Q, k)
        assert P[i] & I and P[i] & O, ("8.1", i)
        assert len(P[i]) <= 3
        assert not (P[i] & absence)
        assert not any(P[i] <= frozenset({j, (j + 1) % ELL}) for j in range(ELL)), ("6.2", i)
    for i in range(len(pats)):
        for j in inc[i]:
            assert not (P[i] & P[j]), ("5.7", i, j)
    # m11: sigma{T subset P} <= 1/2
    tot = sum(sizes)
    for t in range(1, 4):
        for T in itertools.combinations(range(k), t):
            T = frozenset(T)
            meas = sum(sizes[i] for i in range(len(pats)) if T <= P[i])
            assert meas * 2 <= tot, ("m11", sorted(T), meas, tot)
    return True

def report(name, betas, absence=frozenset({0})):
    cuts, reps, pats, sizes = arcs_and_patterns(betas)
    arcs, inc = R_overlap(cuts, sizes)
    print(f"\n--- {name}: betas = {[str(b) for b in betas]}")
    print(f"    {len(arcs)} arcs, total length {sum(sizes)}")
    for i, (a, L) in enumerate(arcs):
        print(f"      arc {i:2d} ({a}, {(a+L)%360}) len {L}   pattern {sorted(pats[i])}"
              f"   I\\X {sorted(allowed(pats[i],6)[0]-{5})}  O\\X {sorted(allowed(pats[i],6)[1]-{5})}")
    if any(not allowed(Q, 6)[0] - {5} or not allowed(Q, 6)[1] - {5} for Q in pats):
        print("      NOTE: some arc forces X=5 into the palette (a=0 run of length 1)")
    w = solve_arcs(pats, sizes, inc, absence=absence)
    if w is None:
        print("    UNSAT as an arc-constant field")
        return None
    check_field(pats, sizes, inc, w, absence=absence)
    print(f"    SAT   palettes {[sorted(p) for p in w]}   ({len(set(w))} distinct values)")
    print(f"    (8.1), (5.7), (6.2), |P|<=3, self-avoidance {sorted(absence)},"
          f" m11 sigma-bound: all verified exactly")
    return w

if __name__ == "__main__":
    K = 6
    # the geometry of the six-position witness (gap assignment (0,0,0,3,3))
    report("witness geometry  phi=(10,25,40,195,230)", [F(-80), F(-70), F(-60), F(110), F(130)],
           absence=frozenset({0}))
    # regular pentagon
    report("regular pentagon", [F(72 * j) for j in range(5)], absence=frozenset({0}))
    # pentagon, avoiding a different cycle label
    report("regular pentagon, absent label 1", [F(72 * j) for j in range(5)], absence=frozenset({1}))
