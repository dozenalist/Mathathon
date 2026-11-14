"""Tightened interface CSP at k = 6: (C1)-(C3) of m5 plus (C4) and (C5) of m6.

Decision procedure A (this file): depth-first search over the six positions with
incremental checking of every constraint, including the two global ones:

  (C4) no two of P_0..P_5 are complementary 3-sets  [m6 Theorem 1, orbit form]
  (C5) at most three of P_0..P_5 are ternary        [m6 Theorem 2, orbit form]

Encoding: label i in Fin k  <->  bit i of a Python int; disjointness is p & q == 0.
All arithmetic is exact integer arithmetic; no floating point anywhere.

Instances: for each interface length ell in {3,...,k} and each ray geometry, i.e.
each cell vector c in {0,...,5}^ell with c_0 = 0 (global rotation by pi/3 is a
symmetry), the sign matrix is SIG[i][j] = sign(cos((c_j + 1 - i) pi/3)) and the
paper's (8.1) gives O_i, I_i; the CSP is on P_0..P_5 with the cyclic index i mod 6.

  python3 tight_csp.py            -> table + tight_csp_results.json
  python3 tight_csp.py 5          -> one interface length
"""

import json
import sys
from itertools import product, combinations

K = 6
FULL = (1 << K) - 1


def cos_sign(m):
    """sign(cos(m pi/3)) for m in Z/6: +1 on {0,1,5}, -1 on {2,3,4}."""
    m %= 6
    return 1 if m in (0, 1, 5) else -1


def sign_matrix(cells):
    """SIG[i][j] = sign(e_i . v_j), e_i = R^i e.  6 x ell."""
    ell = len(cells)
    return [[cos_sign(cells[j] + 1 - i) for j in range(ell)] for i in range(6)]


def oi_masks(ell, sig_row):
    """(O_i, I_i) of paper (8.1) as bitmasks; labels 0..ell-1 are the cycle."""
    T = (1 << ell) - 1
    U = FULL ^ T
    O = I = U
    for j in range(ell):
        a, b = sig_row[(j - 1) % ell], sig_row[j]
        if a == -1 and b == -1:
            O |= 1 << j
        if a == 1 and b == 1:
            I |= 1 << j
    return O, I


def admissible(ell, sig_row, maxsize=K - 3):
    """(C1)+(C2): 1 <= |P| <= k-3, P meets O_i and I_i."""
    O, I = oi_masks(ell, sig_row)
    out = []
    for r in range(1, maxsize + 1):
        for comb in combinations(range(K), r):
            p = 0
            for i in comb:
                p |= 1 << i
            if (p & O) and (p & I):
                out.append(p)
    return out


def is_ternary(p):
    return bin(p).count("1") == 3


def complementary_3(a, b):
    return is_ternary(a) and is_ternary(b) and (a ^ b) == FULL


def solve(cells, maxsize=K - 3, tight=True, want="first", cap=10 ** 9):
    """DFS over the six positions.  Returns (sat, list_of_models)."""
    ell = len(cells)
    sig = sign_matrix(cells)
    adm = [admissible(ell, sig[i], maxsize) for i in range(6)]
    if any(not a for a in adm):
        return False, []
    sols = []
    P = [0] * 6

    def dfs(i, ntern, triples):
        for p in adm[i]:
            if i > 0 and (p & P[i - 1]):
                continue
            if i == 5 and (p & P[0]):
                continue
            is3 = tight and is_ternary(p)
            if is3:
                if ntern == 3:                                   # (C5)
                    continue
                if any((t ^ p) == FULL for t in triples):         # (C4)
                    continue
            P[i] = p
            if is3:
                triples.append(p)
            if i == 5:
                sols.append(list(P))
            else:
                dfs(i + 1, ntern + (1 if is3 else 0), triples)
            if is3:
                triples.pop()
            if sols and want == "first":
                return
            if len(sols) >= cap:
                return

    dfs(0, 0, [])
    return bool(sols), sols


def as_sets(sol):
    return [[i for i in range(K) if (p >> i) & 1] for p in sol]


def check_model(cells, sol, tight=True):
    """Re-verify a claimed model against (C1)-(C5) from scratch; None if valid."""
    ell = len(cells)
    sig = sign_matrix(cells)
    OI = [oi_masks(ell, sig[i]) for i in range(6)]
    for i in range(6):
        p = sol[i]
        n = bin(p).count("1")
        if not (1 <= n <= K - 3):
            return "C1 at %d" % i
        O, I = OI[i]
        if not (p & O) or not (p & I):
            return "C2 at %d" % i
        if p & sol[(i + 1) % 6]:
            return "C3 at %d" % i
    if tight:
        for i in range(6):
            for j in range(i + 1, 6):
                if complementary_3(sol[i], sol[j]):
                    return "C4 (%d,%d)" % (i, j)
        if sum(1 for i in range(6) if is_ternary(sol[i])) > 3:
            return "C5"
    return None


def geometry_list(ell):
    """All cell vectors with c_0 = 0: the rotation-normalised geometry list."""
    return [(0,) + t for t in product(range(6), repeat=ell - 1)]


def scan(ell, maxsize=K - 3, tight=True, verbose=True):
    geoms = geometry_list(ell)
    tot, sat = len(geoms), 0
    first = None
    unsat_geoms = []
    for c in geoms:
        s, sols = solve(c, maxsize=maxsize, tight=tight, want="first")
        if s:
            assert check_model(c, sols[0], tight) is None
            sat += 1
            if first is None:
                first = {"cells": list(c), "palettes": as_sets(sols[0])}
        else:
            unsat_geoms.append(list(c))
    if verbose:
        print("ell=%d  geometries=%d  SAT=%d  UNSAT=%d" % (ell, tot, sat, tot - sat),
              flush=True)
    return {"ell": ell, "geometries": tot, "sat": sat, "first": first,
            "unsat_geometries": unsat_geoms}


def main():
    args = sys.argv[1:]
    if args and args[0] != "all":
        ell = int(args[0])
        r = scan(ell)
        print("first model:", r["first"])
        return
    out = []
    print("Tightened interface CSP, k = 6, constraints (C1)-(C5)")
    for ell in range(3, K + 1):
        r = scan(ell, verbose=False)
        out.append(r)
        print("ell=%d  geometries=%d  SAT=%d  UNSAT=%d   first: %s"
              % (ell, r["geometries"], r["sat"], r["geometries"] - r["sat"],
                 r["first"]), flush=True)
    print("\ncontrol: (C1)-(C3) only   (must reproduce m5: 36, 216, 225, 177)")
    ctrl = []
    for ell in range(3, K + 1):
        r = scan(ell, tight=False, verbose=False)
        ctrl.append(r["sat"])
        print("ell=%d  SAT=%d / %d" % (ell, r["sat"], r["geometries"]), flush=True)
    json.dump({"tightened": out, "control_C1_C3": ctrl},
              open("tight_csp_results.json", "w"), indent=1)
    print("\nwrote tight_csp_results.json")


if __name__ == "__main__":
    main()
