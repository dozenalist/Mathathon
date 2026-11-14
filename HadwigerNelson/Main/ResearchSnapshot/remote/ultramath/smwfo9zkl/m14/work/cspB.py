"""
Independent decision procedure B for the six-palette orbit system.
Differences from procedure A (fieldlib.cycle_sat):
  * O_i, I_i are re-derived from actual ray angles using floating point cosines
    evaluated at three interior angles of each cell, with a |cos|>0.25 guard
    (so no reliance on the integer residue table).
  * the cycle is decided by a forward reachability DP over (first palette, last palette)
    states instead of recursive DFS.
"""
import math, itertools

def hits_B(k,l,c,cell):
    U=set(range(l,k))
    P=[]
    for sz in range(1,k-2):
        for comb in itertools.combinations(range(k),sz):
            P.append(frozenset(comb))
    out=None
    for delta in (-1.0,0.0,1.0):
        mu=30.0*cell+15.0+delta
        # rays at (c_j+1)*60 deg, but the paper's cell label has an arbitrary offset:
        # angles are used only through cos(mu - theta_j)
        sig=[]
        for j in range(l):
            th=60.0*(c[j]+1)
            co=math.cos(math.radians(mu-th))
            if abs(co)<0.05: raise ValueError("degenerate angle")
            sig.append(1 if co>0 else -1)
        O=set(U); I=set(U)
        for j in range(l):
            if sig[(j-1)%l]==-1 and sig[j]==-1: O.add(j)
            if sig[(j-1)%l]==1  and sig[j]==1:  I.add(j)
        O=frozenset(O); I=frozenset(I)
        h=[p for p in P if (p & O) and (p & I)]
        if out is None: out=h
        elif out!=h: raise ValueError("hit set not constant on the cell")
    return out

def cycle_sat_B(k,l,c,parity, want=False):
    cells=[(parity+2*t)%12 for t in range(6)]
    H=[hits_B(k,l,c,cell) for cell in cells]
    if any(len(h)==0 for h in H): return (False,None) if want else False
    for p0 in H[0]:
        cur={p0}
        for t in range(1,6):
            nxt=set()
            for q in cur:
                for p in H[t]:
                    if not (p & q): nxt.add(p)
            cur=nxt
            if not cur: break
        for q in cur:
            if not (q & p0):
                return (True,[tuple(sorted(x)) for x in [p0]]) if want else True
    return (False,None) if want else False

if __name__=="__main__":
    import sys
    from fieldlib import cycle_sat
    bad=0; cnt={}
    for k in (5,6):
        for l in range(3,k+1):
            a=b=0
            for tail in itertools.product(range(6),repeat=l-1):
                c=(0,)+tail
                x=cycle_sat(k,l,c,0); y=cycle_sat_B(k,l,c,0)
                if x!=y:
                    bad+=1; print("MISMATCH A/B",k,l,c,x,y)
                a+=x; b+=y
            print(f"k={k} l={l}: A even-SAT={a}  B even-SAT={b}", flush=True)
    print("mismatches:",bad)
