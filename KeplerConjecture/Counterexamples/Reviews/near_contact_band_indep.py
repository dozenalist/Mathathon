#!/usr/bin/env python3
"""Independent computation of the two-dodecahedra threshold, against Main's C116.

C116 (main 8dc264e) proves two dodecahedral cells are impossible when their centres are closer
than 6/sqrt5 = 2.683281573, and says the sharpness is only for its own arc-cover certificate.

Configuration (the same as X-C043, with the separation free): v at the origin with its twelve
icosahedral neighbours at 2*u_i (u_i the twelve unit icosahedral directions); w at d*u_0 with its
twelve neighbours at d*u_0 + 2*R_t(u_j), R_t the twist about the v-w axis. Any packing containing
two regular dodecahedral cells of inradius 1 contains such a configuration, so if a cross-distance
is < 2 for every twist, no such packing exists.

Result: max over twist of the min cross-distance reaches 2 exactly at

        d* = 3.4555003444...

(twist 36 degrees), and at d* no other centre cuts either cell, so two dodecahedral cells really
are attainable there. Hence the threshold is d*, and C116's 6/sqrt5 is valid but 28.8% short
(d*/2.6832816 = 1.2878).

CORRECTION RECORDED: the first version of this script scaled v's ring by d as well (d*V[i]
instead of 2*V[i]), which produced a spurious "2*phi = 3.236068". That claim was pushed as
X-C051 and is withdrawn; the number below is the corrected one, with v's ring fixed at radius 2.

Run: python3 Reviews/near_contact_band_indep.py     (exit 0 iff d* is reproducible to 1e-6)
"""
import itertools, sys
import numpy as np
from scipy.optimize import minimize_scalar, brentq

phi = (1 + 5**0.5)/2
N = []
for s1 in (1, -1):
    for s2 in (1, -1):
        N += [(0, s1, s2*phi), (s1, s2*phi, 0), (s2*phi, 0, s1)]
N = np.array(sorted(set(N)), float); N = N/np.linalg.norm(N[0])
verts = []
for i, j, k in itertools.combinations(range(12), 3):
    A = np.array([N[i], N[j], N[k]])
    if abs(np.linalg.det(A)) < 1e-9: continue
    x = np.linalg.solve(A, np.ones(3))
    if np.all(N @ x <= 1 + 1e-9): verts.append(x)
VD = np.array(sorted({tuple(np.round(v, 12)) for v in verts}))
hD = lambda u: (VD @ u).max()

u0 = N[0]
a, b = N[1], -u0
ax = np.cross(a, b); ax /= np.linalg.norm(ax); ang = np.arccos(np.clip(a @ b, -1, 1))
def rot(axis, an):
    c, s = np.cos(an), np.sin(an); x, y, z = axis
    return np.array([[c+x*x*(1-c), x*y*(1-c)-z*s, x*z*(1-c)+y*s],
                     [y*x*(1-c)+z*s, c+y*y*(1-c), y*z*(1-c)-x*s],
                     [z*x*(1-c)-y*s, z*y*(1-c)+x*s, c+z*z*(1-c)]])
A0 = rot(ax, ang)

def mincross(d, t):
    w = d*u0
    R = np.array([rot(u0, t) @ (A0 @ r) for r in N])
    return min(np.linalg.norm(2*N[i] - (w + 2*R[j]))          # v's ring FIXED at radius 2
               for i in range(12) if i != 0 for j in range(12) if j != 1)
def best(d):
    ts = np.linspace(0, 2*np.pi/5, 721)
    vals = [mincross(d, t) for t in ts]
    k = int(np.argmax(vals)); lo, hi = ts[max(k-1, 0)], ts[min(k+1, len(ts)-1)]
    r = minimize_scalar(lambda t: -mincross(d, t), bounds=(lo, hi), method='bounded',
                        options={'xatol': 1e-14})
    return -r.fun, r.x

dstar = brentq(lambda d: best(d)[0] - 2.0, 2.0, 4.5, xtol=1e-10)
v, t = best(dstar)
print("threshold d* = %.10f   (min cross-distance %.10f at twist %.4f deg)"
      % (dstar, v, np.degrees(t)))
print("C116's 6/sqrt5 = %.10f ;  d*/2.6832816 = %.6f" % (6/5**0.5, dstar/(6/5**0.5)))
w = dstar*u0; R = np.array([rot(u0, t) @ (A0 @ r) for r in N])
cuts = lambda z: np.linalg.norm(z) > 1e-9 and hD(z/np.linalg.norm(z)) > np.linalg.norm(z)/2 + 1e-12
ncut = sum(cuts(z) for z in [w] + [w + 2*R[j] for j in range(12) if j != 1])
print("centres cutting v's cell at d*: %d (0 means the two cells are attainable)" % ncut)
ok = abs(dstar - 3.4555003444) < 1e-6 and ncut == 0 and abs(v - 2) < 1e-9
print("\nRESULT:", "d* = 3.4555003 reproduced, attainable, C116 28.8%% short" if ok else "CHECK FAILED")
sys.exit(0 if ok else 1)
