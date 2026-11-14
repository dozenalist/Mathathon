#!/usr/bin/env python3
"""
cone_arc.py -- exact verification for the CC60-arc condition on six cyclic interfaces.

Conventions (all exact, no floating point anywhere).
  * An angle is a Fraction x meaning the angle x*pi, taken modulo 2 (so the angle circle is
    T = R/2piZ identified with R/2Z).
  * cdist(x,y) in [0,1] is the circular distance on T, in units of pi.
  * Colour set Z/6; interfaces E_i = {i, i+1 mod 6}, i = 0..5.
  * W = 1/3 (i.e. pi/3).
  * CC60-arc(v):  for EVERY closed arc A of T of angular length W, |union{E_i : v_i in A}| <= 3.

Run:  python3 cone_arc.py      (exit status 0 iff every check passed)
"""
from fractions import Fraction as F
import itertools, random, sys

TWO = F(2)
W = F(1, 3)              # pi/3, in units of pi
K = 6
E = [frozenset({i, (i + 1) % K}) for i in range(K)]
# the 9 pairs of slots that are NOT cyclically consecutive: edges of K6 minus C6 = triangular prism
NONCONSEC = tuple((i, j) for i in range(K) for j in range(i + 1, K)
                  if (j - i) % K not in (1, K - 1))

FAILS = []
NCHECK = [0]


def check(cond, msg):
    NCHECK[0] += 1
    if not cond:
        FAILS.append(msg)
        print("   FAIL:", msg)


def red(x):
    return F(x) % TWO


def cdist(x, y):
    d = abs(red(x) - red(y))
    return d if d <= 1 else TWO - d


def in_arc(x, a, w):
    """closed arc [a, a+w] on T"""
    return red(x - a) <= w


def usz(S):
    u = set()
    for i in S:
        u |= E[i]
    return len(u)


def arc_violation(v, w=W):
    """Direct check of CC60-arc.  S(a) = {i : v_i in [a,a+w]} changes only at a = v_i - w
    (entry) and a = v_i (exit), so testing all critical points and one interior point of each
    complementary interval is exhaustive.  Returns (a, S) with |union E_i over S| > 3, or None."""
    crit = set()
    for x in v:
        crit.add(red(x - w))
        crit.add(red(x))
    cs = sorted(crit)
    tests = list(cs)
    for a, b in zip(cs, cs[1:]):
        tests.append((a + b) / 2)
    if len(cs) >= 2:
        tests.append(red((cs[-1] + cs[0] + TWO) / 2))
    for a in tests:
        S = tuple(i for i, x in enumerate(v) if in_arc(x, a, w))
        if usz(S) > 3:
            return (a, S)
    return None


def pair_violation(v, w=W):
    """The nine strict pairwise constraints: dist > w on every non-consecutive pair."""
    for (i, j) in NONCONSEC:
        if cdist(v[i], v[j]) <= w:
            return (i, j, cdist(v[i], v[j]))
    return None


def in_V(v, w=W):
    return pair_violation(v, w) is None


# ----------------------------------------------------------------------------- 1
def sec1():
    print("[1] Lemma 2 (combinatorial core): |union_{i in S} E_i| <= 3  <=>  S is contained in")
    print("    two cyclically consecutive slots.")
    for r in range(K + 1):
        for S in itertools.combinations(range(K), r):
            lhs = usz(S) <= 3
            rhs = any(set(S) <= {a % K, (a + 1) % K} for a in range(K))
            check(lhs == rhs, "lemma2 mismatch at S=%r (usz=%d rhs=%r)" % (S, usz(S), any(set(S) <= {a % K, (a + 1) % K} for a in range(K))))
    print("    all 64 subsets of the six slots agree;  usz table:",
          {S: usz(S) for S in [(0,), (0, 1), (0, 2), (0, 1, 2), (0, 2, 4)]})


