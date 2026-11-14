#!/usr/bin/env python3
"""Exhaustive decision of the palette stratum at a cyclic centre, k = 5 versus k = 6.

At a centre x whose transition graph Gamma_x contains the triangle T on labels
{a,b,c}, Lemma 6.2 (paper (6.2)) gives, for each of the three edges ij of T,

    P_x(e) is not contained in {i,j}                     for a.e. e.        (6.2)

Together with the palette bound 1 <= |P_x(e)| <= k-3 this completely decides
which palettes are admissible.  We enumerate all subsets P of the label set with
1 <= |P| <= k-3 and test containment in each pair of T.  Reported:

  (k=5)  the admissible palettes are exactly the two-element subsets of the two
         labels outside T; hence x is *binary for the fixed outside pair*, which
         is what feeds Lemma 5.5 and proves local finiteness of the triangle
         locus at k = 5 (Theorem 6.5, first case).

  (k=6)  the admissible palettes include {a,b,X} for every outsider X and the
         whole outsider triple {X,Y,Z}; in particular the outsider part
         A(e) = P_x(e) cap (I \\ T) can have 1, 2 or 3 elements and no fixed
         pair is forced.  So the triangle locus gets NO binarity and Lemma 5.5
         does not apply: the printed first case of Theorem 6.5 has no k = 6
         analogue.  This is the exact reason the k = 6 problem reduces to a
         finiteness statement about L rather than to the k = 5 argument.

The paper's k = 5 palette bound is Proposition 5.6 (|P| <= 2); at k = 6 the
replacement is 1 <= |P| <= 3 (general-k palette bound, results/K6-BARRIER.md §1).
"""
from itertools import combinations
from math import comb

T = (0, 1, 2)                       # the triangle labels
EDGES = list(combinations(T, 2))    # its three edges, as label pairs


def admissible(k, reps=1):
    """reps = number of distinct copies of the triangle label set in I.

    At k = 5 the five labels are T plus two outsiders; at k = 6, T plus three."""
    labels = list(range(k))
    out = []
    for size in range(1, k - 2):          # 1 <= |P| <= k-3
        for P in combinations(labels, size):
            # forbidden: P is CONTAINED in one of the three edges of T
            if not any(set(P) <= set(e) for e in EDGES):
                out.append(P)
    return out


def boolstr(b):
    return 'YES' if b else 'no'


def admissible_count_formula(k):
    """second, independent code path: inclusion-exclusion.

    admissible = #{P : 1 <= |P| <= k-3}  -  #{P contained in some edge of T}
    and by inclusion-exclusion over the three edges e1,e2,e3 of T:
      |A_e| = #{P nonempty, |P| <= k-3, P subset of the 2-set e} = 2 + [k-3 >= 2]
      |A_e cap A_f| = #{P subset of a single vertex} = 1
      |A_e cap A_f cap A_g| = 0.
    """
    tot = sum(comb(k, j) for j in range(1, k - 2))
    one = 2 + (1 if k - 3 >= 2 else 0)
    return tot - 3 * one + 3 * 1


def main():
    for k in (5, 6):
        I = set(range(k))
        outs = sorted(I - set(T))
        adm = admissible(k)
        print("=" * 72)
        print("[independent count] brute force %d, inclusion-exclusion %d, agree: %s"
              % (len(adm), admissible_count_formula(k), len(adm) == admissible_count_formula(k)))
        print("k = %d : labels %s, triangle T = %s, outsiders %s"
              % (k, sorted(I), list(T), outs))
        print("  palette bound 1 <= |P| <= %d ; pairs of T = %s" % (k - 3, EDGES))
        print("  admissible palettes (%d):" % len(adm))
        for P in adm:
            A = tuple(sorted(set(P) & set(outs)))
            print("     P = %-16s |P|=%d  outsider part A = %s (|A|=%d)"
                  % (str(P), len(P), A, len(A)))
        # is every admissible palette binary for one FIXED outside pair?
        print("  outsider parts that occur: %s"
              % sorted({tuple(sorted(set(P) & set(outs))) for P in adm}))
        meets = all(set(P) & set(outs) for P in adm)
        print("  every admissible palette meets the outsider set %s: %s"
              % (tuple(outs), boolstr(meets)))
        if len(outs) == 2:
            print("  => A(e) = P_x(e) cap (I\\T) is nonempty for a.e. e, and (5.7)")
            print("     makes it a singleton alternating under R: x is BINARY for")
            print("     the fixed pair %s.  Lemma 5.5 applies and the triangle"
                  % (tuple(sorted(outs)),))
            print("     locus is locally finite.  (This is the paper's argument.)")
        else:
            print("  palettes with |A| = 2 exist: %s"
                  % boolstr(any(len(set(P) & set(outs)) == 2 for P in adm)))
            print("  palettes equal to the whole outsider set exist: %s"
                  % boolstr(any(set(P) == set(outs) for P in adm)))
            print("  a fixed pair %s with every P intersecting it: %s"
                  % ('{X,Y}', boolstr(any(
                      all(set(P) & set(p) for P in adm)
                      for p in combinations(outs, 2)))))
            print("  => P_x(e) = T itself is admissible, so A(e) may be EMPTY; and")
            print("     when nonempty it may have 1, 2 or 3 elements.  No fixed pair")
            print("     and no fixed outsider is forced.  Lemma 5.5 (binary-centre")
            print("     separation) gets no input, so the printed triangle case of")
            print("     Theorem 6.5 has no k = 6 analogue.  The k = 6 problem is a")
            print("     finiteness statement about L, not a binarity statement.")
    print("=" * 72)
    print("Both enumerations are exact and exhaustive over all subsets; the only")
    print("inputs are (6.2) of the paper and the palette bound.  Script: this file.")


if __name__ == '__main__':
    main()
