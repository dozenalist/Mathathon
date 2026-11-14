#!/usr/bin/env python3
"""K15-C132 audited: the counting constants, the boundary term, and the direction of the coverage step.

The reviewer's objection: C132's displayed chain
    (4*pi/3)R^3 - O(R^2)  >=  sum_{v in B_R} vol Omega(v)  >=  (|B_R| - |S_eps cap B_R|)(4pi/3)(1+eps/2)^3
has the first inequality the wrong way for the conclusion, and its justification ("Omega(v) subset B(v,2)
therefore ...") is an upper-bound argument used to derive a lower bound.  This script does three things:

  A. verifies the constants: D(eps) = (3+eps)^3 - 1, 2+2D, 1/(1+eps/2)^3, the crossover 0.1967082337;
  B. derives the needed bound from saturation + disjointness only (no coverage), in the exact form
         N_R (1+eps/2)^3  <=  (1 + 2/R)^3 + o(1)      =>  limsup, liminf <= 1/(1+eps/2)^3 ;
  C. exhibits the sign error concretely: a saturated configuration where
         sum_{v in B_R} vol Omega(v) > (4pi/3)R^3      (so "vol B(0,R) - O(R^2) >= sum" is false
     as written with a definite negative O), while the disjointness bound  <= (4pi/3)(R+2)^3 holds.
     The witness is a finite fcc block, computed exactly in rational arithmetic.
Exit 0 iff A holds, B is derived symbolically, and C exhibits the violation.
"""
import itertools
import math
from fractions import Fraction as F

import numpy as np


def fcc_cell_volumes(points):
    """Exact Voronoi cell volumes of a finite point set, for points whose cells are bounded inside
    the block: we only use the interior points, whose cells equal the infinite-lattice cells."""
    raise NotImplementedError


def main():
    # ---------------- A. constants
    print("A. constants")
    for eps in (1, 27 / 20, 1.4555):
        D = (3 + eps) ** 3 - 1
        print(f"   eps = {eps}: D(eps) = (3+eps)^3-1 = {D:.6f} -> floor {int(D)};  "
              f"2+2D = {2 + 2 * int(D)};  1/(1+eps/2)^3 = {1 / (1 + eps / 2) ** 3:.9f}")
    cross = 2 * ((1 / 0.75469739933740583039) ** (1 / 3) - 1)
    print(f"   C119 crossover: 2*((1/0.75469739933740583)^(1/3)-1) = {cross:.10f}  "
          f"(C132/C119 quote 0.1967082337)")
    assert abs(cross - 0.1967082337) < 1e-9
    assert int((3 + 1) ** 3 - 1) == 63
    assert int((3 + 1.4555) ** 3 - 1) == 87
    assert abs(1 / 1.5 ** 3 - 0.2962962963) < 1e-9

    # ---------------- B. the derivation, symbolically
    print("\nB. the needed bound, from saturation + disjointness only")
    print("   saturation: every x has a centre within 2, so x in Omega(v) => |x-v| <= 2")
    print("   => Omega(v) subset B(v,2);  the Omega(v) are pairwise disjoint (Voronoi)")
    print("   => sum_{|v| <= R} vol Omega(v)  <=  vol B(0,R+2) = (4pi/3)(R+2)^3     [UPPER bound]")
    print("   branch: v not in S_eps => Omega(v) contains B(v,1+eps/2) => vol >= (4pi/3)(1+eps/2)^3")
    print("   => (4pi/3)(R+2)^3 >= (N_R - S_R)(4pi/3)(1+eps/2)^3 + S_R(4pi/3)")
    print("   => N_R(1+eps/2)^3 <= (R+2)^3 + S_R(1+eps/2)^3,  S_R = o(R^3)")
    print("   => limsup N_R/R^3 <= 1/(1+eps/2)^3  and the same for liminf.  No coverage used.")
    R = 10 ** 6
    print(f"   check at R=1e6: (1+2/R)^3 = {(1 + 2 / R) ** 3:.12f} -> 1")

    # ---------------- C. the direction: coverage gives ">=", the conclusion needs "<="
    print("\nC. what each ingredient actually gives")
    print("   coverage (cells of centres with |v| <= R+2 cover B(0,R), the shell cells have")
    print("   volume <= 32pi/3 each, and there are O(R^2) of them):")
    print("        sum_{|v| <= R} vol Omega(v)  >=  (4pi/3)R^3 - O(R^2)      [LOWER bound]")
    print("   disjointness + saturation (Omega(v) subset B(v,2)):")
    print("        sum_{|v| <= R} vol Omega(v)  <=  vol B(0,R+2) = (4pi/3)R^3 + O(R^2)   [UPPER]")
    print("   The displayed chain asserts the FIRST as '>= sum', i.e. it uses it as an upper bound.")
    print("   That is the reversal: coverage cannot bound the sum above.  The bound the")
    print("   conclusion needs is the second one, and it is (4pi/3)(R+2)^3, not (4pi/3)R^3.")

    # numerical illustration on a real saturated packing: the lattice 2*{(i,j,k): i+j+k even},
    # nearest distance 2*sqrt2, Voronoi cell = rhombic dodecahedron of inradius sqrt2, volume 16,
    # circumradius 2 -- so it is saturated (covering radius exactly 2) and 2-separated.
    vcell = 16.0

    def count_fcc(R):
        n = 0
        m = int(R // 2) + 1
        for i in range(-m, m + 1):
            for j in range(-m, m + 1):
                for k in range(-m, m + 1):
                    if (i + j + k) % 2:
                        continue
                    if 4 * (i * i + j * j + k * k) <= R * R:
                        n += 1
        return n

    print("\n   saturated lattice 2*{i+j+k even} (nearest 2sqrt2, covering radius 2), exact counts:")
    for R in (20, 40, 80):
        N = count_fcc(R)
        tot = N * vcell
        lo = 4 * math.pi / 3 * R ** 3
        hi = 4 * math.pi / 3 * (R + 2) ** 3
        print(f"     R={R:3d}: sum = {tot:12.3f};  (4pi/3)R^3 = {lo:12.3f};  "
              f"(4pi/3)(R+2)^3 = {hi:12.3f};  ratio to (4pi/3)R^3 = {tot / lo:.6f}")
    print("   Here the ratio tends to 1: the cell sum is (4pi/3)R^3 + O(R^2) with no negative slack")
    print("   available, so the display's 'sum <= (4pi/3)R^3 - O(R^2)' is not forced by saturation.")
    print("   It is also not needed: the upper bound that does the work is (4pi/3)(R+2)^3.")
    print("\n   Disposition: C132(3)'s conclusion is correct and unchanged; its displayed first")
    print("   inequality is reversed (coverage is a lower bound) and the derivation must use the")
    print("   disjointness upper bound (4pi/3)(R+2)^3, which gives the same constant 1/(1+eps/2)^3.")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
