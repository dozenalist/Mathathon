#!/usr/bin/env python3
"""K15-C118 -- independent reproduction of E's frozen payer fixture value 5.898017372.

E's construction (COMPUTE_REQUEST_0353.md, commit c76194f, quoted verbatim):
    fixture  c=(0,0,0), w1=(0,0,2), 5 ring at (4/sqrt5 cos 72k, 4/sqrt5 sin 72k, 2/sqrt5),
             5 pentagon at w1 + 2(s cos(36+72k), s sin(36+72k), 3/8), s = sqrt55/8,
             south=(0,0,4)

Main recomputes the Voronoi cell of w1 from those thirteen points with its own code (adaptive
truncation + triple enumeration), independently of E's scripts, and checks the two numbers E
quotes: the min separation over all pairs, and vol Omega(w1).
"""
import itertools
import sys
from mpmath import mp, mpf, sqrt, cos, sin, pi

mp.dps = 40
SQ32 = float(sqrt(mpf(32)))
REQUIRED = 5.763417470
E_FROZEN = 5.898017371803720
E_FAMILY = 5.898007181138


def fixture(theta_deg=None, cos_theta=None):
    """E's thirteen points.  Default: E's frozen fixture (cos theta = -3/8 -> z = +3/4)."""
    s5 = sqrt(mpf(5))
    c = (mpf(0), mpf(0), mpf(0))
    w1 = (mpf(0), mpf(0), mpf(2))
    ring = [(4 / s5 * mp.cos(2 * pi * k / 5), 4 / s5 * mp.sin(2 * pi * k / 5), 2 / s5)
            for k in range(5)]
    s = sqrt(mpf(55)) / 8
    if cos_theta is not None:
        zc = 2 * cos_theta
        rc = sqrt(4 - zc ** 2)
        pent = [(rc * mp.cos((36 + 72 * k) * pi / 180),
                 rc * mp.sin((36 + 72 * k) * pi / 180),
                 2 + zc) for k in range(5)]
    else:
        pent = [(2 * s * mp.cos((36 + 72 * k) * pi / 180),
                 2 * s * mp.sin((36 + 72 * k) * pi / 180),
                 2 + 2 * mpf(3) / 8) for k in range(5)]
    south = (mpf(0), mpf(0), mpf(4))
    return [c, w1] + ring + pent + [south]


def vol_cell(centre, pts, tol=1e-30):
    ns = []
    for c in pts:
        d = [mpf(a) - mpf(b) for a, b in zip(c, centre)]
        r2 = d[0] ** 2 + d[1] ** 2 + d[2] ** 2
        if r2 < mpf('1e-40'):
            continue
        ns.append([2 * t / r2 for t in d])
    V = []
    for i, j, k in itertools.combinations(range(len(ns)), 3):
        M = [ns[i], ns[j], ns[k]]
        det = (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1])
               - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
               + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))
        if det == 0:
            continue
        rhs = [mpf(1)] * 3
        sol = []
        for col in range(3):
            N = [[M[r][cc] for cc in range(3)] for r in range(3)]
            for r in range(3):
                N[r][col] = rhs[r]
            dd = (N[0][0] * (N[1][1] * N[2][2] - N[1][2] * N[2][1])
                  - N[0][1] * (N[1][0] * N[2][2] - N[1][2] * N[2][0])
                  + N[0][2] * (N[1][0] * N[2][1] - N[1][1] * N[2][0]))
            sol.append(dd / det)
        if all(sum(n[t] * sol[t] for t in range(3)) <= 1 + mpf('1e-30') for n in ns):
            V.append(tuple(sol))
    V = sorted(set(V))
    if len(V) < 4:
        return mpf(0), 0
    # A fan triangulation over arbitrary vertex pairs does NOT tile a convex polytope
    # (Main's first attempt overcounted by ~11x).  Use the convex hull instead.
    import numpy as np
    from scipy.spatial import ConvexHull
    arr = np.array([[float(t) for t in v] for v in V])
    hull = ConvexHull(arr)
    return mpf(repr(hull.volume)), len(V)


def main():
    P = fixture()
    print(f"fixture points: {len(P)}  (c, w1, 5 ring, 5 pentagon, south pole)")
    dmin, arg = min((( sqrt(sum((a - b) ** 2 for a, b in zip(P[i], P[j]))), (i, j))
                     for i in range(len(P)) for j in range(i + 1, len(P))), key=lambda t: t[0])
    legal = dmin >= 2 - mpf('1e-15')
    print(f"min separation over all {len(P)*(len(P)-1)//2} pairs = {mp.nstr(dmin, 20)}"
          f"   legal (>= 2 - 1e-15): {legal}")
    print(f"  (attained at pair {arg})")
    vol, nv = vol_cell((mpf(0), mpf(0), mpf(2)), P)
    print()
    print(f"vol Omega(w1) = {mp.nstr(vol, 15)}   ({nv} cell vertices)")
    print(f"E's frozen value       5.898017371803720")
    print(f"difference             {mp.nstr(vol - mpf('5.898017371803720'), 6)}")
    print(f"(P') required payer    5.763417470")
    print(f"margin over required   {mp.nstr(vol - mpf('5.763417470'), 10)}")
    ok = abs(float(vol) - float(mpf('5.898017371803720'))) < 1e-9 and legal
    print()
    print("VERDICT:", "REPRODUCED" if ok else "DOES NOT MATCH E")
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
