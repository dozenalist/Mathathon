#!/usr/bin/env python3
"""
Evaluator for the block inequalities (T'-R2') [one shell] and (T''-R2'') [two shells].

FORMULATION.  Lambda finite 2-separated point set.  c(v) = vol Omega(v).
Defective: c(v) < sqrt(32).  G_def: defective vertices, edge iff dist <= tau.
Components C of G_def.   N(C) = {w : 2 <= dist(w,C) <= rho}.
  R2'  (one shell):  tau = 2*rho = 4.18,  Block(C) = C u N(C)
  R2'' (two shells): tau = 4*rho = 8.36,  Block2(C) = C u N(C) u N(N(C))

WHY THE THRESHOLDS.  Disjointness of one-shell blocks needs: s in N(C1) cap N(C2)
=> dist(v1,v2) <= 2*rho => same component, so components at tau = 2*rho.
Disjointness of two-shell blocks needs dist(v1,v2) <= 4*rho, so tau = 4*rho.
Both are proved in GEOMETRIC_PARTITION.md; this script TESTS them numerically.

(T')  for a block B:  sum_{v in B} c(v) >= sqrt(32) |B|
      <=>  surplus(B) - deficit(B) >= 0  where surplus/deficit split at sqrt(32).

ONE-SIDEDNESS.  Computed cell volumes are UPPER bounds for any packing containing
the point set (adding centres only shrinks cells).  So a computed FAILURE of (T')
is a genuine refutation of (T') FOR THIS SET; a computed success proves nothing.
Cells cut by the buffer (unbounded in the original) invalidate the test.

Run:  python3 Experimental/scripts/block_evaluator.py [--fixture NAME]
Exit: 0 always (it is an evaluator); results printed and written to evidence/.
"""
import numpy as np, json, argparse, sys
from scipy.spatial import Voronoi, ConvexHull, cKDTree
from scipy.spatial.distance import pdist

R32=float(np.sqrt(32)); RHO=2.09; V_DODE=5.5502910285155105

# ---------------- fixtures ----------------
def fib(n):
    i=np.arange(n)+0.5; z=1-2*i/n; ph=np.arccos(z); th=np.pi*(1+5**0.5)*i
    return np.stack([np.cos(th)*np.sin(ph),np.sin(th)*np.sin(ph),z],1)

def fcc(nx=3):
    a=2*np.sqrt(2)
    pts=[]
    for i in range(-nx,nx+1):
        for j in range(-nx,nx+1):
            for k in range(-nx,nx+1):
                for b in ([0,0,0],[0.5,0.5,0],[0.5,0,0.5],[0,0.5,0.5]):
                    pts.append([(i+b[0])*a,(j+b[1])*a,(k+b[2])*a])
    return np.array(pts)

def hcp(nx=3):
    s3=np.sqrt(3.0); h=2*np.sqrt(2.0/3.0); pts=[]
    for L in range(-3,4):
        sh=(0.0,0.0) if L%2==0 else (1.0,s3/3.0)
        for m in range(-nx,nx+1):
            for n in range(-nx,nx+1):
                pts.append([2*m+n+sh[0], n*s3+sh[1], L*h])
    return np.array(pts)

def icosa_cluster():
    phi=(1+5**0.5)/2; V=[]
    for s1 in (1,-1):
        for s2 in (1,-1):
            V += [[0,s1,s2*phi],[s1,s2*phi,0],[s1*phi,0,s2]]
    V=np.array(V,float); return np.vstack([[0,0,0],V/np.linalg.norm(V[0])*2.0])

def fill(core, rmax=6.5, minsep=2.0-1e-9, n=4000, seed=4):
    rng=np.random.default_rng(seed)
    u=rng.normal(size=(n,3)); u/=np.linalg.norm(u,axis=1)[:,None]
    r=(rmax*rng.random(n)**(1/3))[:,None]; cand=u*r
    keep=list(core); t=cKDTree(np.array(keep))
    for p in cand:
        if t.query(p)[0]>=minsep:
            keep.append(p); t=cKDTree(np.array(keep))
    return np.array(keep)

