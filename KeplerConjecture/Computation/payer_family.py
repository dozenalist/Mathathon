#!/usr/bin/env python3
"""K15-C120 -- scan E's C5 pentagon family: is the payer margin a window or a knife-edge?

E's K15-E085/K15-E086 claim: for the pentagon at radius exactly 2, azimuth 36+72k, plus the south
pole, every legal polar angle in [106,120] deg gives Omega(w1) with exactly twelve faces, the
family minimum over the 1-degree grid is 5.898007181 at 112 deg, and the continuous optimum is
5.897967122 at (theta,phi) = (111.7975, 36).  Main recomputes the family from the construction
instead of citing it.

Parameter: z-offset dz of the pentagon above w1 (the frozen fixture has dz = +3/4, which
corresponds to E's cos(theta) = -3/8 with theta measured from the inward direction).
"""
import itertools
import sys
import numpy as np
from mpmath import mp, mpf, sqrt, cos, sin, pi
from scipy.spatial import ConvexHull

mp.dps = 30
REQUIRED = 5.763417470


def build(dz, phi_deg=36.0):
    s5 = sqrt(mpf(5))
    c = (mpf(0), mpf(0), mpf(0))
    w1 = (mpf(0), mpf(0), mpf(2))
    ring = [(4 / s5 * mp.cos(2 * pi * k / 5), 4 / s5 * mp.sin(2 * pi * k / 5), 2 / s5)
            for k in range(5)]
    r = sqrt(4 - dz * dz)
    pent = [(r * mp.cos((phi_deg + 72 * k) * pi / 180),
             r * mp.sin((phi_deg + 72 * k) * pi / 180), 2 + dz) for k in range(5)]
    south = (mpf(0), mpf(0), mpf(4))
    return [c, w1] + ring + pent + [south]


def cell(centre, pts, tol=1e-25):
    ns = []
    for cc in pts:
        d = [mpf(a) - mpf(b) for a, b in zip(cc, centre)]
        r2 = d[0]**2 + d[1]**2 + d[2]**2
        if r2 < mpf('1e-40'):
            continue
        ns.append([2 * t / r2 for t in d])
    V = []
    for i, j, k in itertools.combinations(range(len(ns)), 3):
        M = [ns[i], ns[j], ns[k]]
        det = (M[0][0]*(M[1][1]*M[2][2]-M[1][2]*M[2][1])
               - M[0][1]*(M[1][0]*M[2][2]-M[1][2]*M[2][0])
               + M[0][2]*(M[1][0]*M[2][1]-M[1][1]*M[2][0]))
        if det == 0:
            continue
        sol = []
        for col in range(3):
            N = [[M[r][cc] for cc in range(3)] for r in range(3)]
            for r in range(3):
                N[r][col] = mpf(1)
            dd = (N[0][0]*(N[1][1]*N[2][2]-N[1][2]*N[2][1])
                  - N[0][1]*(N[1][0]*N[2][2]-N[1][2]*N[2][0])
                  + N[0][2]*(N[1][0]*N[2][1]-N[1][1]*N[2][0]))
            sol.append(dd / det)
        if all(sum(n[t]*sol[t] for t in range(3)) <= 1 + mpf('1e-25') for n in ns):
            V.append(tuple(sol))
    V = sorted(set(V))
    if len(V) < 4:
        return mpf(0), 0, 0
    arr = np.array([[float(t) for t in v] for v in V])
    hull = ConvexHull(arr)
    nfaces = len(hull.simplices)
    vol = mpf(repr(hull.volume))
    # count FACES of the cell = distinct supporting planes actually met (equivalently, distinct
    # hull facet normals grouped).  Use the active-halfspace count instead: more robust.
    active = 0
    for n in ns:
        mx = max(sum(n[t]*v[t] for t in range(3)) for v in V)
        if mx >= 1 - 1e-12:
            active += 1
    return vol, len(V), active


def legality(P):
    d = min(sqrt(sum((a - b)**2 for a, b in zip(P[i], P[j])))
            for i in range(len(P)) for j in range(i+1, len(P)))
    return d


def main():
    print("scanning the pentagon z-offset dz (frozen fixture dz = 0.75)")
    print(f"{'dz':>7} {'min sep':>10} {'legal':>6} {'vol':>14} {'verts':>6} {'faces':>6}")
    best = None
    legal_window = []
    for i in range(-18, 19):
        dz = mpf(i) / 20
        P = build(dz)
        d = legality(P)
        ok = d >= 2 - mpf('1e-12')
        if ok:
            legal_window.append(float(dz))
        vol, nv, nf = cell((mpf(0), mpf(0), mpf(2)), P)
        tag = "" if ok else "  illegal"
        print(f"{float(dz):>7.2f} {float(d):>10.4f} {str(ok):>6} {float(vol):>14.9f} "
              f"{nv:>6} {nf:>6}{tag}")
        if ok and (best is None or vol < best[0]):
            best = (vol, dz)
    print()
    print(f"legal dz window: [{min(legal_window):+.2f}, {max(legal_window):+.2f}]"
          f"  ({len(legal_window)} of 37 sampled)")
    print(f"family minimum on the sample: vol = {float(best[0]):.9f} at dz = {float(best[1]):+.2f}")
    print(f"  E's grid min 5.898007181 at theta = 112 deg (dz = 0.75); "
          f"E's continuous optimum 5.897967122")
    print(f"  required 5.763417470; margin {float(best[0]) - REQUIRED:.9f}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
