"""Sliver-profile analysis of the k=6 interface CSP (C1)-(C5).  Fast version.

Definitions (paper Def 5.1 / Lemma 8.1 / Cor 5.4, as recorded in m5/INTERFACE-NOGO.md
sec.1 and m2/L4-k-ladder.md Lemma 1.1):
  sigma[i][j] = sign(e_i . v_j),  e_i at angle i*pi/3, v_j in cell c_j in {0..5}
  sign(cos(t pi/3)) = +1 for t = 0,1,5 (mod 6), -1 for t = 2,3,4
  O_i = U cup {j : sigma[i][j-1] = sigma[i][j] = -1}
  I_i = U cup {j : sigma[i][j-1] = sigma[i][j] = +1},  U = {l,...,k-1}
  (C1) 1 <= |P_i| <= k-3 ; (C2) P_i & O_i, P_i & I_i nonempty ;
  (C3) P_i & P_{i+1} = 0 cyclically ; (C4) no two palettes are complementary 3-sets ;
  (C5) at most three ternary palettes.
"""
from itertools import product, combinations
import json

def cos_sign(t):
    return 1 if t in (0, 1, 5) else -1

def sign_word(ell, c):
    """The six rows as one base row + shifts: row i has sigma[i][j] = cos_sign((c[j]+1-i) % 6)."""
    return tuple(tuple(cos_sign((c[j] + 1 - i) % 6) for j in range(ell)) for i in range(6))

def slivers(ell, k, rows):
    U = frozenset(range(ell, k))
    out = []
    for row in rows:
        O = set(U); I = set(U)
        for j in range(ell):
            a, b = row[(j - 1) % ell], row[j]
            if a == -1 and b == -1:
                O.add(j)
            if a == 1 and b == 1:
                I.add(j)
        out.append((frozenset(O), frozenset(I)))
    return out

def admissible(k, O, I):
    return tuple(frozenset(s) for r in range(1, k - 2)
                 for s in combinations(range(k), r) if set(s) & O and set(s) & I)

def first_model(ell, k, c, tightened):
    rows = sign_word(ell, c)
    sl = slivers(ell, k, rows)
    adm = [admissible(k, O, I) for (O, I) in sl]
    if any(not a for a in adm):
        return None
    full = frozenset(range(k))
    cur = []

    def rec(i):
        if i == 6:
            if cur[5] & cur[0]:
                return False
            if tightened:
                tern = sum(1 for p in cur if len(p) == 3)
                if tern > 3:
                    return False
                t = [p for p in cur if len(p) == 3]
                for a in range(len(t)):
                    for b in range(a + 1, len(t)):
                        if (t[a] | t[b]) == full:
                            return False
            return True
        for q in adm[i]:
            if i and (q & cur[i - 1]):
                continue
            cur.append(q)
            if rec(i + 1):
                return True
            cur.pop()
        return False

    return list(cur) if rec(0) else None

def profile(ell, k, c):
    return tuple((len(O), len(I)) for (O, I) in slivers(ell, k, sign_word(ell, c)))

def scan(k=6):
    out = {}
    for ell in range(3, k + 1):
        rec = {}
        for name, tight in (("C1-C3", False), ("C1-C5", True)):
            sat = 0; first = None; prof_sat = {}; prof_all = {}
            for c in product(range(6), repeat=ell):
                pr = profile(ell, k, c)
                prof_all[pr] = prof_all.get(pr, 0) + 1
                m = first_model(ell, k, c, tight)
                if m is not None:
                    sat += 1
                    prof_sat[pr] = prof_sat.get(pr, 0) + 1
                    if first is None:
                        first = {"cells": list(c), "palettes": [sorted(p) for p in m],
                                 "profile": pr}
            rec[name] = {"geometries": 6 ** ell, "sat": sat, "first": first,
                         "profiles_all": {str(k2): v for k2, v in sorted(prof_all.items())},
                         "profiles_sat": {str(k2): v for k2, v in sorted(prof_sat.items())}}
            print(f"k={k} ell={ell} {name}: {sat}/{6**ell} SAT", flush=True)
        out[ell] = rec
    return out

if __name__ == "__main__":
    out = scan()
    with open("profile_results.json", "w") as f:
        json.dump(out, f, indent=1)
    print("written profile_results.json")
