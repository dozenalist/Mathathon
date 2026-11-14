"""Completeness of m5's 6^ell ray grid: every generic ray geometry is a grid instance.

Claim (used by the INDUCTION LEMMA): let theta_j be ARBITRARY real ray angles and let
e_i = e + i*pi/3 (i = 0..5) be a generic R-orbit direction, so that no e_i is
perpendicular to any v_j (theta_j).  Then the sign matrix SIG[i][j] = sign(e_i . v_j)
is one of the 6^ell matrices enumerated by cells c_j in {0..5}, namely the one with
c_j = the integer of the cell of t_j = (theta_j - theta_e)/(pi/3).

Reason (exact): g(x) = cos(pi x/3) vanishes iff x = 1.5 + 3n, i.e. x in Z + 1.5 mod 6,
and for i in Z/6 the values (t_j - i) hit those zeros exactly when t_j in Z + 0.5 mod 6
(the six numbers i + 1.5 mod 6 are 1.5, 2.5, ..., 6.5).  So on each cell (c+0.5, c+1.5)
the whole sign vector is constant and equals the vector at the integer c+1.

This script checks the claim with exact rational arithmetic on random instances.
Run:  python3 signcells.py
"""
import random
from fractions import Fraction
import math

COS_TABLE = {0: 1, 1: 1, 2: -1, 3: -1, 4: -1, 5: 1}   # sign cos(m pi/3), re-derived below


def sign_cos_pi3(x):
    """Exact sign of cos(pi*x/3) for a rational x given as Fraction, or 0."""
    # reduce x mod 6 into [0,6)
    y = x % 6
    # zeros at 1.5, 4.5
    if y == Fraction(3, 2) or y == Fraction(9, 2):
        return 0
    # cos(pi y/3) > 0  <=>  y < 1.5 or y > 4.5  (within [0,6))
    return 1 if (y < Fraction(3, 2) or y > Fraction(9, 2)) else -1


def grid_sign(m):
    return COS_TABLE[m % 6]


def main():
    # consistency of the two sign routines on integers
    for m in range(12):
        assert sign_cos_pi3(Fraction(m)) == grid_sign(m), m
    rng = random.Random(20240513)
    bad = 0
    trials = 20000
    for _ in range(trials):
        ell = rng.choice([3, 4, 5, 6])
        # arbitrary real ray angles, as rationals with a fine denominator
        thetas = [Fraction(rng.randrange(0, 6 * 10 ** 6), 10 ** 6) for _ in range(ell)]
        theta_e = Fraction(rng.randrange(0, 6 * 10 ** 6), 10 ** 6)
        # genericity: no e_i perpendicular to v_j  <=>  t_j not in Z + 1/2 (mod 6)
        ts = [(thetas[j] - theta_e) % 6 for j in range(ell)]
        if any((t * 2).denominator == 1 for t in ts):
            continue                      # a zero occurred: e is not generic, skip
        # actual sign matrix from the paper's definition sign(e_i . v_j)
        actual = [[sign_cos_pi3(t - i) for t in ts] for i in range(6)]
        # grid instance claimed to represent it: c_j = floor(t_j - 1/2)
        cells = [int(math.floor(t - Fraction(1, 2))) for t in ts]
        grid = [[grid_sign(cells[j] + 1 - i) for j in range(ell)] for i in range(6)]
        if actual != grid:
            bad += 1
            print("MISMATCH", ts, cells, actual, grid)
        # the cell (c+0.5, c+1.5) is a full interval of equal sign matrix: perturb each
        # ray by less than its distance to the cell boundary
        for _ in range(2):
            ts2 = []
            ok = True
            for t, c in zip(ts, cells):
                lo, hi = Fraction(2 * c + 1, 2), Fraction(2 * c + 3, 2)
                margin = min(t - lo, hi - t)
                if margin == 0:
                    ok = False
                    break
                step = margin * Fraction(rng.randrange(1, 90), 100)
                sgn = 1 if rng.randrange(2) else -1
                ts2.append((t + sgn * step) % 6)
            if not ok:
                continue
            if any((t * 2).denominator == 1 for t in ts2):
                continue
            if [[sign_cos_pi3(t - i) for t in ts2] for i in range(6)] != actual:
                bad += 1
                print("CELL NOT CONSTANT", ts, ts2)
    print(f"{trials} random (ell, ray angles) trials, mismatches {bad}")
    assert bad == 0
    print("SIGN-CELL COMPLETENESS OK")


if __name__ == "__main__":
    main()
