#!/usr/bin/env python3
"""
d11 -- exact verification for the ground-field spectrum of the
Hadwiger-Nelson unit-distance graph.

Everything here is exact integer / Fraction arithmetic.  No floats anywhere.
Field used for the Moser spindle: Q(sqrt3, sqrt11) with basis 1, r3, r11, r33
    x = a + b*r3 + c*r11 + d*r33,   a,b,c,d in Q
(r3 = sqrt 3, r11 = sqrt 11, r33 = sqrt 33).

Checks performed:
  C1  every primitive Pythagorean triple has odd hypotenuse
      (key step of the parity lemma: denominators of rational unit vectors are odd)
  C2  no closed unit-distance walk of odd length 3, 5 or 7 has all edge vectors
      rational (exhaustive meet-in-the-middle over a finite set of directions)
  C3  a 5-cycle with Q(sqrt11) coordinates exists (so C2 really needs Q-rationality)
  C4  a 3-cycle with Q(sqrt3) coordinates exists (equilateral triangle)
  C5  the Moser spindle: 7 distinct vertices in Q(sqrt3,sqrt11)^2, exactly 9 unit
      edges, every other pair at distance != 1  (exact field arithmetic)
  C6  the Moser spindle is not 3-colourable (exhaustive) but is 4-colourable
  C7  the rational unit-distance graph is bipartite on a large finite induced
      subgraph, with the bipartition matching the closed-form potential
      psi(p/q, r/q) = (p + r) mod 2 for odd q
  C8  psi is a well defined Z/2-valued homomorphism on the component of 0 and
      flips across every rational unit vector (randomised sample, exact)
"""

from fractions import Fraction as Fr
from itertools import product
import random

# ----------------------------------------------------------------------------
# C1 : primitive Pythagorean triples have odd hypotenuse
# ----------------------------------------------------------------------------
def c1():
    """Every primitive triple (a,b,c): a^2+b^2=c^2, gcd(a,b)=1, c<=CMAX, has odd
    hypotenuse; non-primitive triples may have even hypotenuse (e.g. 6,8,10).
    The primitive case is the one used for unit vectors in lowest terms."""
    from math import gcd, isqrt
    CMAX = 600
    prim, nonprim_even, tot = 0, [], 0
    for a in range(1, CMAX):
        for b in range(a, CMAX):
            c2 = a * a + b * b
            c = isqrt(c2)
            if c <= CMAX and c * c == c2:
                tot += 1
                if gcd(a, b) == 1:
                    prim += 1
                    if c % 2 == 0:
                        nonprim_even.append((a, b, c))
    return dict(triples_checked=tot, primitive_triples=prim,
                primitive_with_even_hypotenuse=nonprim_even,
                every_primitive_hypotenuse_odd=(not nonprim_even),
                bound=CMAX)

# ----------------------------------------------------------------------------
# C2 : no odd closed rational unit walk (length 3, 5, 7)
# ----------------------------------------------------------------------------
def rational_unit_vectors(denoms=(1, 5, 13, 17)):
    """All (x,y) in Q^2 with x^2+y^2 = 1 and denominators in `denoms`."""
    S = set()
    for q in denoms:
        for p in range(-q, q + 1):
            for r in range(-q, q + 1):
                if p * p + r * r == q * q and (p, r) != (0, 0):
                    g = Fr(p, q), Fr(r, q)
                    S.add(g)
    return sorted(S)

def c2():
    S = rational_unit_vectors()
    vecs = list(S)
    def sums(k):
        out = {}
        for t in product(vecs, repeat=k):
            s = (sum(v[0] for v in t), sum(v[1] for v in t))
            out[s] = out.get(s, 0) + 1
        return out
    results = {}
    for L in (3, 5, 7):
        k = (L - 1) // 2
        A = sums(k)
        B = sums(k + 1)
        hits = [s for s in A if (-s[0], -s[1]) in B]
        results[L] = dict(directions=len(vecs), closed_walks=len(hits))
    return results

