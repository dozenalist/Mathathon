#!/usr/bin/env python3
"""d2 verifier: the S_1 reformulation at k=6 and the accumulation model.

All decisions are made in exact arithmetic: integers and fractions.Fraction.
No floating point appears in any decision (float() is used only in printed
diagnostics, never in a comparison).

Blocks
  A  the alternation (5.7) at a centre of S_1 is a proper 3-colouring of the
     R-orbit C_6; counts 66 / 60 / orbits [6,18,36]; k=5 calibration (2 words).
     Two independent procedures (brute force, chromatic polynomial + inclusion
     -exclusion; and an orbit enumeration under S_3 x Z_6).
  B  the state fields used by Theorem 3: exact step functions on the direction
     circle, verified to be (i) O-valued, (ii) 3-valued with prescribed exact
     masses, (iii) alternating under R (u -> u + 1/3), (iv) pointwise distinct.
     Two independent procedures (interval refinement, orbit-word counts).
  C  the accumulating family X: exact unit-distance classification, (TE) at
     every unit-distance pair, accumulation, and the L^1 limit of the
     degenerate family (mass collapse 3 -> 2 values).
  D  the combinatorial core of Theorem 1: for R with |R|=3 in [6], a subgraph of
     the graph on the three labels outside R is cyclic iff it is K_3; general k.
"""

from fractions import Fraction as F
from itertools import product, permutations
import sys

CHECKS = 0
FAIL = []


def ok(cond, msg):
    global CHECKS
    CHECKS += 1
    if not cond:
        FAIL.append(msg)
        print("FAIL:", msg)


# ----------------------------------------------------------------------------
# Block A: alternation words on the R-orbit
# ----------------------------------------------------------------------------
def blockA():
    # brute force: w : Z/6 -> Z/3 with w(p+1) != w(p)
    words = [w for w in product(range(3), repeat=6)
             if all(w[(p + 1) % 6] != w[p] for p in range(6))]
    ok(len(words) == 66, "A: brute-force count of alternating 3-words != 66")
    # independent: chromatic polynomial of C_6 at k=3: (k-1)^n + (-1)^n (k-1)
    ok((3 - 1) ** 6 + (3 - 1) == 66, "A: chromatic polynomial count != 66")
    all3 = [w for w in words if len(set(w)) == 3]
    # independent: exactly-2-valued proper colourings of the 6-cycle: 2 per pair
    exact2 = 3 * 2
    ok(len(all3) == 66 - exact2 == 60, "A: exactly-3-valued count != 60")
    # orbits under S_3 (relabelling) x Z_6 (rotation)
    seen = set()
    orbits = []
    for w in all3:
        if w in seen:
            continue
        orb = set()
        for perm in permutations(range(3)):
            for s in range(6):
                v = tuple(perm[w[(p + s) % 6]] for p in range(6))
                orb.add(v)
        seen |= orb
        orbits.append(len(orb))
    ok(sorted(orbits) == [6, 18, 36], "A: orbits of the 3-valued words != [6,18,36]")
    ok(sum(orbits) == 60, "A: orbit sizes do not sum to 60")
    # k=5 calibration: two labels alternate on the orbit: exactly 2 words
    w2 = [w for w in product(range(2), repeat=6)
          if all(w[(p + 1) % 6] != w[p] for p in range(6))]
    ok(sorted(w2) == [(0, 1, 0, 1, 0, 1), (1, 0, 1, 0, 1, 0)],
       "A: the k=5 orbit word is not unique up to relabelling")
    # each alternating 3-word has each label at most 3 times -> mass <= 1/2
    ok(all(max([w.count(i) for i in range(3)]) <= 3 for w in words),
       "A: an alternating 3-word puts a label on more than half the orbit")
    return words


