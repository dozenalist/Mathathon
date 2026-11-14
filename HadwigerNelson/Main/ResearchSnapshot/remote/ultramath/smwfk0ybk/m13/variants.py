"""Which palette-size window is decisive at k=6?  For each window [lo,hi] decide the
six-palette CSP (C2),(C3) [+ optional (C4),(C5)] over all 6^l ray geometries."""
from itertools import product, combinations
import sys
sys.path.insert(0,"../../smwfhd5sl/m5")
import interface_csp as m5
from profile2 import sign_word, slivers

K=6

def adm(k,O,I,lo,hi):
    return [frozenset(s) for r in range(lo,hi+1) for s in combinations(range(k),r)
            if set(s)&O and set(s)&I]

def exists(ell,k,c,lo,hi,tight):
    sl=slivers(ell,k,sign_word(ell,c))
    A=[adm(k,O,I,lo,hi) for (O,I) in sl]
    if any(not a for a in A): return None
    full=frozenset(range(k)); cur=[]
    def rec(i):
        if i==6:
            if cur[5]&cur[0]: return False
            if tight:
                t=[p for p in cur if len(p)==3]
                if len(t)>3: return False
                for a in range(len(t)):
                    for b in range(a+1,len(t)):
                        if (t[a]|t[b])==full: return False
            return True
        for q in A[i]:
            if i and (q&cur[i-1]): continue
            cur.append(q)
            if rec(i+1): return True
            cur.pop()
        return False
    return [sorted(p) for p in cur] if rec(0) else None

if __name__=="__main__":
    for lo,hi in ((1,3),(2,3),(3,3),(1,2)):
        for tight in (False,True):
            line=[]
            for ell in range(3,K+1):
                s=0; first=None
                for c in product(range(6),repeat=ell):
                    m=exists(ell,K,c,lo,hi,tight)
                    if m is not None:
                        s+=1
                        if first is None: first={"cells":list(c),"palettes":m}
                line.append((ell,s,6**ell,first))
            print(f"window |P| in [{lo},{hi}]  (C4,C5)={'on' if tight else 'off'}")
            for ell,s,t,first in line:
                print(f"   l={ell}: {s}/{t}   first={first}")
            print(flush=True)
