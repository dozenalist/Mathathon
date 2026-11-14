#!/usr/bin/env python3
"""A 'gap' packing: two fcc half-spaces separated by a clean crack.

Purpose (K15-C095): an UNBOUNDED closed component of the 2.09-graph exists, is
saturated, and is harmless for the cut condition -- which is why C089's
'a closed component gives t* = inf' must be restricted to BOUNDED components.

Lower half: fcc layers at z = k*H, k <= 0, offset s_k = k mod 3.
Upper half: fcc layers at z = d + k*H, k >= 0, offset s_k = (shift + k) mod 3.
"""
import numpy as np

A1 = np.array([2.0, 0.0])
A2 = np.array([1.0, np.sqrt(3.0)])
T = (A1 + A2) / 3.0
H = np.sqrt(8.0 / 3.0)


def build(d, shift, span=8, nlow=6, nup=6):
    pts = []
    grp = []
    for k in range(-nlow, 1):                       # lower half, k <= 0
        base = (k % 3) * T
        for i in range(-span, span + 1):
            for j in range(-span, span + 1):
                xy = i * A1 + j * A2 + base
                pts.append((xy[0], xy[1], k * H)); grp.append(0)
    for k in range(0, nup + 1):                     # upper half
        base = ((shift + k) % 3) * T
        for i in range(-span, span + 1):
            for j in range(-span, span + 1):
                xy = i * A1 + j * A2 + base
                pts.append((xy[0], xy[1], d + k * H)); grp.append(1)
    return np.array(pts), np.array(grp)


def minsep(d, shift):
    P, g = build(d, shift, span=4, nlow=4, nup=4)
    best = np.inf
    bestpair = None
    n = len(P)
    for i in range(n):
        dd = np.linalg.norm(P - P[i], axis=1)
        dd[i] = np.inf
        j = int(np.argmin(dd))
        if dd[j] < best:
            best, bestpair = dd[j], (tuple(P[i]), tuple(P[j]))
    return best, bestpair


def covering_radius(d, shift, rng, ns=40000):
    P, _ = build(d, shift, span=6, nlow=5, nup=5)
    pts = np.column_stack([rng.uniform(-2, 2, ns), rng.uniform(-2, 2, ns),
                           rng.uniform(-2 * H, d + 2 * H, ns)])
    best = np.full(ns, np.inf)
    for c in P:
        best = np.minimum(best, np.linalg.norm(pts - c, axis=1))
    return float(best.max())


def cross_gap_min(d, shift, span=6):
    """min distance between a lower-half and an upper-half site."""
    P, g = build(d, shift, span=span, nlow=5, nup=5)
    lo, hi = P[g == 0], P[g == 1]
    best = np.inf
    for a in lo[-40 * 1:]:
        pass
    # cheap: only sites near the crack matter
    lo = lo[lo[:, 2] > -1e-9]
    hi = hi[hi[:, 2] < d + H + 1e-9]
    for a in lo:
        best = min(best, float(np.min(np.linalg.norm(hi - a, axis=1))))
    return best


if __name__ == '__main__':
    rng = np.random.default_rng(7)
    print(f"H = {H:.6f};  saturation needs d <= {2*np.sqrt(4-(2/np.sqrt(3))**2):.6f}")
    print(f"  (minimum cross distance 2 needs d >= {np.sqrt(4-4/3):.6f} with a 2/3 offset)")
    for d in (1.633, 1.8, 2.0, 2.09, 2.2, 2.4, 2.8, 3.2):
        ms, pair = minsep(d, 1)
        cg = cross_gap_min(d, 1)
        cr = covering_radius(d, 1, rng, ns=20000)
        ok_sep = ms >= 2.0 - 1e-9
        ok_cov = cr <= 2.0 + 1e-9
        print(f"  d={d:5.3f}: min separation {ms:.6f} {'OK' if ok_sep else 'FAIL'}"
              f" | min cross-gap {cg:.6f} {'closed@2.09' if cg > 2.09 else 'EDGES'}"
              f" | sampled covering radius {cr:.6f} {'OK' if ok_cov else 'NOT SATURATED'}"
              f" | saturated&closed: {ok_sep and ok_cov and cg > 2.09}")
