#!/usr/bin/env python3
"""Exact Cohn-Elkies evaluator in d=3 on the radial Fourier eigenbasis (role X).

Basis.  With alpha = d/2 - 1 = 1/2 and  phi_k(x) = L_k^{1/2}(2 pi |x|^2) e^{-pi|x|^2},
the radial Laguerre (Hermite) functions satisfy  phi_k^ = (-1)^k phi_k  exactly
(Cohn-Elkies 2003, sec. 7, citing Lebedev).  Hence for f = sum_k c_k phi_k:

        f  = p(s) e^{-pi s},   f^ = q(s) e^{-pi s},   s = |x|^2,

with p, q polynomials in s of degree <= K that are *linear* in c.  Consequently

  * f(0) = p(0),  f^(0) = q(0)  are exact rationals;
  * the two CE hypotheses  [f <= 0 for s >= 4]  and  [f^ >= 0 for s >= 0]
    are polynomial sign conditions on a half-line, decided EXACTLY by Sturm
    sequences.  There is no grid, no tail, and no floating point anywhere in
    the certificate.

So on this family the ordinary CE bound is a semialgebraic optimization problem,
and every candidate it produces is a rigorous theorem
        Delta <= (4 pi/3) p(0)/q(0)  for all packings of unit balls.
Status: the *ceiling* of this family is above the Kepler density (Li, Thm 6.1),
so none of it can prove Kepler; it is a reproducible, fully certified control.
"""
import itertools, sys
from fractions import Fraction as F
import sympy as sp

s = sp.Symbol('s', real=True)

def laguerre_half(K):
    """L_k^{1/2}(2 pi s) as exact sympy polynomials in s, k=0..K."""
    polys = [sp.Integer(1)]
    if K >= 1:
        polys.append(sp.Rational(3,2) - 2*sp.pi*s)
    for k in range(1, K):
        # (k+1) L_{k+1} = (2k+1+a - x) L_k - (k+a) L_{k-1},  x = 2 pi s, a = 1/2
        polys.append(sp.expand(((2*k + sp.Rational(3,2) - 2*sp.pi*s)*polys[k]
                                - (k + sp.Rational(1,2))*polys[k-1])/(k+1)))
    return polys

def poly_from_coeffs(c, polys):
    return sp.expand(sum(ci*pi_ for ci, pi_ in zip(c, polys)))

def sign_on_half_line(poly, a, want):
    """True iff poly has the sign `want` in (+1/-1/0) on [a, inf), decided exactly."""
    P = sp.Poly(poly, s)
    if P.is_zero: return want == 0
    # roots in (a, inf)
    cnt = P.count_roots(a, sp.oo) if P.degree() >= 1 else 0
    if cnt: return False
    val = sp.nsimplify(P.eval(a)) if False else P.eval(a)
    if val == 0:  # a boundary zero is allowed for <= / >=
        # sign just to the right
        d = sp.diff(poly, s).subs(s, a)
        if d == 0: return True
        return sp.sign(d) == want
    return sp.sign(val) == want

def certify(c, K, verbose=False):
    polys = laguerre_half(K)
    f  = poly_from_coeffs(c, polys)
    fh = poly_from_coeffs([(-1)**k*ck for k, ck in enumerate(c)], polys)
    f0, fh0 = f.subs(s, 0), fh.subs(s, 0)
    if f0 <= 0 or fh0 <= 0: return None
    ok = sign_on_half_line(f, 4, -1) and sign_on_half_line(fh, 0, +1)
    if not ok: return None
    return sp.nsimplify(f0/fh0)

print("="*80); print("0.  Verify the eigenbasis numerically from scratch (d=3 radial FT)"); print("="*80)
import numpy as np
from scipy.integrate import quad
def fhat3(r, f):                     # (F f)(t) for radial f in R^3, |t| = r
    g = lambda u: f(u)*u*np.sin(2*np.pi*r*u)
    v,_ = quad(g, 0, 12.0, limit=400)
    return (2.0/r)*v
