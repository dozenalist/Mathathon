"""Stratification of the interface model space: which palette-size stratum is forced?

Adds, on top of the m5 system (C1)-(C3), each subset of the m6 tightening
  (C4) no two palettes A,B with A|B = Fin k        [Theorem 1, general k]
  (C5) at most three palettes of size k-3          [Theorem 2, general k]
and the size caps, so that the *necessary* stratum of the k=6 model space is visible.
Also runs a liveness control (C5b: at most two of size k-3) which must reduce the counts
if the constraint machinery is really being applied.
"""
from itertools import product
from cal_csp import sign_matrix, admissible, popcount


def decide(ell, k, c, c4=False, c5=None, cap=None, want_model=False):
    sig = sign_matrix(ell, c)
    adm = [admissible(ell, k, sig[i]) for i in range(6)]
    if cap is not None:
        adm = [[p for p in a if popcount(p) <= cap] for a in adm]
    if any(not a for a in adm):
        return (False, None) if want_model else False
    full = (1 << k) - 1
    top = k - 3
    limit = c5
    sol = []
    found = []

    def dfs(i):
        if i == 6:
            if sol[5] & sol[0]:
                return False
            if limit is not None and sum(1 for p in sol if popcount(p) == top) > limit:
                return False
            return True
        for q in adm[i]:
            if i > 0 and (q & sol[i - 1]):
                continue
            if c4 and any((q | p) == full for p in sol):
                continue
            sol.append(q)
            if dfs(i + 1):
                return True
            sol.pop()
        return False

    for s in adm[0]:
        sol = [s]
        if dfs(1):
            if want_model:
                found = [sorted(j for j in range(k) if (p >> j) & 1) for p in sol]
                return (True, found)
            return True
    return (False, None) if want_model else False


VARIANTS = [("base", {}), ("C4", {"c4": True}), ("C5", {"c5": 3}),
            ("C4C5", {"c4": True, "c5": 3}), ("cap2", {"cap": 2}),
            ("C4C5cap2", {"c4": True, "c5": 3, "cap": 2}),
            ("C5b(control)", {"c4": True, "c5": 2})]


def scan(ell, k, kw):
    tot = sat = 0
    first = None
    for t in product(range(6), repeat=ell - 1):
        c = (0,) + t
        tot += 1
        if kw.get("cap") is not None:
            ok, w = decide(ell, k, c, want_model=True, **kw)
        else:
            ok, w = decide(ell, k, c, want_model=True, **kw)
        if ok:
            sat += 1
            if first is None:
                first = {"cells": list(c), "palettes": w}
    return tot, sat, first


if __name__ == "__main__":
    import json
    rows = []
    for k in (6, 7):
        for ell in range(3, k + 1):
            line = f"k={k} ell={ell} geoms={6**(ell-1):6d} :"
            rec = {"k": k, "ell": ell, "geometries": 6 ** (ell - 1)}
            for name, kw in VARIANTS:
                tot, sat, first = scan(ell, k, kw)
                line += f"  {name}={sat}"
                rec[name] = sat
                if name == "cap2":
                    rec["cap2_first_witness"] = first
            print(line, flush=True)
            rows.append(rec)
            json.dump(rows, open("cal_variants.json", "w"), indent=1)