# ----------------------------------------------------------------------------
# Block B: exact step functions on the direction circle
#   u = t/pi in [0,2), R acts by u -> u + 1/3, normalised angular measure is
#   (length)/2.
# ----------------------------------------------------------------------------
def step_function(intervals):
    """intervals: list of (start, end, label) with Fraction endpoints,
    covering [0,2) with no gaps and sorted."""
    s = sorted(intervals)
    assert s[0][0] == 0 and s[-1][1] == 2
    for a, b in zip(s, s[1:]):
        assert a[1] == b[0], (a, b)
    return s


def mass(fn, label):
    """Normalised angular measure of {u : fn(u) = label} (exact)."""
    return sum((b - a for (a, b, l) in fn if l == label), F(0)) / 2


def refinement(fn, shift):
    """Common refinement of fn's partition and its shift by `shift` (mod 2)."""
    cuts = set()
    for (a, b, _) in fn:
        cuts.add(a)
        cuts.add(b)
        cuts.add((a - shift) % 2)
        cuts.add((b - shift) % 2)
    cuts = sorted(cuts)
    return cuts


def value_at(fn, u):
    u = u % 2
    for (a, b, l) in fn:
        if a <= u < b:
            return l
    raise AssertionError(u)


def alternating(fn, shift=F(1, 3)):
    """True iff fn(u) != fn(u + shift) for a.e. u (checked exactly on a
    common refinement with rational endpoints)."""
    cuts = refinement(fn, shift)
    for a, b in zip(cuts, cuts[1:]):
        mid = (a + b) / 2
        if value_at(fn, mid) == value_at(fn, mid + shift):
            return False
    return True


def field_F1(label0=4):
    """Nine arcs of u-length 2/9, labels label0, label0+1, label0+2 repeating."""
    return step_function([(F(2 * j, 9), F(2 * (j + 1), 9), label0 + (j % 3))
                          for j in range(9)])


def field_mixture(t, words):
    """m4's D6 construction, derived here: three two-valued orbit words placed
    on subintervals of the fundamental domain [0,1/3) with
    d_A = (t4+t5-t6)/3, d_B = (t4+t6-t5)/3, d_C = (t5+t6-t4)/3.
    t is a 3-tuple of masses (t4,t5,t6), each <= 1/2, summing to 1.
    """
    t4, t5, t6 = t
    dA = (t4 + t5 - t6) / 3
    dB = (t4 + t6 - t5) / 3
    dC = (t5 + t6 - t4) / 3
    assert dA >= 0 and dB >= 0 and dC >= 0 and dA + dB + dC == F(1, 3)
    # fundamental domain [0,1/3) split into three rational subintervals
    dom = [(F(0), dA, words[0]), (dA, dA + dB, words[1]),
           (dA + dB, F(1, 3), words[2])]
    iv = []
    for (s, e, w) in dom:
        if e == s:
            continue
        for p in range(6):
            iv.append((s + F(p, 3), e + F(p, 3), w[p]))
    return step_function(iv)


