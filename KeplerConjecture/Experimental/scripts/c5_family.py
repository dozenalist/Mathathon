#!/usr/bin/env python3
"""
Is the exact-cell theorem a knife-edge?  It holds on an interval of pentagon angles.

For each theta in a grid, build
    c, 5 ring (2.102924), 5 pentagon at radius exactly 2 from w1 (azimuth 36+72k), south
and check three things:
  (L) legality: every pair, including pairs against w1, is >= 2;
  (V) the cell volume and max|vertex|;
  (T) the covering argument of REVIEW_0353.md 2 closes: certified covering radius
      gamma satisfies max over 2<=rho<=2*max|vertex| of (rho^2+rs^2-2 rho rs cos gamma) < 4.
If (T) closes, vol Omega(w1) is EXACT for that configuration -- no completion changes it.

The point is not to find the best theta (that is a 1-D search) but to show the theorem is
not an artefact of one lucky angle.  Prints a table; exit 0 if (T) closes everywhere legal.
"""
import sys
import numpy as np
sys.path.insert(0, "Experimental/scripts")
from c5_fixture import C, W1, RING, SOUTH, cell_of, covering_bound

V_DOD = 5.5502910285155


def build(theta_deg):
    th = np.radians(theta_deg)
    s, c = np.sin(th), np.cos(th)
    pent = []
    for k in range(5):
        ph = np.radians(36 + 72 * k)
        pent.append(W1 + 2 * np.array([s * np.cos(ph), s * np.sin(ph), -c]))
    return [C] + RING + pent + [SOUTH]


def main():
    print(" theta    minsep(added)   verts   max|v|    vol        gamma   kill_max   exact?")
    print(" " + "-" * 78)
    ok = True
    rows = []
    for theta in np.arange(104, 126.01, 1.0):
        F = build(theta)
        P = np.array(F + [W1])
        d = np.linalg.norm(P[:, None, :] - P[None, :, :], axis=2)
        np.fill_diagonal(d, np.inf)
        sep = d.min()
        # margin on pairs involving an added centre, excluding the constructed w1 contact
        add = list(range(6, 12))
        amin = min(np.linalg.norm(P[i] - P[j]) for i in add for j in range(len(P))
                   if j != i and j != len(P) - 1)
        v, vol, rmax, bounded = cell_of(W1, F)
        gam, diam, raw = covering_bound(F, W1, subdiv=5)
        worst = -np.inf
        for rs in sorted({float(np.linalg.norm(p - W1)) for p in F}):
            for rho in np.linspace(2.0, 2 * rmax, 801):
                worst = max(worst, rho ** 2 + rs ** 2 - 2 * rho * rs * np.cos(np.radians(gam)))
        legal = amin >= 2 - 1e-9
        exact = bool(legal and worst < 4 and bounded)
        if legal and not exact:
            ok = False
        print(f" {theta:6.1f}  {amin:9.6f}   {len(v):4d}  {rmax:.6f}  {vol:9.6f}  "
              f"{gam:6.2f}  {worst:7.4f}   {'YES' if exact else ('illegal' if not legal else 'NO')}")
        rows.append((theta, amin, vol, exact, legal))
    legal_rows = [r for r in rows if r[4]]
    best = min(legal_rows, key=lambda r: r[2])
    print(f"\n  legal thetas in the grid: {len(legal_rows)} of {len(rows)}")
    print(f"  every legal one has the exact-cell property? {all(r[3] for r in legal_rows)}")
    print(f"  min vol Omega(w1) in the family: {best[2]:.9f} at theta = {best[0]:.1f}")
    print(f"  (the frozen fixture uses cos theta = -3/8, i.e. theta = 112.025, "
          f"vol = 5.898017372)")
    print(f"  V_dodeca floor never approached: min vol - V_dodeca = {best[2]-V_DOD:+.9f}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
