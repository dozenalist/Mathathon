#!/usr/bin/env python3
"""Cross-run Main's half-line predicates against X's independent `exact_sign`.

X's `sign_on_half_line(p, a, want)` works in the variable `t = 2π|x|²`; Main's
predicates work in `u = π|x|² = t/2`.  The substitution is exact, so the two must
agree claim by claim.  This script runs the half-line claims of the adversarial
suite (plus both defect families) through both.

Usage: python3 xsign_crossrun.py <dir containing exact_sign.py>
Exit 0 iff every claim agrees.
"""
import sys
from fractions import Fraction as F
import sympy as sp

sys.path.insert(0, str(__file__).rsplit('/', 1)[0])
from shell_check import nonneg_on_half_line, _ray


def main(dirpath):
    sys.path.insert(0, dirpath)
    from exact_sign import sign_on_half_line
    t = sp.Symbol('t')
    u = sp.Symbol('u')

    def main_verdict(expr_t, a_t, want):
        """Main's predicate on the same claim, in u = t/2."""
        e = sp.expand(expr_t.subs(t, 2 * u))
        P = sp.Poly(e, u)
        c = [sp.Rational(P.coeff_monomial(u ** i)) for i in range(P.degree() + 1)]
        a_u = sp.Rational(a_t) / 2
        if want == +1:
            return nonneg_on_half_line(c) if a_u == 0 else None
        return _ray(c, a_u)

    claims = [
        ("(t^2-2)(t^2-3) >= 0 on [0,inf)", (t ** 2 - 2) * (t ** 2 - 3), 0, +1),
        ("-(t^2-2)(t^2-3) >= 0 on [0,inf)", -((t ** 2 - 2) * (t ** 2 - 3)), 0, +1),
        ("(t-7/5)^2 - 2e-40 >= 0", (t - sp.Rational(7, 5)) ** 2 - sp.Rational(2, 10 ** 40), 0, +1),
        ("(t-7/5)^2 + 2e-40 >= 0", (t - sp.Rational(7, 5)) ** 2 + sp.Rational(2, 10 ** 40), 0, +1),
        ("(t-5)^2 >= 0", (t - 5) ** 2, 0, +1),
        ("(t-5)^3 >= 0", (t - 5) ** 3, 0, +1),
        ("t(t-1) >= 0 on [0,inf)", t * (t - 1), 0, +1),
        ("-(t-1)(t-3) <= 0 from 2 (Main _ray)", -((t - 1) * (t - 3)), 2, -1),
        ("(t-2)(t-4) <= 0 from 4 (Main _ray)", (t - 2) * (t - 4), 4, -1),
        ("(t-3)^2*(t-1) <= 0 from 1 (odd part)", (t - 3) ** 2 * (t - 1), 1, -1),
    ]
    bad = 0
    for name, expr, a, want in claims:
        theirs = sign_on_half_line(expr, a, want)
        ours = main_verdict(expr, a, want)
        if ours is None:
            print("SKIP  %-44s (Main has no half-line-from-%s nonneg form)" % (name, a))
            continue
        ok = (theirs == ours)
        bad += 0 if ok else 1
        print(("PASS  " if ok else "FAIL  ") + "%-44s X=%-5s Main=%-5s" % (name, theirs, ours))
    print("\nRESULT:", "all claims agree" if bad == 0 else "%d disagreements" % bad)
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print("usage: python3 xsign_crossrun.py <dir containing exact_sign.py>"); sys.exit(0 if len(sys.argv) > 1 else 2)
    sys.exit(main(sys.argv[1]))
