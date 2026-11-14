#!/usr/bin/env python3
"""Audit of the (V)-at-all-positions hypothesis in supervisor/simplify-angular/FIVE-CYCLE-CORE.md.

Model: labels I = Z/5Z, diagonals D_i = {i, i+2}, a list L is VALID iff intersection of D_i is empty.
Positions r in Z/6Z.  Facts:
  (D)  S(r) cap S(r+1) = empty          (paper p.41, all a)
  (N)  every i in S(r) has a neighbour (i+-1) in S(r+1) and in S(r-1)   (paper p.41, all a)
  (R)  0,1 in S(0)                       (paper p.42, after relabelling)
  (V-r) S(r) is valid and nonempty       (proved in the paper ONLY at r = 0 and r = 3)
Question: is (D)+(N)+(R)+(V-0)+(V-3) already unsatisfiable?
"""
from itertools import combinations, product

I = range(5)
D = {i: frozenset({i, (i + 2) % 5}) for i in I}

def valid(L):
    if not L: return False
    inter = None
    for i in L:
        inter = set(D[i]) if inter is None else (inter & set(D[i]))
    return not inter

ALL = [frozenset(c) for k in range(1, 6) for c in combinations(I, k)]
VALID = [L for L in ALL if valid(L)]
print('valid lists (%d):' % len(VALID), sorted(sorted(L) for L in VALID))

def nb(i): return {(i - 1) % 5, (i + 1) % 5}

def ok_D(S):
    return all(not (S[r] & S[(r + 1) % 6]) for r in range(6))

def ok_N(S):
    for r in range(6):
        for i in S[r]:
            if not (nb(i) & S[(r + 1) % 6]): return False
            if not (nb(i) & S[(r - 1) % 6]): return False
    return True

def search(pool_for, require_valid_at, verbose=True):
    """pool_for(r) -> list of admissible lists at position r"""
    sols = []
    pools = [pool_for(r) for r in range(6)]
    def rec(r, S):
        if r == 6:
            if ok_D(S) and ok_N(S): sols.append(dict(S))
            return
        for L in pools[r]:
            S[r] = L
            # prune: (D) with the previous position
            if r > 0 and (S[r] & S[r - 1]): continue
            rec(r + 1, S)
        S.pop(r, None)
    rec(0, {})
    return sols

# --- A. FIVE-CYCLE-CORE's hypotheses: (V) at every position, (R) ---
pool_all_valid = lambda r: [L for L in VALID if (r != 0 or {0, 1} <= L)]
A = search(pool_all_valid, None)
print('\n[A] (V) at all six positions + (D)+(N)+(R): %d solutions' % len(A))

# --- B. the hypotheses the paper actually licenses: (V) only at r = 0 and r = 3 ---
def pool_paper(r):
    if r in (0, 3):  return [L for L in VALID if (r != 0 or {0, 1} <= L)]
    return [L for L in ALL if (r != 0 or {0, 1} <= L)]
B = search(pool_paper, None)
print('[B] (V) only at r=0,3 + (D)+(N)+(R): %d solutions' % len(B))
for s in B[:6]:
    print('   ', {r: sorted(s[r]) for r in range(6)})

# --- C. what if only S(0) is valid (V used at r=0 alone)? ---
def pool_paper2(r):
    if r == 0: return [L for L in VALID if {0, 1} <= L]
    return list(ALL)
C = search(pool_paper2, None)
print('[C] (V) only at r=0 + (D)+(N)+(R): %d solutions' % len(C))
for s in C[:6]:
    print('   ', {r: sorted(s[r]) for r in range(6)})

# --- D. does validity at r=1 need (N)?  check each single failure mode ---
print('\n[E] is {2,4} + (a neighbour-witness for 0 and 1) consistent? samples above show whether')

# --- F. minimality: is dropping validity at a SINGLE position from {1,2,4,5} already fatal? ---
print()
for drop in [1, 2, 4, 5]:
    def pool(r, drop=drop):
        if r in (0, 1, 2, 3, 4, 5) and (r == drop):
            return [L for L in ALL if (r != 0 or {0, 1} <= L)]
        return [L for L in VALID if (r != 0 or {0, 1} <= L)]
    F = search(pool, None)
    print('[F] validity at all positions except r=%d: %d solutions' % (drop, len(F)))
    for s in F[:3]:
        print('    ', {r: sorted(s[r]) for r in range(6)})
