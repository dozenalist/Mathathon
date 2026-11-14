#!/usr/bin/env python3
"""d7, part 3b: exact data for the two-circle cover of the spindle, cleaned up.

Result: the four points p1, p3, p5, p6 are concyclic; so the 7-vertex
4-chromatic spindle is covered by TWO circles (r = 0.5378..., r = 0.7301...),
while ONE circle of any radius has chord graph of chromatic number <= 3.
"""
import sympy as sp

s3, s11 = sp.sqrt(3), sp.sqrt(11)
I = sp.I
A = (s3 + I) / 2
B = (s3 - I) / 2
T = s3
U = (5 + I * s11) / 6
P = [sp.Integer(0), A, B, T, U * A, U * B, U * T]
xy = []
for p in P:
    z = sp.expand(sp.simplify(p))
    xy.append((sp.radsimp(sp.simplify(sp.re(z))), sp.radsimp(sp.simplify(sp.im(z)))))


def det4(idxs):
    rows = []
    for i in idxs:
        x, y = xy[i]
        rows.append([x, y, x ** 2 + y ** 2, sp.Integer(1)])
    return sp.simplify(sp.expand(sp.Matrix(rows).det()))


def circle_of3(i, j, k):
    (x1, y1), (x2, y2), (x3, y3) = xy[i], xy[j], xy[k]
    d = sp.simplify(2 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)))
    ux = sp.radsimp(sp.simplify(((x1 ** 2 + y1 ** 2) * (y2 - y3) + (x2 ** 2 + y2 ** 2) * (y3 - y1) +
                                 (x3 ** 2 + y3 ** 2) * (y1 - y2)) / d))
    uy = sp.radsimp(sp.simplify(((x1 ** 2 + y1 ** 2) * (x3 - x2) + (x2 ** 2 + y2 ** 2) * (x1 - x3) +
                                 (x3 ** 2 + y3 ** 2) * (x2 - x1)) / d))
    r2 = sp.radsimp(sp.simplify((x1 - ux) ** 2 + (y1 - uy) ** 2))
    return ux, uy, r2


print("=" * 78)
print("Concyclicity (exact 4x4 determinant, entries in Q(sqrt3, sqrt11))")
print("=" * 78)
for quad in [(0, 1, 2, 3), (1, 3, 5, 6), (1, 2, 4, 5), (2, 3, 4, 6), (0, 1, 3, 6)]:
    print(f"  det{p} = {sp.simplify(det4(quad))}".replace("p", str(quad)))

print()
print("=" * 78)
print("The two circles")
print("=" * 78)
for name, tri in (("C1 (through p1,p3,p5,p6)", (1, 3, 5, 6)), ("C2 (through p0,p2,p4)", (0, 2, 4))):
    ux, uy, r2 = circle_of3(*tri[:3])
    r = sp.sqrt(r2)
    oncircle = [i for i in range(7)
                if sp.simplify(sp.expand((xy[i][0] - ux) ** 2 + (xy[i][1] - uy) ** 2 - r2)) == 0]
    print(f"{name}")
    print(f"   centre = ({sp.sstr(ux)}, {sp.sstr(uy)})")
    print(f"   r^2 = {sp.sstr(r2)}  = {float(r2.evalf()):.9f}   r = {float(r.evalf()):.9f}")
    print(f"   points exactly on it: {oncircle}")
    print(f"   r < 3/4? {bool(sp.simplify(r2 - sp.Rational(9,16)) < 0)}")
print()
print("Cover: C1 holds p1,p3,p5,p6 and C2 holds p0,p2,p4, i.e. all seven vertices, on two")
print("circles of radius < 3/4.  One circle of ANY radius has chord graph of chromatic")
print("number at most 3 (Theorem A), so two circles are necessary and sufficient here.")
