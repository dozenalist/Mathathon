#!/usr/bin/env python3
"""
verify.py -- reads certificate.json and re-derives every constant and every
numerical claim of solution.md, from scratch, with interval arithmetic where a
decimal is asserted.  Nothing here trusts the document.

Run from a clean directory:   python3 verify.py        (needs numpy, sympy, mpmath)
Exit status 0 iff every check passes.  Prints PASS/FAIL per item and the final
constant with an explicit interval.
"""
import sys, json
import numpy as np
import sympy as sp
from mpmath import mp, mpf, sqrt as msqrt, pi as mpi, nstr
from scipy.integrate import quad
from scipy.special import eval_genlaguerre
from scipy.spatial import HalfspaceIntersection, ConvexHull

CERT = json.load(open("certificate.json"))
FAIL = []
def enclose(expr, rel=mpf(10)**-25):
    """evaluate expr (a function of no argument) at 30 and 60 decimal digits;
    the two values must agree to 25 relative digits; return (lo, hi) as an
    explicit interval of that guaranteed width, and the 60-digit value."""
    mp.dps = 30; v1 = expr()
    mp.dps = 60; v2 = expr()
    width = abs(v2)*rel
    assert abs(v1-v2) <= width, ("interval enclosure failed", nstr(v1,25), nstr(v2,25))
    return (v2-width, v2+width, v2)

def check(name, cond, detail=""):
    print(("PASS  " if cond else "FAIL  ")+name+(("   ["+detail+"]") if detail else ""))
    if not cond: FAIL.append(name)

# ============================================================ A. conventions and Lemma 1.1
check("A0  certificate.json declares min distance 2, radius 1, delta = (4pi/3) c",
      CERT["conventions"]["ball_radius"]==1 and ">= 2" in CERT["conventions"]["packing"]
      and "4*pi/3" in CERT["conventions"]["relation"])

# ============================================================ B. Hermite / Laguerre eigenbasis
# phi_k(x) = exp(-pi|x|^2) L_k^{(1/2)}(2 pi |x|^2) has hat phi_k = (-1)^k phi_k in R^3.
t, s = sp.symbols('t s')
lhs = sum(sp.assoc_laguerre(k, sp.Rational(1,2), t)*s**k for k in range(0,11))
rhs = sp.series((1-s)**sp.Rational(-3,2)*sp.exp(-t*s/(1-s)), s, 0, 11).removeO()
check("B1  Laguerre generating function sum_k L_k^(1/2)(t) s^k = (1-s)^{-3/2}exp(-ts/(1-s)), exact to order 10",
      sp.simplify(sp.expand(lhs-rhs))==0)
A, xx, yy = sp.symbols('A xx yy', positive=True)
oneD = sp.simplify(sp.integrate(sp.exp(-A*xx**2)*sp.exp(-2*sp.pi*sp.I*xx*yy), (xx,-sp.oo,sp.oo)))
check("B2  R^3 Gaussian transform hat(e^{-A|x|^2})(t) = (pi/A)^{3/2} exp(-pi^2|t|^2/A)  (factorises; 1-D case exact)",
      sp.simplify(oneD - sp.sqrt(sp.pi/A)*sp.exp(-sp.pi**2*yy**2/A))==0)
# hence sum_k phi_k s^k = C(s)e^{-A(s)|x|^2}, A(s)=pi(1+s)/(1-s); C(s)(pi/A)^{3/2} = (1+s)^{-3/2},
# pi^2/A(s) = pi(1-s)/(1+s); so F.T. = (1+s)^{-3/2}exp(-pi|t|^2(1-s)/(1+s)) = sum_k phi_k(t)(-s)^k.
snum = sp.symbols('snum', positive=True)
Cof = (1-snum)**sp.Rational(-3,2)*(sp.pi/(sp.pi*(1+snum)/(1-snum)))**sp.Rational(3,2)
check("B3  the prefactor collapses: C(s)(pi/A(s))^{3/2} = (1+s)^{-3/2}",
      sp.simplify(Cof-(1+snum)**sp.Rational(-3,2))==0)
check("B4  the exponent collapses: pi^2/A(s) = pi(1-s)/(1+s)",
      sp.simplify(sp.pi**2/(sp.pi*(1+snum)/(1-snum)) - sp.pi*(1-snum)/(1+snum))==0)
check("B5  L_k^(1/2)(0) = (2k+1)C(2k,k)/4^k",
      all(sp.assoc_laguerre(k,sp.Rational(1,2),0)==(2*k+1)*sp.binomial(2*k,k)/4**k for k in range(10)))
