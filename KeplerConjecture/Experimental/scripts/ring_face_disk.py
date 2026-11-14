#!/usr/bin/env python3
"""
Lemma (disk in the face, whole offset path).  Closes Main's G17 / C136 obligation
independently, and states the hypothesis it rests on.

Setting.  The payer cell has five ring faces at distance R on the path R in [1, b],
b = rho_r/2 = 1.0514622242, with common normal n_r (unit).  Every competing face is
{y.n_j <= d_j} with d_j >= 1 and angle theta_j = angle(n_r, n_j).

Statement.  For every R in [1,b], the ring face F_R = { y.n_r = R } cap {y.n_j <= d_j} contains
the disk of in-plane radius

    t_R = min_j (d_j - R cos theta_j) / sin theta_j ,

and on the admissible family  min_{R in [1,b]} t_R  >=  t* = rho_r/4 = 0.5257311121 .
Hence A_ring >= pi t*^2 = 0.868314853691 on the whole path, which is what the ring-excess
lemma needs.  Equality is attained at rho = 2, R = b: the margin is ZERO, so the hypothesis
"angle >= 58.28252559 deg and distance >= 1 jointly" is load bearing and cannot be weakened.

Proof of the per-face bound.  Write n_j = cos(theta_j) n_r + sin(theta_j) m_j with m_j a unit
vector perpendicular to n_r.  For a unit in-plane direction e and t >= 0 put y = R n_r + t e.
Then  y.n_j = R cos(theta_j) + t sin(theta_j) (e.m_j) <= R cos(theta_j) + t sin(theta_j),
because |e.m_j| <= 1.  So y.n_j <= d_j whenever t <= (d_j - R cos theta_j)/sin theta_j.  []

Proof that the minimum is >= t*.  Three kinds of competing plane.
  * the other four ring faces: d_j = R, theta_j = 72 deg, so t_R = R(1-cos72)/sin72 = 0.7265 R
    >= 0.7265 > t*;
  * the axial face (the centre c): d_j = 1, theta_j = 180 - 58.2825 = 121.7175 deg, so
    t_R = (1 - R cos 121.7175)/sin 121.7175 = (1 + 0.5257 R)/0.8507, INCREASING in R, hence
    >= its value at R = 1, which is 1.793 > t*;
  * a free centre at distance rho: d_j = rho/2 and cos theta_j <= (rho^2 + rho_r^2 - 4)/(2 rho rho_r)
    by 2-separation from the ring centre.  Here theta_j <= 90 deg, so t_R is DECREASING in R and
    its minimum is at R = b.  The remaining one-variable minimum over rho in [2, 2.603447] is
    evaluated below.

Run: python3 Experimental/scripts/ring_face_disk.py
"""
import sys
from fractions import Fraction as F

import numpy as np

RHO_R = 2.1029244484765344
B = RHO_R / 2
TSTAR = RHO_R / 4
ALPHA_AXIAL = 180.0 - np.degrees(np.arccos(RHO_R / 4))     # 121.7175 deg


def reach(d, theta_deg):
    """(d - R cos theta)/sin theta at R -- callers pass d already divided by R where needed."""
    t = np.radians(theta_deg)
    return (d - 0.0 * np.cos(t)) if abs(np.sin(t)) < 1e-15 else (d - B * np.cos(t)) / np.sin(t)


def main():
    print("=" * 78)
    print("DISK IN THE RING FACE, WHOLE PATH  (Main G17 / C136)")
    print(f"  rho_r = {RHO_R:.12f}   b = {B:.12f}   t* = rho_r/4 = {TSTAR:.12f}")
    print(f"  pi t*^2 = {np.pi*TSTAR**2:.12f}")
    ok = True

    # --- ring-ring: d_j = R, theta = 72 deg -> t_R = R(1-cos72)/sin72, min at R = 1
    tr = 1.0 * (1 - np.cos(np.radians(72))) / np.sin(np.radians(72))
    print(f"\n  other four ring faces : t_R = R(1-cos72)/sin72, min at R=1 -> {tr:.9f}"
          f"   {'PASS' if tr >= TSTAR else 'FAIL'}")
    ok &= tr >= TSTAR

    # --- axial face: d = 1, theta = 121.7175 deg, INCREASING in R -> min at R = 1
    ca = np.cos(np.radians(ALPHA_AXIAL)); sa = np.sin(np.radians(ALPHA_AXIAL))
    vals = [(1.0 - R * ca) / sa for R in np.linspace(1.0, B, 2001)]
    print(f"  axial face (c)        : theta = {ALPHA_AXIAL:.6f} deg, increasing in R, "
          f"min at R=1 -> {min(vals):.9f}   {'PASS' if min(vals) >= TSTAR else 'FAIL'}")
    ok &= min(vals) >= TSTAR

    # --- free centres: (d, theta) = (rho/2, alpha(rho)), DECREASING in R -> worst at R = b
    best = (1e9, None)
    for rho in np.linspace(2.0, 2.603447, 6001):
        c = (rho ** 2 + RHO_R ** 2 - 4) / (2 * rho * RHO_R)
        th = np.degrees(np.arccos(min(1.0, c)))
        t = np.radians(th)
        if np.sin(t) < 1e-15:
            continue
        val = (rho / 2 - B * np.cos(t)) / np.sin(t)
        if val < best[0]:
            best = (val, rho)
    print(f"  free centres          : (d,theta) = (rho/2, alpha(rho)), decreasing in R, "
          f"worst at R=b")
    print(f"                          min over rho in [2, 2.603447] = {best[0]:.9f} "
          f"at rho = {best[1]:.6f}   {'PASS' if best[0] >= TSTAR - 1e-12 else 'FAIL'}")
    ok &= best[0] >= TSTAR - 1e-12

    worst = min(tr, min(vals), best[0])
    print(f"\n  min over every competing plane and every R in [1,b]: {worst:.12f}")
    print(f"  t*                                                  : {TSTAR:.12f}")
    print(f"  margin = {worst - TSTAR:+.3e}   (ZERO at rho=2, R=b -- the hypothesis is tight)")
    print(f"\n  A_ring >= pi t*^2 = {np.pi*TSTAR**2:.12f} on the whole path: {ok}")
    print("=" * 78)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
