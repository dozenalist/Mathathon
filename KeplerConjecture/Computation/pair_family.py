#!/usr/bin/env python3
"""K15-C109 -- a compressed SYMMETRIC pair family, a test of (L).

E's search is one-sided: a dodecahedral v and the best payer w.  This tests a different
family -- configurations symmetric under x -> 2-x, so both cells are congruent and the pair
sum is 2*vol.  If any member has pair sum < 2*sqrt(32) = 11.3137085 then (L) is FALSE (the
qualitative (L_delta) survives, since it is proved).

A point at distance 2 from BOTH centres lies on the circle x = 1, radius sqrt(3); n such
points form a ring, mutually 2*sqrt(3)*sin(pi/n) apart, which is >= 2 only for n <= 5.
Antipodes (-2,0,0) and (4,0,0) are at distance 2 from v and w respectively.
"""
import itertools
import sys
import numpy as np
from scipy.spatial import ConvexHull

SQ32 = np.sqrt(32.0)
TWO_SQ32 = 2 * SQ32
V_DOD = 5.550291028515510


def vol_cell(centre, pts, tol=1e-9):
    ns = []
    for c in pts:
        d = np.asarray(c, float) - np.asarray(centre, float)
        r2 = d @ d
        if r2 < 1e-18:
            continue
        ns.append(2.0 * d / r2)
    if not ns:
        return np.inf
    ns = np.array(ns)
    V = []
    for i, j, k in itertools.combinations(range(len(ns)), 3):
        M = ns[[i, j, k]]
        try:
            p = np.linalg.solve(M, np.ones(3))
        except np.linalg.LinAlgError:
            continue
        if np.all(ns @ p <= 1.0 + tol):
            V.append(p)
    if len(V) < 4:
        return np.inf
    V = np.array(V)
    _, idx = np.unique(np.round(V, 9), axis=0, return_index=True)
    V = V[np.sort(idx)]
    if len(V) < 4:
        return np.inf
    return ConvexHull(V).volume


def min_sep(P):
    P = np.array(P, float)
    D = np.linalg.norm(P[:, None] - P[None], axis=2)
    np.fill_diagonal(D, np.inf)
    return float(D.min())


def ring(x, r, n, phase=0.0):
    return [(x, r * np.cos(2 * np.pi * k / n + phase), r * np.sin(2 * np.pi * k / n + phase))
            for k in range(n)]


def build(nring=5, phase=0.0, caps=True, cap_rings=0, cap_phase=0.0):
    P = [(0.0, 0.0, 0.0), (2.0, 0.0, 0.0)]
    if nring:
        P += ring(1.0, np.sqrt(3.0), nring, phase)
    if caps:
        P += [(-2.0, 0.0, 0.0), (4.0, 0.0, 0.0)]
    if cap_rings:
        P += ring(-2.0, np.sqrt(3.0), cap_rings, cap_phase)
        P += ring(4.0, np.sqrt(3.0), cap_rings, cap_phase)
    return P


def evaluate(P, label):
    ms = min_sep(P)
    if ms < 2.0 - 1e-9:
        print(f"  {label:40s} ILLEGAL (min separation {ms:.6f})")
        return None
    v = vol_cell((0, 0, 0), P)
    w = vol_cell((2, 0, 0), P)
    s = v + w
    flag = "   <== BELOW 2sqrt32" if s < TWO_SQ32 - 1e-9 else ""
    print(f"  {label:40s} minsep {ms:.4f}  vol(v) {v:.6f}  vol(w) {w:.6f}  "
          f"sum {s:.9f}  d {s - TWO_SQ32:+.6f}{flag}")
    return s


def main():
    print(f"2*sqrt32 = {TWO_SQ32:.9f};   2*V_dod = {2 * V_DOD:.9f}")
    print()
    print("== symmetric compressed pairs ==")
    results = []
    for n in (5, 4, 3):
        for cap_rings in (0, 5):
            phases = (0.0, 0.6283185307179586) if cap_rings else (0.0,)
            for cap_phase in phases:
                for phase in (0.0, 0.3141592653589793, 0.6283185307179586):
                    P = build(nring=n, phase=phase, caps=True,
                              cap_rings=cap_rings, cap_phase=cap_phase)
                    lab = f"ring{n} ph{phase:.2f} caprings{cap_rings}/{cap_phase:.2f}"
                    s = evaluate(P, lab)
                    if s is not None:
                        results.append((s, lab))
    print()
    if results:
        s, lab = min(results, key=lambda t: t[0])
        print(f"BEST over this family: {s:.9f}   ({lab})")
        print(f"  minus 2*sqrt32 = {s - TWO_SQ32:+.9f}")
        print(f"  minus 2*V_dod  = {s - 2 * V_DOD:+.9f}")
        if s < TWO_SQ32 - 1e-9:
            print("  *** (L) IS REFUTED by this configuration ***")
            return 1
        print("  (L) SURVIVES this family (no refutation).")
    print()
    print("Careful: computed volumes are UPPER bounds for any saturated completion (adding")
    print("centres only shrinks cells), so a value ABOVE 2sqrt32 is NOT evidence for (L);")
    print("only a value BELOW would refute it.")
    return 0


if __name__ == '__main__':
    sys.exit(main())
