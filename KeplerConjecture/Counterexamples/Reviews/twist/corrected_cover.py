#!/usr/bin/env python3
"""A corrected all-twists cover for the two-dodecahedra theorem (repairs C112's certificate).

Main's twist_cover.py (blob 469fc9f1, main 8dc264e) has two independent defects:
  (D1) the constant term of  d^2(t) = A + B cos t + C sin t  omits 2*u_x*q_x;
  (D2) the clash set {t : cos(t-psi) < c} is centred at psi+pi with half-width pi-acos(c),
       while the code uses [psi-acos(c), psi+acos(c)] -- the FAR set, i.e. the complement.

This script rebuilds the cover with both fixed and reports the actual coverage margin.
Geometry: v at 0 with its twelve contacts at 2*u_i (unit icosahedral directions); w at (2,0,0);
w's twelve contacts at w + R_t q_j in w's frame.  Dropping the shared contact from each side leaves
11 x 11 = 121 pairs.  For a pair, with u = w - a,

    d^2(t) = |u|^2 + |q|^2 + 2 u_x q_x + 2(u_y q_y + u_z q_z) cos t + 2(u_z q_y - u_y q_z) sin t.

The twist lives on a circle of period 72 degrees (the icosahedral stabiliser of the shared axis).
Any packing containing two regular dodecahedral cells of inradius 1 contains such a configuration,
so a cover certifies that two such cells cannot coexist at centre distance exactly 2.

Run: python3 corrected_cover.py     (exit 0 iff the corrected arcs cover the circle)
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

def eleven(rot, sign):
    keep = [q for q in rot if abs(q[0] - 2*sign) > mpf('1e-30')]
    assert len(keep) == 11
    return keep

def arcs():
    rot = build(); A = eleven(rot, +1); Q = eleven(rot, -1)
    w = (mpf(2), mpf(0), mpf(0))
    out = []
    for a in A:
        u = (w[0]-a[0], w[1]-a[1], w[2]-a[2])
        for q in Q:
            Aij = u[0]**2 + u[1]**2 + u[2]**2 + q[0]**2 + q[1]**2 + q[2]**2 + 2*u[0]*q[0]
            B = 2*(u[1]*q[1] + u[2]*q[2])
            C = 2*(u[2]*q[1] - u[1]*q[2])
            R = sqrt(B*B + C*C)
            if R == 0:
                if Aij < 4: out.append((mpf(0), PERIOD))
                continue
            if Aij + R < 4:                    # closer than 2 for EVERY twist
                out.append((mpf(0), PERIOD)); continue
            if Aij - R > 4:                    # never closer than 2
                continue
            c = (4 - Aij)/R
            c = max(min(c, mpf(1)), mpf(-1))
            psi = atan2(C, B)
            centre = psi + pi                    # <-- corrected centre
            half = pi - acos(c)                  # <-- corrected half-width
            lo, hi = centre - half, centre + half
            k0 = int(floor(lo/PERIOD)) - 2
            for k in range(k0, k0 + 6):
                L = max(lo + k*PERIOD, mpf(0)); Hh = min(hi + k*PERIOD, PERIOD)
                if Hh > L: out.append((L - EPS, Hh + EPS))
    return out

def merge(iv):
    iv = sorted(iv); out = []
    for lo, hi in iv:
        if out and lo <= out[-1][1]: out[-1][1] = max(out[-1][1], hi)
        else: out.append([lo, hi])
    return out

if __name__ == '__main__':
    raw = arcs(); m = merge(raw)
    print("arcs: %d raw of 121 pairs, %d after merging, period %.6f deg" % (len(raw), len(m), float(mp.degrees(PERIOD))))
    for lo, hi in m:
        print("   [%+10.6f, %+10.6f] deg   width %8.4f" % (float(mp.degrees(lo)), float(mp.degrees(hi)), float(mp.degrees(hi-lo))))
    starts = m[0][0] <= 0; ends = m[-1][1] >= PERIOD
    gaps = [i for i in range(len(m)-1) if m[i][1] < m[i+1][0]]
    print("\nstarts at 0: %s ; reaches period end: %s ; gaps: %d" % (starts, ends, len(gaps)))
    print("coverage: %.6f of %.6f deg" % (float(mp.degrees(sum(hi-lo for lo,hi in m))), float(mp.degrees(PERIOD))))
    ok = starts and ends and not gaps
    print("\nRESULT:", "the CORRECTED arcs cover every twist" if ok else "cover FAILS with the corrected arcs")
    sys.exit(0 if ok else 1)
