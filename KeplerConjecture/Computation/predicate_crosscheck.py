#!/usr/bin/env python3
"""Independent cross-check of the sign predicates via SymPy's exact function_range.

`function_range` computes the exact range of a polynomial on an interval by a
different route (critical points and endpoints, not Sturm chains), so agreement is
meaningful evidence that the repaired predicates of K15-C049 are right.

Covers the three reported cases, the touching cases, and a small random batch on
compact intervals (the unbounded cases are covered by the fuzz script).

Usage: python3 predicate_crosscheck.py [--n 20]
"""
import argparse, random, sys
import sympy as sp
from sympy.calculus.util import function_range

sys.path.insert(0, str(__file__).rsplit('/', 1)[0])
from shell_check import le_on_interval

u = sp.Symbol('u')


def coeffs(e):
    P = sp.Poly(sp.expand(e), u)
    return [sp.Rational(P.coeff_monomial(u ** i)) for i in range(P.degree() + 1)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=20)
    ap.add_argument("--seed", type=int, default=11)
    args = ap.parse_args()
    fixed = [("u(1-u) on [0,1]", u * (1 - u), 0, 1, False),
             ("u(u-1) on [0,1]", u * (u - 1), 0, 1, True),
             ("-(u-1/2)^2 on [0,1]", -(u - sp.Rational(1, 2)) ** 2, 0, 1, True),
             ("(u-1/2)^2 on [0,1]", (u - sp.Rational(1, 2)) ** 2, 0, 1, False),
             ("(u-5)^2 <= 0 on [0,10]", (u - 5) ** 2, 0, 10, False)]
    bad = 0
    for name, e, lo, hi, want in fixed:
        mine = le_on_interval(coeffs(e), 0, lo, hi)
        rng = function_range(e, u, sp.Interval(lo, hi))
        theirs = bool(rng.sup <= 0)
        ok = (mine == theirs == want)
        bad += 0 if ok else 1
        print(("PASS " if ok else "FAIL ") + "%-24s mine=%-5s range sup=%-8s" % (name, mine, rng.sup))
    rng_ = random.Random(args.seed)
    n = 0
    for _ in range(args.n):
        d = rng_.randint(1, 3)
        cs = [rng_.randint(-3, 3) for _ in range(d + 1)]
        e = sum(c * u ** i for i, c in enumerate(cs))
        lo = sp.Rational(rng_.randint(0, 3), 2)
        hi = lo + sp.Rational(rng_.randint(1, 2))
        mine = le_on_interval(coeffs(e), 0, lo, hi)
        theirs = bool(function_range(e, u, sp.Interval(lo, hi)).sup <= 0)
        n += 1
        if mine != theirs:
            bad += 1
            print("DISAGREE:", sp.factor(e), lo, hi, mine, theirs)
    print("\nrandom cases: %d, disagreements: %d" % (n, bad))
    print("RESULT:", "agrees with function_range" if bad == 0 else "DISAGREEMENTS")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
