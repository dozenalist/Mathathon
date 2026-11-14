"""Calibration of the TIGHTENED interface CSP (m5 encoding + m6 (C4),(C5)) at k >= 6.

Independent re-implementation of the m5 interface-state system, used here only to
calibrate the tightening across k (not to decide k=6).

Encoding (m5 / paper Lemma 8.1, Corollary 5.4, Prop 7.1):
  labels 0..k-1, cycle labels T = {0..ell-1}, outsiders U = rest.
  ray cell vector c in {0..5}^ell; sigma_j^(i) = sign(f_i . v_j), f_i = R^i e,
  sigma_j^(i) = +1 iff c_j + 1 - i mod 6 in {0,1,5}.
  O_i = U | { j in T : sigma_{j-1} = sigma_j = -1 },  I_i = U | { j : both +1 }.
  (C1) 1 <= |P_i| <= k-3 ; (C2) P_i meets O_i and I_i ; (C3) P_i cap P_{i+1} = empty (mod 6).
Tightening (m6):
  (C4) [Theorem 1, general k] no two of the six palettes A,B with A | B = Fin k.
  (C5) [Theorem 2, general k] at most three of the six palettes have size k-3.
"""
from itertools import combinations, product

COS_SIGN = {0: 1, 1: 1, 2: -1, 3: -1, 4: -1, 5: 1}


def sign_matrix(ell, c):
    return [[COS_SIGN[(c[j] + 1 - i) % 6] for j in range(ell)] for i in range(6)]


def allowed_sets(ell, k, sig_i):
    T = (1 << ell) - 1
    U = ((1 << k) - 1) ^ T
    O = I = 0
    for j in range(ell):
        if sig_i[(j - 1) % ell] == -1 and sig_i[j] == -1:
            O |= 1 << j
        if sig_i[(j - 1) % ell] == 1 and sig_i[j] == 1:
            I |= 1 << j
    return O | U, I | U


def admissible(ell, k, sig_i):
    O, I = allowed_sets(ell, k, sig_i)
    out = []
    for r in range(1, k - 2):
        for comb in combinations(range(k), r):
            p = 0
            for i in comb:
                p |= 1 << i
            if (p & O) and (p & I):
                out.append(p)
    return out


def popcount(p):
    return bin(p).count('1')


def decide(ell, k, c, tight):
    """True iff the six-position system is satisfiable. tight=True adds (C4),(C5)."""
    sig = sign_matrix(ell, c)
    adm = [admissible(ell, k, sig[i]) for i in range(6)]
    if any(not a for a in adm):
        return False
    full = (1 << k) - 1
    top = k - 3
    sol = []

    def dfs(i):
        if i == 6:
            if sol[5] & sol[0]:
                return False
            if tight and sum(1 for p in sol if popcount(p) == top) > 3:
                return False
            return True
        for q in adm[i]:
            if i > 0 and (q & sol[i - 1]):
                continue
            if tight and any((q | p) == full for p in sol):
                continue
            sol.append(q)
            if dfs(i + 1):
                return True
            sol.pop()
        return False

    for s in adm[0]:
        sol = [s]
        if dfs(1):
            return True
    return False


def witness(ell, k, c, tight):
    sig = sign_matrix(ell, c)
    adm = [admissible(ell, k, sig[i]) for i in range(6)]
    if any(not a for a in adm):
        return None
    full = (1 << k) - 1
    top = k - 3
    sol = []

    def dfs(i):
        if i == 6:
            if sol[5] & sol[0]:
                return False
            if tight and sum(1 for p in sol if popcount(p) == top) > 3:
                return False
            return True
        for q in adm[i]:
            if i > 0 and (q & sol[i - 1]):
                continue
            if tight and any((q | p) == full for p in sol):
                continue
            sol.append(q)
            if dfs(i + 1):
                return True
            sol.pop()
        return False

    for s in adm[0]:
        sol = [s]
        if dfs(1):
            return [sorted(j for j in range(k) if (p >> j) & 1) for p in sol]
    return None


def scan(ell, k, tight):
    total = sat = 0
    first = None
    for t in product(range(6), repeat=ell - 1):
        c = (0,) + t            # rotate: c_0 = 0 is a symmetry
        total += 1
        w = witness(ell, k, c, tight)
        if w is not None:
            sat += 1
            if first is None:
                first = {"cells": list(c), "palettes": w}
    return total, sat, first


if __name__ == "__main__":
    import json, time
    t0 = time.time()
    out = []
    print("k ell  geometries   base_SAT   tight_SAT   diff")
    for k in (6, 7, 8):
        for ell in range(3, k + 1):
            tot, sb, _ = scan(ell, k, tight=False)
            _, st, first = scan(ell, k, tight=True)
            print(f"{k:2d} {ell:3d} {tot:10d} {sb:10d} {st:10d}  {st-sb:+4d}"
                  + ("   UNSAT(tight)" if st == 0 else ""), flush=True)
            out.append({"k": k, "ell": ell, "geometries": tot, "base_sat": sb,
                        "tight_sat": st, "first_tight_witness": first})
            json.dump(out, open("cal_csp_results.json", "w"), indent=1)
    print("elapsed", round(time.time() - t0, 1), "s")
