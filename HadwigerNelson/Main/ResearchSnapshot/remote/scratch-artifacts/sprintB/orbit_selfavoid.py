"""Single-centre R-orbit words at k=6 with the self-avoidance constraints.
i = colour of the centre x (x typical).
(SA) P_j avoids i.
(SA2') if |P_j|=3 then |P_{j+1}|=1.
(SING) if P_j={b} then b not in T_C (cycle label set).
(EDGE) P_j not subset of any cycle edge.
(DISJ) P_j cap P_{j+1}=empty; at most 3 ternary (C2).
"""
from itertools import combinations, product
k=6; FULL=(1<<k)-1

def subsets_of(avail):
    out=[]
    for r in range(1,4):
        for c in combinations(avail,r):
            m=0
            for x in c: m|=1<<x
            out.append(m)
    return out

def allowed(ell, i, edge_ok=True):
    TC=set(range(ell))
    avail=[x for x in range(k) if x!=i]
    base=subsets_of(avail)
    A=[]
    for P in base:
        if edge_ok:
            ok=True
            for j in range(ell):
                e=(1<<j)|(1<<((j+1)%ell))
                if P & ~e == 0: ok=False;break
            if not ok: continue
        A.append(P)
    return A, TC

def words(ell,i):
    A,TC=allowed(ell,i)
    def pc(m): return bin(m).count('1')
    def bits(m): return [x for x in range(k) if (m>>x)&1]
    # transition relation
    trans={}
    for a in A:
        lst=[]
        for b in A:
            if a & b: continue
            if pc(a)==3 and pc(b)!=1: continue      # SA2'
            if pc(b)==1 and bits(b)[0] in TC: continue  # SING
            lst.append(b)
        trans[a]=lst
    res=[]
    # DP with 6-cycle closure
    def rec(pref):
        if len(pref)==6:
            if not (pref[5]&pref[0]): res.append(tuple(pref))
            return
        for b in trans[pref[-1]]:
            rec(pref+[b])
    for a in A:
        rec([a])
    res=[t for t in res if sum(1 for m in t if pc(m)==3)<=3]
    return len(A),res

for ell in (3,4,5,6):
    for i_in in (True,False):
        # i in T_C: use i=0 (symmetry). i notin T_C: use i=ell if ell<6 else impossible
        if i_in: i=0
        else:
            if ell==6: continue
            i=ell
        nA,res=words(ell,i)
        print(f"ell={ell} i={'in T' if i_in else 'outside'}: |A|={nA} words={len(res)}")
        # summarize size patterns
        from collections import Counter
        pat=Counter(tuple(bin(m).count('1') for m in t) for t in res)
        print("   patterns:",dict(list(pat.items())[:8]), "..." if len(pat)>8 else "")
