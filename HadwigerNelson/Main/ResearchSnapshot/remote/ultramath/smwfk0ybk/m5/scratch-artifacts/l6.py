import time
from itertools import product
from csp_nogo import decisive, allowed, witness_alts, POP, tighten
t0=time.time(); k,l=6,6; total=sat=0; first=None
for c in product(range(6), repeat=l):
    total+=1
    m=decisive(l,k,c)
    if m is not None:
        sat+=1
        if first is None: first=(c,[[t for t in range(k) if (p>>t)&1] for p in m])
print(f"k=6 l=6 tightened (C1)-(C5): {sat}/{total} satisfiable, {time.time()-t0:.1f}s")
print("first witness cells",first[0],"palettes",first[1])
