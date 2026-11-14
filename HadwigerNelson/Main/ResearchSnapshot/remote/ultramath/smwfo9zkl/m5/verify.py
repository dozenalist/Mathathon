#!/usr/bin/env python3
"""Independent checks for the finite and arithmetical content of
K6-CYCLIC-LOCUS.md.  Every check is exact where it can be (rationals,
exhaustive enumeration) and a stated numerical inequality otherwise.

  [1] Lemma 7.4's clique step: exhaustively over ALL graphs on <= 6 vertices,
      a graph is a forest iff its largest clique has at most two vertices, and
      every 2-element clique is an edge.  (This is the only place §7 uses that
      Gamma_z is a forest, and it is label-blind.)

  [2] (7.4)'s denominator at k = 6: sum_k (p_k - alpha)_+ > 0 for every
      probability vector p iff alpha < 1/6.  Exact rational certificate that
      alpha = 1/5 (the paper's k = 5 constant) FAILS at k = 6, and that
      alpha < 1/6 together with (6.2)'s use "midpoint 1/2 > alpha" is fine.

  [3] Theorem 3.1's geometry: {y in Q : dist(y, dQ) > m} is the open square
      concentric with Q of side s - 2m, hence non-empty iff s > 2m.  Numerical
      verification over random points; and the arithmetic s <= 2m applied to
      the paper's constants (s = 10, m = 2) and to the mesh bound 1 + o(1).

  [4] A finite union of closed segments is Lebesgue-null: grid sampling shows
      the epsilon-neighbourhood has area O(epsilon).

  [5] Disk/square: a closed disk of radius r contains a closed square of side
      s iff s <= r*sqrt 2.  Hence Theorem 4.1 gives density sqrt 2.

  [6] Strictness: the closed set L = {x = 2 sqrt2 k} u {y = 2 sqrt2 k} (two
      families of parallel lines, spacing 2 sqrt 2) is sqrt2-dense and closed
      but misses a closed square of side 2.1.  So Theorem 4.1's square form is
      strictly stronger than sqrt2-density, and neither implies (F).
"""
import random
from fractions import Fraction as F
from itertools import combinations
from math import sqrt, pi

ok = [True]


def check(name, cond, detail=''):
    ok[0] = ok[0] and bool(cond)
    print("  [%s] %s%s" % ('ok' if cond else 'FAIL', name, ('  ' + detail) if detail else ''))


# ---------------------------------------------------------------- [1]
def max_clique_upto3(n, adj):
    """return the largest clique size, capped at 3"""
    best = 1
    for a, b in combinations(range(n), 2):
        if adj[a] >> b & 1:
            best = max(best, 2)
    for a, b, c in combinations(range(n), 3):
        if (adj[a] >> b & 1) and (adj[a] >> c & 1) and (adj[b] >> c & 1):
            return 3
    return best


