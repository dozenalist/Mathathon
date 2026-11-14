#!/usr/bin/env python3
"""Exact certificate: the density 1/2 of three-label palettes survives the
two-centre translation exclusion on a seven-centre configuration.

Centres.  x, and y_e = x + exp(i e pi/3) for e = 0..5.  Directions are the six
elements f = 0..5 of one R-orbit, R = rotation by pi/3.

Palettes are bitmasks over labels 0..5.  The certificate checks:

  (C1) nonemptiness and the palette bound |P| <= 3 at k = 6
  (C2) (5.7)-type 60-degree exclusion at every centre: P(c,f) & P(c,f+1) == 0
  (C3) (5.2) union constraint at every centre: P(c,f) | P(c,g) != full
  (C4) two-centre translation exclusion (Remark 5.3) for every pair of centres
       at Euclidean distance exactly one: P(c,f) & P(c',f) == 0 for all f
       -- x is at distance 1 from every y_e; y_e from y_{e+-1} (|e^{i} - 1| = 1)
       -- y_e from y_{e+-2} at distance sqrt(3), y_e from y_{e+3} at distance 2:
          not unit, hence no constraint.

Geometry is checked in exact arithmetic over Z[sqrt 3]: the squared distance
between exp(ia pi/3) and exp(ib pi/3) is 2 - 2 cos((a-b) pi/3), an integer.
"""
import itertools


def popcount(m):
    return bin(m).count("1")


FULL = (1 << 6) - 1
T = 0b000111          # labels {0,1,2}

# palette[c][f]; c = 0 is x, c = 1..6 are y_0..y_5
P = {}
for f in range(6):
    P[(0, f)] = T if f % 2 == 0 else 0b001000          # T or {3}
for e in range(6):
    c = e + 1
    for f in range(6):
        if f % 2 == 0:
            P[(c, f)] = 0b001000 if e % 2 == 0 else 0b010000   # {3} or {4}
        else:
            P[(c, f)] = 0b000001 if e % 2 == 0 else 0b000010   # {0} or {1}


def sq_dist_dir(a, b):
    """Exact squared distance |exp(ia pi/3) - exp(ib pi/3)|^2 in Z[sqrt3] (an int)."""
    from fractions import Fraction
    # 2 - 2 cos((a-b) pi/3); cos is one of 1, 1/2, -1/2, -1
    d = (a - b) % 6
    cos = {0: Fraction(1), 1: Fraction(1, 2), 2: Fraction(-1, 2), 3: Fraction(-1),
           4: Fraction(-1, 2), 5: Fraction(1, 2)}[d]
    v = 2 - 2 * cos
    assert v.denominator == 1
    return int(v)


def centre_dist(c, c2):
    """Exact squared distance between centres c, c2 (0 = x, e+1 = y_e)."""
    if c == 0 and c2 == 0:
        return 0
    if c == 0 or c2 == 0:
        return 1                      # |x - y_e| = 1
    return sq_dist_dir(c - 1, c2 - 1)


def main():
    centres = range(7)
    fails = []

    # (C1)
    for c in centres:
        for f in range(6):
            m = P[(c, f)]
            if not (1 <= popcount(m) <= 3):
                fails.append(("C1", c, f, bin(m)))

    # (C2) 60-degree exclusion
    for c in centres:
        for f in range(6):
            if P[(c, f)] & P[(c, (f + 1) % 6)]:
                fails.append(("C2", c, f))

    # (C3) union constraint
    for c in centres:
        for f in range(6):
            for g in range(6):
                if (P[(c, f)] | P[(c, g)]) == FULL:
                    fails.append(("C3", c, f, g))

    # (C4) two-centre translation exclusion at unit-separated pairs
    unit_pairs = [(c, c2) for c, c2 in itertools.product(centres, repeat=2)
                  if c < c2 and centre_dist(c, c2) == 1]
    for (c, c2) in unit_pairs:
        for f in range(6):
            if P[(c, f)] & P[(c2, f)]:
                fails.append(("C4", c, c2, f))

    heavy = sum(1 for f in range(6) if popcount(P[(0, f)]) == 3)
    print("unit-separated centre pairs:", unit_pairs)
    print("heavy directions at x:", heavy, "of 6  (ratio %d/6)" % heavy)
    print("palette at x:", [bin(P[(0, f)]) for f in range(6)])
    if fails:
        print("FAIL", fails[:10])
        raise SystemExit(1)
    print("ALL CONSTRAINTS PASS")
    # also report that the triangle (6.2) condition can be imposed: T = {0,1,2}
    # is contained in no edge of the triangle, {3} is not contained in an edge
    # of the 3-cycle on {0,1,2}; check for completeness
    cyc_edges = [(0, 1), (1, 2), (0, 2)]
    ok = True
    for f in range(6):
        S = {i for i in range(6) if P[(0, f)] >> i & 1}
        for (a, b) in cyc_edges:
            if S <= {a, b}:
                ok = False
    print("(6.2) satisfied at x for the triangle cycle on {0,1,2}:", ok)


if __name__ == "__main__":
    main()