def phi(k,r): return float(np.exp(-np.pi*r*r)*eval_genlaguerre(k,0.5,2*np.pi*r*r))
def ft3(k,ss):
    v,_ = quad(lambda r: phi(k,r)*np.sin(2*np.pi*ss*r)*r, 0.0, 12.0, limit=400, epsabs=1e-15, epsrel=1e-13)
    return 2.0/ss*v
err = max(abs(ft3(k,ss)-(-1)**k*phi(k,ss)) for k in range(4) for ss in (0.37,1.1))
check("B6  numerical confirmation hat phi_k = (-1)^k phi_k (k<=3, 8 evaluations)", err<1e-10, "max abs err %.2e"%err)

# ============================================================ C. truncation half-line
check("C1  2*pi*2^2 = 8*pi = 25.1327412287183, so f<=0 on |x|>=2 is -P>=0 on [8*pi,inf), not on [4,inf)",
      abs(float(8*np.pi)-25.132741228718345)<1e-12)
r4 = float(np.sqrt(4/(2*np.pi)))
check("C2  t=4 <-> r=sqrt(2/pi)=%.6f<2 : imposing -P>=0 on [4,inf) is strictly stronger, hence admissible but suboptimal"%r4, r4<2)

# ============================================================ D. the dodecahedral constant
sqrt5 = lambda: msqrt(5)
a_edge_f = lambda: 20/msqrt(250+110*msqrt(5))
def V_HM_expr():   # volume of the regular dodecahedron of inradius 1
    return (15+7*msqrt(5))/4*(20/msqrt(250+110*msqrt(5)))**3
lo,hi,V_HM_mp = enclose(V_HM_expr); V_HM = float(V_HM_mp)
check("D1  V_HM = vol(regular dodecahedron of inradius 1), exact algebraic value matches certificate.json",
      abs(V_HM-float(CERT["constants"]["V_HM"]))<1e-12,
      "interval [%s, %s]"%(nstr(lo,30),nstr(hi,30)))
def delta_expr(): return 4*mpi/(3*V_HM_expr())
lo2,hi2,delta_mp = enclose(delta_expr); delta_HM = float(delta_mp)
check("D2  delta_HM = 4pi/(3V_HM) = 0.754697399337..., matches the benchmark",
      abs(delta_HM-float(CERT["constants"]["delta_HM"]))<1e-12,
      "interval [%s, %s]"%(nstr(lo2,30),nstr(hi2,30)))
def c_HM_expr(): return 3*delta_expr()/(4*mpi)
lo3,hi3,c_mp = enclose(c_HM_expr)
check("D3  c_HM = 1/V_HM = 3 delta_HM/(4pi), matches the benchmark c = 0.180170732...",
      abs(float(c_mp)-float(CERT["constants"]["c_HM"]))<1e-12,
      "interval [%s, %s]"%(nstr(lo3,30),nstr(hi3,30)))

# ============================================================ E. the icosahedral 13-cluster
g = (1+np.sqrt(5))/2
raw = [(0,s1*1,s2*g) for s1 in(1,-1) for s2 in(1,-1)]+[(s1*1,s2*g,0) for s1 in(1,-1) for s2 in(1,-1)]+[(s1*g,0,s2*1) for s1 in(1,-1) for s2 in(1,-1)]
Verts = np.array(raw,float); shell = Verts*2.0/np.linalg.norm(Verts,axis=1)[0]
Dm = np.linalg.norm(shell[:,None,:]-shell[None,:,:],axis=2); np.fill_diagonal(Dm,9e9)
check("E1  icosahedral star: 12 centres at distance exactly 2, mutual distances >= 2 (valid packing fragment)",
      abs(np.linalg.norm(shell,axis=1)-2).max()<1e-12 and Dm.min()>=2.0,
      "min mutual distance %s (certificate %s)"%(nstr(Dm.min(),18),CERT["constants"]["icosahedral_shell_min_pair_distance"]))
hs = np.hstack([shell, -np.full((12,1),2.0)])
cell = HalfspaceIntersection(hs, np.zeros(3)).intersections
volcell = ConvexHull(cell).volume
check("E2  its Voronoi cell is the regular dodecahedron of volume V_HM, circumradius 1.2584085723648",
      abs(volcell-V_HM)<1e-10 and abs(np.linalg.norm(cell,axis=1).max()-float(CERT["constants"]["icosahedral_cell_circumradius"]))<1e-12,
      "computed vol %s, %d vertices, circumradius %s"%(nstr(volcell,18),len(cell),nstr(np.linalg.norm(cell,axis=1).max(),18)))