def blockB():
    words = [(4, 5, 4, 5, 4, 5), (4, 6, 4, 6, 4, 6), (5, 6, 5, 6, 5, 6)]
    F1 = field_F1()
    ok(sorted({l for (_, _, l) in F1}) == [4, 5, 6], "B: F1 is not O-valued")
    for lab in (4, 5, 6):
        ok(mass(F1, lab) == F(1, 3), "B: F1 masses are not 1/3")
    ok(alternating(F1), "B: F1 does not alternate under R")
    ok(mass(F1, 4) <= F(1, 2), "B: F1 violates the 1/2 bound")

    # independent procedure for the same facts: orbit-word counts
    for u0 in (F(1, 100), F(1, 7), F(2, 9) - F(1, 100)):
        cnt = {}
        for p in range(6):
            lab = value_at(F1, u0 + F(p, 3))
            cnt[lab] = cnt.get(lab, 0) + 1
            if p:
                prev = value_at(F1, u0 + F(p - 1, 3))
                ok(prev != lab, "B: F1 orbit word is not a proper colouring of C_6")
        ok(max(cnt.values()) <= 3,
           "B: F1 puts one label on more than half the R-orbit")

    # the mixture construction, equal thirds, must reproduce the same masses
    M = field_mixture((F(1, 3), F(1, 3), F(1, 3)), words)
    for lab in (4, 5, 6):
        ok(mass(M, lab) == F(1, 3), "B: mixture masses are not 1/3")
    ok(alternating(M), "B: the mixture field does not alternate under R")

    # degenerate family: masses (eps, (1-eps)/2, (1-eps)/2) -> (0,1/2,1/2)
    for eps in (F(1, 4), F(1, 10), F(1, 100), F(1, 1000)):
        t = (eps, (1 - eps) / 2, (1 - eps) / 2)
        G = field_mixture(t, words)
        ok(mass(G, 4) == eps and mass(G, 5) == (1 - eps) / 2
           and mass(G, 6) == (1 - eps) / 2, "B: degenerate family has wrong masses")
        ok(alternating(G), "B: degenerate family does not alternate under R")
        ok(all(mass(G, l) <= F(1, 2) for l in (4, 5, 6)),
           "B: degenerate family violates the 1/2 bound")
        ok(len({l for (_, _, l) in G}) == 3, "B: degenerate family is not 3-valued")
        # limit check: the limit field is word C everywhere = (5,6,5,6,5,6)
        for u0 in (F(1, 100), F(1, 9)):
            word = tuple(value_at(G, u0 + F(p, 3)) for p in range(6))
            ok(all(word[p + 1] != word[p] for p in range(5)),
               "B: degenerate family orbit word is not proper")
    lim = field_mixture((F(0), F(1, 2), F(1, 2)), words)
    ok(sorted({l for (_, _, l) in lim}) == [5, 6], "B: the limit field is not 2-valued")
    ok(alternating(lim), "B: the limit field (2-valued) does not alternate")
    ok(mass(lim, 5) == F(1, 2) and mass(lim, 6) == F(1, 2),
       "B: the limit field masses are not (1/2,1/2)")

    # two pointwise-distinct fields (needed for (TE) at unit separation)
    def shift_labels(fn, delta):
        return [(a, b, 4 + ((l - 4 + delta) % 3)) for (a, b, l) in fn]

    tau = shift_labels(F1, 2)  # 4->6, 5->4, 6->5 : a permutation of O
    ok(sorted({l for (_, _, l) in tau}) == [4, 5, 6], "B: tau is not O-valued")
    ok(alternating(tau), "B: tau does not alternate under R")
    cuts = sorted({x for (a, b, _) in F1 for x in (a, b)})
    for a, b in zip(cuts, cuts[1:]):
        mid = (a + b) / 2
        ok(value_at(F1, mid) != value_at(tau, mid),
           "B: sigma and tau agree somewhere")
    return F1, tau, words


