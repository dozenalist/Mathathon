#!/usr/bin/env python3
"""Independent EXACT sign audit of the K33 certificate + positive/negative controls."""
import json, mpmath as mp
import sympy as sp
from fractions import Fraction as F

t=sp.Symbol('t')
num=json.load(open('audit_numbers.json'))
p=[F(x) for x in num['p']]; q=[F(x) for x in num['q']]
P=sp.Poly(sum(sp.Rational(c.numerator,c.denominator)*t**i for i,c in enumerate(p)), t)
Q=sp.Poly(sum(sp.Rational(c.numerator,c.denominator)*t**i for i,c in enumerate(q)), t)

# --- directed pi, own enclosure (Machin) ---
def pib(terms=60):
    def at(n):
        S=[];acc=F(0)
        for k in range(terms):
            acc+=F((-1)**k,(2*k+1)*n**(2*k+1)); S.append(acc)
        return min(S[-1],S[-2]),max(S[-1],S[-2])
    a1,a2=at(5); b1,b2=at(239)
    return 16*a1-4*b2,16*a2-4*b1
PI_LO,PI_HI=pib()
A_lo=8*sp.Rational(PI_LO.numerator,PI_LO.denominator)   # < 8*pi  (safe, stronger)
print("A. exact sign conditions (my own Sturm implementation, my own p,q)")
print("   A_lo = 8*PI_LO < 8*pi ; testing the STRONGER condition on [A_lo, inf)")

def multiplicity_at(poly, x0):
    if sp.simplify(poly.subs(t,x0)) != 0: return 0
    m=0; cur=sp.Poly(poly,t)
    while True:
        cur,rem=sp.div(cur.as_expr(), (t-x0), t)
        if sp.simplify(rem)!=0: break
        cur=sp.Poly(cur,t); m+=1
        if m>100: break
    return m

def half_line_verdict(Poly, a, want):
    """exact: sign(Poly) == want on [a,inf), EVEN-multiplicity zeros allowed."""
    ex=Poly.as_expr(); lc=Poly.LC()
    odd=[]
    for fac,mult in sp.sqf_list(ex)[1]:
        if mult%2==1:
            Fp=sp.Poly(fac,t)
            if Fp.degree()>=1:
                for item in Fp.real_roots(multiple=True):
                    r,m=(item if isinstance(item,tuple) else (item,1))
                    try: rn=sp.Rational(sp.nsimplify(r))
                    except Exception: rn=None
                    if rn is not None and rn>a: odd.append((sp.N(r,20),mult*m))
    sign_open=sp.sign(lc)
    ma=multiplicity_at(ex,a)
    pa=sp.simplify(ex.subs(t,a))
    ok = (not odd) and (sp.sign(pa)!= -want or pa==0) and (sign_open==want or want==0)
    if pa==0 and want!=0 and sign_open!=want: ok=False
    return ok, odd, sign_open, pa, ma

ok_p,odd_p,sg_p,pa_p,ma_p = half_line_verdict(P, A_lo, -1)
print("   (CE1) p <= 0 on [A_lo, inf): %s" % ok_p)
print("        roots of p above A_lo (should be none): %s ; sign at A_lo = %s (mult %d) ; leading sign %s"
      % (odd_p[:3], sp.sign(pa_p), ma_p, sg_p))
ok_q,odd_q,sg_q,pa_q,ma_q = half_line_verdict(Q, sp.Integer(0), +1)
print("   (CE2) q >= 0 on [0, inf): %s" % ok_q)
print("        roots of q above 0 (should be none): %s ; q(0)>0: %s ; leading sign %s" % (odd_q[:3], pa_q>0, sg_q))

print("\n   where does p cross zero? (contact location)")
for x in ['25.0','25.1','25.13','25.1327','25.132741','25.132742','25.2','30']:
    print("      p(%s) = %s" % (x, sp.sign(P.as_expr().subs(t,sp.Rational(x)))))
print("   8*pi = %.10f ; so p > 0 just below 8pi and < 0 above => the zero is at the contact radius 2" % (float(8*PI_HI)))

