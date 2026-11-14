#!/usr/bin/env python3
"""Independent computation of the true two-dodecahedra threshold, against Main's C116.

C116 (main 8dc264e) proves: two dodecahedral cells are impossible when their centres are closer
than 6/sqrt5 = 2.683281573, and states that the sharpness is only for its own arc-cover
certificate.

This script computes the same obstruction from the other side: put v at 0 with its twelve
icosahedral neighbours at 2*u_i (u_i the twelve unit icosahedral directions) and w at d*u_0 with
its twelve neighbours at d*u_0 + 2*R_t(u_j), R_t the twist about the v-w axis. Any packing
containing two regular dodecahedral cells of inradius 1 contains such a configuration, so if some
cross-distance is < 2 for every twist, no such packing exists.

Result: max over twist of min cross-distance = 2 exactly at d = 2*phi = 3.2360679775 (twist 36
degrees), so the pairwise condition alone already forbids d < 2*phi. Since 2*phi = 1.206011 * 6/sqrt5,
C116's constant is valid but 20.6% short of what this (necessary) condition gives.

Run: python3 Reviews/near_contact_band_indep.py    (exit 0 iff the threshold is 2*phi to 1e-9)
"""
import sys
import numpy as np
from scipy.optimize import minimize_scalar

phi = (1 + 5**0.5)/2
V = []
for s1 in (1, -1):
    for s2 in (1, -1):
        V += [(0, s1, s2*phi), (s1, s2*phi, 0), (s2*phi, 0, s1)]
V = np.array(sorted(set(V)), float); V = V/np.linalg.norm(V[0])
u0 = V[0]

a, b = V[1], -u0
ax = np.cross(a, b); ax /= np.linalg.norm(ax); ang = np.arccos(np.clip(a @ b, -1, 1))
def rot(axis, an):
    c, s = np.cos(an), np.sin(an); x, y, z = axis
    return np.array([[c+x*x*(1-c), x*y*(1-c)-z*s, x*z*(1-c)+y*s],
                     [y*x*(1-c)+z*s, c+y*y*(1-c), y*z*(1-c)-x*s],
                     [z*x*(1-c)-y*s, z*y*(1-c)+x*s, c+z*z*(1-c)]])
A0 = rot(ax, ang)

def mincross(d, t):
    w = d*u0
    R = np.array([rot(u0, t) @ (A0 @ r) for r in V])
    return min(np.linalg.norm(d*V[i] - (w + 2*R[j]))
               for i in range(12) if i != 0 for j in range(12) if j != 1)

def best(d):
    ts = np.linspace(0, 2*np.pi/5, 481)
    vals = [mincross(d, t) for t in ts]
    k = int(np.argmax(vals))
    lo, hi = ts[max(k-1, 0)], ts[min(k+1, len(ts)-1)]
    r = minimize_scalar(lambda t: -mincross(d, t), bounds=(lo, hi), method='bounded',
                        options={'xatol': 1e-14})
    return -r.fun, r.x

d = 2*phi
v, t = best(d)
print("d = 2*phi      = %.15f" % d)
print("max over twist of the min cross-distance = %.15f  at twist %.6f deg" % (v, np.degrees(t)))
print("6/sqrt5        = %.12f   (C116's constant)" % (6/5**0.5))
print("ratio 2phi/(6/sqrt5) = %.6f" % (2*phi/(6/5**0.5)))
low, _ = best(d - 1e-6); high, _ = best(d + 1e-6)
print("just below: %.12f   just above: %.12f  (clean crossing)" % (low, high))
ok = abs(v - 2) < 1e-9 and low < 2 < high
print("\nRESULT:", "threshold is 2*phi to 1e-9; C116's constant is valid but not sharp" if ok else "CHECK FAILED")
sys.exit(0 if ok else 1)
