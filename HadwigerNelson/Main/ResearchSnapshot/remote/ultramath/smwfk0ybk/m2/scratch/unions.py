import sys, itertools; sys.path.insert(0,'.')
from indep import geometry, admissible, search, POP, bits, FULL
def pred_full(ps): return (ps[0]|ps[1]|ps[2]|ps[3]|ps[4]|ps[5]) == FULL
for ell in range(3,7):
    sat=full=0; ex=None
    for t in itertools.product(range(6), repeat=ell-1):
        c=(0,)+t
        adm=admissible(geometry(ell,c))
        if any(not a for a in adm): continue
        m4=search(adm, lambda ps: not any(POP[ps[a]]==3==POP[ps[b]] and (ps[a]|ps[b])==FULL
                                          for a in range(6) for b in range(a+1,6)))
        if m4 is None: continue
        sat+=1
        mf=search(adm, lambda ps: (lambda u: u==FULL)(ps[0]|ps[1]|ps[2]|ps[3]|ps[4]|ps[5]))
        if mf is not None:
            full+=1
            if ex is None: ex=(c,[bits(p) for p in mf])
    print(f'l={ell}: (C1)-(C4) sat geometries {sat}; of those with a survivor using ALL 6 labels: {full}', 'first: '+str(ex) if ex else '')
