import numpy as np
IA=[(0,10),(30,40),(120,130),(140,150),(250,270),(280,290)]
IB=[(90,110),(180,190),(210,230),(300,310),(330,350)]
def in_set(x, intervals):
    y=np.mod(x,360.0); m=np.zeros(y.shape,dtype=bool)
    for lo,hi in intervals: m |= (y>=lo)&(y<hi)
    return m
def member(W, IA, IB, verbose=False):
    r=np.abs(W); out=np.zeros(W.shape,dtype=bool)
    ok=r<=2.0; beta=np.zeros_like(r)
    mask = ok&(r>1e-12)
    np.arccos(np.clip(r/2,0,1), out=beta, where=mask)
    argw=np.angle(W,deg=True)
    for s in (+1,-1):
        th=argw+s*beta; u=np.exp(1j*np.radians(th)); ph=np.angle(W-u,deg=True)
        good1 = mask&in_set(th,IA)&in_set(ph,IB)
        good2 = mask&in_set(th,IB)&in_set(ph,IA)
        if verbose:
            print("  s=",s,"th=",th,"ph=",ph,"good1",good1,"good2",good2, "inA(th)",in_set(th,IA), "inB(ph)",in_set(ph,IB), "inB(th)",in_set(th,IB),"inA(ph)",in_set(ph,IA))
        out |= good1|good2
    return out
w=np.array([0.26-0.14j])
print(member(w,np.array(IA,dtype=float),np.array(IB,dtype=float),verbose=True))
