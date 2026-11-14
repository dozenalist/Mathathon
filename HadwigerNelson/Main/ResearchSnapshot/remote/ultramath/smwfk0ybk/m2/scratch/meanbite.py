import sys; sys.path.insert(0,'.')
from indep import geometry, admissible, POP, FULL
import itertools
def search_min_mean(ell, c, need_four):
    adm = admissible(geometry(ell, c))
    if any(not a for a in adm): return None
    best = [None]
    ps=[]
    def bt(i):
        if i==6:
            if ps[5]&ps[0]: return
            t=sum(1 for p in ps if POP[p]==3)
            if need_four and t<4: return
            s=sum(POP[p] for p in ps)
            if best[0] is None or s<best[0][0]: best[0]=(s,list(ps))
            return
        for q in adm[i]:
            if ps and q&ps[-1]: continue
            ps.append(q); bt(i+1); ps.pop()
    bt(0)
    return best[0]
for ell in range(3,7):
    n_any=n_bite=0; ex=None
    for t in itertools.product(range(6), repeat=ell-1):
        c=(0,)+t
        r=search_min_mean(ell,c,True)
        if r is None: continue
        n_any+=1
        if 2*r[0] <= 6*5:   # mean = s/6 <= 5/2  <=> 2s <= 30
            n_bite+=1
            if ex is None: ex=(c,r)
    print(f'l={ell}: geometries with a 4-ternary model {n_any}; of those, one with mean<=5/2: {n_bite}', ex)
