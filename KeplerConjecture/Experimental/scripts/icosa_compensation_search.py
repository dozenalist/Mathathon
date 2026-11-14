"""
Does a saturated completion of the icosahedral 13-cluster violate (T')?

(T') needs  sum_{i=1..12} vol Omega(w_i) >= 13*sqrt(32) - V_dodeca = 67.9888142149.

ONE-SIDED LOGIC: a computed sum for a FINITE completion is an UPPER bound for that
completion (adding centres only shrinks cells).  So a computed sum BELOW the threshold
REFUTES (T').  A sum above it proves nothing.  Status: exploratory, TESTED_FINITE.
"""
import numpy as np, json, sys
from scipy.spatial import Voronoi, ConvexHull, cKDTree
from scipy.spatial.distance import pdist

R32=float(np.sqrt(32)); VDODE=5.5502910285155105
THRESH=13*R32-VDODE

def icosa12():
    phi=(1+5**0.5)/2
    V=[]
    for s1 in (1,-1):
        for s2 in (1,-1):
            V += [[0,s1,s2*phi],[s1,s2*phi,0],[s1*phi,0,s2]]
    V=np.array(V,float); V=V/np.linalg.norm(V[0])*2.0
    return np.vstack([[0,0,0],V])

def fib_sphere(n):
    i=np.arange(n)+0.5
    z=1-2*i/n; phi=np.arccos(z); th=np.pi*(1+5**0.5)*i
    return np.stack([np.cos(th)*np.sin(phi),np.sin(th)*np.sin(phi),z],1)

def build(core, nmax=900, rmax=7.2, seed=3):
    """greedy 2-separated completion, prioritising points at distance 2 from outer centres."""
    rng=np.random.default_rng(seed)
    outer=core[1:]
    cands=[]
    # shell at distance 2 from each outer centre (most effective shrinkers)
    S=fib_sphere(300)
    for w in outer: cands.append(w+2.0*S)
    # shell at distance 2 from origin
    cands.append(2.0*fib_sphere(300))
    # general filler
    for n in (600,1200,2400,4000):
        u=rng.normal(size=(n,3)); u/=np.linalg.norm(u,axis=1)[:,None]
        r=rmax*rng.random(n)**(1/3)
        cands.append(u*r[:,None])
    cands=np.vstack(cands)
    accepted=[p for p in core]
    tree=cKDTree(np.array(accepted))
    order=rng.permutation(len(cands))
    for idx in order:
        p=cands[idx]
        if np.linalg.norm(p)>rmax: continue
        if tree.query(p)[0] < 2.0-1e-9: continue
        accepted.append(p); tree=cKDTree(np.array(accepted))
        if len(accepted)>=nmax: break
    return np.array(accepted)

def vor_vol(P, R=20.0, nbuf=6000):
    buf=fib_sphere(nbuf)*R
    A=np.vstack([P,buf]); vor=Voronoi(A); vol=np.zeros(len(A))
    for i in range(len(A)):
        ridx=vor.point_region[i]
        if ridx<0: continue
        reg=vor.regions[ridx]
        if -1 in reg or len(reg)<4: continue
        try: vol[i]=ConvexHull(vor.vertices[reg]).volume
        except Exception: vol[i]=0.0
    return vol[:len(P)]

core=icosa12()
best=None
for seed in range(6):
    P=build(core, seed=seed)
    vol=vor_vol(P)
    s12=float(vol[1:13].sum())
    ok=bool(np.min(pdist(P[:200]))>=2.0-1e-9) if len(P)>1 else True
    rec=dict(seed=seed,n=int(len(P)),sum12=s12,mean12=s12/12,
             centre=float(vol[0]),thresh=THRESH,gap=s12-THRESH,
             refuted=bool(s12<THRESH), minsep=float(pdist(P).min()))
    print(json.dumps(rec))
    if best is None or s12<best['sum12']: best=rec
print("\nBEST:",json.dumps(best,indent=1))
print("REFUTED" if best['refuted'] else "not refuted (inconclusive: computed sum is an upper bound)")
open('Experimental/evidence/icosa_compensation_search.txt','w').write(json.dumps(best,indent=1)+"\n")
