#!/usr/bin/env python3
"""K15-C123 -- two adjacent dodecahedral centres impossible for ALL twists, RIGOROUS INNER arcs.

Rounding direction, which Main got wrong once and which the review caught:
  * v1 sampled a twist grid                                              (retracted, review 0523)
  * v2 built an arc cover but INFLATED endpoints outward by 1e-20        (retracted, review 0608)
  * v3 (this file) uses rigorous INNER arcs.

Why inner.  A clash for every twist means the union of the violation sets
T_pq = { t : pair (p,q) closer than 2 } covers the twist circle.  Each T_pq is an open arc.  Arcs
A_pq SUBSET of T_pq that still cover give a correct proof.  Arcs A_pq SUPERSET of T_pq do not:
the cover could be produced entirely by the added material.  So the rounding must go INWARD.

Construction.  d^2(t) = A + B cos t + C sin t = A + R cos(t - psi), so
    T_pq = { t : cos(t - psi) < (4 - A)/R },
an open arc with centre psi and half-width h = arccos((4-A)/R).  With 60-digit mpf arithmetic
(per-operation error ~1e-59, ~20 operations, so < 1e-57 total) and a deliberate inner margin
MARGIN = 1e-30, the interval
    ( psi - h + MARGIN ,  psi + h - MARGIN )
lies strictly inside T_pq.  MARGIN is 27 orders above the arithmetic error and 27 orders below
any arc width, so it costs nothing and guarantees the direction.

A cover of [0, 2*pi/5] by these inner arcs is a cover by strict violations: for every relative
twist some pair is STRICTLY closer than 2.  The period 2*pi/5 is the icosahedral stabiliser of
the shared vertex axis.
"""
import math
import sys
from mpmath import mp, mpf, pi, atan2, sqrt, acos

mp.dps = 60
MARGIN = mpf('1e-30')
PERIOD = 2 * pi / 5


def build():
    two = mpf(2)
    s5 = sqrt(mpf(5))
    H = two / s5
    RHO = 2 * two / s5
    pts = [(mpf(0), mpf(0), two), (mpf(0), mpf(0), -two)]
    for k in range(5):
        a = 2 * pi * k / 5
        pts.append((RHO * mp.cos(a), RHO * mp.sin(a), H))
    for k in range(5):
        a = 2 * pi * k / 5 + pi / 5
        pts.append((RHO * mp.cos(a), RHO * mp.sin(a), -H))
    return [(z, y, -x) for (x, y, z) in pts]          # north pole onto +x


def eleven(rot, sign):
    keep = [q for q in rot if abs(q[0] - 2 * sign) > mpf('1e-40')]
    assert len(keep) == 11, len(keep)
    return keep


def inner_arcs(d=None, threshold=None, verbose=False):
    """inner safe arcs in [0, PERIOD]; d = centre separation (default 2), threshold = 2."""
    rot = build()
    A = eleven(rot, +1)
    Q = eleven(rot, -1)
    dd = mpf(2) if d is None else mpf(d)
    thr = mpf(2) if threshold is None else mpf(threshold)
    t2 = thr * thr
    w = (dd, mpf(0), mpf(0))
    out, kinds = [], {'whole': 0, 'empty': 0, 'arc': 0}
    for a in A:
        u = (w[0] - a[0], w[1] - a[1], w[2] - a[2])
        for q in Q:
            Aij = (u[0]**2 + u[1]**2 + u[2]**2) + (q[0]**2 + q[1]**2 + q[2]**2)
            B = 2 * (u[1] * q[1] + u[2] * q[2])
            C = 2 * (u[2] * q[1] - u[1] * q[2])
            R = sqrt(B * B + C * C)
            if Aij + R < t2:
                out.append((mpf(0), PERIOD)); kinds['whole'] += 1; continue
            if Aij - R > t2:
                kinds['empty'] += 1; continue
            psi = atan2(C, B)
            c = (t2 - Aij) / R
            c = max(min(c, mpf(1)), mpf(-1))
            h = acos(c)
            left = psi - h + MARGIN
            right = psi + h - MARGIN
            if right <= left:
                kinds['empty'] += 1; continue
            kinds['arc'] += 1
            k0 = int(math.floor(float(left) / float(PERIOD))) - 2
            for k in range(k0, k0 + 6):
                l2, h2 = left + k * PERIOD, right + k * PERIOD
                L = max(l2, mpf(0))
                Hh = min(h2, PERIOD)
                if Hh > L:
                    out.append((L, Hh))
    if verbose:
        print(f"  kinds: whole {kinds['whole']} empty {kinds['empty']} proper {kinds['arc']}")
    return out, kinds


def coverage(arcs):
    if not arcs:
        return False, [], [], mpf(0)
    arcs = sorted(arcs)
    merged = []
    for lo, hi in arcs:
        if merged and lo <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], hi)
        else:
            merged.append([lo, hi])
    gaps = [i for i in range(len(merged) - 1) if merged[i][1] < merged[i + 1][0]]
    starts = merged[0][0] <= 0
    ends = merged[-1][1] >= PERIOD
    total = sum(hi - lo for lo, hi in merged)
    return (starts and ends and not gaps), merged, gaps, total


def main():
    print("rigorous INNER arcs (margin 1e-30, arithmetic 60 digits)")
    arcs, kinds = inner_arcs(verbose=True)
    ok, merged, gaps, total = coverage(arcs)
    print(f"arcs placed: {len(arcs)}   merged: {len(merged)}   covered length "
          f"{float(total):.10f} of period {float(PERIOD):.10f}")
    print(f"starts at 0: {merged[0][0] <= 0}   reaches period end: {merged[-1][1] >= PERIOD}"
          f"   gaps: {len(gaps)}")
    for lo, hi in merged:
        print(f"   [{float(lo):+.10f}, {float(hi):+.10f}]")
    print()
    if ok:
        print("CERTIFIED with INNER arcs.  For EVERY relative twist some pair is strictly")
        print("closer than 2, so two adjacent dodecahedral centres are impossible.")
        print("Because the arcs used are subsets of the true violation sets, the cover is a")
        print("cover by strict violations and needs no outward rounding anywhere.")
    else:
        print("NOT CERTIFIED with inner arcs.")
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