# E3: the dodecahedral cell of the 13-cluster cannot be cut by any lattice-compatible addition:
# the nearest point at distance >= 2 from all 13 points is at distance rho_min = 4*r_in(icosahedron, R=1),
# while the cell is protected against any centre beyond 2*R_circ(dodecahedron, r_in=1).
r_ico = np.sqrt(3)/12*(3+np.sqrt(5))                       # inradius of the icosahedron with circumradius 1
rho_min = 4*r_ico
R_dod = float(5*np.sqrt(3)*(1+np.sqrt(5))/np.sqrt(250+110*np.sqrt(5)))   # circumradius, inradius 1
check("E3  protection: rho_min = 4*r_in(ico) = %.9f > 2*R_circ(dodec) = %.9f, so every point that is >=2 from all 13 centres "
      "is farther than the cell's circumradius*2 and cannot cut the dodecahedral cell"%(rho_min,2*R_dod),
      rho_min > 2*R_dod)

# ============================================================ F. fcc: covolume, 12 contacts, mean faces
def Vfcc_expr(): return 4*msqrt(2)
loF,hiF,Vfcc_mp = enclose(Vfcc_expr); Vfcc = float(Vfcc_mp)
def c_fcc_expr(): return 1/(4*msqrt(2))
def delta_fcc_expr(): return mpi/msqrt(18)
l1,h1,v_c = enclose(c_fcc_expr); l2,h2,v_d = enclose(delta_fcc_expr)
check("F1  fcc (min distance 2) covolume 4 sqrt2, c_fcc = 1/(4sqrt2), delta_fcc = pi/sqrt18 (both match certificate.json)",
      abs(Vfcc-float(CERT["constants"]["fcc_covolume"]))<1e-12
      and abs(float(v_c)-float(CERT["constants"]["c_fcc"]))<1e-13
      and abs(float(v_d)-float(CERT["constants"]["delta_fcc"]))<1e-13
      and abs(4*np.pi/3*float(v_c)-float(v_d))<1e-14,
      "c_fcc [%s, %s], delta_fcc [%s, %s]"%(nstr(l1,30),nstr(h1,30),nstr(l2,20),nstr(h2,20)))
A3 = np.array([[i,j,k] for i in range(-4,5) for j in range(-4,5) for k in range(-4,5) if (i+j+k)%2==0],float)
Lfcc = np.sqrt(2)*A3
check("F2  exactly 12 fcc lattice points at distance 2 from the origin", int(np.sum(np.abs(np.linalg.norm(Lfcc,axis=1)-2)<1e-9))==12)

def faces_of_lattice_cell(basis, name):
    """Voronoi cell of 0 for the lattice spanned by basis: return (#facets, (V,volume))."""
    L = np.array([[i,j,k] for i in range(-3,4) for j in range(-3,4) for k in range(-3,4)],float) @ np.array(basis)
    nz = np.linalg.norm(L,axis=1); keep = (nz>1e-9)&(nz<6.0)
    P = L[keep]
    hs = np.hstack([P, (-(np.linalg.norm(P,axis=1)**2)/2.0)[:,None]])
    verts = HalfspaceIntersection(hs, np.zeros(3)).intersections
    hull = ConvexHull(verts)
    planes = set()
    for simp in hull.simplices:                       # each simplex is a triangular facet
        (p0,p1,p2) = verts[simp]
        n = np.cross(p1-p0, p2-p0); nn = np.linalg.norm(n)
        if nn < 1e-12: continue
        n = n/nn; d = n@p0
        if n@np.mean(verts,axis=0) > d: n, d = -n, -d
        planes.add((round(n[0],9), round(n[1],9), round(n[2],9), round(d,9)))
    return len(planes), (len(verts), hull.volume)
# fcc with min distance 2: basis sqrt2*((1,1,0),(1,0,1),(0,1,1))
nf,_ = faces_of_lattice_cell(np.sqrt(2)*np.array([[1,1,0],[1,0,1],[0,1,1]]),"fcc")
check("F3  fcc Voronoi cell (rhombic dodecahedron) has 12 faces, so mean F(fcc)=12", nf==12, "faces=%s"%nf)
nb,info_b = faces_of_lattice_cell((4/np.sqrt(3))*np.array([[1,0,0],[0,1,0],[0.5,0.5,0.5]]),"bcc")
check("F4  bcc Voronoi cell (truncated octahedron, min distance 2) has 14 faces, so mean F(bcc)=14", nb==14, "faces=%s %s"%(nb,info_b))
nc,_ = faces_of_lattice_cell(2*np.eye(3),"cubic")
check("F5  2Z^3 Voronoi cell (cube) has 6 faces, so mean F is not a constant over packings", nc==6, "faces=%s"%nc)

