#!/usr/bin/env python3
"""A sufficient condition for a cut violation, from ball counting alone.

The question this answers: can we exhibit a packing on which C044 provably FAILS, without
constructing one?  Yes -- not by building a dense packing, but by bounding how tightly any packing
can be covered.

LEMMA HD1 (cell inside the covering ball).  Call a packing R-SATURATED if every point of space is
within R of some centre.  Then for every centre v,
        Omega(v)  <=  B(v, R)      and therefore     vol Omega(v) <= (4 pi/3) R^3,
because x in Omega(v) implies |x-v| <= dist(x, Lambda) <= R.

COROLLARY HD2 (deficit floor).  b(v) = sqrt(32) - vol Omega(v)  >=  sqrt(32) - (4 pi/3) R^3
=: b_min(R).  Since a centre has at most 12 neighbours at distance <= 2 (Schuette-van der Waerden),
the singleton cut {v} violates C044 at capacity Phi as soon as

        b_min(R)  >  Phi * deg(v),      and deg(v) <= 12 suffices:   b_min(R) > 12 Phi.

So every R-saturated packing with

        R  <=  R_Phi  :=  ( (sqrt(32) - 12 Phi) * 3/(4 pi) )^(1/3)

FAILS the cut condition at capacity Phi -- at every finite U containing such a v, a fortiori.
The formula is monotone and only meaningful while sqrt(32) - 12 Phi > 0, i.e. Phi < sqrt(32)/12.

COROLLARY HD3 (failure at EVERY finite capacity, no kissing number needed).  If Lambda is
R-saturated with R < R_0 = lambda^(1/3) = 1.105339..., then b(v) >= b_min(R) > 0 at EVERY vertex.
For a box B of side L the finite set U = Lambda cap B therefore has

        sum_U b  >=  b_min(R) * #(Lambda cap B)  =  b_min(R) * rho * L^3,

while the cut side is |delta^+_R(U)| = O(rho R L^2).  The ratio grows like L, so

        sum_U b / |delta^+_R(U)|  ->  infinity,

and the cut condition fails at EVERY finite capacity Phi.  HD2 needs the kissing number to bound
deg(v); HD3 does not, because it uses a box instead of a singleton and lets L grow.  The price is
that it is asymptotic: it says some finite U violates, not which one.

WHAT THIS IS AND IS NOT.
* It is a *negative* result about capacities: no packing that is R-saturated with R <= R_Phi can
  be Phi-admissible.  It constructs no packing, and it does not prove Kepler.
* It is a statement about the covering radius, so it constrains only packings that are tightly
  covered.  FCC has covering radius sqrt2 = 1.41421 > R_0, so it is not caught -- correctly, since
  FCC has b = 0 and satisfies C044 at every Phi.
* The bound is a floor, not the truth: b_min(R) uses only the covering radius, so it is far below
  the actual deficit of any particular packing (the 13-cluster has b_central = 0.1066 against
  b_min(12.327) << 0).

THE RECORDED FORM, AND WHY IT IS NOT REPRODUCED HERE.  My plan carried this lemma as
        "1 - kappa(r) s^3 <= b / vol B_1".
Normalising HD1 by vol B_1 = 4 pi/3 gives the exact version
        b / vol B_1  >=  lambda - R^3,        lambda = sqrt(32)/(4 pi/3) = 1.3504736...
i.e. with R = 1 + s (the covering radius measured as one ball radius plus an excess),
        b / vol B_1  >=  lambda - (1+s)^3.
There is no rearrangement of this into "1 - kappa s^3" with lambda = 1: the constant is lambda =
1.3505, not 1.  So the form I recorded was not right, and the exact inequality above replaces it.

Reproduction: python3 highdensity_cut.py
"""
import mpmath as mp
F = mp.mpf

mp.mp.dps = 30
VOL_B1 = 4 * mp.pi / 3
LAMBDA = mp.sqrt(32) / VOL_B1          # 1.3504736...

def b_min(R):
    """Deficit floor for an R-saturated packing (LEMMA HD1)."""
    return mp.sqrt(32) - VOL_B1 * mp.mpf(R) ** 3

