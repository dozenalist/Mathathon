#!/usr/bin/env python3
"""
Cross-check the certified enclosure against an independent floating-point computation,
at parameters that are NOT the controls.

The controls of rigorous_cell_volume.py are fixed configurations (fcc, hcp, the C5 fixture).
This script samples the C5 family at random (theta, phi), computes the certified enclosure,
and compares its midpoint with the value from the entirely separate float code path in
c5_fixture.py (numpy + scipy ConvexHull).

The comparison is |midpoint - float| < 1e-12, not containment: the float value carries its
own ~1e-15 error, which exceeds the enclosure's 1e-18 width, so demanding containment would
fail for a reason that has nothing to do with either computation.  (The first version of this
check did demand containment and "failed" on a case whose values agreed to 12 digits.)

Run:  python3 Experimental/scripts/volume_crosscheck.py [n_trials] [seed]
"""
import sys
from fractions import Fraction as F

import numpy as np

import rigorous_cell_volume as R
from c5_fixture import cell_of, C, W1, RING, SOUTH


def certified(theta_deg, phi_deg):
    t = F(theta_deg).limit_denominator(10 ** 9) / 180
    p = F(phi_deg).limit_denominator(10 ** 9) / 180
    s, c = R._sincos(t)
    r5 = R.sqrt_iv(R.Iv(5))
    R5 = R.Iv(4) / r5
    Z5 = R.Iv(2) / r5
    P = [(R.Iv(0), R.Iv(0), R.Iv(-2))]
    for k in range(5):
        sk, ck = R._sincos(F(2 * k, 5))
        P.append((R5 * ck, R5 * sk, Z5 - R.Iv(2)))
    for k in range(5):
        sk, ck = R._sincos(p + F(2 * k, 5))
        P.append((R.Iv(2) * s * ck, R.Iv(2) * s * sk, R.Iv(-2) * c))
    P.append((R.Iv(0), R.Iv(0), R.Iv(2)))
    return R.sandwich(P, F(3, 2))[:2]


def floating(theta_deg, phi_deg):
    ths, thc = np.sin(np.radians(theta_deg)), np.cos(np.radians(theta_deg))
    pts = [C] + RING + [W1 + 2 * np.array([ths * np.cos(np.radians(phi_deg + 72 * k)),
                                           ths * np.sin(np.radians(phi_deg + 72 * k)),
                                           -thc]) for k in range(5)] + [SOUTH]
    return cell_of(W1, pts)[1]


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 2026
    rng = np.random.default_rng(seed)
    bad = 0
    print("cross-check: certified midpoint vs independent float hull volume (tolerance 1e-12)")
    for _ in range(n):
        th, ph = float(rng.uniform(107, 119)), float(rng.uniform(23, 35))
        a, b = certified(th, ph)
        vf = floating(th, ph)
        mid = float((a + b) / 2)
        agree = abs(mid - vf) < 1e-12
        bad += 0 if agree else 1
        print(f"  theta={th:7.3f} phi={ph:7.3f}  certified {mid:.12f}  float {vf:.12f}"
              f"  |diff| {abs(mid - vf):.1e}  agree={agree}")
    print(f"  disagreements beyond 1e-12: {bad}/{n}")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
