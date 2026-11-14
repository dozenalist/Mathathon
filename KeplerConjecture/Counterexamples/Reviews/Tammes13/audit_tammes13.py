from fractions import Fraction as F
import math
def _fact(n):
    r=1
    for i in range(2,n+1): r*=i
    return r
def sin_bounds(x, terms=40):
    s=F(0); sign=1
    for k in range(terms):
        s += F(sign)*x**(2*k+1)/_fact(2*k+1); sign=-sign
    nxt = x**(2*terms+1)/_fact(2*terms+1)
    return s-nxt, s+nxt
def cos_bounds(x, terms=40):
    s=F(0); sign=1
    for k in range(terms):
        s += F(sign)*x**(2*k)/_fact(2*k); sign=-sign
    nxt = x**(2*terms)/_fact(2*terms)
    return s-nxt, s+nxt
def div_bounds(a_lo,a_hi,b_lo,b_hi):
    vals=[a_lo/b_lo,a_lo/b_hi,a_hi/b_lo,a_hi/b_hi]; return min(vals),max(vals)
def tan_bounds(x, terms=44):
    slo,shi=sin_bounds(x,terms); clo,chi=cos_bounds(x,terms); assert clo>0
    return div_bounds(slo,shi,clo,chi)
def pi_b():
    def at(n):
        S=[];acc=F(0)
        for k in range(80):
            acc+=F((-1)**k,(2*k+1)*n**(2*k+1)); S.append(acc)
        return min(S[-1],S[-2]),max(S[-1],S[-2])
    a1,a2=at(5); b1,b2=at(239); return 16*a1-4*b2,16*a2-4*b1
def g_bounds(a, terms=44):
    pilo,pihi=pi_b()
    ylo=3*pilo/8-a/4; yhi=3*pihi/8-a/4
    tlo,_=tan_bounds(ylo,terms); _,thi=tan_bounds(yhi,terms)
    clo,chi=cos_bounds(a,terms)
    nlo,nhi=1-2*chi,1-2*clo
    dlo,dhi=min(clo*clo,chi*chi),max(clo*clo,chi*chi)
    qlo,qhi=div_bounds(nlo,nhi,dlo,dhi)
    return 2*tlo-qhi, 2*thi-qlo
print("1. MY OWN rigorous bracket for the root of g")
for x in (F(12113,10000),F(12114,10000)):
    lo,hi=g_bounds(x)
    print("   a=%-9s g in [%+.8f, %+.8f]  %s" % (x,float(lo),float(hi),
          "POSITIVE" if lo>0 else ("NEGATIVE" if hi<0 else "STRADDLES")))
print("   => root in [1.2113,1.2114]; g strictly decreasing => unique")
print("\n2. monotonicity, checked symbolically")
import sympy as sp
a=sp.Symbol('a',positive=True)
gsym=2*sp.tan(3*sp.pi/8-a/4)-(1-2*sp.cos(a))/sp.cos(a)**2
d=sp.simplify(sp.diff(gsym,a))
print("   g'(a) =",sp.simplify(d))
print("   equals -(1/2)sec^2(.) - 2 sin a (1-cos a)/cos^3 a :",
      sp.simplify(d+sp.Rational(1,2)/sp.cos(3*sp.pi/8-a/4)**2+2*sp.sin(a)*(1-sp.cos(a))/sp.cos(a)**3)==0)
print("\n3. the identity claimed to validate transcription")
print("   cos d = cos a/(1-cos a)  =>  cos d/(1+cos d) = cos a IDENTICALLY.")
print("   So alpha(d)=a holds for EVERY solution of (E2), whatever (E1) is.")
print("   => that identity validates (E2) only; (E1) is pinned by the NUMERICAL match.")
for nm,c2 in {"(1-2cos a)/cos a":1,"(1-2cos a)/cos^3 a":3}.items():
    r=sp.nsolve(2*sp.tan(3*sp.pi/8-a/4)-(1-2*sp.cos(a))/sp.cos(a)**c2,1.2)
    dd=sp.acos(sp.cos(r)/(1-sp.cos(r)))
    ident=sp.simplify(sp.cos(dd)/(1+sp.cos(dd))-sp.cos(r))
    print("   variant %-20s a=%.4f deg d=%.4f deg ; identity residual %s (automatic)"
          % (nm,float(r)*180/math.pi,float(dd)*180/math.pi,ident))
print("\n4. the final bound E needs")
ahi=F(12114,10000); clo,chi=cos_bounds(ahi)
hlo=clo/(1-clo)
deg=math.degrees(math.acos(float(hlo)))
print("   cos(a*) >= %.12f  => h >= %.12f => delta_13 <= %.10f deg" % (float(clo),float(hlo),deg))
print("   required <= 57.1709 deg ; margin %.4f deg ; shell lemma at 2.09 holds: %s"
      % (57.1709021867-deg, deg<57.1709021867))
