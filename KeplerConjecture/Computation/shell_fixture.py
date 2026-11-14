#!/usr/bin/env python3
"""A small-degree EXACT shell-allowance fixture (K15-C028).

Family (chosen so that the shell condition holds by construction):
    P(u) = (T - u) * S(u),      S(u) = sum_j s_j u^j  with all s_j >= 0,
    u = pi|x|^2,   T = pi_lo * rho^2   (rational, <= pi*rho^2).
Then
  * p(0) = T*s_0 > 0,
  * p <= 0 for u >= T, hence f <= 0 for |x| >= rho   (exactly, no grid),
  * f <= eta on the shell 2 <= |x| <= rho  is NOT automatic: it is checked
    exactly on [4*pi_lo, T] by the odd-part Sturm test.
The remaining condition is q >= 0 on u >= 0, decided exactly.

The search below is a coarse rational enumeration; it is a PROPOSER. The verdict
on every candidate comes from shell_check's exact tests, so a PASS is a theorem
conditional only on the shell count (12 at rho = 2.09, K15-C027).

Usage: python3 shell_fixture.py [--m 2] [--rho 209/100] [--eta 0]
"""
import argparse, itertools, sys
from fractions import Fraction as F
import sympy as sp

sys.path.insert(0, str(__file__).rsplit('/', 1)[0])
from shell_check import (fourier_map, check, le_on_interval, nonneg_on_half_line,
                         _ray, PI_LO, t_hi_for)

u = sp.Symbol('u')


def build(s, T, m):
    S = sum(sp.Rational(s[j].numerator, s[j].denominator) * u ** j for j in range(m + 1))
    P = sp.expand((T - u) * S)
    pol = sp.Poly(P, u)
    return [F(int(pol.coeff_monomial(u ** i).p), int(pol.coeff_monomial(u ** i).q))
            for i in range(m + 2)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--m", type=int, default=2)
    ap.add_argument("--rho", type=str, default="209/100")
    ap.add_argument("--eta", type=str, default="0")
    ap.add_argument("--grid", type=str, default="0,1/4,1/2,1,2,4,8")
    args = ap.parse_args()
    rho = F(args.rho)
    eta = F(args.eta)
    m = args.m
    T = PI_LO * rho * rho
    levels = [F(x) for x in args.grid.split(",")]
    best = None
    tested = 0
    for s in itertools.product(levels, repeat=m + 1):
        if s[0] == 0:
            continue
        a = build(s, T, m)
        tested += 1
        # exact conditions on the polynomial P (no grids)
        if not _ray(a, T):                     # p <= 0 beyond T
            continue
        if eta > 0 and not le_on_interval(a, eta, 4 * PI_LO, T):
            continue
        M = fourier_map(m + 1)
        b = [sum(M[i, k] * sp.Rational(a[k].numerator, a[k].denominator)
                 for k in range(m + 2)) for i in range(m + 2)]
        if not nonneg_on_half_line([F(int(x.p), int(x.q)) for x in b]):
            continue
        q0 = sp.Rational(b[0].p, b[0].q)
        R = sp.Rational(a[0].numerator, a[0].denominator) / q0
        if best is None or R < best[0]:
            best = (R, s, a)
    print("rho =", rho, " eta =", eta, " T =", T, " candidates tested:", tested)
    if best is None:
        print("RESULT: no admissible candidate in this family at this resolution")
        return 1
    R, s, a = best
    print("best s =", [str(x) for x in s])
    print("P coefficients a =", [str(x) for x in a])
    print("R = p(0)/q(0) =", R, "=", float(R))
    print("Delta <= (4pi/3)R, pi-enclosed: (%.6f, %.6f)" %
          (float(4 * PI_LO / 3 * R), float(4 * F(355, 113) / 3 * R)))
    print("\nfull exact verdict via shell_check:")
    out = check(a, rho=rho, eta=eta, count=12)
    return 0 if out else 2


if __name__ == "__main__":
    sys.exit(main())
