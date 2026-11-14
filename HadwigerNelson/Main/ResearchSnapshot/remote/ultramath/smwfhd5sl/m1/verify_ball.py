#!/usr/bin/env python3
"""d7, part 2: the window ladder at radius one, exactly.

Window          colours forced (exact)
S^1(x)          2        (six-cycles, Theorem 1)
S^1(x) u {x}    3        (cone over six-cycles; lower bound: x sees every circle
                          point, and both neighbours of a circle point are
                          distinct from it)
B(x,1)          >= 4     (the 7-vertex Moser spindle, exact coordinates from
                          lean/OAI/Geometry/PlaneColoring/Moser.lean, fits in a
                          closed disc of radius R_spindle <= 1 -- computed here
                          exactly)

Coordinates (Lean, Moser.lean):
  A = (sqrt3 + i)/2, B = (sqrt3 - i)/2, T = sqrt3, U = (5 + i sqrt11)/6
  p0 = 0, p1 = A, p2 = B, p3 = T, p4 = U*A, p5 = U*B, p6 = U*T
  edges = 01 02 12 31 32 04 05 45 64 65 36
"""
import itertools
import math
import sympy as sp

s3, s11 = sp.sqrt(3), sp.sqrt(11)
I = sp.I

A = (s3 + I) / 2
B = (s3 - I) / 2
T = s3
U = (5 + I * s11) / 6
P = [sp.Integer(0), A, B, T, U * A, U * B, U * T]


def re(z):
    return sp.simplify(sp.re(sp.expand(z)))


def im(z):
    return sp.simplify(sp.im(sp.expand(z)))


def sqd(i, j):
    dx = sp.expand(re(P[i]) - re(P[j]))
    dy = sp.expand(im(P[i]) - im(P[j]))
    return sp.simplify(sp.expand(dx ** 2 + dy ** 2))


print("=" * 78)
print("1. The Moser spindle: exact unit edges, and no extra unit pairs")
print("=" * 78)
lean_edges = [(0, 1), (0, 2), (1, 2), (3, 1), (3, 2), (0, 4), (0, 5),
              (4, 5), (6, 4), (6, 5), (3, 6)]
units = set()
D = {}
for i in range(7):
    for j in range(i + 1, 7):
        d = sqd(i, j)
        D[(i, j)] = d
        if sp.simplify(d - 1) == 0:
            units.add((i, j))
print("pairs at distance exactly 1:", sorted(units))
print("Lean edge list (as unordered pairs):",
      sorted(tuple(sorted(e)) for e in lean_edges))
assert units == set(tuple(sorted(e)) for e in lean_edges), "edge sets differ"
print("agreement: the coordinate distances and the Lean edge list are identical.")
print()

print("=" * 78)
print("2. chi(spindle) = 4 by exhaustive search")
print("=" * 78)
adj = [set() for _ in range(7)]
for a, b in units:
    adj[a].add(b)
    adj[b].add(a)


def colourable(k):
    order = sorted(range(7), key=lambda v: -len(adj[v]))
    col = {}


def find_colouring(k):
    order = sorted(range(7), key=lambda v: -len(adj[v]))
    col = {}

    def rec(i):
        if i == 7:
            return dict(col)
        v = order[i]
        for c in range(k):
            if all(col.get(u) != c for u in adj[v]):
                col[v] = c
                r = rec(i + 1)
                if r is not None:
                    return r
                del col[v]
        return None

    return rec(0)


print("degrees:", [len(adj[v]) for v in range(7)])
for k in (2, 3, 4, 5):
    r = find_colouring(k)
    print(f"  k = {k}: " + ("NOT colourable" if r is None else f"colouring {r}"))
assert find_colouring(3) is None
assert find_colouring(4) is not None
print("chi(spindle) = 4  [exhaustive over all 3^7 and 4^7 assignments]")
print()

print("=" * 78)
print("3. The cone over six-cycles: chi(S^1(x) u {x}) = 3, exactly")
print("=" * 78)
# six consecutive points of a 2pi/6 orbit on the unit circle, plus the centre
C6 = [(sp.cos(sp.pi * k / 3), sp.sin(sp.pi * k / 3)) for k in range(6)]
for k in range(6):
    assert sp.simplify((C6[k][0] - C6[(k + 1) % 6][0]) ** 2 + (C6[k][1] - C6[(k + 1) % 6][1]) ** 2 - 1) == 0
    # every circle point is at distance 1 from the centre 0
    assert sp.simplify(C6[k][0] ** 2 + C6[k][1] ** 2 - 1) == 0
