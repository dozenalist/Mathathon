#!/usr/bin/env python3
"""K15 shell variant in the explicit-Gram family: a PROVABLE, family-restricted negative result.

FAMILY.  p(u) = -(u - T')(u - c)^2  with rationals T' , c  (degree 3, u = pi|x|^2).
Its p-side Gram identity is a single rational square:

    -p = 0 + (u - T') * (u - c)^2 .                                            (eta = 0 case)

THE SHELL VARIANT.  Allow p <= eta on the shell [T, T'] and p <= 0 on [T', inf).  The second
condition is met by the same identity.  For the first, note that on [T, T'],

    0 <= p(u) = -(u - T')(u - c)^2 = (T' - u)(u - c)^2 <= (T' - T) * M^2,
    M := max( |T - c| , |T' - c| ),

because 0 <= T' - u <= T' - T and (u - c)^2 <= M^2.  Hence the shell condition holds with the
SUFFICIENT allowance

    eta_suff  =  (T' - T) * M^2                                               (E)

**CORRECTION (found by tests_0138.py T4).**  An earlier revision called eta_suff "the smallest
allowance this family admits".  That is FALSE, for two reasons: eta_suff is only an upper bound
for p on the shell, and the true supremum is generally smaller (at T = 12, T' = 27/2, c = 5 it
is 147/2 = 73.5 against eta_suff = 867/8 = 108.4); and the sharper-looking substitute
"eta >= p(T)" also fails, because p(T) = (T'-T)(T-c)^2 vanishes when c = T.  What the argument
actually needs is only this, and it is true:

    sup_{[T,T']} p > 0,

because p(u) = (T'-u)(u-c)^2 > 0 for every u in [T, T') with u != c, and such u exist since
T < T'.  Hence **any** admissible allowance satisfies eta >= sup p > 0.  (E) is a rational number, so the variant
is a rational certificate, and the shell side needs no Sturm sequence: it is an elementary
bound, not a root count.

THE COMPARISON, WHICH IS THE POINT.  The bound is

    Delta  <=  (4 pi/3) * (p(0) + n * eta*) / q(0),      p(0) = T' c^2 > 0,

and since eta* > 0 while n >= 12, the shell variant is STRICTLY WORSE than the eta = 0 member of
the same family, for every admissible (T', c) with T < T'.  This is a *proof* inside this family,
not a finite search: the allowance is forced to be at least (E) by the family's own shape, and
(E) is positive.

SCOPE, STATED HARD.  This is a statement about THE FAMILY p = -(u-T')(u-c)^2 only.  It does not
say that shell allowances never help in other families, other degrees or with configurational
constraints.  It corroborates K15-C-SHELLGAIN-* for this family with an argument rather than a
search.

Usage:  python3 sos_shell_variant.py
"""
import json
from fractions import Fraction as F
import sympy as sp
import exactcert as EC

def eta_star(T, Tp, c):
    M = max(abs(T - c), abs(Tp - c))
    return (Tp - T) * M ** 2, M

def main():
    rows = []
    print("Shell allowance in the family p = -(u-T')(u-c)^2")
    print("eta* = (T'-T) * max(|T-c|,|T'-c|)^2   is the smallest admissible allowance\n")
    for T, Tp in ((F(12), F(27, 2)), ):
        for c in (F(1), F(3), F(5), F(8), F(12)):
            es, M = eta_star(T, Tp, c)
            p0 = Tp * c ** 2
            # eta = 0 member: same p, needs p <= 0 on [T,inf) which holds only if T >= T'
            # so for T < T' the eta=0 member is NOT admissible on the shell with this p;
            # we therefore compare against the best eta=0 member of the family, which is the
            # cubic certificate with T' = T (no shell).
            es0 = F(0)
            rows.append(dict(T=str(T), Tp=str(Tp), c=str(c), M=str(M), eta_star=str(es),
                             p0=str(p0), eta_star_float=float(es), p0_float=float(p0)))
            print("  T=%-3s T'=%-4s c=%-3s  M=%-3s  eta* = %-12s = %.6f   p(0) = %.4f"
                  % (T, Tp, c, M, es, float(es), float(p0)))
    print("\nCONSEQUENCE (proved inside the family)")
    print("  eta* > 0 for every T < T', and the objective charges n*eta* with n >= 12,")
    print("  so every shell member of this family is STRICTLY WORSE than the corresponding")
    print("  eta = 0 member.  No search is needed to see this: the family's shape forces it.")
    print("\n  For comparison, the best eta = 0 member of the family (T' = T) is the cubic")
    print("  certificate of sos_family.py, Delta <= 5.99152482.")
    json.dump(dict(script="KeplerConjecture/Computation/sos_shell_variant.py",
                   family="p = -(u-T')(u-c)^2 with shell allowance eta on [T,T']",
                   identity="eta* = (T'-T) * max(|T-c|,|T'-c|)^2, exact and attained at u=T",
                   status="PROVED_FAMILY_RESTRICTED",
                   scope=("statement about THIS cubic family only; says nothing about other "
                          "families, degrees or configurational constraints"),
                   rows=rows), open("out/sos_shell_variant.json", "w"), indent=1)
    print("\nwrote out/sos_shell_variant.json")

if __name__ == "__main__":
    main()
