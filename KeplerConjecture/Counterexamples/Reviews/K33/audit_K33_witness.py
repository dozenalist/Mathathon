#!/usr/bin/env python3
"""Refine the q minimum, build PROPER negative controls, and find a minimal witness."""
import json, mpmath as mp
import sympy as sp
from fractions import Fraction as F
t=sp.Symbol('t')
num=json.load(open('audit_numbers.json'))
q=[F(x) for x in num['q']]
Qe=sum(sp.Rational(c.numerator,c.denominator)*t**i for i,c in enumerate(q))
print("1. where is q's minimum on [0,300]?  (C's note says ~3.5e-29)")
mp.mp.dps=50
fq=sp.lambdify(t,Qe,'mpmath')
xs=[mp.mpf(k)*300/6000 for k in range(6001)]
vals=[(x,fq(x)) for x in xs]
cm,vmin=min(vals,key=lambda z:z[1])
print("   grid (6001 pts): min = %.6e at t = %.6f" % (float(vmin),float(cm)))
# refine with high-precision root of q'
fq1=sp.lambdify(t,sp.diff(Qe,t),'mpmath')
try:
    cstar=mp.findroot(fq1,cm)
    if abs(cstar-cm)<1: print("   refined critical point t* = %.12f, q(t*) = %.6e" % (float(cstar),float(fq(cstar))))
except Exception as e: print("   refine failed:",e)
print("   smallest sampled value: %.6e ; is C's 3.5e-29 reproduced? %s"
      % (float(vmin), abs(float(vmin)-3.5e-29)<1e-25))

print("\n2. PROPER negative controls (synthetic, testing the exact test itself)")
def verdict_expr(expr, a, want, label):
    Poly=sp.Poly(sp.expand(expr),t)
    odd=[]
    for fac,mult in sp.sqf_list(sp.expand(expr))[1]:
        if mult%2==1:
            Fp=sp.Poly(fac,t)
            if Fp.degree()>=1:
                for item in Fp.real_roots(multiple=True):
                    r,m=(item if isinstance(item,tuple) else (item,1))
                    try: rn=sp.Rational(sp.nsimplify(r))
                    except Exception: rn=None
                    if rn is not None and rn>a: odd.append((sp.N(r,12),mult*m))
    lc=sp.sign(Poly.LC()); pa=sp.simplify(expr.subs(t,a))
    ok = (not odd) and lc==want and not (sp.sign(pa)==-want)
    print("   %-42s -> %s  (odd roots above a: %s)" % (label, "ACCEPT" if ok else "REJECT", odd[:2]))
    return ok
A= sp.Rational(25132741228718345907,10**18)   # ~8*pi lower
print("   CE1 synthetic:")
verdict_expr(-(t-30), A, -1, "p=-(t-30): simple root at 30 (should REJECT)")
verdict_expr(-(t-30)**2, A, -1, "p=-(t-30)^2: double root (should ACCEPT)")
verdict_expr(-(t-30)**2*(t-40), A, -1, "p=-(t-30)^2(t-40): simple root at 40 (REJECT)")
print("   CE2 synthetic:")
verdict_expr((t-5)**2, 0, 1, "q=(t-5)^2: double root (should ACCEPT)")
verdict_expr((t-5), 0, 1, "q=t-5: simple root inside (should REJECT)")
verdict_expr((t-5)**2*(t-7), 0, 1, "q=(t-5)^2(t-7): simple root at 7 (REJECT)")

print("\n3. minimal witness: how far must ONE coefficient move to break K33?")
cK=[F(x) for x in json.load(open('K33.json'))['coefficients_rational']]
def lag(N):
    out=[[F(1)]]
    if N>=1: out.append([F(3,2),F(-1)])
    for k in range(1,N):
        a=out[k];b=out[k-1];res=[F(0)]*(max(len(a)+1,len(b))+1)
        c1=F(2*k+1)+F(1,2);c2=F(k)+F(1,2)
        for i,cf in enumerate(a): res[i]+=c1*cf; res[i+1]+=-cf
        for i,cf in enumerate(b): res[i]-=c2*cf
        res=[x/(k+1) for x in res]
        while len(res)>1 and res[-1]==0: res.pop()
        out.append(res)
    return out
Lg=lag(len(cK)-1)
def certifies(cf):
    pp=[F(0)];qq=[F(0)]
    for k,ck in enumerate(cf):
        for i,v in enumerate(Lg[k]):
            while i>=len(pp): pp.append(F(0))
            while i>=len(qq): qq.append(F(0))
            pp[i]+=ck*v; qq[i]+=((-1)**k)*ck*v
    PP=sp.Poly(sum(sp.Rational(x.numerator,x.denominator)*t**i for i,x in enumerate(pp)),t)
    QQ=sp.Poly(sum(sp.Rational(x.numerator,x.denominator)*t**i for i,x in enumerate(qq)),t)
    if PP.eval(0)<=0 or QQ.eval(0)<=0: return False
    def ok(Poly,a,want):
        ex=Poly.as_expr(); lc=sp.sign(Poly.LC())
        for fac,mult in sp.sqf_list(ex)[1]:
            if mult%2==1:
                Fp=sp.Poly(fac,t)
                if Fp.degree()>=1:
                    for item in Fp.real_roots(multiple=True):
                        r,m=(item if isinstance(item,tuple) else (item,1))
                        try: rn=sp.Rational(sp.nsimplify(r))
                        except Exception: rn=None
                        if rn is not None and rn>a: return False
        if lc!=want: return False
        pa=sp.simplify(ex.subs(t,a))
        return not (sp.sign(pa)==-want)
    return ok(PP,A,-1) and ok(QQ,sp.Integer(0),1)
print("   baseline certifies:", certifies(cK))
for idx,name in [(0,'c0'),(5,'c5'),(16,'c16'),(33,'c33')]:
    lo,hi=F(0),F(1)   # search delta in [0,1]; find smallest power-of-10 grid delta that breaks
    broken=None
    for e in range(1,14):
        d=F(1,10**e)
        for s in (+1,-1):
            c2=list(cK); c2[idx]=c2[idx]+s*d
            if not certifies(c2): broken=(s*d,e); break
        if broken: break
    print("   %-4s: smallest breaking |delta| on a 10^-e grid: %s" % (name, broken))
