import numpy as np
r=0.4; d=np.sqrt(3)*r; s3=np.sqrt(3)
def toz(m,n): return d*(m+n*(-0.5+0.5j*s3))
def ab(q):
    z=q/d; b=2*z.imag/s3; a=z.real+b/2; return a,b
def col(q):
    q=np.asarray(q,dtype=complex); a,b=ab(q)
    m0=np.round(a).astype(int); n0=np.round(b).astype(int)
    best=np.full(q.shape,1e9); bm=np.zeros(q.shape,int); bn=np.zeros(q.shape,int)
    for dm in (-1,0,1,2):
        for dn in (-1,0,1,2):
            m=m0+dm; n=n0+dn; dd=np.abs(q-toz(m,n)); up=dd<best
            best=np.where(up,dd,best); bm=np.where(up,m,bm); bn=np.where(up,n,bn)
    return (bm+2*bn)%7
th=np.arange(20000)*(2*np.pi/20000)
def T_ann(p,eps,nr=9):
    cs=set()
    for rr in np.linspace(1-eps,1+eps,nr): cs|=set(col(p+rr*np.exp(1j*th)).tolist())
    return cs
def epsmax(p, target=3):
    # largest eps (binary search) such that |complement of T| >= target
    lo,hi=0.0,0.25
    if len(set(range(7))-T_ann(p,lo,3))<target: return 0.0
    for _ in range(20):
        mid=(lo+hi)/2
        if len(set(range(7))-T_ann(p,mid))>=target: lo=mid
        else: hi=mid
    return lo
cands=[(2/55,16/55),(-2/55,-16/55),(2/55,17/55),(-2/55,-17/55),(1/55,17/55),(-1/55,-16/55),
       (3/55,16/55),(1/55,16/55),(0,16/55),(2/55,15/55),(4/55,16/55),(2/55,18/55),(1/55,18/55),(3/55,18/55)]
for x,y in cands:
    p=x+1j*y
    if abs(p)>=0.4: 
        print("%.5f%+.5fi  outside circumcircle, skip"% (x,y)); continue
    e=epsmax(p); miss=sorted(set(range(7))-T_ann(p,min(e,0.02)))
    print("p=%+.6f%+.6fi |p|=%.5f  eps_max=%.5f  missing=%s"%(x,y,abs(p),e,miss))
