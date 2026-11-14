import sys, itertools; sys.path.insert(0,'.')
from indep import geometry, admissible, search, POP, FULL, bits
def pred(ps):
    if any(POP[ps[a]]==3==POP[ps[b]] and (ps[a]|ps[b])==FULL for a in range(6) for b in range(a+1,6)): return False
    return sum(1 for p in ps if POP[p]==3)==3 and (ps[0]|ps[1]|ps[2]|ps[3]|ps[4]|ps[5])==FULL
for ell in range(3,7):
    n=0; ex=None
    for t in itertools.product(range(6),repeat=ell-1):
        c=(0,)+t
        adm=admissible(geometry(ell,c))
        if any(not a for a in adm): continue
        m=search(adm,pred)
        if m is not None:
            n+=1
            if ex is None: ex=(c,[bits(p) for p in m])
    print(f'l={ell}: geometries with a survivor having exactly 3 ternary AND all 6 labels: {n}  ex={ex}')
