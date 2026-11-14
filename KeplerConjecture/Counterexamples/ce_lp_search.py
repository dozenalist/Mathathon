#!/usr/bin/env python3
"""Exploratory LP search inside the exact-certifiable Laguerre-Gaussian family.

minimise p(0) subject to  p(s)<=0 (s>=4), q(s)>=0 (s>=0), q(0)=1,
where p=f/sqrt-normalisation polynomial, q = parity-flipped partner.
Both constraint families are LINEAR in the coefficients c, so this is an LP on a
grid; the grid is only a SEARCH device.  Every candidate is afterwards certified
exactly by Sturm sequences in ce_laguerre_exact.certify, so the resulting bound
is a theorem regardless of the grid.
"""
import numpy as np, sympy as sp
from scipy.optimize import linprog
from fractions import Fraction as F

s = sp.Symbol('s', real=True)
def lag(K):
    P=[sp.Integer(1)]
    if K>=1: P.append(sp.Rational(3,2)-2*sp.pi*s)
    for k in range(1,K):
        P.append(sp.expand(((2*k+sp.Rational(3,2)-2*sp.pi*s)*P[k]-(k+sp.Rational(1,2))*P[k-1])/(k+1)))
    return P

def build(K, ngrid=400, margin=1e-7):
    P = lag(K)
    L  = sp.lambdify(s, P, 'numpy') if False else None
    f  = [np.array([float(sp.N(p.subs(s, v), 30)) for p in P]) for v in
          np.concatenate([np.linspace(4, 60, ngrid), np.linspace(60, 400, 60)])]
    sv = np.concatenate([np.linspace(4, 60, ngrid), np.linspace(60, 400, 60)])
    q  = [np.array([float(sp.N(((-1)**k*p).subs(s, v), 30)) for k,p in enumerate(P)]) for v in
          np.concatenate([np.linspace(0, 60, ngrid), np.linspace(60, 400, 60)])]
    sq = np.concatenate([np.linspace(0, 60, ngrid), np.linspace(60, 400, 60)])
    c0 = np.array([float(sp.N(p.subs(s,0),30)) for p in P])          # p(0)=c.L(0)
    cq0= np.array([float(sp.N(((-1)**k*p).subs(s,0),30)) for k,p in enumerate(P)])  # q(0)
    return P, f, q, c0, cq0

def search(K, verbose=False):
    P, frows, qrows, c0, cq0 = build(K)
    # variables c (K+1).  objective p(0) = c0 . c  ;  normalise q(0)=1
    A_ub = np.vstack([np.array(frows), -np.array(qrows)])            # p(s)<=0 ; -q(s)<=0
    b_ub = np.full(A_ub.shape[0], -1e-9)                             # strictly negative p, keep q>=0
    A_ub[-len(qrows):] = -np.array(qrows); b_ub[-len(qrows):] = 0.0
    A_eq = cq0.reshape(1,-1); b_eq=[1.0]
    res = linprog(c0, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq,
                  bounds=[(None,None)]*(K+1), method='highs')
    if not res.success: return None
    return res.x, res.fun

def to_exact(c, den=10**7):
    fr = [F(int(round(x*den)), den) for x in c]
    return [sp.Rational(f.numerator, f.denominator) for f in fr]

# exact certifier (kept in one place)
def sign_ok(poly, a, want):
    Pp = sp.Poly(poly, s)
    if Pp.is_zero: return want==0
    if Pp.degree()>=1 and Pp.count_roots(a, sp.oo)!=0: return False
    v = Pp.eval(a)
    if v==0:
        d = sp.diff(poly,s).subs(s,a)
        return True if d==0 else sp.sign(d)==want
    return sp.sign(v)==want

def certify(c, P):
    f  = sp.expand(sum(ci*p for ci,p in zip(c,P)))
    fh = sp.expand(sum(((-1)**k)*ci*p for k,ci in enumerate(c) for p in [P[k]]))
    f0, fh0 = f.subs(s,0), fh.subs(s,0)
    if f0<=0 or fh0<=0: return None
    if not (sign_ok(sp.expand(f),4,-1) and sign_ok(sp.expand(fh),0,1)): return None
    return (sp.nsimplify(f0/fh0), f, fh, f0, fh0)

print("="*84); print(" LP-guided search + exact Sturm certification, d=3, separation 2"); print("="*84)
rows=[]
for K in range(1, 11):
    out = search(K)
    if out is None:
        print("   K=%2d  LP infeasible on the grid" % K); continue
    x, obj = out
    P = lag(K)
    cert = None
    for den in (10**7, 10**6, 10**5, 10**4):
        cert = certify(to_exact(x, den), P)
        if cert: break
    if cert is None:
        print("   K=%2d  LP value %.6f but exact certification FAILED (rounding)" % (K, obj)); continue
    val, f, fh, f0, fh0 = cert
    occ = float(sp.Rational(4,3)*sp.pi*val)
    rows.append((K, val, occ))
    print("   K=%2d  certified bound: f(0)/f^(0) = %-14s occupied volume = %.6f   gap = %.6f"
          % (K, str(val)[:14], occ, occ-float(sp.pi/sp.sqrt(18))))
if rows:
    K,val,occ = min(rows, key=lambda t:t[2])
    print()
    print("   best certified in this family: K=%d, occupied volume %.6f" % (K,occ))
    print("   (Kepler pi/sqrt18 = %.9f ; Li forbids reaching it inside ordinary CE)" % float(sp.pi/sp.sqrt(18)))