print("six orbit points: consecutive distances 1, and each at distance 1 from the centre")
# graph: vertex 6 = the centre, universal to 0..5; 0..5 form a C_6
cone_adj = [set() for _ in range(7)]
for k in range(6):
    cone_adj[6].add(k)
    cone_adj[k].add(6)
    cone_adj[k].add((k + 1) % 6)
    cone_adj[(k + 1) % 6].add(k)


def find_colouring_adj(adj_, n, k):
    order = sorted(range(n), key=lambda v: -len(adj_[v]))
    col = {}

    def rec(i):
        if i == n:
            return dict(col)
        v = order[i]
        for c in range(k):
            if all(col.get(u) != c for u in adj_[v]):
                col[v] = c
                r = rec(i + 1)
                if r is not None:
                    return r
                del col[v]
        return None

    return rec(0)


print("  k = 2:", "NOT colourable" if find_colouring_adj(cone_adj, 7, 2) is None else "colourable")
print("  k = 3:", find_colouring_adj(cone_adj, 7, 3))
assert find_colouring_adj(cone_adj, 7, 2) is None
assert find_colouring_adj(cone_adj, 7, 3) is not None
print("chi = 3 = k-3 at k = 6: the palette bound of Proposition 5.6 at k = 6 is the")
print("chromatic number of the unit ball's skeleton, and it is attained.")
print()

print("=" * 78)
print("4. Exact minimal enclosing circle of the spindle")
print("=" * 78)
xy = [(sp.nsimplify(re(p)), sp.nsimplify(im(p))) for p in P]
for i, (x, y) in enumerate(xy):
    print(f"  p{i} = ({float(x.evalf()):+.6f}, {float(y.evalf()):+.6f})")


def circle_from2(i, j):
    cx = (xy[i][0] + xy[j][0]) / 2
    cy = (xy[i][1] + xy[j][1]) / 2
    r2 = sp.simplify((xy[i][0] - cx) ** 2 + (xy[i][1] - cy) ** 2)
    return cx, cy, r2


def circle_from3(i, j, k):
    (x1, y1), (x2, y2), (x3, y3) = xy[i], xy[j], xy[k]
    d = 2 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
    if sp.simplify(d) == 0:
        return None
    ux = ((x1 ** 2 + y1 ** 2) * (y2 - y3) + (x2 ** 2 + y2 ** 2) * (y3 - y1) + (x3 ** 2 + y3 ** 2) * (y1 - y2)) / d
    uy = ((x1 ** 2 + y1 ** 2) * (x3 - x2) + (x2 ** 2 + y2 ** 2) * (x1 - x3) + (x3 ** 2 + y3 ** 2) * (x2 - x1)) / d
    ux, uy = sp.simplify(ux), sp.simplify(uy)
    r2 = sp.simplify((x1 - ux) ** 2 + (y1 - uy) ** 2)
    return ux, uy, r2


def covers(cx, cy, r2):
    return all(sp.simplify(r2 - ((x - cx) ** 2 + (y - cy) ** 2)) >= 0 for x, y in xy)


best = None
for i, j in itertools.combinations(range(7), 2):
    cx, cy, r2 = circle_from2(i, j)
    if covers(cx, cy, r2):
        if best is None or sp.simplify(r2 - best[2]) < 0:
            best = (cx, cy, r2, ("diameter", i, j))
for i, j, k in itertools.combinations(range(7), 3):
    c = circle_from3(i, j, k)
    if c is None:
        continue
    cx, cy, r2 = c
    if covers(cx, cy, r2):
        if best is None or sp.simplify(r2 - best[2]) < 0:
            best = (cx, cy, r2, ("circumcircle", i, j, k))
cx, cy, r2, how = best
print("minimal enclosing circle: centre =", (sp.nsimplify(cx), sp.nsimplify(cy)),
      " r^2 =", sp.nsimplify(r2), " r =", sp.nsimplify(sp.sqrt(r2)))
print("  r =", float(sp.sqrt(r2).evalf()), " determined by", how)
print("  determined by", how, "; all 7 points inside: ", covers(cx, cy, r2))
print("  r <= 1?", bool(sp.simplify(r2) <= 1), " exakt r^2 - 1 =", sp.simplify(r2 - 1))
print()
print("ALL CHECKS DONE")
