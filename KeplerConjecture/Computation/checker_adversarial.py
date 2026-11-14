#!/usr/bin/env python3
"""Adversarial regression suite for exact sign checkers (K15-C030).

Each case is designed so that a *wrong* checker gives the wrong answer. They are
stated independently of any implementation, so the same list can be run against
Main's shell_check and Computation's exactcert; agreement on all of them is the
evidence required by G8 ("the two checkers are genuinely independent but correct").

Vocabulary: a sign checker answers "is q >= 0 on [0, inf)?" and "is p <= 0 on
[A, inf) / on [lo, hi]?"  Correct answers are decided by sign *changes*, i.e. by
roots of odd multiplicity; roots of even multiplicity must be accepted.

Run:  python3 checker_adversarial.py         (exit 0 iff all expectations hold)
"""
import sys
from fractions import Fraction as F
import sympy as sp

sys.path.insert(0, str(__file__).rsplit('/', 1)[0])
from shell_check import (nonneg_on_half_line, le_on_interval, _ray,
                         PI_LO, t_hi_for)

u = sp.Symbol('u')


def coeffs(expr):
    P = sp.Poly(sp.expand(expr), u)
    return [F(int(P.coeff_monomial(u ** i).p), int(P.coeff_monomial(u ** i).q))
            for i in range(P.degree() + 1)]


