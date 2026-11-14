#!/usr/bin/env python3
"""Independent check of the A15 row that Main corrected after the audit target (C111 / c4134c2).

The audited §5 table listed "A15 | 10098 | 15.875 | above". Main later found that 15.875 is the
sum for an A-B pair, and that A-B is at distance sqrt5 = 2.236, not a contact: the contacts in A15
are the B-B chain bonds at a/2 = 2, giving 2*(129/16) = 16.125.

This script computes the eight Voronoi cells of the Cr3Si (A15, cP8) structure directly by
half-space clipping, with a = 4 so that the nearest distance a/2 = 2 is exact.

Result: the two A sites have volume 125/16 = 7.8125 each, the six B sites 129/16 = 8.0625 each,
the weighted sum is 2*125/16 + 6*129/16 = 64 = a^3 exactly, the minimum site distance is a/2 = 2,
and the A-B distance is sqrt5 = 2.2360679... So Main's correction is right and the table's 15.875
was the wrong pair type.

Run: python3 Reviews/a15_pair_indep.py     (exit 0 iff the volumes and the distances match)
"""
import itertools, sys
import numpy as np
from scipy.spatial import HalfspaceIntersection, ConvexHull

a = 4.0
A = np.array([[0, 0, 0], [0.5, 0.5, 0.5]])*a
B = np.array([[0.25, 0, 0.5], [0.75, 0, 0.5], [0.5, 0.25, 0], [0.5, 0.75, 0],
              [0, 0.5, 0.25], [0, 0.5, 0.75]])*a
base = np.vstack([A, B])
pts = np.array([p + a*np.array(s) for s in itertools.product((-1, 0, 1), repeat=3) for p in base])

def cell_vol(c):
    hs = []
    for q in pts:
        if np.linalg.norm(q - c) < 1e-9: continue
        n = q - c
        if np.linalg.norm(n) > 2.5*a: continue
        hs.append(np.append(2*n, -(q @ q - c @ c)))
    hi = HalfspaceIntersection(np.array(hs), c + np.array([1e-3, 1e-3, 1e-3]))
    return ConvexHull(hi.intersections).volume

vA = [cell_vol(c) for c in A]
vB = [cell_vol(c) for c in B]
print("A15 (Cr3Si, cP8), a = %.0f (nearest distance a/2 = 2)" % a)
print("  A volumes: %s   (125/16 = %.7f)" % (", ".join("%.7f" % v for v in vA), 125/16))
print("  B volumes: %s   (129/16 = %.7f)" % (", ".join("%.7f" % v for v in vB), 129/16))
print("  weighted sum = %.9f   a^3 = %.9f" % (sum(vA) + sum(vB), a**3))
D = np.linalg.norm(base[:, None, :] - base[None, :, :], axis=2) + np.eye(8)*1e9
print("  min site distance = %.9f (a/2 = %.1f);  A-B distance = %.9f (sqrt5 = %.9f)"
      % (D.min(), a/2, np.linalg.norm(A[0]-B[0]), 5**0.5))
print("  contact pairs are B-B at a/2 = 2, so the contact-pair sum is 2*129/16 = %.6f" % (2*129/16))
ok = (all(abs(v - 125/16) < 1e-9 for v in vA) and all(abs(v - 129/16) < 1e-9 for v in vB)
      and abs(sum(vA)+sum(vB) - a**3) < 1e-9 and abs(D.min() - 2) < 1e-9)
print("\nRESULT:", "A15 volumes confirmed; 15.875 is the A-B sum, not a contact pair" if ok else "FAILED")
sys.exit(0 if ok else 1)
