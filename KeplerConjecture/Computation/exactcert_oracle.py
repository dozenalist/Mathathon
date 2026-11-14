#!/usr/bin/env python3
"""Independent EXACT oracle for exactcert.py, plus positive valid examples.

WHY.  The oracle in exactcert_tests.py T6 samples a dense grid.  Sampling is not a proof
and cannot certify a sign: it can miss a narrow excursion.  This module provides an
independent *exact* decision procedure built on different machinery (SymPy's polynomial
algebra: sqf_list for squarefree decomposition and count_roots for exact real-root
counting over a rational interval), so agreement between it and exactcert.py is evidence
about the implementation rather than about a grid.

The two implementations share NO code: exactcert.py uses hand-rolled Fraction polynomial
arithmetic with its own Sturm chain and Yun decomposition; this file uses SymPy's.
They are compared on root counts and on the accept/reject verdict.

WHAT IS DECIDED.  Same predicate as exactcert.certify with allow_touching=True:
  (A1)  p < 0 on [8*PI_LO, inf)     (PI_LO < pi, so this is the safe direction)
  (A2)  q > 0 on [0, inf)
with even-multiplicity zeros permitted and odd-multiplicity crossings rejected.
"""
import sys
from fractions import Fraction as F
import exactcert as EC

try:
    import sympy as sp
except ImportError:                       # pragma: no cover
    sp = None

PI_LO = EC.PI_LO

def _cauchy_bound_sym(coeffs):
    """1 + max|a_i/a_n| as an exact Fraction; all real roots lie strictly inside."""
    c = [F(str(x)) for x in coeffs]
    lead = abs(c[-1])
    return 1 + max(abs(x) / lead for x in c[:-1]) if len(c) > 1 else F(1)

def p_q_sympy(c, t=None):
    """(p, q) as SymPy expressions, built from SymPy's assoc_laguerre."""
    t = t or sp.symbols("t")
    K = len(c) - 1
    p = sp.Integer(0); q = sp.Integer(0)
    for k, ck in enumerate(c):
        L = sp.assoc_laguerre(k, sp.Rational(1, 2), t)
        p += sp.Rational(ck.numerator, ck.denominator) * L
        q += sp.Rational(ck.numerator, ck.denominator) * sp.Integer((-1) ** k) * L
    return sp.expand(p), sp.expand(q)

def _odd_part_sym(expr, t):
    """Squarefree odd-multiplicity part with its leading sign, via SymPy sqf_list."""
    P = sp.Poly(expr, t)
    if P.is_zero:
        return None
    coeff, factors = P.sqf_list()
    u = sp.Integer(1)
    for f, e in factors:
        if e % 2 == 1:
            u *= f.as_expr()
    return sp.expand(coeff * u)

def _half_line_sign_sym(expr, A, t):
    """Exact sign of expr on [A, inf) using SymPy count_roots.  Returns 'pos','neg','fail'."""
    if expr == 0:
        return "fail"
    u = _odd_part_sym(expr, t)
    if u is None or u == 0:
        return "fail"
    U = sp.Poly(u, t)
    A = sp.Rational(F(A).numerator, F(A).denominator)
    if U.eval(A) == 0:
        return "fail"                     # endpoint root: fail closed
    M = sp.Rational(_cauchy_bound_sym(list(U.all_coeffs())[::-1]).numerator,
                    _cauchy_bound_sym(list(U.all_coeffs())[::-1]).denominator)
    n = U.count_roots(A, M)               # exact, distinct real roots in [A, M]
    if n != 0:
        return "fail"
    return "pos" if U.eval(A) > 0 else "neg"

