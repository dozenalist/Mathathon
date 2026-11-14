"""
Reproduce Hales (unabridged) Section 2.1 / Section 3.1 local density constants.
Simplex density = vol(simplex cap union of unit balls at vertices)/vol(simplex).
Unit spheres, edge lengths as stated.  Monte Carlo, status TESTED_FINITE.
"""
import numpy as np, json
rng=np.random.default_rng(20261114)

def coords(y):
    # y=(y1,y2,y3,y4,y5,y6): edges 1,2,3 from origin; 4=(2,3),5=(3,1),6=(1,2)
    def place(a,b,c,ab,ac,bc):
        # returns p with |p|=a, dist to q(=b,0,0) = ab, to r = ac
        x=(a*a+ab*ab-b*b)/(2*ab); y2=a*a-x*x
        # r=(rx,ry,0)
        rx=(a*a+ac*ac-c*c)/(2*ac)
        ry=np.sqrt(max(a*a-rx*rx,0))
        # solve for z-comp
        d=(a*a+bc*bc-0)  # placeholder
        return x,y2,rx,ry
    y1,y2,y3,y4,y5,y6=y
    # v1 at origin, v2 on x-axis at y1, v3 in xy-plane, v4 general
    v2=np.array([y1,0.0,0.0])
    x=(y2**2+y1**2-y6**2)/(2*y1); yy=np.sqrt(max(y2**2-x*x,0))
    v3=np.array([x,yy,0.0])
    # v4: distances y3 to origin, y5 to v2, y4 to v3
    A=np.array([v2,v3]); b=np.array([(y3**2+y1**2-y5**2)/2,(y3**2+(x*x+yy*yy)-y4**2)/2])
    sol,_,_,_=np.linalg.lstsq(A,b,rcond=None)
    z2=y3**2-sol@sol
    if z2<=0: raise ValueError("degenerate")
    v4=np.array([sol[0],sol[1],np.sqrt(z2)])
    return np.zeros(3),v2,v3,v4

def density_of(y, N=400000):
    P=coords(y)
    # reject bad
    M=np.array(P)
    lo=M.min(0); hi=M.max(0)
    # sample in bounding box, keep inside simplex
    X=rng.uniform(lo-0.01,hi+0.01,size=(N*3,3))
    # barycentric test via lu / solve
    from scipy.spatial import Delaunay
    tri=Delaunay(M)
    inside=tri.find_simplex(X)>=0
    X=X[inside][:N]
    inside_count=len(X)
    # volume of simplex
    vol=abs(np.linalg.det(np.stack([P[1]-P[0],P[2]-P[0],P[3]-P[0]])))/6
    # coverage: point within 1 of any vertex
    d=np.min(np.stack([np.linalg.norm(X-p,axis=1) for p in P]),axis=0)
    frac=(d<=1.0).mean()
    return dict(vol_simplex=float(vol), samples=int(len(X)), covered_fraction=float(frac))

out={}
r2=2.0
# regular tetrahedron edge 2
out["tetra_regular_edge2"]=density_of((2,2,2,2,2,2))
# regular octahedron as 2 tetrahedra: use the (2,2,2,2,2,2sqrt2) simplex (half-octahedron)
out["half_octahedron"]=density_of((2,2,2,2,2,2*np.sqrt(2)))
# Hales Section 2.1 extremal simplex (2,2,2,2,l,l), l = sqrt(2(3+sqrt6)), long edges meeting at a vertex
l=np.sqrt(2*(3+np.sqrt(6)))
out["hales_extremal_l"]=float(l)
out["hales_extremal"]=density_of((2,2,2,2,l,l))
print(json.dumps(out,indent=2))
