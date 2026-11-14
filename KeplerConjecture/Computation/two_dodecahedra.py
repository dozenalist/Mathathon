#!/usr/bin/env python3
"""K15-C108 step (4), verified by Main: two adjacent centres cannot both be dodecahedral.

Needed by Theorem D. E's K15-E075 states it; E's computation is numeric, so this is an
independent re-derivation at high precision plus an exact identification of the extremal
value.

Setup.  v = (0,0,0), w = (2,0,0).  For v's Voronoi cell to be the regular dodecahedron of
inradius 1 (Hales-McLaughlin's equality case) v must have twelve tangent neighbours in the
icosahedral arrangement, and one of them is w.  So the other ELEVEN are the antipode of w
plus the two pentagonal rings, i.e. the unit-circumradius-2 icosahedron with a vertex along
the v-w axis, minus that vertex.  Same for w, with an arbitrary relative twist t about the
axis.  Dodecahedral cells are impossible iff for EVERY twist some pair of the two eleven-sets
is closer than 2.
"""
import sys
from mpmath import mp, mpf, sqrt, cos, sin, pi, matrix

mp.dps = 40
R = mpf(2)
H = R / sqrt(mpf(5))          # ring height
RHO = 2 * R / sqrt(mpf(5))    # ring radius


def icosa_pole_axis():
    """icosahedron of circumradius 2 with a vertex at the north pole."""
    pts = [(mpf(0), mpf(0), R), (mpf(0), mpf(0), -R)]
    for k in range(5):
        a = 2 * pi * k / 5
        pts.append((RHO * cos(a), RHO * sin(a), H))
    for k in range(5):
        a = 2 * pi * k / 5 + pi / 5
        pts.append((RHO * cos(a), RHO * sin(a), -H))
    return pts


def rot_y_to_x(p):
    """rotate (0,0,1) -> (1,0,0):  (x,y,z) -> (z, y, -x)."""
    x, y, z = p
    return (z, y, -x)


def rot_x(p, t):
    x, y, z = p
    return (x, y * cos(t) - z * sin(t), y * sin(t) + z * cos(t))


def eleven(v_center, twist, partner_sign=-1):
    """the eleven neighbours of a dodecahedral centre other than its partner.

    The partner sits at q[0] = 2*partner_sign in the centre's own frame: for v (at the
    origin, partner w at +x) that is +2; for w (at +2, partner v at the origin) that is
    -2.  Getting this wrong is E's recorded bug -- it silently replaces the shared
    contact by the far pole and changes the answer."""
    out = []
    for p in icosa_pole_axis():
        q = rot_y_to_x(p)
        if abs(q[0] - 2 * partner_sign) < mpf('1e-30'):
            continue                            # that is the partner, exclude it
        q = rot_x(q, twist)
        out.append((v_center[0] + q[0], v_center[1] + q[1], v_center[2] + q[2]))
    assert len(out) == 11, len(out)
    return out


def min_cross(A, B):
    best = mpf('1e30')
    for a in A:
        for b in B:
            d = sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2)
            if d < best:
                best = d
    return best


def scan(n=1001):
    v = (mpf(0), mpf(0), mpf(0))
    w = (mpf(2), mpf(0), mpf(0))
    A = eleven(v, mpf(0), partner_sign=+1)   # v's partner w is at +2 in v's frame
    best = (mpf(-1), None)
    for i in range(n):
        t = 2 * pi * i / (5 * n)          # one fifth turn, the icosahedral period
        B = eleven(w, t, partner_sign=-1)
        d = min_cross(A, B)
        if d > best[0]:
            best = (d, t)
    return best


if __name__ == '__main__':
    # sanity: the twelve points really are an icosahedron of circumradius 2
    pts = icosa_pole_axis()
    for p in pts:
        assert abs(sqrt(sum(c * c for c in p)) - 2) < mpf('1e-35')
    dd = min(min_cross([pts[i]], [pts[j]]) for i in range(12) for j in range(i + 1, 12))
    print(f"icosahedron check: min pairwise distance = {mp.nstr(dd, 12)}  (edge 2*sqrt(2-2/sqrt5)"
          f" = {mp.nstr(2*sqrt(2 - 2/sqrt(5)), 12)})")

    coarse = scan(1001)
    fine = scan(20001)
    print(f"twist scan: coarse max-min = {mp.nstr(coarse[0], 12)} at t = {mp.nstr(coarse[1], 8)}")
    print(f"            fine   max-min = {mp.nstr(fine[0], 12)} at t = {mp.nstr(fine[1], 8)}")
    worst = max(coarse[0], fine[0])
    print()
    print(f"WORST CASE OVER ALL TWISTS: {mp.nstr(worst, 12)}")
    print(f"required separation:        2")
    print(f"VERDICT: {'two dodecahedral neighbours are IMPOSSIBLE' if worst < 2 else 'a twist is legal'}"
          f"  (shortfall {mp.nstr(2 - worst, 10)})")
    # is the worst case exactly at a 'half-way' twist? report the candidate values
    for name, t in (("0", mpf(0)), ("18 deg", pi / 10), ("36 deg", pi / 5), ("54 deg", 3 * pi / 10)):
        d = min_cross(eleven((mpf(0), mpf(0), mpf(0)), mpf(0)),
                      eleven((mpf(2), mpf(0), mpf(0)), t, partner_sign=-1))
        print(f"  t = {name:8s}: min cross distance = {mp.nstr(d, 12)}")
    print()
    print(f"E's K15-E075 quotes 1.056487696; Main gets {mp.nstr(worst, 12)}")
    sys.exit(0 if worst < 2 else 1)
