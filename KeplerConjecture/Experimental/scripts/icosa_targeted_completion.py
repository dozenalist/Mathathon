"""
Targeted completion: shrink each outer cell by placing neighbours at distance 2
from each outer centre in its FREE OUTWARD hemisphere.

Geometry used: for outer centre w (|w|=2), each icosahedral neighbour w' satisfies
  w.w' = 4 - |w-w'|^2/2 = 1.788854,   so  cos angle((w'-w), -w/2) = 0.52573  -> 58.3 deg
from the inward direction.  Hence the outward hemisphere about +w/2 (angle < 90 deg)
is free of the six known neighbours.

ONE-SIDED: computed sum for a finite completion is an UPPER bound.  Below the
threshold REFUTES (T'); above it proves nothing.  Status: TESTED_FINITE.
"""
import numpy as np, json
from scipy.spatial import Voronoi, ConvexHull, cKDTree
from scipy.spatial.distance import pdist

R32=float(np.sqrt(32)); VDODE=5.5502910285155105; THRESH=13*R32-VDODE
def icosa12():
    phi=(1+5**0.5)/2; V=[]
    for s1 in (1,-1):
        for s2 in (1,-1):
            V += [[0,s1,s2*phi],[s1,s2*phi,0],[s1*phi,0,s2]]
    V=np.array(V,float); return np.vstack([[0,0,0],V/np.linalg.norm(V[0])*2.0])

def frame(n):
    n=n/np.linalg.norm(n)
    a=np.array([1.,0,0]) if abs(n[0])<0.9 else np.array([0,1.,0])
    e1=np.cross(n,a); e1/=np.linalg.norm(e1); e2=np.cross(n,e1)
    return e1,e2

def targeted(core, polar_deg=62.0, nring=6, az_off=0.0, extra_radius=2.0):
    """for each outer centre place nring points at distance 2 in the outward cone"""
    pts=[]
    for w in core[1:]:
        n=w/np.linalg.norm(w); e1,e2=frame(n)
        th=np.radians(polar_deg)
        for k in range(nring):
            az=2*np.pi*k/nring+az_off
            v=np.cos(th)*n+np.sin(th)*(np.cos(az)*e1+np.sin(az)*e2)
            pts.append(w+extra_radius*v)
    return np.array(pts)

def accept(base, cands, minsep=2.0-1e-9):
    keep=list(base); t=cKDTree(np.array(keep))
    for p in cands:
        if t.query(p)[0]>=minsep:
            keep.append(p); t=cKDTree(np.array(keep))
    return np.array(keep)

def fib(n):
    i=np.arange(n)+0.5; z=1-2*i/n; ph=np.arccos(z); th=np.pi*(1+5**0.5)*i
    return np.stack([np.cos(th)*np.sin(ph),np.sin(th)*np.sin(ph),z],1)

def vor_vol(P,R=22.0,nbuf=2500):
    A=np.vstack([P,fib(nbuf)*R]); vor=Voronoi(A); vol=np.zeros(len(A))
    for i in range(len(A)):
        ridx=vor.point_region[i]
        if ridx<0: continue
        reg=vor.regions[ridx]
        if -1 in reg or len(reg)<4: continue
        try: vol[i]=ConvexHull(vor.vertices[reg]).volume
        except Exception: vol[i]=0.0
    return vol[:len(P)]

core=icosa12(); rng=np.random.default_rng(11)
best=None
for polar in (62.,70.):
  for nring in (6,):
    for az in (0.,np.pi/6):
      cand=targeted(core,polar,nring,az)
      P=accept(core,cand)
      # add filler in the outer shell to saturate further
      u=rng.normal(size=(900,3)); u/=np.linalg.norm(u,axis=1)[:,None]
      r=(3.0+4.0*rng.random(900)**(1/3))[:,None]
      P=accept(P,u*r)
      vol=vor_vol(P); s=float(vol[1:13].sum())
      rec=dict(polar=polar,nring=nring,az=round(float(az),3),n=int(len(P)),
               sum12=round(s,6),mean12=round(s/12,6),gap=round(s-THRESH,6),
               refuted=bool(s<THRESH),minsep=round(float(pdist(P).min()),9))
      if best is None or s<best['sum12']: best=rec
print("THRESHOLD sum12 =",round(THRESH,6)," mean12 =",round(THRESH/12,6))
print(json.dumps(best,indent=1))
print("REFUTED" if best['refuted'] else "NOT refuted")
open('Experimental/evidence/icosa_targeted_completion.txt','w').write(json.dumps(best,indent=1)+"\n")
