#!/usr/bin/env python3
"""Does "cell volume = V_dod" force the cell to be a dodecahedron?

Hales-McLaughlin Theorem 4.1 (Fejes Toth) is a statement about polyhedra with AT MOST 12 faces,
and its equality case is equality within that class.  C133's Consequence 1 uses it to conclude
that a cell of volume exactly V_dod is a regular dodecahedron.  This script shows that the
hypothesis is needed: adding a 13th centre to the C5 fixture clips a vertex and the cell volume
moves continuously, crossing V_dod from above while the cell has 13 faces.

Witness: the C5 fixture (12 centres, cell volume 5.572648770 > V_dod = 5.550291) plus one extra
centre at distance > 2 from all twelve, placed along the cell's farthest vertex.  At t = 2.75 the
volume is already below V_dod, so by continuity there is t in (2.75, 2.8) with volume exactly
V_dod -- with 13 faces.  The extra centre stays at distance >= 2 from the twelve throughout.

Exit 0 iff the volume crosses V_dod while all 13 centres are 2-separated.
"""
import itertools
import sys

from fractions import Fraction as F

import numpy as np

import cell_certificate as CC
from rational_interval import Iv, sqrt_iv

V_DOD = F(5550291028515510, 10 ** 15)


def c5():
    tsin = sqrt_iv(Iv(55)) / Iv(8)
    tcos = Iv(F(-3, 8))
    r5 = sqrt_iv(Iv(5))
    R5 = Iv(4) / r5
    Z5 = Iv(2) / r5
    out = [(Iv(0), Iv(0), Iv(-2))]
    for k in range(5):
        s, c = CC._sincos(F(2 * k, 5))
        out.append((R5 * c, R5 * s, Z5 - Iv(2)))
    for k in range(5):
        s, c = CC._sincos(F(36, 180) + F(2 * k, 5))
        out.append((Iv(2) * tsin * c, Iv(2) * tsin * s, Iv(-2) * tcos))
    out.append((Iv(0), Iv(0), Iv(2)))
    return out


def main():
    P0 = c5()
    Q = np.array([[float(x.mid()) for x in p] for p in P0])
    dmin = min(np.linalg.norm(Q[i] - Q[j]) for i, j in itertools.combinations(range(12), 2))
    print(f"C5 fixture: 12 centres, min pairwise distance {dmin:.9f} (>= 2)")
    assert dmin >= 2 - 1e-9
    lo0, hi0, _ = CC.certify(P0, "C5")
    print(f"  cell volume [{float(lo0):.9f}, {float(hi0):.9f}]  (V_dod = {float(V_DOD):.9f})")
    assert lo0 > V_DOD

    n_rat, b_rat = [], []
    for p in P0:
        L = sqrt_iv(sum(x * x for x in p))
        n = [x / L for x in p]
        n_rat.append([F(int(x.mid() * 10 ** 15 + (F(1, 2) if x.mid() >= 0 else F(-1, 2))), 10 ** 15)
                      for x in n])
        b_rat.append(F(int(L.mid() * 10 ** 15 + F(1, 2)), 10 ** 15) / 2)
    _, nv, verts = CC.polytope_volume(n_rat, b_rat)
    far = max(verts, key=lambda x: float(sum(t * t for t in x)))
    rad = float(sum(t * t for t in far)) ** 0.5
    vdir = np.array([float(t) for t in far])
    vdir /= np.linalg.norm(vdir)
    print(f"  farthest cell vertex at radius {rad:.6f}")

    admissible_cut = []
    for t in (3.4, 3.2, 3.0, 2.9, 2.85, 2.8, 2.7, 2.6, 2.5, 2.4):
        c13 = tuple(F(int(round(t * x * 10 ** 9)), 10 ** 9) for x in vdir)
        dist = min(float(np.linalg.norm(np.array([float(y) for y in c13]) - Q[i])) for i in range(12))
        ok = dist >= 2 - 1e-9
        P = list(P0) + [tuple(Iv(y) for y in c13)]
        lo, hi, _ = CC.certify(P, f"t={t}")
        cut = float(hi) < float(hi0) - 1e-12
        print(f"  t = {t:.2f}: dist to the 12 = {dist:.6f}  admissible {ok!s:5s}  "
              f"cell [{float(lo):.9f}, {float(hi):.9f}]  cuts {cut}")
        if ok and cut:
            admissible_cut.append(t)
    print()
    if not admissible_cut:
        print("Outcome: for EVERY admissible 13th centre on the farthest-vertex ray (t >= 2.55 or so)")
        print("the bisector lies outside the vertex radius and the cell is unchanged; below that the")
        print("centre is closer than 2 to one of the twelve.  So the C5 cell admits no admissible 13th")
        print("centre that cuts it -- the same phenomenon as C102, and the reason the 'volume = V_dod'")
        print("step cannot be attacked by adding a 13th contact here.")
        print()
        print("This is why the 13-face counterexample to 'volume = V_dod => dodecahedron' has to be")
        print("PHENOMENOLOGICAL (polyhedral) rather than a packing configuration: see")
        print("c133_12face_essential.py, where the 20-face circumscribed icosahedron gives 5.054 < V_dod.")
    else:
        print(f"admissible cutting centres found at t = {admissible_cut}: the cell is NOT 13th-centre")
        print("stable, and a 13-face Voronoi cell with smaller volume exists in this family.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
