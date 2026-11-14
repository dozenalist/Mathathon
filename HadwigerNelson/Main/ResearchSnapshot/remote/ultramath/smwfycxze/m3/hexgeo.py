"""Exact Q(sqrt3) geometry of the hexagonal seven-colouring c_0.

Data (paper / m3, sprint B):
  w = e^{2 pi i/3}, r = 2/5, d = sqrt3 r = 2 sqrt3/5, Lambda = d (Z + Z w)
  Voronoi cell of d(m+nw) is a regular hexagon of circumradius r, inradius sqrt3/5
  colour of the cell of d(m+nw) is (m + 2n) mod 7.
An element of Q(sqrt3) is a pair (a,b) of Fractions meaning a + b*sqrt(3).
"""

from fractions import Fraction as F


class Q3:
    """a + b sqrt(3), a,b Fractions. Exact."""
    __slots__ = ('a', 'b')

    def __init__(self, a, b=0):
        self.a = F(a)
        self.b = F(b)

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

    def __truediv__(self, o):
        o = q3(o)
        n = o.a * o.a - 3 * o.b * o.b
        if n == 0:
            raise ZeroDivisionError
        return Q3((self.a * o.a - 3 * self.b * o.b) / n,
                  (self.b * o.a - self.a * o.b) / n)

    def __eq__(self, o):
        o = q3(o)
        return self.a == o.a and self.b == o.b

    def __hash__(self):
        return hash((self.a, self.b))

    def __lt__(self, o):
        return sign_q3(self - q3(o)) < 0

    def __le__(self, o):
        return sign_q3(self - q3(o)) <= 0

    def __gt__(self, o):
        return sign_q3(self - q3(o)) > 0

    def __ge__(self, o):
        return sign_q3(self - q3(o)) >= 0

    def __float__(self):
        return float(self.a) + float(self.b) * math.sqrt(3.0)

    def __pow__(self, n):
        if not isinstance(n, int) or n < 0:
            raise TypeError
        r = Q3(1)
        for _ in range(n):
            r = r * self
        return r

    def __abs__(self):
        return self if sign_q3(self) >= 0 else -self

    def __repr__(self):
        if self.b == 0:
            return str(self.a)
        return f"({self.a}+{self.b}s)"


def q3(x):
    if isinstance(x, Q3):
        return x
    return Q3(F(x), F(0))


def sign_q3(x):
    """Exact sign of a + b sqrt3 (a,b rational)."""
    a, b = x.a, x.b
    if b == 0:
        return (a > 0) - (a < 0)
    if a == 0:
        return (b > 0) - (b < 0)
    if a > 0 and b > 0:
        return 1
    if a < 0 and b < 0:
        return -1
    d = a * a - 3 * b * b          # sign(a + b s) = sign(a) if a^2 > 3b^2 else sign(-...)
    if a > 0:                       # b < 0
        return (d > 0) - (d < 0)
    return (d < 0) - (d > 0)        # a < 0, b > 0


S3 = Q3(0, 1)

# Voronoi hexagon of the origin: circumradius 2/5, inradius sqrt3/5, vertices at 30+60k deg
HEX = [(F(1, 5), Q3(0, F(1, 5))),
       (F(0), Q3(F(2, 5), 0)),
       (-F(1, 5), Q3(0, F(1, 5))),
       (-F(1, 5), Q3(0, -F(1, 5))),
       (F(0), Q3(-F(2, 5), 0)),
       (F(1, 5), Q3(0, -F(1, 5)))]
# coordinates are pairs (x, y) with x in Q and y in Q(sqrt3)


def centre(m, n):
    """centre d(m + n w) = ( sqrt3(2m-n)/5 , 3n/5 ), as a pair (x, y) in Q x Q(sqrt3)."""
    x = Q3(0, F(2, 5)) * (Q3(m) - Q3(n) * Q3(F(1, 2)))
    y = Q3(F(3, 5) * n)
    return (x, y)


def colour(m, n):
    return (m + 2 * n) % 7


def sqdist(p, q):
    dx = p[0] - q[0]
    dy = p[1] - q[1]
    return dx * dx + dy * dy


def dot(v, w):
    return v[0] * w[0] + v[1] * w[1]


def _sub(p, q):
    return (p[0] - q[0], p[1] - q[1])


def seg_sqdist(p, a, b):
    """exact squared distance from point p to the segment ab."""
    ab = _sub(b, a)
    ap = _sub(p, a)
    denom = dot(ab, ab)
    t = dot(ap, ab) / denom
    if t <= Q3(0):
        return sqdist(p, a)
    if t >= Q3(1):
        return sqdist(p, b)
    proj = (a[0] + t * ab[0], a[1] + t * ab[1])
    return sqdist(p, proj)


def verts(m, n):
    c = centre(m, n)
    return [(c[0] + vx, c[1] + vy) for (vx, vy) in HEX]


def point_hex_sqdist(p, m, n):
    """exact squared distance from p to the closed hexagon of centre d(m+nw)."""
    vs = verts(m, n)
    inside = True
    for i in range(6):
        a, b = vs[i], vs[(i + 1) % 6]
        e = _sub(b, a)
        cross = e[0] * (p[1] - a[1]) - e[1] * (p[0] - a[0])
        if sign_q3(cross) < 0:
            inside = False
            break
    if inside:
        return Q3(0)
    return min(seg_sqdist(p, vs[i], vs[(i + 1) % 6]) for i in range(6))


def point_hex_sqfar(p, m, n):
    """exact squared distance from p to the farthest point of that hexagon (a vertex)."""
    return max(sqdist(p, v) for v in verts(m, n))


