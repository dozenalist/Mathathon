"""Structure of the (C4)-surviving models: total counts, size profiles, 2-periodicity. Exact, capped."""
import itertools
K=6; FULL=63; CS=[1,1,-1,-1,-1,1]
MASKS=[x for x in range(1,64) if bin(x).count('1')<=3]
POP={x:bin(x).count('1') for x in MASKS}
def adm_of(ell,c,i):
    sig=[CS[(c[j]+1-i)%6] for j in range(ell)]; U=FULL^((1<<ell)-1); O=I=U
    for j in range(ell):
        if sig[(j-1)%ell]==-1 and sig[j]==-1: O|=1<<j
        if sig[(j-1)%ell]== 1 and sig[j]== 1: I|=1<<j
    return [p for p in MASKS if (p&O) and (p&I)]
def ok4(ps):
    for a in range(6):
        for b in range(a+1,6):
            if POP[ps[a]]==3==POP[ps[b]] and (ps[a]|ps[b])==FULL: return False
    return True
def all_models(ell,c,cap=200000):
    adm=[adm_of(ell,c,i) for i in range(6)]
    if any(not a for a in adm): return []
    out=[]
    ps=[]
    def bt(i):
        if len(out)>cap: return True
        if i==6:
            if ps[5]&ps[0]==0 and ok4(ps): out.append(tuple(ps))
            return False
        for q in adm[i]:
            if ps and q&ps[-1]: continue
            ps.append(q)
            if bt(i+1): return True
            ps.pop()
        return False
    bt(0)
    return out
for ell in (5,6):
    per=nonper=0; sat=0; tot_models=0; structural=set()
    for t in itertools.product(range(6),repeat=ell-1):
        c=(0,)+t
        ms=all_models(ell,c)
        if not ms: continue
        sat+=1; tot_models+=len(ms)
        p2=sum(1 for m in ms if m[0]==m[2]==m[4] and m[1]==m[3]==m[5])
        (per:=per+1) if p2 else (nonper:=nonper+1)
        for m in ms: structural.add(tuple(sorted([POP[x] for x in m],reverse=True)))
    print(f'l={ell}: sat geometries {sat}, with a 2-periodic model {per}, only non-2-periodic {nonper}, total models {tot_models}')
    print('   size profiles of surviving models (sorted desc):', sorted(structural,reverse=True))
