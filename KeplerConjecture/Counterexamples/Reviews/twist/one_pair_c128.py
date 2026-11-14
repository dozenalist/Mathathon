#!/usr/bin/env python3
"""K15-C128 checked independently: ONE pair of contacts settles the two-dodecahedra step.

The physical twist space is R/(2*pi/5) -- circumference 72 degrees -- because a 72 degree rotation
about the vertex axis maps the icosahedron to itself.  For the pair with A = 6.444582472 and R = 6.4
the violation set is the complement of an arc of half-width h = arccos((4-A)/R) = 112.4555152 deg,
so it has length 2*pi - 2h = 135.0889696 deg > 72 deg and therefore meets EVERY coset of 72 deg:
for every physical twist some representative puts this pair closer than 2.

Checked directly: max over tau in [0,72) of min over k in {0..4} of d^2(tau + 72k) = 1.266873708 < 4.

Exit 0 iff |T| > 72 deg and that maximum is below 4 and matches C128's 1.266873708.
"""
import importlib.util
import sys
from mpmath import mp, mpf, acos, atan2, cos, sin, pi, sqrt

mp.dps = 40
PER = 2 * pi / 5


def load_cover():
    spec = importlib.util.spec_from_file_location("tc", "twist_cover_a34a3ff1.py")
    tc = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tc)
    return tc


def main():
    tc = load_cover()
    rot = tc.build()
    A11, Q = tc.eleven(rot, +1), tc.eleven(rot, -1)
    w = (mpf(2), mpf(0), mpf(0))
    found = None
    for i, a in enumerate(A11):
        u = (w[0] - a[0], w[1] - a[1], w[2] - a[2])
        for j, q in enumerate(Q):
            A = u[0]**2 + u[1]**2 + u[2]**2 + q[0]**2 + q[1]**2 + q[2]**2 + 2 * u[0] * q[0]
            B = 2 * (u[1] * q[1] + u[2] * q[2])
            C = 2 * (u[2] * q[1] - u[1] * q[2])
            R = sqrt(B * B + C * C)
            if abs(A - mpf('6.444582472')) < 1e-8 and abs(R - mpf('6.4')) < 1e-9:
                found = (i, j, A, R, B, C)
    if found is None:
        print("pair not found")
        return 1
    i, j, A, R, B, C = found
    c = (4 - A) / R
    h = acos(c)
    T = 2 * pi - 2 * h
    print(f"pair A[{i}], Q[{j}]  (C128 writes A[1], Q[8]; the ordering differs, the invariants do not)")
    print(f"  A = {float(A):.9f}   R = {float(R):.9f} = 32/5")
    print(f"  c = (4-A)/R = {float(c):.12f}   -(3-sqrt5)/2 = {float(-(3 - sqrt(5)) / 2):.12f}")
    print(f"  h = {float(h * 180 / pi):.7f} deg    |T| = 2pi-2h = {float(T * 180 / pi):.7f} deg    "
          f"period 72 deg -> |T| > 72: {T * 180 / pi > 72}")
    psi = atan2(C, B)
    N = 4000
    best, arg = -1e9, None
    for k in range(N):
        tau = PER * k / N
        d = min(A + B * cos(tau + m * PER - psi) + C * sin(tau + m * PER - psi) for m in range(5))
        if d > best:
            best, arg = d, float(tau * 180 / pi)
    print(f"  max over tau of min over k d^2(tau + 72k) = {float(best):.9f} at tau = {arg:.3f} deg")
    ok = (T * 180 / pi > 72) and best < 4 and abs(best - mpf('1.266873708')) < 1e-6
    print(f"\n  C128's number reproduced: {abs(best - mpf('1.266873708')) < 1e-6};  < 4: {best < 4}")
    print("  => one pair is closer than 2 at some representative of EVERY physical twist")
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
