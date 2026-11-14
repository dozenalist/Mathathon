"""Check that for each ell in {3,4,5,6} there is a partition of [6] into three
admissible pairs (each avoiding every edge of C_ell) and that the m15 shift
property holds (block index changes by 1 or 2 mod 3 under the forced offsets).
"""
from itertools import combinations
K=6
def edges(ell): return [frozenset((j,(j+1)%ell)) for j in range(ell)]
def admissible_pairs(ell):
    E=edges(ell)
    return [frozenset(c) for c in combinations(range(K),2) if not any(frozenset(c)<=e for e in E)]
def partitions(ell):
    P=admissible_pairs(ell)
    out=[]
    for a,b,c in combinations(P,3):
        if a|b|c==frozenset(range(K)) and not(a&b) and not(a&c) and not(b&c):
            out.append((a,b,c))
    return out
for ell in (3,4,5,6):
    ps=partitions(ell)
    print(f"ell={ell}: admissible pairs={len(admissible_pairs(ell))}, partitions={len(ps)}")
    for p in ps[:4]: print("   ", [sorted(x) for x in p])
# verify the block-shift property: m >= 6, L=2m/3, shifts m-1,m,m+1 give index change 1 or 2 mod 3
print()
for m in (6,9,12,60):
    L=2*m//3
    ok=True
    for base in (m-1,m,m+1):
        for i in range(6*m):
            for t in (base, -base):
                q=(i+t)%(6*m)
                if ((q//L)-(i//L))%3 not in (1,2): ok=False
    print(f"m={m} L={L}: block-index shift in {{1,2}} mod 3 for all i, offsets +-{{m-1,m,m+1}}: {ok}")
