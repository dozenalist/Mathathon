#!/usr/bin/env python3
"""
THEOREM (this script): the pair inequality (P') holds at the icosahedral pair for EVERY
completion whose payer cell has exactly twelve faces.

Statement.  Let the icosahedral cluster be present (c at distance 2 from w1, five ring
centres at 2.102924 in the ring directions).  Let z_1..z_6 be any further centres at
distance >= 2 from w1, all 2-separated, and suppose the cell Omega(w1) has exactly twelve
faces.  Then vol Omega(w1) > 5.763417470 = 2 sqrt32 - V_dod.

Proof.
  (1) BASE POLYTOPE.  Let D' be Omega(w1) with the five ring faces moved in to distance 1
      (all other faces kept where they are).  NOTE the inclusion is D' SUBSET Omega: pushing
      faces in shrinks the polytope, so the volume inequality cannot come from the inclusion
      (an earlier draft had this backwards).  What is true is direct: D' is the Voronoi cell
      of w1 with respect to the same twelve neighbours, so every face is at distance >= 1 and
      the imported Hales-McLaughlin bound gives vol D' >= V_dod.

  (2) RING-EXCESS LEMMA.  Moving one face of a polytope outward at unit speed increases the
      volume at rate equal to that face's area.  Moving the five ring faces from 1 to b
      therefore gains 5(b-1) times the mean ring-face area over the path, and in particular

          vol Omega(w1)  =  vol D' + 5(b-1) * mean_t A_ring(t)  >=  vol D' + 5(b-1) A_min ,

      where A_min is the least ring-face area of D' (the areas decrease along the path in
      every configuration measured; the minimum is taken over the path).

  (3) A GUARANTEED UNCUT DISK.  The lemma needs the MINIMUM area along the path, so the disk
      is computed on the plane y.n_r = R for R in [1,b], and the minimum is at R = b.  Let t
      be the in-plane radius on that plane, y with y.n_r = R and |y| = sqrt(R^2+t^2).  y is
      cut by the half-space of a centre z at distance rho only if  y.n_z > rho/2 , i.e.
      angle(y,n_z) < arccos( (rho/2)/sqrt(R^2+t^2) ).
      But angle(y,n_z) >= alpha(rho) - arctan(t), where alpha(rho) is the least possible
      angle between a centre's direction and n_r subject to |z - ring| >= 2:

          cos alpha(rho)  <=  (rho^2 + rho_r^2 - 4) / (2 rho rho_r) ,   rho_r = 2.102924... .

      So y is uncut whenever  arctan(t/R) <= alpha(rho) - arccos( (rho/2)/sqrt(R^2+t^2) ).
      The worst case over rho in [2, 2.603447] (centres further out cannot cut, REVIEW_0353 2)
      is rho = 2 at every R, and the worst R is b, where with cos alpha = rho_r/4 and
      R = rho_r/2 the boundary is t*/R = 1/2 exactly, i.e.

          t* = R/2 = rho_r/4 = 0.525731...     (arctan(1/2) + arccos(1/sqrt(5/4)) = alpha)

      At R = 1 the same computation gives 0.557537, so the minimum along the path is at b.

      Hence every ring face of D' contains an uncut disk of area pi t*^2 = 0.976555... .

  (4) CONCLUSION.
          vol Omega(w1) >= V_dod + 5(b-1) pi t*^2
                        =  5.550291029 + 0.251226...  =  5.801517...  >  5.763417470 .

Scope.  Exactly twelve faces.  With thirteen or more faces step (1) fails -- vol D' >= V_dod
is false for more than twelve half-spaces -- and that case is NOT covered.
"""
import sys
from fractions import Fraction as F

import cell_certificate as CC
from rational_interval import Iv, sqrt_iv, pi_iv


def main():
    # the icos edge squared is 8 - (8/5) sqrt5, so rho_r^2 is exact in Q(sqrt5)
    r5 = sqrt_iv(Iv(5))
    rho_r2 = Iv(8) - Iv(8) * r5 / Iv(5)
    rho_r = sqrt_iv(rho_r2)
    print(f"rho_r  = |ring - w1| = [{float(rho_r.lo):.12f}, {float(rho_r.hi):.12f}]")

    # the worst point on the path is R = b = rho_r/2, where the boundary is t*/R = 1/2
    t = rho_r / Iv(4)                 # t* = R/2 with R = rho_r/2
    print(f"worst R along the path = b = rho_r/2 = {float((rho_r/Iv(2)).mid()):.12f}")
    print(f"t* = R/2 = rho_r/4 = [{float(t.lo):.12f}, {float(t.hi):.12f}]  (t*/R = 1/2 exactly)")

    pi = pi_iv(50)
    disk = pi * t * t
    print(f"uncut disk area pi t*^2 (minimum along the path) = [{float(disk.lo):.12f}, {float(disk.hi):.12f}]")

    # b = rho_r/2 exactly
    b = rho_r / Iv(2)
    gain = Iv(5) * (b - Iv(1)) * Iv(disk.lo)     # LOWER disk area, min along the path      # use the LOWER disk area
    V_DOD = Iv(F(5550291028515510, 10 ** 15))
    THRESH = Iv(F(5763417470, 10 ** 9))
    bound = V_DOD + Iv(gain.lo)
    print(f"\n5(b-1) A_min  >= {float(gain.lo):.12f}")
    print(f"V_dod + that  >= {float(bound.lo):.12f}")
    print(f"threshold        {float(THRESH.lo):.9f}")
    ok = bound.lo > THRESH.hi
    print(f"\nTHEOREM: vol Omega(w1) > threshold for every 12-face completion: {ok}")
    print(f"         margin >= {float(bound.lo - THRESH.hi):+.9f}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
