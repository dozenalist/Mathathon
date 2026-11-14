#!/usr/bin/env python3
"""CE certificate machinery for the FREE-WIDTH Gaussian family (X-R03).

Family.  f(x) = P(|x|^2) e^{-a|x|^2},  P in Q[s],  a in Q_{>0}.
Threshold for CE1 is |x| >= 2, i.e. s >= 4 (rational, independent of a).

Exact Fourier map.  Let A_n(w) := (-d/dmu)^n [ mu^{-3/2} e^{-w/mu} ]_{mu=1},
computed exactly by differentiation (the a=1 polynomials).  Then
    FT[s^n e^{-a s}](t) = pi^{3/2} a^{-3/2-n} A_n(w) e^{-w},   w = pi^2|t|^2/a,
so with Q(w) := sum_n c_n a^{-n} A_n(w):
    f^(t) = pi^{3/2} a^{-3/2} Q(w) e^{-w},    f(0) = P(0) = c_0,   f^(0) = pi^{3/2}a^{-3/2}Q(0).
Density.  (4 pi/3) f(0)/f^(0) = (4 a^{3/2}/(3 sqrt pi)) P(0)/Q(0).
Kepler.  For P0,Q0 > 0:  (4a^{3/2}/(3 sqrt pi)) P0/Q0 < pi/sqrt18
         <=> 4 a^{3/2} sqrt18 P0 < 3 pi^{3/2} Q0  <=>  32 a^3 P0^2 < pi^3 Q0^2
         (squaring twice, all quantities positive).  a=1 recovers 32P0^2 < pi^3 Q0^2.
"""
import sympy as sp, math
from fractions import Fraction as Fr
import numpy as np

w_ = sp.Symbol('w'); s_ = sp.Symbol('s')

def A_polys(N):
    """A_n(w) for n=0..N, exact, rational coefficients."""
    lam = sp.Symbol('lambda', positive=True)
    A = lam**sp.Rational(-3,2); out=[]
    for n in range(N+1):
        if n > 0:
            A = -sp.diff(A, lam) - (w_/lam**2)*A
        out.append(sp.expand(A.subs(lam,1)))
    return out

def PI_Q(P, a, N=None):
    """Exact Q(w) with f^ = pi^{3/2} a^{-3/2} Q(w) e^{-w}."""
    a = sp.Rational(a); P = sp.expand(P)
    N = N if N is not None else sp.Poly(P, s_).degree()
    As = A_polys(N); coeffs = sp.Poly(P, s_).all_coeffs()[::-1]
    return sp.expand(sum(c*a**(-n)*As[n] for n, c in enumerate(coeffs)))

def _atan_inv_bounds(n, terms=48):
    S=[]; acc=Fr(0)
    for k in range(terms):
        acc += Fr((-1)**k, (2*k+1)*n**(2*k+1)); S.append(acc)
    return min(S[-1],S[-2]), max(S[-1],S[-2])
def pi_bounds(terms=48):
    a_lo,a_hi=_atan_inv_bounds(5,terms); b_lo,b_hi=_atan_inv_bounds(239,terms)
    return 16*a_lo-4*b_hi, 16*a_hi-4*b_lo

def kepler_ok(P0, Q0, a):
    """Three-valued exact test of 32 a^3 P0^2 < pi^3 Q0^2  (True/False/None)."""
    P0=Fr(P0); Q0=Fr(Q0); a=Fr(a)
    if P0<=0 or Q0<=0 or a<=0: return False
    R = 32*a**3*P0*P0/(Q0*Q0)
    lo,hi = pi_bounds()
    if R < lo**3: return True
    if R > hi**3: return False
    return None

def density(P0,Q0,a):
    return sp.Rational(4,3)*sp.Rational(a)**sp.Rational(3,2)/sp.sqrt(sp.pi)*sp.Rational(P0)/sp.Rational(Q0)

if __name__ == "__main__":
    import ce_exact_gauss as G
    print("="*80); print("1. Verify the free-width map against 3-D radial quadrature"); print("="*80)
    from scipy.integrate import quad
    tests=[(1-s_/8, sp.Rational(1,2)), (1-s_/8, 1), (1-s_/8, 2),
           (3-s_*sp.Rational(1,2)+s_**2/40, sp.Rational(3,2))]
    for P,a in tests:
        Q=PI_Q(P,a); f=sp.lambdify(s_,P,'numpy'); fh=sp.lambdify(w_,Q,'numpy'); a=sp.Rational(a)
        for T in (0.0, 0.7):
            if T==0:
                g=lambda r: f(r*r)*math.exp(-float(a)*r*r)*r*r
                lhs=4*math.pi*quad(g,0,14,limit=400)[0]
            else:
                g=lambda r: f(r*r)*math.exp(-float(a)*r*r)*r*math.sin(2*math.pi*T*r)
                lhs=(2/T)*quad(g,0,14,limit=400)[0]
            ww=math.pi**2*T*T/float(a)
            rhs=float(sp.pi**sp.Rational(3,2)*a**sp.Rational(-3,2))*fh(ww)*math.exp(-ww)
            print("   a=%-4s T=%.1f  quad=%+.10f  exact=%+.10f  |d|=%.1e" % (a,T,lhs,rhs,abs(lhs-rhs)))
    print("="*80); print("2. Widths: control and Kepler test at a != 1"); print("="*80)
    print("   control P = 2 - 2s/3  =>  Q = 2 - (1/a) + 2w/(3a), Q(0) = 2 - 1/a >= 0 iff a >= 1/2")
    for a in [sp.Rational(1,2), 1, 2, 4, sp.Rational(3,2)]:
        Q=PI_Q(2-sp.Rational(2,3)*s_, a)
        Q0=Q.subs(w_,0); P0=2
        print("      a=%-4s Q(w)=%-28s Q(0)=%-6s density=%s"
              % (a, str(sp.expand(Q))[:28], Q0, sp.nsimplify(density(P0,Q0,a))))
    print("   kepler_ok(P0=2,Q0=1,a): " + ", ".join("a=%s->%s" % (a, kepler_ok(2,1,a))
          for a in [sp.Rational(1,2),1,2,4]))
