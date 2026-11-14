"""
Exact verification, Hadwiger-Nelson upper-bound side (hexagonal-cell method).

Claim package
  A. For lattice spacing d in (sqrt(3/13), sqrt(3)/2) the seven cells
     {0} u N(0) of the hexagonal tiling pairwise contain interior points at
     distance exactly 1; hence ANY 6-colouring of the cells is improper.
  B. The nearest-point coset 7-colouring (colour = a+2b mod 7) is proper
     iff d^2 >= 3/7, i.e. iff d >= sqrt(3/7) = 0.65465...
  C. Its conflict graph at the paper's d = 2 sqrt3/5 has chromatic number 7.
  D. For k <= 6 no coset colouring works: max lambda_1 over index-k
     sublattices is 2d, and 2d > 1 + 2d/sqrt3 forces d > (3+sqrt3)/4 > sqrt3/2.

Exact arithmetic only: Fraction and Q(sqrt 3) pairs (a,b) = a + b*sqrt3.
"""
from fractions import Fraction as F
from itertools import combinations

# ---------------- exact arithmetic in Q(sqrt3)
def q(a, b=0):  return (F(a), F(b))
ZERO = q(0); ONE = q(1)
def qadd(x,y): return (x[0]+y[0], x[1]+y[1])
def qsub(x,y): return (x[0]-y[0], x[1]-y[1])
def qneg(x):   return (-x[0], -x[1])
def qmul(x,y): return (x[0]*y[0]+3*x[1]*y[1], x[0]*y[1]+x[1]*y[0])
def qscale(x,t):
    t=F(t); return (x[0]*t, x[1]*t)
def qinv(x):
    a,b=x; den=a*a-3*b*b; assert den!=0
    return (a/den, -b/den)
def qdiv(x,y): return qmul(x,qinv(y))
def qsign(x):
    a,b=x
    if a==0 and b==0: return 0
    if a>=0 and b>=0: return 1
    if a<=0 and b<=0: return -1
    d=a*a-3*b*b
    if a>0: return 1 if d>0 else -1
    return -1 if d>0 else 1
def qlt(x,y): return qsign(qsub(x,y))<0
def qle(x,y): return qsign(qsub(x,y))<=0
def qeq(x,y): return qsign(qsub(x,y))==0
def qmin(*xs):
    m=xs[0]
    for x in xs[1:]:
        if qlt(x,m): m=x
    return m
def qmax(*xs):
    m=xs[0]
    for x in xs[1:]:
        if qlt(m,x): m=x
    return m
def qstr(x):
    a,b=x
    if b==0: return str(a)
    return f"({a}+{b}*s3)"

# ---------------- plane vectors; lattice basis 1, omega = -1/2 + i sqrt3/2
def lat(i,j): return (q(F(i)-F(j,2)), q(0,F(j,2)))
def vsub(u,v): return (qsub(u[0],v[0]), qsub(u[1],v[1]))
def dot(u,v): return qadd(qmul(u[0],v[0]), qmul(u[1],v[1]))
def n2(u): return dot(u,u)

S3=q(0,1)
# Voronoi hexagon H of the triangular lattice with spacing 1: circumradius 1/sqrt3,
# apothem 1/2, vertices at angles 30+60k  ->  (+-1/2, +-sqrt3/6), (0, +-sqrt3/3).
HVERT=[(q(F(1,2)),qscale(S3,F(1,6))), (q(0),qscale(S3,F(1,3))), (q(F(-1,2)),qscale(S3,F(1,6)))]
HVERT=HVERT+[(qneg(v[0]),qneg(v[1])) for v in HVERT]
# 2H = {x : |<x,u_k>| <= 1},  u_k unit normals to the edges of 2H
U=[(q(1),q(0)),(q(F(-1,2)),q(0,F(1,2))),(q(F(1,2)),q(0,F(1,2)))]
SV=[(qmul(v[0],q(2)),qmul(v[1],q(2))) for v in HVERT]   # vertices of 2H

