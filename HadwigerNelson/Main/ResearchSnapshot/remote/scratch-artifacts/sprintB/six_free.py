"""At a 6-cycle centre at k=6, with self-avoidance: all palettes avoid the centre's colour 0.
Palettes are admissible (size 2..3, not contained in any C6 edge). Is there a 6-letter word
w_0..w_5 on one R-orbit with consecutive disjointness (w_i cap w_{i+1}=empty)?"""
from itertools import combinations, product
K=6
E=[frozenset((j,(j+1)%6)) for j in range(6)]
def adm(S): return 2<=len(S)<=3 and not any(S<=e for e in E)
vals=[]
for r in (2,3):
    for c in combinations([x for x in range(K) if x!=0],r):
        S=frozenset(c)
        if adm(S): vals.append(S)
print("admissible palettes avoiding 0:",len(vals),[sorted(v) for v in vals])
# DFS over 6-letter words with consecutive disjointness including wrap-around
sols=[]
def rec(pref):
    if len(pref)==6:
        if not (pref[5]&pref[0]): sols.append(tuple(pref))
        return
    for v in vals:
        if not (pref[-1]&v): rec(pref+[v])
for v in vals: rec([v])
print("free-label 6-orbit words:",len(sols))
for w in sols[:10]: print("   ",[sorted(x) for x in w])
# Also: minimum number of distinct labels in the union, over all words without the free-label restriction
vals_all=[]
for r in (2,3):
    for c in combinations(range(K),r):
        S=frozenset(c)
        if adm(S): vals_all.append(S)
sols2=[]
def rec2(pref):
    if len(pref)==6:
        if not (pref[5]&pref[0]): sols2.append(tuple(pref))
        return
    for v in vals_all:
        if not (pref[-1]&v): rec2(pref+[v])
for v in vals_all: rec2([v])
unions=sorted(set(len(set().union(*w)) for w in sols2))
print("all 6-orbit words:",len(sols2),"union sizes:",unions)
minu=min(unions)
for w in sols2:
    if len(set().union(*w))==minu:
        print("min-union witness:",[sorted(x) for x in w]); break
