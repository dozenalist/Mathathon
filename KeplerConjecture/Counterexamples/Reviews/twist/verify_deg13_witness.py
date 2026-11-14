#!/usr/bin/env python3
"""K15-X-C083: check the 17-neighbour witness in exact rational arithmetic.

Claim: there are 17 rational points q with |q - q'| >= 2 for q != q', |q| <= 2 + 0.6832816 < 2.684,
and |q| >= 2.  With the origin, the set is 2-separated and the origin has 17 neighbours within 2+eps,
so the degree in the (2+eps)-graph is at least 17, not <= 12.
"""
import itertools
import json
import sys
from fractions import Fraction as F

EPS = F(6832816, 10 ** 7)
LIM = 2 + EPS


def main():
    pts = [tuple(F(x) for x in q) for q in json.load(open("deg13_witness.json"))]
    n = len(pts)
    d2 = [sum((a[t] - b[t]) ** 2 for t in range(3)) for a, b in itertools.combinations(pts, 2)]
    r2 = [sum(x * x for x in q) for q in pts]
    print(f"points: {n}")
    print(f"min squared distance between them : {float(min(d2)):.6f}  (need >= 4)")
    print(f"max |q|                           : {float(max(r2)) ** 0.5:.10f}  (need <= {float(LIM):.7f})")
    print(f"min |q|                           : {float(min(r2)) ** 0.5:.10f}  (need >= 2)")
    ok = (n >= 13) and min(d2) >= 4 and max(r2) <= LIM * LIM and min(r2) >= 4
    print(f"\ndegree of the origin in the (2+eps)-graph is {n} >= 13: {ok}")
    print("so `deg <= 12` in the (2+eps)-graph is FALSE at eps = 0.6832816")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
