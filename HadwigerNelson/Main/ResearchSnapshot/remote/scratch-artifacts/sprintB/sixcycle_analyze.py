from itertools import combinations
k=6
def pc(m): return bin(m).count('1')
def bits(m): return tuple(x for x in range(k) if (m>>x)&1)
def msk(t):
    m=0
    for x in t: m|=1<<x
    return m
# regenerate ell=6 words
A=[]
for c in combinations(range(k),2):
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
# classify: period 2 (P0=P2=P4, P1=P3=P5) ; period 3 (P0=P3,P1=P4,P2=P5) ; other
p2=p3=other=0; oth=[]
for w in res:
    if w[0]==w[2]==w[4] and w[1]==w[3]==w[5]: p2+=1
    elif w[0]==w[3] and w[1]==w[4] and w[2]==w[5]: p3+=1
    else:
        other+=1; oth.append(w)
print("period2",p2,"period3",p3,"other",other)
for w in oth[:15]: print("  ",[bits(m) for m in w])
# check 3-periodic disjoint pairs covering Fin6
cov=0
for w in res:
    if w[0]==w[3] and w[1]==w[4] and w[2]==w[5]:
        if (w[0]|w[1]|w[2])==63 and not(w[0]&w[1]) and not(w[1]&w[2]) and not(w[0]&w[2]): cov+=1
print("3-periodic disjoint covering pairs words:",cov)
# distribution of patterns
from collections import Counter
print(Counter(("p2" if (w[0]==w[2]==w[4] and w[1]==w[3]==w[5]) else ("p3" if (w[0]==w[3] and w[1]==w[4] and w[2]==w[5]) else "o")) for w in res))
