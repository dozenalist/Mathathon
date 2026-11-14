#!/usr/bin/env python3
"""Exact checker for the shell-allowance benchmark (K15-C018 / K15-C019).

What this is
------------
A *checker*, not an optimiser.  Given a rational profile, it decides exactly
whether the profile is admissible for the shell allowance and prints the
resulting density bound as an exact rational times pi.

EXPLORATORY ONLY as a source of numbers: nothing here produces a bound unless a
rational profile is supplied and every sign verdict below is PASS.

Basis and the rationality trick
-------------------------------
Write  u = pi*|x|^2  and  f(x) = exp(-pi|x|^2) * sum_k a_k u^k  with a_k in Q.
Then fhat(x) = exp(-pi|x|^2) * sum_k b_k u^k with b = M a, where M is a RATIONAL
matrix: because u = t/2 with t = 2 pi |x|^2, the monomial u^k expands in the
radial Hermite-Laguerre basis L_j^{1/2}(t) (which has rational coefficients and
is monic), and phi_j = exp(-pi r^2) L_j^{1/2}(2 pi r^2) satisfies
phi_hat_j = (-1)^j phi_j in R^3.  So M = (Laguerre expansion of u^k), sign-flipped,
re-expanded.  Hence p(u), q(u) in Q[u].

Sign conditions, made rational
------------------------------
The mathematically wanted regions are s = |x|^2 >= 4, i.e. u >= 4*pi = 12.566...,
and the shell 4 <= s <= rho^2, i.e. 4*pi <= u <= pi*rho^2.
* f <= eta on [2, rho]        is implied by  p(u) <= eta  on [T_LO, T_HI]
* f <= 0   for |x| > rho       is implied by  p(u) <= 0    on [T_HI, inf)
provided T_LO <= 4*pi and T_HI <= pi*rho^2, both checked below with directed
rational bounds for pi.  This is the conservative rational threshold of
Main/LOCAL_COMPUTE_REQUESTS.md (M-NUM-002 option 1).
* fhat >= 0 everywhere        <=>  q(u) >= 0 for u >= 0.

Bound
-----
If all verdicts pass, every packing satisfies
    delta <= (4 pi/3) * (p(0) + 12*eta) / q(0),
by K15-C003 (Theorem B) with n = 12 and K15-C002b's bridge, PROVIDED the count
12 is established for rho (K15-C019: it reduces to a Tammes-13 statement; the
value rho = 209/100 is provisional until that is certified).  The count is a
hypothesis here, never a conclusion.

The count `n` is a parameter: `n = 12` is conditional on a Tammes-13 enclosure
(K15-C019); `n = 27` is unconditional at rho = 2.05 by the volume bound
K15-C013(a), `n <= floor((rho+1)^3) - 1`.

Exit status: 0 iff every check passes.  Failures are reported unconditionally
(D13: no failure path may sit behind a verbosity flag).
"""
import sys
from fractions import Fraction as F
import sympy as sp

PI_LO = F(314159265358979323846264338327, 10 ** 29)   # < pi (matches Computation's)
PI_HI = F(314159265358979323846264338329, 10 ** 29)   # > pi
T_LO = F(4) * PI_LO                 # = 4*PI_LO <= 4*pi, rational, no rounding
T_HI_DEFAULT = F(27, 2)             # <= pi*rho^2 only for rho >= 2.0906


def t_hi_for(rho):
    """A rational threshold <= pi*rho^2.

    Using the directed lower bound PI_LO < pi gives T_HI = PI_LO*rho^2 exactly,
    which is rational and loses NOTHING: no integer rounding is needed, so the
    "conservative threshold" loss of the earlier revision is gone.
    """
    return PI_LO * rho * rho

t = sp.Symbol('t')


def lag_poly(j):
    """L_j^{1/2}(t) as a sympy polynomial in t."""
    return sp.expand(sp.assoc_laguerre(j, sp.Rational(1, 2), t))


def mono_to_lag(k):
    """Coefficients a_j with (t/2)^k = sum_j a_j L_j^{1/2}(t)."""
    poly = sp.expand((t / 2) ** k)
    a = [sp.Rational(0)] * (k + 1)
    for j in range(k, -1, -1):
        Lj = lag_poly(j)
        cj = sp.Poly(Lj, t).coeff_monomial(t ** j)
        c = sp.Poly(poly, t).coeff_monomial(t ** j) / cj
        a[j] = sp.Rational(c)
        poly = sp.expand(poly - c * Lj)
    assert sp.expand(poly) == 0, "Laguerre expansion failed"
    return a