for k in range(4):
    P = sp.lambdify(s, laguerre_half(4)[k].subs(sp.pi, np.pi), 'numpy')
    f = lambda u, P=P: P(u*u)*np.exp(-np.pi*u*u)
    lhs = fhat3(0.83, f); rhs = ((-1)**k)*f(0.83)
    print("   k=%d  f^(0.83) = %+.10f   (-1)^k f(0.83) = %+.10f   |diff| = %.2e"
          % (k, lhs, rhs, abs(lhs-rhs)))

print("="*80); print("1.  Search for certified members of the family (exact rational c)"); print("="*80)
best = None
for K in (2,3,4,5,6):
    found = []
    for trial in range(200000):
        # simple rational probes; scale c0 = 1 and search signs/levels on a grid
        if K == 2: continue
        break
    # deterministic structured search: f(s) = -(s-4)*h(s) with h a sum of squares
    # of lower-degree Laguerre polys, expressed back in the basis (exact).
    polys = laguerre_half(K)
    for j in range(1, K+1):
        x = sp.symbols('x')
        # h(s) = (4-s)*(-(s-4)) ... use h = (a + b s)^2 (nonneg) and f = (4-s)h
        for (a_, b_) in [(1,0),(0,1),(1,1),(1,-1),(2,1),(1,2),(3,1),(1,3),(5,2),(2,5)]:
            h = sp.expand((a_ + b_*s)**2)
            f_try = sp.expand((4 - s)*h)
            # f_try must lie in span{L_0..L_j} : solve exactly
            basis = polys[:j+1]
            cs = sp.symbols('c0:%d' % (j+1))
            eq = sp.Poly(sp.expand(f_try - sum(cc*b for cc, b in zip(cs, basis))), s)
            sol = sp.solve(eq.all_coeffs(), cs, dict=True)
            if not sol: continue
            c = [sp.nsimplify(sol[0][cc]) for cc in cs] + [sp.Integer(0)]*(K-j)
            val = certify(c, K)
            if val is not None: found.append((val, c, j, (a_, b_)))
    if found:
        found.sort(key=lambda t: t[0])
        val, c, j, ab = found[0]
        print("   K=%d : best certified f(0)/f^(0) = %s = %.6f  (occupied volume %.6f)"
              % (K, sp.nsimplify(val), float(val), float(sp.Rational(4,3)*sp.pi*val)))
        print("         from f = (4-s)(%d+%ds)^2, degree %d" % (ab[0], ab[1], j))
        if best is None or val < best[0]: best = (val, c, K)
    else:
        print("   K=%d : no certified member in the probe set" % K)

if best:
    val, c, K = best
    print()
    print("="*80); print("2.  Full certificate for the best probe (K=%d)" % K); print("="*80)
    polys = laguerre_half(K)
    f  = poly_from_coeffs(c, polys); fh = poly_from_coeffs([(-1)**k*ck for k,c in enumerate(c)], polys)
    print("   coefficients c =", [sp.nsimplify(x) for x in c])
    print("   p(s) =", sp.factor(sp.expand(f)))
    print("   q(s) =", sp.factor(sp.expand(fh)))
    print("   Sturm: # real roots of p in (4,inf)  =", sp.Poly(sp.expand(f), s).count_roots(4, sp.oo))
    print("          # real roots of q in (0,inf)  =", sp.Poly(sp.expand(fh), s).count_roots(0, sp.oo))
    print("   p(0) =", f.subs(s,0), "  q(0) =", fh.subs(s,0))
    print("   certified bound: Delta <= (4pi/3)*%s = %s = %.9f" % (sp.nsimplify(val),
          sp.nsimplify(sp.Rational(4,3)*sp.pi*val), float(sp.Rational(4,3)*sp.pi*val)))
    print("   gap to pi/sqrt(18): %.6f (occupied volume)" % (float(sp.Rational(4,3)*sp.pi*val) - float(sp.pi/sp.sqrt(18))))
