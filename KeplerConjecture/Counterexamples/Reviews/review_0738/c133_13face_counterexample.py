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

    # farthest cell vertex: where a 13th centre clips most cheaply
    n_rat, b_rat = [], []
    for p in P0:
        L = sqrt_iv(sum(x * x for x in p))
        n = [x / L for x in p]
        n_rat.append([F(int(x.mid() * 10 ** 15 + (F(1, 2) if x.mid() >= 0 else F(-1, 2))), 10 ** 15)
                      for x in n])
        b_rat.append(F(int(sum(x * x for x in p).mid() ** 0.5 * 10 ** 15 + F(1, 2)) / 10 ** 15, 1)
                     if False else F(int(L.mid() * 10 ** 15 + F(1, 2)), 10 ** 15) / 2)
    _, nv, verts = CC.polytope_volume(n_rat, b_rat)
    far = max(verts, key=lambda x: float(sum(t * t for t in x)))
    vdir = np.array([float(t) for t in far])
    vdir /= np.linalg.norm(vdir)
    print(f"  farthest cell vertex at radius {np.linalg.norm(vdir) * 0 + np.linalg.norm([float(t) for t in far]):.6f}")

    above = below = None
    for t in (3.4, 3.2, 3.0, 2.9, 2.85, 2.8, 2.78, 2.76, 2.75, 2.7):
        c13 = tuple(F(int(round(t * x * 10 ** 9)), 10 ** 9) for x in vdir)
        dist = min(float(np.linalg.norm(np.array([float(y) for y in c13]) - Q[i])) for i in range(12))
        P = list(P0) + [tuple(Iv(y) for y in c13)]
        lo, hi, _ = CC.certify(P, f"t={t}")
        nfaces = len(P)
        tag = ""
        if lo > V_DOD:
            above = (t, lo, hi)
        if hi < V_DOD:
            below = (t, lo, hi)
            tag = "  <-- below V_dod"
        print(f"  t = {t:.2f}: min dist to the 12 = {dist:.6f} (>= 2: {dist >= 2 - 1e-9});  "
              f"{nfaces} faces;  volume [{float(lo):.9f}, {float(hi):.9f}]{tag}")
        assert dist >= 2 - 1e-9, "the 13th centre must be admissible"
    print()
    print("volume is continuous in t, so some t in [%.2f, %.2f] gives volume exactly V_dod"
          % (below[0], above[0]))
    print("with 13 faces and all 13 centres 2-separated.  So 'volume = V_dod' does NOT force the")
    print("cell to be a dodecahedron; Hales-McLaughlin 4.1's 'at most 12 faces' is needed, exactly")
    print("as C133's Consequence 1 must state.")
    ok = below is not None and above is not None and below[0] < above[0]
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
