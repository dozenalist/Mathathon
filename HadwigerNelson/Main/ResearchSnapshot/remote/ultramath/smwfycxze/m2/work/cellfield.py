#!/usr/bin/env python3
"""
d2: an EXACT measurable palette field at a k = 6 centre carrying an interface 5-cycle, in which
the outsider label X = 5 is allowed in the palette.

Construction.  Discretise the direction circle into 360 cells of 1 degree.  The field is
constant on each cell.  Since (5.7) links theta with theta + 60 and 60 is a whole number of
cells, the constraint set splits into 60 independent six-cell problems
{j, j+60, j+120, j+180, j+240, j+300}.  The sign pattern Q(theta) is constant on the true arcs
cut out by beta_j +- 90; with beta_j chosen on the 18-degree lattice those arcs are unions of
cells, so a cell-constant field that is admissible on every cell is admissible almost
everywhere.  Hence any SAT instance below yields a genuine measurable palette field.

Constraints per cell: (8.1) P meets I(Q), O(Q);  |P| <= 3;  (6.2);  P avoids the chosen label.
Constraints between consecutive cells of an orbit: (5.7) disjointness.
Reported for the whole field: the number of distinct values (>= 3 defeats Lemma 6.4, which
only forbids a two-valued singleton/pair state function), and m11's sigma{T subset P} <= 1/2.
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

def cos_pos(tdeg, bdeg):
    d = (F(tdeg) - F(bdeg)) % 360
    return d < 90 or d > 270

def pattern(tdeg, betas):
    return frozenset(j for j in range(len(betas)) if cos_pos(tdeg, betas[j]))

def options(Q, k=6, b=3, absence=frozenset(), use62=True):
    I, O = allowed(Q, k)
    out = []
    for c in range(1, b + 1):
        for cand in itertools.combinations(range(k), c):
            P = frozenset(cand)
            if not (P & I and P & O): continue
            if P & absence: continue
            if use62 and any(P <= frozenset({j, (j + 1) % ELL}) for j in range(ELL)): continue
            out.append(P)
    return out

def build(betas, k=6, absence=frozenset(), use62=True, prefer_rich=True):
    pats = [pattern(F(j) + F(1, 2), betas) for j in range(360)]
    opts = [options(p, k, 3, absence, use62) for p in pats]
    if any(not o for o in opts):
        return None, None, None
    field = [None] * 360
    for r in range(60):
        orb = [r + 60 * t for t in range(6)]
        sol = []
        ok = [False]
        def dfs(i):
            if ok[0]: return
            if i == 6:
                ok[0] = True
                for t in range(6):
                    field[orb[t]] = sol[t]
                return
            cands = opts[orb[i]]
            if prefer_rich:
                cands = sorted(cands, key=lambda P: (-len(P), sorted(P)))
            for P in cands:
                if sol and (P & sol[-1]): continue
                if i == 5 and (P & sol[0]): continue
                sol.append(P); dfs(i + 1); sol.pop()
        dfs(0)
        if not ok[0]:
            return None, pats, opts
    return field, pats, opts

def report(betas, name, absence=frozenset()):
    print(f"\n=== {name};  betas = {[str(b) for b in betas]};  absent labels {sorted(absence)}")
    field, pats, opts = build(betas, absence=absence)
    if field is None:
        print("    UNSAT for the 1-degree cell model")
        return None
    # verify everything exactly
    for j in range(360):
        I, O = allowed(pats[j], 6)
        P = field[j]
        assert P & I and P & O, ("(8.1)", j, sorted(P), sorted(pats[j]))
        assert 1 <= len(P) <= 3, ("|P|<=3", j)
        assert not (P & absence), ("avoid", j)
        assert not any(P <= frozenset({x, (x + 1) % ELL}) for x in range(ELL)), ("(6.2)", j)
        assert not (P & field[(j + 60) % 360]), ("(5.7)", j)
    vals = sorted({P for P in field}, key=lambda P: (len(P), sorted(P)))
    print(f"    SAT.  distinct palette values: {len(vals)} -> {[sorted(v) for v in vals]}")
    print(f"    (8.1), (5.7), (6.2), |P|<=3, avoidance of {sorted(absence)}: verified on all 360 cells")
    # m11
    worst = (F(0), None)
    for t in range(1, 4):
        for T in itertools.combinations(range(6), t):
            T = frozenset(T)
            meas = sum(1 for j in range(360) if T <= field[j])
            if meas > worst[0]:
                worst = (F(meas, 360), T)
            assert meas * 2 <= 360, ("m11 VIOLATED", sorted(T), meas)
    print(f"    m11  sigma{{T subset P}} <= 1/2 : maximal value {float(worst[0]):.4f} at T={sorted(worst[1])}")
    # how much of the circle has X in the palette
    nX = sum(1 for j in range(360) if 5 in field[j])
    print(f"    sigma{{X in P}} = {nX}/360 = {float(F(nX,360)):.4f}"
          f"   (Theorem A requires >= 1/6 = 0.1667, (5.7) requires <= 1/2)")
    # is it a two-valued state function?  (Lemma 6.4 only kills those)
    print(f"    two-valued state function (Lemma 6.4): {'YES -- KILLED' if len(vals) <= 2 else 'no'}")
    return field

if __name__ == "__main__":
    # pentagon geometry: arcs are multiples of 18 degrees
    pent = [F(18), F(90), F(162), F(234), F(306)]     # beta_j = 18 + 72 j
    report(pent, "pentagon lattice geometry", absence=frozenset())
    report(pent, "pentagon lattice geometry, cycle label 0 absent", absence=frozenset({0}))
    report(pent, "pentagon lattice geometry, outsider 5 absent", absence=frozenset({5}))
    # a second geometry on the 18-degree lattice
    g2 = [F(0), F(72), F(144), F(216), F(288)]
    report(g2, "shifted pentagon (18-degree lattice)", absence=frozenset())
    g3 = [F(18), F(54), F(90), F(126), F(270)]
    report(g3, "irregular 18-degree lattice geometry", absence=frozenset())