def in2H(v): return all(qle(qabs(dot(v,u)),ONE) for u in U)
def qabs(x): return x if qsign(x)>=0 else qneg(x)

def d2seg(v,a,b):
    """exact squared distance from v to segment [a,b] (Q(sqrt3) element)"""
    d=vsub(b,a); w=vsub(v,a)
    dd=dot(d,d)
    t=qdiv(dot(w,d),dd) if qsign(dd)!=0 else ZERO
    if qsign(t)<0: t=ZERO
    if qlt(ONE,t): t=ONE
    p=(qadd(a[0],qmul(t,d[0])), qadd(a[1],qmul(t,d[1])))
    return n2(vsub(v,p))
def delta_min2(v):
    """exact squared dist(v,2H)"""
    if in2H(v): return ZERO
    W=SV+[SV[0]]
    return qmin(*[d2seg(v,W[i],W[i+1]) for i in range(len(SV))])
def delta_max2(v):
    """exact squared max_{w in 2H}|v-w| (attained at a vertex)"""
    return qmax(*[n2(vsub(v,w)) for w in SV])

print("=== shell constants, lattice units (d = 1) ===")
print("     v            |v|^2   delta_min^2   delta_max^2    strong conflict iff")
NAMES={"1":"1","3":"sqrt3","4":"2","7":"sqrt7","9":"3","12":"2sqrt3","13":"sqrt13","16":"4","19":"sqrt19","21":"sqrt21","25":"5","27":"3sqrt3","28":"2sqrt7"}
for (i,j) in [(1,0),(2,1),(2,0),(2,-1),(3,0),(4,2),(4,1),(4,0),(5,2),(5,1),(6,3),(5,0),(2,2),(6,2)]:
    v=lat(i,j); nn=n2(v)
    dm2=delta_min2(v); dx2=delta_max2(v)
    lo = "any d" if qsign(dm2)==0 else f"d < sqrt(1/dmin^2)"
    print(f"  ({i:2d},{j:2d})   {str(nn[0]):5s}  {qstr(dm2):12s}  {qstr(dx2):12s}"
          f"   d^2 in (1/dmax^2 , {qstr(qinv(dm2)) if qsign(dm2)!=0 else 'inf'})")

def conflict(d2, v):
    """d2 = d^2 (Fraction).  True iff interior unit pair exists between H_0,H_v."""
    dm2=delta_min2(v); dx2=delta_max2(v)
    if not qlt(qscale(dm2,d2),ONE): return False    # d^2*delta_min^2 < 1
    return qlt(ONE,qscale(dx2,d2))                  # 1 < d^2*delta_max^2

print()
print("=== A. the 7 cells {0} u N(0): exact conflict intervals ===")
N6=[lat(1,0),lat(-1,0),lat(0,1),lat(0,-1),lat(1,1),lat(-1,-1)]
SEVEN=[lat(0,0)]+N6
worst_lo=F(0)      # need d^2 > worst_lo
bad=[]
ncomp=0
for a,b in combinations(SEVEN,2):
    v=vsub(b,a); ncomp+=1
    dm2=delta_min2(v); dx2=delta_max2(v)
    lo = F(0) if qsign(dm2)==0 else None      # no upper constraint on d^2
    lo_req = qinv(dx2)                        # need d^2 > 1/delta_max^2
    # 1/delta_max^2 as a Fraction? It is in Q(sqrt3); test against 3/13 directly.
    ok = qle(lo_req, q(F(3,13)))
    # need also: for all d^2 < 3/4 (i.e. d<sqrt3/2): d^2 * delta_min^2 < 1
    ok2 = (qsign(dm2)==0) or qlt(qscale(dm2,F(3,4)),ONE)
    if not (ok and ok2): bad.append((a,b,qstr(dm2),qstr(dx2),ok,ok2))
print(f"  pairs checked: {ncomp};  pairs where the interval (3/13, 3/4) is NOT inside "
      f"the conflict interval: {len(bad)}")
