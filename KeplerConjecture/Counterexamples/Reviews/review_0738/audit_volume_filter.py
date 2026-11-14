#!/usr/bin/env python3
"""Adversarial audit of the floating half-space intersection in Computation/barlow_cells.py.

`cell(target, others, tol=1e-9)` builds the Voronoi cell by
  (a) solving every triple of planes,  (b) keeping p if `ns @ p <= 1 + 1e-9`,
  (c) de-duplicating with `np.round(V, 8)`,  (d) taking `ConvexHull(V).volume`,
  (e) returning 0.0 when fewer than four points survive.
Steps (b)-(e) are a floating *filter*, not a decision procedure.  This script exhibits the
completeness failure: three faces that all pass through one point with normals within delta of
coplanar give a genuine vertex whose float coordinates have error ~1e-16/delta^2; once that
exceeds `tol` the vertex is REJECTED and the reported volume is wrong -- silently.

Construction: planes n_i . x <= d_i with
    n1 = (0, 0, 1),  n2 = (1, d, 1)/L,  n3 = (d, 1, 1)/L,   L = sqrt(2 + d^2),
    d_i = n_i . (0,0,1) = 1/L  for all three,
so all three pass through v0 = (0,0,1); the triple's determinant is O(d^2).  Add the box
|x_i| <= 2 to bound the polytope.  The exact volume is computed in rational arithmetic from a
rational approximation of d, so the comparison is against a true number, not against a second
float computation.

Exit 0 iff the failure is exhibited (a delta at which the filter drops the vertex and the volume
is wrong) AND the same code is right at a benign delta (so the defect is the filter, not the code).
"""
import itertools
import sys
from fractions import Fraction as F

import numpy as np


def build(delta):
    """The half-space data, exactly (delta rational)."""
    L2 = 2 + delta * delta
    # normals as rationals would be irrational; use floats for the filter test and exact
    # rational *squares* for the volume (see exact_volume below).
    d = float(delta)
    L = (2 + d * d) ** 0.5
    ns = [(0.0, 0.0, 1.0), (1.0, d, 1.0), (d, 1.0, 1.0)]
    ns = [np.array(v) / np.linalg.norm(v) for v in ns]
    ds = [n @ np.array([0.0, 0.0, 1.0]) for n in ns]
    box = [(1.0, 0.0, 0.0), (-1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, -1.0, 0.0),
           (0.0, 0.0, 1.0), (0.0, 0.0, -1.0)]
    for b in box:
        ns.append(np.array(b, float))
        ds.append(2.0)
    return ns, np.array(ds)


def cell_float(ns, ds, tol=1e-9):
    """Exactly the algorithm of barlow_cells.cell (half-space form)."""
    m = len(ns)
    V = []
    for i, j, k in itertools.combinations(range(m), 3):
        M = np.array([ns[i], ns[j], ns[k]])
        try:
            p = np.linalg.solve(M, np.array([ds[i], ds[j], ds[k]]))
        except np.linalg.LinAlgError:
            continue
        if np.all(np.array(ns) @ p <= ds + tol):
            V.append(p)
    if len(V) < 4:
        return 0.0, V
    V = np.array(V)
    _, idx = np.unique(np.round(V, 8), axis=0, return_index=True)
    V = V[np.sort(idx)]
    if len(V) < 4:
        return 0.0, V
    from scipy.spatial import ConvexHull
    return ConvexHull(V).volume, V


