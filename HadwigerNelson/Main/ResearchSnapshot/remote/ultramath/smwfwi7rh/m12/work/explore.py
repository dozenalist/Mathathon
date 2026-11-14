import numpy as np, itertools, json
from math import pi, cos, sin

# sector fields: word of length n, sector i = [i*360/n, (i+1)*360/n) degrees
def models():
    M = {}
    # m15 uniform 3-block: Delta=2pi/(6m), L=2m/3 ; m=6 -> n=36 sectors, L=4 sectors per block
    # block index = floor(i/L) mod 3
    for (name, blocks) in [
        ("block_l3", [frozenset({0,3}), frozenset({1,4}), frozenset({2,5})]),
        ("block_l4", [frozenset({0,2}), frozenset({1,4}), frozenset({3,5})]),
        ("block_l5", [frozenset({0,2}), frozenset({1,3}), frozenset({4,5})]),
        ("block_l6", [frozenset({0,3}), frozenset({1,4}), frozenset({2,5})]),
        ("free_l3",  [frozenset({3}),    frozenset({4}),    frozenset({5})]),
        ("free_l4",  [frozenset({0,2}),  frozenset({1,3}),  frozenset({4})]),
        ("free_l5",  [frozenset({0,2}),  frozenset({1,3}),  frozenset({5})]),
    ]:
        n=36; L=4
        word=[blocks[(i//L)%3] for i in range(n)]
        M[name]=(n,word)
    # FREE-LABEL ell=6 36-sector word (12-periodic), from sprint/k6/FREE-LABEL.md
    rows=[[ (3,5),(3,5),(2,5),(2,5),(2,4),(2,4),(2,4),(1,4),(1,4),(1,3),(1,3),(1,3)],
          [ (3,5),(3,5),(2,5),(2,5),(2,4,5),(2,4),(2,4),(1,4),(1,4),(1,3),(1,3),(1,3)],
          [ (3,5),(3,5),(2,5),(2,5),(2,4),(2,4),(2,4),(1,4),(1,4),(1,3),(1,3),(1,3)]]
    word=[frozenset(t) for r in rows for t in r]
    assert len(word)==36
    M["free_l6"]=(36,word)
    # m13 singleton triangle model: values {4+s(t)}, s=floor(9t/2pi) mod 3 -> 3 arcs of 120 deg
    n=36
    word=[]
    for i in range(n):
        th = (i+0.5)*2*pi/n
        s = int(np.floor(9*th/(2*pi)))%3
        word.append(frozenset({4+s}))
    M["sing_l3"]=(n,word)
    return M

def dirset(n,word,value,pad=0.0):
    """returns list of (lo,hi) degree intervals where palette == value (half-open sectors), shrunk by pad deg"""
    out=[]; i=0
    while i<n:
        if word[i]==value:
            j=i
            while j+1<n and word[j+1]==value: j+=1
            out.append((i*360.0/n+pad, (j+1)*360.0/n-pad))
            i=j+1
        else: i+=1
    return out

def sample(intervals,step_deg=0.25):
    pts=[]
    for lo,hi in intervals:
        if hi<=lo: continue
        k=lo
        while k<hi:
            pts.append(k); k+=step_deg
        pts.append(hi-1e-9)
    return pts

def sumcloud(A,B,step=0.25):
    a=np.radians(np.array(sample(A,step))); b=np.radians(np.array(sample(B,step)))
    za=np.exp(1j*a); zb=np.exp(1j*b)
    Z=(za[:,None]+zb[None,:]).ravel()
    return Z

def find_triangles(Z,tol=0.02):
    """search for unit equilateral triangle in point cloud Z"""
    # hash grid
    cell=0.05
    from collections import defaultdict
    grid=defaultdict(list)
    for idx,z in enumerate(Z):
        grid[(int(np.floor(z.real/cell)),int(np.floor(z.imag/cell)))].append(idx)
    def near(q,r):
        out=[]
        cx,cy=int(np.floor(q.real/cell)),int(np.floor(q.imag/cell))
        m=int(np.ceil(r/cell))
        for dx in range(-m,m+1):
            for dy in range(-m,m+1):
                for idx in grid.get((cx+dx,cy+dy),()):
                    if abs(Z[idx]-q)<=r: out.append(idx)
        return out
    hits=[]
    n=len(Z)
    # candidate pairs at distance near 1
    for i in range(n):
        for j in near(Z[i],1.02):
            if j<=i: continue
            d=Z[j]-Z[i]
            if abs(abs(d)-1)>tol: continue
            for sgn in (1,-1):
                w=Z[i]+d*np.exp(1j*sgn*pi/3)
                if near(w,tol):
                    hits.append((i,j,sgn))
                    return hits
    return hits

if __name__=="__main__":
    M=models()
    for name,(n,word) in M.items():
        vals=sorted(set(word), key=lambda s:(len(s),sorted(s)))
        print("="*70); print(name,"n=",n,"values=",[sorted(v) for v in vals])
        for A,B in itertools.combinations(vals,2):
            if A & B: continue
            IA=dirset(n,word,A,pad=0.4); IB=dirset(n,word,B,pad=0.4)
            Z=sumcloud(IA,IB,step=0.75)
            hits=find_triangles(Z,tol=0.03)
            union=len(A|B)
            print(f"  A={sorted(A)} B={sorted(B)} |AuB|={union} T'={6-union} |Z|={len(Z)} triangle={'YES' if hits else 'no'}")
