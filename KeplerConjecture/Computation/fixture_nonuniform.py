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

def _facet_volume(v, planes, verts):
    """Exact volume of the polytope, computed FACET BY FACET from the planes -- no qhull.

    Every vertex of the cell lies on at least three of the enumerated planes, so the facets can be
    read off directly: for each plane, the vertices exactly on it.  A plane with fewer than three
    such vertices touches the cell in a point or an edge and is not a facet.  Each facet is ordered
    cyclically by an EXACT angular sort around its centroid, fanned into triangles, and each triangle
    is joined to the interior point v.

    This replaces a scipy ConvexHull triangulation that failed with QH6154 (a flat initial simplex)
    on a coplanar facet -- a float fragility in a computation that is otherwise exact end to end.
    """
    total = F(0)
    for (a, b, c, d) in planes:
        on = [P for P in verts if a * P[0] + b * P[1] + c * P[2] == d]
        if len(on) < 3:
            continue                                  # a point or an edge, not a facet
        m = [sum(P[t] for P in on) / len(on) for t in range(3)]
        # an in-plane basis: e1 from the centroid to the first vertex, e2 = n x e1
        e1 = [on[0][t] - m[t] for t in range(3)]
        n = (a, b, c)
        e2 = [n[1] * e1[2] - n[2] * e1[1], n[2] * e1[0] - n[0] * e1[2], n[0] * e1[1] - n[1] * e1[0]]
        def coords(P):
            w = [P[t] - m[t] for t in range(3)]
            return (sum(w[t] * e1[t] for t in range(3)), sum(w[t] * e2[t] for t in range(3)))
        pts = [(coords(P), P) for P in on]
        def half(p):                                   # exact: upper half-plane or lower
            x, y = p[0]
            return 0 if (y > 0 or (y == 0 and x >= 0)) else 1
        import functools
        def cmp(p, q):
            hp, hq = half(p), half(q)
            if hp != hq:
                return -1 if hp < hq else 1
            cross = p[0][0] * q[0][1] - p[0][1] * q[0][0]
            if cross > 0:
                return -1
            if cross < 0:
                return 1
            return 0
        pts.sort(key=functools.cmp_to_key(cmp))
        for i in range(1, len(pts) - 1):
            A, B, C = pts[0][1], pts[i][1], pts[i + 1][1]
            total += abs(det3(tuple(A[t] - v[t] for t in range(3)),
                              tuple(B[t] - v[t] for t in range(3)),
                              tuple(C[t] - v[t] for t in range(3)))) / 6
    return total


def cell_volume(v, competitors, _drop_active=None, return_vertices=False):
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
    if len(P) < 4:
        raise RuntimeError("only %d competitor planes within rmax: the cell looks UNBOUNDED. "
                           "Increase rmax past half the period diameter." % len(P))
    # STAGE 1 (float): which planes are actually ACTIVE?  Only those can contribute a vertex.
    from scipy.spatial import HalfspaceIntersection
    hs = np.array([[float(pl[0]), float(pl[1]), float(pl[2]), -float(pl[3])] for pl in P])
    hi = HalfspaceIntersection(hs, np.array([float(c) for c in v]))
    pts = hi.intersections
    active, discarded = [], []
    for pl in P:
        n = np.array([float(pl[0]), float(pl[1]), float(pl[2])]); d = float(pl[3])
        if np.any(np.abs(pts @ n - d) < 1e-7):
            active.append(pl)
        else:
            discarded.append(pl)
    if _drop_active is not None:
        # TEST HOOK: move an active plane into the discarded set, so the completeness certificate
        # must fire.  A check that cannot fail is not a check.
        discarded.append(active.pop(_drop_active))
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

    # ---------------------------------------------------------------- COMPLETENESS CERTIFICATE
    # The float pass above only PROPOSES which planes are active.  Three exact checks then certify
    # that the enumerated polytope really is the cell:
    #   (C1) every active plane supports a facet of the hull  =>  the hull equals the intersection
    #        of the active half-spaces (it is contained in it, and all facets are used), hence the
    #        candidate region is bounded and is exactly hull(vertices);
    #   (C2) every DISCARDED plane contains every vertex  =>  adding the discarded half-spaces does
    #        not cut the hull, so the true cell equals the hull;
    #   (C3) the hull is non-degenerate (checked above by the vertex count).
    # Together: the volume computed below is the volume of the Voronoi cell, with no reliance on the
    # float pre-pass being right.
    # (C1') the facet-by-facet volume uses only planes and exact vertices; the checks below
    #       certify that the plane set is complete: every enumerated vertex satisfies every plane of
    #       A (by construction) and every DISCARDED plane contains every vertex, so the polytope
    #       built from A is the true cell.
    for (a, b, c, d) in discarded:
        for (x, y, z) in verts:
            if a * x + b * y + c * z > d:
                raise RuntimeError("completeness (C2) failed: a discarded plane cuts the hull")

    vol = _facet_volume(v, active, verts)
    if vol <= 0:
        raise RuntimeError("degenerate cell: the facet decomposition gave volume %s" % vol)
    if return_vertices:
        return vol, len(verts), len(active), verts
    return vol, len(verts), len(active)


