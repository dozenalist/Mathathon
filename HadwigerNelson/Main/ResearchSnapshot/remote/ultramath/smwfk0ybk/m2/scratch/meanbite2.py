import sys, itertools; sys.path.insert(0,'.')
from indep import geometry, admissible, POP
from indep2 import dp_sat
def pred(ps):
    return sum(1 for p in ps if POP[p]==3) >= 4 and sum(POP[p] for p in ps)*2 <= 30
for ell in range(3,7):
    n=0; ex=None
    for t in itertools.product(range(6), repeat=ell-1):
        c=(0,)+t
        m=dp_sat(ell,c,pred)
        if m is not None:
            n+=1
            if ex is None: ex=(c,[[i for i in range(6) if (p>>i)&1] for p in m])
    print(f'l={ell}: geometries with a (C1,C2,C3) model that has >=4 ternary AND mean <= 5/2 : {n}')
    if ex: print('   first:', ex)
