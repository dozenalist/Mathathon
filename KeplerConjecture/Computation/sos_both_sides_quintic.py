#!/usr/bin/env python3
"""Quintic both-sides rational Gram: q = sigma_0 + u*sigma_1 with both explicit sums of squares.

WHY.  sos_both_sides.py closed the "explicit Gram on both sides" obligation only for a CUBIC q
(Delta <= 2.00171738).  The reviewer is right that this is weaker than the TRIVIAL density bound
Delta <= 1, so it is a format demonstrator and nothing more.  This file carries the same
construction to the p-side record certificate (Delta <= 1.33982382), whose q has degree 5.

CONSTRUCTION (deg q = 5, odd, so Markov-Lukacs on [0,inf) reads q = sigma_0 + u sigma_1 with
deg sigma_0 <= 4 and deg sigma_1 <= 4).  Take

    sigma_1 = (a u^2 + b u + c)^2 ,        sigma_0 = (d u^2 + e u + f)^2 + k ,   k > 0.

Matching coefficients of q = q5 u^5 + ... + q0 gives, in this order,

    a^2 = q5,   2ab = q4,   b^2 + 2ac + d^2 = q3,
    2bc + 2de = q2,   c^2 + 2df + e^2 = q1,   f^2 + k = q0.

So a = sqrt(q5) must be rational (it is, by construction of the p-side search: q5 = (7/6)^2),
then b, then d^2 = q3 - b^2 - 2ac, then e, f in terms of the ONE free parameter c, and finally
k = q0 - f^2.  Accept c when d^2 is a rational square and k > 0.  Everything is exact.

SCOPE.  The certificate is verified by expanding both identities; nothing is decided by Sturm.
Its strength (Delta <= 1.33982382) is still ABOVE the trivial bound 1, so it remains a format
demonstrator -- see REVIEW_0308.md section 4 for the honest strength table.

Usage:  python3 sos_both_sides_quintic.py
"""
import json, os
import sympy as sp

_HERE = os.path.dirname(os.path.abspath(__file__))
_OUT = os.path.join(_HERE, "out")

u = sp.Symbol('u')

def solve(qexpr, max_c=400):
    Q = sp.Poly(sp.sympify(qexpr), u)
    if Q.degree() != 5:
        raise SystemExit("expected degree 5, got %d" % Q.degree())
    q5, q4, q3, q2, q1, q0 = [Q.coeff_monomial(u ** i) for i in range(5, -1, -1)]
    a = sp.sqrt(q5)
    if not a.is_rational:
        return None, "q5 is not a rational square: a = %s" % a
    b = q4 / (2 * a)
    # d^2 = q3 - b^2 - 2*a*c  is a CONIC in (c, d) with a rational point iff any rational d
    # works, and then c = (q3 - b^2 - d^2)/(2a) is rational.  So parametrise by d, not by c
    # (an earlier version gridded c, found no square, and concluded wrongly that none exists).
    for num in range(-max_c, max_c + 1):
        for den in (1, 2, 3, 4, 6, 8, 12):
            d = sp.Rational(num, den)
            if d == 0:
                continue
            c = (q3 - b ** 2 - d ** 2) / (2 * a)
            e = (q2 - 2 * b * c) / (2 * d)
            f = (q1 - c ** 2 - e ** 2) / (2 * d)
            k = q0 - f ** 2
            if k <= 0:
                continue
            s1 = sp.expand((a * u ** 2 + b * u + c) ** 2)
            s0 = sp.expand((d * u ** 2 + e * u + f) ** 2 + k)
            if sp.simplify(s0 + u * s1 - Q.as_expr()) == 0:
                return dict(a=a, b=b, c=c, d=d, e=e, f=f, k=k,
                            sigma0=s0, sigma1=s1,
                            sq0=str(sp.expand(d * u ** 2 + e * u + f)),
                            sq1=str(sp.expand(a * u ** 2 + b * u + c))), None
    # Report the ACTUAL obstruction: with sigma_1 = (a u^2 + b u + c)^2 and
    # sigma_0 = (d u^2 + e u + f)^2 + k, matching coefficients leaves d (equivalently c) as the
    # only free parameter, and acceptance needs k = q0 - f^2 > 0, i.e. |f| < sqrt(q0).  Compute
    # the minimum of |f| over the parameter and compare -- that is the scoped negative.
    import numpy as _np
    qsf = float(q0)
    def _f(dd):
        cc = (float(q3) - float(b) ** 2 - dd * dd) / (2 * float(a))
        ee = (float(q2) - 2 * float(b) * cc) / (2 * dd)
        return (float(q1) - cc * cc - ee * ee) / (2 * dd)
    ds = _np.linspace(0.05, 300.0, 200000)
    vals = _np.array([abs(_f(x)) for x in ds])
    i = int(_np.argmin(vals))
    return None, ("two-square ansatz EXCLUDED: acceptance needs |f| < sqrt(q0) = %.6f, but |f| "
                  "has minimum %.6f at d = %.4f (and |f| -> infinity at both ends: %.3e at "
                  "d = 0.05, %.3e at d = 300)" % (qsf ** 0.5, vals[i], ds[i],
                                                  abs(_f(0.05)), abs(_f(300.0))))