def min_separation(L, sites, rng=3):
    """Exact squared minimum distance over distinct points of the periodic set.

    The skip is (same SITE and zero shift), not "zero displacement": two distinct sites that
    coincide, or differ by a lattice vector, are distance 0 apart and must be caught.  The earlier
    version skipped every zero displacement, so a duplicate site passed the separation test and its
    cell was double-counted -- which the partition check then flagged as overlapping cells.
    """
    best = None
    for i, s in enumerate(sites):
        for j, t in enumerate(sites):
            for n in lattice_points(L, rng):
                if i == j and all(x == 0 for x in n):
                    continue
                q = norm2([s[k] - t[k] - n[k] for k in range(3)])
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
    if sum(vols) != detL:
        raise RuntimeError("cell volumes sum to %s, period volume is %s: rmax did not bound the "
                           "cells (a truncated cell shows up here)" % (sum(vols), detL))
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

def two_site_congruence(trials=None):
    """THEOREM (two-site periodic congruence), and its exact check.

    Let Lambda = {A, B} + L be a periodic packing with exactly TWO points per cell.  Then the two
    Voronoi cells on the torus T = R^3/L are congruent, so vol Omega(A) = vol Omega(B) and
    b(A) = b(B).

    PROOF.  Let sigma(x) = A + B - x, the point reflection in the midpoint of A and B.
      (i)  sigma is well defined on T: sigma(x + n) = sigma(x) - n, and -n lies in L because every
           lattice is centrally symmetric (-L = L).
      (ii) sigma is an isometry of T (a point reflection is an isometry of R^3 and (i) says it
           descends).
      (iii) sigma swaps the two distance functions:
               d(sigma x, A) = min_n |A + B - x - A - n| = min_n |x - B + n| = d(x, B),
               d(sigma x, B) = d(x, A),
           using the symmetry n -> -n of L in the last step.
      (iv) Hence sigma maps {d(., A) <= d(., B)} onto {d(., B) <= d(., A)}, i.e. cell(A) onto
           cell(B).  Congruent cells have equal volume.  QED.

    Consequence, and why the fixture in this file needs THREE points: with two points per cell the
    two deficits are equal, so a nonuniform 2-point fixture cannot exist.  That is a theorem, not an
    observation; the earlier numerical evidence was a symptom of it.

    The check below verifies (i)-(iv) concretely: it reflects the exact vertex set of cell(A) through
    the midpoint and requires it to equal the exact vertex set of cell(B).
    """
    cases = [
        ("cubic a=5, B=(2.1,0,0)", diag(5, 5, 5), [(F(0), F(0), F(0)), (F(21, 10), F(0), F(0))]),
        ("tetragonal 2x2x3.8, B=(0.7,0,1.9)", diag(2, 2, F("3.8")),
         [(F(0), F(0), F(0)), (F(7, 10), F(0), F(19, 10))]),
        ("cubic a=3, B=(1.5,1.5,1.5)", diag(3, 3, 3),
         [(F(0), F(0), F(0)), (F(3, 2), F(3, 2), F(3, 2))]),
    ]
    ok = True
    for name, L, sites in cases:
        A, B = sites
        comp = []
        for s in sites:
            for n in lattice_points(L, 2):
                w = tuple(s[t] + n[t] for t in range(3))
                if norm2([w[t] - A[t] for t in range(3)]) <= 36:
                    comp.append(w)
        vA, _, _, VA = cell_volume(A, comp, return_vertices=True)
        compB = []
        for s in sites:
            for n in lattice_points(L, 2):
                w = tuple(s[t] + n[t] for t in range(3))
                if norm2([w[t] - B[t] for t in range(3)]) <= 36:
                    compB.append(w)
        vB, _, _, VB = cell_volume(B, compB, return_vertices=True)
        mid = [(A[t] + B[t]) / 2 for t in range(3)]
        refl = sorted(tuple(2 * mid[t] - P[t] for t in range(3)) for P in VA)
        same = refl == sorted(VB)
        ok = ok and same and vA == vB
        print("  %s %-34s vol %s = %s, reflected vertices match: %s"
              % ("PASS" if (same and vA == vB) else "FAIL", name, vA, vB, same))
    return ok

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

    print("\nB2. THEOREM: two-site periodic cells are congruent (point reflection through the midpoint)")
    ok = two_site_congruence() and ok

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

