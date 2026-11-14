import json, sympy as sp
from fractions import Fraction as F
t=sp.Symbol('t')
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
A=sp.Rational(25132741228718345907,10**18)
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
        ex=Poly.as_expr()
        if sp.sign(Poly.LC())!=want: return False
        if sp.simplify(ex.subs(t,a))!=0 and sp.sign(ex.subs(t,a))==-want: return False
        for fac,mult in sp.sqf_list(ex)[1]:
            if mult%2==1:
                Fp=sp.Poly(fac,t)
                if Fp.degree()>=1:
                    for item in Fp.real_roots(multiple=True):
                        r,m=(item if isinstance(item,tuple) else (item,1))
                        try: rn=sp.Rational(sp.nsimplify(r))
                        except Exception: rn=None
                        if rn is not None and rn>a: return False
        return True
    return ok(PP,A,-1) and ok(QQ,sp.Integer(0),1)
print("minimal single-coefficient witness (bisection in delta, sign + and -):")
for idx in (0,5,16,33):
    best={}
    for sgn in (+1,-1):
        lo,hi=F(0),F(1,2)     # lo certifies, hi must break
        c2=list(cK); c2[idx]=c2[idx]+sgn*hi
        if certifies(c2): print("   c%d sign%+d: even 1/2 does not break"%(idx,sgn)); continue
        for _ in range(24):
            mid=(lo+hi)/2; c2=list(cK); c2[idx]=c2[idx]+sgn*mid
            if certifies(c2): lo=mid
            else: hi=mid
        best[sgn]=hi
    for sgn,v in best.items():
        print("   c%-3d sign%+d : certificate breaks for |delta| >= %s = %.3e" % (idx,sgn,v,float(v)))
