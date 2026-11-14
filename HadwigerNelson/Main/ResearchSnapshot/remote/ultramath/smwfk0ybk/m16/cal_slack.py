"""Slack of the surviving stratum: how many pair-stratum models each satisfiable
geometry of the k=6 interface system carries.

This is the quantity the next strengthening round (C6) has to drive to zero.  A candidate
constraint is useful only if it cuts *every* model listed here for at least one geometry.
"""
from itertools import product
from cal_csp import sign_matrix, admissible, popcount


def count_models(ell, k, c, cap):
    sig = sign_matrix(ell, c)
    adm = [admissible(ell, k, sig[i]) for i in range(6)]
    adm = [[p for p in a if popcount(p) <= cap] for a in adm]
    if any(not a for a in adm):
        return 0
    sol = []
    total = 0

    def dfs(i):
        nonlocal total
        if i == 6:
            if not (sol[5] & sol[0]):
                total += 1
            return
        for q in adm[i]:
            if i > 0 and (q & sol[i - 1]):
                continue
            sol.append(q)
            dfs(i + 1)
            sol.pop()

    for s in adm[0]:
        sol = [s]
        dfs(1)
    return total


if __name__ == "__main__":
    import json
    rep = {}
    for (ell, k) in ((5, 6), (6, 6)):
        counts = []
        for t in product(range(6), repeat=ell - 1):
            n = count_models(ell, k, (0,) + t, cap=2)
            if n:
                counts.append(n)
        counts.sort()
        rep[f"k{k}_ell{ell}"] = {
            "sat_geometries": len(counts),
            "total_pair_models": sum(counts),
            "min": counts[0], "median": counts[len(counts) // 2], "max": counts[-1],
        }
        print(f"k={k} ell={ell}: sat geometries={len(counts)}  pair models total={sum(counts)}"
              f"  per-geometry min/median/max = {counts[0]}/{counts[len(counts)//2]}/{counts[-1]}",
              flush=True)
    json.dump(rep, open("cal_slack.json", "w"), indent=1)
