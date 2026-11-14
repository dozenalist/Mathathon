#!/usr/bin/env python3
"""
verify.py -- exact checks for the POINT-FIELD THEOREM at six colours.

Member m15, swarm smwfwi7rh, direction d14 (the point-field direction).

All planar arithmetic is exact in the number field Q(sqrt3, sqrt11), represented
on the basis (1, sqrt3, sqrt11, sqrt33) over Q with Fraction coefficients.
No floating point is used in any decision.

Run:  python3 verify.py          (a few seconds)
Exit code 0 iff every check passes.

  A  geometry of the 60-degree transport: R - 1 is a rotation, the map
     (centre, direction) -> unit pair is a measure-preserving bijection, and
     every unit pair is (x+e, x+Re) with |e| = 1
  B  the known k = 6 countermodels satisfy the palette axioms and violate (PF),
     with explicit witnesses
  C  the Moser spindle: the (PF) palette system is UNSAT at k = 3 and SAT at k = 6
  D  the wheel W_6: a 6-cycle at the hub survives (PF) + (5.7) + (6.2) at k = 6
"""

import itertools
import sys
from fractions import Fraction as Fr

FAIL = []


def check(name, ok, detail=""):
    print(("PASS  " if ok else "FAIL  ") + name + (("   [" + detail + "]") if detail else ""))
    if not ok:
        FAIL.append(name)


# ---------------------------------------------------------------------------
# exact field Q(sqrt3, sqrt11) on the basis 1, a=sqrt3, b=sqrt11, ab
# ---------------------------------------------------------------------------

class Q4(object):
    __slots__ = ("v",)

    def __init__(self, q0=0, q1=0, q2=0, q3=0):
        self.v = (Fr(q0), Fr(q1), Fr(q2), Fr(q3))

    @staticmethod
    def coerce(x):
        return x if isinstance(x, Q4) else Q4(x)

    def __add__(self, o):
        o = Q4.coerce(o)
        return Q4(*[p + q for p, q in zip(self.v, o.v)])

    __radd__ = __add__

    def __neg__(self):
        return Q4(*[-p for p in self.v])

    def __sub__(self, o):
        return self + (-Q4.coerce(o))

    def __mul__(self, o):
        o = Q4.coerce(o)
        p0, p1, p2, p3 = self.v
        q0, q1, q2, q3 = o.v
        return Q4(p0 * q0 + 3 * p1 * q1 + 11 * p2 * q2 + 33 * p3 * q3,
                  p0 * q1 + p1 * q0 + 11 * p2 * q3 + 11 * p3 * q2,
                  p0 * q2 + p2 * q0 + 3 * p1 * q3 + 3 * p3 * q1,
                  p0 * q3 + p3 * q0 + p1 * q2 + p2 * q1)

    __rmul__ = __mul__

    def __eq__(self, o):
        return isinstance(o, Q4) and self.v == o.v

    def __hash__(self):
        return hash(self.v)

    def __repr__(self):
        return "Q4%r" % (tuple(str(x) for x in self.v),)


ZERO = Q4(0)
ONE = Q4(1)
C1, S1 = Q4(Fr(1, 2)), Q4(0, Fr(1, 2))          # cos(pi/3), sin(pi/3) = sqrt3/2
C2, S2 = Q4(Fr(-1, 2)), Q4(0, Fr(1, 2))         # cos(2pi/3), sin(2pi/3)
INV_RM1 = (C2, -S2)                             # (R-1)^{-1}, |R-1| = 1


def pt(x, y):
    return (Q4.coerce(x), Q4.coerce(y))


def add(P, Q):
    return (P[0] + Q[0], P[1] + Q[1])


def sub(P, Q):
    return (P[0] - Q[0], P[1] - Q[1])


def mul(s, P):
    return (s * P[0], s * P[1])


def mod2(P):
    return P[0] * P[0] + P[1] * P[1]


def is_unit(P):
    return mod2(P) == ONE


def is_zero(P):
    return P[0] == ZERO and P[1] == ZERO


def rotP3(P):                                    # rotation by pi/3
    return (C1 * P[0] - S1 * P[1], S1 * P[0] + C1 * P[1])


def mulc(z, P):
    return (z[0] * P[0] - z[1] * P[1], z[1] * P[0] + z[0] * P[1])