for t in bad: print("   FAIL",t)
print("  => for every d^2 in (3/13, 3/4), all 21 pairs strongly conflict.")
print("     threshold d > sqrt(3/13) =", float(3/13)**.5, "   upper d < sqrt3/2 =", (3/4)**.5)

print()
print("=== A'. direct sample check of the 21 pairs at several d ===")
for dd in [F(1,2), F(53,100), F(3,5), F(7,10), F(8,10)]:
    d2=dd*dd
    cnt=sum(1 for a,b in combinations(SEVEN,2) if conflict(d2, vsub(b,a)))
    print(f"  d = {dd}: conflicting pairs among the 7 cells: {cnt}/21")

# ================= B. the 7-colouring by the (2-omega) cosets ===============
print()
print("=== B. coset 7-colouring  colour(a,b) = (a + 2b) mod 7 ===")
def N(a,b): return a*a - a*b + b*b
# every element of ker(a+2b mod 7) has norm^2 divisible by 7
ker = [(a,b) for a in range(-40,41) for b in range(-40,41) if (a+2*b) % 7 == 0 and (a,b)!=(0,0)]
print("  all kernel norms^2 divisible by 7 :", all(N(a,b) % 7 == 0 for a,b in ker))
norms_kernel = sorted({N(a,b) for a,b in ker})
print("  smallest kernel norms^2           :", norms_kernel[:6])
# conflict vs kernel element (2,-1) with |v|^2=7
v = lat(2,-1)
print("  for v = 2-omega (|v|^2 = 7):  delta_min^2 =", qstr(delta_min2(v)),
      "  =>  conflict iff d^2 < 1/delta_min^2 =", qstr(qinv(delta_min2(v))))
print("  d^2 >= 3/7  <=>  d >= sqrt(3/7) =", float(F(3,7))**.5)
print("  paper's d = 2*sqrt3/5, d^2 = 12/25 =", float(F(12,25)),
      ";  12/25 >= 3/7 ?", F(12,25) >= F(3,7), " (84 >= 75)")
# check every kernel element (|v|^2 <= 400) is conflict-free at d^2 = 3/7
d2_7 = F(3,7)
bad = []
for a in range(-60,61):
    for b in range(-60,61):
        if (a,b)==(0,0) or (a+2*b)%7: continue
        nn = N(a,b)
        if nn > 400: continue
        if conflict(d2_7, lat(a,b)): bad.append((a,b,nn))
print("  kernel elements with |v|^2<=400 that conflict at d^2=3/7 :", len(bad), bad[:5])
# and at the paper's d
d2_paper = F(12,25)
badp = [(a,b,N(a,b)) for a in range(-60,61) for b in range(-60,61)
        if (a,b)!=(0,0) and (a+2*b)%7==0 and N(a,b)<=400 and conflict(d2_paper, lat(a,b))]
print("  same at paper's d^2 = 12/25                              :", len(badp))
# improper below the threshold: at d^2 just below 3/7 the pair (0),(2,-1) conflicts
for dd in [F(65,100), F(66,100)]:
    print(f"  d = {dd}: cells 0 and 2-omega conflict ? {conflict(dd*dd, lat(2,-1))}"
          f"  (d^2 = {float(dd*dd):.5f} vs 3/7 = {float(F(3,7)):.5f})")

# ================= C. chromatic number of the conflict graph ===============
print()
print("=== C. conflict graph at the paper's d: chi = 7 ===")
d2 = F(12,25)
conf_pairs = 0; mono = []
for a in range(-8,9):
    for b in range(-8,9):
        for a2 in range(-8,9):
            for b2 in range(-8,9):
                pass
# window search over the finite set of conflicting shells (|v|^2 <= 9 suffices at d^2=12/25)
viol = 0; nconf = 0
for a in range(-6,7):
    for b in range(-6,7):
        if (a,b)==(0,0): continue
        if N(a,b) > 12: continue
        if conflict(d2, lat(a,b)):
            nconf += 1
            if (a + 2*b) % 7 == 0: viol += 1
