import numpy as np, itertools
# paper's 7-colouring: Voronoi hexagons of triangular lattice, circumradius r=2/5.
# lattice Lambda = d*(Z + Z*omega), omega = exp(2 pi i/3), d = sqrt3 * r  (nearest-neighbour distance)
r = 0.4
d = np.sqrt(3)*r
w  = np.exp(2j*np.pi/3)
# lattice point with index (m,n) is d*(m + n*w); colour = (m + 2n) mod 7
def nearest_index(q):
    # nearest lattice point by brute force over a window
    best=None; bi=None
    q = np.atleast_1d(q)
    out_m = np.zeros(q.shape, dtype=int); out_n=np.zeros(q.shape,dtype=int)
    # coarse window
    M = 12
    idx = np.arange(-M, M+1)
    # do it vectorised per point: build window lattice points
    P = d*(idx[:,None] + idx[None,:]*w)
    P = P.ravel()
    MM = idx[:,None]*np.ones_like(idx)[None,:]
    mm = MM.ravel(); nn = (np.ones_like(idx)[:,None]*idx[None,:]).ravel()
    for k,qq in enumerate(q):
        dd = np.abs(P-qq)
        j = np.argmin(dd)
        out_m[k] = mm[j]; out_n[k]=nn[j]
    return out_m, out_n
def colour(q):
    m,n = nearest_index(q)
    return (m+2*n) % 7
# sanity: check the colouring is proper on random unit pairs
rng = np.random.default_rng(0)
pts = rng.uniform(-3,3,size=(20000,2))
u = rng.uniform(-np.pi,np.pi,size=20000)
q1 = pts[:,0]+1j*pts[:,1]
q2 = q1 + np.exp(1j*u)
c1 = colour(q1); c2 = colour(q2)
print("proper violations on 20000 random unit pairs:", int(np.sum(c1==c2)))
# now: for centre p0 in the Voronoi cell of 0, count colours on the unit circle
def T(p0, nang=20000, radius=1.0):
    th = np.arange(nang)*(2*np.pi/nang)
    return set(colour(p0 + radius*np.exp(1j*th)).tolist())
# enumerate p0 over a grid inside the hexagon (Voronoi cell of 0): inradius = sqrt3 r/2
inr = np.sqrt(3)*r/2
print("inradius", inr, "circumradius", r)
best=(99,None)
for x in np.linspace(-inr,inr,25):
    for y in np.linspace(-inr,inr,25):
        p=x+1j*y
        # inside hexagon <=> in Voronoi cell of 0 : |p| <= r  (for the Voronoi cell, |p|<= r suffices? check dist to neighbours)
        if abs(p) > r: continue
        # check p is in Voronoi cell of 0: all neighbours farther
        ok=True
        for (m,n) in [(1,0),(-1,0),(0,1),(0,-1),(1,-1),(-1,1)]:
            if abs(p - d*(m+n*w)) < abs(p) - 1e-12: ok=False;break
        if not ok: continue
        s = T(p)
        if len(s) < best[0]:
            best=(len(s), p, sorted(s), abs(p))
print("min |T| over grid:", best)
