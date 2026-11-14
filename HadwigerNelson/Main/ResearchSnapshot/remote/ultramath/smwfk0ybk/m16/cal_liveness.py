"""Liveness controls for the constraint machinery of cal_variants.decide.

If the restriction code really bites, these variants must change the counts:
  min3   : every palette has size >= 3 (at k=6, ell=6 this is exactly (C1)'s maximum)
  nodup  : the six palettes are pairwise distinct
  cone   : every palette contains label 0  (incompatible with (C3) => 0)
  cap2   : size <= 2  (the stratum that should reproduce the base counts)
"""
from itertools import product
from cal_csp import sign_matrix, admissible, popcount


def decide(ell, k, c, cap=None, mincard=None, nodup=False, cone=False):
    sig = sign_matrix(ell, c)
    adm = [admissible(ell, k, sig[i]) for i in range(6)]
    if cap is not None:
        adm = [[p for p in a if popcount(p) <= cap] for a in adm]
    if mincard is not None:
        adm = [[p for p in a if popcount(p) >= mincard] for a in adm]
    if cone:
        adm = [[p for p in a if p & 1] for a in adm]
    if any(not a for a in adm):
        return False
    sol = []

    def dfs(i):
        if i == 6:
            return not (sol[5] & sol[0]) and (not nodup or len(set(sol)) == 6)
        for q in adm[i]:
            if i > 0 and (q & sol[i - 1]):
                continue
            if nodup and q in sol:
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


def scan(ell, k, **kw):
    sat = 0
    for t in product(range(6), repeat=ell - 1):
        if decide(ell, k, (0,) + t, **kw):
            sat += 1
    return sat


if __name__ == "__main__":
    for (ell, k) in ((3, 6), (5, 6), (6, 6), (6, 7), (7, 7)):
        print(f"k={k} ell={ell}: min3={scan(ell,k,mincard=3)}  nodup={scan(ell,k,nodup=True)}"
              f"  cone={scan(ell,k,cone=True)}  cap2={scan(ell,k,cap=2)}"
              f"  cap2+min2={scan(ell,k,cap=2,mincard=2)}", flush=True)
