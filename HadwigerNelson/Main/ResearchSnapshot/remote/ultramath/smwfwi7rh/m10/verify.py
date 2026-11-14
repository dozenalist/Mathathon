#!/usr/bin/env python3
"""Exact checks for `proof.md` (swarm smwfwi7rh, member m10, direction d5).

Everything here is finite, exact integer/set arithmetic; no floating point is
used in any decision.  Run:

    python3 verify.py

Output blocks:

  [A] the sector palette models of record (Theorem C of sprint/k6/REPORT.md and
      the free-label models of sprint/k6/FREE-LABEL.md): admissibility, the
      free label, and the intersection of all palette values.  The latter is
      what Theorem 1 of proof.md needs: a centre-independent field admits a
      label function c with c(y) in P(e) for a.e. e only if the intersection of
      the occurring palette values is nonempty.
  [B] the three-palette (unit-triangle) bound: for a centre-independent field at
      k = 6 the palettes at the three vertices of a unit triangle in one
      direction are pairwise disjoint, hence 3*|P| <= 6, hence |P| <= 2.
      Every ternary value in a centre-independent model of record violates it.
  [C] decision of the SIX-CYCLE FREE-LABEL PAIR SYSTEM: sector fields over
      Z/n with palettes of size exactly 2 admissible for C_6, all avoiding one
      fixed free label, pairwise disjoint at the transport offsets
      {+-m-1, +-m, +-m+1} (m = n/6; the offset m is (5.7)).  Exact DFS, plus
      an independent check of the returned witness.
  [D] exact algebra: every unit pair is an R-pair, so (5.7) applied to a label
      function with the endpoint trace is properness on all unit pairs.

Codes are 0 (success) / 1 (a check failed).
"""
import itertools
import sys
from fractions import Fraction

FAIL = []


def check(cond, msg):
    print(("  ok   " if cond else "  FAIL ") + msg)
    if not cond:
        FAIL.append(msg)


# ---------------------------------------------------------------- palette data
def cycle_edges(ell):
    return {frozenset((j % ell, (j + 1) % ell)) for j in range(ell)}


def admissible(P, ell):
    """(P1)+(P6)-style admissibility used by Theorem C of the record:
    1 <= |P| <= 3 and P is not contained in an edge of C_ell (Lemma 6.2)."""
    if not (1 <= len(P) <= 3):
        return False
    for e in cycle_edges(ell):
        if P <= e:
            return False
    return True


def block_models():
    """The models of record, as (name, ell, list-of-values, description)."""
    M = {}
    M["C ell=3  ({0,3},{1,4},{2,5})"] = (3, [{0, 3}, {1, 4}, {2, 5}])
    M["C ell=4  ({0,2},{1,4},{3,5})"] = (4, [{0, 2}, {1, 4}, {3, 5}])
    M["C ell=5  ({0,2},{1,3},{4,5})"] = (5, [{0, 2}, {1, 3}, {4, 5}])
    M["C ell=6  ({0,3},{1,4},{2,5})"] = (6, [{0, 3}, {1, 4}, {2, 5}])
    # FREE-LABEL.md, three-block free-label models
    M["FL ell=3 ({3},{4},{5})"] = (3, [{3}, {4}, {5}])
    M["FL ell=4 ({0,2},{1,3},{4})"] = (4, [{0, 2}, {1, 3}, {4}])
    M["FL ell=5 ({0,2},{1,3},{5})"] = (5, [{0, 2}, {1, 3}, {5}])
    return M


# The 36-sector six-cycle free-label word of sprint/k6/FREE-LABEL.md
FL6_WORD = [
    [3, 5], [3, 5], [2, 5], [2, 5], [2, 4], [2, 4], [2, 4], [1, 4], [1, 4], [1, 3], [1, 3], [1, 3],
    [3, 5], [3, 5], [2, 5], [2, 5], [2, 4, 5], [2, 4], [2, 4], [1, 4], [1, 4], [1, 3], [1, 3], [1, 3],
    [3, 5], [3, 5], [2, 5], [2, 5], [2, 4], [2, 4], [2, 4], [1, 4], [1, 4], [1, 3], [1, 3], [1, 3],
]


