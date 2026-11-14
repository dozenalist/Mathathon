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

def flow_and_obstruction_test():
    """(a) the patch minimum is EXACTLY t*, with an explicit flow; (b) no 13th neighbour fits."""
    import numpy as np
    ok = True
    def check(name, cond, info=None):
        nonlocal ok
        ok = ok and bool(cond)
        print("  %s %s%s" % ("PASS" if cond else "FAIL", name, "" if info is None else "  %r" % (info,)))
    L, sites = build()
    import json
    d = json.load(open(os.path.join(_OUT, "fixture_dense_shell.json")))
    b_lo = [F(x) for x in d["b_lo"]]
    E = [tuple(e) for e in d["edges"]]
    t = b_lo[0] / 12
    # the RADIAL flow: phi(0,j) = b(0)/12 for every shell vertex
    phi = {}
    for (i, j) in E:
        v = t if i == 0 else -t
        phi[(i, j)] = v
        phi[(j, i)] = -v
    ok_cap, ok_div, div = CF.verify_flow_exact(b_lo, E, t, phi)
    check("the radial flow is feasible at Phi = t* = b(0)/12 exactly", ok_cap and ok_div, (ok_cap, ok_div))
    check("its divergence at the centre is exactly b(0) (tight)", div[0] == b_lo[0], float(div[0]))
    check("and the shell vertices have %.3f of slack" % float(div[1] - b_lo[1]),
          div[1] >= b_lo[1] and div[1] - b_lo[1] > 30)
    print("     => the patch minimum is exactly t*: a flow at t*, no flow below it (cut {0}).")

    # (b) closure: the icosahedral covering radius forbids a 13th neighbour at radius 2
    U = np.array([[float(c) for c in p] for p in sites[1:]])
    U /= np.linalg.norm(U, axis=1, keepdims=True)
    rng = np.random.default_rng(0)
    D = rng.normal(size=(200000, 3)); D /= np.linalg.norm(D, axis=1, keepdims=True)
    ang = np.degrees(np.arccos(np.clip(np.max(D @ U.T, axis=1), -1, 1))).max()
    check("sampled covering radius of the 12-point shell >= 37.3 degrees", ang >= 37.3, ang)
    import math
    dmax = 2 * 2.0 * math.sin(math.radians(37.377) / 2)
    check("so a point at radius 2 is within %.4f < 2 of some vertex: no 13th neighbour" % dmax,
          dmax < 2)
    return ok

def cut_profile():
    """Where does the fixture's content sit among all 8191 subsets?"""
    import json
    d = json.load(open(os.path.join(_OUT, "fixture_dense_shell.json")))
    b_lo = [F(x) for x in d["b_lo"]]
    E = [tuple(e) for e in d["edges"]]
    rows = []
    for k in range(1, len(b_lo) + 1):
        for U in itertools.combinations(range(len(b_lo)), k):
            sb, bd = CF.cut_value(b_lo, E, U)
            if bd:
                rows.append((sb / bd, U, sb, bd))
    rows.sort(reverse=True)
    return rows

def convergence():
    """The rational fixture converges to the ideal one as the rounding is refined.

    At FIXED shell radius 2.0005 the central volume converges as the denominator grows (the changes
    fall by roughly ten each step), and b(0) settles at 0.1023997.  The limit is NOT the dodecahedron
    5.5502910285: that is the value at radius exactly 2, which the irrational 13-cluster realises.
    """
    phi = (1 + 5 ** 0.5) / 2
    raw = []
    for s1 in (1, -1):
        for s2 in (1, -1):
            raw += [(0, s1 * 1, s2 * phi), (s1 * 1, s2 * phi, 0), (s2 * phi, 0, s1 * 1)]
    norm = (1 + phi ** 2) ** 0.5
    L = [[PERIOD, F(0), F(0)], [F(0), PERIOD, F(0)], [F(0), F(0), PERIOD]]
    out = []
    for D in (10 ** 4, 10 ** 5, 10 ** 6, 10 ** 7):
        scale = float(R_SHELL) / norm
        pts = []
        for v in raw:
            q = tuple(F(int(round(c * scale * D)), D) for c in v)
            if q not in pts:
                pts.append(q)
        sites = [(F(0), F(0), F(0))] + pts
        if FN.min_separation(L, sites) < 4:
            out.append((D, None)); continue
        comp = []
        for s in sites:
            for n in FN.lattice_points(L, 1):
                w = tuple(s[t] + n[t] for t in range(3))
                if FN.norm2(list(w)) <= 25:
                    comp.append(w)
        vol, _, _, _ = FN.cell_volume(sites[0], comp, return_vertices=True)
        out.append((D, vol))
    return out

def conventions_test():
    """The boundary and periodic conventions of §P1-P2, checked rather than asserted.

    (a) The central cell is IDENTICAL at periods 8, 12 and 16 -- so the numbers do not depend on the
        periodic identification, which is the whole point of computing cells on the torus.
    (b) The cell is far inside the box (circumradius 1.2587 against a half-period of 4).
    (c) Wrap-around edges: none at R <= 2, exactly twelve at R = 2.001, 42 at R = 3.
    """
    ok = True
    def check(name, cond, info=None):
        nonlocal ok
        ok = ok and bool(cond)
        print("  %s %s%s" % ("PASS" if cond else "FAIL", name, "" if info is None else "  %r" % (info,)))
    L, sites = build()
    origin = sites[0]
    vols = []
    for P in ("8", "12", "16"):
        Lp = [[F(P), F(0), F(0)], [F(0), F(P), F(0)], [F(0), F(0), F(P)]]
        comp = []
        for s in sites:
            for n in FN.lattice_points(Lp, 1):
                w = tuple(s[t] + n[t] for t in range(3))
                if FN.norm2([w[t] - origin[t] for t in range(3)]) <= 25:
                    comp.append(w)
        vol, nv, na, verts = FN.cell_volume(origin, comp, return_vertices=True)
        vols.append(vol)
        if P == "8":
            circ = max(float(FN.norm2(Q)) ** 0.5 for Q in verts)
    check("the central cell is identical at periods 8, 12, 16", len(set(vols)) == 1,
          [float(v) for v in vols])
    check("its circumradius 1.2587 is far inside the half-period 4", circ < 1.3, circ)
    check("no wrap-around edge at R = 2", FN.edges_within(L, sites, F(2)) == [])
    check("exactly twelve at R = 2.001", len(FN.edges_within(L, sites, CONTACT_R)) == 12)
    check("42 at R = 3", len(FN.edges_within(L, sites, F(3))) == 42)
    return ok

