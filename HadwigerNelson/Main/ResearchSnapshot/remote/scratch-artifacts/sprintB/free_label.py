"""For each cycle length ell, find triples (M0,M1,M2) of pairwise disjoint admissible
palettes whose union omits at least one label (so non-proper self-avoidance can hold).
The m15 block construction then gives an accumulating ell-cycle palette system.
"""
from itertools import combinations
K=6
def edges(ell): return [frozenset((j,(j+1)%ell)) for j in range(ell)]
def admissible(ell):
    out=[]
    for r in range(1,4):
        for c in combinations(range(K),r):
            S=frozenset(c)
            if not any(S<=e for e in edges(ell)): out.append(S)
    return out
for ell in (3,4,5,6):
    A=admissible(ell)
    found=[]
    for M0,M1,M2 in combinations(A,3):
        if M0&M1 or M0&M2 or M1&M2: continue
        U=M0|M1|M2
        free=set(range(K))-U
        if free:
            found.append((M0,M1,M2,sorted(free)))
    print(f"ell={ell}: admissible={len(A)} pairwise-disjoint triples with a free label: {len(found)}")
    for f in found[:8]: print("   ",[sorted(x) if isinstance(x,set) else x for x in f])