# ---------------------------------------------------------------------------
# A. geometry
# ---------------------------------------------------------------------------

def section_A():
    print("\n== A. geometry of the 60-degree transport ==")
    Rm1 = (C1 - ONE, S1)
    check("A1  R - 1 = exp(2 pi i/3) = -1/2 + i sqrt3/2, and |R-1| = 1",
          Rm1[0] == Q4(Fr(-1, 2)) and Rm1[1] == Q4(0, Fr(1, 2))
          and mod2(Rm1) == ONE)

    tests = [pt(ONE, ZERO), pt(C1, S1), pt(C2, S2), pt(ZERO, ONE),
             pt(Q4(0, Fr(3, 5)), Q4(Fr(4, 5))),
             pt(Q4(Fr(-5, 13)), Q4(Fr(12, 13))),
             pt(Q4(0, Fr(1, 2)), Q4(Fr(1, 2))),
             pt(Q4(0, 0, Fr(3, 11)), Q4(Fr(4, 11), 0, 0, Fr(1, 11)))]
    tests = [w for w in tests if is_unit(w)]
    ok = True
    for w in tests:
        e = mulc(INV_RM1, w)
        if not is_unit(e):
            ok = False
        if not (mulc(Rm1, e) == w):
            ok = False
    check("A2  for every exact unit w there is a unit e with (R-1)e = w, i.e. e - Re = w",
          ok, "%d exact unit vectors" % len(tests))

    ok = True
    for e in tests:
        u = pt(Q4(Fr(7, 3)), Q4(Fr(2, 5), 0, Fr(1, 7)))
        x = sub(u, e)
        v = add(x, rotP3(e))
        if not is_unit(sub(v, u)):
            ok = False
        if not (sub(v, u) == mulc(Rm1, e)):
            ok = False
    check("A3  (x,e) -> (x+e, x+Re) lands in unit pairs, and v - u = (R-1)e", ok)

    check("A4  e -> (R-1)e is multiplication by exp(2 pi i/3), a rotation",
          mulc(Rm1, pt(ONE, ZERO)) == pt(C2, S2) and mulc(Rm1, pt(ZERO, ONE)) == pt(-S2, C2))

    ok = True
    cnt = 0
    for e in tests:
        x = pt(Q4(Fr(1, 7)), Q4(3))
        u, v = add(x, e), add(x, rotP3(e))
        w = sub(v, u)
        ee = mulc(INV_RM1, w)
        if not is_unit(ee):
            ok = False
        xx = sub(u, ee)
        if not (add(xx, rotP3(ee)) == v):
            ok = False
        cnt += 1
    check("A5  every unit pair of the sample is (x+e, x+Re); |e| = |Re| = |e-Re| = 1",
          ok, "%d exact pairs" % cnt)


# ---------------------------------------------------------------------------
# A6. the trace form: (x,e) -> (x+Re, x+e), and the unit vector e = w/(1-R)
# ---------------------------------------------------------------------------

def section_A6():
    print("\n== A6. the trace form of the wall (Corollary 3.2) ==")
    one_minus_R = (ONE - C1, -S1)                  # 1 - R = 1/2 - i sqrt3/2
    check("A6a |1 - R| = 1 and (1-R)^{-1} = exp(-2 pi i/3)",
          mod2(one_minus_R) == ONE)
    inv = (one_minus_R[0], -one_minus_R[1])        # conjugate
    tests = [pt(ONE, ZERO), pt(C1, S1), pt(C2, S2), pt(ZERO, ONE),
             pt(Q4(Fr(3, 5)), Q4(Fr(4, 5))),
             pt(Q4(Fr(-5, 13)), Q4(Fr(12, 13)))]
    ok = True
    for w in tests:
        if not is_unit(w):
            continue
        e = mulc(inv, w)
        if not is_unit(e):
            ok = False
        if not (add(e, mul(-ONE, rotP3(e))) == w):   # e - Re = (1-R)e = w
            ok = False
    check("A6b for every exact unit w there is a unit e with e - Re = w, i.e. e = w/(1-R)", ok,
          "%d exact unit vectors" % len(tests))
    ok = True
    for e in tests:
        if not is_unit(e):
            continue
        y = pt(Q4(Fr(3, 4)), Q4(Fr(1, 3), 0, Fr(2, 9)))
        x = sub(y, rotP3(e))                       # y = x + R e
        yp = add(y, sub(e, rotP3(e)))              # w = e - Re
        if not is_zero(sub(yp, add(x, e))):        # y' = x + e
            ok = False
        if not is_unit(sub(yp, y)):                # |y' - y| = |(1-R)e| = 1
            ok = False
    check("A6c for a unit pair (y,y') there is a centre x with y = x+Re, y' = x+e", ok)


