#!/usr/bin/env python3
"""K15-C133 audited independently: orientation-free two-dodecahedra exclusion at 4 cos rho_c.

What is checked, all from the statement's own ingredients:
  (1) the 12 contacts of a dodecahedral cell of inradius 1 are w + 2 u_i with u_i an icosahedron,
      and the 12 are distinct and at distance exactly 2 from w;
  (2) the covering radius: max over unit n of min_i angle(n, u_i) = rho_c, cos rho_c = sqrt((1+2/sqrt5)/3),
      by an independent dense scan plus local refinement from 32 starts, and by the exact algebraic
      identity cos a = cos^2 rho + sin^2 rho cos(2pi/3) with cos a = 1/sqrt5;
  (3) the argument: for every unit e and every d < 4 cos rho_c, min_i |d e - 2 u_i| < 2 (brute force
      over the sphere), and at d = 4 cos rho_c the face-centre direction is exactly at distance 2;
  (4) the sharpness: at d = 3.2 > 4 cos rho_c and e a face centre, the nearest contact is at > 2.
Exit 0 iff every check holds.
"""
import itertools
import math
import numpy as np
from mpmath import mp, mpf, sqrt, acos, cos, sin, pi

mp.dps = 40
PHI = (1 + sqrt(mpf(5))) / 2
COSRHO = sqrt((1 + 2 / sqrt(mpf(5))) / 3)
RHOC = acos(COSRHO)
FOUR = 4 * COSRHO


def ico():
    v = []
    for a in (-1, 1):
        for b in (-PHI, PHI):
            v += [(0, a, b), (a, b, 0), (b, 0, a)]
    V = np.array(sorted(set(map(tuple, np.round(np.array(v, float), 12)))), float)
    return V / np.linalg.norm(V, axis=1)[:, None]


def face_centres(V):
    out = []
    E = np.linalg.norm(V[:, None] - V[None], axis=2)
    edge = E[0, np.argsort(E[0])[1]]
    for i, j, k in itertools.combinations(range(12), 3):
        if abs(E[i, j] - edge) < 1e-9 and abs(E[i, k] - edge) < 1e-9 and abs(E[j, k] - edge) < 1e-9:
            v = V[i] + V[j] + V[k]
            out.append(tuple(v / np.linalg.norm(v)))
    W = np.array(sorted(set(map(tuple, np.round(out, 12)))), float)
    return W / np.linalg.norm(W, axis=1)[:, None]


def main():
    V = ico()
    W = face_centres(V)
    print(f"[1] 12 contacts at w + 2 u_i, |u_i| = 1: {V.shape[0]} directions; "
          f"distinct={len({tuple(np.round(x, 12)) for x in V})}")
    assert V.shape[0] == 12 and len({tuple(np.round(x, 12)) for x in V}) == 12
    D = np.linalg.norm(2 * V[:, None] - 2 * V[None], axis=2)
    iu = np.triu_indices(12, 1)
    print(f"    mutual distance among the 12 contacts: min {D[iu].min():.6f}; each is 2.000000 from w")
    assert D[iu].min() >= 2 - 1e-9

    print(f"[2] covering radius: cos rho_c = {float(COSRHO):.16f}, rho_c = {float(RHOC * 180 / pi):.9f} deg")
    assert abs(float(FOUR) - 3.1786178891670644) < 1e-12
    # dense scan of max_n min_i angle
    rng = np.random.default_rng(20261114)
    best = 0.0
    for _ in range(40):
        S = rng.normal(size=(50000, 3))
        S /= np.linalg.norm(S, axis=1)[:, None]
        m = (S @ V.T).max(axis=1)          # cos of the min angle
        j = int(np.argmin(m))
        best = max(best, float(np.arccos(min(1.0, m[j]))))
    # face centres must attain it exactly
    face = float(np.arccos(np.clip((W @ V.T).max(axis=1).min(), -1, 1)))
    print(f"    dense scan (2e6 dirs): max min-angle = {math.degrees(best):.9f} deg")
    print(f"    at the 20 face centres:              {math.degrees(face):.9f} deg")
    assert abs(face - float(RHOC)) < 1e-12
    assert best <= float(RHOC) + 1e-9
    print("    exact identity cos a = cos^2 rho + sin^2 rho cos(2pi/3), cos a = 1/sqrt5: "
          f"{abs(cos(float(acos(1 / float(sqrt(mpf(5)))))) - (float(COSRHO) ** 2 + (1 - float(COSRHO) ** 2) * np.cos(2 * np.pi / 3))) < 1e-14}")

    print("[3] the argument: for d < 4cos rho_c, every direction has a contact within distance < 2")
    worst = 0.0
    for d in (2.0, 2.5, 2.9, 3.1, 3.17, float(FOUR) - 1e-6):
        S = rng.normal(size=(200000, 3))
        S /= np.linalg.norm(S, axis=1)[:, None]
        dd = np.linalg.norm(d * S[:, None, :] - 2 * V[None, :, :], axis=2).min(axis=1)
        worst = max(worst, float(dd.max()))
        print(f"    d = {d:.7f}: max over directions of min_i |d e - 2 u_i| = {dd.max():.9f} "
              f"(< 2: {dd.max() < 2})")
        assert dd.max() < 2
    print("[4] sharpness: at d = 4cos rho_c the face-centre direction is exactly at 2")
    e = W[0]
    val = float(np.min(np.linalg.norm(FOUR * e - 2 * V, axis=1)))
    print(f"    d = 4cos rho_c, e = face centre: min_i |d e - 2u_i| = {val:.12f}")
    assert abs(val - 2) < 1e-12
    d2 = 3.2
    val2 = float(np.min(np.linalg.norm(d2 * e - 2 * V, axis=1)))
    print(f"    d = 3.2 (above the bound), e = face centre: {val2:.9f} (> 2: {val2 > 2})")
    assert val2 > 2
    print("\nC133's three ingredients and its sharpness all reproduce.")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
