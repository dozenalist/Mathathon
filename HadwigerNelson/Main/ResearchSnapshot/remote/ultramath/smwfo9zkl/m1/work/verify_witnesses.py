#!/usr/bin/env python3
"""
Independent end-to-end verification for d12.

For EVERY graph G on 6 vertices with G != K_6 (32767 of them) construct the witness
palette function  P = S on A, S' on A^c   and verify the four constraints DIRECTLY,
without appealing to the reduction of proof.md:

  (P)   1 <= |S|,|S'| <= k-3
  (57)  P(e) cap P(R e) = empty   for every sector of an exact rational subdivision
  (T1)  no two palette values A,B with A cup B = I both of positive measure
  (62)  for every edge ij of G: neither palette value is a subset of {i,j}

Also verifies, for K_6, that no choice of (S,S') passes (P)/(57)/(T1)/(62) -- exhaustively.
This is a third code path: it checks the OBJECTS, not the combinatorial criterion.
"""
import itertools, sys
from fractions import Fraction

A_SECTORS = [(Fraction(0), Fraction(1, 3)), (Fraction(2, 3), Fraction(1)),
             (Fraction(4, 3), Fraction(5, 3))]

def in_A(t):
    t = t % 2
    return any(lo <= t < hi for lo, hi in A_SECTORS)

def pairs(k):
    return [(i, j) for i in range(k) for j in range(i + 1, k)]

def verify_witness(k, S, T, edge_set, nsub=6):
    """nsub = number of exact sectors; must be a multiple of 6 so that R is a shift"""
    S, T = frozenset(S), frozenset(T)
    if not (1 <= len(S) <= k - 3):
        return "P"
    if not (1 <= len(T) <= k - 3):
        return "P"
    if S & T:
        return "57"                       # needed and used for (57)
    if (S | T) == frozenset(range(k)):
        return "T1"
    for j in range(nsub):
        lo = Fraction(2 * j, nsub)        # theta in units of pi, over [0,2)
        st = S if in_A(lo) else T
        stR = S if in_A(lo + Fraction(1, 3)) else T     # R = rotation by pi/3
        if st & stR:
            return "57"
    for (i, j) in edge_set:
        if S <= {i, j} or T <= {i, j}:
            return "62"
    # A must be R^2-invariant for the two-value construction to be well defined
    for j in range(nsub):
        lo = Fraction(2 * j, nsub)
        if in_A(lo) != in_A(lo + Fraction(2, 3)):
            return "A-not-R2-invariant"
    return None

def witness_for(k, edge_set):
    """construct S,S' for G != K_k, k = 6"""
    allE = set(pairs(k))
    if edge_set == allE:
        return None
    a, b = sorted(allE - edge_set)[0]
    rest = [x for x in range(k) if x not in (a, b)]
    return tuple(sorted((a, b))), tuple(sorted(rest[:k - 3]))

def main():
    k = 6
    allE = pairs(k)
    n_ok = 0
    fails = []
    for r in range(len(allE) + 1):
        for es in itertools.combinations(allE, r):
            edge_set = set(es)
            if edge_set == set(allE):
                continue
            S, T = witness_for(k, edge_set)
            err = verify_witness(k, S, T, edge_set)
            if err:
                fails.append((sorted(edge_set), S, T, err))
            else:
                n_ok += 1
    print(f"k=6: witnesses constructed and verified end-to-end for {n_ok} graphs (G != K_6)")
    print(f"     failures: {len(fails)}")
    for f in fails[:5]:
        print("    ", f)

    # K_6: exhaustive search over all value pairs, INCLUDING constraint (62) for every edge
    full = frozenset(range(k))
    tried = 0
    ok = False
    for r1 in range(1, k - 2):
        for S in itertools.combinations(range(k), r1):
            Sf = frozenset(S)
            if any(Sf <= {i, j} for (i, j) in allE):
                continue                       # (62) already kills |S| <= 2
            for r2 in range(1, k - 2):
                for T in itertools.combinations(range(k), r2):
                    Tf = frozenset(T)
                    tried += 1
                    if any(Tf <= {i, j} for (i, j) in allE):
                        continue
                    if Sf & Tf or (Sf | Tf) == full:
                        continue
                    ok = True
                    print("    unexpected K_6 witness", S, T)
    print(f"K_6: {tried} value pairs tested (after (62) pruning of single values); "
          f"any admissible one? {ok}")
    print(f"K_5/k=5 for contrast: {(1,),(2,)} etc. -- see classify2.py")
    return 0 if (not fails and not ok) else 1

if __name__ == "__main__":
    sys.exit(main())
