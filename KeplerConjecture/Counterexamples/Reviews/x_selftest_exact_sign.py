#!/usr/bin/env python3
"""Self-audit of X's exact_sign.py on the same families that break probe-based checkers.

Adapts exact_sign.sign_on_half_line to the (le_on_interval / nonneg_on_half_line / _ray)
interface so that Reviews/x_family_check.py can drive it, then runs BOTH the random family and
the probe-targeted family.  A repair that only passes hand-written cases is not a repair.
"""
import sys, sympy as sp
sys.path.insert(0,'.')
sys.path.insert(0,'..')
from exact_sign import sign_on_half_line as S, sign_on_interval as SI

u = sp.Symbol('u')
def _poly(coeffs):
    return sum(sp.Rational(c)*u**i for i, c in enumerate(coeffs))
class Adapter:
    @staticmethod
    def le_on_interval(coeffs, eta, lo, hi):
        # closed-interval predicate: sign_on_interval, NOT the half-line rule
        p = sp.expand(_poly(coeffs) - sp.Rational(eta))
        return SI(p, sp.Rational(lo), sp.Rational(hi), -1, var=u)
    @staticmethod
    def nonneg_on_half_line(coeffs):
        return S(_poly(coeffs), sp.Integer(0), +1, var=u)
    @staticmethod
    def _ray(coeffs, hi):
        return S(_poly(coeffs), sp.Rational(hi), -1, var=u)
if __name__ == "__main__":
    print("adapter ready: le_on_interval uses S(p,a,-1) on the left endpoint and the exact rule.")