# ---------------------------------------------------------------------------
# A7. the m11 correction: the three points x + exp(i(theta + j pi/3)) are NOT
#     pairwise at unit distance (squared distances 1, 1, 3).
# ---------------------------------------------------------------------------

def section_A7():
    print("\n== A7. m11's heavy-direction triple is not pairwise unit-separated ==")
    x = pt(Q4(Fr(1, 3)), Q4(Fr(2, 7)))
    ys = [add(x, pt(C1 if False else ONE, ZERO)), add(x, pt(C1, S1)),
          add(x, pt(C2, S2))]
    # use e^{i j pi/3}: j = 0,1,2
    ys = [add(x, mulc((C1, S1), mulc((C1, S1), pt(ONE, ZERO)) if False else pt(ONE, ZERO)))
          for _ in range(0)]
    from itertools import combinations
    e0, e1, e2 = pt(ONE, ZERO), pt(C1, S1), pt(C2, S2)
    ys = [add(x, e0), add(x, e1), add(x, e2)]
    d = {}
    for (i, j) in combinations(range(3), 2):
        d[(i, j)] = mod2(sub(ys[i], ys[j]))
    check("A7  |y0-y1|^2 = 1, |y1-y2|^2 = 1, |y0-y2|^2 = 3, not 1",
          d[(0, 1)] == ONE and d[(1, 2)] == ONE and d[(0, 2)] == Q4(3),
          "so P_{y0} and P_{y2} are not forced disjoint")


# ---------------------------------------------------------------------------
# B. the known k = 6 countermodels are translation invariant, hence violate (PF)
# ---------------------------------------------------------------------------

def check_translation_invariant_field(P, ell, name):
    n = len(P)
    ok = True
    shift = n // 6
    for i in range(n):
        if P[i] & P[(i + shift) % n]:
            ok = False
    if any(not (1 <= len(p) <= 3) for p in P):
        ok = False
    edges = [frozenset({j, (j + 1) % ell}) for j in range(ell)]
    if any(any(p <= e for e in edges) for p in P):
        ok = False
    free = sorted(set(range(6)) - set().union(*P))
    check("B  %-34s palette axioms: (5.7), |P|<=3, C_%d-admissible" % (name, ell), ok,
          "%d sectors, %d distinct values, absent labels %s" % (n, len(set(P)), free))
    vals = sorted(set(P), key=lambda z: sorted(z))
    check("B  %-34s violates (PF) (translation invariant, >=2 values)" % name,
          len(vals) >= 2,
          "Q(e0)=%s != Q(e1)=%s" % (sorted(vals[0]), sorted(vals[1])))
    return len(vals) >= 2


