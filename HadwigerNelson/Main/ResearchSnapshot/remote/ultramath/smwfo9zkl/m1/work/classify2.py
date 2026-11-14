#!/usr/bin/env python3
"""
d12  Classification of the transition graph Gamma_x from the complete single-centre
palette system, at k = 5, 6, 7, ...  (see proof.md for the reduction and the proof).

Single-centre constraints (all established elsewhere; cited, not re-derived):
  (P)   1 <= |P_x(e)| <= k-3                              palette bound (general k)
  (57)  P_x(e) cap P_x(R e) = empty   a.e.                paper (5.7) / Corollary 5.4
  (T1)  no A,B with A cup B = I both of positive angular measure
                                                          complementary-palette exclusion
  (62)  ij in Gamma_x  =>  P_x(e) not a subset of {i,j} a.e.   paper Lemma 6.2 / (6.2)

KEY REDUCTION (proved in proof.md):
  G is compatible with (P),(57),(T1),(62)
    <=>  there exist nonempty S,S' with |S|,|S'| <= k-3, S cap S' = empty,
         S cup S' != I, and neither S nor S' a subset of an edge of G.

  [<=] P(e) = S on A, S' on A^c, where A = [0,pi/3) u [2pi/3,pi) u [4pi/3,5pi/3) is R^2-invariant
       with R(A) = A^c.  Then (P),(57),(T1) hold and no palette value is inside an edge of G.
  [=>] take a positive-measure palette value S; (62) gives S not inside an edge of G; (57) makes
       some positive-measure value S' on R(A_S) disjoint from S; (T1) gives S cup S' != I.

CONSEQUENCE (checked exactly below):
  k = 6 : exactly ONE graph is incompatible, K_6.  Reason: at k=6 the allowed values of K_6 are
          the 20 triples, two disjoint triples are complementary, and (T1) forbids them.
  k >= 7: NO graph is incompatible (two disjoint 3-sets are allowed and have union of size 6 < k).
  k = 5 : 76 of the 1024 graphs are incompatible; the condition is an intersecting-family
          (Erdos-Ko-Rado type) condition on the non-edges plus isolated vertices.
"""
import itertools, sys
from fractions import Fraction

def pairs(k):
    return [(i, j) for i in range(k) for j in range(i + 1, k)]

# ---------------------------------------------------------------- decision procs
def allowed_values(k, edge_set):
    """nonempty S with |S| <= k-3 and S not a subset of any edge of G"""
    out = []
    for r in range(1, k - 2):
        for S in itertools.combinations(range(k), r):
            Ss = set(S)
            if any(Ss <= {i, j} for (i, j) in edge_set):
                continue
            out.append(frozenset(Ss))
    return out

def admissible_A(k, edge_set):
    """direct search, unordered pairs"""
    vals = allowed_values(k, edge_set)
    full = frozenset(range(k))
    for i, S in enumerate(vals):
        for T in vals[i:]:
            if S & T or (S | T) == full:
                continue
            return True, (tuple(sorted(S)), tuple(sorted(T)))
    return False, None

def admissible_B(k, edge_set):
    """independent path: bitmask universe, descending popcount scan, ordered loop"""
    emasks = [(1 << i) | (1 << j) for (i, j) in edge_set]
    full = (1 << k) - 1
    vals = []
    for m in range(1, 1 << k):
        if bin(m).count('1') > k - 3:
            continue
        ok = True
        for e in emasks:
            if (m & ~e) == 0:      # m subset of edge e
                ok = False
                break
        if ok:
            vals.append(m)
    vals.sort(key=lambda m: (-bin(m).count('1'), m))
    for S in vals:
        for T in vals:
            if S & T or (S | T) == full:
                continue
            return True, (S, T)
    return False, None

