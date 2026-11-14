"""correct membership test: w in E_A + E_B (E_A,E_B unions of arcs, degrees)"""
import numpy as np
def in_set(x, intervals):
    y=np.mod(x,360.0); m=np.zeros(y.shape,dtype=bool)
    for lo,hi in intervals: m |= (y>=lo)&(y<hi)
    return m
def member(W, IA, IB):
    IA=np.array(IA,dtype=float).reshape(-1,2); IB=np.array(IB,dtype=float).reshape(-1,2)
    r=np.abs(W); out=np.zeros(W.shape,dtype=bool)
    mask=(r<=2.0)&(r>1e-12)
    beta=np.zeros_like(r)
    np.arccos(np.clip(r/2,0,1),out=beta,where=mask)
    beta=np.degrees(beta)                     # <-- the fix
    argw=np.angle(W,deg=True)
    for s in (+1,-1):
        th=argw+s*beta
        u=np.exp(1j*np.radians(th))
        ph=np.angle(W-u,deg=True)
        out |= mask&in_set(th,IA)&in_set(ph,IB)
        out |= mask&in_set(th,IB)&in_set(ph,IA)
    return out
def brute_member(w, IA, IB, step=0.01):
    best=9e9
    for lo,hi in IA:
        for a in np.arange(lo,hi,step):
            for lo2,hi2 in IB:
                for b in np.arange(lo2,hi2,step):
                    z=np.exp(1j*np.radians(a))+np.exp(1j*np.radians(b))
                    best=min(best,abs(z-w))
    return best
if __name__=="__main__":
    IA=[(0,10),(30,40),(120,130),(140,150),(250,270),(280,290)]
    IB=[(90,110),(180,190),(210,230),(300,310),(330,350)]
    rng=np.random.default_rng(0)
    pts=[0.26-0.14j, 0.25-0.14j, 1.26-0.14j, -0.5+0.5j, 1.5+0j, 0.6789-0.4321j]
    pts += list(rng.uniform(-2,2,6)+1j*rng.uniform(-2,2,6))
    W=np.array(pts)
    M=member(W,IA,IB)
    for w,m in zip(W,M):
        b=brute_member(w,IA,IB,step=0.02)
        flag = "OK" if (m == (b<0.03)) else "MISMATCH"
        print("%10.4f%+10.4fj  member=%-5s brute_dist=%.4f  %s"%(w.real,w.imag,m,b,flag))
