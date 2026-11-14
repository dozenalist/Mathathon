#!/usr/bin/env python3
"""The transfer route PRESUPPOSES the density bound it is meant to prove.

This is the correct, proved version of a claim I previously made from a full-period cut
(which was invalid, because C044's criterion quantifies over FINITE U and a period is not a
finite subset -- see REVIEW_0308.md section 2).  The argument below goes through the TRANSFER
side instead, where it is elementary and rigorous.

THEOREM (K15-C-TRANSFER-DENSITY-001).  Let Lambda be a periodic packing, period lattice with
N centres per fundamental domain and volume V, centre density rho = N/V.  Suppose a transfer
exists: an antisymmetric phi on the range-R graph with |phi| <= Phi and

        sum_w phi(v,w) >= b(v) = sqrt(32) - vol Omega(v)      for every centre v.

Then  rho <= 1/sqrt(32),  i.e. the density is at most the Kepler density.

PROOF.  Phi is periodic (the packing and the cell complex are), so summing the inequality over
the N centres of one fundamental domain gives

        sum_v sum_w phi(v,w)  >=  sum_v b(v) = N*sqrt(32) - V .

The left side is a sum over ordered pairs of centres, and by antisymmetry phi(w,v) = -phi(v,w)
each unordered pair contributes zero -- this includes pairs whose members lie in different
copies of the domain, since periodicity identifies them consistently.  Hence the left side is
exactly 0 and N*sqrt(32) <= V, i.e. rho = N/V <= 1/sqrt(32) = 0.176776695...  QED.

CONSEQUENCE.  For any packing with rho > 1/sqrt(32) -- i.e. any packing that would violate
Kepler -- NO transfer exists at any capacity Phi.  So the transfer/Hoffman route of C035/C044
cannot be used to *establish* the bound for the packings that matter: it applies only where the
conclusion already holds.  The route is therefore circular as a proof of the density bound, and
its real content is confined to C035's negligibility bookkeeping (which is genuine but is not
the geometry).

WHAT THIS DOES NOT SAY.  It does not say the cut INEQUALITIES are false or vacuous, nor that
individual finite cuts are uninformative -- a violating cut is still a genuine obstruction
(REVIEW_0308.md section 1).  It says the existence of a transfer is a strictly stronger
requirement than the density bound.

Reproduction: python3 transfer_necessity.py
"""
import json, os
import mpmath as mp

_HERE = os.path.dirname(os.path.abspath(__file__))
_OUT = os.path.join(_HERE, "out")
mp.mp.dps = 30

def main():
    print("THEOREM: a transfer requires rho <= 1/sqrt(32) = %s" % mp.nstr(1 / (4 * mp.sqrt(2)), 12))
    print()
    print("Check the identity sum_v b(v) = N*sqrt32 - V on the fixtures:")
    rows = []
    # FCC and HCP: every cell is sqrt32, so sum b = 0 exactly and the condition is rho <= 1/sqrt32
    # with rho = 1/sqrt32 -- EQUALITY, as expected for the extremal packings.
    for name, N, V in (("FCC (period 1 cell)", 1, 4 * mp.sqrt(2)),
                       ("HCP (period 1 cell)", 1, 4 * mp.sqrt(2)),
                       ("periodised 13-cluster", 13, mp.mpf(4096))):
        sb = N * 4 * mp.sqrt(2) - V
        rho = mp.mpf(N) / V
        print("  %-24s N=%-3d V=%-12s sum_v b = %-14s rho = %-12s rho <= 1/sqrt32 ? %s"
              % (name, N, mp.nstr(V, 10), mp.nstr(sb, 10), mp.nstr(rho, 8),
                 "yes" if rho <= 1 / (4 * mp.sqrt(2)) + mp.mpf("1e-25") else "NO"))
        rows.append(dict(fixture=name, N=N, V=mp.nstr(V, 12), sum_b=mp.nstr(sb, 12),
                         rho=mp.nstr(rho, 12),
                         density_ok=bool(rho <= 1 / (4 * mp.sqrt(2)) + mp.mpf("1e-25"))))
    print()
    print("Reading:")
    print("  * FCC and HCP sit exactly AT the boundary: sum_v b = 0, so the transfer condition is")
    print("    satisfied with equality and the theorem is sharp there.")
    print("  * The icosahedral cluster has sum_v b = %.2f < 0 and rho = %.6f << 1/sqrt32,"
          % (-4022.46, 0.003174))
    print("    so a transfer CAN exist for it -- consistent with cut_flow.py finding a flow.")
    print("  * Any packing with rho > 1/sqrt(32) has sum_v b > 0 and therefore NO transfer at any")
    print("    Phi.  That is exactly the packings the route would need to rule out.")
    json.dump(dict(script="KeplerConjecture/Computation/transfer_necessity.py",
                   claim="K15-C-TRANSFER-DENSITY-001",
                   status="PROVED (elementary)",
                   statement=("a periodic transfer implies rho <= 1/sqrt(32); hence no transfer "
                              "exists for any packing that violates the Kepler bound"),
                   consequence=("the transfer/Hoffman route cannot establish the density bound "
                                "for the packings that matter: it applies only where the "
                                "conclusion already holds"),
                   not_claimed=("that finite cuts are uninformative; a violating cut remains a "
                                "genuine obstruction"),
                   rows=rows), open(os.path.join(_OUT, "transfer_necessity.json"), "w"), indent=1)
    print("\nwrote out/transfer_necessity.json")

if __name__ == "__main__":
    main()
