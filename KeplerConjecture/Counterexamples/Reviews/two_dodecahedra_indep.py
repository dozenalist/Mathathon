#!/usr/bin/env python3
"""Independent recomputation of Theorem D step 4 (two adjacent dodecahedral cells), and the
resolution of the E/Main discrepancy that GEOMETRIC_LEMMA_0438.md records as unresolved.

Configuration.  A regular dodecahedron of inradius 1 has 12 faces whose outward normals are the
12 vertices of an icosahedron.  So a dodecahedral cell at v forces its 12 contacts at 2*u_i,
u_i the 12 unit icosahedral directions.  Put v = 0 and let w = 2*u_0 (so v and w are a contact
pair).  For w's cell to be dodecahedral as well, w's 12 contacts must be at w + 2*R*u_j where R
is a rotation carrying one icosahedral direction to -u_0 (the contact back to v).  The remaining
freedom is a twist t about the v-w axis; the configuration has period 72 degrees.

What is computed:  m(t) = min over pairs (v's other 11 contacts, w's other 11 contacts) of the
distance.  Two dodecahedra are compatible iff there is t with m(t) >= 2 (every other pair is
automatically >= 2: within a ring by construction, and v-to-w's-ring is 2|u_0 + R u_j| >= 2).

Result (this script):  sup_t m(t) = 1.125554844510 at t = 36 deg, so no twist works: the
shortfall is 0.8744.  Main's number 1.12555484451 is confirmed to 12 digits.

The E/Main discrepancy, resolved.  The document records E's K15-E075 value 1.056487696 "versus"
Main's 1.12555484451 and calls it unreconciled.  Both are values of the SAME function m:
m(33.636862 deg) = m(38.363138 deg) = 1.056487696 exactly as quoted, while sup m = 1.1255548.
So E sampled another twist (or the mirror family); neither is wrong, and Main's is the supremum
over the twist family, hence the one that makes step 4 strongest.  The four values Main tabulates
at 0,18,36,54 deg are the same multiset as m at 36,54,0,18 deg (Main's twist origin is shifted by
36 deg from the one used here).

Run:  python3 Reviews/two_dodecahedra_indep.py     (exit 0 iff sup > 1 and < 2)
"""
import itertools, sys
import numpy as np
from scipy.optimize import brentq, minimize_scalar

phi = (1 + 5**0.5)/2
V = []
for s1 in (1, -1):
    for s2 in (1, -1):
        V += [(0, s1, s2*phi), (s1, s2*phi, 0), (s2*phi, 0, s1)]
V = np.array(sorted(set(V)), float); V = V/np.linalg.norm(V[0])
u0, w = V[0], 2*V[0]

a, b = V[1], -u0
ax = np.cross(a, b); ax /= np.linalg.norm(ax); ang = np.arccos(np.clip(a @ b, -1, 1))
def rot(axis, an):
    c, s = np.cos(an), np.sin(an); x, y, z = axis
    return np.array([[c+x*x*(1-c), x*y*(1-c)-z*s, x*z*(1-c)+y*s],
                     [y*x*(1-c)+z*s, c+y*y*(1-c), y*z*(1-c)-x*s],
                     [z*x*(1-c)-y*s, z*y*(1-c)+x*s, c+z*z*(1-c)]])
A0 = rot(ax, ang)

def mincross(t):
    R = np.array([rot(u0, t) @ (A0 @ r) for r in V])
    return min(np.linalg.norm(2*V[i] - (w + 2*R[j]))
               for i in range(12) if i != 0 for j in range(12) if j != 1)

ts = np.linspace(0, 2*np.pi/5, 2001)
vals = np.array([mincross(t) for t in ts])
k = int(np.argmax(vals))
lo, hi = ts[max(k-1, 0)], ts[min(k+1, len(ts)-1)]
r = minimize_scalar(lambda t: -mincross(t), bounds=(lo, hi), method='bound2') if False else \
    minimize_scalar(lambda t: -mincross(t), bounds=(lo, hi), method='bounded', options={'xatol': 1e-13})
sup = -r.fun
print("sup over twist of the min cross-distance : %.12f  at t = %.6f deg"
      % (sup, np.degrees(r.x)))
print("Main, two_dodecahedra.py                  : 1.12555484451")
print("required for two dodecahedral cells       : 2")
for deg in (0, 18, 36, 54):
    print("  m(%2d deg) = %.9f" % (deg, mincross(np.radians(deg))))
E = 1.056487696
hits = []
ts2 = np.linspace(0, np.radians(72), 20001); v2 = np.array([mincross(t) for t in ts2])
for i in range(len(ts2)-1):
    if (v2[i]-E)*(v2[i+1]-E) < 0:
        hits.append(np.degrees(brentq(lambda t: mincross(t)-E, ts2[i], ts2[i+1], xtol=1e-14)))
print("E's 1.056487696 is attained at t = %s deg  (so it is m at another twist, not a rival value)"
      % ", ".join("%.6f" % h for h in hits))
ok = 1 < sup < 2 and abs(sup - 1.125554844510) < 1e-9
print("\nRESULT:", "step 4 stands (sup < 2) and Main's constant is confirmed" if ok else "CHECK FAILED")
sys.exit(0 if ok else 1)
