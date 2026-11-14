#!/usr/bin/env python3
"""Exact CE certificate machinery for a RATIONAL family with an EXACT Fourier map.

Why the previous X-R01 was not decidable
----------------------------------------
`ce_laguerre_exact.py` used the basis L_k^{1/2}(2*pi*s), whose coefficients are in
Q[pi]: writing them as rationals is wrong, and its success test ("no real roots")
rejects legitimate nonnegative polynomials with even-multiplicity zeros — which is
exactly the case at a contact radius, where f(2)=0 is required.

The family used here
--------------------
    f(x) = P(|x|^2) e^{-|x|^2},      P in Q[s]        (s = |x|^2)
so every coefficient is rational and the CE threshold |x| >= 2 is the rational
half-line s >= 4.

The exact Fourier map (no pi in any coefficient)
-----------------------------------------------
    P(s) -> Q(v),   v = pi^2 |t|^2,     f^(t) = pi^{3/2} Q(v) e^{-v},
obtained from  (d/dlambda)^n of  (pi/lambda)^{3/2} e^{-pi^2|t|^2/lambda}  at lambda=1,
which is a linear map Q[s] -> Q[v] (rational, exact).  Both sign conditions are then
polynomial conditions on rational half-lines:
    (CE1)  P(s) <= 0  for s >= 4          (CE2)  Q(v) >= 0  for v >= 0.
Neither needs pi, grids or tails.  The final bound is
    (4 pi/3) f(0)/f^(0) = (4/(3 sqrt(pi))) P(0)/Q(0),
because f(0)=P(0) and f^(0)=pi^{3/2}Q(0), so (4 pi/3)*(P(0)/(pi^{3/2}Q(0)))
= (4/(3 pi^{1/2})) P(0)/Q(0).  [CORRECTED: an earlier revision of this file had
(4 sqrt(pi)/3) P(0)/Q(0), i.e. pi^{+1/2} instead of pi^{-1/2}.]
Comparing with pi/sqrt(18) for positive constants P(0),Q(0) reduces, by squaring twice, to
    32 P(0)^2  <  pi^3 Q(0)^2 .   [CORRECTED: was 32 P(0)^2 < pi Q(0)^2.]
"""
import sympy as sp
s, v, lam, x, t = sp.symbols('s v lambda x t', real=True, positive=False)
s_ = sp.Symbol('s'); v_ = sp.Symbol('v')

def fourier_map_matrix(N):
    """Exact matrix of Q[s]->Q[v] (degrees <= N) for f=P(s)e^{-s}, f^=pi^{3/2}Q(v)e^{-v}."""
    rows=[]
    for n in range(N+1):
        # (-d/dlam)^n [ lam^{-3/2} exp(-w/lam) ] at lam=1, with w the variable
        w = sp.Symbol('w')
        A = lam**sp.Rational(-3,2)
        for _ in range(n):
            A = -sp.diff(A, lam) - (w/lam**2)*A
        An = sp.expand(A.subs(lam,1))
        rows.append(sp.expand(An))
    return rows           # Q_n(w) for P(s)=s^n

def apply_map(P, N=None):
    P = sp.expand(P)
    N = N if N is not None else sp.Poly(P, s_).degree()
    rows = fourier_map_matrix(N)
    Ppoly = sp.Poly(P, s_)
    Q = 0
    for n,c in enumerate(Ppoly.all_coeffs()[::-1]):
        if c: Q += c*rows[n]
    return sp.expand(Q.subs(sp.Symbol('w'), v_))

