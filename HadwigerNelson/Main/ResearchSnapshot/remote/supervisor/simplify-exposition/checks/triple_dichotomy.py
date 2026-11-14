#!/usr/bin/env python3
"""Exact verification of the k=6 triple dichotomy for palette fields.

Setting.  k labels, a centre y, a fixed label set T with |T| = 3, and the
palette field v |-> P(v) of period N (6 | N) with (5.7)  P(v) & P(v+N/6) = {}.
Assume  S(v) := P(v) & T  is nonempty for every v   (this is exactly what the
paper's constant-sequence-trace argument delivers at k = 6 from a triple
A<=P_x(e), with T = labels \ A).

What the script decides (and one retraction).  A first draft of this file
claimed the dichotomy "either y is binary for some pair in T, or S is exactly
the 3-periodic singleton cycle".  That is FALSE: the cycle is not forced, because
(5.7) relates only S(v) to S(v+60), so S(v) and S(v+120) may overlap and S may
take 2-element values.  The exhaustive counts below (N=6: 234 T-confined fields,
132 non-binary, only 6 of them 3-cycles) refute the strong form and leave the
correct statement, which is the negative one used in the exposition: the triple
case reduces to a *non-rigid* combinatorial object (a 60-degree-disjoint field of
nonempty subsets of a 3-set), so no argument at the palette-constraint level can
close k=6.  The k=5 pair analogue IS rigid (2 fields, both binary, both the
2-periodic alternation (5.8)), which is exactly why the five-label proof closes.
"""
import itertools, json

def fields_T(N, T, sizes):
    step = N // 6
    subs = [frozenset(s) for r in sizes for s in itertools.combinations(sorted(T), r)]
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

def is_binary(f, T):
    return [ (i,j) for i in range(3) for j in range(i+1,3)
             if all(f[t] & {i,j} for t in range(len(f))) ]

def is_3cycle(f, T):
    step = len(f)//6
    n = len(f)
    return all(len(f[t]) == 1 and len(f[(t+step) % n]) == 1 and len(f[(t+2*step) % n]) == 1
               and f[t] | f[(t+step) % n] | f[(t+2*step) % n] == frozenset(T) for t in range(n))

res = {"T": [0,1,2], "spaces": []}
T = (0,1,2)
for N in (6,12):
    for sizes in ((1,2,3),(2,3),(1,),(2,),(3,)):
        F = fields_T(N, T, sizes)
        nb = [f for f in F if not is_binary(f, T)]
        cyc = [f for f in nb if is_3cycle(f, T)]
        res["spaces"].append({"N": N, "sizes": list(sizes), "fields": len(F),
                              "nonbinary": len(nb), "nonbinary_and_3cycle": len(cyc),
                              "dichotomy_holds": len(nb) == len(cyc)})
# periodicity of the 3-cycle branch: l(v+180)=l(v), l(v+60)!=l(v)
N = 12; step = 2
cyc = [f for f in fields_T(N, T, (1,)) if is_3cycle(f, T)]
res["cycle_branch"] = {
    "period_180_holds": all(f[t] == f[(t+3*step) % N] for f in cyc for t in range(N)),
    "consecutive_distinct_holds": all(f[t] != f[(t+step) % N] for f in cyc for t in range(N)),
    "example": [sorted(s) for s in cyc[0]] if cyc else None}
# k = 5 analogue: T a pair.  (5.7) leaves only the 2-step alternation.
T5 = (0,1); N = 6
F5 = [f for f in itertools.product([frozenset({0}),frozenset({1}),frozenset({0,1})], repeat=N)
      if all(not (f[t] & f[(t+1) % N]) for t in range(N))]
res["k5_pair_analogue"] = {
    "fields_with_nonempty_pair_meet": len(F5),
    "all_are_binary_for_the_pair": all(all(f[t] & {0,1} for t in range(N)) for f in F5),
    "all_alternate_2periodically": all(
        (f[t] == frozenset({0}) and f[(t+1)%N] == frozenset({1})) or
        (f[t] == frozenset({1}) and f[(t+1)%N] == frozenset({0}))
        for f in F5 if all(len(s)==1 for s in f) for t in range(N)),
}
print(json.dumps(res, indent=1, sort_keys=True))
