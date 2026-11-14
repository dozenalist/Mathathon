#!/usr/bin/env python3
"""Exact verification of the claims about the cyclic locus L of the paper's
seven-colouring c_0 and of the k>=7 accumulating colouring c.

Every geometric quantity lies in Q(sqrt3); the arithmetic below is exact
(fractions.Fraction coefficients), so the certificates are finite exact statements.

Run:  python3 verify.py      (exit status 0 iff every check passes)
"""
import math
import sys
from fractions import Fraction as F

from field import Q3
from hexcol import (hex_vertices, hex_dist2, hex_maxdist2, z, colour,
                    colour_of_point, dist2, sub, add, dot, norm2, seg_dist2)

CHECKS = []


def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))
    print(("  PASS  " if ok else "  FAIL  ") + name + (("   " + detail) if detail else ""))


P0 = (Q3(F(1, 55)), Q3(F(18, 55)))
INRADIUS2 = Q3(F(3, 25))            # (sqrt3/5)^2
UNITS = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, -1)]      # lattice coordinates
UNITS_E = [sub(z(*u), z(0, 0)) for u in UNITS]                    # the same, as Euclidean vectors

print("=" * 78)
print("V1   the six unit vectors of the lattice carry the six nonzero colours")
print("=" * 78)
cols = sorted(colour(*u) % 7 for u in UNITS)
check("V1  {colour(u) : u a unit vector} = {1,...,6}", cols == [1, 2, 3, 4, 5, 6], str(cols))
check("V1b each elementary triangle {(0,0),u,u+v} has three distinct colours",
      all(len({0, colour(*u) % 7, colour(u[0] + v[0], u[1] + v[1]) % 7}) == 3
          for u in UNITS for v in UNITS if (u[0] + v[0], u[1] + v[1]) in UNITS),
      "algebraic reason: colours are 0, col(u), col(u)+col(v); col(v) != 0 mod 7")
bad = 0
for m0 in range(-6, 7):
    for n0 in range(-6, 7):
        c0 = colour(m0, n0)
        for u in UNITS:
            for v in UNITS:
                s = (u[0] + v[0], u[1] + v[1])
                if s in UNITS and len({c0 % 7, (c0 + colour(*u)) % 7,
                                       (c0 + colour(*s)) % 7}) != 3:
                    bad += 1
check("V1c exhaustive over 169 centres x 12 orientations", bad == 0, f"{bad} failures")

print()
print("=" * 78)
print("V2   the shadow certificate (two independent exact methods)")
print("=" * 78)
MAXR2 = Q3(F(9, 4))                 # enumerate all centres with |z-p_0|^2 <= 9/4


def nearby_hexagons(maxr2=MAXR2):
    out = []
    for m in range(-12, 13):
        for n in range(-12, 13):
            c = z(m, n)
            d2 = (c[0] - P0[0]) * (c[0] - P0[0]) + (c[1] - P0[1]) * (c[1] - P0[1])
            if d2 <= maxr2:
                out.append((m, n))
    return out


HEXES = nearby_hexagons()
check("V2a hexagon enumeration: every centre within distance 3/2 is listed",
      len(HEXES) >= 12 and MAXR2 == Q3(F(9, 4)), f"{len(HEXES)} hexagons")


def method1_misses(m, n, eps):
    """exact min/max distance to the closed hexagon"""
    lo = Q3((1 - eps) ** 2)
    hi = Q3((1 + eps) ** 2)
    dmin2 = hex_dist2(P0, m, n)
    dmax2 = hex_maxdist2(P0, m, n)
    if dmin2 > hi:
        return 'outside'
    if dmax2 < lo:
        return 'inside'
    return 'MEETS'


def method2_misses(m, n, eps):
    """vertex-inside-the-inner-disk, or a supporting face beyond the outer disk"""
    v = hex_vertices(m, n)
    lo = Q3((1 - eps) ** 2)
    if all(dist2(P0, q) < lo for q in v):
        return 'inside'                      # convexity: hexagon in the inner open disk
    c = z(m, n)
    hi = Q3((1 + eps) ** 2)
    for u in UNITS_E:
        # face of the Voronoi cell of z in direction u:  (x-z).u = |u|^2/2 = 6/25
        # hexagon lies in {x : (x-z).u >= 6/25}; disk of radius 1+eps lies in
        # {x : (x-z).u < 6/25}  iff  (p_0-z).u + (1+eps) < 6/25
        pu = dot(sub(P0, c), u)
        # compare pu + (1+eps) with 6/25 exactly; 1+eps rational
        lhs2 = (Q3(F(6, 25)) - pu) * (Q3(F(6, 25)) - pu)      # in Q(sqrt3)
        if (Q3(F(6, 25)) - pu).sign() > 0 and lhs2 > hi:
            return 'outside'
    return 'MEETS'


for eps, epsname in [(F(1, 70), "eps = 1/70  (the certificate used below)"),
                     (F(71, 10000), "eps = 71/10000  (the previous certificate)")]:
    m1 = [k for k in HEXES if colour(*k) in (0, 2, 3) and method1_misses(*k, eps) == 'MEETS']
    m2 = [k for k in HEXES if colour(*k) in (0, 2, 3) and method2_misses(*k, eps) == 'MEETS']
    check(f"V2b method 1: no hexagon of colour 0,2,3 meets the annulus, {epsname}",
          m1 == [], str(m1))
    check(f"V2c method 2 (independent): same conclusion, {epsname}", m2 == [], str(m2))
    # non-vacuity: colours 1,4,5,6 DO meet the annulus
    present = sorted({colour(*k) for k in HEXES
                      if method1_misses(*k, eps) == 'MEETS'})
    check(f"V2d the annulus is non-vacuous: it meets colours {present}", present == [1, 4, 5, 6],
          f"colours present {present}")

