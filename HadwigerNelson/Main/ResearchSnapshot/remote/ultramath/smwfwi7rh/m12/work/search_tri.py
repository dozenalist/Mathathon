import numpy as np, sys
sys.path.insert(0,'work')
from models import words, dirset, member

def scan(name, A, B, step=0.01, R=2.05):
    W = words()[name]; n,word = W
    IA=dirset(n,word,frozenset(A)); IB=dirset(n,word,frozenset(B))
    xs=np.arange(-R,R,step); ys=np.arange(-R,R,step)
    X,Y=np.meshgrid(xs,ys,indexing='ij'); Z=X+1j*Y
    M=member(Z,IA,IB)
    print(f"{name} A={sorted(A)} B={sorted(B)}  |A u B|={len(set(A)|set(B))}  filled={M.mean():.3f}", flush=True)
    # triangles: for each of D directions u, check M & shift(M,+u) & shift(M,+u*e^{i60})
    D=720
    best=None
    Mi=M
    for k in range(D):
        ang=2*np.pi*k/D
        u=np.exp(1j*ang); 
        v=u*np.exp(1j*np.pi/3)
        su=(int(round(u.imag/step)), int(round(u.real/step)))
        sv=(int(round(v.imag/step)), int(round(v.real/step)))
        def shift(M,s):
            out=np.zeros_like(M)
            dy,dx=s
            ys0=max(0,-dy); ye=min(M.shape[0],M.shape[0]-dy)
            xs0=max(0,-dx); xe=min(M.shape[1],M.shape[1]-dx)
            out[ys0:ye,xs0:xe]=M[ys0+dy:ye+dy, xs0+dx:xe+dx]
            return out
        T=Mi & shift(Mi,su) & shift(Mi,sv)
        if T.any():
            idx=np.argwhere(T)[0]
            j,i=idx
            best=(X[j,i],X[j,i]+u,X[j,i]+v); break
    print("   triangle:", "FOUND" if best else "none", 
          [tuple(np.round([w.real,w.imag],3)) for w in best] if best else "", flush=True)
    return best

if __name__=="__main__":
    tests=[("block_l6",{0,3},{1,4}),("block_l4",{0,2},{1,4}),("block_l5",{0,2},{1,3}),("block_l3",{0,3},{1,4}),
           ("free_l6",{3,5},{2,4}),("free_l6",{2,5},{1,4}),("free_l6",{1,3},{2,4,5}),("free_l6",{3,5},{1,4}),
           ("free_l4",{0,2},{1,3}),("free_l5",{0,2},{1,3}),("sing_l3",{4},{5})]
    for name,A,B in tests:
        scan(name,A,B)