def which_hex(p):
    """the lattice point whose Voronoi cell contains p (exact, by min distance)."""
    best = None
    for m in range(-4, 5):
        for n in range(-4, 5):
            d2 = point_hex_sqdist(p, m, n)
            if best is None or d2 < best[0]:
                best = (d2, m, n)
    return best


def c0(p):
    """colour of the cell containing p."""
    d2, m, n = which_hex(p)
    assert d2 == Q3(0), (p, d2)
    return colour(m, n)


# ---------------------------------------------------------------- point location
import math


def _num(x):
    return float(x.a) + float(x.b) * math.sqrt(3.0)


def point_in_hex(p, m, n):
    """exact containment in the closed hexagon (Euclidean coords, p=(x,y) in Q(sqrt3)^2)."""
    vs = verts(m, n)
    for i in range(6):
        a, b = vs[i], vs[(i + 1) % 6]
        e = _sub(b, a)
        cross = e[0] * (p[1] - a[1]) - e[1] * (p[0] - a[0])
        if sign_q3(cross) < 0:
            return False
    return True


def nearest_lattice(p):
    """exact: (m,n) whose Voronoi cell contains p (p not on a cell boundary)."""
    px, py = _num(p[0]), _num(p[1])
    n0 = 5.0 * py / 3.0
    m0 = (5.0 * px / math.sqrt(3.0) + n0) / 2.0
    best = None
    for m in range(int(math.floor(m0)) - 1, int(math.floor(m0)) + 3):
        for n in range(int(math.floor(n0)) - 1, int(math.floor(n0)) + 3):
            d2 = point_hex_sqdist(p, m, n)
            if best is None or d2 < best[0]:
                best = (d2, m, n)
    if best[0] != Q3(0):
        raise ValueError(("point location failed", p, best))
    return (best[1], best[2])


def seg_seg_sqdist(a, b, c, d):
    """exact squared distance between two closed segments (in Q(sqrt3)^2)."""
    if a == b:
        return seg_sqdist(a, c, d)
    if c == d:
        return seg_sqdist(c, a, b)

    def cross(o, p, q):
        return (p[0] - o[0]) * (q[1] - o[1]) - (p[1] - o[1]) * (q[0] - o[0])
    d1, d2 = sign_q3(cross(c, d, a)), sign_q3(cross(c, d, b))
    d3, d4 = sign_q3(cross(a, b, c)), sign_q3(cross(a, b, d))
    if d1 * d2 < 0 and d3 * d4 < 0:
        return Q3(0)
    if d1 == 0 and _on_seg(c, d, a):
        return Q3(0)
    if d2 == 0 and _on_seg(c, d, b):
        return Q3(0)
    if d3 == 0 and _on_seg(a, b, c):
        return Q3(0)
    if d4 == 0 and _on_seg(a, b, d):
        return Q3(0)
    return min(seg_sqdist(a, c, d), seg_sqdist(b, c, d),
               seg_sqdist(c, a, b), seg_sqdist(d, a, b))


def _on_seg(a, b, p):
    ca = _sub(p, a)
    cb = _sub(b, a)
    if sign_q3(ca[0] * cb[1] - ca[1] * cb[0]) != 0:
        return False
    t = (ca[0] * cb[0] + ca[1] * cb[1])
    tt = (cb[0] * cb[0] + cb[1] * cb[1])
    return Q3(0) <= t <= tt


def box_hex_sqdist(box, m, n):
    """exact squared distance between a closed axis-parallel box (x0,x1,y0,y1) and hexagon (m,n).
       0 iff they meet."""
    x0, x1, y0, y1 = box
    if x0 == x1 and y0 == y1:
        return point_hex_sqdist((x0, y0), m, n)
    if point_in_hex(((x0 + x1) / Q3(2), (y0 + y1) / Q3(2)), m, n):
        return Q3(0)
    bc = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    vs = verts(m, n)
    for p in bc:
        if point_in_hex(p, m, n):
            return Q3(0)
    return min(seg_seg_sqdist(bc[i], bc[(i + 1) % 4], vs[j], vs[(j + 1) % 6])
               for i in range(4) for j in range(6))


def box_hex_sqfar(box, m, n):
    """exact squared distance between a closed box and the farthest point of hexagon (m,n)."""
    x0, x1, y0, y1 = box
    bc = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    return max(sqdist(p, v) for p in bc for v in verts(m, n))


# ---------------------------------------------------------------- fast float prefilter
import math as _math

# outward normals of the Voronoi hexagon (unit vectors at angles 0,60,120 deg)
_NORMALS = [(1.0, 0.0),
            (0.5, _math.sqrt(3.0) / 2.0),
            (-0.5, _math.sqrt(3.0) / 2.0)]


def sep_gap_float(box, m, n):
    """float separating-axis gap between the closed box and hexagon (m,n).
       gap > 0 (beyond float noise)  ==>  they are disjoint."""
    x0, x1, y0, y1 = box
    fx0, fx1, fy0, fy1 = float(x0), float(x1), float(y0), float(y1)
    bc = [(fx0, fy0), (fx1, fy0), (fx1, fy1), (fx0, fy1)]
    hv = [(float(v[0]), float(v[1])) for v in verts(m, n)]
    best = -1e18
    for (nx, ny) in _NORMALS + [(1.0, 0.0), (0.0, 1.0)]:
        bp = [x * nx + y * ny for (x, y) in bc]
        hp = [x * nx + y * ny for (x, y) in hv]
        gap = max(min(bp) - max(hp), min(hp) - max(bp))
        if gap > best:
            best = gap
    return best


def box_hex_meets(box, m, n, margin=1e-9):
    """exact decision: does the closed box meet the closed hexagon?"""
    if sep_gap_float(box, m, n) > margin:
        return False
    return box_hex_sqdist(box, m, n) == Q3(0)