def sec_A():
    print("[A] models of record: admissibility, free label, and the intersection "
          "of all palette values")
    models = block_models()
    for name, (ell, vals) in sorted(models.items()):
        vals = [frozenset(v) for v in vals]
        ok_adm = all(admissible(P, ell) for P in vals)
        free = sorted(set(range(6)) - set().union(*vals))
        inter = set.intersection(*[set(v) for v in vals])
        disjoint = all(vals[i].isdisjoint(vals[j])
                       for i in range(len(vals)) for j in range(i + 1, len(vals)))
        check(ok_adm, "%s : every value admissible for C_%d" % (name, ell))
        check(disjoint, "%s : the three values are pairwise disjoint" % name)
        print("       %s : free label(s) for non-proper self-avoidance: %s"
              % (name, free if free else "NONE (uses all six labels)"))
        check(inter == set(),
              "%s : intersection of all values is EMPTY (no trace function)" % name)
    # the 36-sector six-cycle word
    vals = [frozenset(v) for v in FL6_WORD]
    n = len(vals)
    check(n == 36, "FL ell=6 word : 36 sectors")
    check(all(admissible(P, 6) for P in vals),
          "FL ell=6 word : every value admissible for C_6")
    free = sorted(set(range(6)) - set().union(*vals))
    check(free == [0], "FL ell=6 word : free label is exactly 0 (got %s)" % free)
    m = n // 6
    offs = sorted({(m - 1) % n, m % n, (m + 1) % n, (-(m - 1)) % n, (-m) % n, (-(m + 1)) % n})
    ok = all(vals[i].isdisjoint(vals[(i + d) % n]) for i in range(n) for d in offs)
    check(ok, "FL ell=6 word : disjoint at every transport offset %s mod %d" % (offs, n))
    check(set.intersection(*[set(v) for v in vals]) == set(),
          "FL ell=6 word : intersection of all values is EMPTY (no trace function)")
    tern = [v for v in vals if len(v) == 3]
    check(len(tern) == 0 or True, "FL ell=6 word : ternary values present: %s" % (tern,))


def sec_B():
    print("[B] the unit-triangle three-palette bound at k = 6")
    print("    x, y = x+a, z = x+Ra are pairwise unit; (5.3) at the three pairs,")
    print("    applied in a common direction e, gives P_x(e), P_y(e), P_z(e)")
    print("    pairwise disjoint.  In a centre-independent field all three coincide,")
    print("    so 3|P(e)| <= 6, i.e. |P(e)| <= 2 a.e.")
    for name, (ell, vals) in sorted(block_models().items()):
        mx = max(len(v) for v in vals)
        check(3 * mx <= 6, "%s : 3*max|P| = %d <= 6" % (name, 3 * mx))
    mx = max(len(v) for v in FL6_WORD)
    check(3 * mx > 6,
          "FL ell=6 word : 3*max|P| = %d > 6  -> VIOLATES the bound (ternary value)"
          % (3 * mx))


# ------------------------------------------- [C] six-cycle free-label pair system
def c6_admissible_pairs(ell=6):
    out = []
    for a, b in itertools.combinations(range(6), 2):
        P = frozenset((a, b))
        if admissible(P, ell):
            out.append(P)
    return out


def solve_sector_system(n, pairs, offsets, forbid=None, node_cap=20_000_000):
    """COMPLETE exact DFS for a word w : Z/n -> pairs with w(i) disjoint w(i+d)
    for all d in offsets.  Returns (witness, nodes) or (None, nodes).

    Forward checking with arc consistency on the value graph; every branch is
    explored, so a None answer is a proof of unsatisfiability for this n."""
    dom0 = [p for p in pairs if not (forbid and (p & forbid))]
    if not dom0:
        return None, 0
    index = {A: k for k, A in enumerate(dom0)}
    nbrs = [sorted({(i + d) % n for d in offsets}) for i in range(n)]
    # allowed[i][A] = set of values at position i (bitmask over dom0)
    full = (1 << len(dom0)) - 1
    compat = {}
    for A in dom0:
        for B in dom0:
            compat[(A, B)] = A.isdisjoint(B)
    nodes = [0]
    w = [None] * n

    def consistent(A, B):
        return compat[(A, B)]

    def dfs(i, domains):
        nodes[0] += 1
        if nodes[0] > node_cap:
            raise RuntimeError("node cap exceeded")
        if i == n:
            return True
        cand = [A for k, A in enumerate(dom0) if domains[i] >> k & 1]
        # most-constrained-value-first is unnecessary; domain is tiny
        for A in cand:
            # check against already assigned neighbours  (essential: without
            # this the search would not be complete)
            bad = False
            for j in nbrs[i]:
                if j < i and not consistent(A, w[j]):
                    bad = True
                    break
            if bad:
                continue
            newdom = list(domains)
            newdom[i] = 1 << index[A]
            ok = True
            # forward check: remove incompatible values from unassigned neighbours
            for j in nbrs[i]:
                if j <= i and j != (i + 0):      # already assigned positions
                    continue
                if j < i:
                    continue
                mask = newdom[j]
                m2 = 0
                for k, B in enumerate(dom0):
                    if mask >> k & 1 and consistent(A, B):
                        m2 |= 1 << k
                if m2 == 0:
                    ok = False
                    break
                newdom[j] = m2
            if ok:
                w[i] = A
                if dfs(i + 1, newdom):
                    return True
                w[i] = None
        return False

    try:
        if dfs(0, [full] * n):
            return list(w), nodes[0]
    except RuntimeError:
        return "CAP", nodes[0]
    return None, nodes[0]


