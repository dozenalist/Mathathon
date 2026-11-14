#!/usr/bin/env python3
"""The paper's section-1 hexagon upper bound, verified with its actual constants.

The paper (p. 2) reads: "Take Voronoi hexagons of a triangular lattice, each with
circumradius r = 2/5.  Their centers have nearest-neighbor distance sqrt(3) r.
... Distances inside one hexagon are at most 2r < 1.  Centers of distinct
same-color hexagons are at least sqrt(21) r apart, so points in those hexagons
are at least (sqrt(21) - 2) r > 1 apart."

(Checked against the PDF word coordinates on page 2: the line at y=627 carries
"circumradius r = 2/5.", and the radical that a layout extraction prints beside
"lattice" actually belongs to "sqrt(3) r" on the next line at y=641.  So
r = 2/5, not sqrt(2/5).)

H1  r = 2/5 gives 2r = 4/5 < 1.
H2  r = 2/5 gives (sqrt(21) - 2) r > 1.
H3  the index-seven sublattice: |2 - omega|^2 = 7 for omega = e^{2 pi i/3}.
All comparisons are exact rational arithmetic.
"""
from fractions import Fraction as F


def h1():
    r = F(2, 5)
    diam = 2 * r
    inr = 3 * r * r < 1          # inradius^2 = 3r^2/4 < 1/4  <=>  3r^2 < 1
    return diam, diam < 1, inr


def h2():
    # (sqrt21 - 2) r > 1  with r = 2/5  <=>  2 sqrt21 > 9  <=>  84 > 81
    return 4 * 21 > 81


def h3():
    re, im2 = F(5, 2), F(3, 4)
    return re * re + im2, re * re + im2 == 7


if __name__ == "__main__":
    diam, c1, inr = h1()
    print("H1  r = 2/5 : 2r = %s < 1 : %s    inradius^2 = 3r^2/4 < 1/4 : %s"
          % (diam, c1, inr))
    print("H2  (sqrt21-2) r > 1  <=>  2 sqrt21 > 9  <=>  84 > 81 :", h2())
    v, ok = h3()
    print("H3  |2 - omega|^2 =", v, "= 7 :", ok)
    print("H4  Voronoi hexagons cover the plane; boundary points go to an incident")
    print("    hexagon; H1 and H2 keep two same-coloured points away from distance 1.")
    print()
    print("CONCLUSION: the paper's section-1 seven-colouring argument is correct as")
    print("printed, with margins 2r = 0.8 and (sqrt21-2)r = %.6f > 1."
          % (2 * (21 ** 0.5 - 2) / 5))
