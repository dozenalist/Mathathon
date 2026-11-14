import numpy as np
r=0.4; d=np.sqrt(3)*r; w=np.exp(2j*np.pi/3)
idx=np.arange(-8,9)
P=d*(idx[:,None]+idx[None,:]*w); P=P.ravel()
mm=(idx[:,None]*np.ones_like(idx)[None,:]).ravel()
nn=(np.ones_like(idx)[:,None]*idx[None,:]).ravel()
def colour(q):
    q=np.atleast_1d(np.asarray(q,dtype=complex))
    out=np.empty(q.shape,dtype=int)
    for k in range(q.size):
        j=np.argmin(np.abs(P-q[k])); out[k]=(mm[j]+2*nn[j])%7
    return out
# distance from a point to the boundary of its Voronoi cell (hexagon)
def margin(p):
    dl=[abs(p-d*(m+n*w)) for (m,n) in [(1,0),(-1,0),(0,1),(0,-1),(1,-1),(-1,1)]]
    return (min(dl)-abs(p))/2.0   # distance to bisector of nearest neighbour... approximate inradius margin
def annulus_colours(p0, eps, nang=4000, nr=5):
    cs=set()
    th=np.arange(nang)*(2*np.pi/nang)
    for rr in np.linspace(1-eps,1+eps,nr):
        cs |= set(colour(p0+rr*np.exp(1j*th)).tolist())
    return cs
# map over the Voronoi cell of 0
inr=np.sqrt(3)*r/2
rows=[]
N=61
for x in np.linspace(-r,r,N):
    for y in np.linspace(-r,r,N):
        p=x+1j*y
        # inside Voronoi cell of 0?
        if any(abs(p-d*(m+n*w))<abs(p)-1e-9 for (m,n) in [(1,0),(-1,0),(0,1),(0,-1),(1,-1),(-1,1)]): continue
        cs=set(colour(p+np.exp(1j*np.arange(3000)*(2*np.pi/3000))).tolist())
        rows.append((len(cs),x,y,sorted(cs)))
import collections
cnt=collections.Counter(r_[0] for r_ in rows)
print("histogram of |T| over", len(rows), "sample centres:", dict(cnt))
# candidates with |T|<=5, sorted by margin
cands=[r_ for r_ in rows if r_[0]<=5]
cands.sort(key=lambda t:-margin(complex(t[1],t[2])))
print("num candidates with |T|<=5:", len(cands))
for t in cands[:12]:
    p=complex(t[1],t[2])
    print("  |T|=%d p=%.6f%+.6fi |p|=%.6f margin=%.6f missing=%s"%(t[0],t[1],t[2],abs(p),margin(p),sorted(set(range(7))-set(t[3]))))