# ----------------------------------------------------------------------------- 2
def sec2():
    print("[2] Theorem 3: CC60-arc  <=>  dist(v_i,v_j) > pi/3 on the nine prism pairs.")
    batteries = [
        [F(0), F(1, 6), F(1, 3), F(2, 3), F(1)],
        [F(0), F(1, 4), F(1, 3), F(1, 2), F(5, 6)],
        [F(0), F(1, 3), F(2, 3), F(4, 3), F(5, 3)],
    ]
    n = 0
    nviol = 0
    for vals in batteries:
        for v in itertools.product(vals, repeat=K):
            a = arc_violation(v)
            p = pair_violation(v)
            check((a is None) == (p is None), "grid mismatch v=%r arc=%r pair=%r" % (v, a, p))
            n += 1
            if a is not None:
                nviol += 1
    print("    exhaustive over %d rational 6-tuples on three grids: %d violate, all agree" % (n, nviol))
    rng = random.Random(20261114)
    for _ in range(4000):
        v = tuple(F(rng.randrange(0, 121), 60) for _ in range(K))   # multiples of pi/60
        a = arc_violation(v)
        p = pair_violation(v)
        check((a is None) == (p is None), "random mismatch v=%r arc=%r pair=%r" % (v, a, p))
    print("    4000 random points with coordinates in (1/60)Z on T agree")
    # targeted degenerate cases, with independently known verdicts
    cases = [
        ((F(0), F(1, 3), F(2, 3), F(1), F(4, 3), F(5, 3)), True,
         "alternating 6-grid, consecutive gaps exactly pi/3 (grid B)"),
        ((F(0), F(0), F(2, 3), F(2, 3), F(4, 3), F(4, 3)), True,
         "three double clusters 0,120,240 deg (grid A): equal directions in consecutive slots"),
        ((F(0), F(0), F(1, 3), F(1, 3), F(2, 3), F(2, 3)), False,
         "clusters at 0,60,120 deg: non-consecutive pair 0,2 at distance exactly pi/3"),
        ((F(0), F(1, 100), F(2, 100), F(3, 100), F(4, 100), F(5, 100)), False,
         "all six directions inside an arc of length pi/20"),
        ((F(0), F(1, 3), F(1, 3), F(1), F(4, 3), F(5, 3)), False,
         "closed endpoints: non-consecutive pair (0,2) at distance EXACTLY pi/3"),
        ((F(0), F(1), F(1, 2), F(3, 2), F(7, 5), F(0)), True,
         "antipodal pair v_0=0, v_1=pi (consecutive) and v_5=v_0 (also consecutive)"),
        ((F(0), F(0), F(0), F(1), F(4, 3), F(5, 3)), False,
         "three equal directions in slots 0,1,2 (pair 0,2 equal)"),
    ]
    for v, want, desc in cases:
        a = arc_violation(v)
        got = a is None
        check(got == want, "degenerate case %r: got %r want %r" % (desc, got, want))
        check(got == in_V(v), "degenerate case %r: arc/pair disagree" % (desc,))
        print("    %-70s -> %s   %s" % (desc, "SURVIVES" if got else "violated", "" if got else "witness arc a=%s*pi S=%s" % (a[0], a[1])))


# ----------------------------------------------------------------------------- 3
def sec3():
    print("[3] independent cross-check of the arc enumeration (brute force scan + membership recheck)")
    rng = random.Random(7)
    for _ in range(400):
        v = tuple(F(rng.randrange(0, 60), 30) for _ in range(K))
        a = arc_violation(v)
        brute = None
        for k in range(1440):
            s = F(k, 720)
            S = tuple(i for i, x in enumerate(v) if in_arc(x, s, W))
            if usz(S) > 3:
                brute = (s, S)
                break
        if a is not None:
            # the reported witness must really be a closed arc of length pi/3 with >=4 colours
            aa, SS = a
            check(all(in_arc(v[i], aa, W) for i in SS) and usz(SS) > 3,
                  "witness not valid for v=%r" % (v,))
            # and it must contain a non-consecutive pair
            check(any((j - i) % K not in (1, K - 1) for i in SS for j in SS if i != j),
                  "witness has no non-consecutive pair v=%r" % (v,))
        check((brute is not None) <= (a is not None), "brute force found a violation missed by arc_violation v=%r" % (v,))
    print("    400 random points: every witness re-validated, brute-force scan never finds more")


# ----------------------------------------------------------------------------- 4
def cone_filter_grid(q):
    """AC-CONE-SIX filter: for every adjacent direction pair {d,d+1}, |union{E_i: q_i in {d,d+1}}| <= 3."""
    for d in range(K):
        S = tuple(i for i in range(K) if (q[i] - d) % K in (0, 1))
        if usz(S) > 3:
            return False
    return True


def sec4():
    print("[4] Specialisation to the six-direction grid: recovery of AC-CONE-SIX")
    six = [(0, 0, 2, 2, 4, 4), (0, 0, 4, 4, 2, 2), (0, 1, 2, 3, 4, 5),
           (0, 2, 2, 4, 4, 0), (0, 4, 4, 2, 2, 0), (0, 5, 4, 3, 2, 1)]
    surv = []
    for q in itertools.product(range(K), repeat=K):
        v = tuple(F(x, 3) for x in q)      # v_i = q_i * pi/3
        f = cone_filter_grid(q)
        a = arc_violation(v) is None
        p = in_V(v)
        check(f == a == p, "grid mismatch q=%r filter=%r arc=%r pair=%r" % (q, f, a, p))
        if f:
            surv.append(q)
    check(len(surv) == 36, "full grid survivor count %d != 36" % len(surv))
    s0 = sorted(q for q in surv if q[0] == 0)
    check(s0 == sorted(six), "q0=0 survivor list mismatch: %r" % (s0,))
    print("    6^6 grid: %d survivors = 6 rotations x 6;  with q_0=0: %d, equal to the AC-CONE-SIX list:"
          % (len(surv), len(s0)))
    for q in s0:
        print("      ", q)


