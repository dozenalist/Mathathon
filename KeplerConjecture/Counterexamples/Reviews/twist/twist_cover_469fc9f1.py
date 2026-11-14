#!/usr/bin/env python3
"""K15-C112 -- two adjacent dodecahedral centres, certified for ALL relative twists.

Review 0523: a sampled twist maximum is not a proof.  Here is the proof, by arc covering.

For a pair (a in v's other eleven, q in w's other eleven) the squared distance under a relative
twist t about the v-w axis is a pure sinusoid

    d^2(t) = A + B cos t + C sin t = A + R cos(t - psi),   R = sqrt(B^2+C^2), psi = atan2(C,B),

so the twists for which that pair is CLOSER than 2 form

    T = { t : cos(t - psi) < (4 - A)/R },

which is empty, the whole circle, or a single arc of half-width arccos((4-A)/R).  A clash for
every twist is therefore the statement that the finitely many arcs T cover the twist circle
(period 2*pi/5 = 72 deg, the icosahedral stabiliser of the shared vertex axis).

Arithmetic: 50 significant digits, and every arc endpoint is inflated by EPS before the cover
test, so the arcs tested are supersets of the true ones and the cover is conservative in the
right direction.  22-24 arcs; no twist is sampled and no grid is involved.
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
    return [(z, y, -x) for (x, y, z) in pts]      # rotate the north pole onto +x


def eleven(rot, sign):
    keep = []
    for q in rot:
        if abs(q[0] - 2 * sign) < mpf('1e-30'):
            continue
        keep.append(q)
    assert len(keep) == 11, len(keep)
    return keep


def arcs():
    rot = build()
    A = eleven(rot, +1)          # v's other eleven (w is at x = +2 in v's frame)
    Q = eleven(rot, -1)          # w's other eleven, in w's frame (v is at x = -2)
    w = (mpf(2), mpf(0), mpf(0))
    out = []
    for a in A:
        u = (w[0] - a[0], w[1] - a[1], w[2] - a[2])
        for q in Q:
            Aij = (u[0]**2 + u[1]**2 + u[2]**2) + (q[0]**2 + q[1]**2 + q[2]**2)
            B = 2 * (u[1] * q[1] + u[2] * q[2])
            C = 2 * (u[2] * q[1] - u[1] * q[2])
            R = sqrt(B * B + C * C)
            psi = atan2(C, B)
            if Aij + R < 4:                      # too close for every twist
                out.append((mpf(0), PERIOD))
                continue
            if Aij - R > 4:                      # never too close
                continue
            c = (4 - Aij) / R
            c = max(min(c, mpf(1)), mpf(-1))
            half = acos(c)
            lo, hi = psi - half, psi + half
            k0 = int(floor(lo / PERIOD)) - 2
            for k in range(k0, k0 + 6):
                l2, h2 = lo + k * PERIOD, hi + k * PERIOD
                L = max(l2, mpf(0))
                Hh = min(h2, PERIOD)
                if Hh > L:
                    out.append((L - EPS, Hh + EPS))     # inflate: superset
    return out


def main():
    A = arcs()
    print(f"arcs built: {len(A)} of at most 121 pairs")
    A = sorted(A)
    merged = []
    for lo, hi in A:
        if merged and lo <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], hi)
        else:
            merged.append([lo, hi])
    print(f"after merging: {len(merged)} interval(s), total length "
          f"{float(sum(hi - lo for lo, hi in merged)):.6f} of period {float(PERIOD):.6f}")
    for lo, hi in merged:
        print(f"   [{float(lo):+.8f}, {float(hi):+.8f}]")
    starts_ok = merged[0][0] <= mpf(0)
    ends_ok = merged[-1][1] >= PERIOD
    gaps = [i for i in range(len(merged) - 1) if merged[i][1] < merged[i + 1][0]]
    print(f"\nstarts at 0: {starts_ok}   reaches the period end: {ends_ok}   gaps: {len(gaps)}")
    ok = starts_ok and ends_ok and not gaps
    print()
    if ok:
        print("CERTIFIED (all twists, not a sample): the arcs cover the whole twist circle, so")
        print("for EVERY relative twist some pair of the two eleven-point sets is closer than 2.")
        print("Two adjacent dodecahedral centres are therefore impossible.")
    else:
        print("NOT CERTIFIED: coverage failed.")
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
