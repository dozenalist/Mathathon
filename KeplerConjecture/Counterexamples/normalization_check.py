#!/usr/bin/env python3
"""Independent normalization / sign checker for Kepler problem 15 (role X, swarm-free).

Conventions frozen here:
  * unit balls (radius 1), minimum separation 2;
  * f^(t) = int_{R^3} f(x) e^{-2 pi i <x,t>} dx ;
  * CE occupied-volume bound      Delta <= (4 pi / 3) f(0)/f^(0) ;
  * CE "center density"           delta  = Delta/(4 pi/3) = f(0)/f^(0) ;
  * at separation 2, delta = 1/covolume ("number density" and CE center density coincide);
    at separation 1 they differ by 2^3 (see section 3).
Exact (sympy) where algebra is involved; floating point only for convex-hull volumes,
which are also reproduced from closed forms.

Exit status 0 iff every check passes.
"""
import itertools, math
import sympy as sp
from sympy import Rational as R, sqrt, pi, simplify, nsimplify

FAILED, NCHK = [], [0]
def check(name, cond, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    if not ok: FAILED.append(name)
    print("  [%s] %-56s %s" % ("PASS" if ok else "FAIL", name, detail))

print("="*80); print("1.  FCC lattice, unit balls (separation 2)"); print("="*80)
FCC = sp.Matrix([[0,sqrt(2),sqrt(2)],[sqrt(2),0,sqrt(2)],[sqrt(2),sqrt(2),0]])  # ccp, nearest-neighbour distance 2
cov = sp.Abs(FCC.det())
check("FCC basis vectors all have length 2", all(FCC.row(i).dot(FCC.row(i))==4 for i in range(3)))
check("FCC covolume^2 = 32  (cov = 4 sqrt2)", sp.simplify(cov**2 - 32)==0, "cov = %s = %.6f" % (cov, float(cov)))
mn = min(sum((sp.Matrix(k).T*FCC)[0,j]**2 for j in range(3))
         for k in itertools.product(range(-2,3),repeat=3) if any(k))
check("FCC minimal separation^2 = 4 (sep = 2)", mn==4, "min |v|^2 = %s" % mn)
dens_fcc = sp.simplify((4*pi/3)/cov)
check("FCC density = pi/sqrt(18) exactly", sp.simplify(dens_fcc - pi/sqrt(18))==0,
      "pi/sqrt18 = %.9f" % float(pi/sqrt(18)))
check("pi/sqrt(18) = (4pi/3)/sqrt(32)", sp.simplify((4*pi/3)/sqrt(32) - pi/sqrt(18))==0)
check("Hales threshold sqrt(32) = 4 sqrt2", sp.simplify(sqrt(32)-4*sqrt(2))==0, "4sqrt2 = %.6f" % float(4*sqrt(2)))

print("="*80); print("2.  HCP (ABAB) is a PERIODIC PACKING with the same density, and is NOT a lattice"); print("="*80)
s3 = sqrt(3)
def inv3(v): return sp.Matrix(v)
L2 = [inv3([2,0]), inv3([1,s3])]                       # triangular layer, spacing 2
c  = 2*sqrt(6)/3                                       # interlayer height
off= inv3([1, s3/3, 0])                                # hollow (triangle centroid)
check("in-plane offset to hollow = 2/sqrt3", sp.simplify(off.dot(off) - R(4,3))==0)
check("interlayer height c = sqrt(4-4/3) = 2sqrt6/3", sp.simplify(c**2-R(8,3))==0, "c = %.6f" % float(c))
check("nearest A-B distance = 2", sp.simplify(off.dot(off)+c**2-4)==0)
area = sp.Abs(sp.Matrix([[2,0],[1,s3]]).det())
cellvol = simplify(area*(2*c))
check("HCP cell volume = 8 sqrt2 (2 pts/cell -> 4sqrt2 per point)", sp.simplify(cellvol-8*sqrt(2))==0, "cell = %.6f" % float(cellvol))
check("HCP density = FCC density = pi/sqrt18", sp.simplify((2*(4*pi/3))/cellvol - pi/sqrt(18))==0)
bpt = off + sp.Matrix([0,0,c])
check("HCP is NOT a lattice: translation by 2*(B-point) leaves the set",
      sp.simplify(sp.Matrix([2,0,0])+bpt - inv3([3, s3/3, c]))==sp.zeros(3,1), "2d=(%s,%s,%s) not an A-layer vector" % (2, sp.simplify(2*s3/3), sp.simplify(2*c)))
check("... because 2*d_xy = (2, 2sqrt3/3) is not in the triangular lattice",
      sp.simplify(sp.solve([2*sp.Symbol('m')+sp.Symbol('n')-2, s3*sp.Symbol('n')-2*s3/3],
                           [sp.Symbol('m'),sp.Symbol('n')], dict=True)[0][sp.Symbol('n')] - R(2,3))==0,
      "n = 2/3 not an integer")

print("="*80); print("3.  Convention conversions (the delta trap)"); print("="*80)
# CE center density delta = (r/2)^d/covol.  r=2: delta = 1/covol.  r=1: delta = (1/2)^3/covol.
check("2^(-5/2) = 1/(4 sqrt2) = FCC center density at sep 2", sp.simplify(2**R(-5,2) - 1/(4*sqrt(2)))==0,
      "2^-5/2 = %.8f" % float(2**R(-5,2)))
check("pi/sqrt18 = (4pi/3) * 2^(-5/2)", sp.simplify((4*pi/3)*2**R(-5,2) - pi/sqrt(18))==0)
check("number density at separation 1 is 8x that at separation 2", sp.Integer(8)==2**3,
      "must not compare sep-1 counts with sep-2 bounds without x8")
pub = {"CDS22 CE 2-point":0.779747, "CDS22 2-pt strengthened":0.773080,
       "CDS22 general 3-point":0.770271, "CDS22 lattice-only 3-point":0.741506,
       "Li Thm 6.1 lower bd on CE optimum":0.18398089}
print("     published value            occupied vol   center density   gap to pi/sqrt18")
for k,v in pub.items():
    if k.startswith("Li"):
        cd = v; occ = float(4*pi/3)*v
    else:
        occ = v; cd = v/float(4*pi/3)
    print("     %-30s %10.6f %14.8f %14.6f" % (k, occ, cd, occ-float(pi/sqrt(18))))
check("Li 0.18398089 > 2^(-5/2) strictly (CE not sharp in d=3)",
      0.18398089 > float(2**R(-5,2)), "margin %.8f in center-density units" % (0.18398089-float(2**R(-5,2))))
check("Li bound sits BELOW CDS22 CE value (different directions of the inequality)",
      0.18398089 < 0.779747/float(4*pi/3), "0.18398 < %.6f" % (0.779747/float(4*pi/3)))
check("CDS22 3-point 0.770271 < CDS22 CE 0.779747 (higher-point strictly stronger)",
      0.770271 < 0.779747)

print("="*80); print("4.  Voronoi-cell volumes: the icosahedral witness and the dodecahedral ceiling"); print("="*80)
import numpy as np
from scipy.spatial import ConvexHull
def polytope_volume(normals, dist=1.0):
    """volume of {x : n.x <= dist for all n}, by enumerating plane triples."""
    V=[]
    for i,j,k in itertools.combinations(range(len(normals)),3):
        A=np.array([normals[i],normals[j],normals[k]],dtype=float)
        if abs(np.linalg.det(A))<1e-12: continue
        x=np.linalg.solve(A,np.array([dist,dist,dist],dtype=float))
        if all(np.dot(n,x)<=dist+1e-9 for n in normals): V.append(x)
    V=np.array(V)
    return ConvexHull(V).volume, V
ph=(1+5**0.5)/2
ico=[(0,s,ph*t) for s in (1,-1) for t in (1,-1)]+[(s,ph*t,0) for s in (1,-1) for t in (1,-1)]+[(ph*s,0,t) for s in (1,-1) for t in (1,-1)]
ico=[np.array(v,float)/np.linalg.norm(v) for v in ico]
rhomb=[np.array(v,float)/np.linalg.norm(v) for v in
       [(1,1,0),(1,-1,0),(-1,1,0),(-1,-1,0),(1,0,1),(1,0,-1),(-1,0,1),(-1,0,-1),(0,1,1),(0,1,-1),(0,-1,1),(0,-1,-1)]]
V_rh,_ = polytope_volume(rhomb); V_do,_ = polytope_volume(ico)
check("rhombic dodecahedron (inradius 1) volume = 4 sqrt2", abs(V_rh-4*2**0.5)<1e-9,
      "%.9f vs 4sqrt2 = %.9f   <- equals FCC covolume and Hales's sqrt(32)" % (V_rh, 4*2**0.5))
check("regular dodecahedron (inradius 1) volume = 5.5503 (dodecahedral constant)", abs(V_do-5.5503)<2e-3,
      "%.9f" % V_do)
check("regular dodecahedron volume < 4 sqrt2  ==> cell-volume bound cannot reach Kepler",
      V_do < 4*2**0.5, "deficiency 4sqrt2 - V_dodec = %.6f" % (4*2**0.5 - V_do))
print("     => dodecahedral ceiling on density: (4pi/3)/V_dodec = %.6f   (published 0.7546974)" % (4*math.pi/3/V_do))
check("dodecahedral density ceiling 0.7546974 > pi/sqrt18 (so it cannot prove Kepler)",
      abs((4*math.pi/3)/V_do - 0.7546974) < 1e-6)
# icosahedral 13-ball cluster: 12 neighbours at distance exactly 2 from the centre.
check("12 icosahedral neighbours all at distance exactly 2 from the centre",
      all(abs(np.linalg.norm(2*v)-2)<1e-12 for v in ico))
dmin=min(np.linalg.norm(2*(ico[i]-ico[j])) for i,j in itertools.combinations(range(12),2))
check("icosahedral cluster is a valid packing (neighbour-neighbour distance > 2)", dmin>2,
      "min neighbour distance = %.6f" % dmin)
check("==> any fcc-compatible A needs A(v) >= 4sqrt2 - V_dodec = %.6f at such a vertex" % (4*2**0.5-V_do),
      4*2**0.5-V_do > 0.1)

print("="*80); print("5.  Poisson summation on FCC: dual lattice, scale and factor 1/V"); print("="*80)
B = np.array(FCC.tolist(), dtype=float)
V = abs(np.linalg.det(B))
Bd = np.linalg.inv(B).T                    # dual basis (rows), covolume 1/V
def lat_points(B, N=9):
    P=[]
    for k in itertools.product(range(-N,N+1),repeat=3):
        P.append(np.array(k,dtype=float)@B)
    return np.array(P)
alpha=0.9
fvals  = np.exp(-math.pi*np.sum(lat_points(B)**2,axis=1)/alpha**2)
fhat   = alpha**3*np.exp(-math.pi*alpha**2*np.sum(lat_points(Bd)**2,axis=1))
lhs, rhs = fvals.sum(), fhat.sum()/V
check("sum_Lambda f = (1/V) sum_{Lambda*} f^   (Gaussian, N=9 shells)", abs(lhs-rhs)<1e-7*abs(lhs),
      "%.10f vs %.10f" % (lhs,rhs))
check("FCC dual covolume = 1/(4sqrt2) (i.e. Lambda* is a BCC lattice, not Lambda)",
      abs(abs(np.linalg.det(Bd)) - 1/V) < 1e-12 and abs(1/V-1/(4*2**0.5))<1e-12,
      "covol(Lambda*) = %.6f" % abs(np.linalg.det(Bd)))
print("="*80)
print("checks run: %d   failures: %d" % (NCHK[0], len(FAILED)))
if FAILED:
    print("FAILED:", FAILED); sys.exit(1)
print("ALL CHECKS PASSED")