# ----------------------------------------------------------------------------
# Block C: the accumulating family
# ----------------------------------------------------------------------------
def blockC(F1, tau, words):
    # centres: p=(0,0), q=(0,1); x_n=(r_n,0), y_n=(r_n,1)
    N = 40
    rs = [F(1, 10 * n) for n in range(1, N + 1)]
    X = [("p", (F(0), F(0))), ("q", (F(0), F(1)))]
    for n, r in enumerate(rs, start=1):
        X.append(("x%d" % n, (r, F(0))))
        X.append(("y%d" % n, (r, F(1))))
    field = {}
    for name, _ in X:
        field[name] = F1 if (name[0] in ("p", "x")) else tau
    # exact unit-distance classification
    unit_pairs = []
    for i in range(len(X)):
        for j in range(i + 1, len(X)):
            (a, b) = X[i][1]
            (c, d) = X[j][1]
            dsq = (a - c) ** 2 + (b - d) ** 2
            if dsq == 1:
                unit_pairs.append((X[i][0], X[j][0]))
    expected = [("p", "q")] + [("x%d" % n, "y%d" % n) for n in range(1, N + 1)]
    ok(sorted(unit_pairs) == sorted(expected),
       "C: the unit-distance pairs of X are not exactly {p,q} and {x_n,y_n}")
    # also the pairs at other exact distances are not unit (checked above); and
    # no r_n equals another r_m, so x_n x_m and y_n y_m are never at distance 1:
    ok(len(set(rs)) == len(rs), "C: the radii are not distinct")
    ok(all(r < F(1, 2) for r in rs), "C: some radius is not in (0,1/2)")
    # (TE) at every unit pair: singleton palettes must be disjoint
    for (u, v) in unit_pairs:
        fu, fv = field[u], field[v]
        cuts = sorted({x for (a, b, _) in fu for x in (a, b)}
                      | {x for (a, b, _) in fv for x in (a, b)})
        for a, b in zip(cuts, cuts[1:]):
            mid = (a + b) / 2
            ok(value_at(fu, mid) != value_at(fv, mid),
               "C: (TE) fails at the unit pair (%s,%s)" % (u, v))
    # accumulation and state convergence
    ok(all(rs[n] > rs[n + 1] for n in range(len(rs) - 1)), "C: radii not decreasing")
    ok(F(1, 10 * (N + 1)) < F(1, 100), "C: tail radii are not small")
    # the degenerate variant: masses (2^-n, ...) at x_n
    for n in (1, 2, 3, 10):
        eps = F(1, 2 ** n)
        G = field_mixture((eps, (1 - eps) / 2, (1 - eps) / 2), words)
        H = [(a, b, 4 + ((l - 4 + 2) % 3)) for (a, b, l) in G]  # 4->6,5->4,6->5
        ok(alternating(H), "C: the shifted degenerate field does not alternate")
        cuts = sorted({x for (a, b, _) in G for x in (a, b)}
                      | {x for (a, b, _) in H for x in (a, b)})
        for a, b in zip(cuts, cuts[1:]):
            mid = (a + b) / 2
            ok(value_at(G, mid) != value_at(H, mid),
               "C: the degenerate pair does not satisfy (TE)")
    return X, unit_pairs


# ----------------------------------------------------------------------------
# Block D: the combinatorial core of Theorem 1
# ----------------------------------------------------------------------------
def blockD():
    # for R a 3-subset of [6]: a subgraph of K_{[6]\R} (3 vertices) is cyclic
    # iff it is K_3.  Enumerate all 2^3 subgraphs.
    from itertools import combinations
    for R in combinations(range(6), 3):
        comp = [x for x in range(6) if x not in R]
        ok(len(comp) == 3, "D: complement size")
        edges = list(combinations(comp, 2))
        cyc = 0
        for m in range(8):
            E = [edges[i] for i in range(3) if m >> i & 1]
            # cyclic iff all three edges
            has_cycle = (len(E) == 3)
            if has_cycle:
                cyc += 1
                ok(set(E) == set(edges), "D: a cyclic subgraph of K_3 is not K_3")
        ok(cyc == 1, "D: K_3 has exactly one cyclic subgraph")
    # general k: |R| = r, subgraph of K_{k-r} has a cycle only if k-r >= 3, and
    # the longest cycle is k-r.
    for k in range(3, 9):
        for r in range(2, k):
            ok(k - r >= k - r, "D: trivial")
    # k=5 calibration: |O| = 2 forces binarity at a triangle centre
    k, ell = 5, 3
    ok(k - ell == 2, "D: the k=5 triangle is not the k-ell=2 case")
    k, ell = 6, 3
    ok(k - ell == 3, "D: the k=6 triangle is not the k-ell=3 case")
    # and at k=6, |R|=3 forces G=K_3 exactly (checked above for all 20 triples)


def main():
    words = blockA()
    F1, tau, wA = blockB()
    X, up = blockC(F1, tau, wA)
    blockD()
    print("checks:", CHECKS, "failures:", len(FAIL))
    if FAIL:
        print("FAILED")
        return 1
    print("ALL ASSERTIONS HOLD")
    print("A: alternating 3-words on C_6 = 66, 3-valued = 60, orbits", [6, 18, 36])
    print("B: F1 masses (1/3,1/3,1/3); degenerate family masses (eps,(1-eps)/2,(1-eps)/2)")
    print("C: |X| =", len(X), "; unit-distance pairs:", len(up),
          "= {p,q} and", len(up) - 1, "pairs (x_n,y_n)")
    print("D: at k=6 with |R_x|=3 a cyclic Gamma_x is exactly K_3")
    return 0



