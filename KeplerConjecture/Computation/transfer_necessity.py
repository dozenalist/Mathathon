#!/usr/bin/env python3
"""What a bounded transfer implies about the density -- with the hypothesis made exact.

HISTORY, because the earlier version was wrong.  I first argued from a full-period cut, which is
invalid: C044 quantifies over FINITE U and a period is not a finite subset.  I then argued from
"sum the divergence over one period", which is valid ONLY IF the transfer is periodic -- and
periodicity of the PACKING does not make an arbitrary bounded transfer periodic: the flux
crossing a period boundary need not cancel.  Review 0353-C caught both.  The argument below needs
NO periodicity: it uses a large-box averaging passage, which is what the review asked for.

LEMMA S (saturation = bounded cells).  For a packing, "every point of space is within D of some
centre" and "diam Omega(v) <= D for every v" are equivalent.
  Proof.  If x in Omega(v) then |x-v| <= dist(x, Lambda) <= D.  Conversely every x lies in some cell
  Omega(v), and then |x-v| <= diam Omega(v) <= D.  QED.

THEOREM A (K15-C-TRANSFER-DENSITY-002).  Let Lambda be a packing of finite upper density that is
D-SATURATED for some D < infinity (equivalently, by LEMMA S, whose Voronoi cells have uniformly
bounded diameter).  Let G_R be its range-R graph.  Suppose there is an antisymmetric phi on the
edges with |phi| <= Phi and

        sum_{w ~ v} phi(v, w)  >=  b(v) = sqrt(32) - vol Omega(v)        for every centre v.

Then rho <= 1/sqrt(32).

LEMMA B (cell-volume bookkeeping).  If Lambda is D-saturated, then for every box B of side L,

        |B| - O_D(L^2)  <=  sum_{v in Lambda cap B} vol Omega(v)  <=  |B| + O_D(L^2).

  Proof.  Let U* be the union of the cells of the centres in Lambda cap B.  For x in Omega(v) with
  v in B, LEMMA S gives |x-v| <= D, so U* is contained in B grown by D, whence
  |U*| <= (L+2D)^3 = L^3 + O_D(L^2).  Conversely let x in B with dist(x, dB) > D.  Some centre w
  satisfies |x-w| <= D, and then |x-w| <= D < dist(x, dB) forces w in B, so x in U*.  Hence
  |U*| >= (L-2D)^3 = L^3 - O_D(L^2).  QED.

PROOF OF THEOREM A (large-box averaging).  Sum the hypothesis over the centres v in B:

        sum_{v in B} b(v)  <=  sum_{v in B} sum_{w ~ v} phi(v,w).

The right side counts every edge with BOTH endpoints in B twice, with opposite signs, so those
cancel by antisymmetry; only edges CROSSING the boundary survive, each contributing at most Phi in
absolute value.  Hence

        sum_{v in B} b(v)  <=  Phi * #{(v,w) : v in B, w not in B, |v-w| <= R}.

Every such v lies within distance R of the boundary of B, so #crossing <= #(Lambda cap
(dB + B_R)) = O(rho R L^2) for a packing of finite upper density.  With LEMMA B and
#(Lambda cap B) = rho |B| + O(L^2),

        sum_{v in B} b(v) = sqrt(32) rho |B| - |B| + O_D(L^2),

and dividing by |B| = L^3 and letting L -> infinity (along a sequence of boxes realizing the upper
density) gives sqrt(32) rho - 1 <= 0.  QED.

COROLLARY 1 (K15-C-CUTIMPLIES-003).  Suppose Lambda is D-saturated and satisfies only C044's CUT
condition -- sum_{v in U} b(v) <= Phi |delta^+_R(U)| for every FINITE U -- for one finite capacity
Phi.  Then rho <= 1/sqrt(32).  Proof: U = Lambda cap B is finite, so the same computation applies
verbatim; no transfer on the infinite graph and no compactness argument is needed.

  This is the valid replacement for the WITHDRAWN full-period derivation: no period is used, only
  boxes, and a box intersected with Lambda IS finite -- which is what C044 quantifies over.  It also
  locates the real content of C044: since any finite Phi suffices, the criterion is not about the
  SIZE of Phi but about whether a finite Phi can be exhibited at all.

COROLLARY 2 (contrapositive, scope stated).  A D-saturated packing with rho > 1/sqrt(32) admits no
bounded transfer at any Phi and violates some finite cut.  For a packing that is NOT D-saturated
this theorem gives nothing -- see the remark below.

REMARKS.
* No periodicity of phi is used.  This replaces the earlier periodic-sum argument, which needed a
  hypothesis the conclusion does not supply.
* WHY THE SATURATION HYPOTHESIS IS NOT DECORATION.  The identity
  sum_{v in Lambda cap B} vol Omega(v) = |B| + O(L^2) does NOT follow from "the cells tile space".
  Take FCC in a half-space, empty above it: for a box in the void, Lambda cap B is empty, so the sum
  is 0 while |B| = L^3.  The cells of an unbounded void have unbounded diameter, which is exactly
  what D-saturation excludes.  So finite upper density ALONE is not enough for this proof; whether
  the theorem holds without LEMMA B is left open here.
* The hypothesis is cheap in the cases that matter: saturating a packing only increases its density,
  and a saturated packing has D = 2, so every packing that would violate Kepler has a saturated
  relative to which the theorem applies.  It does NOT apply to the sparse period-16 13-cluster of
  cut_flow.py (cells of diameter >= 12.3), and it does not need to: there rho = 0.0032 and the
  analysis is a REFUTATION of a capacity, not a density bound.
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

def sampled_saturation_constant(centres, L, n=40):
    """Largest sampled distance from a point of the period cube to the nearest centre.

    A LOWER bound on the true D-saturation constant (we sample, so the max can only miss),
    which is the direction that matters: a large value certifies that a D-small saturation
    hypothesis FAILS.  TESTED_FINITE arithmetic.
    """
    best = 0.0
    for i in range(n):
        for j in range(n):
            for k in range(n):
                x = (L * (i + 0.5) / n, L * (j + 0.5) / n, L * (k + 0.5) / n)
                d = min(sum((x[t] - c[t]) ** 2 for t in range(3)) ** 0.5 for c in centres)
                best = max(best, d)
    return best

def main():
    print("THEOREM A (large-box averaging, no periodicity hypothesis):")
    print("  a D-saturated packing with a bounded transfer has rho <= 1/sqrt(32) = %s\n"
          % mp.nstr(KEPLER_RHO, 12))
    print("  Hypotheses actually used: finite upper density, and D-SATURATION (LEMMA S:")
    print("  every point within D of a centre, equivalently diam Omega(v) <= D).  LEMMA B")
    print("  supplies |U*| = |B| + O_D(L^2); finite density alone does NOT (remark 2).\n")
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
    print("  Meanwhile LEMMA B gives sum_B b / |B| -> sqrt32 rho - 1, hence rho <= 1/sqrt32.")
    print()
    print("The D in the hypothesis, measured (sampled lower bound on the true constant):")
    # FCC with minimum separation 2 = sqrt2 * {(i,j,k) in Z^3 : i+j+k even};
    # conventional cubic cell side 2 sqrt2, four centres per cell.
    r2 = float(mp.sqrt(2))
    rng = range(-1, 4)
    fcc = [tuple(r2 * t for t in (i, j, k))
           for i in rng for j in rng for k in rng if (i + j + k) % 2 == 0]
    D_fcc = sampled_saturation_constant(fcc, 2 * r2, n=12)
    print("  FCC at separation 2: sampled D >= %.6f   (covering radius is sqrt2 = %.6f)" %
          (D_fcc, float(mp.sqrt(2))))
    print("     => D = 2 suffices for the dense case, so the hypothesis is cheap there.")
    print("  period-16 13-cluster: D >= 12.327 (cut_flow.py V4), so the hypothesis FAILS;")
    print("     the theorem deliberately says nothing about that sparse fixture.")
    print()
    print("COROLLARY 1 (K15-C-CUTIMPLIES-003): the same computation with U = Lambda cap B, which")
    print("  is FINITE, shows the CUT condition alone -- for one finite capacity Phi -- forces")
    print("  rho <= 1/sqrt(32).  No transfer, no compactness, no period.  This is the valid")
    print("  replacement for the withdrawn full-period derivation.")
    print()
    print("WITHDRAWN: the earlier inference that this implication makes the transfer route")
    print("'circular'.  A sufficient condition implying Kepler is not circular; it is circular")
    print("only if its proof assumes Kepler.  The correct statement is that exhibiting a bounded")
    print("transfer is STRICTLY STRONGER than the density bound, so the route must earn it.")
    json.dump(dict(script="KeplerConjecture/Computation/transfer_necessity.py",
                   claim="K15-C-TRANSFER-DENSITY-002",
                   status="PROVED (large-box averaging; no periodicity of phi required)",
                   statement=("a bounded transfer (|phi| <= Phi, divergence >= b) on a packing of "
                              "finite upper density that is D-saturated for some finite D "
                              "implies rho <= 1/sqrt(32)"),
                   hypotheses=["finite upper density",
                               "D-saturation: every point of space within D of a centre "
                               "(equivalent to diam Omega(v) <= D; LEMMA S)"],
                   lemma_B=("D-saturation gives |U*| = |B| + O_D(L^2): cells of centres in B lie in "
                            "B grown by D, and every point of B at distance > D from the boundary "
                            "lies in a cell of a centre in B"),
                   why_saturation_is_needed=("sum_{v in Lambda cap B} vol Omega(v) = |B| + O(L^2) "
                                             "does NOT follow from the cells tiling space: FCC in a "
                                             "half-space has empty intersection with a box in the "
                                             "void, so the sum is 0 while |B| = L^3"),
                   corollary_1="K15-C-CUTIMPLIES-003: the finite-U cut condition alone, at any "
                               "finite Phi, forces rho <= 1/sqrt(32) (take U = Lambda cap B)",
                   corollary_2="a D-saturated packing with rho > 1/sqrt(32) admits no bounded "
                               "transfer and violates some finite cut",
                   does_not_apply_to=("packings that are not D-saturated, e.g. the period-16 "
                                      "13-cluster (cells of diameter >= 12.3); there the cut/flow "
                                      "work is a refutation of a capacity, not a density bound"),
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
