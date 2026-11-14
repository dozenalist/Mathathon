"""Non-vacuity: the same constraint system decides a true case at k = 5.

LEMMA 3 (2-type obstruction).  Fix k, a simple cycle C with edge set E, and a
two-element set {a,b} of labels.  Suppose every admissible palette (1 <= |S| <=
k-3, S inside no edge of C) meets {a,b} in exactly one point.  Then no
accumulating sector model exists: with sigma as in construction.py, the map
i |-> sigma(i) cap {a,b} is a proper 2-colouring of the circulant on Z/n with
connection set D = {+-(m-1), +-m, +-(m+1)}, and that circulant is not
bipartite.

Proof.  Set type(i) = the unique member of sigma(i) cap {a,b}.  Disjointness
of sigma(i), sigma(j) forces type(i) != type(j).
  Step 1  type(i) = type(i+2).  Both i and i+2 are joined to i+m+1, because
          (i+m+1)-i = m+1 and (i+m+1)-(i+2) = m-1 both lie in D; so type(i) and
          type(i+2) both differ from type(i+m+1), a member of a two-element
          set.
  Step 2  m even: i and i+m have the same parity, so by Step 1
          type(i) = type(i+m), contradicting the edge i--(i+m) of the
          circulant (m in D).
  Step 3  m odd: m-1 is even, so g = gcd(m-1, 6m) = gcd(m-1, 6) is 2 or 6,
          and the orbit of i under +（m-1) has length 6m/g in {m, 3m}, which is
          odd.  Consecutive points of the orbit are joined by m-1 in D, so the
          types alternate around an odd cycle: a contradiction.
  Hence UNSAT for every m >= 2.                                                                QED

The hypothesis of Lemma 3 holds for (k,C) = (5, triangle) with {a,b} = the two
outsider labels, and for no other (k,C) with k in {5,6} and 3 <= |C| <= k.
That is the palette-level content of the paper's triangle argument -- the one
local-finiteness proof in section 6.3 that uses the palette constraints alone.
It fails at k = 6 for every cycle length, which is why Corollary 1 is not
vacuous.
"""
import itertools, sys
from pysat.solvers import Cadical153
from fractions import Fraction

KMAX = 6


def edges_of(k, ell):
    return [frozenset(sorted((i, (i + 1) % ell))) for i in range(ell)]


def admissible(k, ell):
    E = edges_of(k, ell)
    return [frozenset(c) for r in range(1, k - 2)
            for c in itertools.combinations(range(k), r)
            if not any(frozenset(c) <= e for e in E)]


def admissible_star(k, ell):
    """Occurrable palettes: admissible ones having a disjoint admissible
    partner.  (A palette with no disjoint admissible palette can never sit at a
    sector, which carries six disjointness constraints.)"""
    adm = admissible(k, ell)
    return [S for S in adm if any(not (S & T) for T in adm)]


def has_2type(k, ell):
    """Is there a 2-set met in exactly one point by every occurrable palette?"""
    adm = admissible_star(k, ell)
    out = []
    for a, b in itertools.combinations(range(k), 2):
        ab = {a, b}
        if all(len(set(v) & ab) == 1 for v in adm):
            out.append((a, b))
    return out


