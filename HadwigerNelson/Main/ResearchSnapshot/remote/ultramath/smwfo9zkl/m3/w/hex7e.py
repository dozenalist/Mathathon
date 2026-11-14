import numpy as np
r=0.4; d=np.sqrt(3)*r; s3=np.sqrt(3)
def toz(m,n): return d*(m+n*(-0.5+0.5j*s3))
def ab(q):
    z=q/d; b=2*z.imag/s3; a=z.real+b/2; return a,b
NB=[(1,0),(-1,0),(0,1),(0,-1),(1,-1),(-1,1)]
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
def margin(p):   # distance from p to the boundary of the Voronoi cell of 0
    return min((abs(p-toz(m,n))**2-abs(p)**2)/(2*np.sqrt(3)*r) for (m,n) in NB)
th=np.arange(1440)*(2*np.pi/1440)
def ann_T(p,eps,nr=5):
    cs=set()
    for rr in np.linspace(1-eps,1+eps,nr): cs|=set(colour(p+rr*np.exp(1j*th)).tolist())
    return frozenset(cs)
rows=[]
N=45
for x in np.linspace(-r,r,N):
    for y in np.linspace(-r,r,N):
        p=x+1j*y
        if abs(p)>r: continue
        mc=margin(p)
        if mc<0.02: continue
        kH=int(np.atleast_1d(colour(p))[0])
        T=ann_T(p,0.004)
        miss=sorted(set(range(7))-set(T))
        usable=[c for c in miss if c!=kH]
        rows.append((len(usable),len(T),mc,p,kH,miss))
rows.sort(key=lambda t:(-t[0],-t[2]))
print("total centres:",len(rows))
for t in rows[:10]:
    print("  usable=%d |T|=%d margin=%.5f p=%.7f%+.7fi kH=%d missing=%s"%(t[0],t[1],t[2],t[3].real,t[3].imag,t[4],t[5]))
print()
for t in rows[:4]:
    p=t[3]
    print("candidate p=",p,"kH=",t[4],"miss=",t[5])
    for eps in (0.001,0.002,0.004,0.008,0.016):
        T=ann_T(p,eps); print("    eps=%.4f |T|=%d T=%s usable=%s"%(eps,len(T),sorted(T),[c for c in set(range(7))-set(T) if c!=t[4]]))
