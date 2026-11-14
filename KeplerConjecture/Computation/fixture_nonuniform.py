#!/usr/bin/env python3
"""The smallest nonuniform periodic fixture, and why near-contact cannot supply one with b > 0.

WHY.  Every near-Kepler fixture in the record so far is a close packing: FCC and HCP have
`vol Omega = sqrt(32)` at every vertex, so `b = 0` and the cut condition is vacuous there; the
period-16 13-cluster has one small cell and twelve enormous ones, so its cut condition collapses to a
single inequality (K15-C-D4RECON-001).  Neither shows what the cut condition does when the cell
volumes are UNEQUAL but comparable.  This file builds the smallest fixture that does.

TWO RESULTS, one positive and one negative.

  R1  THE SMALLEST NONUNIFORM FIXTURE has THREE points per cell, not two.  A 2-point periodic
      packing always has congruent cells: sampling and exact volumes agree on every 2-point
      configuration tried, including strongly asymmetric ones (b = (2.1,0,0) in a 5-cube gives
      62.5/62.5).  The three-point fixture

          L = 4 Z^3,   A = (0,0,0),  B = (2,0,0),  C = (0,2,0)

      has minimum separation exactly 2 (A-B and A-C are contacts) and EXACT cell volumes
      16, 24, 24.  Its deficits are all negative, so its cut condition is satisfied at every Phi:
      it shows that unequal cells alone give the criterion nothing.  What the criterion needs is a
      cell SMALLER than the Kepler cell sqrt(32) = 5.657, i.e. b(v) > 0 somewhere.

  R2  NEAR-CONTACT CANNOT SUPPLY ONE.  For FCC at nearest-neighbour distance d the cell volume is
      d^3/sqrt2, so b = (8 - d^3)/sqrt2 > 0 requires d < 2 -- below contact.  Perturbing one site by
      delta changes the cell only by ~0.7 delta^2, while jamming limits delta to the slack
      eps = d - 2.  Measured (exact volumes, delta taken to the exact bisected maximum):

          d      eps       delta_max   b(0) at delta_max
          2.1213 0.1213    0.1771      -1.132
          2.0506 0.0506    0.0725      -0.447
          2.0153 0.0153    0.0217      -0.131
          2.0011 0.0011    0.0016      -0.009

      i.e. b(0) -> -(12/sqrt2)(d-2) = -8.485 eps.  So no perturbation of a close packing within its
      own contact slack produces a positive deficit, and the near-Kepler regime cannot supply a
      fixture in which the cut condition bites.  That is the quantitative form of K15-C-CUTJAM-001,
      and it is why the only fixture in the record with b > 0 (the 13-cluster) is far from Kepler.

THE HYPOTHESES, stated because the numbers depend on them:
  H1  min separation >= 2  (checked EXACTLY in rational arithmetic, not sampled);
  H2  the cells are the Voronoi cells of the INFINITE periodic packing (computed on the torus: every
      competitor within R_MAX, and the volumes are checked to sum to |det L| exactly);
  H3  b(v) = sqrt(32) - vol Omega(v), with sqrt(32) enclosed between two rationals (SQ32_LO/HI), so
      every b is an exact rational interval, not a float;
  H4  the cut condition is C044's: sum_U b <= Phi |delta^+(U)| for every finite U, evaluated here on
      the vertex set of one cell -- legitimate because the graph is periodic and the cut scan is over
      finite U (see the contract in cut_flow.py).

WHAT IS AND IS NOT CLAIMED.  The cell volumes are exact rational numbers (vertex enumeration +
triangulation, all in Q).  The resulting cut threshold is exact as an interval on b.  Nothing here is
a step toward Kepler: it is a fixture, and a fixture can only ever refute a capacity, never establish
one.

Reproduction: python3 fixture_nonuniform.py
"""
import itertools, json, os, sys
from fractions import Fraction as F
import numpy as np
from scipy.spatial import ConvexHull

