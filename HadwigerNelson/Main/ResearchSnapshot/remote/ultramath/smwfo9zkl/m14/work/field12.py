"""
Full direction-local system on the 12 cells of the direction circle.

Cells i=0..11: open arcs (30i,30i+30) degrees.  R = rotation by 60 degrees: cell i -> cell i+2.
Constraints on P_0..P_11 (bitmasks over k labels):
  (F1) 1 <= |P_i| <= k-3                    palette bound, Prop 5.6 generalised
  (F2) P_i cap P_{i+2} = empty              (5.7) at every direction
  (F3) P_i cup P_j != Fin k for j != i+6    (5.2) non-coverage at every non-parallel pair
  (F4) P_i meets O_i and I_i                (8.1) sliver hits at every direction
Verdict per (k,l,c).  Exact integer arithmetic.
"""
import itertools
from fieldlib import OI, palettes, mask_of, bitnames

FULL = {}
def full(k): 
    if k not in FULL: FULL[k] = (1<<k)-1
    return FULL[k]

def build(k,l,c):
    data=[OI(k,l,c,i) for i in range(12)]
    P=palettes(k)
    hits=[]
    for (O,I) in data:
        om,im=mask_of(O),mask_of(I)
        hits.append([p for p in P if (p&om) and (p&im)])
    return data,hits

def sat12(k,l,c,want=False):
    data,hits=build(k,l,c)
    if any(len(h)==0 for h in hits): return (False,None) if want else False
    FULLk=full(k)
    sol=[0]*12
    def ok(t,p):
        # (F2) with t-2
        if t>=2 and (p & sol[t-2]): return False
        # (F3) with all earlier cells except the antipode
        for u in range(t):
            if (u-t) % 12 == 6: continue
            if (p | sol[u]) == FULLk: return False
        return True
    def dfs(t):
        if t==12:
            # close the cycle: (F2) between 10,11 and 0,1 ; and 11-0, 11-1 for (F3)
            if sol[11] & sol[1]: return False
            if sol[10] & sol[0]: return False
            for u in range(12):
                pass
            return True
        for p in hits[t]:
            if ok(t,p):
                sol[t]=p
                if dfs(t+1): return True
        return False
    for p0 in hits[0]:
        sol[0]=p0
        if dfs(1):
            return (True,[bitnames(k,q) for q in sol]) if want else True
    return (False,None) if want else False