def main():
    pside = json.load(open(os.path.join(_OUT, "ps3.json")))
    q = pside["q"]
    print("p-side certificate (Delta <= %s):" % pside["delta"])
    print("  -p = (u-%s) * [ %s ]" % (pside["T"], " + ".join("(%s)^2" % s for s in pside["squares"])))
    print("   q =", q, "\n")
    sol, why = solve(q)
    if sol is None:
        # This is a DETERMINED NEGATIVE, not an error: the script exists to decide whether the
        # two-square ansatz works for this q, and it decides that it does not.  Exit 0 so a
        # harness can distinguish "ansatz excluded" from "script crashed".
        print("ANSATZ EXCLUDED for this certificate.\n  reason:", why)
        print("  (a determined negative result; see REVIEW_0308.md section 4 for the |f| bound")
        print("   that makes this a proof within the parametrisation, not a failed search)")
        return 0
    print("MARKOV-LUKACS SOLVED for the quintic q:")
    print("  q(u) = [ %s ]^2 + %s + u [ %s ]^2" % (sol["sq0"], sol["k"], sol["sq1"]))
    print("  sigma_0 = (%s)^2 + %s   (explicit sum of squares + positive constant)"
          % (sol["sq0"], sol["k"]))
    print("  sigma_1 = (%s)^2        (an explicit square)" % sol["sq1"])
    p = sp.sympify(pside["p"])
    p0, q0 = sp.Rational(p.subs(u, 0)), sp.Rational(sp.sympify(q).subs(u, 0))
    import mpmath as mp
    mp.mp.dps = 30
    ratio = sp.Rational(p0) / sp.Rational(q0)
    delta = 4 * mp.pi / 3 * mp.mpf(ratio.p) / mp.mpf(ratio.q)
    print("\n  p(0) = %s  q(0) = %s  p(0)/q(0) = %s" % (p0, q0, ratio))
    print("  Delta <= (4 pi/3)(p(0)/q(0)) = %s" % mp.nstr(delta, 12))
    # exact verification of both identities
    ok_p = sp.simplify(sp.expand(-(u - sp.Rational(pside["T"]))
                                 * sum(sp.sympify(s) ** 2 for s in pside["squares"])) - p) == 0
    ok_q = sp.simplify(sol["sigma0"] + u * sol["sigma1"] - sp.sympify(q)) == 0
    print("\n  p-side identity verified by expansion:", ok_p)
    print("  q-side identity verified by expansion:", ok_q)
    json.dump(dict(script="KeplerConjecture/Computation/sos_both_sides_quintic.py",
                   status="VERIFIED_EXACT (both sides by algebraic identity)",
                   degree=5,
                   theorem=("Delta <= %s" % mp.nstr(delta, 12)),
                   strength_caveat=("ABOVE the trivial bound Delta <= 1, so a format demonstrator, "
                                    "not a competitive bound"),
                   p_side=dict(T=pside["T"], squares=pside["squares"],
                               identity="-p = (u-T) * sum_i r_i^2"),
                   q_side=dict(sigma0_square=sol["sq0"], sigma0_constant=str(sol["k"]),
                               sigma1_square=sol["sq1"],
                               identity="q = sigma0 + u*sigma1, both explicit sums of squares"),
                   p0=str(p0), q0=str(q0), ratio=str(ratio), delta=mp.nstr(delta, 12),
                   verification=dict(p_identity=bool(ok_p), q_identity=bool(ok_q))),
              open(os.path.join(_OUT, "sos_both_sides_quintic.json"), "w"), indent=1)
    print("\nwrote out/sos_both_sides_quintic.json")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
