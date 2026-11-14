#!/usr/bin/env python3
"""
d2 / m2 -- FINAL VERIFICATION for "section 8 at k = 6, cycle length ell = 5".

Runs, in order:
  [1] Lemma A  (the combinatorial reduction, all 32 sign patterns of a 5-cycle)
  [2] Theorem 1 (five-cycle gate at k = 6, outsider absent) -- five independent searches
  [3] Theorem 3 (calibration: Proposition 8.2 at k = 5, with and without the palette bound)
  [4] Theorem 4 (sharpness: the decisive hypothesis is the *identity* of the absent label)
  [5] Theorem 5 (an exact measurable palette field with a 5-cycle at k = 6 that avoids a
      cycle label, and hence satisfies Theorem 1's hypotheses except the absent label)
  [6] the hand proof's case analysis, checked as a standalone combinatorial lemma
Exit status 0 iff every assertion holds.
"""
import itertools, sys
from fractions import Fraction as F

sys.path.insert(0, "work")
from verify_d2 import (lemmaA, comp, allowed, internal, palettes, csp_solve,
                       csp_solve_cadical, family, runs, ELL)

K, OUT = 6, 5          # k = 6, outsider label X = 5
OK = True

def line(s=""):
    print(s)

# ---------------------------------------------------------------- [6] the case analysis
def case_analysis():
    """The hand proof of Theorem 1, step 5-6, isolated and checked exhaustively.

    Data: s_0..s_5 in Z/5, delta_0..delta_5 in {2,3}, with
       (i)  s_{i+3} = s_i                      (antipodal collapse: Q(-e) = complement Q(e))
      (ii)  d_i := s_i - s_{i+1} (mod 5) satisfies
              d_i not in {0, delta_{i+1}, -delta_i, delta_{i+1} - delta_i}
            (consecutive palettes {s_i, s_i+delta_i} disjoint).
    Claim: no solution.  The proof: (ii) gives the table
       (delta_i,delta_{i+1}) = (2,2)->d in {1,4}, (2,3)->{2,4}, (3,2)->{1,3}, (3,3)->{1,4},
    (i) gives d_{i+3} = d_i and hence sum_i d_i = 0, so d_0+d_1+d_2 = 0 mod 5; with each
    d_i in {1,2,3,4} the multiset is one of {1,1,3},{1,2,2},{2,4,4},{3,3,4}; each is refuted
    by the table (see RESULTS.md).  Here we verify both the claim and the four-case
    skeleton by exhaustive search."""
    table = {}
    for di in (2, 3):
        for dj in (2, 3):
            bad = {(0) % 5, dj, (-di) % 5, (dj - di) % 5}
            table[(di, dj)] = frozenset(x for x in range(5) if x not in bad)
    assert table == {(2, 2): frozenset({1, 4}), (2, 3): frozenset({2, 4}),
                     (3, 2): frozenset({1, 3}), (3, 3): frozenset({1, 4})}, table
    # exhaustive: no (s, delta) satisfying (i) and (ii)
    sols = 0
    for s0, s1, s2 in itertools.product(range(5), repeat=3):
        s = (s0, s1, s2, s0, s1, s2)
        for dl in itertools.product((2, 3), repeat=6):
            good = True
            for i in range(6):
                d = (s[i] - s[(i + 1) % 6]) % 5
                if d not in table[(dl[i], dl[(i + 1) % 6])]:
                    good = False; break
            if good:
                sols += 1
    assert sols == 0, sols
    # and the four-case skeleton: only these multisets can sum to 0 mod 5
    trips = [t for t in itertools.product((1, 2, 3, 4), repeat=3) if sum(t) % 5 == 0]
    mults = sorted({tuple(sorted(t)) for t in trips})
    assert mults == [(1, 1, 3), (1, 2, 2), (2, 4, 4), (3, 3, 4)], mults
    line("  [6] case analysis: allowed-set table exact; 0 solutions among 125*64 = 8000")
    line("      candidate (s,delta) data; the only 0-mod-5 triples are")
    line(f"      {mults}  -- the four cases of the proof.")