def sign_on_half_line(p, a, want):
    """EXACT decision of sign(p) == want (-1/0/+1) on [a,inf), allowing EVEN-multiplicity zeros.
    Works for a polynomial in any single variable."""
    p = sp.expand(p)
    if p == 0:
        return (want == 0), "zero polynomial"
    fs = p.free_symbols
    S = (list(fs)[0] if len(fs) == 1 else s_)
    P = sp.Poly(p, S); lc = P.LC()
    m_a = 0
    if sp.simplify(p.subs(S, a)) == 0:
        q = P
        while sp.simplify(q.as_expr().subs(S, a)) == 0:
            ok, rem = sp.div(q.as_expr(), (S - a), S)
            if sp.simplify(rem) != 0: break
            q = sp.Poly(ok, S); m_a += 1
            if m_a > 200: break
    odd_roots = []
    for fac, mult in sp.sqf_list(p)[1]:
        if mult % 2 == 1:
            F = sp.Poly(fac, S)
            if F.degree() >= 1:
                for item in F.real_roots(multiple=True):
                    r, m = (item if isinstance(item, tuple) else (item, 1))
                    if sp.simplify(sp.nsimplify(r) - a) > 0:
                        odd_roots.append((sp.nsimplify(r), mult*m))
    if odd_roots:
        return False, "odd-multiplicity root(s) in (%s,inf): %s (sign flips => not %s)" % (a, odd_roots[:3], want)
    sign_open = sp.sign(lc)
    pa = sp.simplify(p.subs(S, a))
    if pa < 0 and want >= 0: return False, "p(a)<0"
    if pa > 0 and want <= 0: return False, "p(a)>0"
    if pa == 0 and want != 0 and sign_open != want:
        return False, "p(a)=0 mult %d, sign just right = %s" % (m_a, sign_open)
    return True, "ok: sign on (a,inf) = %s, multiplicity at a = %d" % (sign_open, m_a)

# ---------------------------------------------------------------------------
# Directed rational enclosure of pi, and the exact Kepler comparison.
# pi = 16*arctan(1/5) - 4*arctan(1/239)  (Machin).  For arctan(1/n) the partial
# sums of the alternating series bracket the limit between consecutive ones, so
# (lo,hi) below are RIGOROUS rational bounds.
# ---------------------------------------------------------------------------
from fractions import Fraction as Fr

def _atan_inv_bounds(n, terms=48):
    S = []
    acc = Fr(0)
    for k in range(terms):
        acc += Fr((-1)**k, (2*k+1)*n**(2*k+1))
        S.append(acc)
    lo, hi = min(S[-1], S[-2]), max(S[-1], S[-2])
    return lo, hi

def pi_bounds(terms=48):
    a_lo, a_hi = _atan_inv_bounds(5, terms)
    b_lo, b_hi = _atan_inv_bounds(239, terms)
    return 16*a_lo - 4*b_hi, 16*a_hi - 4*b_lo

def kepler_ok(P0, Q0):
    """EXACT, directed test of  (4/(3 sqrt pi)) P0/Q0 < pi/sqrt18  for rational P0,Q0>0.

    Equivalent (squaring twice, all quantities positive) to  32 P0^2 < pi^3 Q0^2.
    Returns True / False / None (None = not decided by the enclosure, which the
    caller must treat as a rejection, never as acceptance).
    BUG THIS REPLACES: sp.Integer(P0) truncates a positive rational, so
    (P0,Q0) = (99/100,1) was wrongly accepted.
    """
    P0 = Fr(P0); Q0 = Fr(Q0)
    if P0 <= 0 or Q0 <= 0:
        return False
    R = 32*P0*P0/(Q0*Q0)                 # need R < pi^3
    lo, hi = pi_bounds()
    if R < lo**3:  return True
    if R > hi**3:  return False
    return None

def certify(P, verbose=False):
    P = sp.expand(P)
    Q = apply_map(P)
    reasons = {}
    ok1,r1 = sign_on_half_line(P, 4, -1)
    ok2,r2 = sign_on_half_line(Q, 0, +1)
    P0, Q0 = sp.simplify(P.subs(s_,0)), sp.simplify(Q.subs(v_,0))
    if P0 <= 0 or Q0 <= 0:
        return None, "f(0)=%s, f^(0)~%s : need both positive" % (P0,Q0)
    if not (ok1 and ok2):
        return None, "sign failure: CE1 %s / CE2 %s" % (r1 if not ok1 else 'ok', r2 if not ok2 else 'ok')
    return (sp.nsimplify(P0/Q0), P, Q, reasons), "certified"

