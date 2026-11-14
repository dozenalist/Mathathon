"""k = 6 interface CSP: is the (C4)+(C5) tightening ever binding?

Encoding of the ray geometry and of the slivers O_i, I_i follows the accepted
input (m5, .ultramath/smwfhd5sl/m5/interface_csp.py): cells c_0..c_{l-1} in
{0..5} with c_0 = 0 fixed by the pi/3 rotation symmetry, sign matrix
SIG[i][j] = sign cos((c_j + 1 - i) pi/3), slivers
    O_i = U u {j : the two incident edges at j are both negative}
    I_i = U u {j : the two incident edges at j are both positive}
with U = [k] \\ {0..l-1} the complement of the cycle label set.

Algorithm here is different from m5's: DFS over the six positions with the
palette-exclusion constraint (C4) checked pairwise at insertion, not a bitmask
DP, and the search is run three times per instance with different palette-size
caps so that the sizes of the model classes can be compared.

 (A) rmax = k-3, no (C4)   -> the (C1)-(C3) class of m5 (cross-check target)
 (B) rmax = k-3, with (C4) -> the tightened (C1)-(C5) class
 (C) rmax = 2,    with (C4) -> the class with no ternary palette at all;
                               (C4) and (C5) are both vacuous on it
"""
from itertools import combinations, product
import json, sys, time

COS = {0: 1, 1: 1, 2: -1, 3: -1, 4: -1, 5: 1}


def sig_matrix(l, c):
    return [[COS[(c[j] + 1 - i) % 6] for j in range(l)] for i in range(6)]


def slivers(l, k, s):
    T = (1 << l) - 1
    U = ((1 << k) - 1) ^ T
    O = I = 0
    for j in range(l):
        if s[(j - 1) % l] == -1 and s[j] == -1:
            O |= 1 << j
        if s[(j - 1) % l] == 1 and s[j] == 1:
            I |= 1 << j
    return O | U, I | U


def admissible(l, k, sig, rmax):
    """six lists of masks: 1 <= |P| <= rmax, P meets O_i and I_i."""
    out = []
    for i in range(6):
        O, I = slivers(l, k, sig[i])
        lst = []
        for r in range(1, rmax + 1):
            for comb in combinations(range(k), r):
                p = 0
                for x in comb:
                    p |= 1 << x
                if (p & O) and (p & I):
                    lst.append(p)
        out.append(lst)
    return out


def pc(m):
    return bin(m).count("1")


def solve(adm, c4):
    """DFS for a 6-cycle of admissible masks, consecutive (and cyclic) disjoint,
    and - when c4 - no two ternary palettes complementary, i.e. no two 3-masks
    with empty intersection (in Fin 6 two 3-sets are complementary iff disjoint)."""
    n = 6
    sol = []

    def ok(i, q):
        if i and (sol[i - 1] & q):
            return False
        if c4 and pc(q) == 3:
            for j in range(i):
                if pc(sol[j]) == 3 and not (sol[j] & q):
                    return False
        return True

    def dfs(i):
        if i == n:
            return not (sol[n - 1] & sol[0])
        for q in adm[i]:
            if ok(i, q):
                sol.append(q)
                if dfs(i + 1):
                    return True
                sol.pop()
        return False

    if dfs(0):
        return [sorted(x for x in range(6) if (p >> x) & 1) for p in sol]
    return None


def main(k=6):
    res = {}
    for l in range(3, k + 1):
        t0 = time.time()
        tot = a = b = c_ = 0
        wA = wB = wC = None
        c4_kills = []          # instances: (A) SAT but (B) UNSAT
        no_binary = []         # instances: (B) SAT but (C) UNSAT
        for tail in product(range(6), repeat=l - 1):
            c = (0,) + tail
            tot += 1
            sig = sig_matrix(l, c)
            adm3 = admissible(l, k, sig, k - 3)
            adm2 = admissible(l, k, sig, 2)
            if any(not x for x in adm3):
                a_ok = b_ok = False
                w = None
            else:
                w = solve(adm3, False)
                a_ok = w is not None
            if a_ok:
                wb = solve(adm3, True)
                b_ok = wb is not None
            else:
                b_ok = False
            if b_ok:
                wc = solve(adm2, True) if all(adm2) else None
                c_ok = wc is not None
            else:
                c_ok = False
            a += a_ok
            b += b_ok
            c_ += c_ok
            if a_ok and wA is None:
                wA = {"cells": list(c), "palettes": w}
            if b_ok and wB is None:
                wB = {"cells": list(c), "palettes": wb}
            if c_ok and wC is None:
                wC = {"cells": list(c), "palettes": wc}
            if a_ok and not b_ok:
                c4_kills.append(list(c))
            if b_ok and not c_ok:
                no_binary.append(list(c))
        res[l] = {"geometries": tot, "A_C1C3": a, "B_C1C5": b, "C_binary": c_,
                  "c4_kills": len(c4_kills), "c4_kill_example": c4_kills[:3],
                  "sat_without_binary": len(no_binary),
                  "nobinary_example": no_binary[:3],
                  "witness_A": wA, "witness_B": wB, "witness_C": wC,
                  "seconds": round(time.time() - t0, 2)}
        print(f"l={l}: geometries={tot} (C1-C3)={a} (C1-C5)={b} binary={c_} "
              f"| C4 kills {len(c4_kills)} | SAT but no binary {len(no_binary)} "
              f"| {time.time()-t0:.1f}s", flush=True)
    with open("csp_vacuity.json", "w") as f:
        json.dump(res, f, indent=1)
    return res


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 6)
