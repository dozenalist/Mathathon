"""
Angular lower bound on an outer-cell Voronoi volume given the six FIXED neighbours.

For x = w + t u in Omega(w):  t <= d_z/(2 cos phi_z) for every other centre z.
So   t(u) >= min_z  d_z/(2 cos phi_z)  over z with cos phi_z > 0,
and any centre has d_z >= 2, so a valid lower bound uses the directions we KNOW
(the six cluster neighbours) plus the fallback: at most 12 centres lie in
[2, 2.09] (K15-E014), so any further centre has d >= 2.09 and hence
contributes  2.09/(2 cos phi) >= 1.045.

    vol Omega(w) >= (1/3) * integral_{S^2} t_lb(u)^3 du .

We minimise this over the SIX FREE neighbour directions, with the six fixed ones
imposed.  The six fixed: c at distance 2 (direction -w/2), and five icosahedral
neighbours at distance 2.102851 (angle 58.28 deg from -w/2, pentagonally placed).

Status: exploratory (quadrature + local optimisation). NOT a certificate.
"""
import numpy as np, json
from scipy.optimize import minimize
from scipy.spatial.distance import pdist

R32=float(np.sqrt(32)); VOCT=4*np.pi/3
FIXED_D=[2.0]+[2.1028513]*5          # c, then five neighbours
FALLBACK=2.09/2.0                     # >= 1.045

def icosa_cluster():
    phi=(1+5**0.5)/2; V=[]
    for s1 in (1,-1):
        for s2 in (1,-1):
            V += [[0,s1,s2*phi],[s1,s2*phi,0],[s1*phi,0,s2]]
    V=np.array(V,float); V=V/np.linalg.norm(V[0])*2.0
    return np.vstack([[0,0,0],V])

core=icosa_cluster()
w=core[1]
fixed_dirs=[(core[0]-w) for _ in [0]]
fixed_dirs=[(core[0]-w)]+[ (core[j]-w) for j in range(2,13) ]
# keep only the 5 icosahedral neighbours of w (distance ~2.1029) plus c
fixed=[]
for j in range(1,13):
    d=np.linalg.norm(core[j]-w)
    if abs(d-2.0)<1e-6 or abs(d-2.1028513)<1e-4:
        v=core[j]-w; fixed.append((d, v/np.linalg.norm(v)))
fixed=[(2.0,(core[0]-w)/np.linalg.norm(core[0]-w))]+[(d,v) for d,v in fixed if abs(d-2.1028513)<1e-4]
FD=np.array([d for d,v in fixed]); FU=np.array([v for d,v in fixed])
print("fixed neighbours:",len(FD),"distances",np.round(FD,6))

# quadrature nodes on S^2
def fib(n):
    i=np.arange(n)+0.5; z=1-2*i/n; ph=np.arccos(z); th=np.pi*(1+5**0.5)*i
    return np.stack([np.cos(th)*np.sin(ph),np.sin(th)*np.sin(ph),z],1)
U=fib(2500); Wq=4*np.pi/len(U)          # equal-area => uniform weight

def sep_penalty(free_u, free_d, wl=400.0):
    """near neighbours of w must be mutual distance >= 2 in 3-D.
       For directions a,b with radii da,db:  dist^2 = da^2+db^2-2 da db cos(angle) >= 4."""
    allU=np.vstack([FU,free_u]); allD=np.concatenate([FD,free_d])
    C=allU@allU.T; D2=(allD[:,None]**2+allD[None,:]**2-2*allD[:,None]*allD[None,:]*C)
    n=len(allD); pen=0.0
    for i in range(n):
        for j in range(i+1,n):
            if D2[i,j] < 4.0-1e-9:
                pen += (4.0-D2[i,j])
    return wl*pen

def vol_lb(free_u, free_d, penalise=True):
    allU=np.vstack([FU,free_u]); allD=np.concatenate([FD,free_d])
    cosang=U@allU.T                      # (nq, nc)
    with np.errstate(divide='ignore',invalid='ignore'):
        cand=np.where(cosang>1e-12, allD[None,:]/(2*np.maximum(cosang,1e-12)), np.inf)
    t_near=cand.min(axis=1)              # min over the twelve near neighbours (inf if none aligned)
    # CORRECT DIRECTION: t = min over ALL centres, so a lower bound on t is the
    # MINIMUM of the per-centre lower bounds, not the maximum.  Far centres obey
    # d >= 2.09 hence d/(2 cos phi) >= 1.045.  (An earlier version used max here,
    # which inflated the bound and was caught by the direction check.)
    t=np.minimum(t_near, FALLBACK)
    v=float((t**3).sum()*Wq/3.0)
    if penalise: v += sep_penalty(free_u, free_d)
    return v

def unpack(x):
    x=np.asarray(x).reshape(-1,3)
    n=np.linalg.norm(x,axis=1)[:,None]
    return x/np.maximum(n,1e-12)

best=None
rng=np.random.default_rng(5)
for trial in range(4):
    x0=rng.normal(size=(6,3)).ravel()
    f=lambda x: vol_lb(unpack(x), np.full(6,2.0))
    r=minimize(f,x0,method='L-BFGS-B',options=dict(maxiter=200))
    # separation check among free dirs and against fixed (must be >=2 apart in 3-D)
    Fu=unpack(r.x)
    P=np.vstack([[w], w+2.0*Fu])         # crude: only 2-separation of the new ring
    Fu=unpack(r.x)
    rec=dict(trial=trial,val=float(r.fun),valor=vol_lb(Fu,np.full(6,2.0),penalise=False),
             feasible=bool(sep_penalty(Fu,np.full(6,2.0),wl=1.0)<=1e-7))
    if best is None or r.fun<best['val']: best=rec
print(json.dumps(best,indent=1))
print("threshold per outer cell      :", round(13*R32/12-5.5502910285155105/12,9))
print("dodecahedral floor            : 5.550291029")
print("12-direction (count-only) floor:", "~5.5503 (McLaughlin)")
print("inscribed-ball bound          :", round(VOCT,9))
print("angular bound (unpenalised)   :", round(best.get('valor',best['val']),9),
      " feasible:", best.get('feasible'))
print("VERDICT:", "above threshold" if best['val']>5.665734518 else "BELOW threshold -> (T') refuted approximate")
open('Experimental/evidence/outer_cell_angular_bound.txt','w').write(json.dumps(best,indent=1)+"\n")
