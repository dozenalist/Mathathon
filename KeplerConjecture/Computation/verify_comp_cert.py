#!/usr/bin/env python3
"""Independently check a Computation-format certificate with Main's checker.

Computation's JSON stores `coefficients_rational` = c in the Laguerre basis
    f = sum_k c_k L_k^{1/2}(t) e^{-t/2},   t = 2 pi |x|^2,
and its verdict comes from exactcert.py.  This script converts c to Main's
monomial basis in u = pi|x|^2 = t/2,
    P(u) = sum_k c_k L_k^{1/2}(2u),
and then decides the same two sign conditions with shell_check's independent
Sturm code (different implementation, same mathematics).  Agreement of the
verdict and of the final Delta is the audit this file exists for.

Usage: python3 verify_comp_cert.py <certificate.json>
"""
import json, sys
from fractions import Fraction as F
import sympy as sp

sys.path.insert(0, str(__file__).rsplit('/', 1)[0])
from shell_check import check, PI_LO, PI_HI

t = sp.Symbol('t')
u = sp.Symbol('u')


def comp_c_to_main_P(c):
    K = len(c) - 1
    expr = sum(sp.Rational(c[k].numerator, c[k].denominator)
               * sp.expand(sp.assoc_laguerre(k, sp.Rational(1, 2), t))
               for k in range(K + 1))
    P = sp.expand(expr.subs(t, 2 * u))
    pol = sp.Poly(P, u)
    return [F(int(pol.coeff_monomial(u ** i).p), int(pol.coeff_monomial(u ** i).q))
            for i in range(K + 1)]


def main(path):
    d = json.load(open(path))
    c = [F(x) for x in d["coefficients_rational"]]
    print("certificate:", path)
    print("  claimed     :", d.get("theorem"))
    print("  degree      :", len(c) - 1)
    P = comp_c_to_main_P(c)
    print("  converted to Main's monomial basis in u = pi|x|^2")
    out = check(P, rho=F(2), eta=F(0), count=0)
    print("\n  Main checker:", "ACCEPT" if out else "REJECT")
    if out:
        print("  Delta in (%.12f, %.12f)" % (float(out[0]), float(out[1])))
        stored = d.get("delta_upper") or d.get("Delta_upper") or d.get("delta")
        if stored is not None:
            print("  stored      :", stored)
            same = abs(float(out[1]) - float(stored)) < 1e-9
            print("  agreement   :", "PASS" if same else "CHECK (differs)")
    return 0 if out else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
