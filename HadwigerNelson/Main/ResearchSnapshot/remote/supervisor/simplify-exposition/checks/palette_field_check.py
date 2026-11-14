#!/usr/bin/env python3
"""Exact finite check of the combinatorial step in Proposition 5.6 (paper Sec. 5.4)
and of what survives at k = 6.

Model.  A palette field of period N (6 | N) on k labels is a map
P : Z/N -> nonempty subsets of {0..k-1} with the 60-degree exclusion

    (5.7)  P(t) & P(t + N/6) = {}   for every t

(paper Corollary 5.4; Lean `EuclideanFiveColor.palette_sixty`).  A field is
binary for the pair {i,j} when  P(t) & {i,j} != {}  for every t  (paper Sec. 5.3;
Lean `BinaryCenter`).  A field is T-confined when P(t) <= T for every t.

Every count below is exhaustive over the declared finite space.  Nothing is
sampled, and no search is truncated.
"""
import itertools, json

def all_fields(k, N, sizes):
    """All fields with palette sizes in `sizes`, (5.7) enforced on the N-cycle."""
    step = N // 6
    subs = [frozenset(s) for r in sizes for s in itertools.combinations(range(k), r)]
    out, cur = [], []
    def rec(t):
        if t == N:
            if all(not (cur[i] & cur[(i + step) % N]) for i in range(N)):
                out.append(tuple(cur))
            return
        for S in subs:
            if t >= step and (cur[t - step] & S):
                continue
            cur.append(S); rec(t + 1); cur.pop()
    rec(0)
    return out

def binary_pairs(f, k):
    return [(i, j) for i in range(k) for j in range(i + 1, k)
            if all(f[t] & {i, j} for t in range(len(f)))]

def summary(k, N, sizes):
    F = all_fields(k, N, sizes)
    nb = [f for f in F if not binary_pairs(f, k)]
    wit = None
    if nb:
        # prefer a witness all of whose palettes have size >= 2, if one exists
        rich = [f for f in nb if all(len(s) >= 2 for s in f)]
        w = rich[0] if rich else nb[0]
        wit = {"field": [sorted(s) for s in w], "min_size": min(map(len, w))}
    return {"k": k, "N": N, "sizes": list(sizes), "fields": len(F),
            "nonbinary": len(nb), "witness": wit,
            "rich_nonbinary": sum(1 for f in nb if all(len(s) >= 2 for s in f))}

res = {"spaces": [], "ternary_k6": None}
res["spaces"].append(summary(5, 6, (1, 2)))
res["spaces"].append(summary(6, 6, (1, 2, 3)))
res["spaces"].append(summary(6, 6, (2, 3)))
res["spaces"].append(summary(6, 6, (3,)))

# Uniform ternary fields at k = 6: (5.7) forces P(t+1) = complement of P(t),
# hence period 2; then every pair meets both T and its complement.
T = []
for S in itertools.combinations(range(6), 3):
    T.append(frozenset(S))
pairwise = [(i, j) for i in range(6) for j in range(i + 1, 6)]
ok_all = all(all(({i, j} & s) and ({i, j} & (frozenset(range(6)) - s)) for s in T0)
             for (i, j) in pairwise) if T else None
res["ternary_k6"] = {
    "three_subsets": len(T),
    "every_2periodic_ternary_field_binary_for_every_pair": ok_all,
    "note": "(5.7)+|P|=3 forces P(t+1)=P(t)^c hence period 2; a pair meets both a 3-set and its complement",
}
print(json.dumps(res, indent=1, sort_keys=True))
