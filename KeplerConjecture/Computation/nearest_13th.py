#!/usr/bin/env python3
"""How close can a 13th centre get to the icosahedral twelve at radius rho?

For a direction u, the constraint |r u - x_i| >= 2 is
    r^2 - 2 r <u,x_i> + (rho^2 - 4) >= 0,
so with c = <u,x_i> the forbidden interval is (r-, r+) where
    r+ = c + sqrt(c^2 - (rho^2-4)),   defined iff c^2 >= rho^2-4.
The smallest admissible r along u is max_i r+(u,x_i), floored at rho.

If the nearest admissible p has |p| > 2*R_cell, its bisector lies outside the cell's
circumradius, so its half-space CONTAINS the cell; redundancy is per half-space, so no
set of extra points can then change the cell. That settles case (B) of K15-C101 for the
icosahedral base (K15-C102).
"""
import numpy as np
from mpmath import mp, mpf, sqrt

mp.dps = 25
RHO = 2.09
FLOOR = RHO * RHO - 4.0          # 0.3681 > 0


def ico_dirs():
    p = (1 + 5 ** 0.5) / 2
    v = []
    for a in (-1, 1):
        for b in (-p, p):
            v += [(0, a, b), (a, b, 0), (b, 0, a)]
    V = np.array(sorted(set(map(tuple, np.round(v, 12)))), float)
    return V / np.linalg.norm(V, axis=1)[:, None]


def r_plus(c):
    disc = c * c - FLOOR
    out = np.full_like(c, -np.inf)
    m = disc >= 0
    out[m] = c[m] + np.sqrt(disc[m])
    return out


def min_admissible(U, X, rho=RHO):
    """vectorised: smallest admissible r per row of U."""
    c = U @ X.T                                    # (m,12)
    rp = r_plus(c)
    r = np.maximum(rp.max(axis=1), rho)
    return r


if __name__ == '__main__':
    D = ico_dirs()
    X = D * RHO
    Dm = np.linalg.norm(X[:, None] - X[None], axis=2)
    iu = np.triu_indices(12, 1)
    Rcell = (RHO / 2) * np.sqrt(2)
    print(f"icosahedral twelve at rho = {RHO}: min mutual distance {Dm[iu].min():.9f}")
    print(f"cell circumradius = (rho/2)*sqrt2 = {Rcell:.9f};  2*R_cell = {2*Rcell:.9f}")

    # exact hole directions (dodecahedron vertices) and the 12 vertex directions
    p = (1 + 5 ** 0.5) / 2
    dd = []
    for s1 in (1, -1):
        for s2 in (1, -1):
            dd += [(0, s1 / p, s2), (s1 / p, s2, 0), (s2, 0, s1 / p)]
    Dd = np.array(sorted(set(map(tuple, np.round(dd, 12)))), float)
    Dd /= np.linalg.norm(Dd, axis=1)[:, None]
    print(f"\n{len(Dd)} dodecahedral (hole) directions")
    r_hole = min_admissible(Dd, X)
    k = int(np.argmin(r_hole))
    print(f"  nearest admissible radius among holes: {r_hole[k]:.9f}")
    r_vert = min_admissible(D, X)
    print(f"  along the 12 vertex directions:        {r_vert.min():.9f}")

    # dense random search over directions
    rng = np.random.default_rng(7)
    best = np.inf; bestu = None
    for _ in range(40):
        U = rng.normal(size=(50000, 3))
        U /= np.linalg.norm(U, axis=1)[:, None]
        r = min_admissible(U, X)
        j = int(np.argmin(r))
        if r[j] < best:
            best, bestu = r[j], U[j]
    print(f"  random search (2e6 directions):        {best:.9f}")

    # local refinement from the best random direction and from each hole
    from scipy.optimize import minimize
    def f(v):
        v = v / np.linalg.norm(v)
        return float(min_admissible(v[None, :], X)[0])
    starts = [bestu] + list(Dd) + list(D)
    glob = np.inf; gu = None
    for s in starts:
        res = minimize(f, s, method='Nelder-Mead',
                       options=dict(xatol=1e-10, fatol=1e-12, maxfev=20000))
        if res.fun < glob:
            glob, gu = res.fun, res.x / np.linalg.norm(res.x)
    print(f"  after local refinement:                {glob:.9f}")
    print(f"    direction {np.round(gu, 9)}")
    print()
    m = min(glob, best, r_hole.min())
    print(f"NEAREST ADMISSIBLE EXTRA POINT: |p| = {m:.9f}")
    print(f"  a point can cut the cell only if |p| < 2*R_cell = {2*Rcell:.9f}")
    print(f"  VERDICT: {'every extra point is REDUNDANT -> cell determined by the twelve' if m >= 2*Rcell else 'A POINT CAN CUT THE CELL'}")
