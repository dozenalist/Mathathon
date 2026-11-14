#!/usr/bin/env python3
"""
Search for the DENSEST completion of the icosahedral 13-cluster, and test the
Hall condition (H_R) / block inequality (T') on the best ones found.

Motivation: every completion built so far is sparse (density ~0.10 vs 0.177 for
fcc), so the computed surplus S-D (~+50) is inflated by free space.  This harness
pushes density up by local search so the inequality is tested near its hardest.

OBJECTIVE  minimise  sum_{i=1..12} vol Omega(w_i)   (lower = harder for (T')).
MOVES      insert a random 2-separated point in the annulus; delete a random point;
           accept on improvement, accept worsening with low probability (annealing).

RESOURCE CAP  one CPU, <= 1 GiB, hard wall-clock cap (default 300 s, max 600 s).
All reported volumes are UPPER bounds for any packing containing the set, so a
FAILURE (S-D < 0) refutes (T')/(H_R) for that set; success does not certify.
Status: TESTED_FINITE.

Run: python3 Experimental/scripts/dense_completion_search.py --seconds 120
"""
import numpy as np, json, time, argparse, sys
from scipy.spatial import cKDTree
sys.path.insert(0,"Experimental/scripts")
import block_evaluator as BE

R32=float(np.sqrt(32)); R=2.09

def sep_ok(P, p, tree):
    return tree.query(p)[0] >= 2.0-1e-9

_CACHE={}
def score(P):
    """Voronoi volumes; cached on the point-set hash since it dominates runtime."""
    key=(len(P), float(np.abs(P).sum()))
    if key in _CACHE: return _CACHE[key]
    vol,touched=BE.vor_volumes(P)
    if touched[:13].any():
        _CACHE[key]=(np.inf,None,None); return _CACHE[key]
    _CACHE[key]=(float(vol[1:13].sum()), vol, touched)
    return _CACHE[key]

def search(seconds=120.0, seed=1, rmax=7.0):
    rng=np.random.default_rng(seed)
    core=BE.icosa_cluster()
    # start from a random fill
    P=BE.fill(core, rmax, seed=seed)
    best_s,best_P=None,None
    vol,touched=BE.vor_volumes(P); best_s=float(vol[1:13].sum()); best_P=P.copy()
    t0=time.time(); it=0; cur_s=best_s; cur=P.copy()
    while time.time()-t0 < seconds:
        it+=1
        Q=cur.copy()
        if rng.random()<0.6:          # insert
            u=rng.normal(size=3); u/=np.linalg.norm(u)
            r=rmax*rng.random()**(1/3); p=u*r
            tree=cKDTree(Q)
            if sep_ok(Q,p,tree): Q=np.vstack([Q,p])
        else:                          # delete (never a core point)
            if len(Q)>13:
                Q=np.delete(Q, rng.integers(13,len(Q)), axis=0)
        s,vol_,touched_ = score(Q)
        if not np.isfinite(s): continue
        T=max(1e-6, 5.0*(1-(time.time()-t0)/seconds))
        if s<cur_s or rng.random()<np.exp(-(s-cur_s)/T):
            cur, cur_s = Q, s
        if s<best_s:
            best_s, best_P = s, Q.copy()
    return best_P, best_s, it

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--seconds",type=float,default=120.0)
    ap.add_argument("--seeds",type=int,default=3)
    a=ap.parse_args()
    sec=min(max(a.seconds,1.0),600.0)
    out={"cap_seconds":sec,"seeds":a.seeds,"runs":[]}
    for sd in range(a.seeds):
        t0=time.time()
        P,s,it=search(sec/a.seeds, seed=sd)
        el=time.time()-t0
        ev=BE.evaluate(P, f"dense_seed{sd}", verbose=False)
        rec={"seed":sd,"n":int(len(P)),"sum12":float(s),"mean12":float(s/12),
             "iters":int(it),"elapsed_s":round(el,2),
             "threshold_sum":13*R32-5.5502910285155105,
             "refuted":bool(s < 13*R32-5.5502910285155105),
             "minsep":float(__import__("scipy.spatial.distance",fromlist=["pdist"]).pdist(P).min())}
        for label,rep in ev.get("r2",{}).items():
            if "blocks" in rep:
                rec[f"{label}_min_SD"]=min(b["S_minus_D"] for b in rep["blocks"])
        out["runs"].append(rec)
        print(json.dumps(rec))
    best=min(out["runs"], key=lambda r: r["sum12"])
    out["best"]=best
    print("\nBEST:", json.dumps(best,indent=1))
    if best["refuted"]: print("=> REFUTED (T') for this completion")
    else: print("=> not refuted; computed sum is an UPPER bound so this is inconclusive")
    with open("Experimental/evidence/dense_completion_search.json","w") as f:
        json.dump(out,f,indent=1,default=float)
    print("written Experimental/evidence/dense_completion_search.json")