def oracle(c):
    """Independent exact verdict.  Returns dict(ok, reason, p0, q0)."""
    if sp is None:
        raise RuntimeError("sympy required for the exact oracle")
    t = sp.symbols("t")
    c = [F(x) for x in c]
    p, q = p_q_sympy(c, t)
    if p == 0 or q == 0:
        return dict(ok=False, reason="p or q identically zero")
    v1 = _half_line_sign_sym(p, PI_LO * 8, t)
    if v1 != "neg":
        return dict(ok=False, reason="A1: got %s" % v1)
    v2 = _half_line_sign_sym(q, F(0), t)
    if v2 != "pos":
        return dict(ok=False, reason="A2: got %s" % v2)
    p0 = sp.Rational(F(sp.Poly(p, t).eval(0)).numerator, F(sp.Poly(p, t).eval(0)).denominator)
    q0 = sp.Rational(F(sp.Poly(q, t).eval(0)).numerator, F(sp.Poly(q, t).eval(0)).denominator)
    if q0 <= 0 or p0 <= 0:      # f(0) = p(0) must be POSITIVE for a CE certificate
        return dict(ok=False, reason="p0/q0 not a positive ratio")
    return dict(ok=True, reason=None, p0=p0, q0=q0)

if __name__ == "__main__":
    if sp is None:
        sys.exit("sympy not available")
    import random
    print("E1 POSITIVE valid example, degree 1:  c = (4, 1)")
    print("   p = 11/2 - t  < 0 for t > 11/2, so certainly on [8pi, inf)")
    print("   q =  5/2 + t  > 0 on [0, inf)")
    mine = EC.certify([4, 1], verbose=False)
    theirs = oracle([4, 1])
    print("   exactcert ok=%s  oracle ok=%s" % (mine["ok"], theirs["ok"]))
    if mine["ok"]:
        print("   exact p0/q0 = %s ; Delta upper (rounded up) = %s"
              % (mine["ratio_f0_fhat0"], EC.delta_upper_decimal(mine, 6)))
    assert mine["ok"] and theirs["ok"], "the degree-1 certificate must be accepted"

    print("\nE2 even multiplicity inside the half-line is ALLOWED")
    t = sp.symbols("t")
    A = 8 * PI_LO
    # NOTE: 8*pi ~ 25.13, so a root at t = 10 is OUTSIDE [8pi, inf) and must be
    # ignored; roots at t = 30 are inside.  An earlier version of this test used
    # t = 10 for the in-line cases and was itself wrong -- the code was right.
    for label, expr, want in (
        ("-(t-30)^2  double root at 30 (in-line)", -(t - 30) ** 2, "neg"),
        ("-(t-30)^3  triple root at 30 (in-line)", -(t - 30) ** 3, "fail"),
        (" (t-30)^2  double, positive",            (t - 30) ** 2, "pos"),
        ("-(t-10)^3  triple root at 10 (OUTSIDE)", -(t - 10) ** 3, "neg"),
    ):
        got = _half_line_sign_sym(sp.expand(expr), A, t)
        cf, uf = EC.yun_odd_part([F(q) for q in sp.Poly(sp.expand(expr), t).all_coeffs()[::-1]])
        mine_sgn, mine_reason = EC._half_line_sign(cf, uf, A)
        print("   %-32s sympy=%-4s exactcert=%-4s  %s"
              % (label, got, mine_sgn, "AGREE" if got == mine_sgn else "DISAGREE"))
        assert got == want and mine_sgn == want, (label, got, mine_sgn)

    print("\nE3 endpoint root fails closed in both implementations")
    expr = sp.expand(t - sp.Rational(F(A).numerator, F(A).denominator))
    got = _half_line_sign_sym(expr, A, t)
    cf, uf = EC.yun_odd_part([F(q) for q in sp.Poly(expr, t).all_coeffs()[::-1]])
    mine_sgn, _ = EC._half_line_sign(cf, uf, A)
    print("   sympy=%s  exactcert=%s" % (got, mine_sgn))
    assert got == "fail" and mine_sgn == "fail"

    print("\nE4 exact agreement on random candidates (no sampling)")
    random.seed(11)
    n = agree = 0; dis = []
    for _ in range(20):
        K = random.choice([1, 3, 5])
        c = [F(random.randint(-5, 5), random.randint(1, 4)) for _ in range(K + 1)]
        if all(x == 0 for x in c):
            continue
        a = EC.certify(c, verbose=False)["ok"]
        b = oracle(c)["ok"]
        n += 1
        if a == b: agree += 1
        else: dis.append((c, a, b))
    print("   %d candidates, %d agree, %d disagree" % (n, agree, len(dis)))
    if dis: print("   disagreements:", dis[:3])
    assert not dis, "exact oracle disagrees with exactcert"
    print("\nALL ORACLE CHECKS PASS (exact, not sampled)")