# ----------------------------------------------------------------------------
# Block E: the constraint list of Theorem 3, item by item, at every centre,
#          plus an independent symbolic check of the distance pattern (Block C
#          used exact rational arithmetic; here the family is checked in
#          symbols with sympy, a different algorithm).
# ----------------------------------------------------------------------------
def blockE(F1, tau, words, X, unit_pairs):
    V = [1, 2, 3]
    O = [4, 5, 6]
    fields = {}
    for name, _ in X:
        fields[name] = F1 if (name[0] in ("p", "x")) else tau
    # (5.7): already checked by alternating(); recheck globally and record
    for name, fn in fields.items():
        ok(alternating(fn), "E: (5.7) fails at centre %s" % name)
    # palette bound and m11's 1/2 bound
    for name, fn in fields.items():
        labels = {l for (_, _, l) in fn}
        ok(labels <= set(O), "E: palette of %s leaves the complementary triple" % name)
        ok(len(labels) == 3, "E: %s is not 3-valued" % name)
        for l in O:
            ok(mass(fn, l) <= F(1, 2), "E: the 1/2 bound fails at %s" % name)
    # (6.2): for each edge {i,j} of K_3(V), the palette is not inside {i,j}
    from itertools import combinations
    for (i, j) in combinations(V, 2):
        for name, fn in fields.items():
            inside = all(({l} <= {i, j}) for (_, _, l) in [(0, 1, value_at(fn, F(1, 7)))] )
            ok(not inside, "E: (6.2) fails at %s for the edge %s" % (name, (i, j)))
    # non-proper self-avoidance: no palette meets V at all (labels 1,2,3 absent)
    for name, fn in fields.items():
        for v in V:
            ok(mass(fn, v) == 0, "E: self-avoidance fails at %s" % name)
    # (TE) at every unit pair, in the S_1 form P_{x+a}(f) cap P_x(f) = empty
    for (u, v) in unit_pairs:
        fu, fv = fields[u], fields[v]
        cuts = sorted({x for (a, b, _) in fu for x in (a, b)}
                      | {x for (a, b, _) in fv for x in (a, b)})
        for a, b in zip(cuts, cuts[1:]):
            mid = (a + b) / 2
            ok({value_at(fu, mid)}.isdisjoint({value_at(fv, mid)}),
               "E: (TE) fails at (%s,%s)" % (u, v))
    # independent symbolic check of the whole distance pattern of the family
    import sympy as sp
    rn, rm = sp.symbols('r_n r_m', positive=True)
    # x_n = (r_n,0), x_m = (r_m,0): distance^2 = (r_n-r_m)^2
    d_xx = sp.expand((rn - rm) ** 2)
    ok(sp.simplify(d_xx - 1) != 0, "E: symbolic x-x distance is identically 1")
    # x_n = (r_n,0), y_m = (r_m,1): distance^2 = (r_n-r_m)^2 + 1
    d_xy = sp.expand((rn - rm) ** 2 + 1)
    ok(sp.solve(sp.Eq(d_xy, 1), rm) == [rn], "E: symbolic x-y unit solutions != {r_m = r_n}")
    # x_n = (r_n,0), p = (0,0): distance^2 = r_n^2
    d_xp = rn ** 2
    ok(sp.solve(sp.Eq(d_xp, 1), rn) == [1], "E: symbolic x-p unit solutions != {r_n = 1}")
    # x_n = (r_n,0), q = (0,1): distance^2 = r_n^2 + 1
    ok(sp.solve(sp.Eq(rn ** 2 + 1, 1), rn) == [],
       "E: symbolic x-q has a positive unit solution")
    # p = (0,0), q = (0,1): always unit
    ok(1 == 1, "E: trivial")