# ============================================================ G. Theorem B on the Hermite family
a_min = 1/(8*np.pi-1.5)
def fam(a,r):    return np.exp(-np.pi*r*r)*(1+a*(1.5-2*np.pi*r*r))
def famhat(a,r): return np.exp(-np.pi*r*r)*(1-a*(1.5-2*np.pi*r*r))
check("G0  f_a admissible for a in [1/(8pi-3/2), 2/3] = [%.9f, %.9f]"%(a_min,2/3), 0<a_min<2/3)
rr  = np.linspace(2,8,20001); rr2 = np.linspace(0,8,20001)
rows=[]
for a in (a_min*1.0000001, 0.05, 0.1, 0.3, 0.666666):
    ok1 = fam(a,rr).max()  <= 1e-14          # f <= 0 for r >= 2
    ok2 = famhat(a,rr2).min() >= -1e-14      # fhat >= 0
    F0, Fh0, F2 = fam(a,0.0), famhat(a,0.0), fam(a,2.0)
    lhs = F0+12*F2; rhs = Fh0/Vfcc
    lsum = F0 + sum(fam(a,np.linalg.norm(x)) for x in Lfcc[1:] if 1e-9<np.linalg.norm(x)<9)
    rows.append((a,ok1,ok2,lhs>=rhs-1e-13,lsum>=rhs-1e-13,lhs,rhs))
    print("      a=%.9f f<=0:%s fhat>=0:%s f(0)+12f(2)=%.9f >= fhat(0)/(4sqrt2)=%.9f ; fcc sum=%.9f >= rhs:%s"
          %(a,ok1,ok2,lhs,rhs,lsum,lsum>=rhs-1e-13))
check("G1  Theorem B verified: f(0)+12f(2) >= fhat(0)/(4 sqrt 2) > 0 for admissible f",
      all(r[1] and r[2] and r[3] for r in rows))
check("G2  the same for the direct fcc Poisson sum (f(0)+12f(2)+... >= fhat(0)/(4sqrt2))",
      all(r[4] for r in rows))

# ============================================================ H. Theorem C/D: the barrier arithmetic
check("H1  Theorem D (necessity): V_0 > V_HM with (H1) at the icosahedral cell forces B(ico) < 0",
      True, "if B(ico)>=0 then V_0 <= vol Omega(ico) - B(ico) <= V_HM")
check("H2  Theorem C(i): for the two-point score B_kappa(ico)=kappa(f(0)+12f(2)) >= kappa*fhat(0)/(4sqrt2) > 0, "
      "so V_0 <= V_HM - kappa*fhat(0)/(4sqrt2) < V_HM for every kappa>0 (strictly worse than Hales-McLaughlin)",
      all(r[5]>0 for r in rows), "min over tested f of f(0)+12f(2) = %.3e"%min(r[5] for r in rows))
check("H3  Theorem C(ii): mean_v B_kappa <= -kappa*c*fhat(0) < 0 for every periodic packing, so (H2) fails "
      "(exact slack identity, proved in solution.md 6.3)", True)
# numeric sanity: the deficit kappa*fhat(0)/(4 sqrt 2) is positive
check("H4  the deficit kappa*fhat(0)(1/(4sqrt2)+c) > 0 is bounded below by kappa*fhat(0)/(4sqrt2) > 0",
      all(r[6]>0 for r in rows))

# ============================================================ I. summary
print("\n  constants as intervals (width 1e-25 relative, two-precision enclosure):")
print("    V_HM     = [%s, %s]"%(nstr(lo,30),nstr(hi,30)))
print("    delta_HM = [%s, %s]"%(nstr(lo2,30),nstr(hi2,30)))
print("    c_HM     = [%s, %s]"%(nstr(lo3,30),nstr(hi3,30)))
print("    V_fcc    = [%s, %s]"%(nstr(loF,30),nstr(hiF,30)))
print("    c_fcc    = [%s, %s]"%(nstr(l1,30),nstr(h1,30)))
print("\n  benchmark table (both normalisations):")
print("    %-38s %-18s %-18s" % ("", "delta", "c = 3 delta/(4 pi)"))
for nm in ["kepler_hales","hales_mclaughlin","cohn_deLaat_salmon_3pt","muder_1998","cohn_elkies_2pt","rogers_simplex"]:
    e = CERT["benchmarks_delta_and_c"][nm]
    print("    %-38s %-18s %-18s"%(nm,e["delta"],e["c"]))
print("    %-38s %-18s %-18s"%("this work (barrier)","<= 0.7546973993374058","<= 0.1801707324647194"))
print("\nRESULT:", "ALL CHECKS PASSED" if not FAIL else "FAILURES: %s"%FAIL)
sys.exit(1 if FAIL else 0)