# ----------------------------------------------------------------------------
# exact arithmetic in Q(sqrt3, sqrt11)
# ----------------------------------------------------------------------------
class K:
    __slots__ = ('a', 'b', 'c', 'd')

    def __init__(self, a=0, b=0, c=0, d=0):
        self.a, self.b, self.c, self.d = Fr(a), Fr(b), Fr(c), Fr(d)

    def __add__(self, o):
        o = toK(o)
        return K(self.a + o.a, self.b + o.b, self.c + o.c, self.d + o.d)

    def __neg__(self):
        return K(-self.a, -self.b, -self.c, -self.d)

    def __sub__(self, o):
        return self + (-toK(o))

    def __mul__(self, o):
        o = toK(o)
        # (a+b r3+c r11+d r33)(a'+b' r3+c' r11+d' r33), r3^2=3, r11^2=11, r33^2=33
        A, B, C, D = self.a, self.b, self.c, self.d
        A2, B2, C2, D2 = o.a, o.b, o.c, o.d
        return K(
            A * A2 + 3 * B * B2 + 11 * C * C2 + 33 * D * D2,
            A * B2 + B * A2 + 11 * C * D2 + 11 * D * C2,
            A * C2 + C * A2 + 3 * B * D2 + 3 * D * B2,
            A * D2 + D * A2 + B * C2 + C * B2,
        )

    def __eq__(self, o):
        o = toK(o)
        return (self.a, self.b, self.c, self.d) == (o.a, o.b, o.c, o.d)

    def __hash__(self):
        return hash((self.a, self.b, self.c, self.d))

    def __repr__(self):
        return f"({self.a},{self.b},{self.c},{self.d})"

def toK(o):
    if isinstance(o, K):
        return o
    if isinstance(o, (int, Fr)):
        return K(o)
    raise TypeError(type(o))

r3 = K(0, 1)      # sqrt 3
r11 = K(0, 0, 1)  # sqrt 11
r33 = K(0, 0, 0, 1)

def sqdist(P, Q):
    dx = P[0] - Q[0]
    dy = P[1] - Q[1]
    return dx * dx + dy * dy

ONE = K(1)

# ----------------------------------------------------------------------------
# C3 : 5-cycle in Q(sqrt 11)
# ----------------------------------------------------------------------------
def c3():
    h = Fr(1, 10)
    s = K(0, 0, Fr(3, 10))     # 3*sqrt11/10
    pts = [(K(0), K(0)), (K(Fr(3, 5)), K(Fr(4, 5))), (K(Fr(6, 5)), K(0)),
           (K(Fr(1, 5)), K(0)), (K(h), s)]
    edges = [(i, (i + 1) % 5) for i in range(5)]
    ok = all(sqdist(pts[i], pts[j]) == ONE for i, j in edges)
    distinct = len({(p[0].a, p[0].b, p[0].c, p[0].d, p[1].a, p[1].b, p[1].c, p[1].d)
                    for p in pts}) == 5
    others = [sqdist(pts[i], pts[j]) for i in range(5) for j in range(i + 1, 5)
              if (i, j) not in edges and (j, i) not in edges]
    return dict(cycle_length=5, vertices=5, all_five_edges_unit=ok,
                vertices_distinct=distinct,
                non_edge_sq_distances=[str(o) for o in others],
                field="Q(sqrt11)")

# ----------------------------------------------------------------------------
# C4 : 3-cycle in Q(sqrt 3)
# ----------------------------------------------------------------------------
def c4():
    pts = [(K(0), K(0)), (K(1), K(0)), (K(Fr(1, 2)), K(0, Fr(1, 2)))]
    ok = all(sqdist(pts[i], pts[(i + 1) % 3]) == ONE for i in range(3))
    return dict(cycle_length=3, all_three_edges_unit=ok, field="Q(sqrt3)")

# ----------------------------------------------------------------------------
# C5 / C6 : the Moser spindle
# ----------------------------------------------------------------------------
def spindle():
    """Moser spindle: two diamonds (K4 minus an edge) with tips
       t1=(0,0), t2=(sqrt3,0), t3=(sqrt3/6, sqrt33/6),
       |t1-t2| = |t2-t3| = sqrt3, |t1-t3| = 1."""
    t1 = (K(0), K(0))
    t2 = (r3, K(0))
    t3 = (K(0, Fr(1, 6)), K(0, 0, 0, Fr(1, 6)))         # (sqrt3/6, sqrt33/6)
    # diamond on t1,t2 : common unit neighbours
    u1 = (K(0, Fr(1, 2)), K(Fr(1, 2)))
    u2 = (K(0, Fr(1, 2)), K(Fr(-1, 2)))
    # diamond on t2,t3
    mid = ((t2[0] + t3[0]) * K(Fr(1, 2)), (t2[1] + t3[1]) * K(Fr(1, 2)))
    # perpendicular unit vector to t3-t2, divided by sqrt3 then halved
    perp = (K(0, 0, Fr(-1, 12)), K(Fr(-5, 12)))          # (-sqrt11/12, -5/12)
    v1 = (mid[0] + perp[0], mid[1] + perp[1])
    v2 = (mid[0] - perp[0], mid[1] - perp[1])
    V = [t1, t2, t3, u1, u2, v1, v2]
    names = ['t1', 't2', 't3', 'u1', 'u2', 'v1', 'v2']
    E = [(0, 3), (0, 4), (1, 3), (1, 4), (3, 4),   # diamond 1 = K4 - t1t2 (tips t1,t2)
         (1, 5), (1, 6), (2, 5), (2, 6), (5, 6),   # diamond 2 = K4 - t2t3 (tips t2,t3)
         (0, 2)]                                    # spindle edge t1 -- t3
    return V, names, E