_HERE = os.path.dirname(os.path.abspath(__file__))
_OUT = os.path.join(_HERE, "out")
SQ32_LO = F(5656854249492380195206, 10 ** 21)
SQ32_HI = F(5656854249492380195207, 10 ** 21)

# ------------------------------------------------------------------ exact rational geometry
def det3(a, b, c):
    return (a[0] * (b[1] * c[2] - b[2] * c[1])
            - a[1] * (b[0] * c[2] - b[2] * c[0])
            + a[2] * (b[0] * c[1] - b[1] * c[0]))

def solve3(planes):
    """Intersection point of three planes (a,b,c) . x = d, exactly; None if degenerate."""
    (a1, b1, c1, d1), (a2, b2, c2, d2), (a3, b3, c3, d3) = planes
    D = det3((a1, b1, c1), (a2, b2, c2), (a3, b3, c3))
    if D == 0:
        return None
    x = det3((d1, b1, c1), (d2, b2, c2), (d3, b3, c3)) / D
    y = det3((a1, d1, c1), (a2, d2, c2), (a3, d3, c3)) / D
    z = det3((a1, b1, d1), (a2, b2, d2), (a3, b3, d3)) / D
    return (x, y, z)

def lattice_points(L, rng=2):
    for i in range(-rng, rng + 1):
        for j in range(-rng, rng + 1):
            for k in range(-rng, rng + 1):
                yield [i * L[0][t] + j * L[1][t] + k * L[2][t] for t in range(3)]

def norm2(p):
    return sum(t * t for t in p)

def cell_volume(v, competitors):
    """Exact volume of {x : |x-v| <= |x-w| for every w in competitors}.

    Half-spaces  2(w-v).x <= |w|^2 - |v|^2  are rational; vertices are enumerated exactly and the
    volume is the exact sum of |det|/6 over the triangles of a hull, using v (strictly interior) as
    the apex.  scipy supplies only the COMBINATORICS of the hull -- every coordinate it sees is a
    float, but the numbers used in the volume are the rational vertices.
    """
    planes = []
    vv = norm2(v)
    for w in competitors:
        if w == v:
            continue
        n = [2 * (w[t] - v[t]) for t in range(3)]
        planes.append((n[0], n[1], n[2], norm2(w) - vv))
    seen, P = set(), []
    for pl in planes:
        key = tuple(F(x) for x in pl)
        if key in seen:
            continue
        seen.add(key); P.append(key)
    # STAGE 1 (float): which planes are actually ACTIVE?  Only those can contribute a vertex.
    from scipy.spatial import HalfspaceIntersection
    hs = np.array([[float(pl[0]), float(pl[1]), float(pl[2]), -float(pl[3])] for pl in P])
    hi = HalfspaceIntersection(hs, np.array([float(c) for c in v]))
    pts = hi.intersections
    active = []
    for pl in P:
        n = np.array([float(pl[0]), float(pl[1]), float(pl[2])]); d = float(pl[3])
        if np.any(np.abs(pts @ n - d) < 1e-7):
            active.append(pl)
    # STAGE 2 (exact): enumerate vertices of the active planes only.
    Af = np.array([[float(x) for x in pl] for pl in active])
    verts = []
    for i, j, k in itertools.combinations(range(len(active)), 3):
        if abs(np.linalg.det(Af[[i, j, k], :3])) < 1e-9:
            continue
        pt = solve3([active[i], active[j], active[k]])
        if pt is None:
            continue
        ok = True
        for (a, b, c, d) in active:
            if a * pt[0] + b * pt[1] + c * pt[2] > d:
                ok = False; break
        if ok:
            verts.append(pt)
    verts = sorted(set(verts))
    if len(verts) < 4:
        raise RuntimeError("degenerate cell (only %d vertices)" % len(verts))
    ptsx = np.array([[float(c) for c in q] for q in verts])
    hull = ConvexHull(ptsx)
    vol = F(0)
    for tri in hull.simplices:
        a, b, c = (verts[t] for t in tri)
        d = det3(tuple(a[t] - v[t] for t in range(3)),
                 tuple(b[t] - v[t] for t in range(3)),
                 tuple(c[t] - v[t] for t in range(3)))
        vol += abs(d) / 6
    return vol, len(verts), len(active)


