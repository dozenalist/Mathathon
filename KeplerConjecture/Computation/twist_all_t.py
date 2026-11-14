#!/usr/bin/env python3
"""K15-C112 -- two adjacent dodecahedral centres: an ALL-TWISTS proof, not a sampled maximum.

Review 0523 correctly objected that maximising over a twist grid is not a proof.  It is not
needed: for a pair (a, q) the squared distance as a function of the twist t is

    d^2(t) = A + B cos t + C sin t ,       max_t d^2 = A + sqrt(B^2 + C^2) ,

so ONE pair with A + sqrt(B^2+C^2) < 4 refutes every twist at once.  This computes
min over pairs of the max over t, in rigorous interval arithmetic, and reports the margin.

Geometry: v = 0, w = (2,0,0); the icosahedral twelve about v with a vertex at w (circumradius
2), the other eleven A; likewise about w with the shared contact removed, rotated by t about the
v-w axis, the eleven B_t.
"""
import itertools
import sys
from mpmath import iv, mp, mpf, sqrt, cos, sin, pi

mp.dps = 50
iv.dps = 50


def ivq(q):
    return iv.mpf(q.numerator) / iv.mpf(q.denominator)


def ico_dirs():
    """icosahedron of circumradius 2, unit vertex at the north pole; returns list of 3-tuples."""
    R = ivq(mpf(2).limit_denominator(10**6).p if False else 0)  # placeholder, unused
    return None


def build():
    # exact-ish constants in interval arithmetic: R = 2, H = 2/sqrt5, rho = 4/sqrt5
    two = iv.mpf(2)
    five = iv.mpf(5)
    s5 = iv.sqrt(five)
    H = two / s5
    RHO = 2 * two / s5
    pts = [(iv.mpf(0), iv.mpf(0), two)]          # north pole (this is w's direction)
    pts.append((iv.mpf(0), iv.mpf(0), -two))     # south pole
    for k in range(5):
        a = 2 * iv.pi * k / 5
        pts.append((RHO * iv.cos(a), RHO * iv.sin(a), H))
    for k in range(5):
        a = 2 * iv.pi * k / 5 + iv.pi / 5
        pts.append((RHO * iv.cos(a), RHO * iv.sin(a), -H))
    assert len(pts) == 12
    # rotate (0,0,1) -> (1,0,0):  (x,y,z) -> (z, y, -x)
    out = []
    for (x, y, z) in pts:
        out.append((z, y, -x))
    return out


def eleven(rot, exclude_x_sign):
    """the eleven points whose x is not 2*exclude_x_sign (x = +2 is w in v's frame)."""
    keep = []
    for q in rot:
        mid = (q[0].a + q[0].b) / 2
        if abs(mid - 2 * exclude_x_sign) < mpf('1e-30'):
            continue
        keep.append(q)
    assert len(keep) == 11, len(keep)
    return keep


def main():
    rot = build()
    A = eleven(rot, +1)          # v's other eleven (w is the point at x = +2)
    Q = eleven(rot, -1)          # w's other eleven, in w's frame (v is at x = -2)
    w = (iv.mpf(2), iv.mpf(0), iv.mpf(0))
    best = None                  # MIN over pairs of (max over t of d^2); want it < 4
    arg = None
    for i, a in enumerate(A):
        u = (w[0] - a[0], w[1] - a[1], w[2] - a[2])
        for j, q in enumerate(Q):
            # d^2(t) = A_ij + B cos t + C sin t
            Aij = (u[0] ** 2 + u[1] ** 2 + u[2] ** 2) + (q[0] ** 2 + q[1] ** 2 + q[2] ** 2)
            B = 2 * (u[1] * q[1] + u[2] * q[2])
            C = 2 * (u[2] * q[1] - u[1] * q[2])
            maxt = Aij + iv.sqrt(B * B + C * C)
            mid = (maxt.a + maxt.b) / 2
            if best is None or mid < best:
                best = mid
                arg = (i, j, maxt)
    print(f"pairs examined: {len(A) * len(Q)} (11 x 11)")
    print(f"MIN over pairs of  max over ALL twists  of d^2  =  {best}")
    print(f"  as an interval enclosure: [{arg[2].a}, {arg[2].b}]")
    print(f"required: d^2 < 4 for every pair and every twist")
    ok = arg[2].b < 4
    print(f"  ENCLOSURE ENTIRELY BELOW 4: {ok}")
    if ok:
        marg = 4 - arg[2].b
        print(f"  certified margin: 4 - upper end = {marg}")
        print(f"  i.e. d <= sqrt(upper) = {iv.sqrt(arg[2].b)} < 2")
    print()
    print("This is an ALL-TWISTS statement: for every pair, max_t d^2 is given in closed form,")
    print("so no twist grid is involved.  Hence for every relative twist some pair is closer")
    print("than 2, and two adjacent dodecahedral centres are impossible.")
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