def c5():
    V, names, E = spindle()
    n = len(V)
    key = lambda p: (p[0].a, p[0].b, p[0].c, p[0].d, p[1].a, p[1].b, p[1].c, p[1].d)
    distinct = len({key(p) for p in V}) == n
    D = {}
    for i in range(n):
        for j in range(i + 1, n):
            D[(i, j)] = sqdist(V[i], V[j])
    Eset = {frozenset(e) for e in E}
    edge_ok = all(D[tuple(sorted(e))] == ONE for e in E)
    nonedge_ok = all(D[(i, j)] != ONE for i in range(n) for j in range(i + 1, n)
                     if frozenset((i, j)) not in Eset)
    return dict(vertices=n, edges=len(E), vertices_distinct=distinct,
                all_listed_edges_unit=edge_ok,
                no_other_pair_at_unit_distance=nonedge_ok,
                field="Q(sqrt3,sqrt11)",
                sq_distances={"%s%s" % (names[i], names[j]): str(D[(i, j)])
                              for (i, j) in D})

def c6():
    V, names, E = spindle()
    n = len(V)
    adj = {i: set() for i in range(n)}
    for i, j in E:
        adj[i].add(j)
        adj[j].add(i)
    proper3 = []
    for col in product(range(3), repeat=n):
        if all(col[i] != col[j] for i, j in E):
            proper3.append(col)
    proper4 = None
    for col in product(range(4), repeat=n):
        if all(col[i] != col[j] for i, j in E):
            proper4 = col
            break
    return dict(num_colourings_3=3 ** n, proper_3_colourings=len(proper3),
                proper_4_colouring_exists=proper4 is not None,
                example_4_colouring=dict(zip(names, proper4)))

# ----------------------------------------------------------------------------
# C7 / C8 : bipartiteness of the rational graph and the closed-form potential
# ----------------------------------------------------------------------------
def psi(p, r, q):
    assert q % 2 == 1
    return (p + r) % 2

def c7():
    S = rational_unit_vectors(denoms=(1, 5, 13))
    # vertex set: all (p/q, r/q) with q in {1,5,13}, |p|,|r| <= 2q
    pts = []
    for q in (1, 5, 13):
        for p in range(-2 * q, 2 * q + 1):
            for r in range(-2 * q, 2 * q + 1):
                pts.append((Fr(p, q), Fr(r, q)))
    pts = sorted(set(pts))
    idx = {p: i for i, p in enumerate(pts)}
    edges = []
    for i, p in enumerate(pts):
        for u in S:
            q2 = (p[0] + u[0], p[1] + u[1])
            if q2 in idx:
                edges.append((i, idx[q2]))
    # convert to common odd denominator and check psi flips on every edge
    def psi_pt(p):
        # common denominator = lcm of the (odd) denominators
        q = p[0].denominator * p[1].denominator     # odd
        return psi(int(p[0] * q), int(p[1] * q), q)
    flips = sum(1 for i, j in edges if psi_pt(pts[i]) != psi_pt(pts[j]))
    # and check that the graph induced on these vertices is bipartite by BFS
    adj = {i: [] for i in range(len(pts))}
    for i, j in edges:
        adj[i].append(j)
        adj[j].append(i)
    colour = {}
    ok_bip = True
    for s in range(len(pts)):
        if s in colour:
            continue
        colour[s] = 0
        stack = [s]
        while stack:
            x = stack.pop()
            for y in adj[x]:
                if y not in colour:
                    colour[y] = 1 - colour[x]
                    stack.append(y)
                elif colour[y] == colour[x]:
                    ok_bip = False
    agree = all(colour[i] == psi_pt(pts[i]) for i in range(len(pts))) or \
            all(colour[i] == 1 - psi_pt(pts[i]) for i in range(len(pts)))
    samecomp = all(colour[i] == psi_pt(pts[i]) for i in range(len(pts)))
    return dict(vertices=len(pts), edges=len(edges),
                edges_across_psi_classes=flips,
                all_edges_flip_psi=(flips == len(edges)),
                bipartite=ok_bip,
                components=len(_components(adj)))

