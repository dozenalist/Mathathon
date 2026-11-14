"""The paper's seven-colouring: exact geometry.

Lattice Lambda = d (Z + Z omega),  d = sqrt3 * r,  r = 2/5,  omega = e^{2 pi i/3}.
z(m,n) = d(m + n omega) = ( sqrt3 (2m-n)/5 , 3n/5 ).
Colour of the Voronoi hexagon of z(m,n) is (m + 2n) mod 7
(Lambda / (2-omega)Lambda = Z/7, and omega = 2 in that quotient).
Hexagons have circumradius r=2/5, inradius sqrt3/5; vertices at angles 30+60k deg.
"""
from fractions import Fraction as F
from field import Q3

R_HEX = F(2, 5)


def z(m, n):
    """lattice centre, exact"""
    return (Q3(0, F(2 * m - n, 5)), Q3(F(3 * n, 5)))


def colour(m, n):
    return (m + 2 * n) % 7


# hexagon vertex offset directions  cos/sin of 30+60k, exact
_OFF = [
    (Q3(0, F(1, 5)), Q3(F(1, 5))),      # (sqrt3/5, 1/5)
    (Q3(0), Q3(F(2, 5))),               # (0, 2/5)
    (Q3(0, F(-1, 5)), Q3(F(1, 5))),
    (Q3(0, F(-1, 5)), Q3(F(-1, 5))),
    (Q3(0), Q3(F(-2, 5))),
    (Q3(0, F(1, 5)), Q3(F(-1, 5))),
]


def hex_vertices(m, n):
    c = z(m, n)
    return [(c[0] + dx, c[1] + dy) for dx, dy in _OFF]


def sub(p, q):
    return (p[0] - q[0], p[1] - q[1])


def add(p, q):
    return (p[0] + q[0], p[1] + q[1])


def dot(p, q):
    return p[0] * q[0] + p[1] * q[1]


def norm2(p):
    return dot(p, p)


def dist2(p, q):
    return norm2(sub(p, q))


def seg_dist2(p, a, b):
    """squared distance from p to the closed segment ab, exactly (Q(sqrt3))."""
    ab = sub(b, a)
    ap = sub(p, a)
    L = norm2(ab)
    if L == 0:
        return norm2(ap)
    t = dot(ap, ab) / L          # in Q(sqrt3)
    if t <= 0:
        return norm2(ap)
    if t >= 1:
        return dist2(p, b)
    # |ap|^2 - t^2 |ab|^2
    return norm2(ap) - t * t * L


def hex_dist2(p, m, n):
    """squared distance from p to the closed hexagon of (m,n); 0 if p is inside."""
    v = hex_vertices(m, n)
    c = z(m, n)
    # convex: p inside iff p is on the inner side of every edge.
    # edges of the Voronoi cell: p is inside iff for every lattice neighbour w,
    # |p-c|^2 <= |p-(c+w)|^2 , i.e. 2 <p-c, w> <= |w|^2.
    for (dm, dn) in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1),
                     (1, -1), (-1, 1), (2, -1), (-2, 1)]:
        w = sub(z(m + dm, n + dn), c)
        if norm2(w) == Q3(0):
            continue
        # only the six nearest neighbours matter (|w|^2 = d^2); skip the rest
        if norm2(w) > Q3(F(12, 25)) + Q3(F(1, 1000)):
            continue
        if 2 * dot(sub(p, c), w) > norm2(w):
            break
    else:
        return Q3(0)
    # outside: minimum over edges
    best = None
    for i in range(6):
        dd = seg_dist2(p, v[i], v[(i + 1) % 6])
        if best is None or dd < best:
            best = dd
    return best


def hex_maxdist2(p, m, n):
    v = hex_vertices(m, n)
    return max(dist2(p, q) for q in v)


def colour_of_point(p):
    """colour of the hexagon containing p (nearest lattice point)."""
    # search a generous window of lattice points
    best = None
    bestc = None
    for m in range(-6, 7):
        for n in range(-6, 7):
            dd = dist2(p, z(m, n))
            if best is None or dd < best:
                best, bestc = dd, colour(m, n)
    return bestc, best
