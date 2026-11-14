"""Corrected single-centre R-orbit constraints at k=6.
i = colour of centre x (typical, so all palettes avoid i).
(SA2) if |P_j|=3 then |P_{j+1}|<=2.
(MON) if |P_j|+|P_{j+2}|=5 and P_j cap P_{j+2}=empty -> forbidden (unit sum, monochromatic i).
(SING) if |P_j|=1, its label is outside the cycle vertex set V.
(C1) no two palettes in the word are complementary 3-sets.
(C2) at most 3 ternary.
(EDGE) P_j not subset of any cycle edge.
"""
from itertools import combinations
k=6; FULL=(1<<k)-1
def pc(m): return bin(m).count('1')
def bits(m): return tuple(x for x in range(k) if (m>>x)&1)

def words(ell,i,mode='full'):
    V=set(range(ell))
    A=[P for P in [sum(1<<x for x in c) for r in range(1,4) for c in combinations([x for x in range(k) if x!=i],r)]
       if all((P & ~((1<<j)|(1<<((j+1)%ell))))!=0 for j in range(ell))]
    def ok_trans(a,b):
        if a&b: return False
        if pc(a)==3 and pc(b)>2: return False
        if pc(b)==1 and bits(b)[0] in V: return False
        return True
    def ok_word(w):
        if sum(1 for m in w if pc(m)==3)>3: return False
        for j in range(6):
            for d in (1,2,3):
                a,b=w[j],w[(j+d)%6]
                if a==b and d!=3: pass
                # complementary 3-sets anywhere
                if pc(a)==3 and pc(b)==3 and (a&b)==0: return False
            # MON at distance 2
            if pc(w[j])+pc(w[(j+2)%6])==5 and (w[j]&w[(j+2)%6])==0: return False
        return True
    res=[]
    def rec(p):
        if len(p)==6:
            if not ok_trans(p[5],p[0]): return
            if ok_word(p): res.append(tuple(p))
            return
        for b in A:
            if ok_trans(p[-1],b): rec(p+[b])
    for a in A: rec([a])
    return A,res

for ell in (3,4,5,6):
    for i_in in (True,False):
        if i_in: i=0
        else:
            if ell==6: continue
            i=ell
        A,res=words(ell,i)
        from collections import Counter
        pat=Counter(tuple(pc(m) for m in t) for t in res)
        print(f"ell={ell} i={'in' if i_in else 'out'}: |A|={len(A)} words={len(res)}  size-patterns={dict(pat)}")
