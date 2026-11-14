#!/usr/bin/env python3
"""Differential fuzz of the sign predicates (K15-C049 follow-up).

The predicates are exact; this script is *not* a proof, it is a bug-hunt in the
direction that matters.  For random integer polynomials it compares

    predicate(coeffs)            (exact)
    sampled(coeffs)              (a fine rational/float grid on [0, U])

and flags only the dangerous disagreement:

    predicate says "the condition holds"  AND  the sample finds a violation.

The reverse disagreement (predicate says False, sample finds nothing) is expected
and harmless: the violation may be beyond the sampled range or exactly at a point
the grid misses.

Covers all three predicates:
    nonneg_on_half_line(p)          p >= 0 on [0, inf)
    _ray(p, A)                      p <= 0 on [A, inf)
    le_on_interval(p, eta, lo, hi)  p <= eta on [lo, hi]

Usage: python3 predicate_fuzz.py [--n 2000] [--seed 0]
"""
import argparse, random, sys
import numpy as np
import sympy as sp

sys.path.insert(0, str(__file__).rsplit('/', 1)[0])
from shell_check import nonneg_on_half_line, le_on_interval, _ray


def coeffs_of(expr, var):
    P = sp.Poly(sp.expand(expr), var)
    return [sp.Rational(P.coeff_monomial(var ** i)) for i in range(P.degree() + 1)]


def sample_minmax(expr, lo, hi, n=40001):
    u = sp.Symbol('u')
    f = sp.lambdify(u, expr, 'numpy')
    xs = np.linspace(lo, hi, n)
    vals = f(xs)
    vals = np.atleast_1d(np.asarray(vals, dtype=float))
    return float(np.nanmin(vals)), float(np.nanmax(vals))


def structured_cases(rng, n):
    """Perfect squares and their negations: the family that defeated two repairs.

    Random coefficients in a box essentially never produce a polynomial all of
    whose roots have even multiplicity, so a uniform random fuzz cannot find this
    failure mode.  Here the polynomial is built AS a square on purpose:
        p = sign * prod_i (u - r_i)^2  with rational roots r_i.
    Its sign is constant (= sign) and it is zero at every r_i, so any checker that
    decides the sign only at the roots will accept the wrong inequality.
    """
    out = []
    for _ in range(n):
        m = rng.randint(1, 3)
        roots = [sp.Rational(rng.randint(-4, 6), rng.choice([1, 2, 3])) for _ in range(m)]
        expr = sp.prod((sp.Symbol('u') - r) ** 2 for r in roots)
        sign = rng.choice([1, -1])
        out.append((sign * expr, roots))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=2000)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--deg", type=int, default=6)
    args = ap.parse_args()
    rng = random.Random(args.seed)
    u = sp.Symbol('u')
    bad = 0
    checked = 0
    for _ in range(args.n):
        d = rng.randint(1, args.deg)
        cs = [rng.randint(-4, 4) for _ in range(d + 1)]
        if all(c == 0 for c in cs):
            continue
        expr = sum(c * u ** i for i, c in enumerate(cs))
        A = sp.Rational(rng.randint(0, 3), 2)
        ok_nonneg = nonneg_on_half_line(coeffs_of(expr, u))
        mn, mx = sample_minmax(expr, 0.0, 40.0)
        checked += 1
        if ok_nonneg and mn < -1e-9:
            print("FALSE ACCEPT (nonneg):", sp.factor(expr), "min sampled", mn)
            bad += 1
        ok_ray = _ray(coeffs_of(expr, u), A)
        _, mxA = sample_minmax(expr, float(A), 40.0)
        if ok_ray and mxA > 1e-9:
            print("FALSE ACCEPT (_ray at %s):" % A, sp.factor(expr), "max sampled", mxA)
            bad += 1
        lo = sp.Rational(rng.randint(0, 3), 2)
        hi = lo + sp.Rational(rng.randint(1, 4), 1)
        ok_int = le_on_interval(coeffs_of(expr, u), 0, lo, hi)
        _, mxI = sample_minmax(expr, float(lo), float(hi))
        if ok_int and mxI > 1e-9:
            print("FALSE ACCEPT (interval [%s,%s]):" % (lo, hi), sp.factor(expr), "max sampled", mxI)
            bad += 1
    # structured pass: perfect squares, the family that broke the first two repairs
    uu = sp.Symbol('u')
    sbad = 0
    for expr, roots in structured_cases(rng, max(20, args.n // 10)):
        cs = coeffs_of(expr, uu)
        for r in roots + [sp.Rational(1, 7)]:
            val = sp.simplify(expr.subs(uu, r))
            if val > 0:
                # a positive value must force the <=0 predicates to decline
                if nonneg_on_half_line([-c for c in cs]):
                    print("FALSE ACCEPT (structured, nonneg of -p):", sp.factor(expr), "at", r)
                    sbad += 1
                # p <= 0 on [0,inf) is FALSE when p > 0 somewhere: the predicate
                # must decline.  (Asking for "-p <= 0", i.e. "_ray(-p)", would be
                # true and correct -- that was a bug in the first version of this
                # structured test, not in the checker.)
                if _ray(coeffs_of(expr, uu), 0):
                    print("FALSE ACCEPT (structured, _ray of +p):", sp.factor(expr), "at", r)
                    sbad += 1
                break
    print("structured (perfect-square) cases also checked; false accepts:", sbad)
    bad += sbad
    print("\nchecked %d random polynomials, false accepts found: %d" % (checked, bad))
    print("RESULT:", "no false accept found" if bad == 0 else "FALSE ACCEPTS PRESENT")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
