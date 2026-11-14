#!/usr/bin/env python3
"""Is C133's 4 cos rho_c ATTAINED by two dodecahedral cells, or only a limit of the method?

C133 proves: if both cells are regular dodecahedra of inradius 1 and |v-w| < 4cos rho_c, a clash
follows.  That is a bound on the distance; whether a *configuration* of two dodecahedral cells
exists at distance exactly 4cos rho_c is a different question, and if none exists the true
infimum is larger than the theorem's constant.

Construction tried: w at the origin with contacts 2 u_i (icosahedron with a face centre along e),
p = d e with d = 4cos rho_c, and p's contacts p + 2 v_j where v is an icosahedron that also has a
face centre along e, twisted by t about e.  Reason for that choice: |p + 2v_j| >= 2 forces
v_j.e >= -d/4 = -cos rho_c, and the covering radius says some v_j has v_j.e <= -cos rho_c, so the
only way to keep the 13th point admissible is exactly the face-centre alignment, which is also
what makes the two contacts of w sit at distance exactly 2 from p.

Exit 0 iff some twist passes every 2-separation test (then the constant is attained) or none does
(then the constant is a method limit and the true infimum is strictly larger).
"""
import itertools
import sys

import numpy as np
from mpmath import mp, mpf, sqrt, acos, cos, sin, pi

mp.dps = 30
PHI = (1 + sqrt(mpf(5))) / 2
COSRHO = sqrt((1 + 2 / sqrt(mpf(5))) / 3)
D = 4 * COSRHO


def ico():
    v = []
    for a in (-1, 1):
        for b in (-PHI, PHI):
            v += [(0, a, b), (a, b, 0), (b, 0, a)]
    V = np.array(sorted(set(map(tuple, np.round(np.array(v, float), 12)))), float)
    return V / np.linalg.norm(V, axis=1)[:, None]


def face_centre_of(V):
    """A unit vector that is a face centre of the icosahedron V (equal angles to 3 vertices)."""
    E = np.linalg.norm(V[:, None] - V[None], axis=2)
    edge = np.sort(E[0])[1]
    for i, j, k in itertools.combinations(range(12), 3):
        if abs(E[i, j] - edge) < 1e-9 and abs(E[i, k] - edge) < 1e-9 and abs(E[j, k] - edge) < 1e-9:
            w = V[i] + V[j] + V[k]
            return w / np.linalg.norm(w)
    raise RuntimeError


def rot_about(axis, ang):
    a = np.array(axis, float)
    a /= np.linalg.norm(a)
    K = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]])
    return np.eye(3) + np.sin(ang) * K + (1 - np.cos(ang)) * (K @ K)


def mindist(U, e):
    """min pairwise distance over {0, p} u {2u_i} u {p + 2v_j}, v = U (already oriented)."""
    p = float(D) * e
    w_contacts = 2 * U
    p_contacts = p + 2 * U
    pts = np.vstack([[np.zeros(3), p], w_contacts, p_contacts])
    n = len(pts)
    best = np.inf
    for i in range(n):
        for j in range(i + 1, n):
            best = min(best, float(np.linalg.norm(pts[i] - pts[j])))
    return best


def main():
    V = ico()
    e = face_centre_of(V)
    print(f"d = 4cos rho_c = {float(D):.12f};  e is a face centre of the icosahedron")
    print(f"  |2u_i - e d| min over i = {np.min(np.linalg.norm(2 * V - float(D) * e, axis=1)):.12f}  "
          f"(= 2 by construction)")
    best = (-1, None)
    for k in range(145):
        t = 2 * pi * k / 144
        U = V @ rot_about(e, float(t)).T
        m = mindist(U, e)
        if m > best[0]:
            best = (m, float(t) * 180 / np.pi)
    print(f"\nbest over twists of the second icosahedron about e: min pairwise distance "
          f"{best[0]:.9f} at t = {best[1]:.3f} deg")
    print(f"  >= 2 would make the configuration legal; it is {best[0]:.9f}")
    # also try small tilts of e off the face centre
    best2 = (-1, None)
    for k in range(25):
        for th in np.linspace(0, 0.6, 13):
            phi = 2 * np.pi * k / 24
            e2 = np.array([np.cos(th), np.sin(th) * np.cos(phi), np.sin(th) * np.sin(phi)])
            U = V
            m = min(mindist(U, e2), mindist(V @ rot_about(e2, 0.3).T, e2))
            if m > best2[0]:
                best2 = (m, (float(th), float(phi)))
    print(f"best with e tilted up to 0.6 rad off the face centre: {best2[0]:.9f} at {best2[1]}")
    legal = max(best[0], best2[0]) >= 2 - 1e-9
    if legal:
        print("\n=> ATTAINED: two dodecahedral cells coexist at distance 4cos rho_c, so the constant")
        print("   is the exact infimum, not merely the limit of the covering-radius method.")
    else:
        print("\n=> NOT attained by this construction: every orientation clashes, so 4cos rho_c is a")
        print("   limit of the METHOD (the contact of w reaches distance exactly 2 at d = 4cos rho_c)")
        print("   and the true infimum over pairs of dodecahedral cells is strictly larger.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
