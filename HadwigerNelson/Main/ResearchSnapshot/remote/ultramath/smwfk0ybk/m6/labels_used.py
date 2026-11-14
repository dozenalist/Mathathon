"""Minimum number of labels needed by a model, per satisfiable geometry at k=6.

Reason this matters: if a model of the x-interface uses at most k-2 = 4 labels,
two labels are free, and the alternation of two free labels is a model of the
constraints at a SECOND centre y = x + a that is disjoint from the first in every
direction (Remark 5.3 / (5.3): P_y(f) cap P_x(f) = empty, a.e. f != +-a).
So no finitely-many-centre strengthening of the CSP can bite at k = 6.
"""
import json
from itertools import combinations
import tight_csp as T

def solve_in_labels(cells, L):
    """SAT of (C1)-(C5) using only labels in L (a sorted tuple of labels)."""
    ell = len(cells)
    sig = T.sign_matrix(cells)
    adm = [[p for p in T.admissible(ell, sig[i]) if p & ~sum(1 << x for x in L) == 0]
           for i in range(6)]
    if any(not a for a in adm):
        return False
    P = [0] * 6
    def dfs(i, ntern, triples):
        for p in adm[i]:
            if i > 0 and (p & P[i-1]):
                continue
            if i == 5 and (p & P[0]):
                continue
            is3 = T.is_ternary(p)
            if is3:
                if ntern == 3 or any((t ^ p) == T.FULL for t in triples):
                    continue
            P[i] = p
            if is3: triples.append(p)
            if i == 5:
                return True
            if dfs(i+1, ntern + (1 if is3 else 0), triples):
                return True
            if is3: triples.pop()
        return False
    return dfs(0, 0, [])

res = {}
for ell in (3,4,5,6):
    dist = {}
    worst = 0
    for c in T.geometry_list(ell):
        ok, sols = T.solve(c, tight=True, want="first")
        if not ok:
            continue
        # minimum label-set size
        m = None
        for size in range(1, 7):
            found = False
            for L in combinations(range(6), size):
                if solve_in_labels(c, L):
                    found = True; break
            if found:
                m = size; break
        dist[m] = dist.get(m, 0) + 1
        worst = max(worst, m if m else 0)
    res[ell] = {"min_labels_distribution": dist, "max_min_labels": worst}
    print("ell=%d  min-labels distribution %s  max = %d" % (ell, dist, worst), flush=True)
json.dump(res, open("labels_used.json","w"), indent=1)