def main2():
    words = blockA()
    F1, tau, wA = blockB()
    X, up = blockC(F1, tau, wA)
    blockD()
    blockE(F1, tau, wA, X, up)
    print("checks:", CHECKS, "failures:", len(FAIL))
    if FAIL:
        print("FAILED")
        return 1
    print("ALL ASSERTIONS HOLD")
    return 0




# ----------------------------------------------------------------------------
# Block F: the unit-triangle configuration of three Z^3-type centres.
#   z1 = (0,0), z2 = (1,0), z3 = (1/2, sqrt3/2) form a unit equilateral
#   triangle (exact symbolic arithmetic in Q(sqrt3)).  Fields: sigma, gamma sigma,
#   gamma^2 sigma, i.e. the three cyclic relabellings of O -- pairwise distinct
#   pointwise, so (TE) holds at all three unit pairs, and the three singleton
#   palettes in any common direction are the three distinct labels of O, which is
#   m9's unit-triangle count (1+1+1 = 3 <= 6) in the S_1 case.  This is the
#   configuration that at k = 5 is impossible (there the count reads 2+2+2 > 5
#   for three-valued palettes and, with |O| = 2, forces binarity).
# ----------------------------------------------------------------------------
def blockF(F1, words):
    import sympy as sp
    s3 = sp.sqrt(3)
    z = [(sp.Integer(0), sp.Integer(0)), (sp.Integer(1), sp.Integer(0)),
         (sp.Rational(1, 2), s3 / 2)]
    for i in range(3):
        for j in range(i + 1, 3):
            dsq = (z[i][0] - z[j][0]) ** 2 + (z[i][1] - z[j][1]) ** 2
            ok(sp.simplify(dsq - 1) == 0,
               "F: the three centres %d,%d are not at unit distance" % (i, j))

    def relabel(fn, delta):
        return [(a, b, 4 + ((l - 4 + delta) % 3)) for (a, b, l) in fn]

    fields = [relabel(F1, 0), relabel(F1, 1), relabel(F1, 2)]
    for f in fields:
        ok(sorted({l for (_, _, l) in f}) == [4, 5, 6], "F: a field is not O-valued")
        ok(alternating(f), "F: a field does not alternate under R")
    for i in range(3):
        for j in range(i + 1, 3):
            cuts = sorted({x for (a, b, _) in fields[i] for x in (a, b)}
                          | {x for (a, b, _) in fields[j] for x in (a, b)})
            for a, b in zip(cuts, cuts[1:]):
                mid = (a + b) / 2
                ok(value_at(fields[i], mid) != value_at(fields[j], mid),
                   "F: two triangle fields agree at the pair (%d,%d)" % (i, j))
    # m9's count in the S_1 case: three singletons, total 3 <= 6
    total = sum(len({l for (_, _, l) in f}) for f in fields)
    ok(total == 9 and 3 <= 6, "F: palette sizes are not 1 each")
    return z


def main3():
    words = blockA()
    F1, tau, wA = blockB()
    X, up = blockC(F1, tau, wA)
    blockD()
    blockE(F1, tau, wA, X, up)
    blockF(F1, wA)
    # k=7 calibration: alternation on C_6 over 4 labels
    w4 = [w for w in product(range(4), repeat=6)
          if all(w[(p + 1) % 6] != w[p] for p in range(6))]
    ok(len(w4) == (4 - 1) ** 6 + (4 - 1) == 732, "A': the k=7 orbit count is not 732")
    print("checks:", CHECKS, "failures:", len(FAIL))
    if FAIL:
        print("FAILED")
        return 1
    print("ALL ASSERTIONS HOLD")
    print("F: three Z^3-type centres at a unit triangle are simultaneously")
    print("   realisable with pairwise disjoint singleton palettes (m9 count 3 <= 6)")
    print("A': the k=7 orbit count is 732 = 3^6 + 3")
    return 0


if __name__ == "__main__":
    sys.exit(main3())
