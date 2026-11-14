#!/usr/bin/env python3
"""A CERTIFIED two-dodecahedra threshold, by the corrected arc cover at general separation d.

`X-C051` computed the threshold d* = 3.4555003 by maximising the minimum distance over the twist —
a sampled statement.  This file makes it a cover: run the corrected arcs (constant including
2 u_x q_x, arc centred at psi+pi with half-width pi-acos c, inner shrink) with the partner centre
at d*u_0 instead of 2*u_0, and ask for which d the arcs still cover the twist circle.

A cover at d proves: for every twist some pair is STRICTLY closer than 2, hence no packing can
contain two dodecahedral cells at centre distance d.  The threshold is where the cover first fails.

Run: python3 certified_threshold.py      (exit 0 iff the certified threshold agrees with X-C051)
"""
import sys
from mpmath import mp, mpf, pi, atan2, sqrt, acos, floor, cos, sin

mp.dps = 60
EPS = mpf('1e-30')
PERIOD = 2*pi/5

def build():
    two = mpf(2); s5 = sqrt(mpf(5)); H = two/s5; RHO = 2*two/s5
    pts = [(mpf(0), mpf(0), two), (mpf(0), mpf(0), -two)]
    for k in range(5):
        a = 2*pi*k/5
        pts.append((RHO*cos(a), RHO*sin(a), H))
    for k in range(5):
        a = 2*pi*k/5 + pi/5
        pts.append((RHO*cos(a), RHO*sin(a), -H))
    return [(z, y, -x) for (x, y, z) in pts]

ROT = build()
A = [q for q in ROT if abs(q[0] - 2) > mpf('1e-30')]
Q = [q for q in ROT if abs(q[0] + 2) > mpf('1e-30')]

def covers(d):
    """Do the corrected clash arcs cover [0, PERIOD] at partner separation d?"""
    w = (d, mpf(0), mpf(0))
    raw = []
    for a in A:
        u = (w[0]-a[0], w[1]-a[1], w[2]-a[2])
        for q in Q:
            Aij = u[0]**2+u[1]**2+u[2]**2 + q[0]**2+q[1]**2+q[2]**2 + 2*u[0]*q[0]
            B = 2*(u[1]*q[1]+u[2]*q[2]); C = 2*(u[2]*q[1]-u[1]*q[2])
            R = sqrt(B*B+C*C)
            if R == 0:
                if Aij < 4: raw.append((mpf(0), PERIOD))
                continue
            if Aij + R < 4: raw.append((mpf(0), PERIOD)); continue
            if Aij - R > 4: continue
            c = max(min((4-Aij)/R, mpf(1)), mpf(-1))
            centre = atan2(C, B) + pi
            half = pi - acos(c) - EPS
            if half <= 0: continue
            lo, hi = centre-half, centre+half
            k0 = int(floor(lo/PERIOD)) - 2
            for k in range(k0, k0+6):
                L = max(lo+k*PERIOD, mpf(0)); Hh = min(hi+k*PERIOD, PERIOD)
                if Hh > L: raw.append((L, Hh))
    m = []
    for lo, hi in sorted(raw):
        if m and lo <= m[-1][1]: m[-1][1] = max(m[-1][1], hi)
        else: m.append([lo, hi])
    return (m and m[0][0] <= 0 and m[-1][1] >= PERIOD and not [i for i in range(len(m)-1) if m[i][1] < m[i+1][0]]), len(m)

if __name__ == '__main__':
    print("  d        cover?   merged intervals")
    for d in (2.0, 2.5, 3.0, 3.3, 3.4, 3.45, 3.455, 3.456, 3.46, 3.5):
        ok, n = covers(mpf(str(d)))
        print("  %.3f    %-7s  %d" % (d, "yes" if ok else "NO", n))
    # bisect the threshold
    lo, hi = mpf('2'), mpf('4')
    for _ in range(40):
        mid = (lo+hi)/2
        if covers(mid)[0]: lo = mid
        else: hi = mid
    print("\n  certified threshold (cover holds below, fails above): d in [%.9f, %.9f]" % (float(lo), float(hi)))
    print("  X-C051's sampled threshold:                            3.455500344")
    ok = abs(float(lo) - 3.455500344) < 1e-4
    print("\nRESULT:", "the certified threshold agrees with X-C051" if ok else "DISAGREEMENT")
    sys.exit(0 if ok else 1)
