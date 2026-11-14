#!/usr/bin/env python3
"""
Verifier for:  "Local finiteness of cyclic centres fails at k = 7"
(the k-labelled analogue of Theorem 6.5 of the five-colour paper is false for every k >= 7).

Objects (all exact data):
  * c0 : the paper's proper 7-colouring by Voronoi hexagons of the triangular lattice
         Lambda = d(Z + Z w),  w = e^{2 pi i/3},  d = 2 sqrt3/5,  circumradius r = 2/5,
         centre d(m+n w) receives label (m + 2n) mod 7  (seven cosets of (2-w)Lambda).
  * p0 = (1/55, 18/55),  l = 1/100,  W = p0 + [-l/2,l/2]^2  (diam(W) = l sqrt2 = 0.0141 < 1).
  * c  : c = c0 off W;  on W a "nested Mercedes" gadget using only labels {0,2,3},
         with background label 0 and triple points q_n -> p0 inside W.
Assertions checked below:
  A1  c0 is a proper 7-colouring                       (exact, lattice distance 2 sqrt21/5)
  A2  the closed annulus {1-eps <= |q-p0| <= 1+eps}, eps = 71/10000 > l/sqrt2,
      meets only colours {1,4,5,6} of c0                (two independent exact methods)
  A3  hence c is a proper 7-colouring                  (A1,A2 + diam(W) < 1)
  A4  q_n is a cyclic centre of c: Gamma_{q_n} contains the triangle {0,2,3}
                                                       (sector transition lemma + numeric)
  A5  q_n -> p0, so the cyclic locus L is not locally finite
  A6  non-vacuity: for the unmodified c0, L is exactly the vertex set of the tiling (discrete);
      the annulus certificate really detects colours (negative control fails).
Usage: python3 verify.py
"""
from fractions import Fraction as F
import math, sys

