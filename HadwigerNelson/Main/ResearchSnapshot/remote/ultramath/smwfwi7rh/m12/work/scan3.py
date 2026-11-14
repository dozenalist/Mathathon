import numpy as np, sys, itertools
sys.path.insert(0,'work')
from fractions import Fraction as F
from orbit_crit import criterion, width
from gamma_crit import PSI_LO, PSI_HI
WORD = [(0,[1,4]),(1,[1,2,4]),(2,[2,4]),(3,[1,4]),(4,[1,3,4]),(5,[1,3,5]),(6,[2,3,5]),(7,[3,5]),
        (8,[3,5]),(9,[2,5]),(10,[2,5]),(11,[2,4]),(12,[1,4]),(13,[2,4]),(14,[1,4]),(15,[1,3,4]),
        (16,[1,3,4]),(17,[1,3,5]),(18,[2,5]),(19,[3,5]),(20,[2,3,5]),(21,[2,5]),(22,[2,5]),(23,[2,4]),
        (24,[1,3]),(25,[1,4]),(26,[1,4]),(27,[1,3,4]),(28,[1,4]),(29,[1,5]),(30,[2,5]),(31,[3,5]),
        (32,[3,5]),(33,[2,5]),(34,[2,5]),(35,[2,4])]
word=[frozenset(t) for i,t in WORD]
def arcs(val):
    out=[];i=0
    while i<36:
        if word[i]==val:
            j=i
            while j+1<36 and word[j+1]==val: j+=1
            out.append((10*i,10*(j+1))); i=j+1
        else: i+=1
    return out
def in_set(x, intervals):
    y=np.mod(x,360.0); m=np.zeros(y.shape,dtype=bool)
    for lo,hi in intervals: m |= (y>=lo)&(y<hi)
    return m
def member(W, IA, IB):
    r=np.abs(W); out=np.zeros(W.shape,dtype=bool)
    ok=r<=2.0; beta=np.zeros_like(r)
    np.arccos(np.clip(r/2,0,1), out=beta, where=ok&(r>1e-12))
    argw=np.angle(W,deg=True)
    for s in (+1,-1):
        th=argw+s*beta; u=np.exp(1j*np.radians(th)); ph=np.angle(W-u,deg=True)
        out |= ok&(r>1e-12)&in_set(th,IA)&in_set(ph,IB)
        out |= ok&(r>1e-12)&in_set(th,IB)&in_set(ph,IA)
    return out
def tri(IA,IB,step=0.02,R=2.02):
    xs=np.arange(-R,R,step); ys=np.arange(-R,R,step)
    Z=xs[:,None]+1j*ys[None,:]
    M=member(Z,IA,IB)
    def sh(M,dy,dx):
        out=np.zeros_like(M); i0=max(0,dx); i1=M.shape[0]+min(0,dx); j0=max(0,dy); j1=M.shape[1]+min(0,dy)
        out[i0:i1,j0:j1]=M[i0-dx:i1-dx, j0-dy:j1-dy]; return out
    for k in range(720):
        ang=2*np.pi*k/720; u=np.exp(1j*ang); v=u*np.exp(1j*np.pi/3)
        di=int(round(u.real/step)); dj=int(round(u.imag/step)); ei=int(round(v.real/step)); ej=int(round(v.imag/step))
        T=M & sh(M,dj,di) & sh(M,ej,ei)
        if T.any():
            i,j=np.argwhere(T)[0]; z0=xs[i]+1j*ys[j]
            return (float(M.mean()), np.round([z0,z0+u,z0+v],4))
    return (float(M.mean()), None)
vals=sorted(set(word), key=lambda s:(len(s),sorted(s)))
print("distinct values:", [sorted(v) for v in vals])
for A,B in itertools.combinations(vals,2):
    if A&B: continue
    IA=arcs(A); IB=arcs(B)
    w1,w2=criterion([(F(a),F(b)) for a,b in IA],[(F(a),F(b)) for a,b in IB],PSI_LO,PSI_HI)
    fill,t = tri(IA,IB)
    print("A=%-9s B=%-9s |AuB|=%d T'=%d  gamma=%s  filled=%.4f  triangle_in_sum=%s"%(
        sorted(A),sorted(B),len(A|B),6-len(A|B), "FIRE" if (width(w1)>0 or width(w2)>0) else "silent",
        fill, "YES "+str(t) if t is not None else "no"))