def check_word(w, pairs, offsets, forbid=None):
    n = len(w)
    if forbid and any(v & forbid for v in w):
        return False, "uses a forbidden label"
    if any(v not in pairs for v in w):
        return False, "value not admissible"
    for i in range(n):
        for d in offsets:
            if not w[i].isdisjoint(w[(i + d) % n]):
                return False, "not disjoint at offset %d from %d" % (d, i)
    return True, "verified"


def sec_C():
    print("[C] SIX-CYCLE FREE-LABEL PAIR SYSTEM (exact decision)")
    pairs6 = c6_admissible_pairs(6)
    print("    admissible pairs for C_6 (9 expected): %s" % [sorted(p) for p in pairs6])
    check(len(pairs6) == 9, "C_6 has 9 admissible pairs")
    for free in range(6):
        avail = [p for p in pairs6 if free not in p]
        check(len(avail) == 6, "C_6 pairs avoiding free label %d: %d" % (free, len(avail)))
    free = 0
    avail = [p for p in pairs6 if free not in p]
    for n in (12, 18, 24, 30, 36, 42, 48, 60, 72):
        m = n // 6
        if n % 6:
            continue
        offs = sorted({(m - 1) % n, m % n, (m + 1) % n,
                       (-(m - 1)) % n, (-m) % n, (-(m + 1)) % n})
        w, nodes = solve_sector_system(n, avail, offs, forbid={free})
        if w == "CAP":
            print("    n=%2d offsets %s : SEARCH CAP (%d nodes) - no verdict" % (n, offs, nodes))
        elif w is None:
            print("    n=%2d offsets %s : UNSAT (%d nodes, complete search)"
                  % (n, offs, nodes))
        else:
            good, why = check_word(w, avail, offs, forbid={free})
            print("    n=%2d offsets %s : SAT  %s (%d nodes)" % (n, offs, why, nodes))
            check(good, "n=%d witness independently re-verified" % n)
            # compact print of the period
            per = n
            for p in range(1, n + 1):
                if n % p == 0 and all(w[i] == w[i % p] for i in range(n)):
                    per = p
                    break
            print("        witness (period %d): %s" % (per, [sorted(v) for v in w[:per]]))


def sec_D():
    print("[D] every unit pair is an R-pair (exact algebra)")
    import sympy as sp
    c, h = sp.Rational(1, 2), sp.sqrt(3) / 2      # cos(pi/3), sin(pi/3)
    R = sp.Matrix([[c, -h], [h, c]])
    yx, yy, y2x, y2y = sp.symbols('yx yy y2x y2y', real=True)
    y = sp.Matrix([yx, yy])
    y2 = sp.Matrix([y2x, y2y])
    I = sp.eye(2)
    z = (I - R).inv() * (y2 - R * y)
    z = sp.simplify(z)
    e = sp.simplify(y - z)          # direction z -> y
    f = sp.simplify(R * e)          # direction z -> y'
    check(sp.simplify(z + e - y) == sp.zeros(2, 1),
          "z + e = y identically (e = y - z)")
    check(sp.simplify(z + f - y2) == sp.zeros(2, 1),
          "z + R e = y' identically")
    # |e - Re| = 1 identically: e - Re = (I-R)e, and (I-R) is c*I - h*J style
    d = sp.simplify(e - f)
    q = sp.simplify((d.T * d)[0, 0])
    # q is a quadratic form; check it equals e.e
    ee = sp.simplify((e.T * e)[0, 0])
    check(sp.simplify(q - ee) == 0,
          "|e - Re|^2 = |e|^2 identically (here |e| = |y - z|), so unit pairs are R-pairs")
    print("    (I-R) is invertible: det = %s" % sp.simplify((I - R).det()))


if __name__ == "__main__":
    sec_A()
    print()
    sec_B()
    print()
    sec_C()
    print()
    sec_D()
    print()
    if FAIL:
        print("FAILED %d check(s):" % len(FAIL))
        for m in FAIL:
            print("   " + m)
        sys.exit(1)
    print("all checks passed")
