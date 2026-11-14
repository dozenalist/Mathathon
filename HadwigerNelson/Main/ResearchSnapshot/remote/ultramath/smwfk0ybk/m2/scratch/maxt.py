import sys, itertools; sys.path.insert(0,'.')
from indep import geometry, admissible, POP, FULL, bits
def c4(ps): return not any(POP[ps[a]]==3==POP[ps[b]] and (ps[a]|ps[b])==FULL for a in range(6) for b in range(a+1,6))
def best(ell,c):
    adm=admissible(geometry(ell,c))
    if any(not a for a in adm): return None
    bst=[None]; ps=[]
    def bt(i):
        if i==6:
            if ps[5]&ps[0] or not c4(ps): return
            u=ps[0]|ps[1]|ps[2]|ps[3]|ps[4]|ps[5]
            key=(sum(1 for p in ps if POP[p]==3), bin(u).count('1'))
            if bst[0] is None or key>bst[0][0]: bst[0]=(key,list(ps))
            return
        for q in adm[i]:
            if ps and q&ps[-1]: continue
            ps.append(q); bt(i+1); ps.pop()
    bt(0); return bst[0]
for ell in range(3,7):
    mx=(0,0); ex=None; n3=0
    for t in itertools.product(range(6),repeat=ell-1):
        c=(0,)+t
        r=best(ell,c)
        if r is None: continue
        if r[0][0]==3: n3+=1
        if r[0]>mx: mx=r[0]; ex=(c,[bits(p) for p in r[1]])
    print(f'l={ell}: max (#ternary, #labels used) over survivors = {mx}; geometries admitting 3 ternary: {n3}; example {ex}')