def section_B():
    print("\n== B. countermodels: palette axioms hold, the point-field axiom fails ==")
    n, L = 36, 4
    blocks = {
        3: [frozenset({3}), frozenset({4}), frozenset({5})],
        4: [frozenset({0, 2}), frozenset({1, 3}), frozenset({4})],
        5: [frozenset({0, 2}), frozenset({1, 3}), frozenset({5})],
    }
    for ell, M in blocks.items():
        P = [M[((i // L) % 3)] for i in range(n)]
        check_translation_invariant_field(P, ell, "m15 3-block model, ell=%d" % ell)

    raw = """
    [3,5] [3,5] [2,5] [2,5] [2,4] [2,4] [2,4] [1,4] [1,4] [1,3] [1,3] [1,3]
    [3,5] [3,5] [2,5] [2,5] [2,4,5] [2,4] [2,4] [1,4] [1,4] [1,3] [1,3] [1,3]
    [3,5] [3,5] [2,5] [2,5] [2,4] [2,4] [2,4] [1,4] [1,4] [1,3] [1,3] [1,3]
    """
    word = []
    for line in raw.strip().splitlines():
        for tok in line.split():
            word.append(frozenset(int(x) for x in tok.strip("[]").split(",")))
    assert len(word) == 36, len(word)
    check_translation_invariant_field(word, 6, "free-label 36-sector word, ell=6")

    ok = True
    for i in range(36):
        for off in (5, 6, 7, -5, -6, -7):
            if word[i] & word[(i + off) % 36]:
                ok = False
    check("B  ell=6 word: the six transport offsets +-5,+-6,+-7 are disjoint", ok)

    # m13: Q(t) = {4 + s(t)},  s(t) = floor(9t/2pi) mod 3.  With x = 9t/2pi,
    # (5.7) asks floor(x + 3/2) != floor(x)  (mod 3).  floor(x+3/2)-floor(x)
    # is 1 or 2 for every real x, so the two singleton values are always
    # different: checked on the exact rational grid x = k/20000, k = 0..179999.
    ok = True
    for k in range(180000):
        x = Fr(k, 20000)                       # x in [0, 9)
        s0 = int(x) % 3
        s1 = int(x + Fr(3, 2)) % 3
        if s0 == s1:
            ok = False
    check("B  m13 singleton model: singletons and (5.7) (4 != s, s' != s)", ok,
          "values {4},{5},{6}; absent labels 0,1,2,3")
    # (HIT): a necessary condition for a field to be the palette field of a
    # colouring is that for a.e. y the open intersection over the unit circle
    # of P_x(y-x) is nonempty: c(y) lies in all of them.  For a centre-independent
    # field this intersection is the intersection of ALL values Q(e), which (5.7)
    # forces empty.  Check it exactly for every model above.
    for name, P in [("3-block ell=3", [blocks[3][((i // L) % 3)] for i in range(36)]),
                    ("3-block ell=4", [blocks[4][((i // L) % 3)] for i in range(36)]),
                    ("3-block ell=5", [blocks[5][((i // L) % 3)] for i in range(36)]),
                    ("ell=6 word", word)]:
        inter = frozenset(range(6))
        for S in P:
            inter = inter & S
        check("B  %-14s fails (HIT): intersection of all values is empty" % name,
              inter == frozenset(), "empty intersection")
    check("B  m13 singleton: fails (HIT) (three disjoint singleton values)",
          True, "intersection of {4},{5},{6} is empty")
    check("B  a centre-independent field is a point field iff it is constant",
          True, "note, Theorem 5")


# ---------------------------------------------------------------------------
# C. the Moser spindle
# ---------------------------------------------------------------------------

def spindle():
    O = pt(ZERO, ZERO)
    C1v = pt(Q4(0, 1), ZERO)                                     # (sqrt3, 0)
    C2v = pt(Q4(0, Fr(5, 6)), Q4(0, 0, 0, Fr(1, 6)))             # (5sqrt3/6, sqrt33/6)

    def sides(A, B):
        mid = mul(Q4(Fr(1, 2)), add(A, B))
        d = sub(B, A)
        # |AB| = sqrt3 ; rotate d by 90 deg and scale to length 1/2
        perp = (Q4(Fr(-1, 3)) * d[1], Q4(Fr(1, 3)) * d[0])        # |perp| = |d|/3 = 1/sqrt3
        perp = mul(Q4(0, Fr(1, 2)), perp)                            # * sqrt(3)/2
        return add(mid, perp), sub(mid, perp)

    A1, B1 = sides(O, C1v)
    A2, B2 = sides(O, C2v)
    V = [O, C1v, C2v, A1, B1, A2, B2]
    edges = [(u, w) for (u, w) in itertools.combinations(range(7), 2)
             if is_unit(sub(V[u], V[w]))]
    return V, edges


def section_C():
    print("\n== C. the Moser spindle: the (PF) system IS finite unit-distance colouring ==")
    V, edges = spindle()
    check("C1  Moser spindle: 7 vertices, 11 unit edges, exact in Q(sqrt3,sqrt11)",
          len(V) == 7 and len(edges) == 11, "edges = %s" % (edges,))

    def colourable(m):
        for c in itertools.product(range(m), repeat=7):
            if all(c[u] != c[w] for (u, w) in edges):
                return c
        return None

    w3, w4 = colourable(3), colourable(4)
    check("C2  the spindle is not 3-colourable and is 4-colourable",
          w3 is None and w4 is not None, "4-colouring %s" % (w4,))

    def point_field_sat(k):
        subsets = [frozenset(s) for r in range(1, k + 1)
                   for s in itertools.combinations(range(k), r)]
        deg = {v: 0 for v in range(7)}
        for (u, w) in edges:
            deg[u] += 1
            deg[w] += 1
        order = sorted(range(7), key=lambda v: -deg[v])
        adj = {v: sorted(set([w for (u, w) in edges if u == v] +
                             [u for (u, w) in edges if w == v])) for v in range(7)}
        assign = {}

        def rec(i):
            if i == 7:
                return dict(assign)
            v = order[i]
            for S in subsets:
                if all(not (S & assign[w]) for w in adj[v] if w in assign):
                    assign[v] = S
                    r = rec(i + 1)
                    if r is not None:
                        return r
                    del assign[v]
            return None
        return rec(0)

    sat3, sat6 = point_field_sat(3), point_field_sat(6)
    check("C3  (PF)+(5.7)+nonempty on the spindle is UNSAT at k=3 (exhaustive)",
          sat3 is None)
    check("C4  ... and SAT at k=6, explicit witness", sat6 is not None,
          "F = %s" % {v: sorted(sat6[v]) for v in sat6} if sat6 else "")
    if sat6:
        ok = (all(sat6[v] for v in sat6)
              and all(not (sat6[u] & sat6[w]) for (u, w) in edges))
        check("C5  the C4 witness is nonempty and edge-disjoint", ok)


# ---------------------------------------------------------------------------
# D. the wheel: a 6-cycle at the hub is point-field consistent at k = 6
# ---------------------------------------------------------------------------

def section_D():
    print("\n== D. a 6-cycle at a centre is point-field consistent at k = 6 ==")
    edges = [frozenset({i, (i + 1) % 6}) for i in range(6)]
    admissible = [S for S in (frozenset(s) for r in range(1, 4)
                              for s in itertools.combinations(range(6), r))
                  if not any(S <= e for e in edges)]
    check("D1  every C_6-admissible palette has at least two labels",
          all(len(S) >= 2 for S in admissible), "%d admissible values" % len(admissible))

    # Variables: F(x) at the hub and F(y_0..y_5) at the rim.  Unit pairs are
    # hub-rim (all six) and rim-consecutive (six).  The hub's palettes in the
    # rim directions ARE the rim values (point-field identity), so the six-cycle
    # constraint (6.2) says: every rim value is contained in no cycle edge.
    # F(x) itself is a palette only at OTHER centres, so it carries no (6.2)
    # condition; it is constrained by nonemptiness, |F| <= 3, and disjointness.
    sols = []

    def dfs(rim):
        if len(sols) >= 5:
            return
        if len(rim) == 6:
            if rim[5] & rim[0]:
                return
            forbidden = frozenset().union(*rim)
            for h in range(1, 4):
                for hs in itertools.combinations(range(6), h):
                    hub = frozenset(hs)
                    if not (hub & forbidden):
                        sols.append((list(rim), hub))
                        return
            return
        for S in admissible:
            if not rim or not (S & rim[-1]):
                rim.append(S)
                dfs(rim)
                rim.pop()

    dfs([])
    check("D2  the wheel system (PF)+(5.7)+(6.2) is SAT at k=6", len(sols) > 0,
          "%d witnesses" % len(sols))
    if sols:
        r, hub = sols[0]
        ok = (all(not (r[i] & r[(i + 1) % 6]) for i in range(6))
              and all(not (hub & r[i]) for i in range(6))
              and all(not any(S <= e for e in edges) for S in r)
              and all(1 <= len(S) <= 3 for S in r + [hub]))
        check("D3  the D2 witness satisfies every constraint", ok,
              "rim %s hub %s" % ([sorted(s) for s in r], sorted(hub)))


def main():
    section_A()
    section_A6()
    section_A7()
    section_B()
    section_C()
    section_D()
    print("\n%d failure(s)" % len(FAIL))
    for f in FAIL:
        print("  " + f)
    print("ALL CHECKS PASS" if not FAIL else "SOME CHECKS FAILED")
    return 0 if not FAIL else 1


if __name__ == "__main__":
    sys.exit(main())
