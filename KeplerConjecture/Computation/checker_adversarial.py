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
    return out


def main():
    ok = True
    print("adversarial sign-checker suite (T = pi_lo*rho^2 = %s)" % t_hi_for(F(209, 100)))
    for name, got, want in cases():
        good = (got == want)
        ok = ok and good
        print(("PASS  " if good else "FAIL  ") + name + ("" if good else "   (got %s)" % got))
    print("\nSUITE:", "ALL EXPECTATIONS HOLD" if ok else "MISMATCH")
    print("These same cases should be run against Computation's exactcert;"
          "\nthey are stated in Main's basis, so convert with "
          "interface_xcheck.main_to_comp.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
