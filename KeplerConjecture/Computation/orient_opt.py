#!/usr/bin/env python3
"""K15-C131 -- local optimisation over SO(3): can two icosahedra of radius 2 sit legally at d > 2?"""
import numpy as np
from scipy.optimize import minimize


def icosa(r=2.0):
    p = (1 + 5 ** 0.5) / 2
    v = []
    for a in (-1, 1):
        for b in (-p, p):
            v += [(0, a, b), (a, b, 0), (b, 0, a)]
    V = np.array(sorted(set(map(tuple, np.round(v, 12)))), float)
    return V / np.linalg.norm(V, axis=1)[:, None] * r


A = icosa()


def rotvec(t):
    th = np.linalg.norm(t)
    if th < 1e-12:
        return np.eye(3)
    k = t / th
    K = np.array([[0, -k[2], k[1]], [k[2], 0, -k[0]], [-k[1], k[0], 0]])
    return np.eye(3) + np.sin(th) * K + (1 - np.cos(th)) * (K @ K)


def f(t, d):
    B = A @ rotvec(t).T + np.array([d, 0.0, 0.0])
    D = np.linalg.norm(A[:, None, :] - B[None, :, :], axis=2)
    return -D.min()


def best(d, starts=60, seed=1):
    rng = np.random.default_rng(seed)
    bb, bt = 1e9, None
    for s in range(starts):
        t0 = rng.normal(size=3) * (2.0 if s else 0.0)
        res = minimize(f, t0, args=(d,), method='Nelder-Mead',
                       options=dict(maxfev=4000, xatol=1e-10, fatol=1e-12))
        if res.fun < bb:
            bb, bt = res.fun, res.x
    return -bb, bt


if __name__ == '__main__':
    print("local optimisation over SO(3) (60 starts), maximising the min cross-distance")
    print(f"{'d':>6} {'best min cross-dist':>20} {'legal?':>8}")
    for d in (2.0, 2.02, 2.1, 2.2, 2.5, 3.0, 3.5, 4.0):
        v, t = best(d)
        print(f"{d:>6.2f} {v:>20.10f} {str(v >= 2 - 1e-9):>8}")
