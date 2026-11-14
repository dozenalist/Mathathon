"""Independent covering certificate (exact, in Q(sqrt3)) for:
   the closed annulus { q : 1-eps <= |q-p0| <= 1+eps } of the paper's hexagonal
   7-colouring contains no point of colour 0, 2 or 3.
Method: cover the annulus by closed axis-parallel squares Q.  For every square Q and every
lattice point z of colour 0/2/3 with dist(z,Q)<=r we exhibit one face of the Voronoi hexagon
of z whose supporting half-plane misses Q entirely (max of the affine face function over the
four corners of Q is < inradius).  Then no point of Q lies in the hexagon of z."""
from fractions import Fraction as F
import math
def q(a,b=0): return (F(a),F(b))
def A(x,y): return (x[0]+y[0],x[1]+y[1])
def Sc(x,y): return (x[0]-y[0],x[1]-y[1])
def M(x,y): return (x[0]*y[0]+3*x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def sgn(x):
    p,r=x
    if p==0 and r==0: return 0
    if r==0: return 1 if p>0 else -1
    if p==0: return 1 if r>0 else -1
    if p>0 and r>0: return 1
    if p<0 and r<0: return -1
    v=p*p-3*r*r
    return (1 if v>0 else -1) if p>0 else (1 if v<0 else -1)
def fl(x): return float(x[0])+float(x[1])*math.sqrt(3)
def subv(P,Q): return (Sc(P[0],Q[0]),Sc(P[1],Q[1]))
def dot(P,Q): return A(M(P[0],Q[0]),M(P[1],Q[1]))
INR=(F(0),F(1,5))
UNIT={0:(q(1),q(0)),60:(q(F(1,2)),(F(0),F(1,2))),120:(q(F(-1,2)),(F(0),F(1,2))),
      180:(q(-1),q(0)),240:(q(F(-1,2)),(F(0),F(-1,2))),300:(q(F(1,2)),(F(0),F(-1,2)))}
def zpoint(m,n): return ((F(0),F(2*m-n,5)),(F(3*n,5),F(0)))
def colour(m,n): return (m+2*n)%7
def run(p0,eps,side,colours=(0,2,3),report=True):
    p0f=(fl(p0[0]),fl(p0[1])); ep=float(eps); sf=F(side); sff=float(sf)
    lo=1-ep; hi=1+ep; hd=math.sqrt(2)*sff/2
    LAT=[(m,n,zpoint(m,n)) for m in range(-6,7) for n in range(-6,7)]
    LAT=[(m,n,z,(fl(z[0]),fl(z[1]))) for (m,n,z) in LAT if colour(m,n) in colours]
    R0=hi+hd+1e-6
    i0=math.floor((p0f[0]-R0)/sff)-1; i1=math.ceil((p0f[0]+R0)/sff)+1
    j0=math.floor((p0f[1]-R0)/sff)-1; j1=math.ceil((p0f[1]+R0)/sff)+1
    checked=0; fails=[]
    for i in range(i0,i1+1):
        cxf=sff*(i+0.5)
        for j in range(j0,j1+1):
            cyf=sff*(j+0.5)
            dc=math.hypot(cxf-p0f[0],cyf-p0f[1])
            if dc-hd>hi or dc+hd<lo: continue
            cx=q(F(cxf).limit_denominator(10**9)); cy=q(F(cyf).limit_denominator(10**9))
            h=q(sf/2); hm=(-h[0],-h[1])
            corners=[(A(cx, h if sx>0 else hm), A(cy, h if sy>0 else hm))
                     for sx in(-1,1) for sy in(-1,1)]
            for (m,n,z,zf) in LAT:
                if math.hypot(zf[0]-cxf,zf[1]-cyf) > 0.4+hd: continue
                ok=False
                for k in range(6):
                    u=UNIT[60*k]; mn=None
                    for C in corners:
                        v=dot(subv(C,z),u)
                        mn=v if mn is None else (v if sgn(Sc(v,mn))<0 else mn)
                    if sgn(Sc(mn,INR))>0: ok=True; break
                if not ok: fails.append((i,j,m,n))
                checked+=1
    if report: print("  side=%s  (square,z) pairs checked=%d  failures=%d"%(side,checked,len(fails)))
    for f in fails[:4]: print("     FAIL",f)
    return len(fails)==0, checked
if __name__=="__main__":
    p0=(q(F(1,55)),q(F(18,55)))
    eps=F(71,10000)
    print("p0 = (1/55, 18/55);  eps = 71/10000 = %s  (>= 1/(100*sqrt2) = %.7f)"%(float(eps),1/100/math.sqrt(2)))
    print("NEGATIVE CONTROL (colour 1 is present in the annulus; the test must fail):")
    for side in (F(1,50),F(1,200)):
        ok,n=run(p0,eps,side,colours=(1,)); print("  side",side,"certified free of colour 1?:",ok)
    print("POSITIVE CERTIFICATE:")
    for side in (F(1,100),F(1,200),F(1,400),F(1,800)):
        ok,n=run(p0,eps,side); print("  ==> annulus certified free of colours 0,2,3 at side",side,":",ok)
