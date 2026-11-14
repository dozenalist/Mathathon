import sys, numpy as np
from scipy.spatial import cKDTree
from math import pi
sys.path.insert(0,'work')
import explore as E
def cloud(intervals, step_deg):
    pts=[]
    for lo,hi in intervals:
        k=lo
        while k<hi: pts.append(k); k+=step_deg
        pts.append(hi-1e-6)
    return np.exp(1j*np.radians(np.array(pts)))
M=E.models()
name="block_l6"; A=frozenset({0,3}); B=frozenset({1,4})
n,word=M[name]
IA=E.dirset(n,word,A,pad=0.3); IB=E.dirset(n,word,B,pad=0.3)
print("IA",IA,"IB",IB, flush=True)
a=cloud(IA,0.5); b=cloud(IB,0.5)
print("samples",len(a),len(b), flush=True)
Z=(a[:,None]+b[None,:]).ravel()
print("Z",len(Z), flush=True)
uniq=np.unique(np.round(np.c_[Z.real,Z.imag],9),axis=0)
P=uniq[:,0]+1j*uniq[:,1]
print("uniq",len(P), flush=True)
tree=cKDTree(np.c_[P.real,P.imag])
pairs=tree.query_pairs(1.01, output_type='ndarray')
print("pairs",len(pairs), flush=True)
d=P[pairs[:,1]]-P[pairs[:,0]]; ad=np.abs(d); sel=(np.abs(ad-1)<0.01)
print("near-unit pairs",sel.sum(), flush=True)
pairs=pairs[sel]; d=d[sel]
found=0
for (i,j),dv in zip(pairs,d):
    for s in (1,-1):
        w=P[i]+dv*np.exp(1j*s*pi/3)
        dd,ii=tree.query([w.real,w.imag],k=1)
        if dd<0.01:
            print("TRIANGLE:",np.round(P[i],5),np.round(P[j],5),np.round(P[ii],5),"s",s, flush=True); found=1; break
    if found: break
print("done",found, flush=True)
