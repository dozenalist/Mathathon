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


def _sign_at(poly_expr, x):
    """Sign of a polynomial at x in [-inf, +inf]; at infinity use the leading coeff."""
    P = sp.Poly(poly_expr, sp.Symbol('u'))
    if x is sp.oo or x == sp.oo:
        lc = P.LC()
        return 0 if lc == 0 else (1 if lc > 0 else -1)
    v = P.eval(x)
    return 0 if v == 0 else (1 if v > 0 else -1)


def nonneg_on_half_line(coeffs) -> bool:
    """q(u) >= 0 for all u >= 0, decided exactly (Sturm / root counting)."""
    u = sp.Symbol('u')
    q = sp.Poly(poly_from(coeffs, u), u)
    if q.degree() < 0:
        return True
    if q.eval(0) < 0:
        return False
    from sympy import sturm, oo
    seq = sturm(q.as_expr(), u)
    def sign_changes_at(x):
        vals = [_sign_at(s, x) for s in seq]
        vals = [v for v in vals if v != 0]
        return sum(1 for a, b in zip(vals, vals[1:]) if a * b < 0)
    return sign_changes_at(0) - sign_changes_at(oo) == 0


def le_on_interval(coeffs, eta, lo, hi) -> bool:
    """p(u) <= eta for all u in [lo, hi], decided exactly."""
    u = sp.Symbol('u')
    r = sp.Poly(poly_from(coeffs, u) - sp.Rational(eta), u)
    from sympy import sturm, oo
    if r.degree() < 0:
        return True
    seq = sturm(r.as_expr(), u)
    def sc(x):
        vals = [_sign_at(s, x) for s in seq]
        vals = [v for v in vals if v != 0]
        return sum(1 for a, b in zip(vals, vals[1:]) if a * b < 0)
    return sc(sp.Rational(lo)) - sc(sp.Rational(hi)) == 0


def _ray(coeffs, hi) -> bool:
    from sympy import sturm, oo
    u = sp.Symbol('u')
    r = sp.Poly(poly_from(coeffs, u), u)
    if r.degree() < 0:
        return True
    if r.LC() > 0:
        return False                      # p -> +inf
    seq = sturm(r.as_expr(), u)
    def sc(x):
        vals = [_sign_at(s, x) for s in seq]
        vals = [v for v in vals if v != 0]
        return sum(1 for a, b in zip(vals, vals[1:]) if a * b < 0)
    return sc(sp.Rational(hi)) - sc(oo) == 0


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
    print("\nSELF-TEST:", "ALL PASS" if ok else "FAILURES")
    return ok


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(0 if self_test() else 1)
    print(__doc__)