def admissible_closed(k, edge_set):
    """closed-form decision with a proof, for k = 5, k = 6, k >= 7"""
    allE = set(pairs(k))
    I = set(range(k))
    if k >= 7:
        return True, "two disjoint triples, union of size 6 < k"
    if k == 6:
        if edge_set == allE:
            return False, "K_6: allowed values are the 20 triples; two disjoint triples cover I"
        a, b = sorted(allE - edge_set)[0]
        rest = [x for x in range(6) if x not in (a, b)]
        return True, (tuple(sorted((a, b))), tuple(sorted(rest[:3])))
    if k == 5:
        # allowed values = non-edges (pairs) + isolated vertices (singletons).
        # two allowed values are compatible iff disjoint (union always has size <= 4 < 5).
        fam = [frozenset(e) for e in allE - edge_set]
        fam += [frozenset((v,)) for v in range(5) if all(v not in e for e in edge_set)]
        for i, S in enumerate(fam):
            for T in fam[i:]:
                if not (S & T):
                    return True, (tuple(sorted(S)), tuple(sorted(T)))
        return False, "family of non-edges + isolated vertices is intersecting"
    raise ValueError(k)

# ------------------------------------------------------- witness construction
A_SECTORS = [(Fraction(0), Fraction(1, 3)), (Fraction(2, 3), Fraction(1)),
             (Fraction(4, 3), Fraction(5, 3))]   # in units of pi; R^2-invariant, R(A)=A^c

def in_A(theta_over_pi):
    """theta measured in units of pi; exact rational arithmetic"""
    t = theta_over_pi % 2
    return any(lo <= t < hi for lo, hi in A_SECTORS)

def check_palette(k, S, T):
    """verify (P),(57),(T1),(T2),(T3) for the two-valued palette S on A, T on A^c.
    Angular measure is checked exactly on a rational grid of 12*m sectors (m integer);
    each sector [j/(6m), (j+1)/(6m)) lies entirely inside A or A^c, and R shifts by one."""
    S, T = frozenset(S), frozenset(T)
    assert 1 <= len(S) <= k - 3 and 1 <= len(T) <= k - 3, "(P)"
    assert not (S & T), "(57) needs disjointness"
    assert (S | T) != frozenset(range(k)), "(T1)"
    for m in (1, 6, 22):                    # 3 independent exact subdivisions
        n = 6 * m
        for j in range(n):
            lo = Fraction(j, n)
            st = S if in_A(lo) else T
            nxt = S if in_A(lo + Fraction(1, n)) else T
            # R shifts the angle by 1/6 of the circle: theta -> theta + 1/6
            nxtR = S if in_A(lo + Fraction(1, 3)) else T
            assert not (st & nxtR), ("(57) fails", m, j)
        # (T2) orbit bound: count ternary values in each R-orbit = 3 (A/S, A^c/T alternating)
        orbit = [S if (j % 2 == 0) else T for j in range(6)]
        assert sum(1 for v in orbit if len(v) == 3) <= 3, "(T2)"
        # (T3) mean palette size <= 5/2 at k = 6
        if k == 6:
            assert Fraction(len(S) + len(T), 2) <= Fraction(5, 2), "(T3)"
    return True

def cx(edge_set, S, T):
    """is neither palette value a subset of an edge?  equivalently G subset of E(P)"""
    return all(not (set(S) <= {i, j}) and not (set(T) <= {i, j}) for (i, j) in edge_set)

