"""Numerical validation of the estimates of Theorem B (explicit delta* = 1/100).

Definitions follow dstar.md:
  rho(t) = |d+e^{it}|, Th(t) = t + arg(1+d e^{-it}), beta(t) = arccos(rho/2),
  alpha_pm(t) = Th(t) +- beta(t), H = alpha_+ o alpha_-^{-1}, F = H - 2 pi/3,
  F_j(t) = j pi/3 + F(t - j pi/3).

Checks
 (1) the identity e^{i alpha_+} + e^{i alpha_-} = d + e^{it}                        [eq (P2)]
 (2) F(t) = t + 2 beta(sigma(t)) - 2 pi/3                                           [eq (P3)]
 (3) F'(t) = 1 + 2 beta'(sigma(t)) / alpha_-'(sigma(t))   (finite differences)      [eq (P4)]
 (4) F''(t) formula                                                                 [eq (P4)]
 (5) the paper's (5.9) first-order law  F(t)-t = (2d/sqrt3) sin(t-pi/6) + O(d^2)
 (6) the bounds of (5.10) with c_0 = 1/2, C_0 = 2 at d = 1/100 (and larger d)
 (7) the aux bounds of Lemmas B, C, D, E at d = 1/100
"""
import numpy as np
from math import atan2, acos, cos, sin, sqrt, pi

kap = pi/3

def rho(t, d):  return sqrt(1 + 2*d*cos(t) + d*d)
def Th(t, d):   return t + atan2(-d*sin(t), 1 + d*cos(t))
def beta(t, d): return acos(rho(t, d)/2)
def b1(t, d):
    r = rho(t, d); return d*sin(t)/(r*sqrt(4-r*r))
def b2(t, d):
    r = rho(t, d)
    h  = 1/(r*sqrt(4-r*r))
    hp = (2*r*r - 4)/(r*r*(4-r*r)**1.5)
    return d*cos(t)*h - d*d*sin(t)*sin(t)*hp/r
def T1(t, d):
    r = rho(t, d); return (1 + d*cos(t))/(r*r)
def T2(t, d):
    r = rho(t, d); return d*sin(t)*(r*r - 2*(d*cos(t) + d*d))/r**4
def alpha_minus(s, d): return Th(s, d) - beta(s, d)
def amin1(s, d):       return T1(s, d) - b1(s, d)
def amin2(s, d):       return T2(s, d) - b2(s, d)

def sigma(t, d):
    """alpha_-^{-1}(t), Newton from s=t (alpha_- is a degree-one diffeomorphism)."""
    s = t
    for _ in range(60):
        s -= (alpha_minus(s, d) - t)/amin1(s, d)
    return s

def F(t, d):    s = sigma(t, d); return t + 2*beta(s, d) - 2*kap
def Fp(t, d):   s = sigma(t, d); return 1 + 2*b1(s, d)/amin1(s, d)
def Fpp(t, d):
    s = sigma(t, d)
    a1, a2 = amin1(s, d), amin2(s, d)
    return (2*b2(s, d)*a1 - 2*b1(s, d)*a2)/a1**3

d0 = 1e-2
ts = np.linspace(-pi, pi, 4001)

# (1) representation identity
e1 = max(abs(cos(Th(t,d0)+beta(t,d0)) + cos(Th(t,d0)-beta(t,d0)) - (d0 + cos(t)))
         + abs(sin(Th(t,d0)+beta(t,d0)) + sin(Th(t,d0)-beta(t,d0)) - sin(t)) for t in ts)
print(f"(1) max |e^(i a+) + e^(i a-) - (d+e^it)| = {e1:.3e}")

# (2) F via (P3): compare with a direct composition H = a+ o a-^{-1}
print(f"(2) max |F(t) - (t + 2 beta(sigma) - 2k)| = {max(abs(F(t,d0) - (t + 2*beta(sigma(t,d0),d0) - 2*kap)) for t in ts):.3e}")