# ---------------------------------------------------------------- [5] the field
def cos_pos(t, b):
    d = (F(t) - F(b)) % 360
    return d < 90 or d > 270

def build_field():
    """The explicit model of Theorem 5 (all angles in degrees, coordinates exact rationals).
    geometry beta_j = 18 + 72j;  the field is constant on each 6-degree cell."""
    betas = [F(18 + 72 * j) for j in range(5)]
    vals = [frozenset({1, 3}), frozenset({2, 4}), frozenset({5})]   # B, C, A
    # A = {5} on (60,72) u (132,180) u (240,252) u (312,360);  B = {1,3} on (0,60) u (180,240);
    # C = {2,4} on (72,132) u (252,312).   Period 180, three pairwise disjoint values.
    def val(t):
        t = F(t) % 360
        if t < 60: return frozenset({1, 3})
        if t < 72: return frozenset({5})
        if t < 132: return frozenset({2, 4})
        if t < 180: return frozenset({5})
        if t < 240: return frozenset({1, 3})
        if t < 252: return frozenset({5})
        if t < 312: return frozenset({2, 4})
        return frozenset({5})
    field = [val(F(j)) for j in range(360)]
    pats = [frozenset(j for j in range(5) if cos_pos(F(c) + F(1, 2), betas[j])) for c in range(360)]
    assert len(set(field)) == 3
    # (8.1) on every cell
    for c in range(360):
        I, O = allowed(pats[c], K)
        assert field[c] & I and field[c] & O, ("8.1", c, sorted(field[c]), sorted(pats[c]))
        assert 1 <= len(field[c]) <= 2, ("|P|<=2", c)
        assert not any(field[c] <= frozenset({x, (x + 1) % 5}) for x in range(5)), ("6.2", c)
        assert 0 not in field[c], ("avoids the cycle label 0", c)
    # (5.7) for every direction
    for c in range(360):
        assert not (field[c] & field[(c + 60) % 360]), ("5.7", c)
    # (SUM): disjoint palettes of total size >= k are impossible  (palette-only content of (5.2))
    for i in range(360):
        for j in range(360):
            assert field[i] & field[j] or len(field[i]) + len(field[j]) < K, ("SUM", i, j)
    # (M11)
    worst = F(0)
    for t in range(1, 4):
        for T in itertools.combinations(range(K), t):
            T = frozenset(T)
            meas = F(sum(1 for c in range(360) if T <= field[c]), 360)
            worst = max(worst, meas)
            assert meas <= F(1, 2), ("M11", sorted(T), meas)
    nX = sum(1 for c in range(360) if OUT in field[c])
    # the record's own six-orbit constraint list (sprint/k6/STRUCTURE.md, Theorem 5),
    # with the centre colour i = 0 (a cycle label) and the cycle V(C) = {0,1,2,3,4}:
    for c in range(360):
        P = field[c]; nxt = field[(c + 60) % 360]; n2 = field[(c + 120) % 360]
        assert 0 not in P,                       ("Thm5.1  i not in P_j", c)
        assert not (P & nxt),                    ("Thm5.2  (5.7)", c)
        assert not (len(P) == 3 and len(nxt) == 3), ("Thm5.3", c)
        assert not (len(P) == 1 and min(P) in range(5)), ("Thm5.4  singleton in V(C)", c)
        assert not (not (P & n2) and len(P) + len(n2) == 5), ("Thm5.5", c)
        assert not (len(P) == 3 and len(n2) == 3 and not (P & n2)), ("Thm5.6", c)
    assert sum(1 for c in range(360) if len(field[c]) == 3) <= 180, "Thm5.7"
    return betas, pats, field, worst, nX

