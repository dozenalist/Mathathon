"""Do (C4),(C5) prune ANY satisfiable ray geometry at k=6?  Independent implementation."""
import time
from itertools import product
from csp_nogo import allowed, admissible, tighten, POP

def solve(l,k,c,use_tight):
    O,I=allowed(l,k,c); adm=[admissible(k,O[i],I[i]) for i in range(6)]
    if any(not a for a in adm): return None
    sol=[]
    def dfs(i):
        if i==6: return not (sol[5]&sol[0]) and (tighten(k,sol) if use_tight else True)
        for p in adm[i]:
            if i and (p&sol[i-1]): continue
            sol.append(p)
            if dfs(i+1): return True
            sol.pop()
        return False
    for p in adm[0]:
        sol=[p]
        if dfs(1):
            return list(sol)
    return None

t0=time.time()
for l in (3,4,5,6):
    free=tight=0; diff=0; first=None
    for c in product(range(6),repeat=l):
        a=solve(l,6,c,False); b=solve(l,6,c,True)
        if a is not None: free+=1
        if b is not None: tight+=1
        if (a is None)!=(b is None): diff+=1; first=first or c
    print(f"k=6 l={l}: untightened {free}/{6**l}, tightened {tight}/{6**l}, words changed by (C4),(C5): {diff}"
          + (f"  first {first}" if first else ""))
print(f"{time.time()-t0:.1f}s")