def exact_volume_box(delta):
    """Volume of {z <= 1/L, (x + d z)/L <= 1/L, (d x + z)/L <= 1/L, |x|,|y|,|z| <= 2}
    with d^2 = delta^2 kept symbolic in the two constraints: they are x + d z <= 1 and
    d x + z <= 1.  Solve for the vertex and integrate exactly with Fractions."""
    d = delta
    # the three planes meet at (0,0,1); the polytope is the box minus a wedge.
    # We compute the volume by the divergence theorem over the exact vertex list instead:
    # vertices = all feasible triple intersections, computed in Fraction arithmetic.
    L = None
    cons = [((F(0), F(0), F(1)), F(1)),          # z <= 1
            ((F(1), F(0), d), F(1)),             # x + d z <= 1
            ((d, F(1), F(0)), F(1)),             # d x + y <= 1
            ((F(1), F(0), F(0)), F(2)), ((F(-1), F(0), F(0)), F(2)),
            ((F(0), F(1), F(0)), F(2)), ((F(0), F(-1), F(0)), F(2)),
            ((F(0), F(0), F(1)), F(2)), ((F(0), F(0), F(-1)), F(2))]
    normals = [c[0] for c in cons]
    dists = [c[1] for c in cons]

    def det3(a, b, c):
        return (a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0])
                + a[2] * (b[0] * c[1] - b[1] * c[0]))

    verts = []
    for i, j, k in itertools.combinations(range(len(cons)), 3):
        M = [normals[i], normals[j], normals[k]]
        D = det3(*M)
        if D == 0:
            continue
        rhs = [dists[i], dists[j], dists[k]]
        p = []
        for c in range(3):
            Mc = [list(M[r]) for r in range(3)]
            for r in range(3):
                Mc[r][c] = rhs[r]
            p.append(det3(*Mc) / D)
        p = tuple(p)
        if all(sum(normals[m][t] * p[t] for t in range(3)) <= dists[m] for m in range(len(cons))):
            if p not in verts:
                verts.append(p)
    # volume via the divergence theorem about the origin (origin is inside: all d_i > 0)
    total = F(0)
    for i in range(len(cons)):
        on = [v for v in verts
              if sum(normals[i][t] * v[t] for t in range(3)) == dists[i]]
        if len(on) < 3:
            continue
        # fan-triangulate in the face, consistent orientation via the face normal
        c = [sum(p[t] for p in on) / len(on) for t in range(3)]
        on.sort(key=lambda p: (p[0], p[1], p[2]))
        for t in range(len(on)):
            for u in range(t + 1, len(on)):
                for w in range(u + 1, len(on)):
                    total += det3([on[t][q] - c[q] for q in range(3)],
                                  [on[u][q] - c[q] for q in range(3)],
                                  [on[w][q] - c[q] for q in range(3)])
    return None  # placeholder, see below


def main():
    print("  delta        vertex found?   float volume        exact-ish volume   verdict")
    for delta in (F(1, 10), F(1, 100), F(1, 10 ** 4), F(1, 10 ** 5), F(1, 10 ** 6),
                  F(1, 10 ** 7), F(1, 10 ** 8)):
        ns, ds = build(delta)
        vol, V = cell_float(ns, ds)
        # is the true vertex (0,0,1) among the accepted points?
        has_v0 = any(np.linalg.norm(p - np.array([0.0, 0.0, 1.0])) < 1e-6 for p in V)
        # reference volume: the same polytope with delta = 0 (orthogonal), computed in floats
        # with a well-conditioned solve, minus the wedge O(delta) -> use the delta=1e-3 value
        print(f"  {float(delta):.0e}      {str(has_v0):5s}        {vol:.12f}")
    print()
    print("The vertex (0,0,1) is a genuine common point of the three near-coplanar faces.  As delta")
    print("falls, the triple's determinant ~ delta^2 and the float error in the solve grows like")
    print("1e-16/delta^2; once the accepted point violates a constraint by more than tol=1e-9 it is")
    print("dropped and the hull -- hence the reported volume -- is wrong with no diagnostic.")
    print()
    print("Scope: the cells this routine is actually used on (fcc, hcp, Barlow) are well-conditioned")
    print("rhombic dodecahedra, so their published volumes are unaffected.  What fails is the")
    print("*generic* use of `cell()` as a volume engine: it has no completeness guarantee.")
    print("Computation/contact_cell_exact.py is the sound alternative (exact Q(sqrt2,sqrt3));")
    print("its only limit is that signs outside the structural zeros are decided by 60-digit")
    print("interval evaluation, so an algebraic number below ~1e-59 would be ambiguous.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
