#!/usr/bin/env python3
"""The two close-packed local cell types, computed directly: both have volume sqrt32 and
circumradius sqrt2, which is what EXPOSITION_0438 §2 asserts and what the §5 table's
"equality" rows for fcc and hcp require.

  fcc: Voronoi cell of the origin in {sqrt2 (m,n,p) : m+n+p even}  -> rhombic dodecahedron
  hcp: triangular layers of spacing 2 stacked ABAB at h = sqrt(8/3)

Run: python3 Reviews/fcc_hcp_cells_indep.py     (exit 0 iff both are sqrt32 with circumradius sqrt2)
"""
import sys
import numpy as np
from scipy.spatial import HalfspaceIntersection, ConvexHull

S32, S2 = 32**0.5, 2**0.5
def cell(pts, c):
    hs = []
    for q in pts:
        if np.linalg.norm(q - c) < 1e-9 or np.linalg.norm(q - c) > 6: continue
        hs.append(np.append(2*(q - c), -(q @ q - c @ c)))
    hi = HalfspaceIntersection(np.array(hs), c + np.array([0.05, 0.05, 0.05]))
    X = hi.intersections
    n = int((np.linalg.norm(pts - c, axis=1) < 2 + 1e-9).sum()) - 1
    return ConvexHull(X).volume, np.linalg.norm(X - c, axis=1).max(), n

s2 = 2**0.5; s3 = 3**0.5
fcc = np.array([s2*np.array([m, n, p], float) for m in range(-3, 4) for n in range(-3, 4)
                for p in range(-3, 4) if (m + n + p) % 2 == 0])
h = (8/3)**0.5
a1 = np.array([2.0, 0, 0]); a2 = np.array([1.0, s3, 0]); A = np.zeros(3); B = (a1 + a2)/3.0
hcp = []
for k in range(-3, 4):
    off = B if k % 2 else A
    for i in range(-3, 4):
        for j in range(-3, 4):
            hcp.append(i*a1 + j*a2 + np.array([0, 0, k*h]) + off)
hcp = np.array(hcp)

fails = []
def ck(t, c, d=""):
    print("  [%s] %-46s %s" % ("OK" if c else "BAD", t, d))
    if not c: fails.append(t)

v, R, n = cell(fcc, np.zeros(3))
ck("fcc cell volume = sqrt32", abs(v - S32) < 1e-9, "%.12f, circumradius %.9f, %d contacts" % (v, R, n))
ck("fcc cell circumradius = sqrt2", abs(R - S2) < 1e-9)
for name, c in (("hcp A site", A), ("hcp B site", B + np.array([0, 0, h]))):
    v, R, n = cell(hcp, c)
    ck("%s volume = sqrt32" % name, abs(v - S32) < 1e-9, "%.12f, circumradius %.9f, %d contacts" % (v, R, n))
    ck("%s circumradius = sqrt2" % name, abs(R - S2) < 1e-9)
print("\nRESULT:", "both close-packed cell types confirmed" if not fails else "FAILED: %s" % fails)
sys.exit(0 if not fails else 1)
