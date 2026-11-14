"""Sliver-profile analysis of the k=6 interface CSP (C1)-(C5).

Independent re-derivation from the paper's own definitions as recorded in
m5/INTERFACE-NOGO.md sec.1 and m2/L4-k-ladder.md Lemma 1.1:
  sigma[i][j] = sign(e_i . v_j),  e_i at angle i*pi/3, v_j in cell c_j in {0..5}
  sign(cos(t pi/3)) = +1 for t = 0,1,5 (mod 6), -1 for t = 2,3,4
  O_i = U union {j : sigma[i][j-1] = sigma[i][j] = -1}
  I_i = U union {j : sigma[i][j-1] = sigma[i][j] = +1},  U = {l,...,k-1}
  (C1) 1 <= |P_i| <= k-3 ; (C2) P_i & O_i and P_i & I_i nonempty ;
  (C3) P_i & P_{i+1} = 0 cyclically ; (C4) no two palettes complementary 3-sets ;
  (C5) at most three ternary palettes.
"""
from itertools import product, combinations
import json, sys

def cos_sign(t):
    return 1 if t in (0, 1, 5) else -1

def sign_matrix(ell, c):
    return tuple(tuple(cos_sign((c[j] + 1 - i) % 6) for j in range(ell))
                 for i in range(6))

def slivers(ell, k, sig):
    U = frozenset(range(ell, k))
    out = []
    for i in range(6):
        row = sig[i]
        O = set(U); I = set(U)
        for j in range(ell):
            a, b = row[(j - 1) % ell], row[j]
            if a == -1 and b == -1:
                O.add(j)
            if a == 1 and b == 1:
                I.add(j)
        out.append((frozenset(O), frozenset(I)))
    return tuple(out)

def admissible(ell, k, O, I):
    return tuple(frozenset(s) for r in range(1, k - 2)
                 for s in combinations(range(k), r)
                 if set(s) & O and set(s) & I)

def all_models(ell, k, sig, tightened):
    """All six-tuples of palettes satisfying the constraints.  Backtracking over
    the cyclic order 0..5 with (C3) pruned on the fly; (C4)/(C5) checked at the end."""
    adm = [admissible(ell, k, O, I) for (O, I) in slivers(ell, k, sig)]
    if any(not a for a in adm):
        return []
    full = frozenset(range(k))
    sols = []

    def rec(i, cur):
        if i == 6:
            if cur[5] & cur[0]:
                return
            if tightened:
                tern = [p for p in cur if len(p) == 3]
                if len(tern) > 3:                       # (C5)
                    return
                for a in range(6):                      # (C4)
                    for b in range(a + 1, 6):
                        if len(cur[a]) == 3 and len(cur[b]) == 3 and (cur[a] | cur[b]) == full:
                            return
            sols.append(tuple(cur))
            return
        for q in adm[i]:
            if i and (q & cur[i - 1]):
                continue
            cur.append(q)
            rec(i + 1, cur)
            cur.pop()

    rec(0, [])
    return sols

def run(k=6, tightened_values=(False, True)):
    res = {}
    for ell in range(3, k + 1):
        total = 6 ** ell
        d = {}
        for tightened in tightened_values:
            sat = 0
            first = None
            for c in product(range(6), repeat=ell):
                sols = all_models(ell, k, sign_matrix(ell, c), tightened)
                if sols:
                    sat += 1
                    if first is None:
                        first = {"cells": list(c),
                                 "palettes": [sorted(p) for p in sols[0]],
                                 "n_models": len(sols)}
            d["C1-C5" if tightened else "C1-C3"] = {"geometries": total, "sat": sat,
                                                   "first": first}
            print(f"k={k} ell={ell} {'C1-C5' if tightened else 'C1-C3'}: "
                  f"{sat}/{total}", flush=True)
        res[ell] = d
    return res

if __name__ == "__main__":
    out = run()
    with open("profile_results.json", "w") as f:
        json.dump(out, f, indent=1)
