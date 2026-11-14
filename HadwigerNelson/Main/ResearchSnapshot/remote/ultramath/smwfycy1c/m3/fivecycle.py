#!/usr/bin/env python3
"""d3 five-cycle-finite-core: exact brute-force over Z/5Z support lists.

D_i = {i, (i+2) mod 5}.  A list L (subset of Z/5Z) is VALID iff L != {} and
   intersect_{i in L} D_i == {}.
Positions r in Z/6Z (r = rotation R^r a).  Adjacent position lists are disjoint.
Every i in S(r) has a neighbour ((i-1) or (i+1) mod 5) in S(r+1) and in S(r-1).

No floats anywhere; only set/int arithmetic (exact by construction).
"""
import itertools, json, sys

M = 5
def D(i):
    return frozenset(((i % M), ((i + 2) % M)))

def diag_inter(L):
    if not L:
        return None                      # empty list: undefined, excluded
    it = iter(L)
    s = D(next(it))
    for i in it:
        s = s & D(i)
    return s

def valid(L):
    if not L:
        return False
    return len(diag_inter(L)) == 0

def has_adjacent(L):
    s = set(L)
    return any(((i + 1) % M) in s for i in s)

def nbrs(i):
    return {(i - 1) % M, (i + 1) % M}

ALL = [frozenset(c) for k in range(1, M + 1) for c in itertools.combinations(range(M), k)]
VALID = [L for L in ALL if valid(L)]

out = {}

# ---------- basic facts ----------
out['n_subsets_nonempty'] = len(ALL)
out['n_valid_lists'] = len(VALID)
out['valid_lists'] = sorted(sorted(L) for L in VALID)
out['valid_implies_adjacent'] = all(has_adjacent(L) for L in VALID)
# every valid list is an "index-set with empty diagonal intersection";
# the paper's remark: such a list must contain adjacent indices.
out['invalid_with_both_2_4'] = sorted(sorted(L) for L in ALL
                                      if L != frozenset() and {2, 4} <= L and not valid(L))
# the crucial one: is {2,4} itself valid?
out['{2,4}_is_valid'] = valid(frozenset({2, 4}))
out['diag_inter_{2,4}'] = sorted(diag_inter(frozenset({2, 4})))
out['{2,3,4}_is_valid'] = valid(frozenset({2, 3, 4}))
out['valid_lists_containing_2_and_4'] = sorted(sorted(L) for L in VALID if {2, 4} <= L)
out['valid_lists_containing_2_and_4_avoiding_0_1'] = sorted(
    sorted(L) for L in VALID if {2, 4} <= L and not (L & {0, 1}))

# ---------- PART 1: all triples (S0,S1,S5) ----------
triples = []
for S0 in VALID:
    if not ({0, 1} <= S0):
        continue
    for S1 in VALID:
        if S1 & S0:
            continue
        for S5 in VALID:
            if S5 & S0:
                continue
            ok = True
            for i in S0:
                if not (nbrs(i) & S1):
                    ok = False; break
                if not (nbrs(i) & S5):
                    ok = False; break
            if ok:
                triples.append((tuple(sorted(S0)), tuple(sorted(S1)), tuple(sorted(S5))))
out['n_triples'] = len(triples)
out['triples'] = triples
out['hypothesis_set_empty'] = (len(triples) == 0)

def common(which):
    if not triples:
        return None
    s = set(triples[0][which])
    for t in triples:
        s &= set(t[which])
    return sorted(s)

def possible(which):
    p = set()
    for t in triples:
        p |= set(t[which])
    return sorted(p)

out['S0_forced'] = common(0); out['S0_possible'] = possible(0)
out['S1_forced'] = common(1); out['S1_possible'] = possible(1)
out['S5_forced'] = common(2); out['S5_possible'] = possible(2)
out['strongest_conclusion_S1'] = ('S(1) = %s exactly' % (common(1),)) if triples else 'vacuous'

# ---------- PART 2: the j step ----------
# S(3) is valid hence contains an adjacent pair {j,j+1}.  Writing S(3) >= {j,j+1},
# the same neighbour argument gives j-1, j+2 in S(2) (and in S(4)); S(2) must be a
# valid list, and S(2) & S(1) = {} because adjacent position lists are disjoint.

def survivors(reading):
    res = []
    detail = {}
    S1fix = set(out['S1_forced']) if out['S1_forced'] else set()
    for j in range(M):
        a, b = (j - 1) % M, (j + 2) % M
        cands = []
        for S2 in VALID:
            if not ({a, b} <= S2):
                continue
            if reading == 'W':            # paper: uses only 2,4 in S(1)
                if S2 & {2, 4}:
                    continue
            elif reading == 'S':          # full force: S(1) = {2,3,4}
                if S2 & S1fix:
                    continue
            cands.append(tuple(sorted(S2)))
        detail[j] = [a, b, cands]
        if cands:
            res.append(j)
    return res, detail

sW, dW = survivors('W')
sS, dS = survivors('S')
out['j_surviving_weak_reading'] = sW
out['j_detail_weak'] = dW
out['j_surviving_strong_reading'] = sS
out['j_detail_strong'] = dS

# ---------- PART 3: full 6-position configuration, exhaustive DFS ----------
# positions 0..5 cyclic; every list valid; adjacent lists disjoint;
# every index has a neighbour in the position before and after; 0,1 in S(0).
sol = []
def dfs(pos, cur):
    if len(sol) > 4000:
        return
    if pos == 6:
        # closure: S(5) vs S(0)
        if cur[5] & cur[0]:
            return
        for i in cur[5]:
            if not (nbrs(i) & cur[0]):
                return
        for i in cur[0]:
            if not (nbrs(i) & cur[5]):
                return
        sol.append(tuple(tuple(sorted(x)) for x in cur))
        return
    for L in VALID:
        if pos == 0 and not ({0, 1} <= L):
            continue
        if pos > 0 and (L & cur[pos - 1]):
            continue
        if pos > 0:
            if any(not (nbrs(i) & cur[pos - 1]) for i in cur[pos - 1]):
                continue
            if any(not (nbrs(i) & L) for i in cur[pos - 1]):
                continue
        cur.append(L)
        dfs(pos + 1, cur)
        cur.pop()

dfs(0, [])
out['n_full_six_list_configurations'] = len(sol)
out['full_config_examples'] = sol[:3]
out['full_hypothesis_empty'] = (len(sol) == 0)

print(json.dumps(out, indent=1, sort_keys=False))