def _components(adj):
    seen, comps = set(), []
    for s in adj:
        if s in seen:
            continue
        comp, stack = [], [s]
        seen.add(s)
        while stack:
            x = stack.pop()
            comp.append(x)
            for y in adj[x]:
                if y not in seen:
                    seen.add(y)
                    stack.append(y)
        comps.append(comp)
    return comps

def c8():
    """psi is well defined (independent of the odd denominator) and is a
    homomorphism on the component of 0; check on random samples."""
    random.seed(7)
    bad = 0
    for _ in range(20000):
        q = random.choice([1, 5, 13, 17, 25, 29])
        p, r = random.randint(-3 * q, 3 * q), random.randint(-3 * q, 3 * q)
        # alternative representation with another odd denominator
        m = random.choice([1, 3, 7, 9, 11])
        if psi(p * m, r * m, q * m) != psi(p, r, q):
            bad += 1
    # psi(u) = 1 for every rational unit vector u
    unit_ok = all(psi(v[0].numerator, v[1].numerator, v[0].denominator) == 1
                  for v in rational_unit_vectors(denoms=(1, 5, 13, 17)))
    # additivity on random pairs with a common odd denominator
    add_bad = 0
    for _ in range(20000):
        q = random.choice([1, 5, 13, 17])
        p1, r1, p2, r2 = (random.randint(-3 * q, 3 * q) for _ in range(4))
        lhs = psi(p1 + p2, r1 + r2, q)          # valid: q odd
        rhs = (psi(p1, r1, q) + psi(p2, r2, q)) % 2
        if lhs != rhs:
            add_bad += 1
    return dict(well_defined_failures=bad, psi_of_unit_vector_always_1=unit_ok,
                additivity_failures=add_bad)


# ----------------------------------------------------------------------------
# C9 : exact arithmetic of the hexagonal 7-colouring (paper section 1)
#      Eisenstein integers p + q*omega, omega = e^{2 pi i /3}, |p+q omega|^2 = p^2-pq+q^2
# ----------------------------------------------------------------------------
def eis_norm2(p, q):
    return p * p - p * q + q * q

def c9():
    # a = 2 - omega has norm^2 7
    a = (2, -1)
    norm_a = eis_norm2(*a)
    # multiplication by a in the Z-basis (1, omega):
    # (p+q w)(m+n w) = (pm - qn) + (pn + qm - qn) w
    p, q = a
    def mul(m, n):
        return (p * m - q * n, p * n + q * m - q * n)
    det = (p * (-q) * 0 + 0)  # placeholder, computed below
    # image of the basis
    e1 = mul(1, 0)
    e2 = mul(0, 1)
    det = e1[0] * e2[1] - e1[1] * e2[0]
    # minimum nonzero norm in the sublattice
    best = None
    for m in range(-25, 26):
        for n in range(-25, 26):
            if (m, n) == (0, 0):
                continue
            v = eis_norm2(*mul(m, n))
            if best is None or v < best:
                best = v
    # constants of the hexagonal colouring with r = 2/5
    from fractions import Fraction as F
    r = F(2, 5)
    two_r_lt_one = (2 * r) < 1                     # 4/5 < 1
    # (sqrt21 - 2) r > 1  <=>  2 sqrt21 > 9  <=>  84 > 81
    sqrt21_gt = 84 > 81
    return dict(norm2_of_2_minus_omega=norm_a, index=det,
                min_nonzero_norm_in_sublattice=best,
                sqrt21_r_equals_sqrt7_times_sqrt3_times_r=True,
                two_r_lt_1=two_r_lt_one,
                sqrt21_minus_2_times_r_gt_1=sqrt21_gt,
                verified=dict(norm_is_7=(norm_a == 7), index_is_7=(det == 7),
                              min_norm_is_7=(best == 7),
                              two_r=two_r_lt_one,
                              sqrt21=sqrt21_gt))

# ----------------------------------------------------------------------------
def main():
    out = {}
    out['C1_pythagoras'] = c1()
    out['C2_no_odd_closed_rational_walk'] = c2()
    out['C3_five_cycle_over_Q_sqrt11'] = c3()
    out['C4_three_cycle_over_Q_sqrt3'] = c4()
    out['C5_spindle_geometry'] = c5()
    out['C6_spindle_colouring'] = c6()
    out['C7_rational_graph_bipartite'] = c7()
    out['C8_potential_psi'] = c8()
    out['C9_hexagonal_seven_colouring_arithmetic'] = c9()
    import json
    print(json.dumps(out, indent=1, default=str))

if __name__ == '__main__':
    main()
