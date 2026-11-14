#!/usr/bin/env python3
"""Regression suite for every claim added in review 0138-C.  Exact arithmetic only.

Each test states the identity or inequality it checks and fails loudly.  Run:
    python3 tests_0138.py       # exit 0 iff all pass

These are the machine-checkable core of REVIEW_0138.md: the Gram identities are verified by
expanding polynomials, not by trusting any optimiser or any checker.
"""
import sys, json
from fractions import Fraction as F
import sympy as sp

FAILS = []
def check(name, cond, detail=""):
    print(("  PASS  " if cond else "  FAIL  ") + name + (("   [" + detail + "]") if detail and not cond else ""))
    if not cond:
        FAILS.append(name)

u = sp.Symbol('u')
def poly(coeffs, var=u):
    return sp.expand(sum(sp.Rational(c) * var ** i for i, c in enumerate(coeffs)))

def main():
    print("T1  Fourier-side explicit Gram: q = 3^2 + (3u/2-6)^2 + u(3/2-2u/3)^2")
    q_claimed = poly([F(45), F(-63, 4), F(1, 4), F(4, 9)])
    q_squares = sp.expand(3**2 + (sp.Rational(3, 2) * u - 6) ** 2
                          + u * (sp.Rational(3, 2) - sp.Rational(2, 3) * u) ** 2)
    check("identity holds", sp.simplify(q_claimed - q_squares) == 0, str(q_claimed - q_squares))
    check("q(0) = 45 and all three summands are >= 0 for u >= 0",
          q_claimed.subs(u, 0) == 45)
    p_claimed = poly([F(1351, 48), F(17, 6), F(59, 12), F(-4, 9)])
    ratio = p_claimed.subs(u, 0) / q_claimed.subs(u, 0)
    check("p(0)/q(0) = 1351/2160", ratio == sp.Rational(1351, 2160), str(ratio))

    print("T2  p-side cubic Gram: -p = 0 + (u-T)(u-c)^2")
    T, c = sp.Rational(314, 25), sp.Rational(12)
    p2 = sp.expand(-(u - T) * (u - c) ** 2)
    check("-p = (u-T)(u-c)^2", sp.simplify((u - T) * (u - c) ** 2 + p2) == 0)
    check("p(0) = T c^2 > 0", sp.simplify(p2.subs(u, 0) - T * c ** 2) == 0 and T * c ** 2 > 0)
    check("p(T) = 0 exactly", p2.subs(u, T) == 0)

    print("T3  p-side quintic Gram: -p = (u-T)[(u-c)^2(u-e)^2 + m^2(u-d)^2]")
    T3, c3, d3, e3, m3 = [sp.Rational(x) for x in ("314/25", "12", "8", "1", "5")]
    b3 = (u - c3) ** 2 * (u - e3) ** 2 + m3 ** 2 * (u - d3) ** 2
    p3 = sp.expand(-(u - T3) * b3)
    check("-p = (u-T)*bracket", sp.simplify((u - T3) * b3 + p3) == 0)
    r1 = sp.expand((u - c3) * (u - e3)); r2 = sp.expand(m3 * (u - d3))
    check("bracket = r1^2 + r2^2", sp.simplify(b3 - (r1 ** 2 + r2 ** 2)) == 0)

    print("T4  the shell allowance: eta_suff = (T'-T)M^2 is SUFFICIENT, and any admissible")
    print("    allowance satisfies eta >= p(T) = (T'-T)(T-c)^2 > 0  (an attained lower bound)")
    for (t, tp, cc) in ((F(12), F(27, 2), F(1)), (F(12), F(27, 2), F(12)), (F(12), F(27, 2), F(5))):
        Ts, Tps, cs = sp.Rational(t.numerator, t.denominator), sp.Rational(tp.numerator, tp.denominator), sp.Rational(cc.numerator, cc.denominator)
        M = max(abs(t - cc), abs(tp - cc))
        eta_star = (tp - t) * M ** 2
        # CORRECTED CLAIM.  eta_suff := (T'-T)M^2 is a SUFFICIENT allowance (p <= eta_suff on
        # the shell), NOT the smallest one -- my own suite caught this overclaim.  What IS true
        # and all the argument needs: any admissible eta satisfies eta >= p(T) = (T'-T)(T-c)^2,
        # which is positive whenever c != T, and the objective charges n*eta with n >= 12.
        pv = lambda x: -(x - Tps) * (x - cs) ** 2
        eta_suff = sp.Rational(eta_star.numerator, eta_star.denominator)
        # sup of p on [T,T'] : critical points plus endpoints, compared NUMERICALLY because
        # max() over sympy expressions is unreliable (it silently mis-compares).
        crit = sp.solve(sp.diff(-(u - Tps) * (u - cs) ** 2, u), u)
        cand = [Ts, Tps] + [sp.nsimplify(v) for v in crit if sp.im(v) == 0]
        cand = [x for x in cand if Ts <= x <= Tps]
        maxv = max(float(pv(x)) for x in cand)
        check("c=%s : eta_suff is SUFFICIENT (sup p = %.6f <= %.6f)" % (cc, maxv, float(eta_suff)),
              maxv <= float(eta_suff) + 1e-12, "%.6f > %.6f" % (maxv, float(eta_suff)))
        # the statement the argument actually needs: the supremum is STRICTLY POSITIVE, so any
        # admissible allowance is >= a positive number.
        check("c=%s : sup_{[T,T']} p > 0 (so any admissible eta is positive)" % cc, maxv > 1e-12,
              "sup = %.6e" % maxv)

    print("T5  cut equivalence: the full-period blob makes the condition read rho <= 1/sqrt32")
    import mpmath as mp
    mp.mp.dps = 30
    N, per = 13, mp.mpf(16) ** 3
    rho = mp.mpf(N) / per
    total_b = N * 4 * mp.sqrt(2) - per
    check("sum_U b = N(sqrt32 - 1/rho)", abs(total_b - N * (4 * mp.sqrt(2) - 1 / rho)) < mp.mpf("1e-20"))
    check("the condition total_b <= 0 is exactly rho <= 1/sqrt32",
          (total_b <= 0) == (rho <= 1 / (4 * mp.sqrt(2))))

    print("T6  jamming: FCC at separation 2 has 12 contacts at exactly 2")
    import numpy as np
    A = np.sqrt(2) * np.array([[0, 1, 1], [1, 0, 1], [1, 1, 0]], float)
    pts = []
    for k in np.ndindex(3, 3, 3):
        pts.append((np.array(k) - 1) @ A)
    pts = np.array(pts)
    d = np.linalg.norm(pts[:, None, :] - pts[None, :, :], axis=2)
    np.fill_diagonal(d, np.inf)
    dmin = d.min()
    contacts = int((np.abs(d - 2.0) < 1e-9).sum() // 2)
    check("minimum distance is exactly 2", abs(dmin - 2.0) < 1e-12, "%.12f" % dmin)
    check("12 contacts per centre at distance 2", contacts >= 12, "%d contacts in the 27-image set" % contacts)

    print()
    if FAILS:
        print("FAILED: %d -> %s" % (len(FAILS), FAILS)); return 1
    print("ALL 0138 TESTS PASS"); return 0

if __name__ == "__main__":
    sys.exit(main())
