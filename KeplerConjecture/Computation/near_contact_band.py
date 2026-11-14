#!/usr/bin/env python3
"""K15-C116 -- how wide is the near-contact band in which two dodecahedral cells stay impossible?

C114 claims the two-dodecahedra clash persists for centres at distance d > 2, which is what lets
Theorem D and the bridge be widened from exact contacts to pairs at distance <= 2+eps.  This
check makes the claim quantitative: it runs the arc cover of twist_cover.py for a range of d and
reports the largest d for which the cover still holds, i.e. the largest separation at which two
dodecahedral cells are still impossible.

Same machinery as twist_cover.py: the "closer than 2" set of each pair is a single arc in the
twist, the arcs are inflated by EPS, and a cover of [0, 2pi/5] with no gap is the certificate.
"""
import sys
from mpmath import mp, mpf, pi, atan2, sqrt, floor, acos

mp.dps = 50
EPS = mpf('1e-20')
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
    return [(z, y, -x) for (x, y, z) in pts]


def eleven(rot, sign):
    return [q for q in rot if abs(q[0] - 2 * sign) > mpf('1e-30')]


def covers(d, thr):
    """does the union of 'too close' arcs cover the twist circle, for centres d apart?"""
    rot = build()
    A = eleven(rot, +1)
    Q = eleven(rot, -1)
    w = (mpf(d), mpf(0), mpf(0))
    t2 = thr * thr
    out = []
    for a in A:
        u = (w[0] - a[0], w[1] - a[1], w[2] - a[2])
        for q in Q:
            Aij = (u[0]**2 + u[1]**2 + u[2]**2) + (q[0]**2 + q[1]**2 + q[2]**2)
            B = 2 * (u[1] * q[1] + u[2] * q[2])
            C = 2 * (u[2] * q[1] - u[1] * q[2])
            R = sqrt(B * B + C * C)
            psi = atan2(C, B)
            if Aij + R < t2:
                return True, 1.0
            if Aij - R > t2:
                continue
            c = (t2 - Aij) / R
            c = max(min(c, mpf(1)), mpf(-1))
            half = acos(c)
            lo, hi = psi - half, psi + half
            k0 = int(floor(lo / PERIOD)) - 2
            for k in range(k0, k0 + 6):
                l2, h2 = lo + k * PERIOD, hi + k * PERIOD
                L, Hh = max(l2, mpf(0)), min(h2, PERIOD)
                if Hh > L:
                    out.append((L - EPS, Hh + EPS))
    out.sort()
    merged = []
    for lo, hi in out:
        if merged and lo <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], hi)
        else:
            merged.append([lo, hi])
    cov = 0
    if merged and merged[0][0] <= mpf(0) and merged[-1][1] >= PERIOD:
        cov = sum(hi - lo for lo, hi in merged) / PERIOD
        gaps = sum(1 for i in range(len(merged) - 1) if merged[i][1] < merged[i + 1][0])
        return gaps == 0, float(cov)
    return False, float(cov)


def main():
    print("two dodecahedral cells with centres d apart: is the clash still unavoidable?")
    print(f"{'d':>8} {'cover?':>8} {'coverage':>10}")
    last_ok = None
    for d in ('2.00', '2.02', '2.05', '2.10', '2.20', '2.40', '2.60', '2.80', '3.00'):
        ok, cov = covers(mpf(d), mpf(2))
        print(f"{d:>8} {str(ok):>8} {cov:>10.4f}")
        if ok:
            last_ok = d
    print()
    print(f"largest tested d with a certified cover: {last_ok}")
    print("So two dodecahedral cells are impossible at least out to that separation; beyond it")
    print("this test says nothing.  This is what quantifies C114's near-contact widening:")
    print("the band is at least as wide as the largest certified d minus 2.")
    return 0


if __name__ == '__main__':
    sys.exit(main())
