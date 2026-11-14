"""Fast float implementation of the seven-colouring (independent of the exact code).

Lattice d(Z + Z omega); colour (m + 2n) mod 7.  Nearest lattice point found by
testing the nine integer candidates around (u,v) and comparing |.|^2 exactly
(|u e1 + v e2|^2 = D^2 (u^2 + v^2 - uv), since the angle between e1,e2 is 120 deg).
"""
import numpy as np

D = 2 * np.sqrt(3) / 5
W3 = np.sqrt(3)


def lattice_coords(x, y):
    """(m,n) of the nearest lattice point, vectorised."""
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    v = 2 * y / (D * W3)
    u = x / D + v / 2
    u0, v0 = np.round(u), np.round(v)
    best = None
    bm = bn = None
    for i in (-1, 0, 1):
        for j in (-1, 0, 1):
            m = u0 + i
            n = v0 + j
            du = u - m
            dv = v - n
            dd = du * du + dv * dv - du * dv
            if best is None:
                best, bm, bn = dd, m, n
            else:
                better = dd < best
                best = np.where(better, dd, best)
                bm = np.where(better, m, bm)
                bn = np.where(better, n, bn)
    return bm.astype(np.int64), bn.astype(np.int64)


def colour_arr(x, y):
    m, n = lattice_coords(x, y)
    return (m + 2 * n) % 7
