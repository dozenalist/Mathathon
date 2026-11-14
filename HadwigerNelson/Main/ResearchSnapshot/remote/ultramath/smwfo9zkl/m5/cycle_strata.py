#!/usr/bin/env python3
"""Palette strata at a cyclic centre for every cycle length, k = 5 and k = 6.

At a centre x with a simple cycle C (on the label set of C) in Gamma_x, paper
(6.2) gives, for each EDGE {i,j} of C,

    P_x(e) is not contained in {i,j}          for a.e. e,

and the palette bound gives 1 <= |P| <= k-3.  That is the entire single-centre
content.  We enumerate all admissible palettes, for every cycle length
ell = 3,4,5,6, at k = 5 and 6, and record:

  * the admissible 1-element palettes  (labels outside V(C) only),
  * the admissible 2-element palettes  (the "diagonals": pairs of C-vertices not
    joined by an edge of C, together with pairs meeting the complement of V(C)),
  * the number of admissible 3-element palettes at k = 6 (none of them is ever
    excluded, because an edge has only two endpoints).

Two independent code paths: brute force over all subsets of I, and a closed-form
count using  #{2-sets inside E(C)} = |E(C)| = ell  and  #{2-sets inside V(C)} = C(ell,2).

Output is the input table for the per-cycle-length local-finiteness work at k=6.
"""
from itertools import combinations
from math import comb


def cycle_edges(ell):
    return [tuple(sorted(((i) % ell, (i + 1) % ell))) for i in range(ell)]


def admissible(k, ell):
    """all P with 1 <= |P| <= k-3, P not contained in an edge of the ell-cycle"""
    E = set(cycle_edges(ell))
    out = []
    for size in range(1, k - 2):
        for P in combinations(range(k), size):
            S = set(P)
            if not any(S <= set(e) for e in E):
                out.append(P)
    return out


def count_formula(k, ell):
    """independent count: total minus #{P contained in some edge} by inclusion-exclusion.

    Only singletons and pairs can sit inside an edge (an edge has 2 endpoints),
    so the excluded sets are: the ell singletons of V(C), and the ell pairs that
    are edges of C.  Edges of a simple cycle are pairwise distinct, so there is
    no over-count and no inclusion-exclusion correction is needed."""
    tot = sum(comb(k, j) for j in range(1, k - 2))
    return tot - ell - ell


def main():
    print("=" * 78)
    print("palette strata at a cyclic centre: (6.2) + palette bound 1 <= |P| <= k-3")
    print("=" * 78)
    for k in (5, 6):
        for ell in range(3, min(k, 6) + 1):
            adm = admissible(k, ell)
            bf, cf = len(adm), count_formula(k, ell)
            singles = [P for P in adm if len(P) == 1]
            pairs = [P for P in adm if len(P) == 2]
            triples = [P for P in adm if len(P) == 3]
            print("\nk = %d, cycle length ell = %d  (V(C) = 0..%d, extras %s)"
                  % (k, ell, ell - 1, list(range(ell, k))))
            print("  admissible: %d [brute force] vs %d [formula], agree: %s"
                  % (bf, cf, bf == cf))
            print("    singletons: %d  %s" % (len(singles), singles if len(singles) <= 8 else '...'))
            print("    2-element : %d  %s" % (len(pairs), pairs))
            print("    3-element : %d  (never excluded: an edge has 2 endpoints)"
                  % len(triples))
            if ell == k:
                print("    note: the cycle spans every label, so no palette of size 3 is")
                print("          excluded and (6.2) constrains only palettes of size <= 2.")
    print("\n" + "=" * 78)
    print("Consequences for the k = 6 cycle cases (single-centre content only):")
    print("  * A palette of size 3 is compatible with a cycle through ANY pair of")
    print("    labels, so at k = 6 no palette bound can forbid a cycle of any length.")
    print("    The single-centre constraints are powerless at every cyclic centre,")
    print("    consistently with the 'powerless class' theorem cited in the brief.")
    print("  * For ell = 6 the admissible 2-element palettes are exactly the 15 - 6 = 9")
    print("    diagonals of C_6 (6 at distance 2, 3 at distance 3); every singleton is")
    print("    excluded.  A 6-cycle at k = 6 therefore leaves a 3-periodic structure:")
    print("    distances 2 and 3 along C_6 are the two orbits of the dihedral group.")
    print("  * For ell = 5, k = 6: the admissible pairs are the 5 diagonals {i,i+2} and")
    print("    the 5 pairs {i,X} with the single extra label X.")
    print("  * For ell = 4, k = 6: the admissible pairs are the 2 diagonals, the 8 pairs")
    print("    {i,X},{i,Y} with the two extra labels, and {X,Y}.")
    print("  * For ell = 3, k = 6: 35 admissible palettes, including P = T (see")
    print("    triangle_stratum.py for the full table and its discussion).")
    print("=" * 78)


if __name__ == '__main__':
    main()
