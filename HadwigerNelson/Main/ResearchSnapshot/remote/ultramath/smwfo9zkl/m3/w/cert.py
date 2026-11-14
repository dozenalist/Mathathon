"""Exact certification in Q(sqrt 3) that a thin annulus around a rational point p0 meets only
four of the seven colours of the paper's hexagonal 7-colouring (circumradius r=2/5).
A number a+b*sqrt3 is the pair (a,b) of Fractions.  A point is a pair of such numbers."""
from fractions import Fraction as F
import math

# ---------- arithmetic in Q(sqrt3) ----------
def q(a,b=0): return (F(a),F(b))
def A(x,y): return (x[0]+y[0], x[1]+y[1])
def S(x,y): return (x[0]-y[0], x[1]-y[1])
def M(x,y): return (x[0]*y[0]+3*x[1]*y[1], x[0]*y[1]+x[1]*y[0])
def N(x):   return (-x[0],-x[1])
def sgn(x):
    p,r=x
    if p==0 and r==0: return 0
    if r==0: return 1 if p>0 else -1
    if p==0: return 1 if r>0 else -1
    if p>0 and r>0: return 1
    if p<0 and r<0: return -1
    v=p*p-3*r*r
    if p>0: return 1 if v>0 else -1
    return 1 if v<0 else -1
def ge0(x): return sgn(x)>=0
def gt0(x): return sgn(x)>0
def fl(x):  # approximate float
    return float(x[0])+float(x[1])*math.sqrt(3)
# ---------- points ----------
def addv(P,Q): return (A(P[0],Q[0]), A(P[1],Q[1]))
def subv(P,Q): return (S(P[0],Q[0]), S(P[1],Q[1]))
def sc(c,P):   return (M(c,P[0]), M(c,P[1]))
def dot(P,Q):  return A(M(P[0],Q[0]), M(P[1],Q[1]))
def dist2(P,Q):
    d=subv(P,Q); return dot(d,d)
def norm2(P):  return dot(P,P)
# ---------- the seven-colouring ----------
R   = q(F(2,5))
INR = (F(0),F(1,5))          # sqrt3/5 = inradius = d/2, d = 2 sqrt3/5
import math as _m
_UNIT={}
for _d in range(0,360,30):
    c=_m.cos(_m.radians(_d)); s=_m.sin(_m.radians(_d))
    def _q(v):
        for cand in [(F(2)*v,None),(v,None),(F(1,2)*v,None)]:
            pass
        return None
    _UNIT[_d]=None
def unit(deg):
    deg%=360
    tab={0:(q(1),q(0)),
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
         330:((F(0),F(1,2)),q(F(-1,2)))}
    return tab[deg]
def zpoint(m,n):
    """z = d(m + n w), w = -1/2 + i sqrt3/2, d = 2 sqrt3/5  ==>  (sqrt3(2m-n)/5, 3n/5)"""
    return ((F(0),F(2*m-n,5)), (F(3*n,5),F(0)))
def colour(m,n): return (m+2*n)%7
def hexvert(z,k):
    u=unit(30+60*k); return addv(z,(M(R,u[0]),M(R,u[1])))
def in_hexagon(p,z):
    for k in range(6):
        u=unit(60*k); w=subv(p,z)
        if gt0(S(dot(w,u),INR)): return False
    return True
def dmax2(p,z):
    return max((dist2(hexvert(z,k),p) for k in range(6)), key=sgn)
def dmin2(p,z):
    if in_hexagon(p,z): return q(0)
    best=None
    for k in range(6):
        u=unit(60*k); w=subv(p,z)
        f=dot(w,u)                       # <p-z,u>
        t=S(INR,f)
        qs=addv(p,(M(t,u[0]),M(t,u[1])))
        va=hexvert(z,(k-1)%6); vb=hexvert(z,k)
        e=subv(vb,va); uu=subv(qs,va)
        num=dot(uu,e); den=norm2(e)
        if ge0(num) and ge0(S(den,num)):
            cand=dist2(qs,p)
            best=cand if best is None else (cand if sgn(S(cand,best))<0 else best)
    for k in range(6):
        cand=dist2(hexvert(z,k),p)
        best=cand if best is None else (cand if sgn(S(cand,best))<0 else best)
    return best
# ---------- the annulus test ----------
def misses_colour(p0,c,eps):
    """True iff the closed annulus {q: 1-eps <= |q-p0| <= 1+eps} contains no point of colour c.
       Also returns the worst slack (min over colour-c hexagons of max(dmin-1, 1-dmax))."""
    slack=None
    lo=(F(1)-eps-F(2,5)-F(1,100),F(0)); hi=(F(1)+eps+F(2,5)+F(1,100),F(0))
    for m in range(-8,9):
        for n in range(-8,9):
            if colour(m,n)!=c: continue
            z=zpoint(m,n); dz2=dist2(z,p0)
            if gt0(S(dz2,M(hi,hi))): continue
            if sgn(S(dz2,M(lo,lo)))<0: continue
            dm2=dmin2(p0,z); dM2=dmax2(p0,z)
            s=max(fl(dm2)**0.5-1.0, 1.0-fl(dM2)**0.5)
            slack=s if slack is None else min(slack,s)
    if slack is None: return True, None
    return slack>=float(eps), slack
if __name__=="__main__":
    p0=(q(F(1,55)),q(F(18,55)))
    print("p0 = (1/55,18/55) =", fl(p0[0]), fl(p0[1]))
    print("|p0| =", math.sqrt(fl(norm2(p0))), " (needs < 2/5)")
    for ef in (0.0071,0.0170,0.0200):
        eps=F(ef).limit_denominator(10**7)
        out={}
        for c in range(7):
            ok,sl=misses_colour(p0,c,eps); out[c]=(ok, None if sl is None else round(sl,6))
        print("eps=%.4f ->"%ef, out)
