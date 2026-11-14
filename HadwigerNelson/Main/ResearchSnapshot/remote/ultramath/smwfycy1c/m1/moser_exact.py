#!/usr/bin/env python3
"""Exact verification of the Moser-spindle claims of Lemma 8.9.

Geometry is done in K = Q(sqrt3, sqrt11) with the exact Q-basis
{1, r3, r11, r3*r11}; a field element is a 4-tuple of Fractions.
No floating point is used anywhere.
Colourings are counted by complete enumeration (exact integers).
"""

from fractions import Fraction as F
from itertools import product

# ---------------------------------------------------------------- exact field
# element a + b*r3 + c*r11 + d*r3*r11   (r3^2 = 3, r11^2 = 11)

def E(a=0, b=0, c=0, d=0):
    return (F(a), F(b), F(c), F(d))

ZERO = E(0)
ONE = E(1)


def add(x, y): return tuple(x[i] + y[i] for i in range(4))
def sub(x, y): return tuple(x[i] - y[i] for i in range(4))
def neg(x): return tuple(-x[i] for i in range(4))


def mul(x, y):
    a1, b1, c1, d1 = x
    a2, b2, c2, d2 = y
    return (a1*a2 + 3*b1*b2 + 11*c1*c2 + 33*d1*d2,      # constant
            a1*b2 + b1*a2 + 11*(c1*d2 + d1*c2),          # * r3
            a1*c2 + c1*a2 + 3*(b1*d2 + d1*b2),           # * r11
            a1*d2 + d1*a2 + b1*c2 + c1*b2)               # * r3*r11


def is_zero(x): return all(v == 0 for v in x)
def eq(x, y): return all(x[i] == y[i] for i in range(4))


def show(x):
    """Pretty print a + b r3 + c r11 + d r33 with rational coefficients."""
    parts = []
    names = ["1", "r3", "r11", "r33"]
    for v, n in zip(x, names):
        if v != 0:
            parts.append(f"{v}*{n}" if n != "1" else f"{v}")
    return " + ".join(parts) if parts else "0"


R3 = E(0, 1)
R11 = E(0, 0, 1)
R33 = E(0, 0, 0, 1)
HALF = E(F(1, 2))
SIXTH = E(F(1, 6))

# ------------------------------------------------------- the seven points
# Points are pairs (x, y) of field elements, meaning z = x + i*y.

def cmul(z, w):
    """Complex multiplication of pairs over K."""
    (x1, y1), (x2, y2) = z, w
    return (sub(mul(x1, x2), mul(y1, y2)), add(mul(x1, y2), mul(y1, x2)))


u  = (E(F(5, 6)), mul(SIXTH, R11))     # u = (5 + i sqrt11)/6
Z  = (ZERO, ZERO)                      # 0
A  = (mul(HALF, R3), HALF)             # (sqrt3 + i)/2
B  = (mul(HALF, R3), neg(HALF))        # (sqrt3 - i)/2
T  = (R3, ZERO)                        # sqrt3
uA = cmul(u, A)
uB = cmul(u, B)
uT = cmul(u, T)

names = ["0", "A", "B", "T", "uA", "uB", "uT"]
P = {"0": Z, "A": A, "B": B, "T": T, "uA": uA, "uB": uB, "uT": uT}


def sqdist(z, w):
    dx = sub(z[0], w[0])
    dy = sub(z[1], w[1])
    return add(mul(dx, dx), mul(dy, dy))


edges = [("0", "A"), ("0", "B"), ("A", "B"), ("T", "A"), ("T", "B"),
         ("0", "uA"), ("0", "uB"), ("uA", "uB"), ("uT", "uA"), ("uT", "uB"),
         ("T", "uT")]

print("=" * 72)
print("1. COORDINATES  (over Q + Q*r3 + Q*r11 + Q*r3*r11)")
print("=" * 72)
for n in names:
    x, y = P[n]
    print(f"  {n:3s}: x = {show(x):45s}  y = {show(y)}")

print()
print("=" * 72)
print("2. SQUARED EDGE LENGTHS  (must all be exactly 1)")
print("=" * 72)
all_unit = True
for a, b in edges:
    d2 = sqdist(P[a], P[b])
    ok = eq(d2, ONE)
    all_unit &= ok
    print(f"  |{a:2s}-{b:2s}|^2 = {show(d2):20s}   == 1 ? {ok}")
print(f"\n  ALL ELEVEN EDGES HAVE SQUARED LENGTH EXACTLY 1: {all_unit}")
print(f"  number of edges = {len(edges)}, distinct undirected pairs = "
      f"{len({frozenset(e) for e in edges})}")

print()
print("=" * 72)
print("3. PAIRWISE DISTINCTNESS OF THE SEVEN POINTS")
print("=" * 72)
distinct = True
collisions = []
for i in range(len(names)):
    for j in range(i + 1, len(names)):
        same = eq(P[names[i]][0], P[names[j]][0]) and eq(P[names[i]][1], P[names[j]][1])
        if same:
            distinct = False
            collisions.append((names[i], names[j]))
