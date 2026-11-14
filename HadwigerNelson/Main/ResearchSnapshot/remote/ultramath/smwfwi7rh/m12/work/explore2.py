import numpy as np, itertools
from scipy.spatial import cKDTree
from math import pi
import explore as E

def cloud(intervals, step_deg):
    pts=[]
    for lo,hi in intervals:
        k=lo
        while k<hi: pts.append(k); k+=step_deg
        pts.append(hi-1e-6)
    return np.exp(1j*np.radians(np.array(pts)))

def tri_in_sum(IA,IB,step=0.5,tol=0.01):
    a=cloud(IA,step); b=cloud(IB,step)
    Z=(a[:,None]+b[None,:]).ravel()
    uniq=np.unique(np.round(np.c_[Z.real,Z.imag],9),axis=0)
    P=uniq[:,0]+1j*uniq[:,1]
    tree=cKDTree(np.c_[P.real,P.imag])
    pairs=tree.query_pairs(1.0+tol, output_type='ndarray')
    d=P[pairs[:,1]]-P[pairs[:,0]]
    ad=np.abs(d)
    sel=(np.abs(ad-1)<tol)
    pairs=pairs[sel]; d=d[sel]
    if len(pairs)==0: return None
    for (i,j),dv in zip(pairs,d):
        for s in (1,-1):
            w=P[i]+dv*np.exp(1j*s*pi/3)
            dd,ii=tree.query([w.real,w.imag],k=1)
            if dd<tol:
                return (P[i],P[j],P[ii],s)
    return None

M=E.models()
tests=[("block_l6",{0,3},{1,4}),("block_l4",{0,2},{1,4}),("block_l5",{0,2},{1,3}),
       ("free_l6",{3,5},{2,4}),("free_l6",{3,5},{1,4}),("free_l6",{2,5},{1,4}),("free_l6",{2,5},{1,3}),
       ("free_l6",{2,4},{1,3}),("free_l6",{1,3},{2,4,5}),("free_l4",{0,2},{1,3}),("free_l5",{0,2},{1,3})]
for name,A,B in tests:
    n,word=M[name]
    A=frozenset(A); B=frozenset(B)
    IA=E.dirset(n,word,A,pad=0.3); IB=E.dirset(n,word,B,pad=0.3)
    r=tri_in_sum(IA,IB,step=0.5,tol=0.01)
    print(f"{name:9s} A={sorted(A)!s:10s} B={sorted(B)!s:10s} |AuB|={len(A|B)} T'={6-len(A|B)}",
          "TRIANGLE" if r else "none", (np.round(r[0],4),np.round(r[1],4),np.round(r[2],4)) if r else "")
