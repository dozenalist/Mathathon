"""Generate the exact block-sum gap constraints for a given cyclic slot order.

slots: list of frozensets of indices sharing one direction (a collision class).
order: cyclic sequence of slot ids (order[0], order[1], ...) -- directions increase.
Gaps h_t = (direction of order[t+1]) - (direction of order[t])  (cyclically, sum 360).
For a set G of indices: the G-points are the slots meeting G; the G-gaps are the
block sums of consecutive h's between consecutive G-slots;  d(a_G) = 360 - max G-gap.
  d > 60   <=> every G-gap < 300      (strict)
  d >= 120 <=> every G-gap <= 240
  d >= 180 <=> every G-gap <= 180
"""
from itertools import permutations
MC = [(0,2,4),(1,3,5)]+[(i,(i+1)%6,(i+3)%6) for i in range(6)]+[(i,(i+1)%6,(i+4)%6) for i in range(6)]
EM = [(0,2,4),(1,3,5),(0,1,3,4),(0,2,3,5),(1,2,4,5)]
PAIRS = [(i,j) for i in range(6) for j in range(i+1,6) if (j-i)%6 in (2,3,4)]

def blocks(order, G):
    """cyclic positions of slots meeting G, and the block index-ranges between them"""
    n=len(order)
    pos=[t for t in range(n) if order[t] & set(G)]
    if len(pos)<=1: return None      # degenerate: d = 0
    out=[]
    for k in range(len(pos)):
        a=pos[k]; b=pos[(k+1)%len(pos)]
        # block = gaps h_a, h_{a+1}, ..., h_{b-1} (cyclic)
        idx=[]; t=a
        while t!=b:
            idx.append(t); t=(t+1)%n
        out.append(tuple(idx))
    return out

def constraints(order):
    """returns (strict_list, nonstrict_list, degenerate_flag) with blocks as index tuples"""
    strict=[]; nonstrict=[]; degen=[]
    for (i,j) in PAIRS:
        b=blocks(order,(i,j))
        if b is None: degen.append(('P1',(i,j))); continue
        for blk in b: strict.append((blk,300,('P1',(i,j))))
    for G in MC:
        b=blocks(order,G)
        if b is None: degen.append(('P2',G)); continue
        for blk in b: nonstrict.append((blk,240,('P2',G)))
    for G in EM:
        b=blocks(order,G)
        if b is None: degen.append(('P3',G)); continue
        for blk in b: nonstrict.append((blk,180,('P3',G)))
    return strict,nonstrict,degen

def fmt(blk):
    return 'h'+'+h'.join(str(t+1) for t in blk) if len(blk)>1 else 'h'+str(blk[0]+1)

def show(slots):
    slots=[frozenset(s) for s in slots]
    anchor=next(k for k,s in enumerate(slots) if 0 in s)
    rest=[s for k,s in enumerate(slots) if k!=anchor]
    print('=== slot 0 =',sorted(slots[anchor]))
    for perm in permutations(rest):
        order=[slots[anchor]]+list(perm)
        st,ns,dg=constraints(order)
        # keep only constraints not implied: just dedupe
        seen=set(); S=[];N=[]
        for blk,bd,src in st:
            if (blk,bd) in seen: continue
            seen.add((blk,bd)); S.append((blk,bd,src))
        seen=set()
        for blk,bd,src in ns:
            if (blk,bd) in seen: continue
            seen.add((blk,bd)); N.append((blk,bd,src))
        cyc=tuple(sorted(tuple(sorted(s)) for s in order))
        lab=' '.join(''.join(map(str,sorted(s))) for s in order)
        print(f'  order {lab}   strict:{len(S)} nonstrict:{len(N)} degenerate:{len(dg)}')
        for blk,bd,src in S: print(f'      {fmt(blk)} < {bd}      [{src}]')
        for blk,bd,src in N: print(f'      {fmt(blk)} <= {bd}     [{src}]')
        if dg: print('      DEGENERATE:',dg)
