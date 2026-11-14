#!/usr/bin/env python3
"""K15-C131 -- when does a LEGAL placement of two dodecahedral cells exist at separation d?

At d = 2 the second centre is a CONTACT of the first, so the axis is a vertex direction of BOTH
icosahedra: only a twist is free (C128/C129).  At d > 2 the second icosahedron may be in ANY
orientation, giving a 3-parameter family -- the point the review raises.

Necessary condition for a legal placement: every point b of w's twelve (on the sphere of radius 2
about (d,0,0)) must be at distance >= 2 from every a of v's twelve.  For fixed a that forbids a
spherical cap of angular radius theta_a on w's sphere:

    |b - a| >= 2   with |b - (d,0,0)| = 2   <=>   cos(angle between (b - w) and (a - w)) <= (|a-w|^2 + 4 - 4) / (2*2*|a-w|)
                                               i.e.  cos <= |a - w| / 4 .

So the forbidden cap has angular radius arccos(|a-w|/4) around the direction from w to a.  If the
twelve caps COVER w's sphere, no legal placement exists.  This computes the covering threshold.
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


A = icosa()


def caps_cover(d, ndir=200000, seed=3):
    """fraction of w's sphere covered by the twelve forbidden caps."""
    w = np.array([d, 0.0, 0.0])
    dirs = A - w
    r = np.linalg.norm(dirs, axis=1)
    # forbidden cap around dirs[i] with cos(angle) <= r[i]/4
    ok = r <= 4.0                      # if r > 4 the cap is empty (point too far to forbid anything)
    if not ok.any():
        return 0.0
    dirs = dirs[ok] / r[ok][:, None]
    thr = r[ok] / 4.0                  # cos threshold
    rng = np.random.default_rng(seed)
    u = rng.normal(size=(ndir, 3))
    u /= np.linalg.norm(u, axis=1)[:, None]
    C = u @ dirs.T                     # (ndir, ncaps) cosines
    inside = (C >= thr[None, :]).any(axis=1)
    return float(inside.mean())


if __name__ == '__main__':
    print("fraction of w's sphere forbidden by the twelve caps (1.0 = no legal placement)")
    print(f"{'d':>6} {'covered fraction':>18} {'no legal placement?':>20}")
    for d in (2.0, 2.1, 2.2, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0):
        fr = caps_cover(d)
        print(f"{d:>6.2f} {fr:>18.6f} {str(fr >= 0.9999):>20}")