def fourier_map(K):
    """Rational matrix M with b = M a for f = e^{-pi r^2} sum a_k u^k."""
    M = [[sp.Rational(0)] * (K + 1) for _ in range(K + 1)]
    for k in range(K + 1):
        a = mono_to_lag(k)                      # in the t variable
        # fhat_k = e^{-pi r^2} sum_j (-1)^j a_j L_j(t), then t = 2u
        expr = sum(((-1) ** j) * a[j] * lag_poly(j) for j in range(k + 1))
        expr = sp.expand(expr.subs(t, 2 * sp.Symbol('u')))
        P = sp.Poly(expr, sp.Symbol('u'))
        for i in range(K + 1):
            M[i][k] = sp.Rational(P.coeff_monomial(sp.Symbol('u') ** i))
    return sp.Matrix(M)


def poly_from(coeffs, var):
    return sum(sp.Rational(c) * var ** i for i, c in enumerate(coeffs))


def _isolating(expr, lo, hi, eps_den=10 ** 8):
    """Isolating rational intervals for the real roots of `expr` meeting [lo,hi].

    Returns (intervals, strict) where `intervals` is a sorted list of (a, b) and
    `strict` says whether consecutive intervals are separated by a non-empty
    rational gap (b_i < a_{i+1}).  `strict = False` means the gap argument below
    is NOT conclusive.
    """
    uu = sp.Symbol('u')
    P = sp.Poly(expr, uu)
    lo = sp.Rational(lo)
    if P.degree() < 1:
        return [], True
    out = []
    for (ivl, m) in P.intervals(eps=sp.Rational(1, eps_den)):
        a, b = (ivl, ivl) if not isinstance(ivl, tuple) else ivl
        if b < lo:
            continue
        if hi is not sp.oo and a > sp.Rational(hi):
            continue
        out.append((a, b))
    out.sort(key=lambda t: t[0])
    strict = True
    for (a1, b1), (a2, b2) in zip(out, out[1:]):
        if not (b1 < a2):
            strict = False
    return out, strict


def _gap_verdict(expr, lo, hi, want_nonneg):
    """Decide by testing one point per component of the region minus its roots.

    CORRECTNESS.  A polynomial has constant sign on every component of
    `[lo,hi] \\ {roots}`, and equals 0 at the roots, so testing one point per
    component decides the sign everywhere.  The components are separated by the
    roots; with isolating intervals `[a_i, b_i]` (r_i in the interior, or the
    interval degenerate at a rational root) the components are met by:
      * `lo` and `hi`,
      * the midpoint of every gap `(b_i, a_{i+1})` when the gap is non-empty,
      * the shared endpoint when `b_i = a_{i+1}` (that point is strictly between
        the two roots unless it IS one of them).
    This routine returns True/False only when it is conclusive, and None
    otherwise.  In particular it returns None as soon as two isolating intervals
    touch or overlap, which is the case that produced the false accept of
    `(u-7/5)^2 - 2/10^40` (two intervals sharing the endpoint 7/5, so no gap
    midpoint existed and the negative dip was never sampled).
    """
    uu = sp.Symbol('u')
    P = sp.Poly(expr, uu)
    lo = sp.Rational(lo)
    # Refine the isolation once before giving up: a finer eps separates intervals
    # that merely touched.  COST NOTE: refinement and `function_range` are both
    # expensive at high degree with clustered roots (a degree-35 polynomial with a
    # pair 1e-10 apart takes minutes), so the ladder stops at eps = 1e-14.  No
    # certificate in this project reaches this branch: on the sign regions the
    # polynomials have no real root and the first pass is already strict.
    intervals, strict = None, False
    for den in (10 ** 8, 10 ** 14):
        intervals, strict = _isolating(P.as_expr(), lo, hi, den)
        if strict:
            break
    if not strict:
        return None
    pts = [lo] + ([sp.Rational(hi)] if hi is not sp.oo else [])
    prev = lo
    for (a, b) in intervals:
        if a > prev:
            pts.append((prev + a) / 2)
        prev = max(prev, b)
    if hi is sp.oo:
        pts.append(prev + 1)
    elif sp.Rational(hi) > prev:
        pts.append((prev + sp.Rational(hi)) / 2)
    vals = [P.eval(x) for x in pts]
    if want_nonneg:
        return all(v >= 0 for v in vals)
    return all(v <= 0 for v in vals)