if __name__ == "__main__":
    print("="*84); print("1. Verify the exact Fourier map against numerical quadrature (3D radial)"); print("="*84)
    import numpy as np, math
    from scipy.integrate import quad
    for P in [1, 1 - s_/8, 3 - sp.Rational(1,2)*s_ + s_**2/40]:
        Q = apply_map(P)
        f  = sp.lambdify(s_, P, 'numpy'); fh = sp.lambdify(v_, Q, 'numpy')
        for T in (0.0, 0.55, 1.3):
            # (F f)(T) = (2/T) int_0^inf f(r) r sin(2 pi T r) dr  (radial transform in R^3)
            g = lambda r: f(r*r)*math.exp(-r*r)*r*math.sin(2*math.pi*T*r)
            if T == 0:
                g0 = lambda r: f(r*r)*math.exp(-r*r)*r*r
                lhs = 4*math.pi*quad(g0,0,12,limit=400)[0]
            else:
                lhs = (2/T)*quad(g,0,12,limit=400)[0]
            rhs = math.pi**1.5*fh(math.pi**2*T*T)*math.exp(-math.pi**2*T*T)
            print("   P=%-22s T=%.2f  quad=%+.10f  exact=%+.10f  |d|=%.1e"
                  % (str(P)[:22], T, lhs, rhs, abs(lhs-rhs)))

    print("="*84); print("2. Sign test must ACCEPT an even-multiplicity zero at the contact radius"); print("="*84)
    for P, note in [(-(s_-4)**2, "double zero at s=4"), (-(s_-4), "simple zero at s=4"),
                    (-(s_-4)**2*(s_-6), "double at 4, simple at 6"), (-1, "constant -1")]:
        r = sign_on_half_line(sp.expand(P), 4, -1)
        print("   %-28s (%s) -> %s : %s" % (str(sp.factor(sp.expand(P)))[:28], note, r[0], r[1]))
    r = sign_on_half_line(sp.expand((v_-1)**2), 0, +1)
    print("   %-28s (double zero at v=1) -> %s : %s" % ("(v-1)^2", r[0], r[1]))
    r = sign_on_half_line(sp.expand((v_-1)), 0, +1)
    print("   %-28s (simple zero at v=1) -> %s : %s" % ("v-1", r[0], r[1]))

    print("="*84); print("3. Candidate certification (Kepler comparison reduced to rationals + pi)"); print("="*84)
    cands = [-(s_-4)**2,                     # CE1 ok, CE2 fails (not PD) -> must reject
             sp.expand(2 - s_/4),            # CE1 ok at s=4? 2-1=1 >0 -> fails
             sp.expand(-(s_-4)*(1 + s_/10)) ]
    for P in cands:
        (res, msg) = certify(sp.expand(P))
        print("   P = %-24s -> %s" % (str(sp.factor(sp.expand(P)))[:24], msg))
    print()
    print("="*84); print("4. Directed pi enclosure and the exact Kepler test"); print("="*84)
    lo,hi = pi_bounds()
    print("   pi in [%.20f, %.20f]  (width %.2e)" % (float(lo), float(hi), float(hi-lo)))
    print("   acceptance threshold: bound < pi/sqrt18  <=>  P0/Q0 < sqrt(pi^3/32) = %.8f"
          % (float(hi)**1.5/32**0.5))
    for (P0,Q0) in [(99,100),(1,1),(2,3),(98,100),(9843,10000),(9844,10000)]:
        r=Fr(P0,Q0)
        print("      P0/Q0 = %-9s  32 P0^2 = %-12s vs pi^3 Q0^2 = %-12.6f => kepler_ok = %s"
              % (str(r), str(32*Fr(P0)**2), float(Fr(Q0)**2*hi**3), kepler_ok(Fr(P0),Fr(Q0))))
    print("   A successful certificate reports P(0)/Q(0) rational and the test")
    print("        32 P(0)^2 < pi^3 Q(0)^2  (<=> bound (4/(3 sqrt pi))P0/Q0 < pi/sqrt18),")
    print("   decided with rational enclosures of pi; the SEARCH over P is a separate LP.")
    print("   No float residual is used as an identity: the map is applied by exact")
    print("   differentiation, and only the quadrature cross-check above is floating point.")
