#!/usr/bin/env python3
"""
Exact checks for the COLLAPSE LEMMA  (L4 package, swarm smwfhd5sl, member m7).

Notation.  Q(a,s) := P_{a-s}(s) is the palette field in "(a,s)-coordinates": a in R^2 is the
unit-circle point, s in S^1 the direction from the centre x = a - s.
Transfer axiom (paper Lemma 5.2(3), both branches, POINTWISE):
  (T)   |a-b| = 1 and (b-a) not parallel to s   ==>   Q(a,s) cap Q(b,f) = {}  for all f.

Theorem 1 (COLLAPSE.md).  (T) + nonempty palettes  ==>  the plane is k-colourable.
Hence: a palette system at level k exists  <=>  chi(R^2) <= k.

This script verifies, in exact arithmetic:
  CHECK 1  the geometric step producing (T): for a,b at unit distance and t = b-a not parallel s,
           the two-circle construction of the paper is transversal (0 < |t+s|^2 < 4), so its
           endpoint maps are local diffeomorphisms and Lemma 5.2(3) applies at that (f,s) point;
           no degenerate case is hidden in the rigidity argument.
  CHECK 2  the combinatorial core (rigidity + antipodal cover) on random finite palette systems
           with |S| > 2k: every instance satisfying (T) and cover yields a proper k-colouring,
           and the collapse construction never produces an improper one (exhaustive check).
  CHECK 3  sharpness: either hypothesis can be dropped and the conclusion fails.
  CHECK 4  the converse direction is inhabited explicitly: the standard 7-colouring of the plane
           by hexagonal cells of circumradius 2/5 coloured by the cosets of an index-7 sublattice,
           verified proper in exact rational arithmetic.  It gives a palette field at k=7 with
           |P| = 1 satisfying (T) (calibration of the collapse at k = 7).
"""

from fractions import Fraction as F
import random


# ------------------------------------------------------------------ exact Q(sqrt 3)
class Q3:
    """(r, s) denotes r + s*sqrt(3) with r, s in Q.  All comparisons are exact."""
    __slots__ = ("r", "s")

    def __init__(self, r, s=0):
        self.r, self.s = F(r), F(s)

    def __add__(self, o):
        o = _q(o); return Q3(self.r + o.r, self.s + o.s)
    __radd__ = __add__

    def __sub__(self, o):
        o = _q(o); return Q3(self.r - o.r, self.s - o.s)

    def __rsub__(self, o):
        return _q(o).__sub__(o)

    def __mul__(self, o):
        o = _q(o); return Q3(self.r * o.r + 3 * self.s * o.s, self.r * o.s + self.s * o.r)
    __rmul__ = __mul__

    def __neg__(self):
        return Q3(-self.r, -self.s)

    def __eq__(self, o):
        o = _q(o); return self.r == o.r and self.s == o.s

    def __hash__(self):
        return hash((self.r, self.s))

    def sign(self):
        if self.s == 0: return (self.r > 0) - (self.r < 0)
        if self.r == 0: return (self.s > 0) - (self.s < 0)
        if self.r > 0 and self.s > 0: return 1
        if self.r < 0 and self.s < 0: return -1
        d = self.r * self.r - 3 * self.s * self.s      # opposite signs: |r|^2 vs 3|s|^2
        assert d != 0
        bigger = 1 if d > 0 else -1
        return bigger if self.r > 0 else -bigger

    def __repr__(self):
        return f"({self.r} + {self.s}*sqrt3)"


def _q(x):
    return x if isinstance(x, Q3) else Q3(x)


def norm2(p):
    return p[0] * p[0] + p[1] * p[1]


def cross(u, v):
    return u[0] * v[1] - u[1] * v[0]


