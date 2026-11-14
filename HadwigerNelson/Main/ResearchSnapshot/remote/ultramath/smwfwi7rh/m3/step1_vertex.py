"""Step 1: exact structure of the seven-colouring's transition graph.

Key exact fact: the six unit vectors of Z+Zomega have the six distinct nonzero
colours mod 7; hence at every vertex of the hexagonal tiling the three incident
hexagons carry three distinct colours.
"""
from fractions import Fraction as F
from field import Q3
from hexcol import z, colour, hex_vertices, dist2

# the six unit vectors of Z + Z omega, as (m,n) pairs
UNITS = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, -1)]
print("unit vector colours:", [(u, colour(*u) % 7) for u in UNITS])
assert sorted(colour(*u) % 7 for u in UNITS) == [1, 2, 3, 4, 5, 6]
print("=> the six unit vectors carry exactly the six nonzero residues mod 7")

# elementary triangles: c, c+u, c+u+v with u, v, u+v units (all six directions)
unit_set = set(UNITS)
triples = []
for u in UNITS:
    for v in UNITS:
        s = (u[0] + v[0], u[1] + v[1])
        if s in unit_set and v != (0, 0):
            triples.append((u, v, s))
print("number of oriented elementary triangles per centre:", len(triples))

# exact check: distinct colours in every elementary triangle, for every centre
bad = 0
for m0 in range(-3, 4):
    for n0 in range(-3, 4):
        c0 = colour(m0, n0)
        for (u, v, s) in triples:
            cols = {c0 % 7, (c0 + colour(*u)) % 7, (c0 + colour(*s)) % 7}
            if len(cols) != 3:
                bad += 1
print("elementary triangles with a repeated colour:", bad)
print("(proof: colours are c, c+col(u), c+col(u)+col(v); col(u),col(v) in {1..6},")
print(" and col(v) != 0 forces col(u) != col(u)+col(v) mod 7.)")

# the vertex set: circumcentres.  A vertex is the point v30 of a hexagon.
verts = set()
for m in range(-4, 5):
    for n in range(-4, 5):
        for (x, y) in hex_vertices(m, n):
            verts.add((x, y))
print("distinct vertices found in a window:", len(verts))
# each vertex is at distance r from exactly three centres -> check one
v = hex_vertices(0, 0)[0]
hits = [(m, n) for m in range(-3, 4) for n in range(-3, 4)
        if dist2(v, z(m, n)) == Q3(F(4, 25))]
print("centres at distance exactly r = 2/5 from that vertex:", hits,
      "colours", [colour(m, n) for m, n in hits])
