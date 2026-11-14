#!/usr/bin/env python3
"""Independent audit of Main's shell_check.fourier_map and threshold (bbad129d)."""
import math, sys
from fractions import Fraction as F
import sympy as sp
import numpy as np
from scipy.integrate import quad
sys.path.insert(0,'.')
import shell_check_main as SC

u=sp.Symbol('u'); t=sp.Symbol('t')
print("1. Main's fourier_map vs DIRECT 3-D quadrature (independent)")
print("   convention under test: f = P(u)e^{-pi r^2}, f^ = Q(u)e^{-pi r^2}, u = pi r^2")
K=3
M=SC.fourier_map(K)
print("   M (rows = output power of u, cols = input power of u):")
for i in range(K+1):
    print("      ", [str(M[i,j]) for j in range(K+1)])
for avec in ([1,0,0,0],[0,1,0,0],[1,-1,2,0],[F(1,2),F(-1,3),F(2,5),F(-1,7)]):
    a=[sp.Rational(x) for x in avec]
    b=[sum(M[i,j]*a[j] for j in range(K+1)) for i in range(K+1)]   # Q coefficients
    P=lambda uu: float(sum(a[i]*uu**i for i in range(K+1)))
    Qf=lambda uu: float(sum(b[i]*uu**i for i in range(K+1)))
    worst=0.0
    for T in (0.0,0.37,0.9,1.4):
        # f(x)=P(pi r^2) e^{-pi r^2}; radial FT in R^3
        g=lambda r: P(math.pi*r*r)*math.exp(-math.pi*r*r)*r*r
        gs=lambda r: P(math.pi*r*r)*math.exp(-math.pi*r*r)*r*math.sin(2*math.pi*T*r)
        if T==0: lhs=4*math.pi*quad(g,0,12,limit=400)[0]
        else:    lhs=(2/T)*quad(gs,0,12,limit=400)[0]
        rhs=Qf(math.pi*T*T)*math.exp(-math.pi*T*T)
        worst=max(worst,abs(lhs-rhs)/max(1e-12,abs(lhs)))
    print("   a=%-22s -> max rel. error vs quadrature = %.2e" % (str(avec), worst))

print("\n2. threshold direction (CE1 domain is |x|>=2  <=>  u >= 4*pi)")
print("   PI_LO =", float(SC.PI_LO), " PI_HI =", float(SC.PI_HI))
print("   T_LO = 4*PI_LO =", float(SC.T_LO), " <= 4*pi = %.10f ? %s" % (4*math.pi, float(SC.T_LO)<=4*math.pi))
print("   4*pi =", 4*math.pi, "; T_LO below it by %.3e (so testing on [T_LO,inf) is STRONGER => safe)"
      % (4*math.pi-float(SC.T_LO)))
print("   PI_LO < pi < PI_HI ?", float(SC.PI_LO)<math.pi<float(SC.PI_HI))

print("\n3. odd-part logic: even-multiplicity zeros must NOT count as sign changes")
uu=sp.Symbol('u')
for expr,expect in [(-(uu-3)**2,'kept'), (-(uu-3),'flag'), (-(uu-3)**2*(uu-5),'flag'),
                    ((uu-2)**2,'kept')]:
    od=SC._odd_part(sp.expand(expr))
    has_root_above = any(float(sp.N(r))>2.0 for r in sp.real_roots(od) if abs(float(sp.N(r).imag))<1e-12) if od.degree()>=1 else False
    # real_roots may be complex; use Poly
    P=sp.Poly(od,uu); real=[]
    if P.degree()>=1:
        for item in P.real_roots(multiple=True):
            r,m=(item if isinstance(item,tuple) else (item,1))
            if float(sp.N(r))>2.0: real.append(float(sp.N(r)))
    print("   %-16s odd part = %-18s roots above 2: %-12s (%s)"
          % (str(expr)[:16], str(sp.factor(od))[:18], str([round(x,6) for x in real]), expect))

print("\n4. does Main's own self-test run?")
try:
    import subprocess
    r=subprocess.run([sys.executable,'shell_check_main.py'],capture_output=True,text=True,timeout=120)
    print("   exit", r.returncode); print("   tail:", (r.stdout or '').strip().splitlines()[-3:])
except Exception as e:
    print("   self-test not runnable standalone:", type(e).__name__, e)
