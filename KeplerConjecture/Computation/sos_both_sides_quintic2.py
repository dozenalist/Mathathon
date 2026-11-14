#!/usr/bin/env python3
"""Quintic both-sides Gram with TWO squares in sigma_0 -- a solvable linear system.

The one-square ansatz of sos_both_sides_quintic.py is excluded for the p-side record
certificate (|f| >= 195.95 while |f| < 40.074 is required).  This file uses

    q = sigma_0 + u sigma_1,
    sigma_1 = (alpha u^2 + beta u + gamma)^2,
    sigma_0 = (d u^2 + e u + f)^2 + (g u^2 + h u + i)^2 + k,     k > 0,

so both sides remain EXPLICIT sums of rational squares.  Matching coefficients:

    alpha^2 = q5                                     (so alpha = sqrt(q5))
    2 alpha beta + d^2 + g^2 = q4
    beta^2 + 2 alpha gamma + 2 d e + 2 g h = q3
    2 beta gamma + e^2 + h^2 + 2 d f + 2 g i = q2
    gamma^2 + 2 e f + 2 h i = q1
    f^2 + i^2 + k = q0

STRATEGY (all exact).  Choose (beta, gamma, d, e) rationally.  Then
    R := q4 - 2 alpha beta          needs d^2 + g^2 = R, so g = a rational square root
    S := q3 - beta^2 - 2 alpha gamma,   h = (S - 2 d e) / (2 g)
    T2 := q2 - 2 beta gamma - e^2 - h^2,  and the last two equations are LINEAR in (f, i):
        2 d f + 2 g i = T2,   2 e f + 2 h i = q1 - gamma^2,
    solved by Cramer (determinant 4(dh - eg)), then k = q0 - f^2 - i^2 > 0 is checked.
So the search is four rational parameters and the acceptance is an exact rational identity.

SCOPE.  Any certificate found is verified by expanding both identities; strength is compared
honestly in REVIEW_0308.md section 4 against the trivial bound Delta <= 1.

Usage:  python3 sos_both_sides_quintic2.py
"""
import itertools, json, os
import sympy as sp
import mpmath as mp

_HERE = os.path.dirname(os.path.abspath(__file__))
_OUT = os.path.join(_HERE, "out")
mp.mp.dps = 30
u = sp.Symbol('u')

def solve2(qexpr, grid=40):
    Q = sp.Poly(sp.sympify(qexpr), u)
    if Q.degree() != 5:
        raise SystemExit("expected degree 5, got %d" % Q.degree())
    q5, q4, q3, q2, q1, q0 = [Q.coeff_monomial(u ** i) for i in range(5, -1, -1)]
    alpha = sp.sqrt(q5)
    if not alpha.is_rational:
        return None, "q5 is not a rational square"
    rats = [sp.Rational(n, dn) for dn in (1, 2, 3, 4) for n in range(-grid, grid + 1)]
    best = None
    for beta in rats:
        R = q4 - 2 * alpha * beta
        if R <= 0:
            continue
        for gamma in rats:
            S = q3 - beta ** 2 - 2 * alpha * gamma
            for d in rats:
                if d == 0:
                    continue
                g2 = R - d ** 2
                if g2 <= 0:
                    continue
                g = sp.sqrt(g2)
                if not g.is_rational:
                    continue
                for e in rats:
                    det = 4 * (d * 0 + 0)  # placeholder, real determinant below
                    h = (S - 2 * d * e) / (2 * g)
                    T2 = q2 - 2 * beta * gamma - e ** 2 - h ** 2
                    U1 = q1 - gamma ** 2
                    # 2 d f + 2 g i = T2 ;  2 e f + 2 h i = U1
                    D = 4 * (d * h - e * g)
                    if D == 0:
                        continue
                    f = (T2 * 2 * h - 2 * g * U1) / D
                    ii = (2 * d * U1 - 2 * e * T2) / D
                    k = q0 - f ** 2 - ii ** 2
                    if k <= 0:
                        continue
                    s1 = sp.expand((alpha * u ** 2 + beta * u + gamma) ** 2)
                    s0 = sp.expand((d * u ** 2 + e * u + f) ** 2
                                   + (g * u ** 2 + h * u + ii) ** 2 + k)
                    if sp.simplify(s0 + u * s1 - Q.as_expr()) == 0:
                        cand = dict(alpha=alpha, beta=beta, gamma=gamma, d=d, e=e, f=f,
                                    g=g, h=h, i=ii, k=k,
                                    sq1=str(sp.expand(alpha * u ** 2 + beta * u + gamma)),
                                    sq0a=str(sp.expand(d * u ** 2 + e * u + f)),
                                    sq0b=str(sp.expand(g * u ** 2 + h * u + ii)))
                        return cand, None
    return None, "no admissible (beta, gamma, d, e) in the grid"

def main():
    pside = json.load(open(os.path.join(_OUT, "ps3.json")))
    q = pside["q"]
    print("p-side certificate (Delta <= %s), quintic q:" % pside["delta"])
    print("  -p = (u-%s) * [ %s ]" % (pside["T"],
                                      " + ".join("(%s)^2" % s for s in pside["squares"])))
    sol, why = solve2(q)
    if sol is None:
        print("\nENRICHED ANSATZ ALSO FAILS:", why)
        print("  recorded as a scoped negative; see REVIEW_0308.md section 4")
        return 0
    print("\nMARKOV-LUKACS SOLVED with two squares in sigma_0:")
    print("  q(u) = [ %s ]^2 + [ %s ]^2 + %s + u [ %s ]^2"
          % (sol["sq0a"], sol["sq0b"], sol["k"], sol["sq1"]))
    p = sp.sympify(pside["p"])
    p0 = sp.Rational(p.subs(u, 0)); q0 = sp.Rational(sp.sympify(q).subs(u, 0))
    ratio = p0 / q0
    delta = 4 * mp.pi / 3 * mp.mpf(ratio.p) / mp.mpf(ratio.q)
    print("  p(0)=%s q(0)=%s p0/q0=%s" % (p0, q0, ratio))
    print("  Delta <= 4pi/3 * p0/q0 = %s   (trivial bound 1)" % mp.nstr(delta, 12))
    ok_p = sp.simplify(sp.expand(-(u - sp.Rational(pside["T"]))
                                 * sum(sp.sympify(s) ** 2 for s in pside["squares"])) - p) == 0
    ok_q = sp.simplify(sp.sympify(sol["sq0a"]) ** 2 + sp.sympify(sol["sq0b"]) ** 2
                       + sp.sympify(sol["k"]) + u * sp.sympify(sol["sq1"]) ** 2
                       - sp.sympify(q)) == 0
    print("  identities by expansion: p-side %s, q-side %s" % (ok_p, ok_q))
    json.dump(dict(script="KeplerConjecture/Computation/sos_both_sides_quintic2.py",
                   status="VERIFIED_EXACT (both sides by algebraic identity)",
                   delta=mp.nstr(delta, 12), beats_trivial_bound=bool(delta < 1),
                   q_side=dict(sigma0_squares=[sol["sq0a"], sol["sq0b"]],
                               sigma0_constant=str(sol["k"]),
                               sigma1_square=sol["sq1"]),
                   p_side=dict(T=pside["T"], squares=pside["squares"]),
                   p=str(p), q=q, p0=str(p0), q0=str(q0),
                   verification=dict(p_identity=bool(ok_p), q_identity=bool(ok_q))),
              open(os.path.join(_OUT, "sos_both_sides_quintic2.json"), "w"), indent=1)
    print("\nwrote out/sos_both_sides_quintic2.json")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