# (3),(4) finite-difference checks of F' and F''
hh = 1e-6
e3 = max(abs((F(t+hh,d0)-F(t-hh,d0))/(2*hh) - Fp(t,d0)) for t in ts[5:-5])
e4 = max(abs((Fp(t+1e-5,d0)-Fp(t-1e-5,d0))/2e-5 - Fpp(t,d0)) for t in ts[5:-5])
print(f"(3) max |FD(F) - F'|  = {e3:.3e}      (4) max |FD(F') - F''| = {e4:.3e}")

# (5) first-order law of (5.9)
for d in (1e-3, 1e-2):
    res = max(abs(F(t,d) - t - (2*d/sqrt(3))*sin(t - pi/6)) for t in ts)/d**2
    print(f"(5) d={d:.0e}: sup |F(t)-t-(2d/sqrt3)sin(t-pi/6)| / d^2 = {res:.4f}")

# (6) displayed (5.10) with c_0=1/2, C_0=2
print("(6)  d        min_t max_j (F_j-t)/d   min_t max_j (F_j'-1)/d   sup|F-t|/d   sup|F'-1|/d   sup|F''|/d   [need >=1/2, >=1/2, <=2, <=2, <=2]")
for d in (1e-4, 1e-3, 1e-2):
    Fjs  = np.array([[F(t-j*kap,d)-(t-j*kap) for t in ts] for j in range(6)])
    Fpjs = np.array([[Fp(t-j*kap,d)-1      for t in ts] for j in range(6)])
    print(f"     {d:8.0e}   {np.min(np.max(Fjs,axis=0))/d:14.5f}   {np.min(np.max(Fpjs,axis=0))/d:18.5f}"
          f"   {np.max(np.abs([F(t,d)-t for t in ts]))/d:10.5f}   {np.max(np.abs([Fp(t,d)-1 for t in ts]))/d:10.5f}"
          f"   {np.max(np.abs([Fpp(t,d) for t in ts]))/d:10.5f}")

# (7) the auxiliary bounds, all in units of d (or d^2)
d = 1e-2
supPhi  = max(abs(Th(t,d)-t) for t in ts)/d
supT1   = max(abs(T1(t,d)-1) for t in ts)/d
supT2   = max(abs(T2(t,d)) for t in ts)/d
supb    = max(abs(beta(t,d)-kap) for t in ts)/d
supb1   = max(abs(b1(t,d)) for t in ts)/d
supb2   = max(abs(b2(t,d)) for t in ts)/d
supb1d  = max(abs(b1(t,d)-(d/sqrt(3))*sin(t)) for t in ts)/d**2
supD    = max(abs(2*beta(t,d)-2*kap+(2*d/sqrt(3))*cos(t)) for t in ts)/d**2
supam1  = max(abs(amin1(t,d)-1) for t in ts)/d
supam2  = max(abs(amin2(t,d)) for t in ts)/d
supinv  = max(abs(sigma(t,d)-(t+kap)) for t in ts)/d
print(f"""(7) d=1e-2, quoted bound in parentheses:
    |Theta-t|/d      = {supPhi:.4f}  (<=1.02)     |Theta'-1|/d  = {supT1:.4f}  (<=1.04)
    |Theta''|/d      = {supT2:.4f}  (<=1.09)      |beta-k|/d    = {supb:.4f}   (<=0.60)
    |beta'|/d        = {supb1:.4f}  (<=0.586)     |beta''|/d    = {supb2:.4f}  (<=0.590)
    |beta'-(d/r3)s|/d^2 = {supb1d:.4f} (<=0.42)   |2beta-2k+(2d/r3)cos|/d^2 = {supD:.4f} (<=1.38)
    |alpha_-'-1|/d   = {supam1:.4f} (<=1.63)      |alpha_-''|/d = {supam2:.4f} (<=1.68)
    |sigma(t)-(t+k)|/d = {supinv:.4f} (<=1.65)""")