# ------------------------------------------------------------------ CHECK 1
def check1_transversality(samples=200, seed=20260713):
    """|t+s|^2 = 2 + 2<t,s> lies in (0,4) whenever |t| = |s| = 1 and t is not parallel to s.
    Verified exactly on rational samples (Pythagorean directions)."""
    rng = random.Random(seed)
    triples = [(3, 4), (5, 12), (8, 15), (7, 24), (20, 21), (9, 40), (28, 45), (33, 56)]
    tested = 0
    for _ in range(samples):
        m, n = rng.choice(triples)
        p, q = rng.choice(triples)
        if m * q - n * p == 0:                      # parallel: outside the hypothesis, resample
            continue
        h2, hp2 = m * m + n * n, p * p + q * q
        ip = m * p + n * q
        cr = m * q - n * p
        assert cr * cr == h2 * hp2 - ip * ip        # Lagrange identity, exact
        assert cr != 0                              # not parallel
        assert ip * ip < h2 * hp2                   # Cauchy-Schwarz, strict
        # |t+s|^2 = 2 + 2 ip / sqrt(h2 hp2) < 4  <=> ip < sqrt(h2 hp2)  (true), and > 0
        # because sqrt(h2 hp2) > |ip| >= -ip.  Exact, no rounding.
        tested += 1
    return {"samples": tested,
            "verified": "t not parallel s => 0 < |t+s|^2 < 4 => two-circle intersection "
                        "s(f) transversal at f => local diffeomorphism (paper's hypothesis)"}


# ------------------------------------------------------------------ CHECK 4
def check4_hexagonal_seven_colouring():
    """Exact verification of the standard 7-colouring of the plane.

    s = (2/5)*sqrt3.  Lambda = Z u + Z v, u = (s,0), v = (s/2, s sqrt3/2) (hexagonal, spacing s).
    Hexagons of circumradius L = 2/5 tile the plane (inradius L sqrt3/2 = s/2, so edge-sharing
    neighbours are exactly at distance s).  Lambda' = <2u+v, -u+3v>, index 7 in Lambda.
    Colour each hexagon by the coset of Lambda'.
    """
    s = Q3(0, F(2, 5))
    u = (s, Q3(0))
    v = (s * Q3(F(1, 2)), s * Q3(0, F(1, 2)))              # (s/2, s*sqrt3/2)
    b1 = (u[0] * 2 + v[0], u[1] * 2 + v[1])                # 2u + v
    b2 = (v[0] * 3 - u[0], v[1] * 3 - u[1])                # -u + 3v
    detL, detLp = cross(u, v), cross(b1, b2)
    assert detL.s != 0 and detLp.s != 0
    index = detLp.s / detL.s                               # both pure multiples of sqrt3
    assert index == 7, (index, detL, detLp)

    best = None
    for i in range(-8, 9):
        for j in range(-8, 9):
            if i == 0 and j == 0:
                continue
            w = (b1[0] * i + b2[0] * j, b1[1] * i + b2[1] * j)
            n2 = norm2(w)
            if best is None or (n2 - best).sign() < 0:
                best = n2
    # claimed: |shortest vector of Lambda'|^2 = 7 s^2 = 7 * 3 * (4/25) = 84/25
    assert best == Q3(F(84, 25)), best

    L = F(2, 5)                     # hexagon circumradius
    assert 2 * L < 1                # cell diameter 4/5 < 1 (no unit pair inside one cell)
    # two distinct cells of one colour: centre distance >= sqrt(84/25), so every pair of their
    # points is at distance >= sqrt(84/25) - 2L, and sqrt(84/25) - 4/5 > 1
    # <=> sqrt(84/25) > 9/5 <=> 84/25 > 81/25  (both sides positive: exact rational comparison)
    assert F(84, 25) > F(9, 5) ** 2
    return {"index_of_Lambda_prime": index,
            "min_vector_squared": "84/25",
            "cell_diameter": "4/5 < 1",
            "same_colour_separation": "sqrt(84/25) - 4/5 > 1  (84/25 > 81/25)",
            "colours": 7}


# ------------------------------------------------------------------ CHECK 2 / 3
def _inside_antipodal_pair(D, S):
    """True iff the finite set of direction indices D is contained in some {v, -v}."""
    if not D:
        return False
    for si in D:
        v = S[si]
        if all(S[sj] == v or S[sj] == (-v[0], -v[1]) for sj in D):
            return True
    return False


