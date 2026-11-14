#!/usr/bin/env python3
"""The icosahedral-cluster fixture: what a finite completion can and cannot show.

K15-C036 claims that no finite completion can verify the pointwise inequality
    sum_w phi(v,w) >= sqrt(32) - vol Omega(v)
because cells computed inside a completion are UPPER bounds for the cells in any
packing containing the cluster (more bisectors only shrink).  This script exhibits
the mechanism numerically:

  1. build the 13-cluster (centre + 12 icosahedral neighbours at distance 2);
  2. complete it with further 2-separated points, all at distance >= 2.6 from the
     centre, so they cannot cut the centre's cell (its circumradius is 1.2584, and
     a point at distance d cuts only within d/2 >= 1.3);
  3. compute every cell inside the completion (scipy half-space intersection);
  4. report vol Omega(centre) (should stay 5.550291...) and
     sum_{v in K} (vol Omega_K(v) - sqrt32) as the completion grows.

The sets are nested as the completion radius DECREASES (each keeps the points at
distance >= rad), so the cells shrink monotonically and the reported sum decreases.
Every value is an upper bound for the packing value, so a positive sum at any
finite stage proves nothing about the packing: monotonicity is the whole point.

Usage: python3 cluster_fixture.py
"""
import itertools, math, sys
import numpy as np
from scipy.spatial import HalfspaceIntersection

SQ32 = math.sqrt(32.0)


def icosahedron():
    phi = (1 + math.sqrt(5)) / 2
    pts = []
    for a, b in ((0, 1), (0, -1), (1, 0), (-1, 0)):
        pass
    # 12 vertices of the icosahedron, circumradius 1
    v = []
    for s1 in (1, -1):
        for s2 in (1, -1):
            v.append((0, s1 * 1, s2 * phi))
            v.append((s1 * 1, s2 * phi, 0))
            v.append((s1 * phi, 0, s2 * 1))
    v = np.array(v, dtype=float)
    return v / np.linalg.norm(v[0])


def cell_volume(points, i, box=6.0):
    """Volume of the Voronoi cell of points[i] inside the cube [-box,box]^3."""
    p = points[i]
    # half spaces: (x - m).(q - p) <= 0  for each other point q, m = midpoint
    rows = []
    for j, q in enumerate(points):
        if j == i:
            continue
        n = q - p
        rows.append(np.concatenate([n, [-n @ ((p + q) / 2)]]))
    # box constraints keep the cell bounded
    for k in range(3):
        e = np.zeros(3); e[k] = 1
        rows.append(np.concatenate([e, [-box]]))
        rows.append(np.concatenate([-e, [-box]]))
    hs = np.array(rows)
    # find an interior point by averaging nearby points and shrinking toward p
    interior = p + 0.05 * np.mean(points - p, axis=0)
    for _ in range(50):
        if np.all(hs[:, :3] @ interior + hs[:, 3] <= -1e-9):
            break
        interior = 0.5 * (interior + p)
    else:
        return 0.0
    try:
        hi = HalfspaceIntersection(hs, interior)
    except Exception:
        return 0.0
    from scipy.spatial import ConvexHull
    if len(hi.intersections) < 4:
        return 0.0
    return ConvexHull(hi.intersections).volume


def completion(centre, radius, core=None, extent=6, spacing=2.2):
    """2-separated lattice points at distance >= radius from the centre.

    Two conditions are ESSENTIAL and were missing from the first version:
      * distance >= 2 from every CORE point (otherwise the "completion" overlaps
        the cluster and the point set is not a packing at all), and
      * distance >= 2.5188 from the centre, so the centre's cell is not cut.
    The lattice EXTENT is fixed so the sets are nested as `radius` decreases.
    """
    out = []
    steps = np.arange(-extent, extent + 1) * spacing
    for x in steps:
        for y in steps:
            for z in steps:
                q = np.array([x, y, z]) + centre
                if np.linalg.norm(q - centre) < max(radius, 2.5188):
                    continue
                if core is not None and len(core) and np.min(np.linalg.norm(core - q, axis=1)) < 2 - 1e-9:
                    continue
                out.append(q)
    return np.array(out) if out else np.zeros((0, 3))


def main():
    ico = icosahedron()
    centre = np.zeros(3)
    core = np.vstack([centre[None, :], 2.0 * ico])
    print("13-cluster: centre + 12 at distance %.6f, min mutual %.6f"
          % (np.linalg.norm(core[1]), min(np.linalg.norm(core[i] - core[j])
                                          for i in range(1, 13) for j in range(i + 1, 13))))
    v_core = cell_volume(core, 0)
    print("vol Omega(centre) inside the bare 13-cluster (box-truncated): %.6f  (sqrt32 = %.6f)"
          % (v_core, SQ32))
    # NB: completion(rad) keeps points at distance >= rad, so the sets are NESTED
    # as rad DECREASES.  Iterating 5.0 -> 3.5 -> 2.6 adds points at each step,
    # which is what makes the comparison a test of monotonicity.
    for rad in (5.0, 3.5, 2.7):
        ext = completion(centre, rad, core=core)
        pts = np.vstack([core, ext]) if len(ext) else core
        # VALIDATION (required before any claim about this fixture): the whole
        # point set must be a genuine packing, so the minimum over ALL pairs --
        # core-core, core-background AND background-background -- must be >= 2.
        from scipy.spatial.distance import pdist
        dmin = float(pdist(pts).min()) if len(pts) > 1 else 0.0
        assert dmin >= 2 - 1e-9, "completion is not a packing: min separation %.6f" % dmin
        vols = [cell_volume(pts, i) for i in range(13)]
        s = sum(v - SQ32 for v in vols)
        print("completion radius %.1f (%4d extra points): min sep %.4f, centre %.6f, sum_K(vol - sqrt32) = %+.6f"
              % (rad, len(ext), dmin, vols[0], s))
    print("\nMonotonicity: every entry above is an UPPER bound for the packing value, so a")
    print("positive sum at a finite stage cannot certify the inequality (K15-C036).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