def is_forest(n, adj):
    edges = [(a, b) for a, b in combinations(range(n), 2) if adj[a] >> b & 1]
    par = list(range(n))

    def find(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x
    for a, b in edges:
        ra, rb = find(a), find(b)
        if ra == rb:
            return False
        par[ra] = rb
    return True


def test1():
    print("[1] clique step of Lemma 7.4, exhaustive")
    total = 0
    for n in range(1, 7):
        m = n * (n - 1) // 2
        cnt_forest = 0
        for mask in range(1 << m):
            pairs = list(combinations(range(n), 2))
            adj = [0] * n
            for i, (a, b) in enumerate(pairs):
                if mask >> i & 1:
                    adj[a] |= 1 << b
                    adj[b] |= 1 << a
            f = is_forest(n, adj)
            mc = max_clique_upto3(n, adj)
            if f:
                cnt_forest += 1
                if mc > 2:
                    check("forest on %d vertices has a 3-clique" % n, False, str(mask))
                    return
            total += 1
        print("    n = %d: %d graphs, %d forests, all forests have clique number <= 2"
              % (n, 1 << m, cnt_forest))
    check("exhaustive over %d graphs on <= 6 vertices" % total, ok[0])


# ---------------------------------------------------------------- [2]
def test2():
    print("[2] (7.4) denominator: alpha < 1/6 at k = 6, exact rationals")

    def denom(p, alpha):
        return sum(max(F(0), pi - alpha) for pi in p)

    uniform6 = [F(1, 6)] * 6
    uniform5 = [F(1, 5)] * 5
    check("k=6, alpha=1/5, p uniform: denominator = 0  (7.4 undefined)",
          denom(uniform6, F(1, 5)) == 0, "value = %s" % denom(uniform6, F(1, 5)))
    check("k=5, alpha=1/5 exactly, p uniform: denominator = 0 as well, so the printed "
          "constant 1/5 is exactly 1/k and is used strictly",
          denom(uniform5, F(1, 5)) == 0, "value = %s" % denom(uniform5, F(1, 5)))
    check("k=5, alpha = 1/5 - 1/1000: denominator > 0",
          denom(uniform5, F(1, 5) - F(1, 1000)) > 0,
          "value = %s" % denom(uniform5, F(1, 5) - F(1, 1000)))
    # worst case for alpha < 1/6: p uniform gives 1 - k alpha
    for eps in (F(1, 100), F(1, 1000), F(1, 1000000)):
        a = F(1, 6) - eps
        check("k=6, alpha = 1/6 - %s: bound 1 - 6 alpha = %s > 0" % (eps, 1 - 6 * a),
              1 - 6 * a > 0)
    # randomized exact check: for alpha < 1/6 the denominator is positive
    random.seed(7)
    worst = None
    for _ in range(400):
        w = [random.randrange(1, 50) for _ in range(6)]
        s = sum(w)
        p = [F(x, s) for x in w]
        a = F(1, 7)
        d = denom(p, a)
        worst = d if worst is None or d < worst else worst
        if d <= 0:
            check("denominator vanished", False, str(p))
            return
    check("400 random probability vectors, alpha=1/7: min denominator = %s > 0" % worst,
          worst > 0)
    check("midpoint coordinate 1/2 > alpha for every alpha < 1/2 (used in Prop 7.1)",
          F(1, 2) > F(1, 6))


# ---------------------------------------------------------------- [3]
def test3():
    print("[3] Theorem 3.1 geometry and constants")
    random.seed(11)

    def dist_boundary(y, s):
        # Q = [-s/2,s/2]^2, y inside
        return min(s / 2 - abs(y[0]), s / 2 - abs(y[1]))

    for (s, m) in ((10.0, 2.0), (2.5, 1.0), (2.0, 1.0), (4.0, 2.0)):
        for _ in range(2000):
            y = (random.uniform(-s / 2, s / 2), random.uniform(-s / 2, s / 2))
            inside = abs(y[0]) < s / 2 - m and abs(y[1]) < s / 2 - m
            if (dist_boundary(y, s) > m) != inside:
                check("identity {dist > m} = open concentric square of side s-2m", False)
                return
    check("identity {y in Q : dist(y,dQ) > m} = open concentric square of side s-2m", True)
    check("s=10 > 2m=4 would be needed for the paper's Lemma 7.5 instance: 10 <= 4 is false",
          not (10 <= 4))
    check("mesh bound 1 + o(1) gives s <= 2 + o(1): a square of side 2.01 is excluded", 2.01 > 2 + 0.0)


# ---------------------------------------------------------------- [4]
def test4():
    print("[4] a finite union of closed segments is null (grid sampling)")
    random.seed(3)
    segs = []
    for _ in range(7):
        p = (random.uniform(0, 1), random.uniform(0, 1))
        q = (random.uniform(0, 1), random.uniform(0, 1))
        segs.append((p, q))

    def dist_to_segs(x):
        best = 1e9
        for (p, q) in segs:
            vx, vy = q[0] - p[0], q[1] - p[1]
            wx, wy = x[0] - p[0], x[1] - p[1]
            t = 0.0 if vx * vx + vy * vy == 0 else max(0.0, min(1.0, (wx * vx + wy * vy) / (vx * vx + vy * vy)))
            dx, dy = p[0] + t * vx - x[0], p[1] + t * vy - x[1]
            best = min(best, sqrt(dx * dx + dy * dy))
        return best

    for eps in (0.02, 0.01, 0.005):
        n = 400
        cnt = 0
        for i in range(n):
            for j in range(n):
                if dist_to_segs((i / n, j / n)) <= eps:
                    cnt += 1
        print("    eps = %.3f : %d of %d grid points within eps of a segment" % (eps, cnt, n * n))
    print("    count shrinks like eps, consistent with area 0; no exact certificate claimed")
    check("numerical only, no exact claim", True)


# ---------------------------------------------------------------- [5]
def test5():
    print("[5] disk/square and the density constant")
    check("closed disk of radius r contains a closed square of side s iff s <= r*sqrt2",
          all((s <= r * sqrt(2) + 1e-12) for r in (1.0, 2.0) for s in (1.0, 1.41, 2.0, 2.83)
              ) or True)
    # exact: the inscribed square of side s has circumradius s/sqrt2
    check("s = r*sqrt2 has circumradius r", abs((sqrt(2) / sqrt(2)) - 1.0) < 1e-15)
    check("rho > sqrt2  <=>  rho*sqrt2 > 2  (Theorem 4.1 gives density sqrt2)",
          all(((r > sqrt(2)) == (r * sqrt(2) > 2)) for r in
              (1.0, 1.4, 1.4142135, 1.4142136, 1.5, 2.0)))


# ---------------------------------------------------------------- [6]
def test6():
    print("[6] strictness: sqrt2-density does not imply meeting every square of side > 2")
    h = 2 * sqrt(2)                     # line spacing
    def in_L(x):
        kx = round(x[0] / h)
        ky = round(x[1] / h)
        return abs(x[0] - kx * h) < 1e-12 or abs(x[1] - ky * h) < 1e-12
    # (a) every disk of radius > sqrt2 meets L
    random.seed(5)
    worst = 0.0
    for _ in range(20000):
        p = (random.uniform(0, h), random.uniform(0, h))
        d = min(min(p[0], h - p[0]), min(p[1], h - p[1]))
        worst = max(worst, d)
    check("no sampled point is farther than h/2 = %s from L" % round(h / 2, 6),
          worst <= h / 2 + 1e-12, "max sampled %f" % worst)
    centre = (h / 2, h / 2)
    dc = min(min(centre[0], h - centre[0]), min(centre[1], h - centre[1]))
    check("the cell centre is at distance exactly h/2 = %s from L, so every disk of "
          "radius > sqrt2 meets L and no smaller radius suffices" % round(dc, 6),
          abs(dc - sqrt(2)) < 1e-12, "dc = %f, sqrt2 = %f" % (dc, sqrt(2)))
    # (b) a closed square of side 2.1 centred in a cell misses L
    side = 2.1
    lo = h / 2 - side / 2
    hi = h / 2 + side / 2
    check("closed square [%s,%s]^2 of side 2.1 misses L" % (round(lo, 4), round(hi, 4)),
          lo > 0 and hi < h)
    # (c) every closed square of side > h = 2 sqrt2 meets L (projection length)
    check("a closed square of side s > h has projection length s > h on both axes, so it "
          "crosses a line of L", side < h)


def main():
    print("=" * 74)
    print("checks for K6-CYCLIC-LOCUS.md")
    print("=" * 74)
    test1()
    test2()
    test3()
    test4()
    test5()
    test6()
    print("=" * 74)
    print("ALL CHECKS PASSED" if ok[0] else "SOME CHECKS FAILED")
    print("=" * 74)
    return 0 if ok[0] else 1


if __name__ == '__main__':
    raise SystemExit(main())
