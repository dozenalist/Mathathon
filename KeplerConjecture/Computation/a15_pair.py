#!/usr/bin/env python3
"""K15-C111 -- independent check of E's A15 (Cr3Si) row: minimum pair sum 15.875.

A15 / Pm-3n, 8 sites per cubic cell of side a = 4 (nearest B-B chain distance a/2 = 2).
Uses the adaptive truncation of Main's Lemma 3 (BARLOW_CELLS.md): start from a few nearest
centres, then verify no centre within 2*R_cell can cut the cell, expanding only if needed.
"""
import itertools
import sys
import numpy as np
from scipy.spatial import ConvexHull

SQ32 = np.sqrt(32.0)
A = 4.0
SITES = [(0, 0, 0), (0.5, 0.5, 0.5),
         (0.25, 0.0, 0.5), (0.5, 0.25, 0.0), (0.0, 0.5, 0.25),
         (0.75, 0.0, 0.5), (0.5, 0.75, 0.0), (0.0, 0.5, 0.75)]


def build(n):
    pts = []
    for i in range(-n, n + 1):
        for j in range(-n, n + 1):
            for k in range(-n, n + 1):
                base = np.array([i, j, k], float) * A
                for s in SITES:
                    pts.append(base + np.array(s, float) * A)
    return np.array(pts)


def cell_from(centre, cand, tol=1e-9):
    """Voronoi cell of `centre` against the centres in `cand` (already truncated)."""
    ns = []
    for c in cand:
        d = np.asarray(c, float) - np.asarray(centre, float)
        r2 = d @ d
        if r2 < 1e-14:
            continue
        ns.append(2.0 * d / r2)
    ns = np.array(ns)
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
        return np.inf, None, ns
    V = np.array(V)
    _, idx = np.unique(np.round(V, 9), axis=0, return_index=True)
    V = V[np.sort(idx)]
    if len(V) < 4:
        return np.inf, V, ns
    return ConvexHull(V).volume, V, ns


def adaptive_vol(centre, allpts, k0=20, grow=15, kmax=400):
    """volume of the cell, with Lemma 3 certifying that the truncation is complete."""
    d = np.linalg.norm(allpts - np.asarray(centre, float), axis=1)
    order = np.argsort(d)
    k = k0
    while k <= kmax:
        cand = allpts[order[:k]]
        vol, V, ns = cell_from(centre, cand)
        if V is None or len(V) < 4:
            k += grow
            continue
        R = float(np.max(np.linalg.norm(V, axis=1)))
        # every excluded centre within 2R must not cut
        far = order[k:]
        far = far[d[far] <= 2 * R + 1e-9]
        worst = -np.inf
        for idx in far:
            c = allpts[idx] - np.asarray(centre, float)
            n = 2.0 * c / (c @ c)
            worst = max(worst, float(np.max(V @ n) - 1.0))
        if worst <= 1e-9:
            return vol, R, k, worst
        k += grow
    return np.nan, np.nan, k, np.nan


def main():
    P = build(1)
    D = np.linalg.norm(P[:, None] - P[None], axis=2)
    np.fill_diagonal(D, np.inf)
    ms = float(D.min())
    print(f"sites: {len(P)}   min separation {ms:.6f}   (a/2 = {A/2})")
    if abs(ms - 2) > 1e-9:
        print("  WARNING: scaling wrong")
        return 1
    vols = {}
    for s in SITES:
        c = np.array(s, float) * A
        v, R, k, w = adaptive_vol(c, P)
        vols[s] = v
        print(f"  site {str(s):22s} vol = {v:.9f}  R_cell = {R:.4f}  "
              f"truncation k = {k}  slack {w:+.1e}")
    tot = sum(vols.values())
    print(f"\nsum over the 8 sites = {tot:.9f}   (a^3 = {A ** 3:.1f})")
    Bs = [s for s in SITES if s not in ((0, 0, 0), (0.5, 0.5, 0.5))]
    As = [(0, 0, 0), (0.5, 0.5, 0.5)]
    vb = [vols[s] for s in Bs]
    va = [vols[s] for s in As]
    print(f"  B volumes equal? {max(vb) - min(vb) < 1e-6}   "
          f"A volumes equal? {max(va) - min(va) < 1e-6}")
    # contacts: B-B along a chain at a/2 = 2 (A-B is 2.236, A-A is 3.464)
    pair = 2 * (sum(vb) / len(vb))
    print(f"\nB-B contact pair sum = 2*vol_B = {pair:.9f}")
    print(f"  vs 2*sqrt32 = {2 * SQ32:.9f}   difference {pair - 2 * SQ32:+.9f}")
    print(f"  E's A15 row quotes 15.875000000   difference {pair - 15.875:+.9f}")
    ok = pair >= 2 * SQ32 - 1e-6
    print(f"\n(P') holds on A15: {ok}")
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