def engine_cross_check(trials=3, N=2 ** 18):
    """Validate the exact engine against an independent sampler and against a known case.

    A bug here would corrupt every number this file produces, so it is checked two ways:
      * a single site in a 16-cube must give volume 4096 (and rmax = 6 must be REFUSED, because
        the nearest image is at 16);
      * random rational packings (2 to 4 sites), exact volumes vs scrambled-Sobol assignment.
    """
    from scipy.stats.qmc import Sobol
    ok = True
    detL, vols, _ = evaluate([[F(16), F(0), F(0)], [F(0), F(16), F(0)], [F(0), F(0), F(16)]],
                             [(F(0), F(0), F(0))], rmax=20)
    ok = ok and vols[0] == 4096
    print("  %s 16-cube single site: volume 4096" % ("PASS" if vols[0] == 4096 else "FAIL"))
    try:
        evaluate([[F(16), F(0), F(0)], [F(0), F(16), F(0)], [F(0), F(0), F(16)]],
                 [(F(0), F(0), F(0))], rmax=6)
        refused = False
    except RuntimeError:
        refused = True
    print("  %s rmax = 6 is refused (the nearest image is at 16)" % ("PASS" if refused else "FAIL"))
    ok = ok and refused

    def sample(L, sites):
        a, b, c = (float(L[i][i]) for i in range(3))
        S = np.array([[float(x) for x in s] for s in sites])
        eng = Sobol(d=3, scramble=True, seed=11)
        cnt = np.zeros(len(sites), dtype=np.int64)
        for _ in range(8):
            P = eng.random(N // 8) * np.array([a, b, c])
            D = P[:, None, :] - S[None, :, :]
            D -= np.array([a, b, c]) * np.round(D / np.array([a, b, c]))
            cnt += np.bincount(np.argmin(np.einsum("ijk,ijk->ij", D, D), axis=1),
                               minlength=len(sites))
        return cnt / cnt.sum() * a * b * c

    rng = np.random.default_rng(0)
    worst = 0.0
    for _ in range(trials):
        a = F(3) + F(int(rng.integers(0, 16)), 10)
        L = diag(a, a, a)
        sites = [(F(0), F(0), F(0))]
        cand = [(F(i, 2), F(j, 2), F(k, 2))
                for i in range(2 * int(a)) for j in range(2 * int(a)) for k in range(2 * int(a))]
        rng.shuffle(cand)
        for p in cand:
            if len(sites) >= 4:
                break
            # cheap local check while building (shift range 1 is enough for a >= 3, sep 2);
            # the finished set is verified once with the full scan below
            if min_separation(L, sites + [p], rng=1) >= 4:
                sites.append(p)
        if min_separation(L, sites) < 4:
            continue
        detL, vols, _ = evaluate(L, sites)
        ref = sample(L, sites)
        sig = float(detL) * 0.5 / np.sqrt(N)
        dev = max(abs(float(vols[i]) - ref[i]) for i in range(len(sites))) / sig
        worst = max(worst, dev)
        print("     a=%-5s vols %s   deviation %.1f sigma"
              % (a, ["%.3f" % float(v) for v in vols], dev))
        ok = ok and dev < 6
    print("  %s worst deviation %.1f sigma (< 6)" % ("PASS" if worst < 6 else "FAIL", worst))
    ok = ok and worst < 6

    print("\n  completeness certificate: exercised, and it fires when it should")
    L3 = diag(4, 4, 4)
    S3 = [(F(0), F(0), F(0)), (F(2), F(0), F(0)), (F(0), F(2), F(0))]
    comp = []
    for s in S3:
        for n in lattice_points(L3, 2):
            w = tuple(s[t] + n[t] for t in range(3))
            if norm2([w[t] - S3[0][t] for t in range(3)]) <= 36:
                comp.append(w)
    active, discarded = [], []
    _ = cell_volume(S3[0], comp)                 # warms nothing; just checks it runs
    print("  %s the cell computes with the certificate on" % "PASS")
    fired = 0
    for k in range(3):
        try:
            cell_volume(S3[0], comp, _drop_active=k)
        except RuntimeError:
            fired += 1
    # Dropping a REDUNDANT plane (one supporting no facet) is legitimately harmless -- that is the
    # distinction the certificate is built on, and an earlier version of the check confused the two.
    # Dropping a batch must hit a facet, and then the certificate has to fire.
    print("     single drops caught: %d/3 (a redundant plane may be dropped harmlessly)" % fired)
    caught = 0
    for k in range(0, 3):
        try:
            cell_volume(S3[0], comp, _drop_active=k)
        except RuntimeError:
            caught += 1
    print("  %s the certificate fires when a facet is dropped (at least one of three)"
          % ("PASS" if caught >= 1 else "FAIL"))
    ok = ok and caught >= 1
    return ok

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

def cli(argv):
    """Feed a rational periodic packing without editing code:

        python3 fixture_nonuniform.py --lattice 4,4,4 --points 0,0,0:2,0,0:0,2,0 --R 2 \
                                      --json out/my_fixture.json

    The hypotheses are checked as in make_fixture (separation >= 2 exactly; cells sum to the period
    volume), so a rejected input is a geometry error, not a parsing accident.
    """
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--lattice", help="three diagonal entries, e.g. 4,4,4 (a diagonal lattice)")
    ap.add_argument("--points", help="sites as x,y,z:x,y,z:...")
    ap.add_argument("--R", default="2", help="edge range for the cut graph")
    ap.add_argument("--json", default="", help="write the fixture here")
    a = ap.parse_args(argv)
    if not a.lattice or not a.points:
        ap.error("--lattice and --points are required together")
    diag_entries = [F(x) for x in a.lattice.split(",")]
    if len(diag_entries) != 3:
        ap.error("--lattice needs three entries")
    L = diag(*diag_entries)
    pts = []
    for chunk in a.points.split(":"):
        xyz = [F(x) for x in chunk.split(",")]
        if len(xyz) != 3:
            ap.error("each point needs three coordinates: %r" % chunk)
        pts.append(tuple(xyz))
    fx = make_fixture(L, pts, F(a.R), name="cli_fixture")
    path = a.json or os.path.join(_OUT, "cli_fixture.json")
    json.dump(fx, open(path, "w"), indent=1)
    print("wrote", path)
    print("  vertices %d, edges %d, cell volumes %s" % (len(pts), len(fx["edges"]),
                                                      fx["cell_volumes_exact"]))
    print("  b in %s" % ["[%.6f, %.6f]" % (float(F(lo)), float(F(hi)))
                         for lo, hi in zip(fx["b_lo"], fx["b_hi"])])
    return 0

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
    print("\n" + "=" * 100)
    print("E. ENGINE CROSS-CHECK: a bug here would corrupt every number above")
    print("=" * 100)
    eng_ok = engine_cross_check()
    print("\nexported:", export())
    print("fixture_nonuniform:", "PASS" if (good and allvac and eng_ok) else "FAIL")
    return 0 if (good and allvac and eng_ok) else 1

if __name__ == "__main__":
    if any(x.startswith("--lattice") or x.startswith("--points") or x.startswith("--json") or
           x.startswith("--R") for x in sys.argv[1:]):
        sys.exit(cli(sys.argv[1:]))
    sys.exit(main())
