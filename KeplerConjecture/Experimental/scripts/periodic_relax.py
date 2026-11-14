#!/usr/bin/env python3
"""
Bounded periodic relaxation: search for a DENSE saturated packing with a cell
below sqrt(32), i.e. try to answer (Q) positively.

Parametrise N points in a cubic cell of side L with periodic boundary conditions.
Minimise  L^3 + P * sum_{i<j} max(0, 2 - d_ij)^2  over (positions, L), so density
increases until contacts lock.  Then scale to min separation exactly 2 and compute
Voronoi cell volumes.  Density = (4pi/3) N / L^3, so the mean cell volume is
(4pi/3)/density; a phase dense enough that the mean is near sqrt(32) can have
individual cells below it.

RESOURCE: one CPU, <= 1 GiB, --seconds cap (default 120).  TESTED_FINITE.
Run: python3 Experimental/scripts/periodic_relax.py --seconds 120 --starts 6
"""
import numpy as np, json, time, argparse, sys
from scipy.optimize import minimize
from scipy.spatial import ConvexHull, Voronoi
sys.path.insert(0,"Experimental/scripts")

R32=float(np.sqrt(32)); PEN=2.0e4

def min_image_dists(pos, L):
    d=pos[:,None,:]-pos[None,:,:]
    d-=L*np.round(d/L)
    return np.linalg.norm(d,axis=2)

def unpack(x, N):
    return x[:3*N].reshape(N,3)%1.0, x[3*N]

def objective(x, N):
    f,L=unpack(x,N)
    if L<=0.5: return 1e12
    D=min_image_dists(f*L, L); np.fill_diagonal(D,np.inf)
    viol=np.maximum(0.0, 2.0-D)
    return L**3 + PEN*np.sum(viol**2)

def relax(N, rng, iters=400):
    x0=np.concatenate([rng.random(3*N), [ (4.0/3.0*np.pi*N/0.74)**(1/3) ]])
    r=minimize(objective, x0, args=(N,), method="L-BFGS-B",
               bounds=[(0,1)]*(3*N)+[(1.0,20.0)], options=dict(maxiter=iters))
    return r

def cell_volumes(f, L, idxs=None):
    """Voronoi cell volumes in the periodic cell, via a 3x3x3 replica."""
    pts=[]
    for i in (-1,0,1):
        for j in (-1,0,1):
            for k in (-1,0,1):
                pts.append(f*L+np.array([i,j,k])*L)
    P=np.vstack(pts); n=len(f); c=n*13+n//2   # a core copy
    # pick the central replica's points
    start=13*n  # the (0,0,0) replica
    out={}
    D=min_image_dists(f*L,L)
    for t in (idxs if idxs is not None else range(n)):
        idx=start+t
        ridx=None
        # local Voronoi with far buffer to bound
        i2=np.arange(1500)+0.5
        z=1-2*i2/1500; ph=np.arccos(z); th=np.pi*(1+5**0.5)*i2
        buf=np.stack([np.cos(th)*np.sin(ph),np.sin(th)*np.sin(ph),z],1)*(L*6+20)
        A=np.vstack([P,buf]); vor=Voronoi(A)
        ridx=vor.point_region[idx]; reg=vor.regions[ridx]
        if ridx<0 or -1 in reg or len(reg)<4: out[t]=None; continue
        V=vor.vertices[reg]
        out[t]=(ConvexHull(V).volume, float(np.max(np.linalg.norm(V-P[idx],axis=1))))
    return out

if __name__=="__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("--seconds",type=float,default=120.0)
    ap.add_argument("--starts",type=int,default=6); a=ap.parse_args()
    sec=min(max(a.seconds,1.0),600.0); t0=time.time()
    best=None; recs=[]; perN={}
    for N in (4,6,8,12,16):
        for s in range(max(1,a.starts//3)):
            if time.time()-t0>sec: break
            rng=np.random.default_rng(100*N+s)
            r=relax(N,rng)
            f,L=unpack(r.x,N)
            D=min_image_dists(f*L,L); np.fill_diagonal(D,np.inf)
            dens=(4.0/3.0*np.pi*N)/L**3
            # PROJECT to exact separation 2 by scaling L; legal by construction
            Lp=L*(2.0/D.min()); densp=(4.0/3.0*np.pi*N)/Lp**3
            rec={"N":N,"start":s,"L_raw":float(L),"L_proj":float(Lp),
                 "min_d_raw":float(D.min()),"density":float(densp),
                 "mean_cell":float((4*np.pi/3)/densp)}
            if best is None or densp>best["density"]:
                best=dict(rec); best["_f"]=f.tolist(); best["_L"]=float(Lp)
            # keep the best per N so every N gets its cells examined
            if N not in perN or densp>perN[N]["density"]:
                perN[N]={"density":float(densp),"f":f.tolist(),"L":float(Lp),
                         "mean_cell":float((4*np.pi/3)/densp)}
            recs.append(rec)
            print(json.dumps({k:v for k,v in rec.items() if k!="_f"}))
    print("\n=== per-N: does any optimised phase have a cell below sqrt32? ===")
    perN_out={}
    for N in sorted(perN):
        f=np.array(perN[N]["f"]); L=perN[N]["L"]
        cv=cell_volumes(f,L)
        vals=sorted(v[0] for v in cv.values() if v is not None)
        if not vals: continue
        flag="  <-- HAS A CELL BELOW sqrt32" if vals[0]<R32-1e-9 else ""
        print(f"  N={N:2d} density={perN[N]['density']:.6f} mean={perN[N]['mean_cell']:.6f} "
              f"min_cell={vals[0]:.6f} max_cell={vals[-1]:.6f}{flag}")
        perN_out[N]={"density":perN[N]['density'],"min_cell":vals[0],"max_cell":vals[-1],
                     "any_below":bool(vals[0]<R32-1e-9)}
    print("\nbest (after projection):", json.dumps({k:v for k,v in best.items() if k!="_f"},indent=1))
    f=np.array(best["_f"]); L=best["_L"]
    cv=cell_volumes(f,L)
    vals=[v[0] for v in cv.values() if v is not None]
    print(f"mean cell volume = {(4*np.pi/3)/best['density']:.6f}  sqrt32 = {R32:.6f}")
    print("cell volumes:", [round(v,6) for v in sorted(vals)])
    print("ANY cell below sqrt32?", (min(vals)<R32-1e-9) if vals else "n/a")
    json.dump({"best":{k:v for k,v in best.items() if k!="_f"},
               "cell_volumes":{str(k):v for k,v in cv.items()},
               "sqrt32":R32,"any_below":bool(vals and min(vals)<R32-1e-9),
               "per_N":perN_out},
              open("Experimental/evidence/periodic_relax.json","w"), indent=1)
