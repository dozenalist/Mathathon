#!/usr/bin/env python3
"""Does E's (T) survive a DENSE completion of the icosahedral 13-cluster?

(T) needs  sum_{i=1..12} vol Omega(w_i) >= 13*sqrt(32) - V_dod = 67.9888142.
Adding centres only SHRINKS Voronoi cells (monotonicity, E003), so any finite completion
gives an UPPER bound on the saturated sum: if a completion already falls below the
threshold, (T) is REFUTED.  Otherwise the test is inconclusive but informative.
"""
import numpy as np, itertools, math
from scipy.spatial import Voronoi, ConvexHull

alive = 2.0
phi=(1+5**0.5)/2
ico=[np.array(v,float) for v in
     [(0,s,phi*t) for s in (1,-1) for t in (1,-1)]
    +[(s,phi*t,0) for s in (1,-1) for t in (1,-1)]
    +[(phi*s,0,t) for s in (1,-1) for t in (1,-1)]]
ico=[2*v/np.linalg.norm(v) for v in ico]          # 12 points at distance exactly 2
cluster=[np.zeros(3)]+ico                          # centre is index 0
print("cluster: centre + 12 at distance 2; min outer-outer distance = %.6f"
      % min(np.linalg.norm(ico[i]-ico[j]) for i,j in itertools.combinations(range(12),2)))

# dense FCC background, min separation 2
B=np.array([[0,2**0.5,2**0.5],[2**0.5,0,2**0.5],[2**0.5,2**0.5,0]],float)
R=9.0
pts=[]
for k in itertools.product(range(-6,7),repeat=3):
    p=np.array(k,float)@B
    if np.linalg.norm(p)<=R: pts.append(p)
pts=np.array(pts)
keep=[]
for p in pts:
    if min(np.linalg.norm(p-c) for c in cluster) >= alive-1e-12: keep.append(p)
keep=np.array(keep)
allpts=np.vstack([np.array(cluster)]+[keep])
print("background points kept: %d (of %d), total %d" % (len(keep),len(pts),len(allpts)))
# validity: min separation
from scipy.spatial import cKDTree
tr=cKDTree(allpts); dd,_=tr.query(allpts,k=2)
print("min pairwise distance in the configuration: %.12f (must be >= 2)" % dd[:,1].min())

vor=Voronoi(allpts)
def cell_volume(i):
    reg=vor.regions[vor.point_region[i]]
    if len(reg)==0 or (-1) in reg: return None   # unbounded
    V=vor.vertices[reg]
    return ConvexHull(V).volume if len(V)>=4 else None
vs=[cell_volume(i) for i in range(13)]
if any(v is None for v in vs):
    print("some cluster cells are unbounded (background too small):", [v is None for v in vs])
else:
    Vd=(15+7*5**0.5)/4*(4/math.sqrt(10+22/5**0.5))**3
    tot=sum(vs[1:]); thr=13*math.sqrt(32)-Vd
    print("vol Omega(centre)        = %.7f   (V_dod = %.7f ; sqrt32 = %.7f)" % (vs[0],Vd,math.sqrt(32)))
    print("sum of the 12 outer cells= %.7f   (mean %.7f)" % (tot,tot/12))
    print("(T) threshold            = %.7f" % thr)
    print("=> (T) HOLDS in this completion by margin %+.7f" % (tot-thr) if tot>=thr else
          "=> (T) is REFUTED by this completion: shortfall %.7f" % (thr-tot))
    print("   NOTE: upper bound only (monotonicity); a positive margin is NOT a proof.")
