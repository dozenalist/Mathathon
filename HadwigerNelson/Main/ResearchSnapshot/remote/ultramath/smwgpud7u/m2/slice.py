from check import check
import itertools, sys

def feasible(a3,a4,step=3):
    pts=[]
    for a2 in range(61,300,step):
        for a5 in range(61,300,step):
            al=[0,0,a2,a3,a4,a5]
            if len(set(al))!=5: continue
            if not check(al): pts.append((a2,a5))
    return pts

for (a3,a4) in [(120,240),(150,210),(130,200),(120,180),(180,240),(140,190),(125,235)]:
    P=feasible(a3,a4)
    if not P:
        print(f'a3={a3} a4={a4}: EMPTY'); continue
    a2s=sorted({p[0] for p in P}); a5s=sorted({p[1] for p in P})
    print(f'a3={a3} a4={a4}: n={len(P)}  a2 range [{min(a2s)},{max(a2s)}] a5 range [{min(a5s)},{max(a5s)}]')
