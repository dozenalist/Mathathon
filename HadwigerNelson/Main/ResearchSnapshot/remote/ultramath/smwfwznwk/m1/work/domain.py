from itertools import combinations
K=6
E=[frozenset((j,(j+1)%K)) for j in range(K)]
def adm(S): return 1<=len(S)<=3 and not any(S<=e for e in E)
vals=[]
for r in (2,3):
    for c in combinations(range(1,K),r):
        S=frozenset(c)
        if adm(S): vals.append(S)
print("domain size",len(vals))
for i,S in enumerate(vals): print(i,sorted(S),len(S))
print()
pairs=[S for S in vals if len(S)==2]
print("pairs:",[sorted(S) for S in pairs])
print()
# disjointness graph among pairs
idx={S:i for i,S in enumerate(pairs)}
print("disjointness edges:")
deg={i:0 for i in range(len(pairs))}
for a,b in combinations(range(len(pairs)),2):
    if not (pairs[a]&pairs[b]):
        print(" ",sorted(pairs[a]),"--",sorted(pairs[b]))
        deg[a]+=1; deg[b]+=1
print("degrees",[ (sorted(pairs[i]),deg[i]) for i in range(len(pairs))])
# triples
trip=[S for S in vals if len(S)==3]
print()
print("triples and their compatible values:")
for T in trip:
    comp=[S for S in vals if not (S&T)]
    print(" ",sorted(T),"->",[sorted(S) for S in comp])
