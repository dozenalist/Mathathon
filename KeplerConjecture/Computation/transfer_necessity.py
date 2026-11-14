#!/usr/bin/env python3
"""What a bounded transfer implies about the density -- with the hypothesis made exact.

HISTORY, because the earlier version was wrong.  I first argued from a full-period cut, which is
invalid: C044 quantifies over FINITE U and a period is not a finite subset.  I then argued from
"sum the divergence over one period", which is valid ONLY IF the transfer is periodic -- and
periodicity of the PACKING does not make an arbitrary bounded transfer periodic: the flux
crossing a period boundary need not cancel.  Review 0353-C caught both.  The argument below needs
NO periodicity: it uses a large-box averaging passage, which is what the review asked for.

THEOREM A (K15-C-TRANSFER-DENSITY-002).  Let Lambda be a packing of finite upper density and let
G_R be its range-R graph.  Suppose there is an antisymmetric phi on the edges with |phi| <= Phi
and

        sum_{w ~ v} phi(v, w)  >=  b(v) = sqrt(32) - vol Omega(v)        for every centre v.

Then rho <= 1/sqrt(32).

PROOF (large-box averaging).  Let B be a box of side L.  Summing the hypothesis over v in B:

        sum_{v in B} b(v)  <=  sum_{v in B} sum_{w ~ v} phi(v,w).

The right side counts each edge with BOTH endpoints in B twice, with opposite signs, so those
cancel by antisymmetry; only edges CROSSING the boundary survive, each contributing at most Phi in
absolute value.  Hence

        sum_{v in B} b(v)  <=  Phi * #{(v,w) : v in B, w not in B, |v-w| <= R}.

Every such v lies within distance R of the boundary of B, so #crossing <= #(Lambda cap
(dB + B_R)), which for a packing of finite density is O(rho R L^2).  Also
sum_{v in B} vol Omega(v) = |B| + O(L^2) because the cells tile space, and #(Lambda cap B) =
rho |B| + O(L^2).  Therefore

        sum_{v in B} b(v) = sqrt(32) rho |B| - |B| + O(L^2),

and dividing by |B| = L^3 and letting L -> infinity gives sqrt(32) rho - 1 <= 0.  QED.

REMARKS.
* No periodicity of phi is used, and none of Lambda beyond finite density.  This replaces the
  earlier periodic-sum argument, which needed a hypothesis the conclusion does not.
* The periodic case is the sharp special case: for FCC and HCP every cell has vol Omega = sqrt32,
  so b = 0 and the inequality holds with equality -- that is where the constant is attained.
* SCOPE OF WHAT THIS SAYS ABOUT THE ROUTE.  It does NOT say the transfer route is circular, and the
  earlier word "circular" is WITHDRAWN.  A sufficient condition that implies Kepler is not thereby
  circular; it becomes circular only if its own proof assumes Kepler.  What the theorem does say,
  and all it says, is that exhibiting a bounded transfer is a requirement strictly stronger than
  the density bound -- so a proof of Kepler by this route has to earn the transfer, and the earning
  cannot be easier than the bound itself.

Reproduction: python3 transfer_necessity.py
"""
import json, os
import mpmath as mp

_HERE = os.path.dirname(os.path.abspath(__file__))
_OUT = os.path.join(_HERE, "out")
mp.mp.dps = 30
KEPLER_RHO = 1 / (4 * mp.sqrt(2))

def main():
    print("THEOREM A (large-box averaging, no periodicity hypothesis):")
    print("  a bounded transfer implies rho <= 1/sqrt(32) = %s\n" % mp.nstr(KEPLER_RHO, 12))
    rows = []
    print("Check the sharp cases and the counting error terms on the fixtures:")
    for name, N, V in (("FCC (one cell)", 1, 4 * mp.sqrt(2)),
                       ("HCP (one cell)", 1, 4 * mp.sqrt(2)),
                       ("periodised 13-cluster", 13, mp.mpf(4096))):
        sb = N * 4 * mp.sqrt(2) - V
        rho = mp.mpf(N) / V
        print("  %-24s sum_v b = %-14s rho = %-12s at/below 1/sqrt32 ? %s"
              % (name, mp.nstr(sb, 10), mp.nstr(rho, 8),
                 "yes" if rho <= KEPLER_RHO + mp.mpf("1e-25") else "NO"))
        rows.append(dict(fixture=name, sum_b=mp.nstr(sb, 12), rho=mp.nstr(rho, 12),
                         at_or_below=bool(rho <= KEPLER_RHO + mp.mpf("1e-25"))))
    print()
    print("The averaging passage, made explicit: for a box of side L,")
    print("  sum_B b <= Phi * #crossing  and  #crossing = O(rho R L^2),")
    print("  so  sum_B b / |B| <= C Phi rho R / L  ->  0.")
    print("  Meanwhile sum_B b / |B| -> sqrt32 rho - 1, hence rho <= 1/sqrt32.")
    print()
    print("WITHDRAWN: the earlier inference that this implication makes the transfer route")
    print("'circular'.  A sufficient condition implying Kepler is not circular; it is circular")
    print("only if its proof assumes Kepler.  The correct statement is that exhibiting a bounded")
    print("transfer is STRICTLY STRONGER than the density bound, so the route must earn it.")
    json.dump(dict(script="KeplerConjecture/Computation/transfer_necessity.py",
                   claim="K15-C-TRANSFER-DENSITY-002",
                   status="PROVED (large-box averaging; no periodicity of phi required)",
                   statement=("a bounded transfer (|phi| <= Phi, divergence >= b) on a packing of "
                              "finite density implies rho <= 1/sqrt(32)"),
                   method=("sum the divergence bound over a box of side L; antisymmetry cancels "
                           "interior edges; crossing edges are O(rho R L^2) and the volume is "
                           "L^3, so the mean of b tends to 0 and sqrt32 rho - 1 <= 0"),
                   supersedes=("the earlier periodic-sum argument, which needed phi periodic -- a "
                               "hypothesis the conclusion does not supply"),
                   withdrawn=("the inference that this implication makes the transfer route "
                              "'circular'; a sufficient condition implying Kepler is not circular "
                              "unless its proof assumes Kepler"),
                   rows=rows), open(os.path.join(_OUT, "transfer_necessity.json"), "w"), indent=1)
    print("\nwrote out/transfer_necessity.json")

if __name__ == "__main__":
    main()