def cases():
    T = t_hi_for(F(209, 100))
    TL = 4 * PI_LO
    out = []
    # --- nonnegativity on [0, inf)
    out.append(("q=(u-5)^2 : touching zero, must PASS", nonneg_on_half_line(coeffs((u - 5) ** 2)), True))
    out.append(("q=-(u-5)^2 : negative, must FAIL", nonneg_on_half_line(coeffs(-(u - 5) ** 2)), False))
    out.append(("q=(u-5)^3 : sign change, must FAIL", nonneg_on_half_line(coeffs((u - 5) ** 3)), False))
    out.append(("q=(u-1)^2(u-2)^2 : two touching zeros, must PASS", nonneg_on_half_line(coeffs((u - 1) ** 2 * (u - 2) ** 2)), True))
    out.append(("q=(u-1)^2(u-2) : one sign change, must FAIL", nonneg_on_half_line(coeffs((u - 1) ** 2 * (u - 2))), False))
    out.append(("q=u^2 : double root at the endpoint 0, must PASS", nonneg_on_half_line(coeffs(u ** 2)), True))
    out.append(("q=prod_{k=1..10}(u-k) : ten simple positive roots, must FAIL",
                nonneg_on_half_line(coeffs(sp.prod(u - k for k in range(1, 11)))), False))
    # --- p <= 0 on [T, inf)
    out.append(("p=-(u-T)^2 : touching at T, must PASS", _ray(coeffs(-(u - sp.Rational(T.numerator, T.denominator)) ** 2), T), True))
    out.append(("p=(u-T) : crosses at T, must FAIL", _ray(coeffs(u - sp.Rational(T.numerator, T.denominator)), T), False))
    out.append(("p=-(u-T) : negative beyond T, must PASS", _ray(coeffs(sp.Rational(T.numerator, T.denominator) - u), T), True))
    # --- p <= eta on the compact shell window [TL, T]
    out.append(("p=-(u-13)^2 <= 0 on the window, must PASS", le_on_interval(coeffs(-(u - 13) ** 2), 0, TL, T), True))
    out.append(("p=(u-13)^2 <= 0 on the window, must FAIL", le_on_interval(coeffs((u - 13) ** 2), 0, TL, T), False))
    out.append(("p=-1 <= 0 on the window, must PASS", le_on_interval(coeffs(-sp.Integer(1)), 0, TL, T), True))
    # --- review 0138 evidence: positivity BETWEEN two endpoint roots.
    # These were falsely accepted by the pre-0138 predicates, which tested the
    # endpoints only when the odd part had no root strictly inside.
    out.append(("u(1-u) <= 0 on [0,1] : +1/4 inside, must FAIL",
                le_on_interval([0, 1, -1], 0, 0, 1), False))
    out.append(("u(u-1) >= 0 on [0,inf) : -1/4 inside, must FAIL",
                nonneg_on_half_line([0, -1, 1]), False))
    out.append(("u(1-u) <= 0 on [0,inf) : +1/4 inside, must FAIL",
                _ray([0, 1, -1], 0), False))
    out.append(("-(u-1/2)^2 <= 0 on [0,1] : touching only, must PASS",
                le_on_interval(coeffs(-(u - sp.Rational(1, 2)) ** 2), 0, 0, 1), True))
    out.append(("(u-1/2)^2 >= 0 on [0,inf) : touching only, must PASS",
                nonneg_on_half_line(coeffs((u - sp.Rational(1, 2)) ** 2)), True))
    out.append(("u(u-1) <= 0 on [0,1] : NEGATIVE between two endpoint roots, must PASS",
                le_on_interval([0, -1, 1], 0, 0, 1), True))
    # --- review 0138, SECOND round: perfect squares defeat any odd-part argument
    # (all roots have even multiplicity, so the odd part is constant).  The test
    # points must come from the polynomial's own roots, never from its odd part.
    sq1 = (u * (u - sp.Rational(1, 2)) * (u - 1)) ** 2
    out.append(("([u(u-1/2)(u-1)]^2 <= 0 on [0,1] : +9/4096 at 1/4, must FAIL",
                le_on_interval(coeffs(sq1), 0, 0, 1), False))
    sq2 = -(u * (u - 1) * (u - sp.Rational(1, 2)) * (u - 2)) ** 2
    out.append(("(-[u(u-1)(u-1/2)(u-2)]^2 >= 0 : -441/65536 at 1/4, must FAIL",
                nonneg_on_half_line(coeffs(sq2)), False))
    sq3 = (u * (u - 1) * (u - 2)) ** 2
    out.append(("([u(u-1)(u-2)]^2 <= 0 from 0 : +9/64 at 1/2, must FAIL",
                _ray(coeffs(sq3), 0), False))
    out.append(("([u(u-1/2)(u-1)]^2 <= 0 on [2,3] : positive there, must FAIL",
                le_on_interval(coeffs(sq1), 0, 2, 3), False))
    out.append(("(-[u(u-1)(u-2)]^2 <= 0 on [0,3] : square with a sign, must PASS",
                le_on_interval(coeffs(-sq3), 0, 0, 3), True))
    # --- review 0223: a NEARLY double root.  The two isolating intervals of
    # (u-7/5)^2 - eps share the rational endpoint 7/5, so any "test the gaps
    # between intervals" scheme sees no gap and misses the negative dip between
    # the two roots.  Four witnesses, plus the sign-flipped controls.
    eps = sp.Rational(2, 10 ** 40)
    near_neg = (u - sp.Rational(7, 5)) ** 2 - eps
    near_pos = (u - sp.Rational(7, 5)) ** 2 + eps
    out.append(("(u-7/5)^2 - 2e-40 >= 0 : negative dip of size 2e-40, must FAIL",
                nonneg_on_half_line(coeffs(near_neg)), False))
    out.append(("-(u-7/5)^2 + 2e-40 <= 0 from 0 : must FAIL",
                _ray(coeffs(-near_neg), 0), False))
    out.append(("-(u-7/5)^2 + 2e-40 <= 0 on [0,3] : must FAIL",
                le_on_interval(coeffs(-near_neg), 0, 0, 3), False))
    out.append(("(u-7/5)^2 + 2e-40 >= 0 : strictly positive, must PASS",
                nonneg_on_half_line(coeffs(near_pos)), True))
    near_end = (u - sp.Rational(1, 5)) ** 2 - eps
    out.append(("(u-1/5)^2 - 2e-40 >= 0 on [0,1] : dip inside, must FAIL",
                le_on_interval(coeffs(-near_end), 0, 0, 1), False))
    # --- review 0223, second batch: domain boundaries, multiplicities, clusters.
    out.append(("roots exactly at both endpoints, negative between, must PASS",
                le_on_interval(coeffs((u - 1) * (u - 3)), 0, 1, 3), True))
    out.append(("root exactly at the domain start, must PASS",
                le_on_interval(coeffs(u * (u - 2)), 0, 0, 2), True))
    out.append(("triple root (u-2)^3 >= 0 on [0,inf) : sign change, must FAIL",
                nonneg_on_half_line(coeffs((u - 2) ** 3)), False))
    out.append(("(u-2)^4 >= 0 : even multiplicity everywhere, must PASS",
                nonneg_on_half_line(coeffs((u - 2) ** 4)), True))
    out.append(("(u-2)^4 <= 0 on [0,3] : positive away from 2, must FAIL",
                le_on_interval(coeffs((u - 2) ** 4), 0, 0, 3), False))
    cluster = (u - 1) ** 2 * (u - 1 - sp.Rational(1, 10 ** 15)) ** 2 - sp.Rational(1, 10 ** 30)
    out.append(("clustered roots with a 1e-30 dip, must FAIL",
                nonneg_on_half_line(coeffs(cluster)), False))
    return out


