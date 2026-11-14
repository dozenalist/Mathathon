"""Exact arithmetic in Q(sqrt 3), and exact planar geometry for lattice Voronoi tilings.

A Q3 number is a pair (a, b) of Fractions meaning a + b*sqrt(3).  All coordinates of every
object used by cellbar.py lie in Q(sqrt 3)^2, so every comparison below is exact.
"""
from fractions import Fraction as F


class Q3:
    __slots__ = ("a", "b")

    def __init__(self, a, b=0):
        self.a = F(a)
        self.b = F(b)

    # --- ring operations -------------------------------------------------
    def __add__(self, o):
        o = q3(o)
        return Q3(self.a + o.a, self.b + o.b)

    __radd__ = __add__

    def __neg__(self):
        return Q3(-self.a, -self.b)

    def __sub__(self, o):
        o = q3(o)
        return Q3(self.a - o.a, self.b - o.b)

    def __rsub__(self, o):
        return q3(o) - self

    def __mul__(self, o):
        o = q3(o)
        return Q3(self.a * o.a + 3 * self.b * o.b, self.a * o.b + self.b * o.a)

    __rmul__ = __mul__

    def inv(self):
        d = self.a * self.a - 3 * self.b * self.b          # norm, rational, nonzero iff self != 0
        assert d != 0
        return Q3(self.a / d, -self.b / d)

    def __truediv__(self, o):
        return self * q3(o).inv()

    # --- order ------------------------------------------------------------
    def sign(self):
        """Return -1, 0, +1 for the sign of a + b*sqrt3.  Exact."""
        a, b = self.a, self.b
        if a == 0 and b == 0:
            return 0
        if a >= 0 and b >= 0:
            return 1
        if a <= 0 and b <= 0:
            return -1
        # opposite signs: compare a^2 with 3 b^2
        lhs, rhs = a * a, 3 * b * b
        if lhs == rhs:
            return 0
        if a > 0:                    # b < 0 : sign(a - |b|sqrt3)
            return 1 if lhs > rhs else -1
        # a < 0 < b : sign(b sqrt3 - |a|)
        return 1 if rhs > lhs else -1

    def __lt__(self, o):
        return (self - q3(o)).sign() < 0

    def __le__(self, o):
        return (self - q3(o)).sign() <= 0

    def __gt__(self, o):
        return (self - q3(o)).sign() > 0

    def __ge__(self, o):
        return (self - q3(o)).sign() >= 0

    def __eq__(self, o):
        o = q3(o)
        return self.a == o.a and self.b == o.b

    def __hash__(self):
        return hash((self.a, self.b))

    def __repr__(self):
        if self.b == 0:
            return f"{self.a}"
        return f"({self.a}+{self.b}r3)"

    def float(self):
        return float(self.a) + float(self.b) * 3 ** 0.5


def q3(x):
    if isinstance(x, Q3):
        return x
    if isinstance(x, tuple):
        return Q3(*x)
    return Q3(x, 0)


SQ3 = Q3(0, 1)          # sqrt 3
ZERO, ONE, HALF = Q3(0), Q3(1), Q3(F(1, 2))


class Pt:
    __slots__ = ("x", "y")

    def __init__(self, x, y):
        self.x, self.y = q3(x), q3(y)

    def __add__(self, o):
        return Pt(self.x + o.x, self.y + o.y)

    def __sub__(self, o):
        return Pt(self.x - o.x, self.y - o.y)

    def __mul__(self, s):
        s = q3(s)
        return Pt(self.x * s, self.y * s)

    __rmul__ = __mul__

    def __eq__(self, o):
        return self.x == o.x and self.y == o.y

    def __hash__(self):
        return hash((self.x, self.y))

    def dot(self, o):
        return self.x * o.x + self.y * o.y

    def norm2(self):
        return self.dot(self)

    def __repr__(self):
        return f"({self.x},{self.y})"

    def float(self):
        return (self.x.float(), self.y.float())


def seg_dist2(p, a, b):
    """Exact squared distance from point p to closed segment ab, in Q(sqrt3)."""
    ab = b - a
    ap = p - a
    den = ab.norm2()
    if den == ZERO:
        return ap.norm2()
    t = ap.dot(ab) / den               # rational-in-Q3 parameter
    if t < ZERO:
        return ap.norm2()
    if t > ONE:
        return (p - b).norm2()
    # |ap - t ab|^2
    d = ap - ab * t
    return d.norm2()


def hexagon(r):
    """Regular hexagon with circumradius r, one vertex on the +x axis (flat top/bottom edges)."""
    r = q3(r)
    c = [(ONE, ZERO), (HALF, SQ3 * Q3(F(1, 2))), (-HALF, SQ3 * Q3(F(1, 2))),
         (-ONE, ZERO), (-HALF, -SQ3 * Q3(F(1, 2))), (HALF, -SQ3 * Q3(F(1, 2)))]
    return [Pt(r * u, r * v) for (u, v) in c]


def poly_dist2(p, poly):
    """Exact squared distance from p to a convex polygon given as a counterclockwise vertex list.
    Interior points (including the boundary) give 0; exterior points give the minimum over the
    edges of the point-to-segment distance."""
    n = len(poly)
    inside = True
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        e = b - a
        d = p - a
        cr = e.x * d.y - e.y * d.x          # cross product, in Q(sqrt3)
        if cr < ZERO:
            inside = False
            break
    if inside:
        return ZERO
    m = None
    for i in range(n):
        d = seg_dist2(p, poly[i], poly[(i + 1) % n])
        if m is None or d < m:
            m = d
    return m


def lattice_pt(i, j, r):
    """The lattice point L*(i + j*omega), omega = e^(2 pi i/3), L = sqrt(3) r.

    Real coordinates: x = sqrt3 r (i - j/2) = r(sqrt3 i - sqrt3 j/2),  y = 3 r j / 2."""
    r = q3(r)
    x = SQ3 * r * (Q3(i) - Q3(F(1, 2)) * Q3(j))
    y = r * Q3(F(3, 2)) * Q3(j)
    return Pt(x, y)
