#!/usr/bin/env python3
"""K15-C131 -- does the near-contact exclusion survive FREE ORIENTATION?

Main's C128/C129 excluded two dodecahedral cells at distance d with the two icosahedra sharing the
vertex axis.  At d = 2 that is forced: each centre is a contact of the other, so the axis is a
vertex direction for BOTH icosahedra and the only freedom is a twist.

At d > 2 it is NOT forced: w's cell may be dodecahedral with v nowhere among its twelve contacts,
so w's icosahedron can sit in ANY orientation relative to the axis.  That is a 3-parameter family,
not a 1-parameter twist.  This script optimises the relative orientation for two icosahedra of
circumradius 2 at separation d, maximising the minimum cross-distance.  If that maximum reaches 2,
a legal pair of dodecahedral cells exists at that d and the near-contact band is EMPTY beyond d = 2.
"""
import sys
import numpy as np


def icosa(r=2.0):
    p = (1 + 5 ** 0.5) / 2
    v = []
    for a in (-1, 1):
        for b in (-p, p):
            v += [(0, a, b), (a, b, 0), (b, 0, a)]
    V = np.array(sorted(set(map(tuple, np.round(v, 12)))), float)
    return V / np.linalg.norm(V, axis=1)[:, None] * r


def rot(axis, ang):
    axis = np.asarray(axis, float)
    axis = axis / np.linalg.norm(axis)
    K = np.array([[0, -axis[2], axis[1]], [axis[2], 0, -axis[0]], [-axis[1], axis[0], 0]])
    return np.eye(3) + np.sin(ang) * K + (1 - np.cos(ang)) * (K @ K)


def min_cross(d, R):
    A = icosa()
    B = icosa() @ R.T + np.array([d, 0.0, 0.0])
    D = np.linalg.norm(A[:, None, :] - B[None, :, :], axis=2)
    return float(D.min())


def best_at(d, seed=0, n=4000):
    """random search over SO(3) for the orientation maximising the min cross-distance."""
    rng = np.random.default_rng(seed)
    best, arg = -1.0, None
    for _ in range(n):
        q = rng.normal(size=4)
        q /= np.linalg.norm(q)
        w, x, y, z = q
        R = np.array([
            [1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
            [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
            [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]])
        v = min_cross(d, R)
        if v > best:
            best, arg = v, R
    return best, arg


if __name__ == '__main__':
    print("two icosahedra of circumradius 2, centres d apart, FREE relative orientation")
    print("maximising the minimum cross-distance over SO(3) (random search, 4000 orientations)")
    print(f"{'d':>6} {'best min cross-dist':>20} {'legal (>= 2)?':>14}")
    for d in (2.0, 2.02, 2.05, 2.1, 2.2, 2.5, 3.0, 3.5, 4.0):
        best, _ = best_at(d)
        print(f"{d:>6.2f} {best:>20.10f} {str(best >= 2 - 1e-9):>14}")
    print()
    print("at d = 2 there is essentially no freedom (the axis is a vertex direction for both)")
    print("so this random search is a poor test there; it is the d > 2 rows that matter.")