# ----------------------------------------------------------------------------- 5
def is_grid_rotation(v):
    """Is v a rotation of a 6-grid configuration satisfying the cone filter?  Equivalent to:
    all pairwise angular differences are multiples of pi/3 AND the resulting grid point survives."""
    d0 = [(v[i] - v[0]) * 3 for i in range(K)]
    for x in d0:
        if x.denominator != 1:
            return False
    q = tuple(int(red(x)) % K for x in d0)
    return cone_filter_grid(q)


def sec5():
    print("[5] Explicit non-grid survivor, exact certificate")
    vstar = tuple(F(m, 20) for m in (1, 5, 14, 18, 28, 32))
    print("    v* = (pi/20) * (1, 5, 14, 18, 28, 32)   [degrees: 9, 45, 126, 162, 252, 288]")
    mind = None
    for (i, j) in NONCONSEC:
        d = cdist(vstar[i], vstar[j])
        print("      dist(v%d, v%d) = %s*pi   (%s deg)" % (i, j, d, d * 180))
        if mind is None or d < mind:
            mind = d
    print("    minimal constrained distance = %s*pi = %s deg ; threshold 1/3*pi = 60 deg" % (mind, mind * 180))
    check(mind > W, "v* not in V")
    check(arc_violation(vstar) is None, "v* violates CC60-arc")
    check(not is_grid_rotation(vstar), "v* is a grid rotation")
    slack = mind - W
    rho = slack / 3
    print("    slack = %s*pi ; Lipschitz box radius rho = slack/3 = %s*pi = %s deg"
          % (slack, rho, rho * 180))
    # every point of the sup-norm box of radius rho around v* is in V: moving both endpoints of a
    # pair by at most rho changes its circular distance by at most 2*rho = 2*slack/3 < slack.
    # So all 9 constrained distances stay > mind - 2*rho = W + slack/3 > W.
    nbox = 0
    for sgn in itertools.product([1, -1], repeat=K):
        w = tuple(vstar[i] + sgn[i] * rho for i in range(K))
        check(in_V(w) and arc_violation(w) is None, "box corner %r not in V" % (sgn,))
        nbox += 1
    rng = random.Random(11)
    for _ in range(200):
        w = tuple(vstar[i] + F(rng.randrange(-1000, 1001), 1000) * rho for i in range(K))
        check(arc_violation(w) is None, "random interior box point not in V: %r" % (w,))
    print("    all %d corners + 200 random interior points of that box satisfy CC60-arc exactly" % nbox)


# ----------------------------------------------------------------------------- 6
def family(alpha, beta, gamma, t=F(0)):
    """v = t + (0, alpha, 2/3, 2/3+beta, 4/3, 4/3+gamma)   (units of pi)"""
    return (red(t), red(t + alpha), red(t + F(2, 3)), red(t + F(2, 3) + beta),
            red(t + F(4, 3)), red(t + F(4, 3) + gamma))


def sec6():
    print("[6] 4-parameter family of survivors containing grid A at (alpha,beta,gamma)=(0,0,0):")
    print("    v(alpha,beta,gamma;t) = t + (0, alpha, 2/3, 2/3+beta, 4/3, 4/3+gamma),  0<=alpha,beta,gamma<=1/4")
    vals = [F(0), F(1, 20), F(1, 10), F(3, 20), F(1, 4)]
    ts = [F(0), F(1, 7), F(1, 3), F(-5, 13)]
    n = 0
    for a in vals:
        for b in vals:
            for g in vals:
                for t in ts:
                    v = family(a, b, g, t)
                    check(arc_violation(v) is None, "family member outside V: %r" % (v,))
                    n += 1
    print("    %d exact family members verified (all satisfy every CC60-arc condition)" % n)
    # the two extremes
    print("    (0,0,0;0)  = %r  -> grid-A point;  equal directions only in consecutive slots" % (family(F(0), F(0), F(0)),))
    print("    (1/4,1/4,1/4;0) = %r  -> six distinct directions, non-grid" % (family(F(1, 4), F(1, 4), F(1, 4)),))
    check(not is_grid_rotation(family(F(1, 4), F(1, 4), F(1, 4))), "family member is a grid rotation")
    # the closed-form bound asserted in the writeup
    worst = None
    for a in vals:
        for b in vals:
            for g in vals:
                v = family(a, b, g)
                m = min(cdist(v[i], v[j]) for (i, j) in NONCONSEC)
                if worst is None or m < worst:
                    worst = m
    print("    minimal constrained distance over the whole parameter box = %s*pi (claimed bound 5/12*pi)" % worst)
    check(worst >= F(5, 12), "family bound 5/12 violated")