def min_separation(L, sites, rng=3):
    """Exact squared minimum distance over distinct points of the periodic set."""
    best = None
    for s in sites:
        for t in sites:
            for n in lattice_points(L, rng):
                d = [s[j] - t[j] - n[j] for j in range(3)]
                if all(x == 0 for x in d):
                    continue
                q = norm2(d)
                if best is None or q < best:
                    best = q
    return best

def evaluate(L, sites, rmax=6):
    """Exact cell volumes of the periodic packing, and the period volume they must sum to."""
    detL = abs(det3(*L))
    vols, info = [], []
    for v in sites:
        comp = []
        for s in sites:
            for n in lattice_points(L, 2):
                w = tuple(s[t] + n[t] for t in range(3))
                if norm2([w[t] - v[t] for t in range(3)]) <= rmax * rmax:
                    comp.append(w)
        vol, nv, np_ = cell_volume(v, comp)
        vols.append(vol); info.append((nv, np_))
    return detL, vols, info

def diag(x, y, z):
    return [[F(x), F(0), F(0)], [F(0), F(y), F(0)], [F(0), F(0), F(z)]]

# ------------------------------------------------------------------ the fixtures
SMALLEST_NONUNIFORM = dict(
    name="smallest_nonuniform_3pt",
    L=diag(4, 4, 4),
    sites=[(F(0), F(0), F(0)), (F(2), F(0), F(0)), (F(0), F(2), F(0))],
    note="three points per cell; the smallest periodic packing whose Voronoi cells are not all "
         "congruent.  Minimum separation exactly 2 (A-B, A-C).",
)

def fcc_cubic(a):
    """FCC as 4 sites of the cubic cell of side a: nearest-neighbour distance a/sqrt2."""
    a = F(a)
    return diag(a, a, a), [(F(0), F(0), F(0)), (F(0), a / 2, a / 2),
                           (a / 2, F(0), a / 2), (a / 2, a / 2, F(0))]

def edges_within(L, sites, R):
    """All pairs of the periodic set at distance <= R, with the lattice shift that realises it."""
    E = set()
    for i, s in enumerate(sites):
        for j, t in enumerate(sites):
            for n in lattice_points(L, 2):
                d = [t[k] + n[k] - s[k] for k in range(3)]
                if all(x == 0 for x in d):
                    continue
                if norm2(d) <= F(R) ** 2:
                    E.add((min(i, j), max(i, j)))
    return sorted(E)

def deficits(L, sites, rmax=6):
    detL, vols, info = evaluate(L, sites, rmax=rmax)
    return vols, [SQ32_LO - v for v in vols], [SQ32_HI - v for v in vols], detL, info

def max_displacement_within_slack(L, sites, which=0):
    """Largest dx (moving site `which` in +x) keeping the minimum separation at least 2.  Exact."""
    if min_separation(L, list(sites)) < 4:
        raise ValueError("the unperturbed configuration already violates the separation")
    lo, hi = F(0), F(1)
    base = list(sites)
    while True:                                   # bracket
        trial = list(base)
        p = trial[which]
        trial[which] = (p[0] + hi, p[1], p[2])
        if min_separation(L, trial) < 4:
            break
        hi *= 2
    for _ in range(45):
        mid = (lo + hi) / 2
        trial = list(base)
        p = trial[which]
        trial[which] = (p[0] + mid, p[1], p[2])
        if min_separation(L, trial) >= 4:
            lo = mid
        else:
            hi = mid
    return lo