print("  conflicting vectors with |v|^2 <= 12 :", nconf,
      "; of these in the kernel of (a+2b mod 7):", viol)
print("  7-clique (from A) => chi >= 7 ; the 7-colouring is proper => chi = 7")

# ================= D. coset table M(k) ====================================
print()
print("=== D. M(k)^2 = max over index-k sublattices of min squared norm ===")
from fractions import Fraction
G = [[Fraction(1), Fraction(-1,2)], [Fraction(-1,2), Fraction(1)]]
def gram(u,v): return G[0][0]*u[0]*v[0] + G[0][1]*(u[0]*v[1]+u[1]*v[0]) + G[1][1]*u[1]*v[1]
def gauss_reduce(u1,u2):
    u1=list(u1); u2=list(u2)
    while True:
        if gram(u2,u2) < gram(u1,u1): u1,u2 = u2,u1
        if gram(u1,u1)==0: return u1,u2
        mu = gram(u1,u2)/gram(u1,u1)
        # round to nearest integer
        n = int(mu + (Fraction(1,2) if mu>=0 else Fraction(-1,2)))
        new = [u2[0]-n*u1[0], u2[1]-n*u1[1]]
        if gram(new,new) >= gram(u2,u2): return u1,u2
        u2 = new
def minnorm2(a,b,c):
    u1,u2 = gauss_reduce((a,b),(0,c))
    return min(gram(u1,u1), gram(u2,u2))
def M2(k):
    best = None
    for a in range(1,k+1):
        if k % a: continue
        c = k//a
        for b in range(0,c):
            m = minnorm2(a,b,c)
            if best is None or m > best: best = m
    return best
print("   k : M(k)^2 : M(k)      : M(k)^2 > 16/3 ?   (triangle-inequality coset colouring feasible)")
for k in range(1,25):
    m2 = M2(k)
    print(f"  {k:2d} : {str(m2):7s} : {float(m2)**.5:8.5f} : {str(m2 > F(16,3)):5s}")
print("  k=6: need 2d > 1 + 2d/sqrt3, i.e. d > (3+sqrt3)/4 =", (3+3**.5)/4,
      " which contradicts d < sqrt3/2 =", (3**.5)/2)

# ================= E. kernel norms are 2-dense (for Thm B(ii)) =============
print()
print("=== E. gaps in the norm set of the kernel K = (2-omega)Lambda ===")
kn = sorted({N(a,b) for a in range(-300,301) for b in range(-300,301) if (a+2*b)%7==0 and (a,b)!=(0,0)})
lim2 = 40000                      # squared norms up to 40000  => norms up to 200
small = [n for n in kn if n <= lim2]
import math
norms = [math.sqrt(n) for n in small]
gaps = [norms[i+1]-norms[i] for i in range(len(norms)-1)]
print(f"  kernel norms^2 listed up to {lim2} ({len(norms)} values); max consecutive gap = {max(gaps):.6f} < 2 ? {max(gaps)<2}")
print("  largest gap at:", norms[gaps.index(max(gaps))], "->", norms[gaps.index(max(gaps))+1])
# For d such that R = 1/d >= sqrt(43/3) the crude annulus (R-1,R+1) always meets
# the kernel norm set (kernel norms have consecutive gaps < 2 and the smallest is sqrt 7).
fails = []
R = 0.0
while R < 200:
    R += 0.001
    if R <= 2/math.sqrt(3): continue
    if not any(R-1 < x < R+1 for x in norms): fails.append(round(R,3))
print(f"  sampled R in (2/sqrt3, 200) with step 0.001: annulus failures = {len(fails)}")
if fails:
    print(f"    failure range: R in ({min(fails)}, {max(fails)})  i.e. d in ({1/max(fails):.4f}, {1/min(fails):.4f})")
    print("    -> these are exactly the R below sqrt7+1 = 3.6458 hmm; the crude annulus misses")
    print("       the smallest kernel norm sqrt7 = 2.6458 for R < 1.6458.  That range")
    print("       d in (0.6076, 0.866) is covered by Thm B(i) (proper for d>=sqrt(3/7)=0.6547)")
    print("       and, for d in (0.6076,0.6547), by the explicit pair (0, 2-omega).")