def _decide(expr, lo, hi, want_nonneg) -> bool:
    """Complete decision: p >= 0 (or p <= 0) on [lo,hi], hi possibly oo.

    ORDER OF BUSINESS.
      1. The gap argument of `_gap_verdict`, when conclusive.  This is the path
         taken by every certificate in this project: on the sign regions the
         polynomials have no real root, the isolating list is empty, and the
         verdict rests on probes at rational points only.
      2. Otherwise `function_range`, which computes the exact range of a
         polynomial on an interval (its extrema are attained at the endpoints or
         at critical points).  It is the complete rule; it is slower and is NOT
         used on the certificate path, so the certificate checks do not depend on
         it.
    Nothing here samples a grid: both branches are exact.
    """
    v = _gap_verdict(expr, lo, hi, want_nonneg)
    if v is not None:
        return v
    from sympy.calculus.util import function_range
    uu = sp.Symbol('u')
    iv = sp.Interval(sp.Rational(lo), sp.oo if hi is sp.oo else sp.Rational(hi))
    rng = function_range(sp.expand(expr), uu, iv)
    if want_nonneg:
        return bool(rng.inf >= 0)
    return bool(rng.sup <= 0)


def le_on_interval(coeffs, eta, lo, hi) -> bool:
    """p(u) <= eta for all u in the closed interval [lo, hi]."""
    u_ = sp.Symbol('u')
    r = sp.expand(poly_from(coeffs, u_) - sp.Rational(eta))
    return _decide(r, lo, hi, want_nonneg=False)


def nonneg_on_half_line(coeffs) -> bool:
    """q(u) >= 0 for all u >= 0."""
    u_ = sp.Symbol('u')
    q = sp.expand(poly_from(coeffs, u_))
    if sp.Poly(q, u_).degree() < 0:
        return True
    return _decide(q, 0, sp.oo, want_nonneg=True)


def _ray(coeffs, hi) -> bool:
    """p(u) <= 0 for all u >= hi."""
    u_ = sp.Symbol('u')
    p_ = sp.expand(poly_from(coeffs, u_))
    if sp.Poly(p_, u_).degree() < 0:
        return True
    return _decide(p_, hi, sp.oo, want_nonneg=False)


def _sign_at(poly_expr, x):
    """Sign of a polynomial at x in [-inf, +inf]; at infinity use the leading coeff."""
    P = sp.Poly(poly_expr, sp.Symbol('u'))
    if x is sp.oo or x == sp.oo:
        lc = P.LC()
        return 0 if lc == 0 else (1 if lc > 0 else -1)
    v = P.eval(x)
    return 0 if v == 0 else (1 if v > 0 else -1)


def check(a, rho=F(209, 100), eta=F(0), K=None, count=12, verbose=True):
    """Full verdict for a rational coefficient list a (monomial, u = pi s)."""
    K = K if K is not None else len(a) - 1
    a = [F(x) for x in a] + [F(0)] * (K + 1 - len(a))
    M = fourier_map(K)
    b = [sum(M[i, k] * sp.Rational(a[k].numerator, a[k].denominator)
             for k in range(K + 1)) for i in range(K + 1)]
    b = [F(int(x.p), int(x.q)) for x in b]

    ok = True
    def rep(name, cond, detail=""):
        nonlocal ok
        print(("PASS  " if cond else "FAIL  ") + name + (("   [" + detail + "]") if detail else ""))
        ok = ok and bool(cond)

    rep("containment T_LO = %s <= 4*pi" % T_LO, T_LO <= 4 * PI_LO, "4pi in (%s, %s)" % (4 * PI_LO, 4 * PI_HI))
    T_HI = t_hi_for(rho)
    rep("containment T_HI = %s <= pi*rho^2" % T_HI,
        T_HI <= PI_LO * rho * rho, "pi*rho^2 > %s" % (PI_LO * rho * rho))
    if rho > 2:
        rep("window non-degenerate (T_LO < T_HI)", T_LO < T_HI,
            "else the allowance is empty and this is ordinary CE")
    rep("fhat >= 0 for u >= 0 (q >= 0)", nonneg_on_half_line(b))
    if rho > 2:
        rep("f <= eta on the shell (p <= eta on [T_LO, T_HI])",
            le_on_interval(a, eta, T_LO, T_HI))
    rep("f <= 0 beyond rho (p <= 0 on [T_HI, inf))", _ray(a, T_HI))
    p0, q0 = F(a[0]), F(b[0])
    rep("fhat(0) > 0", q0 > 0, "q(0) = %s" % q0)
    if not ok:
        return None
    val = (p0 + count * eta) / q0
    lo = 4 * PI_LO / 3 * val
    hi = 4 * PI_HI / 3 * val
    print("  p(0) = %s, q(0) = %s, eta = %s" % (p0, q0, eta))
    print("  R = (p(0)+%d eta)/q(0) = %s = %.12f" % (count, val, float(val)))
    print("  delta <= (4pi/3) R in (%.12f, %.12f)   [rational pi enclosure]" % (float(lo), float(hi)))
    return (lo, hi)


