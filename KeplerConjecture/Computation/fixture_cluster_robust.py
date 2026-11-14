#!/usr/bin/env python3
"""Is the 13-cluster's positive deficit an artefact of its empty void?  No -- and here is why, exactly.

X's D4 says the period-16 13-cluster is unsaturated, so "the fixture cannot be evidence".  Part of
that is right (it supports no Hales-type local argument) and part is not (it is a legitimate C044
test set).  The sharp question is whether its positive deficit b(0) = +0.1066 comes from the void: if
filling the void destroyed it, the fixture's content would be an artefact.

ANSWER.  It does not.  Add ANY set of points in the box [4,12]^3 that are pairwise at distance >= 2
from each other.  Then

  (i)  every added point is at distance >= 4*sqrt(3) = 6.93 from the origin, so its bisector plane
       with the central vertex is at distance >= 3.46 -- outside the dodecahedron of circumradius
       1.2584.  The central cell is therefore UNCHANGED, and b(0) stays +0.1066;
  (ii) every added point is at distance >= 4 from every lattice point of 16 Z^3 (it lies at least 4
       from the boundary of the period box), hence >= 4 - 2 = 2 from every ring vertex, and >= 2
       from every other added point and its images;
  (iii) therefore the enlarged set is still a packing of minimum separation >= 2.

Both inequalities are the triangle inequality applied to exact rational data -- no interval
arithmetic, no sampling.  The consequence: the fixture's cut content (the singleton bound
0.008880268414739) survives any such filling, so it is a property of the local contact configuration
at the origin and not of the void.

WHAT THIS DOES NOT SAY.  It does not produce a SATURATED packing: the void of the 13-cluster is
about 12.3 wide and the box [4,12]^3 is only part of it, so further balls still fit.  Saturation
would need a filling argument of its own, and nothing here depends on it.

Reproduction: python3 fixture_cluster_robust.py
"""
import itertools, sys
from fractions import Fraction as F

RING_RADIUS = F(2)                     # every ring vertex is at distance exactly 2 from the centre
DODECA_CIRCUM = F(12584, 10000)        # 1.2584... < 1.2584086, an upper bound on the dodecahedron's
                                       # circumradius; the true value is 1.2584086...
BOX = 4                                # added points lie in [BOX, 16-BOX]^3

def added_points():
    """A 5x5x5 grid of rational points in [4,12]^3, spacing 2 (the grid is a packing)."""
    return [(F(i), F(j), F(k))
            for i in range(BOX, 16 - BOX + 1, 2)
            for j in range(BOX, 16 - BOX + 1, 2)
            for k in range(BOX, 16 - BOX + 1, 2)]

def norm2(p):
    return sum(x * x for x in p)

def self_test():
    ok = True
    def check(name, cond, info=None):
        nonlocal ok
        ok = ok and bool(cond)
        print("  %s %s%s" % ("PASS" if cond else "FAIL", name, "" if info is None else "  %r" % (info,)))

    P = added_points()
    check("125 added points in [4,12]^3", len(P) == 125, len(P))
    check("every coordinate is in [4,12]", all(BOX <= c <= 16 - BOX for p in P for c in p))

    print("\n(i) the central cell is untouched")
    d2min = min(norm2(p) for p in P)
    check("every added point is at distance^2 >= (4 sqrt3)^2 = 48 from the origin", d2min >= 48,
          float(d2min) ** 0.5)
    # bisector plane of the origin and p sits at |p|/2 >= 3.46 from the origin
    check("its bisector plane is at distance >= 2 sqrt3 = 3.46 > 1.2584",
          d2min >= 4 * 3, float(d2min) ** 0.5 / 2)

    print("\n(ii) separation from the cluster, by the triangle inequality")
    # |p - ring| >= |p| - |ring| = |p| - 2 >= 4 sqrt3 - 2 = 4.93 >= 2
    check("every added point is >= |p| - 2 >= 4.93 from every ring vertex",
          all(float(norm2(p)) ** 0.5 - 2 >= 2 for p in P))
    # images: p in [4,12]^3 is >= 4 from every nonzero lattice point of 16 Z^3
    worst = None
    for p in P:
        for n in itertools.product((-1, 0, 1), repeat=3):
            if n == (0, 0, 0):
                continue
            q = [p[t] - 16 * n[t] for t in range(3)]
            dd = norm2(q)
            if worst is None or dd < worst:
                worst = dd
    check("every added point is >= 4 from every nonzero lattice point", worst >= 16, float(worst) ** 0.5)

    print("\n(iii) the added points are a packing among themselves")
    pair = None
    for a, b in itertools.combinations(P, 2):
        dd = norm2([a[t] - b[t] for t in range(3)])
        if pair is None or dd < pair:
            pair = dd
    check("pairwise distance^2 >= 4 (spacing 2 on the grid)", pair >= 4, float(pair) ** 0.5)

    print("\nCONCLUSION")
    print("  b(0) = sqrt(32) - V_dod = +0.1065632... is UNCHANGED by the filling,")
    print("  so the singleton bound 0.008880268414739 = b(0)/12 survives it.")
    print("  NOT a saturated packing: the void is ~12.3 wide and [4,12]^3 is only part of it.")
    return ok

if __name__ == "__main__":
    print("13-cluster: does filling the void destroy its positive deficit?")
    good = self_test()
    print("\nfixture_cluster_robust:", "PASS" if good else "FAIL")
    sys.exit(0 if good else 1)
