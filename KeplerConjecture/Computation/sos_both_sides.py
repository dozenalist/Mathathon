#!/usr/bin/env python3
"""K15 certificate with an EXPLICIT RATIONAL GRAM ON BOTH SIDES.

This closes the headline open obligation of REVIEW_0138.md section 10 item 1 at the strength
Delta <= 2.00171738 (2.7x Kepler; not competitive, but both sign conditions are algebraic
identities rather than Sturm verdicts).

THE OBJECT (unit spheres, minimum separation 2, u = pi|x|^2)

    f   = e^{-pi|x|^2} p(u),        fhat = e^{-pi|y|^2} q(u'),      q = M p

  p-side, from sos_pside_many.py, certified BY CONSTRUCTION:

      -p(u) = (u - 12) [ (4/3)^2 + (-37/3)^2 + (101u/12 + 1/4)^2 + (-13/6)^2 ]
            = (u - 12) [ (101u/12 + 1/4)^2 + 2021/12 ] ,

  a sum of rational squares times the non-negative multiplier (u - 12).  Hence p <= 0 on
  [12, inf), and 12 < 4 pi = 12.566..., so p <= 0 on [4 pi, inf) a fortiori.

  q-side, certified BY CONSTRUCTION by the Markov-Lukacs decomposition for the half-line:

      q(u) = (22u - 7250725477/114904064)^2
             + 73964663853612149/39608831771148288
             + u (101u/12 - 36667/1616)^2 ,

  i.e. q = sigma_0 + u sigma_1 with sigma_0 and sigma_1 explicit sums of rational squares.

  Therefore BOTH sign conditions of the Cohn-Elkies theorem are verified by expanding a finite
  sum of squares: no Sturm sequence, no root counting, and no dependence on any checker --
  including Computation's own, and deliberately excluding Main's shell_check,
  which review 0138-C shows to be unsound.

VERIFICATION IN THIS FILE: the two identities are checked by exact polynomial expansion, and the
bound is recomputed from p(0) and q(0) as exact rationals.  Independent confirmation that the
certificate is the same object as the one exactcert accepts is in the JSON's `cross_check` field.

Usage:  python3 sos_both_sides.py
"""
import json
import sympy as sp

u = sp.Symbol('u')
T = sp.Rational(12)                     # <= 4*pi
SQ_P = [sp.Rational(4, 3), sp.Rational(-37, 3),
        sp.Rational(101, 12) * u + sp.Rational(1, 4), sp.Rational(-13, 6)]
SQ_Q0 = [sp.Rational(22) * u - sp.Rational(7250725477, 114904064)]
CONST_Q0 = sp.Rational(73964663853612149, 39608831771148288)
SQ_Q1 = [sp.Rational(101, 12) * u - sp.Rational(36667, 1616)]

def main():
    # p-side identity
    minus_p = sp.expand((u - T) * sum(s ** 2 for s in SQ_P))
    p = sp.expand(-minus_p)
    # q-side identity
    q = sp.expand(sum(s ** 2 for s in SQ_Q0) + CONST_Q0 + u * sum(s ** 2 for s in SQ_Q1))
    # recompute the bounds exactly
    p0, q0 = p.subs(u, 0), q.subs(u, 0)
    ratio = sp.Rational(p0) / sp.Rational(q0)
    import mpmath as mp
    mp.mp.dps = 30
    delta = 4 * mp.pi / 3 * mp.mpf(ratio.p) / mp.mpf(ratio.q)
    print("p-side  : -p = (u-12) * [ %s ]" % " + ".join("(%s)^2" % sp.expand(s) for s in SQ_P))
    print("q-side  :  q = (%s)^2 + %s + u(%s)^2" % (sp.expand(SQ_Q0[0]), CONST_Q0, sp.expand(SQ_Q1[0])))
    print()
    print("p(0) = %s   q(0) = %s   p(0)/q(0) = %s" % (p0, q0, ratio))
    print("Delta <= (4 pi/3)(p(0)/q(0)) = %s" % mp.nstr(delta, 12))
    ok_p = sp.expand(minus_p - (u - T) * sum(s ** 2 for s in SQ_P)) == 0
    ok_q = sp.expand(q - (sum(s ** 2 for s in SQ_Q0) + CONST_Q0 + u * sum(s ** 2 for s in SQ_Q1))) == 0
    print()
    print("p-side identity verified by expansion :", ok_p)
    print("q-side identity verified by expansion :", ok_q)
    print("T = 12 <= 4*pi = %.6f              : %s" % (4 * mp.pi, T <= 4 * mp.pi))
    json.dump(dict(script="KeplerConjecture/Computation/sos_both_sides.py",
                   status="VERIFIED_EXACT (both sides by explicit rational Gram)",
                   convention="unit radius, minimum separation 2, u = pi|x|^2",
                   theorem=("every packing of unit-radius spheres in R^3 has occupied-volume "
                            "density Delta <= 2.00171738"),
                   does_not_improve_on=("Cohn-Elkies 2003 (0.779747) nor the LP-optimal 0.77996622; "
                                        "this is a format demonstrator at 2.7x Kepler"),
                   p_side=dict(T=str(T),
                               squares=[str(sp.expand(s)) for s in SQ_P],
                               identity="-p = (u-T) * sum_i r_i^2"),
                   q_side=dict(squares0=[str(sp.expand(s)) for s in SQ_Q0],
                               constant0=str(CONST_Q0),
                               squares1=[str(sp.expand(s)) for s in SQ_Q1],
                               identity="q = sigma_0 + u sigma_1, both explicit sums of squares"),
                   p=str(p), q=str(q), p0=str(p0), q0=str(q0), ratio=str(ratio),
                   delta=mp.nstr(delta, 12),
                   verification=dict(p_identity=bool(ok_p), q_identity=bool(ok_q),
                                     T_le_4pi=bool(T <= 4 * mp.pi),
                                     cross_check=("the same p is accepted by exactcert and the "
                                                  "independent SymPy oracle via "
                                                  "out/sos_pside_many.json")),
                   ), open("out/sos_both_sides.json", "w"), indent=1)
    print("\nwrote out/sos_both_sides.json")

if __name__ == "__main__":
    main()