print(f"  #distinct points = {len({(P[n][0], P[n][1]) for n in names})} (expect 7)")
if collisions:
    print(f"  COLLISIONS: {collisions}")
print(f"  ALL SEVEN POINTS PAIRWISE DISTINCT: {distinct}")

print()
print("=" * 72)
print("4. WHICH PAIRS ARE AT UNIT DISTANCE (among all 21 pairs)")
print("=" * 72)
unit_pairs = []
for i in range(len(names)):
    for j in range(i + 1, len(names)):
        if eq(sqdist(P[names[i]], P[names[j]]), ONE):
            unit_pairs.append((names[i], names[j]))
print(f"  unit-distance pairs found: {len(unit_pairs)}")
print(f"  {unit_pairs}")
print(f"  equals the 11-edge list as a set: "
      f"{set(map(frozenset, unit_pairs)) == set(map(frozenset, edges))}")

# --------------------------------------------------------------- colourings
print()
print("=" * 72)
print("5. PROPER COLOURINGS  (complete enumeration, exact)")
print("=" * 72)

idx = {n: k for k, n in enumerate(names)}
adj = [(idx[a], idx[b]) for a, b in edges]


def count_colourings(k, edge_list):
    """Number of proper k-colourings of the graph (V=7 vertices, edge_list)."""
    total = 0
    colourings = []
    for c in product(range(k), repeat=7):
        if all(c[i] != c[j] for i, j in edge_list):
            total += 1
            colourings.append(c)
    return total, colourings


def up_to_perm(colourings, k):
    """Number of colourings modulo permutation of the k colours
    (i.e. number of proper k-partitions-with-unused-colours merged)."""
    canon = set()
    for c in colourings:
        # canonical form: order colours by first appearance
        m = {}
        out = []
        for v in c:
            if v not in m:
                m[v] = len(m)
            out.append(m[v])
        canon.add(tuple(out))
    return len(canon)


full3, _ = count_colourings(3, adj)
print(f"  full 11-edge graph, proper 3-colourings: {full3}")
full4, col4 = count_colourings(4, adj)
print(f"  full 11-edge graph, proper 4-colourings: {full4}")
print(f"    of which modulo colour permutation:  {up_to_perm(col4, 4)}")
print()
print("  chromatic polynomial at k (full graph):")
for k in range(0, 8):
    n, _ = count_colourings(k, adj)
    print(f"    P({k}) = {n}")

print()
print("=" * 72)
print("6. SINGLE-EDGE DELETIONS: proper 3-colourings of G - e")
print("=" * 72)
rows = []
minimal = True
for e in edges:
    sub_edges = [x for x in adj if frozenset(x) != frozenset((idx[e[0]], idx[e[1]]))]
    assert len(sub_edges) == 10
    n3, cols3 = count_colourings(3, sub_edges)
    n3p = up_to_perm(cols3, 3)
    rows.append((e, n3, n3p))
    if n3 == 0:
        minimal = False
print(f"  {'edge e':>10s} | 3-colourings of G-e | modulo colour perm")
for e, n3, n3p in rows:
    print(f"  {e[0]:>2s}-{e[1]:<7s} | {n3:>19d} | {n3p:>18d}")
print()
print(f"  number of edges whose deletion makes G 3-colourable: "
      f"{sum(1 for _, n3, _ in rows if n3 > 0)} / 11")
print(f"  redundant edges (G-e still not 3-colourable): "
      f"{[e for e, n3, _ in rows if n3 == 0]}")
print(f"  EDGE-MINIMAL FOR NON-3-COLOURABILITY (every deletion 3-colourable): "
      f"{all(n3 > 0 for _, n3, _ in rows)}")
print()
print(f"  full graph 4-colourable: {full4 > 0}; full graph 3-colourable: {full3 > 0}")
print(f"  chi(G) = 4 and chi(G-e) = 3 for every e  =>  G is 4-critical: "
      f"{full3 == 0 and all(n3 > 0 for _, n3, _ in rows) and full4 > 0}")

# extra: independence/pairing structure of the unique-up-to-permutation colourings
print()
print("=" * 72)
print("7. THE 3-COLOURINGS OF G - e, LISTED (up to colour permutation)")
print("=" * 72)
for e in edges:
    sub_edges = [x for x in adj if frozenset(x) != frozenset((idx[e[0]], idx[e[1]]))]
    n3, cols3 = count_colourings(3, sub_edges)
    canon = {}
    for c in cols3:
        m = {}
        out = []
        for v in c:
            if v not in m:
                m[v] = len(m)
            out.append(m[v])
        canon.setdefault(tuple(out), 0)
        canon[tuple(out)] += 1
    reps = list(canon)
    print(f"  G - ({e[0]},{e[1]}): {n3} colourings = {len(reps)} up to perm, "
          f"{[dict(zip(names, r)) for r in reps]}")
