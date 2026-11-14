import sys, itertools; sys.path.insert(0,'.')
from indep import geometry, admissible, search, POP, bits
def pred(ps):
    return sum(1 for p in ps if POP[p]==3) >= 4 and 2*sum(POP[p] for p in ps) <= 30
for ell in range(3,7):
    n=0; ex=None
    for t in itertools.product(range(6), repeat=ell-1):
        c=(0,)+t
        adm=admissible(geometry(ell,c))
        if any(not a for a in adm): continue
        m=search(adm,pred)
        if m is not None:
            n+=1
            if ex is None: ex=(c,[bits(p) for p in m])
    print(f'l={ell}: (C1,C2,C3) models with >=4 ternary and mean <= 5/2 : geometries {n}'); 
    if ex: print('   first:', ex)