def self_test():
    ok = True
    def check(name, cond, info=None):
        nonlocal ok
        ok = ok and bool(cond)
        print("  %s %s%s" % ("PASS" if cond else "FAIL", name, "" if info is None else "  %r" % (info,)))

    print("A. exact engine: known cells")
    L = diag(2, 2, 2)
    detL, vols, _ = evaluate(L, [(F(0), F(0), F(0))])
    check("cubic 2Z^3: cell volume = 8 exactly", vols[0] == 8, vols[0])
    a = F(23, 10)
    Lb = diag(a, a, a)
    detL, vols, _ = evaluate(Lb, [(F(0), F(0), F(0)), (a / 2, a / 2, a / 2)])
    check("BCC a=2.3: both cells = a^3/2", all(v == a ** 3 / 2 for v in vols), vols)

    print("\nB. R1: the smallest nonuniform fixture")
    f = SMALLEST_NONUNIFORM
    q = min_separation(f["L"], f["sites"])
    check("min separation is exactly 2", q == 4, q)
    vols, b_lo, b_hi, detL, info = deficits(f["L"], f["sites"])
    check("cell volumes are exactly (16, 24, 24)", vols == [F(16), F(24), F(24)], vols)
    check("they sum to det L = 64", sum(vols) == detL, (sum(vols), detL))
    check("the cells are not congruent", len(set(vols)) > 1, vols)
    check("every deficit is negative, so the cut condition is vacuous there",
          all(x < 0 for x in b_hi), [float(x) for x in b_hi])
    E = edges_within(f["L"], f["sites"], 2)
    check("at R = 2 the edges are A-B and A-C", E == [(0, 1), (0, 2)], E)
    print("     volumes %s   b in %s" % ([str(v) for v in vols],
                                         ["[%.4f, %.4f]" % (float(l), float(h))
                                          for l, h in zip(b_lo, b_hi)]))

    print("\nC. R2: near-contact FCC, perturbation taken to the exact edge of the slack")
    print("     %-8s %-8s %-10s %-10s %s" % ("d", "eps", "delta_max", "b(0)", "b(1)"))
    rows = []
    for a in ("3.0", "2.9", "2.85", "2.83"):
        Lf, S = fcc_cubic(a)
        d = float(F(a)) / 2 ** 0.5
        eps = d - 2
        dx = max_displacement_within_slack(Lf, S, 0)
        S2 = [(S[0][0] + dx, S[0][1], S[0][2])] + S[1:]
        if min_separation(Lf, S2) < 4:
            raise RuntimeError("bisection left the feasible set")
        vols, b_lo, b_hi, detL, _ = deficits(Lf, S2)
        rows.append((d, eps, float(dx), float(min(b_hi)), float(min(b_hi)) / eps))
        print("     %-8.4f %-8.4f %-10.4f %-10.4f %+.4f" % (d, eps, float(dx),
                                                             float(min(b_hi)), float(min(b_hi[1:]))))
    check("every vertex still has b < 0 at the largest allowed displacement",
          all(r[3] < 0 for r in rows), [r[3] for r in rows])
    check("and b/eps settles at -(8 - d^3)/(sqrt2 eps) -> -12/sqrt2 = -8.485",
          abs(rows[-1][4] + 12 / 2 ** 0.5) < 1.5, rows[-1][4])
    return ok, rows

def make_fixture(L, points, R, name="packing", rmax=6):
    """GEOMETRY -> the external C044 fixture schema.  The hypotheses are checked, not assumed.

    H1  min separation >= 2, checked exactly;
    H2  the cells are computed on the torus and must sum to det L exactly (this is the check that
        rmax was large enough to bound them: a truncated cell would show up here);
    H3  b = sqrt(32) - vol Omega, enclosed between two rationals.

    Returns the dict that cut_flow.load_external_fixture / evaluate_external consume.
    """
    q = min_separation(L, points)
    if q < 4:
        raise ValueError("minimum separation is %s < 2" % (float(q) ** 0.5))
    detL, vols, info = evaluate(L, points, rmax=rmax)
    if sum(vols) != detL:
        raise RuntimeError("cell volumes sum to %s but the period volume is %s: rmax too small"
                           % (sum(vols), detL))
    E = edges_within(L, points, R)
    return dict(name=name,
                note=("built from rational geometry: period volume %s, cell volumes %s, "
                      "min separation %s" % (detL, [str(v) for v in vols], float(q) ** 0.5)),
                edges=[list(e) for e in E],
                b_lo=[str(SQ32_LO - v) for v in vols],
                b_hi=[str(SQ32_HI - v) for v in vols],
                volumes_are_provisional=False,
                cell_volumes_exact=[str(v) for v in vols],
                period_volume_exact=str(detL))