# ----------------------------------------------------------------------------- 7
def sec7():
    print("[7] Sharp threshold: CC60-arc with cone width theta is satisfiable iff theta < 2/3*pi.")
    # (a) theta < 2/3 : the three-cluster configuration with cluster diameter eps
    for eps in [F(1, 100), F(1, 10), F(1, 5), F(1, 3)]:
        theta = F(2, 3) - eps
        v = (F(0), eps, F(2, 3), F(2, 3) + eps, F(4, 3), F(4, 3) + eps)
        check(arc_violation(v, theta) is None, "cluster config fails for theta=%s" % theta)
        m = min(cdist(v[i], v[j]) for (i, j) in NONCONSEC)
        print("    theta = 2/3 - %-6s : clusters of diameter %-5s survive (min constrained dist %s)"
              % (eps, eps, m))
    # (b) theta >= 2/3 : impossible, already inside the triangle {0,2,4}
    for theta in [F(2, 3), F(7, 10), F(1)]:
        rng = random.Random(5)
        for _ in range(2000):
            w = tuple(F(rng.randrange(0, 241), 120) for _ in range(3))
            far = all(cdist(w[i], w[j]) > theta for i in range(3) for j in range(i + 1, 3))
            check(not far, "three pairwise-far points found for theta=%s: %r" % (theta, w))
        print("    theta = %-5s : no triple of directions is pairwise farther than theta (2000 tries)" % theta)
    print("    hence V_theta is empty for theta >= 2/3*pi: the 60 deg bound has a factor-2 margin.")


# ----------------------------------------------------------------------------- 8
def sec8():
    print("[8] Sharp equality at pi/3: Theorem 7 (maximal confinement forces the alternating grid)")
    vals = [F(-1, 3), F(-1, 6), F(0), F(1, 6), F(1, 3)]
    n1 = 0
    for s in itertools.product(vals, repeat=K):
        if not all(abs(s[i] + s[(i + 1) % K]) > W for i in range(K)):
            continue
        n1 += 1
        check(all(x > 0 for x in s) or all(x < 0 for x in s),
              "sign-constancy step fails at %r" % (s,))
    print("    step 1 (sign constancy) on the grid: %d confined step vectors, all of one sign" % n1)
    n2 = 0
    for s in itertools.product(vals, repeat=K):
        if not all(abs(s[i] + s[(i + 1) % K]) > W for i in range(K)):
            continue
        if sum(s) not in (F(0), F(2), F(-2)):     # closing/winding condition: sum s_i = 2m
            continue
        n2 += 1
        check(all(x == F(1, 3) for x in s) or all(x == F(-1, 3) for x in s),
              "closed confined step vector not the alternating grid: %r" % (s,))
    print("    step 2 (+ winding): %d closed step vectors, all equal to (+1/3,...,+1/3) or its negation" % n2)
    # the two alternating grids, and their rotations, are in V and maximally confined
    for t in [F(0), F(1, 7), F(1, 2)]:
        for sgn in (1, -1):
            v = tuple(red(t + sgn * i * F(1, 3)) for i in range(K))
            check(arc_violation(v) is None, "alternating grid not in V: %r" % (v,))
            check(all(cdist(v[i], v[(i + 1) % K]) <= W for i in range(K)), "grid not confined")
    print("    alternating grid and its reflection, at 3 rotations, are in V and maximally confined")
    rng = random.Random(3)
    wrong = 0
    for _ in range(20000):
        s = tuple(rng.choice(vals) for _ in range(K))
        if sum(s) not in (F(0), F(2), F(-2)):
            continue
        if not all(abs(s[i] + s[(i + 1) % K]) > W for i in range(K)):
            continue
        if not (all(x == F(1, 3) for x in s) or all(x == F(-1, 3) for x in s)):
            wrong += 1
    check(wrong == 0, "%d counterexamples to Theorem 7 step 2" % wrong)
    print("    20000 random closed step vectors: no counterexample")


def main():
    for f in (sec1, sec2, sec3, sec4, sec5, sec6, sec7, sec8):
        f()
        print()
    print("=" * 78)
    if FAILS:
        print("FAILED: %d of %d checks" % (len(FAILS), NCHECK[0]))
        for m in FAILS[:20]:
            print("  ", m)
        return 1
    print("ALL %d CHECKS PASSED" % NCHECK[0])
    return 0


if __name__ == "__main__":
    sys.exit(main())
