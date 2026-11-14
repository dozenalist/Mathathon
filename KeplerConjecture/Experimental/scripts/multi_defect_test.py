#!/usr/bin/env python3
"""
Can two defects share paying neighbours, and how close can two icosahedral
defects be?  Both bear on the Hall condition (H_R).

Facts tested:
 (1) two icosahedral motifs with centres at distance d are legal only if their
     outer points stay >= 2 apart, i.e. d >= 6 (outer radius 2 each);
 (2) components merge at tau = 4.18, so defects merge only if d <= 4.18;
 (1)+(2) => two icosahedral defects are ALWAYS in different components, hence
     their paying neighbourhoods are disjoint and no surplus is shared.
 (3) an icosahedral grid: several independent defects, check H_R per defect.
"""
import numpy as np, json, sys
from scipy.spatial import cKDTree
from scipy.spatial.distance import pdist
sys.path.insert(0,"Experimental/scripts")
import block_evaluator as BE

R32=float(np.sqrt(32)); R=2.09; TAU=2*R

def two_clusters(d):
    c=BE.icosa_cluster()
    return np.vstack([c, c+np.array([d,0,0])])

def _main():
    print("== (1)+(2) can two icosahedral defects be < tau = 4.18 apart? ==")
    for d in (4.0,4.18,5.0,5.5,6.0,6.2):
        P=two_clusters(d)
        sep=float(pdist(P).min())
        print(f"  d={d:>5}: min separation = {sep:.6f}  legal={sep>=2.0-1e-9}  "
              f"components_merged={d<=TAU}")
    print("  => d <= 4.18 would merge, but separation < 2 already at d = 5.0; the")
    print("     minimum legal separation is d ~ 5.5 (corrected: not 6, as I first wrote).")
    print("  => since 5.5 > 4.18 = 2R, icosahedral defects never share paying neighbours.\n")

    def icosa_grid(n=2, spacing=9.0, seed=3):
        cores=[]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    cores.append(BE.icosa_cluster()+np.array([i*spacing,j*spacing,k*spacing]))
        core=np.vstack(cores)
        rng=np.random.default_rng(seed)
        keep=list(core); t=cKDTree(np.array(keep))
        for c in core[::13]:
            u=rng.normal(size=(4000,3)); u/=np.linalg.norm(u,axis=1)[:,None]
            r=3.4*rng.random(4000)**(1/3)
            for q in u*r[:,None]+c:
                if t.query(q)[0]>=2.0-1e-9:
                    keep.append(q); t=cKDTree(np.array(keep))
        return np.array(keep)

    print("== (3) icosahedral grid ==")
    for n in (1,2):
        P=icosa_grid(n)
        r=BE.evaluate(P, f"icosa_grid_{n}x{n}x{n}", verbose=False)
        print(f"  {n}x{n}x{n}: n={r['n']} minsep={r['minsep']:.6f} defects={r['n_defective']} "
              f"buffer_limited={r['buffer_limited_cells']}")
        for label,rep in r.get("r2",{}).items():
            if "note" in rep or "blocks" not in rep: continue
            sds=[b["S_minus_D"] for b in rep["blocks"]]
            print(f"    {label}: {rep['components']} component(s) disjoint={rep['disjoint']} "
                  f"min S-D={min(sds):+.6f} max S-D={max(sds):+.6f} any_negative={any(x<0 for x in sds)}")
        json.dump(r, open(f"Experimental/evidence/multi_defect_{n}.json","w"), indent=1, default=float)


if __name__ == "__main__":
    _main()
