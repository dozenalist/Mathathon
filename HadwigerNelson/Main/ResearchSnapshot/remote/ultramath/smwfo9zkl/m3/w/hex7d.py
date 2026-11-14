import numpy as np
r=0.4; d=np.sqrt(3)*r; s3=np.sqrt(3)
def toz(m,n): return d*(m+n*(-0.5+0.5j*s3))
def ab(q):
    z=q/d; b=2*z.imag/s3; a=z.real+b/2; return a,b
def nearest(q):
    q=np.asarray(q,dtype=complex); a,b=ab(q)
    m0=np.round(a).astype(int); n0=np.round(b).astype(int)
    best=np.full(q.shape,1e9); bm=np.zeros(q.shape,int); bn=np.zeros(q.shape,int)
    for dm in (-1,0,1,2):
        for dn in (-1,0,1,2):
            m=m0+dm; n=n0+dn; dd=np.abs(q-toz(m,n)); upd=dd<best
            best=np.where(upd,dd,best); bm=np.where(upd,m,bm); bn=np.where(upd,n,bn)
    return bm,bn,best
def colour(q):
    m,n,_=nearest(q); return (m+2*n)%7
def margin(p):
    dl=[abs(p-toz(m,n)) for (m,n) in [(1,0),(-1,0),(0,1),(0,-1),(1,-1),(-1,1)]]
    return (min(dl)-abs(p))/2.0
th=np.arange(2880)*(2*np.pi/2880)
def ann_T(p,eps):
    cs=set()
    for rr in np.linspace(1-eps,1+eps,9): cs|=set(colour(p+rr*np.exp(1j*th)).tolist())
    return frozenset(cs)
# fine search
best=[]
N=81
for x in np.linspace(-0.42,0.42,N):
    for y in np.linspace(-0.42,0.42,N):
        p=x+1j*y
        if abs(p)>r: continue
        if any(abs(p-toz(m,n))<abs(p)-1e-9 for (m,n) in [(1,0),(-1,0),(0,1),(0,-1),(1,-1),(-1,1)]): continue
        mg=margin(p)
        if mg<0.09: continue
        T=ann_T(p,0.006)
        kH=int(np.atleast_1d(colour(p))[0])
        miss=sorted(set(range(7))-set(T))
        ok=[c for c in miss if c!=kH]
        if len(ok)>=2: best.append((mg,len(T),p,kH,miss))
best.sort(key=lambda t:(-len(t[4]),-t[0]))
print("candidates (|miss|>=2 and 2 usable + kH safe), top by #missing then margin:")
for b in best[:12]:
    print("  margin=%.5f |T|=%d p=%.7f%+.7fi  colour(H)=%d  missing(all)=%s"%(b[0],b[1],b[2].real,b[2].imag,b[3],b[4]))
# pick the first one and certify
mg,nt,p,kH,miss=best[0]
print()
print("CHOSEN p0 =",repr(p), " |p0|=%.12f"%abs(p))
print("hexagon colour k_H =",kH)
print("annulus colours (eps=0.006) =",sorted(set(range(7))-set(miss)))
print("missing =",miss)
for eps in (0.002,0.004,0.006,0.01,0.02,0.04):
    T=ann_T(p,eps); print("  eps=%.3f  |T|=%d  T=%s"%(eps,len(T),sorted(T)))
