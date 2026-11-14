"""verify.py -- exact, corrected computations for D13 (cell-constant hexagonal family).

Valid gadgets only:
  * a clique of the reachability graph of size m gives chi >= m;
  * any proper colouring restricts to an induced subgraph, so chi(indiced subgraph) <= chi(graph),
    and that induced chromatic number is computed EXACTLY here;
  * a coset colouring (sublattice of index n with minimum length > 1+2r) gives chi <= n.

By translation invariance of the reachability graph, a clique of size m exists iff one exists
containing the origin, so the clique search over offsets with |v| <= 1+2r is exhaustive.
"""
from fractions import Fraction as F
from math import sqrt
import json
from q3 import Q3, Pt, q3, SQ3, ZERO, ONE, HALF, hexagon, poly_dist2, lattice_pt
from cellbar import reachable, offsets_within, form, colour7

Q = lambda *a: Q3(*a)
OUT = {}


def max_clique(r, cap=12):
    """Exact clique number of the reachability graph (finite search, complete by translation
    invariance).  Returns (size, exact_points_as_ij)."""
    cand = offsets_within(r, ONE + Q3(2) * q3(r))
    pts = [(i, j, v) for (i, j, v) in cand]
    n = len(pts)
    nb = [[False] * n for _ in range(n)]
    for p in range(n):
        for q_ in range(p + 1, n):
            if reachable(pts[q_][2] - pts[p][2], r):
                nb[p][q_] = nb[q_][p] = True
    best = [[]]

    def ext(cur, allowed):
        if len(cur) + len(allowed) <= len(best[0]):
            return
        if len(cur) > len(best[0]):
            best[0] = cur[:]
        if len(cur) >= cap:
            return
        for pos, w in enumerate(allowed):
            ext(cur + [w], [u for u in allowed[pos + 1:] if nb[w][u]])

    ext([], list(range(n)))
    return len(best[0]), [(pts[k][0], pts[k][1]) for k in best[0]], n


def chi_induced(r, R=None):
    """Exact chromatic number of the induced subgraph on offsets with |v| <= R (default 1+2r)."""
    if R is None:
        R = ONE + Q3(2) * q3(r)
    cand = offsets_within(r, R)
    pts = [v for (_, _, v) in cand]
    n = len(pts)
    nb = [set() for _ in range(n)]
    for p in range(n):
        for q_ in range(p + 1, n):
            if reachable(pts[q_] - pts[p], r):
                nb[p].add(q_)
                nb[q_].add(p)
    # greedy upper bound
    col = [-1] * n
    for v in sorted(range(n), key=lambda x: -len(nb[x])):
        used = {col[u] for u in nb[v] if col[u] >= 0}
        c = 0
        while c in used:
            c += 1
        col[v] = c
    best = [max(col) + 1 if n else 0]
    col = [-1] * n
    nodes = [0]

    def rec(done, used_cols, limit_nodes=2_000_000):
        nodes[0] += 1
        if nodes[0] > limit_nodes:
            return
        if used_cols >= best[0]:
            return
        if done == n:
            best[0] = used_cols
            return
        # DSATUR pick
        bv, bs = -1, -1
        for u in range(n):
            if col[u] >= 0:
                continue
            sat = len({col[w] for w in nb[u] if col[w] >= 0})
            if sat > bs:
                bv, bs = u, sat
        used = {col[w] for w in nb[bv] if col[w] >= 0}
        for c in range(min(used_cols + 1, best[0] - 1) + 1):
            if c in used:
                continue
            col[bv] = c
            rec(done + 1, max(used_cols, c + 1))
            col[bv] = -1
            if nodes[0] > limit_nodes:
                return

    rec(0, 0)
    return best[0], n, nodes[0] > 2_000_000


def main():
    OUT["2-sqrt3"] = 2 - sqrt(3)
    OUT["r0"] = 1 / (sqrt(21) - 2)

    # (a) the exact threshold for the seven-clique, by testing rationals around 2-sqrt3
    th = []
    for rnum in [F(26, 100), F(267, 1000), F(268, 1000), F(27, 100), F(3, 10), F(2, 5), F(9, 20)]:
        s, cl, n = max_clique(rnum, cap=12)
        th.append({"r": str(rnum), "r_float": float(rnum), "clique": s, "offset_count": n,
                   "clique_points": cl})
    OUT["clique_number"] = th

    # (b) at the paper's radius: is there an 8-clique?
    s8, _, _ = max_clique(F(2, 5), cap=8)
    OUT["clique_at_2_5_capped8"] = s8

    # (c) induced-subgraph chromatic numbers (valid lower bounds) for r below 2 - sqrt3
    low = []
    for rnum in [F(1, 4), F(1, 5), F(3, 10)]:
        chi, n, hit = chi_induced(rnum)
        low.append({"r": str(rnum), "r_float": float(rnum), "vertices": n, "chi_induced": chi,
                    "search_truncated": hit})
    OUT["induced_chi_below_threshold"] = low

    with open("verify_results.json", "w") as f:
        json.dump(OUT, f, indent=1, default=str)
    print(json.dumps(OUT, indent=1, default=str))


if __name__ == "__main__":
    main()