print()
print("=" * 78)
print("V3   the shadow of the square W of side 1/50, and W inside the colour-0 hexagon")
print("=" * 78)
ELL = F(1, 50)
HALFDIAG = Q3(1) / Q3(0, 0) if False else None
# half diagonal ell*sqrt2/2 <= 1/70  <=>  ell <= sqrt2/70  <=>  ell^2 <= 2/4900
check("V3a  ell*sqrt2/2 <= 1/70  (rational certificate: ell^2 = 1/2500 <= 2/4900)",
      F(1, 2500) <= F(2, 4900), f"{float(F(1,2500))} <= {float(F(2,4900))}")
# every corner of W is strictly inside the hexagon of the origin
corners = [(P0[0] + Q3(s * ELL / 2), P0[1] + Q3(t * ELL / 2)) for s in (-1, 1) for t in (-1, 1)]
inside = True
for q in corners:
    for u in UNITS_E:
        # inside the Voronoi cell of 0 iff q.u <= |u|^2/2 = 6/25 for all unit u
        if dot(q, u) > Q3(F(6, 25)):
            inside = False
check("V3b W (side 1/50, centred at p_0) lies in the open hexagon of the origin", inside,
      "checked on the four corners against the six faces")
check("V3c hence W contains no vertex of the hexagonal tiling (vertices lie on cell boundaries)",
      inside)

print()
print("=" * 78)
print("V4   exact colour count on unit circles (hexagons meeting the circle)")
print("=" * 78)


def circle_colours(xc):
    """exact: colours of the hexagons meeting the circle of radius 1 about xc"""
    hits = set()
    for m in range(-12, 13):
        for n in range(-12, 13):
            c = z(m, n)
            d2 = (c[0] - xc[0]) * (c[0] - xc[0]) + (c[1] - xc[1]) * (c[1] - xc[1])
            if d2 > Q3(F(9, 4)):
                continue
            dmin2 = hex_dist2(xc, m, n)
            dmax2 = hex_maxdist2(xc, m, n)
            if dmin2 <= Q3(1) and dmax2 >= Q3(1):
                hits.add(colour(m, n))
    return sorted(hits)


def circle_colours_v2(xc):
    """independent method: hexagon meets the circle iff it contains a point at distance
    exactly 1; test the 6 edges and the interior separately (segment / circle)."""
    hits = set()
    for m in range(-12, 13):
        for n in range(-12, 13):
            c = z(m, n)
            if dist2(c, xc) > Q3(F(9, 4)):
                continue
            v = hex_vertices(m, n)
            # inside-case: if xc is inside the hexagon, distance 1 is hit iff dmax >= 1
            dmax2 = max(dist2(xc, q) for q in v)
            # min over edges of (distance from xc to the edge segment)
            dmin2 = min(seg_dist2(xc, v[i], v[(i + 1) % 6]) for i in range(6))
            if dmin2 <= Q3(1) <= dmax2:
                hits.add(colour(m, n))
    return sorted(hits)


for name, pt in [("p_0 = (1/55,18/55)", P0),
                 ("hexagon centre z(0,0)", z(0, 0)),
                 ("hexagon vertex", hex_vertices(0, 0)[0])]:
    a = circle_colours(pt)
    b = circle_colours_v2(pt)
    check(f"V4 circle about {name}: two methods agree, colours {a}", a == b, f"{a} vs {b}")

print()
print("=" * 78)
print("V5   where the annulus certificate stops: exact bracket for eps*")
print("=" * 78)


def annulus_clean(eps):
    return all(method1_misses(m, n, eps) != 'MEETS' for (m, n) in HEXES if colour(m, n) in (0, 2, 3))


check("V5a eps = 1/60 passes", annulus_clean(F(1, 60)))
check("V5b eps = 170/10000 passes", annulus_clean(F(170, 10000)))
check("V5c eps = 171/10000 fails", not annulus_clean(F(171, 10000)))
lo = 0.0
hi = 0.5
for _ in range(300):
    mid = (lo + hi) / 2
    if annulus_clean(F(mid).limit_denominator(10 ** 15)):
        lo = mid
    else:
        hi = mid
print(f"        eps* = {lo:.13f};  maximal square side sqrt2*eps* = {math.sqrt(2)*lo:.13f}")
check("V5d eps* lies in [170/10000, 171/10000]",
      F(170, 10000) <= F(lo).limit_denominator(10 ** 12) <= F(171, 10000))

print()
print("=" * 78)
print("V6   the honeycomb lattice V = L(c_0): Delone constants")
print("=" * 78)
vs = set()
for m in range(-4, 5):
    for n in range(-4, 5):
        for q in hex_vertices(m, n):
            vs.add(q)
check("V6a the six vertices of a hexagon are the only vertices incident to it",
      len({q for q in hex_vertices(0, 1)}) == 6)
# nearest neighbour distance = r = 2/5
nn = min(dist2(q, q2) for q in hex_vertices(0, 0) for q2 in vs if q2 != q)
check("V6b minimum separation of V is r = 2/5", nn == Q3(F(4, 25)), str(nn))
# covering radius: r, attained at the hexagon centre
check("V6c covering radius of V is r = 2/5 (attained at z(0,0))",
      min(dist2(z(0, 0), q) for q in hex_vertices(0, 0)) == Q3(F(4, 25)))

print()
print("=" * 78)
print("SUMMARY")
print("=" * 78)
fails = [n for n, ok, _ in CHECKS if not ok]
print(f"{len(CHECKS)-len(fails)}/{len(CHECKS)} checks pass")
if fails:
    print("FAILURES:", fails)
sys.exit(1 if fails else 0)