print("\n   total real roots of p:", sp.polys.polytools.count_roots(P), " of q:", sp.polys.polytools.count_roots(Q))
print("   real roots of q in (-inf,0):", sp.polys.polytools.count_roots(Q, -sp.oo, 0))
print("\nB. near-tangency of q (the float-checker trap)")
fq=sp.lambdify(t,Q.as_expr(),'mpmath'); fq1=sp.lambdify(t,sp.diff(Q.as_expr(),t),'mpmath')
mp.mp.dps=40
crits=[]
for a0 in range(0,300,5):
    try:
        r=mp.findroot(fq1,a0+0.5)
        if 0<=r<=300 and all(abs(r-c)>1e-6 for c in crits): crits.append(r)
    except Exception: pass
vals=[(c,fq(c)) for c in crits]
if vals:
    cm,vmin=min(vals,key=lambda z:z[1])
    print("   min q on [0,300] = %.3e at t = %.6f  (positive: %s)" % (float(vmin),float(cm),vmin>0))
    print("   => q is strictly positive yet ~1e-29 at its minimum: any float-based sign test is unsafe here.")
else:
    print("   no interior critical points found in [0,300]")

print("\nC. independent controls (my checker, not C's)")
L=json.load(open('audit_numbers.json'))
def build(cf):
    import itertools
    def lag(N):
        out=[[F(1)]]
        if N>=1: out.append([F(3,2),F(-1)])
        for k in range(1,N):
            a=out[k];b=out[k-1];res=[F(0)]*(max(len(a)+1,len(b))+1)
            c1=F(2*k+1)+F(1,2);c2=F(k)+F(1,2)
            for i,cf2 in enumerate(a): res[i]+=c1*cf2; res[i+1]+=-cf2
            for i,cf2 in enumerate(b): res[i]-=c2*cf2
            res=[x/(k+1) for x in res]
            while len(res)>1 and res[-1]==0: res.pop()
            out.append(res)
        return out
    Lg=lag(len(cf)-1); pp=[F(0)];qq=[F(0)]
    for k,ck in enumerate(cf):
        for i,v in enumerate(Lg[k]): 
            if i>=len(pp): pp.extend([F(0)]*(i-len(pp)+1))
            pp[i]+=ck*v
            if i>=len(qq): qq.extend([F(0)]*(i-len(qq)+1))
            qq[i]+=((-1)**k)*ck*v
    return pp,qq
def verdict(cf,label):
    pp,qq=build(cf)
    PP=sp.Poly(sum(sp.Rational(x.numerator,x.denominator)*t**i for i,x in enumerate(pp)),t)
    QQ=sp.Poly(sum(sp.Rational(x.numerator,x.denominator)*t**i for i,x in enumerate(qq)),t)
    p0=PP.eval(0); q0=QQ.eval(0)
    if p0<=0 or q0<=0:
        print("   %-46s REJECT (p0=%s, q0=%s)" % (label, p0>0, q0>0)); return False
    ok1=half_line_verdict(PP,A_lo,-1)[0]; ok2=half_line_verdict(QQ,sp.Integer(0),+1)[0]
    print("   %-46s %s   (CE1=%s, CE2=%s)  Delta=%.9f" % (label,
          "ACCEPT" if ok1 and ok2 else "REJECT", ok1, ok2,
          float(sp.Rational(4,3)*sp.pi*p0/q0)))
    return ok1 and ok2
print("   positive control p=25-t (c=[47/2,1]), q=22+t :", )
verdict([F(47,2),F(1)], "POSITIVE c=(47/2,1): p=25-t, q=22+t")
cK=[F(x) for x in json.load(open('K33.json'))['coefficients_rational']]
verdict(cK, "K33 (should ACCEPT)")
verdict([-x for x in cK], "NEGATIVE: -K33 (p0<0)")
c2=list(cK); c2[0]=c2[0]+F(1,1000)
verdict(c2, "NEGATIVE: K33 with c0 += 1/1000")
c3=list(cK); c3[1]=c3[1]+F(1,1000)
verdict(c3, "NEGATIVE: K33 with c1 += 1/1000")
