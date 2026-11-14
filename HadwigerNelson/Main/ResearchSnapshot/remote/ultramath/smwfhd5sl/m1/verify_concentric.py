#!/usr/bin/env python3
"""Is the 4-chromatic spindle realisable on two CONCENTRIC circles?
If yes, Theorem B must be restricted to a single radius (several radii would
then suffice to beat 3 colours at one centre).  Exact search over partitions.
"""
import itertools
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
    z = sp.expand(p)
    xy.append((sp.nsimplify(sp.simplify(sp.re(z))), sp.nsimplify(sp.simplify(sp.im(z)))))


def circumcentre(idxs):
    """centre equidistant from the given points, exact (or None)."""
    (x1, y1), (x2, y2), (x3, y3) = xy[idxs[0]], xy[idxs[1]], xy[idxs[2]]
    d = sp.simplify(2 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)))
    if d == 0:
        return None
    ux = sp.simplify(((x1 ** 2 + y1 ** 2) * (y2 - y3) + (x2 ** 2 + y2 ** 2) * (y3 - y1) +
                      (x3 ** 2 + y3 ** 2) * (y1 - y2)) / d)
    uy = sp.simplify(((x1 ** 2 + y1 ** 2) * (x3 - x2) + (x2 ** 2 + y2 ** 2) * (x1 - x3) +
                      (x3 ** 2 + y3 ** 2) * (x2 - x1)) / d)
    return ux, uy


def ncircles(c):
    return len({sp.simplify((x - c[0]) ** 2 + (y - c[1]) ** 2) for x, y in xy})


found = []
# candidate centres: circumcentres of triples, and midpoints of pairs
cands = []
for tri in itertools.combinations(range(7), 3):
    c = circumcentre(tri)
    if c is not None:
        cands.append(c)
for pair in itertools.combinations(range(7), 2):
    cands.append(((xy[pair[0]][0] + xy[pair[1]][0]) / 2, (xy[pair[0]][1] + xy[pair[1]][1]) / 2))
for c in cands:
    n = ncircles(c)
    if n <= 2:
        found.append((c, n))
print("centres giving at most two distinct distances:", len(found))
for c, n in found[:5]:
    print("   centre", (sp.nsimplify(c[0]), sp.nsimplify(c[1])), "-> circles:", n)
if not found:
    print("   NONE: the spindle is NOT realisable on two concentric circles.")
print()
print("distance-squared profile from the origin:", len({sp.simplify(x**2 + y**2) for x, y in xy}),
      "distinct values")