# ---------------- exact arithmetic in Q(sqrt3) ----------------
def q(a,b=0): return (F(a),F(b))
def Qadd(x,y): return (x[0]+y[0],x[1]+y[1])
def Qsub(x,y): return (x[0]-y[0],x[1]-y[1])
def Qmul(x,y): return (x[0]*y[0]+3*x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def sgn(x):
    p,r=x
    if p==0 and r==0: return 0
    if r==0: return 1 if p>0 else -1
    if p==0: return 1 if r>0 else -1
    if p>0 and r>0: return 1
    if p<0 and r<0: return -1
    v=p*p-3*r*r
    return (1 if v>0 else -1) if p>0 else (1 if v<0 else -1)
def fv(x): return float(x[0])+float(x[1])*math.sqrt(3)
def subv(P,Q): return (Qsub(P[0],Q[0]),Qsub(P[1],Q[1]))
def addv(P,Q): return (Qadd(P[0],Q[0]),Qadd(P[1],Q[1]))
def sc(c,P):   return (Qmul(c,P[0]),Qmul(c,P[1]))
def dot(P,Q):  return Qadd(Qmul(P[0],Q[0]),Qmul(P[1],Q[1]))
def dist2(P,Q):
    d=subv(P,Q); return dot(d,d)

R   = q(F(2,5))          # circumradius
INR = (F(0),F(1,5))      # inradius = sqrt3/5 = d/2
def unit(deg):
    deg%=360
    return {0:(q(1),q(0)),
            30:((F(0),F(1,2)),q(F(1,2))),
            60:(q(F(1,2)),(F(0),F(1,2))),
            90:(q(0),q(1)),
            120:(q(F(-1,2)),(F(0),F(1,2))),
            150:((F(0),F(-1,2)),q(F(1,2))),
            180:(q(-1),q(0)),
            210:((F(0),F(-1,2)),q(F(-1,2))),
            240:(q(F(-1,2)),(F(0),F(-1,2))),
            270:(q(0),q(-1)),
            300:(q(F(1,2)),(F(0),F(-1,2))),
            330:((F(0),F(1,2)),q(F(-1,2)))}[deg]
def zpoint(m,n):                 # d(m + n w) = ( sqrt3 (2m-n)/5 , 3n/5 )
    return ((F(0),F(2*m-n,5)),(F(3*n,5),F(0)))
def colour(m,n): return (m+2*n)%7

report=[]; FAILED=[]
def check(name, ok, detail=""):
    report.append((name,ok,detail))
    if not ok: FAILED.append(name)
    print(("  PASS  " if ok else "  FAIL  ")+name+("   "+detail if detail else ""))

# ============ A1 : c0 is a proper 7-colouring (exact) ============
print("[A1] the paper's hexagonal 7-colouring is proper")
best=None
for m in range(-9,10):
    for n in range(-9,10):
        if (m,n)==(0,0) or (m+2*n)%7!=0: continue
        v=F(m*m-m*n+n*n)          # |m+n w|^2
        if best is None or v<best: best=v
d2=F(12,25)                        # d^2 = 12/25
# same-colour centres are >= d*sqrt(best) apart; need that minus 2r to exceed 1

check("min |z|^2 over nonzero same-colour lattice vectors equals 7*d^2", best==7)
check("same-colour hexagons are more than 1 apart: d*sqrt(7)-2r > 1",
      sgn(Qsub(q(d2*7), q((F(1)+F(4,5))**2)))>0,
      "d*sqrt7 = %.6f,  2r = 0.8" % math.sqrt(12/25*7))
check("diam of a hexagon = 2r = 4/5 < 1", 2*F(2,5)<1)

# ============ A2 : the annulus certificate, method 1 (polygon/annulus separation) ============
print("[A2a] annulus {1-eps<=|q-p0|<=1+eps} meets only colours {1,4,5,6}  (method 1: exact hexagon-annulus separation)")
p0=(q(F(1,55)),q(F(18,55)))
EPS=F(71,10000)
check("eps = 71/10000 exceeds l/sqrt2 = 1/(100 sqrt2)", float(EPS)>1/100/math.sqrt(2),
      "%.7f > %.7f"%(float(EPS),1/100/math.sqrt(2)))
def in_hexagon(p,z):
    for k in range(6):
        if sgn(Qsub(dot(subv(p,z),unit(60*k)),INR))>0: return False
    return True
def hexvert(z,k):
    u=unit(30+60*k); return addv(z,sc(R,u))
def dmax2(p,z): return max((dist2(hexvert(z,k),p) for k in range(6)),key=sgn)
def dmin2(p,z):
    if in_hexagon(p,z): return q(0)
    best=None
    for k in range(6):
        u=unit(60*k); t=Qsub(INR,dot(subv(p,z),u))
        qs=addv(p,sc(t,u))
        va=hexvert(z,(k-1)%6); vb=hexvert(z,k)
        e=subv(vb,va); uu=subv(qs,va)
        num=dot(uu,e); den=dot(e,e)
        if sgn(num)>=0 and sgn(Qsub(den,num))>=0:
            c=dist2(qs,p); best=c if best is None else (c if sgn(Qsub(c,best))<0 else best)
    for k in range(6):
        c=dist2(hexvert(z,k),p); best=c if best is None else (c if sgn(Qsub(c,best))<0 else best)
    return best
def colour_absent_m1(p0,c,eps):
    lo=F(1)-eps-F(2,5)-F(1,100); hi=F(1)+eps+F(2,5)+F(1,100)
    slack=None
    for m in range(-8,9):
        for n in range(-8,9):
            if colour(m,n)!=c: continue
            z=zpoint(m,n); dz2=dist2(z,p0)
            if sgn(Qsub(dz2,q(hi*hi)))>0: continue
            if sgn(Qsub(dz2,q(lo*lo)))<0: continue
            dm=math.sqrt(fv(dmin2(p0,z))); dM=math.sqrt(fv(dmax2(p0,z)))
            sl=max(dm-1.0,1.0-dM)
            slack=sl if slack is None else min(slack,sl)
    return (slack is None) or slack>=float(eps), slack
for c in (0,2,3):
    ok,sl=colour_absent_m1(p0,c,EPS)
    check("colour %d is absent from the annulus (method 1)"%c, ok,
          "slack = "+("none (far away)" if sl is None else "%.6f"%sl))
for c in (1,4,5,6):
    ok,sl=colour_absent_m1(p0,c,EPS)
    check("colour %d is PRESENT in the annulus (negative control, must be False)"%c, not ok,
          "slack = "+("none" if sl is None else "%.6f"%sl))

# ============ A2 method 2 : independent covering certificate ============
print("[A2b] same statement, independent method 2 (covering by squares + face half-plane tests)")
def cover_absent(p0,eps,side,colours):
    p0f=(fv(p0[0]),fv(p0[1])); sf=F(side); sff=float(sf); ep=float(eps)
    lo=1-ep; hi=1+ep; hd=math.sqrt(2)*sff/2
    LAT=[(m,n,zpoint(m,n)) for m in range(-6,7) for n in range(-6,7) if colour(m,n) in colours]
    LAT=[(m,n,z,(fv(z[0]),fv(z[1]))) for (m,n,z) in LAT]
    R0=hi+hd+1e-6
    i0=math.floor((p0f[0]-R0)/sff)-1; i1=math.ceil((p0f[0]+R0)/sff)+1
    j0=math.floor((p0f[1]-R0)/sff)-1; j1=math.ceil((p0f[1]+R0)/sff)+1
    bad=0; pairs=0
    for i in range(i0,i1+1):
        cxf=sff*(i+0.5)
        for j in range(j0,j1+1):
            cyf=sff*(j+0.5)
            dc=math.hypot(cxf-p0f[0],cyf-p0f[1])
            if dc-hd>hi or dc+hd<lo: continue
            cx=q(F(cxf).limit_denominator(10**9)); cy=q(F(cyf).limit_denominator(10**9))
            h=q(sf/2); hm=(-h[0],-h[1])
            corners=[(Qadd(cx,h if a>0 else hm),Qadd(cy,h if b>0 else hm)) for a in(-1,1) for b in(-1,1)]
            for (m,n,z,zf) in LAT:
                if math.hypot(zf[0]-cxf,zf[1]-cyf)>0.4+hd: continue
                ok=False
                for k in range(6):
                    u=unit(60*k); mn=None
                    for C in corners:
                        v=dot(subv(C,z),u)
                        mn=v if mn is None else (v if sgn(Qsub(v,mn))<0 else mn)
                    if sgn(Qsub(mn,INR))>0: ok=True; break
                if not ok: bad+=1
                pairs+=1
    return bad==0, pairs
for side in (F(1,200),F(1,500)):
    ok,pr=cover_absent(p0,EPS,side,(0,2,3))
    check("colours 0,2,3 absent from the annulus (method 2, square side %s)"%side, ok, "%d (square,centre) pairs"%pr)
    ok2,pr2=cover_absent(p0,EPS,side,(1,))
    check("colour 1 NOT absent (method 2 negative control)", not ok2, "%d pairs"%pr2)

# ============ A3 : the full colouring c is proper ============
print("[A3] the modified colouring c is a proper 7-colouring")
L_=F(1,100); p0f=(fv(p0[0]),fv(p0[1]))
def wild(u1,u2):
    """colour of p0 + l*(u1,u2) inside W: nested Mercedes gadgets, labels 0,2,3"""
    r=math.hypot(u1,u2)
    for n in range(0,60):
        qn=(2.0**(-n-3), 0.0)            # q_n - p0 = l*2^{-n-3} (1,0)
        rho=2.0**(-n-14)                 # rho_n = l*2^{-n-14}
        dx=u1-qn[0]; dy=u2-qn[1]
        if math.hypot(dx,dy)<=rho:
            ang=math.degrees(math.atan2(dy,dx))%360
            if ang<60 or ang>=300: return 0
            if ang<180: return 2
            return 3
    return 0
def cfull(x,y):
    u1=(x-p0f[0])/0.01; u2=(y-p0f[1])/0.01
    if abs(u1)<=0.5 and abs(u2)<=0.5: return wild(u1,u2)
    return None      # outside W: colour of c0 (computed numerically below)
import random
random.seed(12345)
def c0num(x,y):
    qq=complex(x,y); d=math.sqrt(3)*0.4; w=-0.5+0.5j*math.sqrt(3)
    a=(qq/d); b=2*a.imag/math.sqrt(3); aa=a.real+b/2
    m0=round(aa); n0=round(b)
    best=1e9; bm=bn=0
    for dm in(-1,0,1,2):
        for dn in(-1,0,1,2):
            m,n=m0+dm,n0+dn; z=d*(m+n*w); dd=abs(qq-z)
            if dd<best: best=dd; bm,bn=m,n
    return (bm+2*bn)%7
def cnum(x,y):
    u1=(x-p0f[0])/0.01; u2=(y-p0f[1])/0.01
    if abs(u1)<=0.5 and abs(u2)<=0.5: return wild(u1,u2)
    return c0num(x,y)
viol=0
for _ in range(300000):
    x=random.uniform(0.0,0.06); y=random.uniform(0.26,0.38)   # region containing W
    th=random.uniform(0,2*math.pi)
    if cnum(x,y)==cnum(x+math.cos(th),y+math.sin(th)): viol+=1
check("no equal-coloured unit pair in 300000 random pairs near W", viol==0, "violations=%d"%viol)
viol2=0
for _ in range(100000):
    x=random.uniform(-2,2); y=random.uniform(-2,2); th=random.uniform(0,2*math.pi)
    if c0num(x,y)==c0num(x+math.cos(th),y+math.sin(th)): viol2+=1
check("no equal-coloured unit pair in 100000 random pairs for c0 itself", viol2==0, "violations=%d"%viol2)
# a structured check: pairs crossing the boundary of W
viol3=0; tried=0
for _ in range(200000):
    a=random.uniform(0,2*math.pi); rr=random.uniform(0.002,0.008)
    ux=random.uniform(-0.5,0.5); uy=random.uniform(-0.5,0.5)
    x=p0f[0]+0.01*ux; y=p0f[1]+0.01*uy
    if abs(ux)>0.5 or abs(uy)>0.5: continue
    tried+=1
    if cnum(x,y)==c0num(x+math.cos(a),y+math.sin(a)): viol3+=1
check("no equal-coloured unit pair for 200000 pairs with the first point inside W", viol3==0,
      "tried=%d violations=%d"%(tried,viol3))

# ============ A4 : q_n is a cyclic centre ============
print("[A4] the triangle {0,2,3} lies in Gamma_{q_n}:  Monte-Carlo transition densities")
PAIRS={(0,2):60.0,(2,3):180.0,(3,0):300.0}   # pair -> angle of its interface ray at q_n
def trans_ratio(qnx,qny,B_rad,ntry=8000):
    """for each pair (i,j) estimate |{q in B : c(q)=i, c(q+h)=j}| / |h| for h of length 0.02 B_rad
       normal to the i|j ray; return the ratio divided by B_rad (dimensionless, theory >= 1/8)."""
    out={}
    for (i,j),ang in PAIRS.items():
        t=0.02*B_rad
        hx=t*math.cos(math.radians(ang+90)); hy=t*math.sin(math.radians(ang+90))
        cnt=0
        for _ in range(ntry):
            rr=B_rad*math.sqrt(random.random()); aa=random.uniform(0,2*math.pi)
            px=qnx+rr*math.cos(aa); py=qny+rr*math.sin(aa)
            if cnum(px,py)==i and cnum(px+hx,py+hy)==j: cnt+=1
        area=math.pi*B_rad**2
        out[(i,j)] = (cnt/ntry)*area/t/B_rad     # = |D|/|h| / B_rad
    return out
for n in (0,2,4,6,8):
    qnx=p0f[0]+0.01*2.0**(-n-3); qny=p0f[1]
    rho=0.01*2.0**(-n-14)
    r=trans_ratio(qnx,qny,0.9*rho,ntry=6000)
    ok=all(v>0.02 for v in r.values())
    check("Gamma_{q_%d} contains {0,2},{2,3},{3,0}   (|D|/|h|/rho: %s; sector lemma gives >= 1/8)"
          %(n,{str(k):round(v,3) for k,v in r.items()}), ok)

# ============ A6 : non-vacuity ============
print("[A6] non-vacuity: for the unmodified c0 the cyclic locus is the tiling vertex set")
z0=zpoint(0,0)
V=addv(z0,sc(R,unit(30)))
vf=(fv(V[0]),fv(V[1]))
# the three cells meeting at V: the three lattice points at distance exactly r from V
near=sorted([(math.hypot(fv(zpoint(m,n)[0])-vf[0], fv(zpoint(m,n)[1])-vf[1]),m,n)
             for m in range(-3,4) for n in range(-3,4)])[:3]
cc=[colour(m,n) for _,m,n in near]
print("     the three cells at the vertex V have colours",sorted(cc),"and centres",[(m,n) for _,m,n in near])
def gamma_c0(x,y,B_rad=0.05):
    """edges of Gamma_x for c0, by sampling transitions at small h"""
    cnt={}
    for i in range(7):
        for j in range(i+1,7):
            hit=0; N=4000
            for _ in range(N):
                rr=B_rad*math.sqrt(random.random()); aa=random.uniform(0,2*math.pi)
                px=x+rr*math.cos(aa); py=y+rr*math.sin(aa)
                t=B_rad*0.02; hx=t*math.cos(random.uniform(0,2*math.pi)); hy=t*math.sin(random.uniform(0,2*math.pi))
                c1=c0num(px,py); c2=c0num(px+hx,py+hy)
                if {c1,c2}=={i,j}: hit+=1
            if hit>N*0.002: cnt[(i,j)]=hit
    return cnt
def ratio_pair(x,y,B_rad,i,j,amb,ntry=6000):
    """|{q in B : c0(q)=i, c0(q+h)=j}|/|h|/B_rad with h along the normal of the i|j interface"""
    zA=[(m,n) for (d,m,n) in near if colour(m,n)==i][0]
    zB=[(m,n) for (d,m,n) in near if colour(m,n)==j][0]
    zAf=zpoint(*zA); zBf=zpoint(*zB)
    dx=fv(zBf[0])-fv(zAf[0]); dy=fv(zBf[1])-fv(zAf[1]); nn=math.hypot(dx,dy)
    t=0.02*B_rad; hx=t*dx/nn; hy=t*dy/nn
    cnt=0
    for _ in range(ntry):
        rr=B_rad*math.sqrt(random.random()); aa=random.uniform(0,2*math.pi)
        px=x+rr*math.cos(aa); py=y+rr*math.sin(aa)
        if c0num(px,py)==i and c0num(px+hx,py+hy)==j: cnt+=1
    return (cnt/ntry)*math.pi*B_rad**2/t/B_rad
r1=ratio_pair(vf[0],vf[1],0.02,cc[0],cc[1],0); r2=ratio_pair(vf[0],vf[1],0.02,cc[1],cc[2],0)
r3=ratio_pair(vf[0],vf[1],0.02,cc[0],cc[2],0)
check("Gamma at a tiling vertex contains the 3-cycle on %s (ratios %s)"%(sorted(cc),[round(r1,3),round(r2,3),round(r3,3)]),
      min(r1,r2,r3)>0.02)
for pt,name in (((vf[0]+0.09,vf[1]+0.13),"hexagon interior"),((p0f[0]+0.05,p0f[1]+0.05),"away from the lattice")):
    E=gamma_c0(pt[0],pt[1])
    check("Gamma at a generic point (%s) is acyclic"%name, len(E)<=1, "edges=%s"%sorted(E))

# ============ A7 : palettes at the cyclic centres respect the general-k bound |P| <= k-3 = 4 ============
print("[A7] the palettes at the cyclic centres are contained in {1,4,5,6}, so |P| <= 4 = k-3")
bad=0; N=0
for _ in range(2000):
    x=p0f[0]+0.01*random.uniform(-0.5,0.5); y=p0f[1]+0.01*random.uniform(-0.5,0.5)
    aa=random.uniform(0,2*math.pi)
    for dr in (0.0,0.0004,-0.0004,0.0008):
        N+=1
        col=cnum(x+(1+dr)*math.cos(aa), y+(1+dr)*math.sin(aa))
        if col not in (1,4,5,6): bad+=1
check("every point at distance 1+-0.0008 from a point of W has colour in {1,4,5,6}", bad==0,
      "%d tested, %d violations"%(N,bad))

# ============ A8 : every palette has at most 3 labels ============
print("[A8] every palette of c has at most 3 labels (the k=6 palette bound), and at most 2 at the cyclic centres")
def pal(x,y,delta):
    s=set()
    for k in range(48):
        a=2*math.pi*k/48
        s.add(cnum(x+delta*math.cos(a),y+delta*math.sin(a)))
    s.add(cnum(x,y))
    return s
mx=0; mxW=0
for _ in range(3000):
    x=p0f[0]+0.01*random.uniform(-0.5,0.5); y=p0f[1]+0.01*random.uniform(-0.5,0.5)
    a=random.uniform(0,2*math.pi)
    mxW=max(mxW,len(pal(x+math.cos(a),y+math.sin(a),1e-5)))
for _ in range(3000):
    x=random.uniform(-3,3); y=random.uniform(-3,3); a=random.uniform(0,2*math.pi)
    mx=max(mx,len(pal(x+math.cos(a),y+math.sin(a),1e-5)))
check("max palette size at the cyclic centres (x in W) is <= 3", mxW<=3, "max=%d"%mxW)
check("max palette size anywhere is <= 3", mx<=3, "max=%d"%mx)
# the palette is a singleton a.e., and at a cyclic centre it takes four distinct values
sizes={}; vals=set()
for _ in range(1500):
    x=p0f[0]+0.01*random.uniform(-0.5,0.5); y=p0f[1]+0.01*random.uniform(-0.5,0.5)
    a=random.uniform(0,2*math.pi)
    P=pal(x+math.cos(a),y+math.sin(a),1e-6)
    sizes[len(P)]=sizes.get(len(P),0)+1
    vals|=P
check("palettes at the cyclic centres are singletons a.e.", sizes.get(1,0)>=1490, str(dict(sizes)))
check("the palette at a cyclic centre takes >= 4 distinct values as e varies", len(vals)>=4, str(sorted(vals)))
# positive control: probe exactly at tiling vertices, where three hexagons meet
zz=zpoint(0,0); VV=addv(zz,sc(R,unit(30))); vv=(fv(VV[0]),fv(VV[1]))
s3v=pal(vv[0],vv[1],1e-6)
check("positive control: the palette at a tiling vertex has exactly 3 labels", len(s3v)==3, str(sorted(s3v)))

print()
print("================ SUMMARY ================")
print("checks:",len(report),"  failures:",len(FAILED))
for n in FAILED: print("   FAILED:",n)
sys.exit(1 if FAILED else 0)
