#!/usr/bin/env python3
"""A NONVACUOUS 3-D cut/flow fixture: rational coordinates, exact volumes, b(0) > 0.

WHY THIS FILE EXISTS.  Every fixture in the record so far is either vacuous (`b = 0` at FCC/HCP, or
all `b < 0` as in the nonuniform and near-contact families) or irrational (the period-16 13-cluster,
whose central cell is the regular dodecahedron with volume in Q(sqrt5)).  The cut condition has never
been evaluated on a fixture that (a) has a strictly positive deficit, (b) has coordinates in Q, so
every volume is an exact rational, and (c) is a legal packing.

THE CONSTRUCTION ("dense local cell").  Take a central vertex at the origin and twelve neighbours
arranged as an icosahedral shell of radius just over 2, with every coordinate ROUNDED TO A RATIONAL
with denominator 10^6 and the shell radius chosen so that rounding cannot break the separation.  The
central Voronoi cell is then a slight deformation of the regular dodecahedron of inradius 1, whose
volume 5.5502910285... is below the Kepler cell sqrt(32) = 5.6568542494..., so

        b(0) = sqrt(32) - vol Omega(0) > 0.

Because the deformation moves each face out by (r - 2)/2, the cell stays well below sqrt(32) as long
as r - 2 is small compared with 0.106; r = 2.0005 moves each face by 0.00025 and the volume by about
(0.00025) x (surface area 12 x 1.26) = 0.004, leaving b(0) ~ 0.10.

THE CONVENTIONS, stated because the numbers depend on them:
  P1  period 8 Z^3, thirteen points per cell (the origin plus the shell);
  P2  an edge joins two centres at distance <= R = 2.001.  The shell sits at 2.0005, so R = 2.001
      includes exactly the twelve shell contacts and nothing else (R = 2 would give a graph with no
      edges at all and a degree-zero centre -- a different, vacuous failure).  With period 8 and
      diameter 4.002 there is NO wrap-around edge for R <= 3, so the periodic graph is the plain
      13-vertex graph (checked, not assumed);
  P3  the cells are the Voronoi cells of the INFINITE periodic packing, computed on the torus; the
      thirteen of them must sum to |det L| = 512, which is the check that no cell was truncated;
  P4  b(v) = sqrt(32) - vol Omega(v) with sqrt(32) enclosed between two rationals, so b(0) > 0 is a
      RATIONAL inequality: vol Omega(0) < SQ32_LO.

WHAT IS CLAIMED.  A legal packing of unit spheres, rational coordinates, exact cell volumes, a
strictly positive deficit at the central vertex, and therefore a cut condition that constrains the
capacity: Phi >= b(0)/deg(0) > 0 for this fixture.  A fixture can only ever REFUTE a capacity; it
cannot establish one, and nothing here bears on Kepler beyond that.

Reproduction: python3 fixture_dense_shell.py      (~10 s)
"""
import itertools, json, os, sys
from fractions import Fraction as F
import fixture_nonuniform as FN
import cut_flow as CF

_HERE = os.path.dirname(os.path.abspath(__file__))
_OUT = os.path.join(_HERE, "out")
PERIOD = F(8)
DEN = 10 ** 6
R_SHELL = F(20005, 10000)          # 2.0005: the shell radius before rounding
CONTACT_R = F(2001, 1000)          # 2.001: the edge range that includes exactly the shell contacts

def icosahedron():
    """The 12 icosahedral directions, as exact rationals of denominator 10^6, scaled to R_SHELL."""
    phi = (1 + 5 ** 0.5) / 2
    raw = []
    for s1 in (1, -1):
        for s2 in (1, -1):
            raw += [(0, s1 * 1, s2 * phi), (s1 * 1, s2 * phi, 0), (s2 * phi, 0, s1 * 1)]
    norm = (1 + phi ** 2) ** 0.5
    scale = float(R_SHELL) / norm
    out = []
    for v in raw:
        q = tuple(F(int(round(c * scale * DEN)), DEN) for c in v)
        if q not in out:
            out.append(q)
    return out

def build():
    """The fixture: origin + 12 rational shell points, period 8 Z^3."""
    L = [[PERIOD, F(0), F(0)], [F(0), PERIOD, F(0)], [F(0), F(0), PERIOD]]
    sites = [(F(0), F(0), F(0))] + icosahedron()
    return L, sites

