from itertools import combinations
k=6
def bits(m): return tuple(x for x in range(k) if (m>>x)&1)
def msk(t):
    m=0
    for x in t: m|=1<<x
    return m
i=0
A=[]
for c in combinations([x for x in range(k) if x!=i],2):
    m=msk(c)
    if all((m & ~((1<<j)|(1<<((j+1)%6))))!=0 for j in range(6)): A.append(m)
trans={a:[b for b in A if not(a&b)] for a in A}
res=[]
def rec(p):
    if len(p)==6:
        if not(p[5]&p[0]): res.append(tuple(p))
        return
    for b in trans[p[-1]]: rec(p+[b])
for a in A: rec([a])
print("total",len(res))
from collections import Counter
def typ(w):
    if w[0]==w[2]==w[4] and w[1]==w[3]==w[5]: return "p2"
    if w[0]==w[3] and w[1]==w[4] and w[2]==w[5]: return "p3"
    return "o"
print(Counter(typ(w) for w in res))
# how many have all adjacent pairs disjoint (should be all) and all avoid 0 (by construction)
# look for invariant: maybe P_j and P_{j+2} always intersect? or union?
for w in [w for w in res if typ(w)=="o"][:20]:
    print([bits(m) for m in w])
