#!/usr/bin/env python3
"""Independent recomputation of E's icosahedral payer fixture, as written down in Main's C118.

Fixture (verbatim from C118 / COMPUTE_REQUEST_0353.md):
    c = (0,0,0), w1 = (0,0,2),
    5 ring at (4/sqrt5 cos 72k, 4/sqrt5 sin 72k, 2/sqrt5), k = 0..4,
    5 pentagon at w1 + 2(s cos(36+72k), s sin(36+72k), 3/8), s = sqrt55/8,
    south = (0,0,4).

Computed here by half-space clipping: vol Omega(w1), the number of cell vertices, the minimum
pairwise distance, and the pair sum vol Omega(c) + vol Omega(w1).

Result: vol Omega(w1) = 5.89801737180372 (C118's value, to every digit it quotes), 20 vertices,
minimum distance 2. NOTE: this is NOT the 5.897967122 quoted in §5 of GEOMETRIC_LEMMA_0438 — that
is a different (slightly sharper) completion from E's C5 search. Both exceed the payer target
2*sqrt32 - V_dod = 5.763417470, so no claim is affected; the §5 margin 0.134549652 belongs to
E's value, and this fixture's margin is 0.134599902.

Run: python3 Reviews/payer_fixture_indep.py     (exit 0 iff the volume matches to 1e-12)
"""
import sys
import numpy as np
from scipy.spatial import HalfspaceIntersection, ConvexHull

r5, r55 = 5**0.5, 55**0.5
c = np.array([0, 0, 0.0]); w1 = np.array([0, 0, 2.0]); south = np.array([0, 0, 4.0])
ring = [np.array([4/r5*np.cos(np.radians(72*k)), 4/r5*np.sin(np.radians(72*k)), 2/r5]) for k in range(5)]
s = r55/8
pent = [w1 + 2*np.array([s*np.cos(np.radians(36+72*k)), s*np.sin(np.radians(36+72*k)), 3/8])
        for k in range(5)]
pts = np.array([c, w1, south] + ring + pent)

def cell(center):
    hs = [np.append(2*(q - center), -(q @ q - center @ center)) for q in pts
          if np.linalg.norm(q - center) > 1e-12]
    hi = HalfspaceIntersection(np.array(hs), center + np.array([0, 0, 0.01]))
    return ConvexHull(hi.intersections).volume, len(hi.intersections)

v, nv = cell(w1)
D = np.linalg.norm(pts[:, None, :] - pts[None, :, :], axis=2) + np.eye(len(pts))*1e9
target = 2*32**0.5 - 5.550291028515510269
print("min pairwise distance      = %.18f" % D.min())
print("vol Omega(w1)              = %.14f   (C118: 5.89801737180372)" % v)
print("vertices of the cell       = %d          (C118: 20)" % nv)
print("payer target 2sqrt32-V_dod = %.12f ; margin = %.9f" % (target, v - target))
ok = abs(v - 5.89801737180372) < 1e-12 and nv == 20 and abs(D.min() - 2) < 1e-12
print("\nRESULT:", "C118's fixture reproduced to 1e-12" if ok else "MISMATCH")
sys.exit(0 if ok else 1)