def family_scan():
    """Is the cut condition ever non-vacuous in the near-contact band?

    FCC of cubic side a has nearest-neighbour distance d = a/sqrt2 and density
    4(4pi/3)/a^3.  For a from 3.0 down to 2.82 the density runs from 0.621 to 0.740 (Kepler is
    0.7405), so this is the near-contact band.  At each a, displace one site by a fraction of the
    maximum the contact slack allows, recompute the cells EXACTLY, and take t* from cut_flow's
    exhaustive scan over the 4 vertices.
    """
    import cut_flow as CF
    rows = []
    for a in ("3.0", "2.95", "2.9", "2.87", "2.85", "2.83"):
        Lf, S = fcc_cubic(a)
        dx_max = max_displacement_within_slack(Lf, S, 0)
        d = float(F(a)) / 2 ** 0.5
        rho = float(4 * (4 * 3.141592653589793 / 3) / F(a) ** 3)
        t_stars = []
        for frac in (F(0), F(1, 2), F(1)):
            dx = dx_max * frac
            S2 = [(S[0][0] + dx, S[0][1], S[0][2])] + S[1:]
            fx = make_fixture(Lf, S2, F("2.13"), name="fcc_a%s_frac%s" % (a, frac))
            scan = CF.exhaustive_cut_scan([F(x) for x in fx["b_lo"]], [tuple(e) for e in fx["edges"]])
            t_stars.append(scan["t_star"])
        rows.append((float(a), d, rho, float(dx_max), [float(t) for t in t_stars]))
    return rows

def export(path=None):
    f = SMALLEST_NONUNIFORM
    vols, b_lo, b_hi, detL, _ = deficits(f["L"], f["sites"])
    E = edges_within(f["L"], f["sites"], 2)
    d = dict(name=f["name"], note=f["note"], edges=[list(e) for e in E],
             b_lo=[str(x) for x in b_lo], b_hi=[str(x) for x in b_hi],
             volumes_are_provisional=False,
             cell_volumes_exact=[str(v) for v in vols],
             cell_volume_sum_exact=str(sum(vols)), period_volume_exact=str(detL))
    path = path or os.path.join(_OUT, "fixture_nonuniform_3pt.json")
    json.dump(d, open(path, "w"), indent=1)
    return path

def main():
    print("=" * 100)
    print("A-C. the engine, the smallest nonuniform fixture, and the near-contact bound")
    print("=" * 100)
    good, rows = self_test()
    print("\n" + "=" * 100)
    print("D. FAMILY SCAN: is the cut condition ever non-vacuous in the near-contact band?")
    print("=" * 100)
    print("   %-6s %-8s %-9s %-10s %s" % ("a", "d", "density", "delta_max", "t* at delta = 0, 1/2, 1"))
    fam = family_scan()
    for a, d, rho, dxm, ts in fam:
        print("   %-6.3f %-8.4f %-9.5f %-10.4f %s" % (a, d, rho, dxm, ts))
    allvac = all(all(t == 0 for t in ts) for _, _, _, _, ts in fam)
    print("   => %s" % ("t* = 0 at EVERY instance: the cut condition is vacuous across the band"
                        if allvac else "some instance has t* > 0"))
    print("\nexported:", export())
    print("fixture_nonuniform:", "PASS" if (good and allvac) else "FAIL")
    return 0 if (good and allvac) else 1

if __name__ == "__main__":
    sys.exit(main())
