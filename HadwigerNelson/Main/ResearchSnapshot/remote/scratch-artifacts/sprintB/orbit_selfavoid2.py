"""Fixed: enforce the ternary->singleton rule also across the wrap-around."""
from itertools import combinations
k=6; FULL=(1<<k)-1
def subsets_of(avail):
    out=[]
    for r in range(1,4):
        for c in combinations(avail,r):
            m=0
            for x in c: m|=1<<x
            out.append(m)
    return out
def pc(m): return bin(m).count('1')
def bits(m): return [x for x in range(k) if (m>>x)&1]

def words(ell,i):
    TC=set(range(ell))
    A=[P for P in subsets_of([x for x in range(k) if x!=i])
       if all((P & ~((1<<j)|(1<<((j+1)%ell))))!=0 for j in range(ell))]
    trans={}
    for a in A:
        lst=[]
        for b in A:
            if a&b: continue
            if pc(a)==3 and pc(b)!=1: continue
            if pc(b)==1 and bits(b)[0] in TC: continue
            lst.append(b)
        trans[a]=lst
    res=[]
    def rec(pref):
        if len(pref)==6:
            if pref[5]&pref[0]: return
            # wrap-around rules: from P5 to P0
            a,b=pref[5],pref[0]
            if pc(a)==3 and pc(b)!=1: return
            if pc(b)==1 and bits(b)[0] in TC: return
            res.append(tuple(pref)); return
        for b in trans[pref[-1]]:
            rec(pref+[b])
    for a in A: rec([a])
    res=[t for t in res if sum(1 for m in t if pc(m)==3)<=3]
    return A,res

for ell in (3,4,5,6):
    for i_in in (True,False):
        if i_in: i=0
        else:
            if ell==6: continue
            i=ell
        A,res=words(ell,i)
        print(f"ell={ell} i={'in T' if i_in else 'outside'}: |A|={len(A)} words={len(res)}")
        from collections import Counter
        print("   pat:",dict(Counter(tuple(pc(m) for m in t) for t in res)))
        if ell>=5 and res:
            for t in res[:4]: print("    ",[bits(m) for m in t])