# NOTE (recorded, not fixed): a legal "perturbed fcc" fixture CANNOT be built by
# displacing a centre.  In fcc every one of the 12 neighbours sits at distance exactly
# 2, so any nonzero displacement violates the 2-separation.  Creating a defect needs a
# locally compressed motif, which is why the icosahedral cluster is the natural source.

def a15_fixture(reps=4):
    """A15 (beta-W) scaled to minimum separation 2: the only fixture whose interior
    cells satisfy the saturation criterion Omega(v) subset B(v,2)."""
    A=[(0,0,0),(0.5,0.5,0.5)]
    B=[(0.25,0,0.5),(0.5,0.25,0),(0,0.5,0.25),
       (0.75,0,0.5),(0.5,0.75,0),(0,0.5,0.75)]
    basis=(np.array(A+B,float))*(2.0/0.5)      # unscaled min distance is 0.5
    L=4.0
    pts=[]
    for i in range(-reps,reps+1):
        for j in range(-reps,reps+1):
            for k in range(-reps,reps+1):
                pts.append(basis+np.array([i,j,k])*L)
    return np.vstack(pts)

def two_icosa(sep=16.0, seed=7):
    """Two icosahedral clusters far apart, each with its own fill: TWO defect
    components, so the disjointness / overlap accounting is genuinely exercised."""
    c1=icosa_cluster(); c2=icosa_cluster()+np.array([sep,0,0])
    core=np.vstack([c1,c2])
    rng=np.random.default_rng(seed)
    keep=list(core); t=cKDTree(np.array(keep))
    # fill around EACH cluster centre separately, so neither sits on a boundary
    for centre in (np.zeros(3), np.array([sep,0,0])):
        u=rng.normal(size=(6000,3)); u/=np.linalg.norm(u,axis=1)[:,None]
        r=7.0*rng.random(6000)**(1/3)
        for q in u*r[:,None]+centre:
            if np.linalg.norm(q-centre)>7.05: continue
            if t.query(q)[0]>=2.0-1e-9:
                keep.append(q); t=cKDTree(np.array(keep))
    return np.array(keep)

def icosa_in_fcc_shell(seed=2, rmax=9.0):
    """Icosahedral 13-cluster plus a dense fcc lattice shell: the densest completion
    we can build cheaply.  Rotated fcc, accepting only points >= 2 from everything."""
    core=icosa_cluster()
    rng=np.random.default_rng(seed)
    phi=(1+5**0.5)/2
    A=np.array([[0,1,phi],[1,phi,0],[phi,0,1]],float)
    A=A/np.linalg.norm(A[:,0])*2.0*np.sqrt(2)      # fcc nearest-neighbour distance 2
    R=rng.normal(size=(3,3)); R=np.linalg.qr(R)[0]; A=A@R.T
    idx=np.array(np.meshgrid(*[np.arange(-6,7)]*3)).reshape(3,-1).T
    lat=idx@A
    lat=lat[np.linalg.norm(lat,axis=1)<rmax]
    lat=lat[rng.permutation(len(lat))]
    keep=list(core); t=cKDTree(np.array(keep))
    for p in lat:
        if t.query(p)[0]>=2.0-1e-9:
            keep.append(p); t=cKDTree(np.array(keep))
    return np.array(keep)

FIXTURES={
 "random_fill":    lambda: fill(np.zeros((1,3)), 6.5),          # sparse: expect NO defects
 "fcc_plain":      lambda: fcc(2),
 "hcp":            lambda: hcp(2),
 "icosa_fill":     lambda: fill(icosa_cluster(), 7.0, seed=4),
 "icosa_fill_b":   lambda: fill(icosa_cluster(), 7.0, seed=9),
 "a15_saturated":  lambda: a15_fixture(3),
 "two_icosa":      lambda: two_icosa(),
 "icosa_fcc_shell": lambda: icosa_in_fcc_shell(2),
 "icosa_fcc_shell_b": lambda: icosa_in_fcc_shell(5),
}