def R_Phi(Phi):
    """Largest covering radius that still forces a violation at capacity Phi (COROLLARY HD2)."""
    Phi = mp.mpf(Phi)
    num = mp.sqrt(32) - 12 * Phi
    if num <= 0:
        return None
    return (num * 3 / (4 * mp.pi)) ** (mp.mpf(1) / 3)

def self_test():
    ok = True
    def check(name, cond, info=None):
        nonlocal ok
        ok = ok and bool(cond)
        print("  %s %s%s" % ("PASS" if cond else "FAIL", name,
                             "" if info is None else "  %s" % (info,)))

    print("HD1/HD2: the covering-radius threshold")
    check("b_min(1) = sqrt32 - 4pi/3 = lambda - 1 > 0", b_min(1) > 0,
          mp.nstr(b_min(1), 10))
    check("b_min(2) < 0 (a ball of radius 2 around a centre is bigger than sqrt32)",
          b_min(2) < 0, mp.nstr(b_min(2), 10))
    check("the crossover is at R = lambda^(1/3) = %.6f" % float(LAMBDA ** (mp.mpf(1) / 3)),
          abs(b_min(LAMBDA ** (mp.mpf(1) / 3))) < mp.mpf("1e-20"))
    check("R_0 (Phi = 0) equals that crossover", abs(R_Phi(0) - LAMBDA ** (mp.mpf(1) / 3)) < mp.mpf("1e-25"))
    check("R_Phi is decreasing in Phi", R_Phi("0.001") > R_Phi("0.01") > R_Phi("0.05"))
    check("R_Phi is undefined past Phi = sqrt32/12 = %.6f" % float(mp.sqrt(32) / 12),
          R_Phi(mp.sqrt(32) / 12) is None)
    check("FCC's covering radius sqrt2 = 1.41421 exceeds R_0, so FCC is not caught",
          mp.sqrt(2) > R_Phi(0))
    check("HD3: b_min(R) > 0 exactly when R < R_0", b_min(R_Phi(0)) > 0 and b_min(R_Phi(0)) < mp.mpf("1e-25"))
    check("HD3: b_min(1.10) > 0 > b_min(1.11), so the sign changes at R_0",
          b_min("1.10") > 0 and b_min("1.11") < 0, (float(b_min("1.10")), float(b_min("1.11"))))
    # with |delta^+| <= C rho R L^2 and C = 8 (a crude but explicit boundary constant), the cut
    # fails once L > Phi C R / b_min: a finite threshold for every finite Phi, growing linearly.
    b110 = b_min("1.10")
    Ls = {Phi: float(F(Phi) * 8 * mp.mpf("1.10") / b110) for Phi in (1, 10, 10 ** 6)}
    print("     HD3: L needed to force a violation at R = 1.10 (C = 8): " +
          ", ".join("Phi=%s -> L > %.0f" % (k, v) for k, v in Ls.items()))
    check("HD3: that threshold is finite and grows linearly in Phi",
          Ls[10 ** 6] > 1000 * Ls[1] * 0.9, (Ls[1], Ls[10 ** 6]))
    print()
    print("  capacity Phi        R_Phi (max covering radius forcing a violation)")
    rows = []
    for Phi in ("0", "0.001", "0.008880268414739", "0.01", "0.05", "0.1", "0.4"):
        r = R_Phi(Phi)
        print("  %-16s    %s" % (Phi, "n/a (Phi >= sqrt32/12)" if r is None else mp.nstr(r, 10)))
        rows.append((Phi, None if r is None else mp.nstr(r, 12)))
    print()
    print("  Reading: any packing covered by balls of radius <= %.4f fails C044 at Phi = 0,"
          % float(R_Phi(0)))
    print("  and tightening Phi barely moves the threshold (%.4f -> %.4f from Phi = 0 to 0.05):"
          % (float(R_Phi(0)), float(R_Phi("0.05"))))
    print("  the constraint is on the covering radius, not on the capacity.")
    print()
    print("highdensity_cut self-test:", "PASS" if ok else "FAIL")
    return ok, rows

if __name__ == "__main__":
    ok, _ = self_test()
    raise SystemExit(0 if ok else 1)
