#!/usr/bin/env python3
"""Can a 13th (or 14th) point at distance >= 2.09 cut the scaled dodecahedral cell?

The 12 icosahedral points at radius rho give the dodecahedron scaled by rho/2, volume
V_dod (rho/2)^3 = 6.333804 at rho = 2.09, which is 12% ABOVE sqrt(32). So the singleton
closed component is excluded *if* no configuration does better. This probe asks whether
adding points can bring the cell below sqrt(32).
"""
import itertools
import numpy as np
from scipy.optimize import minimize

SQ32 = np.sqrt(32.0)
VDOD = 5.550291028515510


def vol_cell(P, tol=1e-9):
    P = np.asarray(P, float)
    if len(P) < 4:
        return np.inf
    ns = 2.0 * P / np.sum(P * P, axis=1)[:, None]
    V = []
    for i, j, k in itertools.combinations(range(len(ns)), 3):
        M = ns[[i, j, k]]
        try:
            p = np.linalg.solve(M, np.ones(3))
        except np.linalg.LinAlgError:
            continue
        if np.all(ns @ p <= 1.0 + tol):
            V.append(p)
    if len(V) < 4:
        return np.inf
    V = np.array(V)
    _, idx = np.unique(np.round(V, 9), axis=0, return_index=True)
    V = V[np.sort(idx)]
    if len(V) < 4:
        return np.inf
    from scipy.spatial import ConvexHull
    return ConvexHull(V).volume


def ico_dir():
    p = (1 + 5 ** 0.5) / 2
    v = []
    for a in (-1, 1):
        for b in (-p, p):
            v += [(0, a, b), (a, b, 0), (b, 0, a)]
    V = np.array(sorted(set(map(tuple, np.round(v, 12)))), float)
    return V / np.linalg.norm(V, axis=1)[:, None]


def dodeca_dir():
    p = (1 + 5 ** 0.5) / 2
    v = [(0, 1 / p, p), (0, -1 / p, p), (0, 1 / p, -p), (0, -1 / p, -p)]
    for s in (1, -1):
        for t in (1, -1):
            v += [(s / p, p, 0), (s / p, -p, 0), (p, 0, s / p), (-p, 0, s / p)]
    V = np.array(sorted(set(map(tuple, np.round(v, 12)))), float)
    return V / np.linalg.norm(V, axis=1)[:, None]


def probe(rho, extra_radii, verbose=True):
    I = ico_dir()
    D = dodeca_dir()
    base = rho * I
    v0 = vol_cell(base)
    if verbose:
        print(f"rho = {rho}")
        print(f"  12 icosahedral at rho:            vol = {v0:.9f}  "
              f"(V_dod (rho/2)^3 = {VDOD*(rho/2)**3:.9f})  vs sqrt32 {v0/SQ32-1:+.4%}")
    # one extra point, swept over radii along the 20 face-centre directions (dodeca dirs)
    best = (v0, None)
    for r in extra_radii:
        for d in D:
            p = r * d
            # must be >= 2 from all icosahedral points
            if np.min(np.linalg.norm(base - p, axis=1)) < 2.0 - 1e-12:
                continue
            v = vol_cell(np.vstack([base, p]))
            if v < best[0] - 1e-12:
                best = (v, (r, tuple(np.round(d, 6))))
    if verbose:
        if best[1] is None:
            print("  no extra point in a face-centre direction is admissible "
                  "AND cuts the cell")
        else:
            print(f"  best with one extra point:        vol = {best[0]:.9f} "
                  f"({best[0]/SQ32-1:+.4%} vs sqrt32) at r={best[1][0]:.3f}")
    return v0, best


if __name__ == '__main__':
    for rho in (2.0127, 2.09, 2.2):
        rs = np.arange(rho, 4.01, 0.005)
        probe(rho, rs)
        print()