# ---------------- Voronoi with buffer + unbounded detection ----------------
def vor_volumes(P, R=26.0, nbuf=3000, extent_cap=2.0):
    """Returns (vol, unreliable_flag).

    A cell is flagged UNRELIABLE when its computed extent from its own centre
    exceeds `extent_cap`.  Two things make that the right test:
      * in a SATURATED packing Omega(v) is contained in B(v,2), so a cell with
        extent > 2 cannot be the cell of a saturated packing;
      * a sparse finite fixture (or one truncated by the buffer) produces exactly
        such cells, and their volumes are meaningless for the packing bound.
    An earlier version tested only "vertex radius > R - 1e-6", which silently
    missed cells truncated at radius ~18 by an unbounded buffer sphere."""

    buf=fib(nbuf)*R
    A=np.vstack([P,buf]); vor=Voronoi(A); n=len(P)
    vol=np.zeros(len(A)); touched=np.zeros(len(A),bool)
    for i in range(len(A)):
        ridx=vor.point_region[i]
        if ridx<0: continue
        reg=vor.regions[ridx]
        if len(reg)<4: continue
        if -1 in reg:
            touched[i]=True; continue
        V=vor.vertices[reg]
        try: vol[i]=ConvexHull(V).volume
        except Exception: touched[i]=True; continue
        # unreliable if the cell reaches farther than a saturated cell may
        if np.max(np.linalg.norm(V-P[i],axis=1)) > extent_cap+1e-9: touched[i]=True
    return vol[:n], touched[:n]

# ---------------- graph / blocks ----------------
def components(P, tau):
    n=len(P); parent=list(range(n))
    def find(a):
        while parent[a]!=a: parent[a]=parent[parent[a]]; a=parent[a]
        return a
    def union(a,b):
        ra,rb=find(a),find(b)
        if ra!=rb: parent[ra]=rb
    D=np.linalg.norm(P[:,None,:]-P[None,:,:],axis=2)
    for i in range(n):
        for j in range(i+1,n):
            if D[i,j]<=tau: union(i,j)
    comp={}
    for i in range(n): comp.setdefault(find(i),[]).append(i)
    return list(comp.values()), D