def theorem5():
    betas, pats, field, worst, nX = build_field()
    line("  [5] explicit measurable palette field, geometry beta_j = 18+72j degrees:")
    line(f"      values {{1,3}}, {{2,4}}, {{5}} on a 180-degree periodic schedule")
    line(f"      (8.1), (5.7), |P|<=2, (6.2), (SUM), (M11) verified on all 360 cells")
    line(f"      cycle label 0 absent from every palette (self-avoidance for 0)")
    line(f"      sigma{{X in P}} = {nX}/360 = {float(F(nX,360)):.4f}"
         f"   (Theorem 2: >= 1/6;  (5.7): <= 1/2)")
    line(f"      max_T sigma{{T subset P}} = {float(worst):.4f}  <= 1/2   (m11)")
    line(f"      two-valued state function (Lemma 6.4)? NO (three values)")
    line(f"      a state representing 3 labels (needed for Lemma 6.3)? NO (all |P| <= 2)")
    assert nX == 120 and worst <= F(1, 2)
    return True

def main():
    line("=" * 78)
    line("d2 / m2 -- section 8 at k = 6, cycle length ell = 5.  Final verification.")
    line("=" * 78)
    line("\n[1][2][3][4] are run by work/verify_d2.py and work/verify2_d2.py;")
    line("              their assertions are re-run here in abbreviated form.\n")
    G, table = lemmaA()
    fam = list(family(table))
    line(f"  [1] Lemma A: |G| = {len(G)}; the reduction, A(Q) = {{s+2,s+3}} and")
    line(f"      s(complement Q) = s(Q) hold for every sign pattern (exact).")
    # [2]
    for nm, fn in (("reduced s/delta search", lambda p: _reduced(p, table)),
                   ("full palette |P|<=3", lambda p: csp_solve(p, K, 3, frozenset({OUT}), True)),
                   ("full palette unbounded", lambda p: csp_solve(p, K, 5, frozenset({OUT}), True)),
                   ("CaDiCaL |P|<=3", lambda p: csp_solve_cadical(p, K, 3, frozenset({OUT}), True)),
                   ("CaDiCaL unbounded", lambda p: csp_solve_cadical(p, K, 5, frozenset({OUT}), True))):
        sat = sum(1 for p in fam if fn(p) is not None)
        line(f"  [2] Theorem 1, {nm:24s}: SAT {sat}/{len(fam)}")
        assert sat == 0
    # [3]
    for nm, fn in (("backtracking", lambda p: csp_solve(p, 5, 2)),
                   ("CaDiCaL", lambda p: csp_solve_cadical(p, 5, 2)),
                   ("backtracking, no palette bound", lambda p: csp_solve(p, 5, 5)),
                   ("CaDiCaL, no palette bound", lambda p: csp_solve_cadical(p, 5, 5))):
        sat = sum(1 for p in fam if fn(p) is not None)
        line(f"  [3] calibration k=5, {nm:30s}: SAT {sat}/{len(fam)}")
        assert sat == 0
    # [4]
    for nm, ab, st in (("nothing absent", frozenset(), False),
                       ("cycle label 0 absent", frozenset({0}), False),
                       ("outsider 5 absent", frozenset({OUT}), True)):
        sat = sum(1 for p in fam if csp_solve(p, K, 3, ab, st) is not None)
        line(f"  [4] sharpness, {nm:22s} (|P|<=3): SAT {sat:4d}/{len(fam)}")
        if nm == "outsider 5 absent":
            assert sat == 0
        else:
            assert sat > 0, nm
    case_analysis()
    line()
    theorem5()
    line("\nALL ASSERTIONS HOLD.")
    return 0

def _reduced(patterns, table):
    n = len(patterns)
    s = [table[Q][0] for Q in patterns]
    A = [table[Q][1] for Q in patterns]
    cand = [[frozenset({s[i], a}) for a in A[i]] for i in range(n)]
    sol = []
    def dfs(i):
        if i == n: return True
        for P in cand[i]:
            if sol and (P & sol[-1]): continue
            if i == n - 1 and (P & sol[0]): continue
            sol.append(P)
            if dfs(i + 1): return True
            sol.pop()
        return False
    return tuple(sol) if dfs(0) else None

if __name__ == "__main__":
    sys.exit(main())