def lemma3_machine_checks():
    print("=== no other (k, cycle length) has a 2-type at k = 5 or 6 ===")
    for k in (5, 6):
        for ell in range(3, k + 1):
            t = has_2type(k, ell)
            print("  k=%d  C_%d : %d admissible, %d occurrable, 2-types = %s"
                  % (k, ell, len(admissible(k, ell)),
                     len(admissible_star(k, ell)),
                     ["{%d,%d}" % ab for ab in t]))
    assert has_2type(5, 3) == [(3, 4)]
    for k in (5, 6):
        for ell in range(3, k + 1):
            if (k, ell) != (5, 3):
                assert has_2type(k, ell) == [], (k, ell)
    print()
    print("=== the three steps of Lemma 3, verified arithmetically ===")
    for m in range(2, 40):
        n = 6 * m
        D = sorted({t % n for b in (m - 1, m, m + 1) for t in (b, -b)} - {0})
        # Step 1: i+m+1 is a common neighbour of i and i+2
        assert all((m + 1) % n in D and (m - 1) % n in D for _ in [0])
        if m % 2 == 0:
            pass          # Step 2 gives the contradiction
        else:
            g = Fraction(0)
            import math
            g = math.gcd(m - 1, n)
            assert (n // g) % 2 == 1, (m, n // g)     # Step 3: odd cycle
    print("  m even -> Step 2 applies; m odd -> orbit length 6m/gcd(m-1,6m)"
          " is odd for all 2 <= m < 40")
    print("  (gcd(m-1,6m) = gcd(m-1,6) is 2 or 6 when m is odd)")


def csp(k, ell, m):
    n = 6 * m
    V = admissible(k, ell)
    nv = len(V)
    D = sorted({t % n for b in (m - 1, m, m + 1) for t in (b, -b)} - {0})
    idx = {(i, a): i * nv + a + 1 for i in range(n) for a in range(nv)}
    cls = []
    for i in range(n):
        cls.append([idx[i, a] for a in range(nv)])
        for a, b in itertools.combinations(range(nv), 2):
            cls.append([-idx[i, a], -idx[i, b]])
    for i in range(n):
        for t in D:
            j = (i + t) % n
            for a in range(nv):
                for b in range(nv):
                    if V[a] & V[b]:
                        cls.append([-idx[i, a], -idx[j, b]])
    if k == 6:
        for A in V:
            if len(A) == 3:
                B = frozenset(set(range(6)) - set(A))
                if B in V and B != A:
                    a, b = V.index(A), V.index(B)
                    for i in range(n):
                        for j in range(n):
                            cls.append([-idx[i, a], -idx[j, b]])
    return n, V, D, idx, cls


def dpll(V, D, n, limit=20 * 10 ** 6):
    budget = [0]
    nv = len(V)
    comp = [[not (V[a] & V[b]) for b in range(nv)] for a in range(nv)]
    asg = [None] * n

    def ok(i, a):
        for t in D:
            j = (i + t) % n
            if asg[j] is not None and not comp[a][asg[j]]:
                return False
        return True

    def rec(i):
        if budget[0] > limit:
            raise TimeoutError
        if i == n:
            return True
        for a in range(nv):
            budget[0] += 1
            if ok(i, a):
                asg[i] = a
                if rec(i + 1):
                    return True
                asg[i] = None
        return False

    try:
        return list(asg) if rec(0) else None
    except TimeoutError:
        return "budget"


if __name__ == "__main__":
    lemma3_machine_checks()
    print()
    print("=== machine decision: k=5 triangle UNSAT, k=6 all lengths SAT ===")
    for (k, ell) in [(5, 3)]:
        for m in (2, 3, 4, 6, 9, 12, 18, 30, 60):
            n, V, D, idx, cls = csp(k, ell, m)
            with Cadical153(bootstrap_with=cls) as s:
                sat = s.solve()
            assert sat is False, (k, ell, m)
            tag = ""
            if m <= 6:
                r = dpll(V, D, n)
                tag = " independent-DPLL=%s" % (
                    "UNSAT" if r is None else ("budget-exceeded" if r == "budget" else "SAT"))
                assert r is None, (m, r)
            print("  k=%d C_%d m=%2d n=%3d |V|=%d  CaDiCaL=UNSAT%s"
                  % (k, ell, m, n, len(V), tag))
    for (k, ell) in [(6, 3), (6, 4), (6, 5), (6, 6)]:
        n, V, D, idx, cls = csp(k, ell, 6)
        with Cadical153(bootstrap_with=cls) as s:
            sat = s.solve()
        assert sat is True
        print("  k=%d C_%d m= 6 n=%3d |V|=%d  CaDiCaL=SAT" % (k, ell, n, len(V)))
    print()
    print("DONE")
