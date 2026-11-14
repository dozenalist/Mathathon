"""Independent decision of the (C1)-(C5) tightened interface CSP at k=6.

Written from the definitions in .ultramath/smwfhd5sl/m5/INTERFACE-NOGO.md section 1
(paper Lemma 8.1 display (8.1), Corollary 5.4 display (5.7), Prop 5.6), not from
m5's code: the sign matrix is rebuilt from the cell formula
    sigma_j^(i) = +1  iff  c_j + 1 - i mod 6 in {0,1,5},
the allowed sets from
    O_i = U | {j in T : sigma_(j-1)^(i) = sigma_j^(i) = -1},
    I_i = U | {j in T : sigma_(j-1)^(i) = sigma_j^(i) = +1},
with T = {0..l-1} the cycle labels and U = {l..k-1} the outsiders.

Constraints:
 (C1) 1 <= |P_i| <= k-3
 (C2) P_i meets O_i and P_i meets I_i
 (C3) P_i cap P_{i+1} = empty, indices mod 6
 (C4) k=6: no two of the six palettes are complementary 3-sets
 (C5) k=6: at most three of the six palettes are ternary
"""
import itertools, json, sys

def sigma(c, j, i):
    return 1 if ((c[j] + 1 - i) % 6) in (0, 1, 5) else -1

def allowed(l, k, c, i):
    T = (1 << l) - 1
    U = ((1 << k) - 1) ^ T
    O = I = 0
    for j in range(l):
        if sigma(c, (j - 1) % l, i) == -1 and sigma(c, j, i) == -1:
            O |= 1 << j
        if sigma(c, (j - 1) % l, i) == +1 and sigma(c, j, i) == +1:
            I |= 1 << j
    return O | U, I | U

def admissible(l, k, c, i, lo=1):
    O, I = allowed(l, k, c, i)
    out = []
    for r in range(lo, k - 2):
        for comb in itertools.combinations(range(k), r):
            p = 0
            for x in comb:
                p |= 1 << x
            if (p & O) and (p & I):
                out.append(p)
    return out

def popcount(x):
    return bin(x).count("1")

def ok45(pals, k):
    """(C4) and (C5) at k=6, plus (C3) cyclically."""
    for i in range(6):
        if pals[i] & pals[(i + 1) % 6]:
            return False
    if k == 6:
        full = (1 << k) - 1
        for i in range(6):
            for j in range(i + 1, 6):
                if popcount(pals[i]) == 3 and pals[j] == full ^ pals[i]:
                    return False
        if sum(1 for p in pals if popcount(p) == 3) > 3:
            return False
    return True

def decide(l, k, constraints, normalise=True):
    """DFS over the six positions of the pi/3-orbit. Returns a witness or None."""
    total = 6 if not normalise else 1
    c0s = range(total)
    for c0 in c0s:
        for rest in itertools.product(range(6), repeat=l - 1):
            c = (c0,) + rest
            cand = [admissible(l, k, c, i) for i in range(6)]
            if any(not a for a in cand):
                continue
            # (C4)/(C5) can be pruned per step; simple DFS is fast enough here.
            sol = [0] * 6
            def dfs(i):
                if i == 6:
                    return check_full(sol, c, l, k, constraints)
                for p in cand[i]:
                    if i > 0 and (p & sol[i - 1]):
                        continue
                    sol[i] = p
                    if dfs(i + 1):
                        return True
                return False
            if dfs(0):
                return {"cells": list(c), "palettes": [lab(p, k) for p in sol]}
    return None

def check_full(sol, c, l, k, constraints):
    if sol[5] & sol[0]:
        return False
    if "C45" in constraints and not ok45(sol, k):
        return False
    return True

def lab(p, k):
    return [i for i in range(k) if (p >> i) & 1]

def scan(l, k, constraints=("C1C3",), normalise=True, stop_after=None):
    total, sat, first = 0, 0, None
    for c0 in (range(1) if normalise else range(6)):
        for rest in itertools.product(range(6), repeat=l - 1):
            c = (c0,) + rest
            cand = [admissible(l, k, c, i) for i in range(6)]
            total += 1
            if any(not a for a in cand):
                continue
            sol = [0] * 6
            found = [False]
            def dfs(i):
                if i == 6:
                    if check_full(sol, c, l, k, constraints):
                        found[0] = True
                        return True
                    return False
                for p in cand[i]:
                    if i > 0 and (p & sol[i - 1]):
                        continue
                    sol[i] = p
                    if dfs(i + 1):
                        return True
                return False
            if dfs(0):
                sat += 1
                if first is None:
                    first = {"cells": list(c), "palettes": [lab(p, k) for p in sol]}
                if stop_after is not None and sat >= stop_after:
                    return total, sat, first
    return total, sat, first

if __name__ == "__main__":
    out = {}
    print(f"{'k':>2} {'l':>2} {'m':>2} {'geoms':>7} {'C1C3':>7} {'C1C5':>7}  keys")
    for k in (4, 5, 6):
        for l in range(3, k + 1):
            t1, s1, f1 = scan(l, k, ("C1C3",))
            t2, s2, f2 = scan(l, k, ("C45",))
            print(f"{k:>2} {l:>2} {k-l:>2} {t1:>7} {s1:>7} {s2:>7}")
            out[f"k{k}_l{l}"] = {"k": k, "l": l, "geometries": t1,
                                 "sat_C1C3": s1, "sat_C1C5": s2,
                                 "witness_C1C5": f2}
            sys.stdout.flush()
    with open("csp45_results.json", "w") as f:
        json.dump(out, f, indent=1)
