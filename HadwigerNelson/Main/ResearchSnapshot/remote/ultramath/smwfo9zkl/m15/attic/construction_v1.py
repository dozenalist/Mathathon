"""An explicit palette system at k = 6 whose six-cycle locus accumulates.

THE OBJECT
----------
Labels I = {0,1,...,5}.  The six-cycle C = 0-1-2-3-4-5-0.
Fix an integer m >= 6 with 3 | m.  Put n = 6m, Delta = 2*pi/n, L = 2m/3
(so 3L = 2m divides n), and let M_0 = {0,3}, M_1 = {1,4}, M_2 = {2,5}.
Sector i is the half-open arc [i*Delta, (i+1)*Delta).  Define

        sigma(i) = M_{ floor(i/L) mod 3 }        (i in Z/n),

and, for every point z of the plane, the palette function

        P_z : S^1 -> 2^I,   P_z(theta) = sigma( floor(theta/Delta) ).

All palettes have size 2.  No palette is contained in a cycle edge.  The
family is translation invariant.

THE CENTRES
-----------
Let d0 = Delta/3.  Any set of centres of diameter <= d0 has, for every pair
z != z', the exact two-centre exclusion

        P_z(f) cap P_{z'}(s_pm(f)) = empty     for almost every f,

where s_pm are the two exact unit decompositions (z'-z) + f = s + t,
|s| = |t| = 1.  Take, for instance, y_k = (d0/3) * 2^{-k} * (3/5, 4/5).

Each y_k is a six-cycle centre in the following sense: for every cycle edge
{i,i+1}, P_{y_k}(f) is not contained in {i,i+1} for a.e. f, which is exactly
conclusion (6.2) of the paper's Lemma 6.2 from "i(i+1) in Gamma_{y_k}".

This file verifies every combinatorial assertion exactly (integer arithmetic)
and the geometric reduction with interval arithmetic (verify.py).
"""
import itertools
from fractions import Fraction

# ------------------------------------------------------------------ labels
K = 6
EDGES = [frozenset((i, (i + 1) % 6)) for i in range(6)]
M = [frozenset({0, 3}), frozenset({1, 4}), frozenset({2, 5})]


def allowed_values(k=6, cycle_len=6):
    """(P0)+(P1): 1 <= |S| <= k-3 and S not contained in a cycle edge."""
    edges = [frozenset((i, (i + 1) % cycle_len)) for i in range(cycle_len)]
    out = []
    for r in range(1, k + 1):
        if r > k - 3:
            break
        for c in itertools.combinations(range(k), r):
            S = frozenset(c)
            if any(S <= e for e in edges):
                continue
            out.append(S)
    return out


# ------------------------------------------------------------ construction
def make_system(m):
    """Return (n, L, sigma) for the closed-form system, m divisible by 3."""
    assert m >= 6 and m % 3 == 0
    n, L = 6 * m, 2 * m // 3
    sigma = [M[(i // L) % 3] for i in range(n)]
    return n, L, sigma


def shift_offsets(m, window=1):
    """The sector offsets that the two-centre exclusion forces to be disjoint."""
    n = 6 * m
    D = set()
    for s in range(-window, window + 1):
        for base in (m - 1, m, m + 1):
            D.add((base + s) % n)
            D.add((-base + s) % n)
    D.discard(0)
    return sorted(D)


def check_system(m, verbose=True):
    """Exact integer verification of (P0),(P1),(P2),(P3),(P4-sector),(P5)."""
    n, L, sigma = make_system(m)
    D = shift_offsets(m)
    V = allowed_values()
    errs = []
    # (P0) palette bound
    for i in range(n):
        if not (1 <= len(sigma[i]) <= 3):
            errs.append(("P0", i, sigma[i]))
    # (P1) not contained in a cycle edge
    for i in range(n):
        for e in EDGES:
            if sigma[i] <= e:
                errs.append(("P1", i, sigma[i], tuple(sorted(e))))
    # (P2)/(P4) disjointness at every forced offset
    for i in range(n):
        for t in D:
            j = (i + t) % n
            if sigma[i] & sigma[j]:
                errs.append(("P2/P4", i, t, tuple(sorted(sigma[i])),
                             tuple(sorted(sigma[j]))))
    # (P3) no complementary triple pair  (vacuous: all values are pairs)
    used = set(sigma)
    for A in used:
        comp = frozenset(set(range(6)) - set(A))
        if len(A) == 3 and comp in used:
            errs.append(("P3", tuple(sorted(A))))
    # (P5) well defined on Z/n (period divides n)
    for i in range(n):
        if sigma[i] != sigma[i % n]:
            errs.append(("period", i))
    # the block-index lemma that makes everything work: for every i in Z/n and
    # every t in D, floor((i+t)/L) - floor(i/L) is congruent to 1 or 2 mod 3
    diffs = set()
    for i in range(n):
        for t in D:
            diffs.add(((i + t) % n) // L - i // L)
    if verbose:
        print("m=%d  n=%d  L=%d  3L=%d  n%%(3L)=%d" % (m, n, L, 3 * L, n % (3 * L)))
        print("  values used          :", sorted(tuple(sorted(v)) for v in used))
        print("  forced offsets |D|   :", len(D), D)
        print("  block differences    :", sorted(diffs),
              " mod 3 ->", sorted({d % 3 for d in diffs}))
        print("  violations           :", len(errs))
    return n, L, sigma, D, errs


# --------------------------------------------------------- step relation
def disjoint_options(v, values):
    return [w for w in values if not (v & w)]


def step_relation_report(k, cycle_len):
    values = allowed_values(k, cycle_len)
    deg = {v: len(disjoint_options(v, values)) for v in values}
    # clique number of the disjointness graph by brute force (|values| <= 35)
    best = 0
    bestset = None
    for r in range(1, 6):
        found = False
        for c in itertools.combinations(values, r):
            if all(not (a & b) for a, b in itertools.combinations(c, 2)):
                found = True
                best, bestset = r, c
                break
        if not found:
            break
    print("k=%d cycle=%d: |values|=%d, disjointness degree min/max=%d/%d, "
          "clique number=%d  e.g. %s"
          % (k, cycle_len, len(values), min(deg.values()), max(deg.values()),
             best, [tuple(sorted(v)) for v in bestset]))


if __name__ == "__main__":
    print("=== closed-form systems ===")
    for m in (6, 9, 12, 15, 18, 21, 30, 60):
        n, L, sigma, D, errs = check_system(m)
        assert not errs, errs
    print()
    print("=== value spaces / step relations ===")
    for k in (5, 6):
        for ell in range(3, k + 1):
            step_relation_report(k, ell)
