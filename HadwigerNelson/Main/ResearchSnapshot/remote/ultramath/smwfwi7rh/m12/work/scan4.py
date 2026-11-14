import numpy as np, sys, itertools
sys.path.insert(0,'work')
from sumtest import member
from fractions import Fraction as F
from orbit_crit import criterion, width
from gamma_crit import PSI_LO, PSI_HI
from models import words, dirset

def true_points(IA,IB,n=40):
    pts=[]
    for lo,hi in IA:
        for a in np.linspace(lo,hi,n):
            for lo2,hi2 in IB:
                for b in np.linspace(lo2,hi2,n):
                    pts.append(np.exp(1j*np.radians(a))+np.exp(1j*np.radians(b)))
    return np.array(pts)

def find_tri(IA,IB,step=0.02,R=2.02,D=720):
    xs=np.arange(-R,R,step); ys=np.arange(-R,R,step)
    Z=xs[:,None]+1j*ys[None,:]
    M=member(Z,np.array(IA),np.array(IB))
    def sh(M,dy,dx):
        out=np.zeros_like(M); i0=max(0,dx); i1=M.shape[0]+min(0,dx); j0=max(0,dy); j1=M.shape[1]+min(0,dy)
        out[i0:i1,j0:j1]=M[i0-dx:i1-dx, j0-dy:j1-dy]; return out
    for k in range(D):
        ang=2*np.pi*k/D; u=np.exp(1j*ang); v=u*np.exp(1j*np.pi/3)
        di=int(round(u.real/step)); dj=int(round(u.imag/step)); ei=int(round(v.real/step)); ej=int(round(v.imag/step))
        T=M & sh(M,dj,di) & sh(M,ej,ei)
        if T.any():
            i,j=np.argwhere(T)[0]; z0=xs[i]+1j*ys[j]
            return float(M.mean()), [z0,z0+u,z0+v]
    return float(M.mean()), None

# sanity: true positives
IA=[(0,10),(30,40),(120,130),(140,150),(250,270),(280,290)]
IB=[(90,110),(180,190),(210,230),(300,310),(330,350)]
P=true_points(IA,IB,15)
print("true positives test: all member =", bool(member(P,np.array(IA),np.array(IB)).all()), "of", len(P))

print()
W=words()
tests=[("block_l6",{0,3},{1,4}),("block_l4",{0,2},{1,4}),("block_l5",{0,2},{1,3}),
       ("free_l6",{3,5},{2,4}),("free_l6",{2,5},{1,4}),("free_l6",{1,4},{2,5}),("free_l6",{1,4},{3,5}),
       ("free_l6",{1,3},{2,4,5}),("free_l3",{3},{4}),("sing_l3",{4},{5})]
for name,A,B in tests:
    n,word=W[name]
    IA=dirset(n,word,frozenset(A)); IB=dirset(n,word,frozenset(B))
    w1,w2=criterion([(F(a),F(b)) for a,b in IA],[(F(a),F(b)) for a,b in IB],PSI_LO,PSI_HI)
    fill,t=find_tri(IA,IB)
    print("%-11s A=%-9s B=%-9s T'=%d  gamma=%-6s filled=%.4f  triangle=%s"%(
        name,sorted(A),sorted(B),6-len(set(A)|set(B)),
        "FIRE" if (width(w1)>0 or width(w2)>0) else "silent", fill,
        "YES "+str(np.round(t,4)) if t is not None else "no"))
