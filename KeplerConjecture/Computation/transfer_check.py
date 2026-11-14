#!/usr/bin/env python3
"""Numerical sanity check of K15-C035 (transfer => negligibility), exactly.

Statement under test.  Let Lambda be 2-separated, phi antisymmetric with
phi(v,w) = 0 when |v-w| > R and |phi| <= Phi, and A(v) = sum_w phi(v,w).  Then
    sum_{v in Lambda cap B(x,r)} A(v)  <=  3 Phi (R+1)^5 r^2      for all r >= 1.
The bound is proved; this script checks it on a concrete packing (fcc) with a
random rational antisymmetric transfer, over a range of radii.  It is a test of
the *arithmetic* of the constant, not a substitute for the proof.

Usage: python3 transfer_check.py [--R 2] [--seed 0]
"""
import argparse, itertools, random, sys
from fractions import Fraction as F
import numpy as np


def fcc_points(r):
    """fcc lattice at minimum separation 2: all integer/near-integer combinations."""
    pts = []
    for i in range(-r, r + 1):
        for j in range(-r, r + 1):
            for k in range(-r, r + 1):
                # fcc = {(a,b,c) : a+b+c even} with basis of length sqrt2 scaled by sqrt2
                if (i + j + k) % 2 == 0:
                    pts.append(np.array([i * np.sqrt(2) / 1.0,
                                         j * np.sqrt(2) / 1.0,
                                         k * np.sqrt(2) / 1.0]))
    return pts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--R", type=float, default=2.0)
    ap.add_argument("--Phi", type=float, default=1.0)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--rmax", type=float, default=6.0)
    args = ap.parse_args()
    R, Phi = args.R, args.Phi
    rng = random.Random(args.seed)
    box = int(np.ceil(max(args.rmax, R))) + 2
    pts = fcc_points(box)
    # note: this parametrisation gives separations sqrt(2)*sqrt(2)=2 for fcc? check:
    idx = {}
    for n, p in enumerate(pts):
        idx[tuple(np.round(p, 12))] = n
    # neighbours within R, computed in chunks (vectorised)
    P = np.array(pts)
    nbr = {}
    CH = 256
    for start in range(0, len(P), CH):
        block = P[start:start + CH]
        d = np.linalg.norm(block[:, None, :] - P[None, :, :], axis=2)
        for n_local in range(block.shape[0]):
            n = start + n_local
            nbr[n] = [m for m in np.nonzero(d[n_local] <= R + 1e-12)[0] if m != n]
    # random antisymmetric transfer, |phi| <= Phi
    phi = {}
    for n, lst in nbr.items():
        for m in lst:
            if (m, n) in phi:
                phi[(n, m)] = -phi[(m, n)]
            else:
                phi[(n, m)] = F(rng.randint(-4, 4), 4) * F(int(Phi * 4), 4)
    A = {n: sum(phi[(n, m)] for m in nbr[n]) for n in range(len(pts))}
    print("R =", R, " Phi =", Phi, " |Lambda| =", len(pts))
    print("max |A(v)| =", max(abs(float(a)) for a in A.values()),
          " bound Phi*k_R =", Phi * ((R + 1) ** 3 - 1))
    ok = True
    for r in (1.0, 2.0, 3.0, 4.0, 5.0, 6.0):
        S = sum(a for n, a in A.items()
                if np.linalg.norm(pts[n]) <= r + 1e-12)
        bound = 3 * Phi * (R + 1) ** 5 * r ** 2
        good = float(S) <= bound + 1e-9
        ok = ok and good
        print("  r = %.1f : sum A = %+.6f   bound 3*Phi*(R+1)^5*r^2 = %.6f   %s"
              % (r, float(S), bound, "OK" if good else "VIOLATED"))
    print("\nRESULT:", "bound holds on this instance" if ok else "BOUND VIOLATED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