def main():
    ok = True
    print("adversarial sign-checker suite (T = pi_lo*rho^2 = %s)" % t_hi_for(F(209, 100)))
    for name, got, want in cases():
        good = (got == want)
        ok = ok and good
        print(("PASS  " if good else "FAIL  ") + name + ("" if good else "   (got %s)" % got))
    # --- review 0353: PRECONDITIONS of check() (K15-C098).  A negative shell
    # allowance is not a sign-predicate question; check() must refuse it, because the
    # count-price bound is licensed only for eta >= 0 and the eta < 0 statement is the
    # plain two-point bound.  Passing eta < 0 used to return a smaller number.
    print("\npreconditions of check() (not sign predicates):")
    from shell_check import check
    a_ok = [F(1), F(-11), F(1)]
    for eta, want_none, label in ((-F(1, 10), True, "eta = -1/10 rejected"),
                                 (-F(1), True, "eta = -1 rejected")):
        got = check(a_ok, rho=F(209, 100), eta=eta, verbose=False)
        good = (got is None) == want_none
        ok = ok and good
        print(("PASS  " if good else "FAIL  ") + label)
    n = len(cases()) + 2
    print("\n%d cases; SUITE: %s" % (n, "ALL EXPECTATIONS HOLD" if ok else "MISMATCH"))
    print("These same cases should be run against Computation's exactcert;"
          "\nthey are stated in Main's basis, so convert with "
          "interface_xcheck.main_to_comp.")
    return 0 if ok else 1


def against_exactcert(dirpath):
    """Run the same polynomials through Computation's exactcert sign engine.

    exactcert works in t = 2*pi*|x|^2 (so substitute u = t/2) and its engine is
    `yun_odd_part` followed by `_half_line_sign`, which is fail-closed: it
    returns 'fail' whenever the sign on [A, inf) is not constant, including when
    A itself is a root.  Each case therefore carries the verdict exactcert is
    expected to give.  'fail' where shell_check accepts a *touching* zero at the
    threshold is a POLICY difference, recorded, not a disagreement about
    mathematics.
    """
    sys.path.insert(0, dirpath)
    import exactcert as EC
    tt = sp.Symbol('t')
    T = t_hi_for(F(209, 100))
    Tr = sp.Rational(T.numerator, T.denominator)
    items = [
        ("q=(u-5)^2", (u - 5) ** 2, 0, 'pos'),
        ("q=-(u-5)^2", -(u - 5) ** 2, 0, 'neg'),
        ("q=(u-5)^3", (u - 5) ** 3, 0, 'fail'),
        ("q=(u-1)^2(u-2)^2", (u - 1) ** 2 * (u - 2) ** 2, 0, 'pos'),
        ("q=(u-1)^2(u-2)", (u - 1) ** 2 * (u - 2), 0, 'fail'),
        ("q=u^2", u ** 2, 0, 'pos'),
        ("q=prod_1..10", sp.prod(u - k for k in range(1, 11)), 0, 'fail'),
        ("p=-(u-T)^2", -(u - Tr) ** 2, Tr, 'neg'),   # even-multiplicity endpoint root: exactcert factors it out and decides
        ("p=(u-T)", u - Tr, Tr, 'fail'),
        ("p=-(u-T)", Tr - u, Tr, 'fail'),
        # review 0223 classes (t in exactcert's variable, so substitute u = t/2)
        ("(u-1)(u-3): exactcert sees a HALF-LINE from t=2, where it is not <= 0", (u - 1) * (u - 3), 2, 'fail'),
        ("(u-2)^3 on [0,inf) (t >= 0)", (u - 2) ** 3, 0, 'fail'),
        ("(u-2)^4 on [0,inf)", (u - 2) ** 4, 0, 'pos'),
        ("near-double (u-7/5)^2-2e-40", (u - sp.Rational(7, 5)) ** 2 - sp.Rational(2, 10 ** 40), 0, 'fail'),
        ("near-double above (u-7/5)^2+2e-40", (u - sp.Rational(7, 5)) ** 2 + sp.Rational(2, 10 ** 40), 0, 'pos'),
    ]
    ok = True
    for name, expr, A, want in items:
        pol = sp.Poly(sp.expand(expr.subs(u, tt / 2)), tt)     # u = t/2
        coeff = [F(int(pol.coeff_monomial(tt ** i).p), int(pol.coeff_monomial(tt ** i).q))
                 for i in range(pol.degree() + 1)]
        c, odd = EC.yun_odd_part(coeff)
        verdict, reason = EC._half_line_sign(c, odd, F(A.numerator, A.denominator))
        good = (verdict == want)
        ok = ok and good
        note = "   <- endpoint-root policy (shell_check accepts the touching zero)" if verdict == 'fail' and want == 'fail' and A != 0 else ""
        print(("PASS  " if good else "FAIL  ") + name + "  [exactcert: %s, expected %s]%s" % (verdict, want, note))
    print("\nNOTE: exactcert's engine decides HALF-LINES only; compact-interval claims"
          "\n(such as [1,3]) are not in its scope and are covered by function_range instead.")
    print("CROSS-RUN:", "AGREES with exactcert on every case" if ok else "DISAGREES")
    return 0 if ok else 1


if __name__ == "__main__":
    if "--against-exactcert" in sys.argv:
        sys.exit(against_exactcert(sys.argv[sys.argv.index("--against-exactcert") + 1]))
    sys.exit(main())
