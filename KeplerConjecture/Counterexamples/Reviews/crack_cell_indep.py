#!/usr/bin/env python3
"""Independent recomputation of the crack-packing cell volume quoted in §5 of
GEOMETRIC_LEMMA_0438.md (6.985) and used by C095.

Construction (m2's explicit form): Lambda_eps = {(2i + (k mod 2), 2j + (k mod 2),
k*sqrt2 + eps*[k>=1]) : i,j,k in Z}, i.e. fcc layers stacked with spacing sqrt2, the upper
half-space translated by eps in z.

Checked here by explicit half-space clipping + hull volumes:
  * min pairwise distance is exactly 2 for every eps >= 0 (within-layer),
  * eps = 0 gives the fcc cell, volume sqrt32 = 5.656854249492 exactly,
  * the facing-layer cell has volume sqrt32 + 2*eps exactly (6.656854249 at eps = 1/2),
  * eps = 0.664073 reproduces the file's 6.985 to five decimals (6.985000249).

Run: python3 Reviews/crack_cell_indep.py     (exit 0 iff the four statements hold)
"""
import sys
import numpy as np
from scipy.spatial import HalfspaceIntersection, ConvexHull

s2 = 2**0.5
S32 = 32**0.5
def build(eps, K=3, L=2):
    pts = []
    for k in range(-K, K+1):
        for i in range(-L, L+1):
            for j in range(-L, L+1):
                pts.append((2*i + (k % 2), 2*j + (k % 2), k*s2 + (eps if k >= 1 else 0.0)))
    return np.array(pts, float)

def cell_volume(eps):
    P = build(eps); v = np.zeros(3)
    hs = []
    for q in P:
        if np.linalg.norm(q) < 1e-12: continue
        if np.linalg.norm(q - v) >= 4.5: continue
        hs.append(np.append(2*(q - v), -(q @ q)))
    hi = HalfspaceIntersection(np.array(hs), v + np.array([0, 0, 0.001]))
    return ConvexHull(hi.intersections).volume, np.linalg.norm(hi.intersections - v, axis=1).max()

def min_dist(eps):
    P = build(eps)
    D = np.linalg.norm(P[:, None, :] - P[None, :, :], axis=2) + np.eye(len(P))*1e9
    return D.min()

fails = []
def ck(t, c, d=""):
    print("  [%s] %-58s %s" % ("OK" if c else "BAD", t, d))
    if not c: fails.append(t)

v0, R0 = cell_volume(0.0)
ck("eps=0 is fcc: cell volume = sqrt32", abs(v0 - S32) < 1e-9, "%.12f" % v0)
ck("eps=0: min distance = 2", abs(min_dist(0.0) - 2) < 1e-12)
for eps in (0.5, 0.664073):
    vol, R = cell_volume(eps)
    ck("eps=%.6f: facing cell = sqrt32 + 2 eps" % eps, abs(vol - (S32 + 2*eps)) < 1e-9,
       "%.12f (sqrt32+2eps = %.12f), circumradius %.6f" % (vol, S32 + 2*eps, R))
    ck("eps=%.6f: min distance = 2" % eps, abs(min_dist(eps) - 2) < 1e-12)
print("\nRESULT:", "crack cell volumes confirmed" if not fails else "FAILED: %s" % fails)
sys.exit(0 if not fails else 1)