def wedge(p):
    """2*pi * |x|^2 convention: t = 2 pi r^2, so the cut graph uses |x| directly."""
    return p

def self_test():
    ok = True
    def check(name, cond, info=None):
        nonlocal ok
        ok = ok and bool(cond)
        print("  %s %s%s" % ("PASS" if cond else "FAIL", name, "" if info is None else "  %r" % (info,)))

    L, sites = build()
    check("13 points: the origin and a 12-point shell", len(sites) == 13, len(sites))
    check("every coordinate is rational with denominator 10^6",
          all(isinstance(c, F) and c.denominator <= DEN for p in sites for c in p))

    print("\nP1/P2  the packing and the period convention")
    q = FN.min_separation(L, sites)
    check("minimum separation >= 2 exactly (squared: %s)" % q, q >= 4, float(q) ** 0.5)
    d_shell = [FN.norm2(p) for p in sites[1:]]
    check("every shell point is at distance >= 2 from the origin, and < 2.01",
          all(4 <= d <= F(201, 100) ** 2 for d in d_shell),
          (float(min(d_shell)) ** 0.5, float(max(d_shell)) ** 0.5))
    check("the diameter is < 4.1, so period 8 leaves no wrap-around edge for R <= 3",
          2 * 2.01 < 8 - 3)
    E = FN.edges_within(L, sites, CONTACT_R)
    check("at R = 2.001 the graph has exactly the twelve shell edges",
          sorted(E) == [(0, j) for j in range(1, 13)], E[:5])
    check("at R = 2 it would have none (which is why R = 2.001 is the contact range)",
          FN.edges_within(L, sites, 2) == [])

    print("\nP3  exact cell volumes on the torus")
    detL, vols, info = FN.evaluate(L, sites, rmax=6)
    check("the thirteen cells sum to 512 exactly", sum(vols) == detL, (sum(vols), detL))
    v0 = vols[0]
    print("     central cell volume = %s = %.12f" % (v0, float(v0)))
    print("     Kepler cell sqrt(32) = 5.656854249492 (the comparison is rational)")

    print("\nP4  the deficit at the centre, as a rational inequality")
    b0_lo, b0_hi = CF.SQ32_LO - v0, CF.SQ32_HI - v0
    check("b(0) > 0 STRICTLY (vol Omega(0) < SQ32_LO)", v0 < CF.SQ32_LO, float(b0_lo))
    print("     b(0) in [%.12f, %.12f]" % (float(b0_lo), float(b0_hi)))
    ring = vols[1:]
    check("the twelve shell cells are all far below the Kepler cell (b < 0)",
          all(v > CF.SQ32_HI for v in ring), [float(v) for v in ring[:3]])
    check("the total deficit is negative, so a transfer is not pointwise impossible",
          sum(CF.SQ32_LO - v for v in vols) < 0, float(sum(CF.SQ32_LO - v for v in vols)))
    return ok, L, sites, vols, b0_lo, b0_hi

def export(L, sites, vols, path=None):
    b_lo = [CF.SQ32_LO - v for v in vols]
    b_hi = [CF.SQ32_HI - v for v in vols]
    E = FN.edges_within(L, sites, CONTACT_R)
    d = dict(name="dense_shell_rational",
             note=("NONVACUOUS fixture: a rational 12-point icosahedral shell of radius ~2.0005 "
                   "around a central vertex, period 8 Z^3.  Exact rational cell volumes; "
                   "b(0) > 0, so the cut condition constrains the capacity."),
             edges=[list(e) for e in E],
             b_lo=[str(x) for x in b_lo], b_hi=[str(x) for x in b_hi],
             volumes_are_provisional=False,
             cell_volumes_exact=[str(v) for v in vols],
             period_volume_exact=str(abs(FN.det3(*L))),
             coordinates=[[str(c) for c in p] for p in sites])
    path = path or os.path.join(_OUT, "fixture_dense_shell.json")
    json.dump(d, open(path, "w"), indent=1)
    return path

if __name__ == "__main__":
    print("=" * 100)
    print("A dense local cell: rational icosahedral shell, exact volumes")
    print("=" * 100)
    good, L, sites, vols, b0_lo, b0_hi = self_test()
    p = export(L, sites, vols)
    print("\nexported:", p)
    print("dense_shell:", "PASS" if good else "FAIL")
    sys.exit(0 if good else 1)