def evaluate(P, name, verbose=True):
    out={"fixture":name,"n":int(len(P))}
    if P is None: out["error"]="fixture could not be built legally"; return out
    sep=float(pdist(P).min())
    out["minsep"]=sep
    if sep < 2.0-1e-9:
        out["error"]=f"ILLEGAL: min separation {sep:.6f} < 2"; return out
    vol,touched=vor_volumes(P)
    nbuf_cells=int(touched.sum())
    out["buffer_limited_cells"]=nbuf_cells
    defect_idx=[i for i in range(len(P)) if vol[i] < R32 - 1e-12 and not touched[i]]
    out["n_defective"]=len(defect_idx)
    out["defective_vols"]=[float(vol[i]) for i in defect_idx][:20]
    out["defective_touched"]=int(sum(1 for i in range(len(P)) if touched[i] and vol[i]<R32))

    res={}
    for label,tau in (("R2_one_shell",2*RHO),("R2pp_two_shell",4*RHO)):
        sub=P[defect_idx] if defect_idx else np.zeros((0,3))
        if len(sub)==0:
            res[label]={"components":0,"note":"no defects: all blocks are singletons; (T) holds by definition"}
            continue
        comps_local,_=components(sub,tau)
        comps=[[defect_idx[j] for j in cc] for cc in comps_local]
        D=np.linalg.norm(P[:,None,:]-P[None,:,:],axis=2)
        report={"components":len(comps),"threshold":tau,"blocks":[]}
        allsets=[]
        for ci,C in enumerate(comps):
            Nc=set()
            for v in C:
                Nc |= {int(u) for u in np.where((D[v]>=2-1e-12)&(D[v]<=RHO+1e-12))[0]}
            Nc -= set(C)
            if label=="R2_one_shell":
                B=set(C)|Nc
            else:
                N2=set()
                for w in Nc:
                    N2 |= {int(u) for u in np.where((D[w]>=2-1e-12)&(D[w]<=RHO+1e-12))[0]}
                B=set(C)|Nc|(N2-set(C))
            allsets.append(B)
            Bl=sorted(B)
            tot=sum(vol[i] for i in Bl)
            need=R32*len(Bl)
            deficit=sum(max(0.0,R32-vol[i]) for i in C)
            surplus=sum(max(0.0,vol[i]-R32) for i in Bl if i not in C)
            rep={"component_size":len(C),"block_size":len(Bl),
                 "sum_vol":float(tot),"need":float(need),
                 "T_holds":bool(tot>=need-1e-9),
                 "deficit_D":float(deficit),"surplus_S":float(surplus),
                 "S_minus_D":float(surplus-deficit),
                 "block_has_buffer_cell":bool(any(touched[i] for i in Bl)),
                 "diam_block":float(max(np.linalg.norm(P[i]-P[j]) for i in Bl for j in Bl)),
                 "surplus_minus_deficit_direct":float(tot-need)}
            report["blocks"].append(rep)
        # disjointness / coverage check
        ov=0
        for a in range(len(allsets)):
            for b in range(a+1,len(allsets)):
                ov=max(ov,len(allsets[a]&allsets[b]))
        report["max_pairwise_overlap"]=ov
        report["disjoint"]=bool(ov==0)
        res[label]=report
    out["r2"]=res
    if verbose:
        print(f"\n=== {name} : n={out['n']} minsep={sep:.6f} ===")
        print(f"  buffer-limited cells: {nbuf_cells}   defective: {out['n_defective']}")
        for label,rep in res.items():
            if "note" in rep: print(f"  {label}: {rep['note']}"); continue
            print(f"  {label}: {rep['components']} component(s), disjoint={rep['disjoint']} (max overlap {rep['max_pairwise_overlap']})")
            for bi,b in enumerate(rep["blocks"]):
                print(f"    block {bi}: |C|={b['component_size']} |B|={b['block_size']} "
                      f"sum={b['sum_vol']:.6f} need={b['need']:.6f} "
                      f"(T)={b['T_holds']} S-D={b['S_minus_D']:+.6f} "
                      f"diam={b['diam_block']:.3f} buffer={b['block_has_buffer_cell']}")
    return out

if __name__=="__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("--fixture",default="all")
    a=ap.parse_args()
    names=list(FIXTURES) if a.fixture=="all" else [a.fixture]
    results={}
    for nm in names:
        try: results[nm]=evaluate(FIXTURES[nm](), nm)
        except Exception as e: results[nm]={"fixture":nm,"error":repr(e)}; print(f"{nm}: ERROR {e!r}")
    import os; os.makedirs("Experimental/evidence",exist_ok=True)
    with open("Experimental/evidence/block_evaluator.json","w") as f:
        json.dump(results,f,indent=1,default=float)
    # --- summary: min over fixtures of S-D for each rule (the quantity to beat is 0) ---
    print("\n=== SUMMARY (S - D should be >= 0; deficit is ~0.1066) ===")
    for label in ("R2_one_shell","R2pp_two_shell"):
        vals=[]
        for nm,r in results.items():
            rep=r.get("r2",{}).get(label,{})
            for b in rep.get("blocks",[]):
                vals.append(b["S_minus_D"])
        if vals:
            print(f"  {label}: {len(vals)} block(s) tested, min S-D = {min(vals):+.6f}, "
                  f"max = {max(vals):+.6f}, any negative = {any(v<0 for v in vals)}")
        else:
            print(f"  {label}: no non-vacuous block tested")
    print("  NOTE: computed volumes are UPPER bounds, so a positive S-D does NOT certify;")
    print("        only a negative value would refute.  Status: TESTED_FINITE.")
    print("\nwritten Experimental/evidence/block_evaluator.json")