def self_test():
    print("== S1: the Fourier map reproduces the Laguerre eigen-relation ==")
    M = fourier_map(4)
    for k in range(3):
        col = [M[i, k] for i in range(5)]
        # u^k = (t/2)^k expands in L_j; the transform flips (-1)^j
        print("   M[:,%d] = %s" % (k, [str(x) for x in col]))
    ok = True
    # phi_k = e^{-pi r^2} L_k(2 pi r^2) is an eigenfunction: check on k<=2 by
    # expanding L_k(2u) in monomials and applying M, expecting (-1)^k identity.
    u = sp.Symbol('u')
    for k in range(3):
        Lk = sp.expand(lag_poly(k).subs(t, 2 * u))
        coeffs = [sp.Rational(sp.Poly(Lk, u).coeff_monomial(u ** i)) for i in range(k + 1)]
        coeffs += [sp.Rational(0)] * (5 - len(coeffs))
        b = M * sp.Matrix([sp.Rational(c) for c in coeffs])
        expect = [((-1) ** k) * c for c in coeffs]
        same = all(sp.simplify(b[i] - expect[i]) == 0 for i in range(5))
        print("   %s  phi_%d maps to (-1)^%d phi_%d" % ("PASS" if same else "FAIL", k, k, k))
        ok = ok and same

    print("== S2: a deliberately bad profile must be REJECTED ==")
    # q(u) = (u-1)(u-10): negative on (1,10), so q >= 0 fails; must be caught.
    bad = check([F(1), F(-11), F(1)], rho=F(209, 100), eta=F(0))
    ok = ok and (bad is None)
    print("== S3: an obviously good sign pair must be ACCEPTED by the sign tests ==")
    # p(u) = 2 - 2u/9 vanishes for u >= 9 (so f <= 0 for u >= T_HI), q(u) = 1 + 2u/3 > 0.
    # It is not a Fourier pair; this tests only the sign machinery, via the
    # internal helpers, not the benchmark (which requires b = M a).
    uu = sp.Symbol('u')
    p_ok = _ray([F(2), F(-2, 9)], T_HI_DEFAULT) and le_on_interval([F(2), F(-2, 9)], F(0), T_LO, T_HI_DEFAULT)
    q_ok = nonneg_on_half_line([F(1), F(2, 3)])
    print("   %s  p = 2 - 2u/9 satisfies both p-conditions" % ("PASS" if p_ok else "FAIL"))
    print("   %s  q = 1 + 2u/3 is nonnegative" % ("PASS" if q_ok else "FAIL"))
    ok = ok and p_ok and q_ok
    print("== S4: even-multiplicity zeros must be ACCEPTED (tight certificates) ==")
    cases = [("p = (u-5)^2 <= 0 on [0,10] must FAIL", le_on_interval([25, -10, 1], 0, 0, 10), False),
             ("p = -(u-5)^2 <= 0 on [0,10] must PASS", le_on_interval([-25, 10, -1], 0, 0, 10), True),
             ("q = u^2 >= 0 on [0,inf) must PASS", nonneg_on_half_line([0, 0, 1]), True),
             ("q = u-1 >= 0 on [0,inf) must FAIL", nonneg_on_half_line([-1, 1]), False)]
    for name, got, want in cases:
        good = (got == want)
        print("   %s  %s" % ("PASS" if good else "FAIL", name))
        ok = ok and good

    print("\nSELF-TEST:", "ALL PASS" if ok else "FAILURES")
    return ok


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(0 if self_test() else 1)
    print(__doc__)
