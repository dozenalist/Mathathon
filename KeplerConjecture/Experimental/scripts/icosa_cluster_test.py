"""
K15-E: local-cell fixtures for a cluster-averaged correction criterion.

Unit spheres, minimum centre separation 2.  FCC/HCP Voronoi volume is
sqrt(32) = 4*sqrt(2) ~ 5.656854.

Fixture A: regular dodecahedron of inradius 1 is the Voronoi cell of the
centre of the icosahedral 13-cluster (12 tangent neighbours).  Its volume
is < sqrt(32), which refutes every pointwise criterion "vol Omega(v) >= L"
with L > 5.5503.

Fixture B: cluster average of vol Omega over that 13-cluster in an explicit
saturated-by-shell extension.

IMPORTANT one-sidedness: for a fixed finite cluster K, the computed
vol Omega(v) can only DECREASE when more centres are added.  Hence a finite
computation is an UPPER bound for the cell volumes of any packing containing
K.  A computed average ABOVE sqrt(32) therefore does NOT certify the cluster
criterion; only a value BELOW sqrt(32) refutes it.  Status: TESTED_FINITE.
"""
import numpy as np, json, sys
from scipy.spatial import Voronoi
from scipy.spatial.distance import pdist

R32 = np.sqrt(32.0)

def dodeca_volume_inradius1():
    # regular dodecahedron, inradius r: V = (15+7 sqrt5)/4 * a^3, a = 4r/sqrt(20+10 sqrt5)... use exact form
    import sympy as sp
    r = sp.Integer(1)
    # edge a in terms of inradius: r = a/4*sqrt(10+22/sqrt5)
    a = 4*r/sp.sqrt(10+22/sp.sqrt(5))
    V = (15+7*sp.sqrt(5))/4*a**3
    return sp.nsimplify(V), float(V)

def icosa_13():
    phi = (1+5**0.5)/2
    verts = []
    for s1 in (1,-1):
        for s2 in (1,-1):
            verts.append([0, s1*1.0, s2*phi]); verts.append([s1*1.0, s2*phi, 0]); verts.append([s1*phi, 0, s2*1.0])
    V = np.array(verts, float)
    # icosahedron with circumradius 1 -> scale to circumradius 2 (tangent unit spheres)
    V = V/np.linalg.norm(V[0])*2.0
    return np.vstack([[0,0,0], V])

def fib_shell(n, R, jitter=0.0, seed=0):
    i = np.arange(n)+0.5
    phi = np.arccos(1-2*i/n); th = np.pi*(1+5**0.5)*i
    P = np.stack([np.cos(th)*np.sin(phi), np.sin(th)*np.sin(phi), np.cos(phi)],1)*R
    if jitter>0:
        rng = np.random.default_rng(seed); P = P + rng.normal(0,jitter,P.shape)
        P = P/np.linalg.norm(P,axis=1)[:,None]*R
    return P

def fill_ball(core=None, rmax=7.0, minsep=2.0+1e-3, seed=1, tries=200000):
    from scipy.spatial import cKDTree
    rng = np.random.default_rng(seed)
    r = rmax*rng.random(tries)**(1/3)
    u = rng.normal(size=(tries,3)); u/= np.linalg.norm(u,axis=1)[:,None]
    cand = u*r[:,None]
    cand = cand[r>=minsep]
    pts=[]
    ref = np.array(core) if core is not None else np.zeros((0,3))
    for p in cand:
        if len(ref):
            if cKDTree(ref).query(p)[0] < minsep: continue
        if pts:
            if cKDTree(np.array(pts)).query(p)[0] < minsep: continue
        pts.append(p)
        ref = np.vstack([ref,p]) if len(ref) else p[None,:]
    return np.array(pts)

def vor_volumes(points, core_n, buffer_R=16.0, buffer_n=4000, seed=7):
    from scipy.spatial import ConvexHull
    buf = fib_shell(buffer_n, buffer_R)
    P = np.vstack([points, buf])
    vor = Voronoi(P)
    vol = np.zeros(len(P))
    for i in range(len(P)):
        ridx = vor.point_region[i]
        reg = vor.regions[ridx]
        if ridx < 0 or (-1 in reg) or len(reg) < 4:
            continue
        V = vor.vertices[reg]
        try:
            vol[i] = ConvexHull(V).volume
        except Exception:
            vol[i] = 0.0
    return vol[:len(points)]

def main():
    out={}
    Vex, Vnum = dodeca_volume_inradius1()
    out["dodecahedron_volume_exact"]=str(Vex); out["dodecahedron_volume"]=Vnum
    out["sqrt32"]=float(R32); out["dodeca_deficit"]=float(R32-Vnum)
    out["pointwise_dodeca_refutes_L_above"]=Vnum

    core = icosa_13()
    out["icosa_core_minsep"]=float(pdist(core).min())
    fill = fill_ball(core=core)
    pts = np.vstack([core, fill])
    out["cluster_size"]=int(len(pts)); out["minsep_all"]=float(pdist(pts).min())
    vol = vor_volumes(pts, len(core))
    out["centre_cell_volume"]=float(vol[0])
    out["twelve_mean"]=float(vol[1:13].mean())
    out["cluster13_sum"]=float(vol[:13].sum())
    out["cluster13_mean"]=float(vol[:13].mean())
    out["cluster13_mean_minus_sqrt32"]=float(vol[:13].mean()-R32)
    print(json.dumps(out, indent=2))

main()
