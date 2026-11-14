#!/usr/bin/env python3
"""THIRD-OPINION cross-check of C's K33: convert to Main's u-basis and run MAIN's checker.
Exact conversion: u = t/2, so P(u)=p(2u)=sum c_k L_k(2u) and Q(u)=sum (-1)^k c_k L_k(2u)."""
import json, sys
from fractions import Fraction as F
import sympy as sp
sys.path.insert(0,'.')
import shell_check_main as SC
import importlib.util
spec=importlib.util.spec_from_file_location("ak","K33/audit_K33.py")
u=sp.Symbol('u'); t=sp.Symbol('t')
def lag_t(j):
    return sp.expand(sp.assoc_laguerre(j, sp.Rational(1,2), t))
c=[F(x) for x in json.load(open('K33/K33.json'))['coefficients_rational']]
K=len(c)-1
# a = monomial coefficients in u of sum c_k L_k(2u)
Pexpr=sp.expand(sum(sp.Rational(x.numerator,x.denominator)*lag_t(k).subs(t,2*u) for k,x in enumerate(c)))
Ppoly=sp.Poly(Pexpr,u); a=[Ppoly.coeff_monomial(u**i) for i in range(K+1)]
Qexpr=sp.expand(sum(((-1)**k)*sp.Rational(x.numerator,x.denominator)*lag_t(k).subs(t,2*u) for k,x in enumerate(c)))
Qpoly=sp.Poly(Qexpr,u); b_mine=[Qpoly.coeff_monomial(u**i) for i in range(K+1)]
M=SC.fourier_map(K)
b_M=[sum(M[i,j]*sp.Rational(a[j]) for j in range(K+1)) for i in range(K+1)]
print("1. does Main's fourier_map reproduce the direct conversion on a REAL degree-33 vector?")
print("   b via fourier_map == b via direct L_k(2u) expansion:", [sp.simplify(x-y) for x,y in zip(b_M,b_mine)]==[0]*(K+1))
print("2. Main's checker on C's certificate (converted)")
print("   p(0)=%s (p>0: %s) ; q(0)=%s (q>0: %s)" % (a[0], a[0]>0, b_mine[0], b_mine[0]>0))
ok_ray=SC._ray(a, SC.T_LO)
print("   CE1  Main _ray(a, T_LO)          -> p <= 0 on [T_LO,inf): %s" % ok_ray)
ok_nn=SC.nonneg_on_half_line(b_mine)
print("   CE2  Main nonneg_on_half_line(b) -> q >= 0 on [0,inf):   %s" % ok_nn)
print("3. bound recomputed by Main's constants")
r=sp.Rational(a[0])/sp.Rational(b_mine[0])
lo=F(4,3)*F(SC.PI_LO)*F(r.p,F(r.q)); hi=F(4,3)*F(SC.PI_HI)*F(r.p,F(r.q))
print("   Delta in [%.15f, %.15f]  (C's delta_upper_exact >= this: %s)"
      % (float(lo),float(hi), F(json.load(open('K33/K33.json'))['delta_upper_exact'])>=hi))
print("VERDICT:", "ACCEPT (third independent implementation agrees)" if (ok_ray and ok_nn and a[0]>0 and b_mine[0]>0) else "DISAGREEMENT")