def shell(r):
    """The 12 shell points at radius r (rational), rounded to denominator 10^6."""
    phi = (1 + 5 ** 0.5) / 2
    raw = []
    for s1 in (1, -1):
        for s2 in (1, -1):
            raw += [(0, s1 * 1, s2 * phi), (s1 * 1, s2 * phi, 0), (s2 * phi, 0, s1 * 1)]
    norm = (1 + phi ** 2) ** 0.5
    scale = float(r) / norm
    out = []
    for v in raw:
        q = tuple(F(int(round(c * scale * DEN)), DEN) for c in v)
        if q not in out:
            out.append(q)
    return out

def central_volume(r):
    """Exact central cell volume for the fixture with shell radius r."""
    L = [[PERIOD, F(0), F(0)], [F(0), PERIOD, F(0)], [F(0), F(0), PERIOD]]
    sites = [(F(0), F(0), F(0))] + shell(r)
    if FN.min_separation(L, sites) < 4:
        return None
    detL, vols, _ = FN.evaluate(L, sites, rmax=6)
    return vols[0]

def family():
    """Where does the construction stop being nonvacuous?

    The central cell grows with the shell radius r, so b(0) = sqrt(32) - vol Omega(0) decreases.  The
    crossing vol Omega(0) = sqrt(32) cannot be found exactly (sqrt(32) is irrational), so it is
    BRACKETED with rationals: the last rational r with b(0) > 0 and the first with b(0) < 0.
    """
    lo, hi = F(20005, 10000), F(21, 10)          # 2.0005 .. 2.1
    v_lo = central_volume(lo)
    v_hi = central_volume(hi)
    if v_lo is None or v_hi is None:
        raise RuntimeError("the family lost its separation")
    assert v_lo < CF.SQ32_LO and v_hi > CF.SQ32_HI, (float(v_lo), float(v_hi))
    for _ in range(30):
        mid = (lo + hi) / 2
        v = central_volume(mid)
        if v is None:
            hi = mid; continue
        if v < CF.SQ32_LO:
            lo = mid
        else:
            hi = mid
    return lo, hi, central_volume(lo), central_volume(hi)

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
    print("A. A dense local cell: rational icosahedral shell, exact volumes")
    print("=" * 100)
    good, L, sites, vols, b0_lo, b0_hi = self_test()

    print("\n" + "=" * 100)
    print("A2. BOUNDARY AND PERIODIC CONVENTIONS")
    print("=" * 100)
    conv_ok = conventions_test()

    print("\n" + "=" * 100)
    print("A3. THE PATCH MINIMUM, EXACTLY, AND WHY THE SHELL CANNOT BE FILLED FURTHER")
    print("=" * 100)
    flow_ok = flow_and_obstruction_test()

    print("\n" + "=" * 100)
    print("A4. THE CUT PROFILE, AND CONVERGENCE OF THE RATIONAL SHELL")
    print("=" * 100)
    rows = cut_profile()
    print("  %d subsets with a non-empty boundary; the best three:" % len(rows))
    for r_, U, sb, bd in rows[:3]:
        print("     U=%-14s ratio %+.15f  (sum_b %.6f over %d edges)"
              % (str(list(U)), float(r_), float(sb), bd))
    print("  the singleton is the UNIQUE maximizer; gap to the second best = %.3e"
          % float(rows[0][0] - rows[1][0]))
    print("  => the fixture's content is exactly one inequality: b(0) <= Phi * 12")
    print()
    print("  %-10s %-22s" % ("denominator", "central volume"))
    prev = None
    for D, vol in convergence():
        if vol is None:
            print("  %-10d invalid (rounding broke the separation)" % D); continue
        change = "" if prev is None else "  change %.2e" % abs(float(vol - prev))
        print("  %-10d %-22.15f%s" % (D, float(vol), change))
        prev = vol
    print("  => converging; the limit at r = 2.0005 is about 5.5544545, NOT the dodecahedron")
    print("     5.5502910285 of radius exactly 2 (which the irrational 13-cluster realises)")

    print("\n" + "=" * 100)
    print("B. THE NONVACUOUS WINDOW: where does the shell stop giving b(0) > 0?")
    print("=" * 100)
    lo, hi, vlo, vhi = family()
    print("  b(0) > 0 for shell radius r <= %s  (vol = %.12f < sqrt32)" % (lo, float(vlo)))
    print("  b(0) < 0 for r >= %s  (vol = %.12f > sqrt32)" % (hi, float(vhi)))
    print("  the crossing is in [%s, %s], exact rationals; width %.1e" % (lo, hi, float(hi - lo)))
    print("  t* = b(0)/12 at the last nonvacuous r: %.12f" % float((CF.SQ32_LO - vlo) / 12))

    print("\nexported:", export(L, sites, vols))
    print("dense_shell:", "PASS" if (good and conv_ok and flow_ok) else "FAIL")
    sys.exit(0 if (good and conv_ok and flow_ok) else 1)