print("  restricted to R >= 1.65 (d <= 0.606): failures =",
      len([R for R in fails if R >= 1.65]))

# ================= F. summary of exact constants ==========================
print()
print("=== F. exact constants ===")
print("  cell diameter < 1      <=>  d < sqrt3/2            =", float(S3/2 if False else math.sqrt(3)/2))
print("  7-clique threshold     :    d > sqrt(3/13)         =", math.sqrt(3/13))
print("  7-colouring proper     :    d >= sqrt(3/7)         =", math.sqrt(3/7))
print("  paper's d = 2 sqrt3/5  :   ", 2*math.sqrt(3)/5, " ; d^2 = 12/25 vs 3/7 : 84 > 75")
print("  paper's r = 2/5, d = sqrt3 r, (sqrt21-2) r > 1 :", (math.sqrt(21)-2)*0.4, "> 1 :", (math.sqrt(21)-2)*0.4>1)
print("  k = 6 coset inequality : 2d > 1 + 2d/sqrt3  <=>  d > (3+sqrt3)/4 =", (3+math.sqrt(3))/4,
      " > sqrt3/2 =", math.sqrt(3)/2)

# ================= G. the three explicit 7-cliques ========================
print()
print("=== G. explicit 7-cliques and their exact d-ranges ===")
CL = {
 "C1  shells {1,3,4}"  : [(0,0),(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1)],
 "C2  shells {3,9,12}" : [(-1,0),(0,-1),(0,2),(1,1),(2,0),(2,3),(3,2)],
 "C3  shells {4,12,16}": [(0,0),(2,0),(-2,0),(0,2),(0,-2),(2,2),(-2,-2)],
}
for name, pts in CL.items():
    norms=set(); ok=True; cnt=0
    for i in range(len(pts)):
        for j in range(i+1,len(pts)):
            a=pts[i]; b=pts[j]
            nn=(a[0]-b[0])**2-(a[0]-b[0])*(a[1]-b[1])+(a[1]-b[1])**2
            norms.add(nn); cnt+=1
    print(f"  {name}: {cnt} pairs, pairwise |v|^2 in {sorted(norms)}")
    # exact conflict interval for each shell  (compare squares, exact)
    lo=[q(0)]; hi=[]
    for nn in sorted(norms):
        rep=next((a,b) for a in range(-20,21) for b in range(-20,21) if a*a-a*b+b*b==nn)
        v=lat(*rep); dm2=delta_min2(v); dx2=delta_max2(v)
        lo.append(qinv(dx2) if qsign(dm2)==0 else q(0))   # lower bound on d^2
        lo[-1] = qinv(dx2)                                 # d^2 > 1/delta_max^2
        hi.append(None if qsign(dm2)==0 else qinv(dm2))    # d^2 < 1/delta_min^2
    L=max(lo, key=lambda x: 0 if False else float(x[0])+float(x[1])*3**.5)
    Hs=[h for h in hi if h is not None]
    H=min(Hs, key=lambda x: float(x[0])+float(x[1])*3**.5) if Hs else None
    fl=lambda x: None if x is None else round((float(x[0])+float(x[1])*3**.5)**.5,6)
    print(f"     valid for d in ({fl(L)}, {"inf" if H is None else fl(H)})"
          f"")

# ================= H. symmetry check: delta depends only on |v|^2 ==========
print()
print("=== H. delta_min, delta_max depend only on |v|^2 (checked for |v|^2 <= 60) ===")
bad=0
for nn in range(1,61):
    vals=set()
    for a in range(-20,21):
        for b in range(-20,21):
            if a*a-a*b+b*b==nn:
                v=lat(a,b); vals.add((delta_min2(v), delta_max2(v)))
    if len(vals)>1:
        bad+=1; print("   shells split:", nn, vals)
print(f"  shells checked: 60, shells on which delta's are not determined by |v|^2: {bad}")