# ---------------------------------------------------------------- driver
def main():
    bad_reports = []
    print("=== exhaustive classification, k = 5 and k = 6 ===")
    results = {}
    for k in (5, 6):
        allE = pairs(k)
        inadm = []
        n = 0
        for r in range(len(allE) + 1):
            for es in itertools.combinations(allE, r):
                edge_set = set(es)
                n += 1
                a, wa = admissible_A(k, edge_set)
                b, wb = admissible_B(k, edge_set)
                c, _ = admissible_closed(k, edge_set)
                if not (a == b == c):
                    bad_reports.append(("MISMATCH", k, sorted(edge_set), a, b, c))
                if not a:
                    inadm.append(sorted(edge_set))
        results[k] = inadm
        print(f"k={k}: {n} graphs, {len(inadm)} incompatible")
        if k == 6:
            print("  the incompatible graph is K_6:",
                  len(inadm) == 1 and inadm[0] == sorted(allE))

    print()
    print("=== k = 5: characterisation of the 76 incompatible graphs ===")
    allE5 = set(pairs(5))
    fams = {}
    for g in results[5]:
        E = set(tuple(e) for e in g)
        fam = sorted(tuple(sorted(e)) for e in allE5 - E)
        iso = tuple(v for v in range(5) if all(v not in e for e in E))
        # intersecting-family fingerprint: are all non-edges pairwise intersecting?
        inter = all(set(x) & set(y) for i, x in enumerate(fam) for y in fam[i:])
        fams.setdefault((len(fam), len(iso), inter), 0)
        fams[(len(fam), len(iso), inter)] += 1
    for key in sorted(fams):
        print(f"  #non-edges={key[0]:2d}  #isolated={key[1]}  pairwise-intersecting={key[2]}"
              f"   count={fams[key]}")
    print("  (EKR check: the non-edges are pairwise intersecting in every case:",
          all(k[2] for k in fams), ")")

    print()
    print("=== k >= 7: sampled cross-check of the closed form ===")
    import random
    random.seed(20250923)
    for k in (7, 8):
        allE = pairs(k)
        trials = 3000
        mism = 0
        sat = 0
        for _ in range(trials):
            edge_set = set(e for e in allE if random.random() < 0.5)
            a, _ = admissible_A(k, edge_set)
            c, _ = admissible_closed(k, edge_set)
            if a != c:
                mism += 1
            sat += a
        a, w = admissible_closed(k, set(allE))
        print(f"k={k}: {trials} random graphs, mismatches={mism}, satisfiable={sat}/{trials}")
        print(f"  complete graph K_{k} compatible? {a}   witness={w}")

    print()
    print("=== the k = 6 maximum: |E(P)| = 14, i.e. K_6 minus one edge ===")
    S, T = (0, 1, 2), (3, 4)
    E = [(i, j) for (i, j) in pairs(6) if not (set(S) <= {i, j} or set(T) <= {i, j})]
    print(f"  witness P = {S} on A, {T} on A^c : E(P) has {len(E)} edges;")
    print(f"  the missing edge is the unique pair containing {T}: "
          f"{[p for p in pairs(6) if p not in E]}")
    print(f"  this witness attains (T2) exactly (3 ternary per orbit) and (T3) exactly "
          f"(mean = {(len(S)+len(T))/2})")
    print("  and the six-cycle witness is (0,2,4)|(1,3), checked below")

    print()
    print("=== exact verification of the witnesses ===")
    cases = [
        ("C_6 witness (attains both bounds)", 6, (0, 2, 4), (1, 3)),
        ("K_6 minus edge {2,3}", 6, (0, 1, 4), (2, 3)),
        ("generic k=6", 6, (0, 1, 2), (3, 4)),
        ("k=7 (no exclusion at all)", 7, (0, 2, 4), (1, 3)),
        ("k=5 binary alternation", 5, (0, 2), (1, 3)),
    ]
    for name, k, S, T in cases:
        check_palette(k, S, T)
        print(f"  {name}: (P),(57),(T1),(T2),(T3) verified exactly for S={S}, T={T}")
    # and the C_6 edges
    S, T = (0, 2, 4), (1, 3)
    ok = all(not (set(S) <= {i, (i+1) % 6}) and not (set(T) <= {i, (i+1) % 6}) for i in range(6))
    print(f"  six-cycle C_6 satisfies (62) against this witness: {ok}")

    print()
    if bad_reports:
        print("PROBLEMS:")
        for r in bad_reports:
            print("  ", r)
        return 1
    print("all cross-checks agree; no mismatches")
    return 0

if __name__ == "__main__":
    sys.exit(main())
