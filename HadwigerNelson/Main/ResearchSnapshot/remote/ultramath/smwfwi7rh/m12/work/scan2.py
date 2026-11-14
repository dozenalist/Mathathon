import numpy as np, sys
sys.path.insert(0,'work')
from models import words, dirset

def in_set(x, intervals):
    y = np.mod(x,360.0); m=np.zeros(y.shape,dtype=bool)
    for lo,hi in intervals: m |= (y>=lo)&(y<hi)
    return m

def member(W, IA, IB):
    r=np.abs(W); out=np.zeros(W.shape,dtype=bool)
    ok = r<=2.0
    beta=np.zeros_like(r)
    np.arccos(np.clip(r/2,0,1), out=beta, where=ok&(r>1e-12))
    argw=np.angle(W,deg=True)
    for s in (+1,-1):
        th=argw+s*beta
        u=np.exp(1j*np.radians(th))
        ph=np.angle(W-u,deg=True)
        out |= ok&(r>1e-12)&in_set(th,IA)&in_set(ph,IB)
        out |= ok&(r>1e-12)&in_set(th,IB)&in_set(ph,IA)
    return out

def find_tri(name,A,B,step=0.02,R=2.02):
    n,word=words()[name]
    IA=dirset(n,word,frozenset(A)); IB=dirset(n,word,frozenset(B))
    xs=np.arange(-R,R,step); ys=np.arange(-R,R,step)
    # grid index i <-> x, j <-> y  (explicit, no meshgrid confusion)
    X=xs[:,None]+0j*ys[None,:]; Y=0j*xs[:,None]+ys[None,:]; Z=X+1j*Y   # Z[i,j] = xs[i] + i*ys[j]
    M=member(Z,IA,IB)
    print(f"{name} {sorted(A)} {sorted(B)}: filled={M.mean():.4f}")
    def shift(M,dy,dx):
        out=np.zeros_like(M)
        j0=max(0,dy); j1=M.shape[1]+min(0,dy); i0=max(0,dx); i1=M.shape[0]+min(0,dx)
        out[i0:i1, j0:j1] = M[i0-dx:i1-dx, j0-dy:j1-dy]
        return out
    for k in range(1440):
        ang=2*np.pi*k/1440; u=np.exp(1j*ang); v=u*np.exp(1j*np.pi/3)
        di=int(round(u.real/step)); dj=int(round(u.imag/step))
        dvi=int(round(v.real/step)); dvj=int(round(v.imag/step))
        T=M & shift(M,dj,di) & shift(M,dvj,dvi)
        if T.any():
            i,j=np.argwhere(T)[0]
            z0=xs[i]+1j*ys[j]
            print("   UNIT TRIANGLE (grid):", np.round([z0,z0+u,z0+v],4), " edge-dirs deg:",round(np.degrees(ang),2))
            return (z0,u,v)
    print("   no triangle at this grid")
    return None

for name,A,B in [("free_l6",{1,4},{2,5}),("free_l6",{1,4},{3,5}),("free_l6",{1,3},{2,4,5}),
                 ("sing_l3",{4},{5}),("free_l3",{3},{4})]:
    find_tri(name,A,B)