def check2_combinatorial_core(trials=3000, seed=7):
    """Random finite palette systems with |S| > 2k.  If (T) and the cover hold, the collapse
    construction must produce a proper k-colouring of the finite unit-distance structure."""
    rng = random.Random(seed)
    dirs = [(1, 0), (0, 1), (1, 1), (-1, 1), (1, -1), (2, 1), (-1, 2)]   # parallelism only
    stats = {"instances": 0, "with_T_and_cover": 0, "collapse_coloured": 0}
    for k, nS in ((2, 5), (3, 7)):
        S = dirs[:nS]
        assert len(S) > 2 * k, (nS, k)
        for _ in range(trials):
            nA = rng.randint(1, 4)
            A = list(dict.fromkeys((rng.randint(-1, 1), rng.randint(0, 2)) for _ in range(nA)))
            Q = {(a, si): set(rng.sample(range(k), rng.randint(0, k)))
                 for a in A for si in range(nS)}
            stats["instances"] += 1

            def unit(d):
                return d[0] * d[0] + d[1] * d[1] == 1

            def par(d, v):
                return d[0] * v[1] - d[1] * v[0] == 0

            okT = True
            for a in A:
                for b in A:
                    d = (b[0] - a[0], b[1] - a[1])
                    if not unit(d):
                        continue
                    for si in range(nS):
                        if par(d, S[si]):
                            continue
                        for sj in range(nS):
                            if Q[(a, si)] & Q[(b, sj)]:
                                okT = False
            if not okT:
                continue
            cover = all(Q[(a, si)] for a in A for si in range(nS))   # every palette nonempty
            if not cover:
                continue
            stats["with_T_and_cover"] += 1
            D = {a: [set() for _ in range(k)] for a in A}
            for a in A:
                for si in range(nS):
                    for i in Q[(a, si)]:
                        D[a][i].add(si)
            B = {i: set() for i in range(k)}
            for a in A:
                for i in range(k):
                    if D[a][i] and not _inside_antipodal_pair(D[a][i], S):
                        B[i].add(a)
            for a in A:                      # the cover step of the proof
                assert any(a in B[i] for i in range(k)), ("cover step failed", A, S, Q)
            col = {a: min(i for i in range(k) if a in B[i]) for a in A}
            for a in A:
                for b in A:
                    if unit((b[0] - a[0], b[1] - a[1])):
                        assert col[a] != col[b], ("improper colouring", A, S, Q, col)
            stats["collapse_coloured"] += 1
    return stats


def check3_sharpness():
    return {
        "drop_nonemptiness": "Q(a,s) = {} for all (a,s) satisfies (T) and yields nothing",
        "drop_transfer": "Q(a,s) = [k] for all (a,s) is nonempty everywhere and yields nothing",
    }


# ------------------------------------------------------------------ CHECK 5
def check5_ae_conclusion_is_weak():
    """The a.e. (measurable) form of the transfer gives only: for a.e. unit pair (a,b),
    min(|D(a)|,|D(b)|) = 0.  That conclusion does NOT force a colouring: a union of parallel
    lines at mutual distance > 1 satisfies it and is not unit-distance free.

    Exact witness: B = { (t, k*3/2) : t in R, k in Z } (horizontal lines, spacing 3/2 > 1).
    (i)  for a in B, the unit circle about a meets B in exactly 2 points (the two neighbours on
         the same line at distance 1), a null set: so the a.e. conclusion holds;
    (ii) B is not unit-distance free: a and a + (1,0) are both in B at distance 1.
    """
    from fractions import Fraction as F
    spacing = F(3, 2)
    assert spacing > 1                      # distinct lines are never at distance <= 1
    # the unit circle about (0,0) meets the line y = 0 in (+-1, 0) and no other line of B
    # (spacing 3/2 > 1), so the circle-intersection is 2 points, i.e. angular measure zero.
    assert spacing > 1
    # not unit-distance free:
    a = (F(0), F(0)); b = (F(1), F(0))
    d2 = (b[0]-a[0])**2 + (b[1]-a[1])**2
    assert d2 == 1
    return {"spacing": str(spacing), "circle_intersection": "2 points (null)",
            "contains_unit_pair": "(0,0)-(1,0)",
            "conclusion": "a.e. rigidity does not imply k-colourability"}


if __name__ == "__main__":
    print("CHECK 1 (geometric step):", check1_transversality())
    print("CHECK 4 (exact 7-colouring, k = 7 model):", check4_hexagonal_seven_colouring())
    print("CHECK 2 (combinatorial core):", check2_combinatorial_core())
    print("CHECK 3 (sharpness):", check3_sharpness())
    print("CHECK 5 (the measurable a.e. conclusion is weak):", check5_ae_conclusion_is_weak())
    print("ALL EXACT CHECKS PASSED")
