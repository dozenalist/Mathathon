import numpy as np, collections
r=0.4; d=np.sqrt(3)*r; s3=np.sqrt(3)
# lattice point (m,n) <-> complex d*(m + n*omega), omega=-1/2+i s3/2
def ab(q):   # (a,b) coordinates: q/d = a + b*omega
    z=q/d; b=2*z.imag/s3; a=z.real+b/2; return a,b
def toz(m,n): return d*(m+n*(-0.5+0.5j*s3))
def colour(q):
    q=np.asarray(q,dtype=complex); a,b=ab(q)
    m0=np.round(a).astype(int); n0=np.round(b).astype(int)
    best=np.full(q.shape,1e9); bm=np.zeros(q.shape,int); bn=np.zeros(q.shape,int)
    for dm in (-1,0,1,2):
        for dn in (-1,0,1,2):
            m=m0+dm; n=n0+dn
            dd=np.abs(q-toz(m,n))
            upd=dd<best
            best=np.where(upd,dd,best); bm=np.where(upd,m,bm); bn=np.where(upd,n,bn)
    return (bm+2*bn)%7
# sanity: compare with brute force on random points
idx=np.arange(-8,9); P=d*(idx[:,None]+idx[None,:]*(-0.5+0.5j*s3)); P=P.ravel()
MM=(idx[:,None]*np.ones_like(idx)[None,:]).ravel(); NN=(np.ones_like(idx)[:,None]*idx[None,:]).ravel()
rng=np.random.default_rng(1); Q=rng.uniform(-2,2,3000)+1j*rng.uniform(-2,2,3000)
bf=np.array([ (MM[np.argmin(np.abs(P-q))]+2*NN[np.argmin(np.abs(P-q))])%7 for q in Q])
print("nearest-index method agrees with brute force:", np.all(bf==colour(Q)))
# properness check: many random unit pairs
Q1=rng.uniform(-4,4,200000)+1j*rng.uniform(-4,4,200000); U=np.exp(1j*rng.uniform(-np.pi,np.pi,200000))
print("unit-pair violations (200000 random pairs):", int(np.sum(colour(Q1)==colour(Q1+U))))
# same-colour distance bound: min |z| over z in Lambda with colour(z)==0, z!=0 -> should be sqrt21*r
ts=np.arange(0,2*np.pi,1e-4)
print("sqrt21*r =", np.sqrt(21)*r, "  3r =",3*r)
# colour-set on unit circle over the Voronoi cell of 0
inr=s3*r/2
th=np.arange(1440)*(2*np.pi/1440)
res={}
N=41
pts=[]
for x in np.linspace(-r,r,N):
    for y in np.linspace(-r,r,N):
        p=x+1j*y
        if abs(p)>r: continue
        if any(abs(p-toz(m,n))<abs(p)-1e-9 for (m,n) in [(1,0),(-1,0),(0,1),(0,-1),(1,-1),(-1,1)]): continue
        pts.append(p)
print("sample centres:",len(pts))
def T(p,rads=(1.0,)):
    cs=set()
    for rr in rads: cs|=set(colour(p+rr*np.exp(1j*th)).tolist())
    return frozenset(cs)
cnt=collections.Counter(len(T(p)) for p in pts)
print("histogram |T|:",dict(sorted(cnt.items())))
good=[(len(T(p)),p) for p in pts if len(T(p))<=5]
# margin to hexagon boundary
def margin(p):
    dl=[abs(p-toz(m,n)) for (m,n) in [(1,0),(-1,0),(0,1),(0,-1),(1,-1),(-1,1)]]
    return (min(dl)-abs(p))/2.0
goods=sorted([(margin(p),len(T(p)),p,sorted(set(range(7))-set(T(p)))) for _,p in good],key=lambda t:-t[0])
print("centres with |T|<=5, best margins:")
for g in goods[:15]: print("   margin=%.5f |T|=%d p=%.6f%+.6fi missing=%s"%(g[0],g[1],g[2].real,g[2].imag,g[3]))
