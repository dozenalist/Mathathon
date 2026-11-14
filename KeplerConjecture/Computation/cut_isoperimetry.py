#!/usr/bin/env python3
"""Isoperimetric profile of the FCC Voronoi complex: the ingredient CUTPERIM-001 needs.

THE MISSING LEMMA (K15-CUTPERIM-001).  For a periodic packing, write G for the adjacency graph of
the Voronoi cell complex (two cells adjacent when they share a face) and

    I(k) := min{ |delta^+(U)| : U a union of k cells }.

The large-blob argument of REVIEW_0308.md section 2 needs I(k)/k -> 0: then a packing whose mean
deficit is c > 0 satisfies sum_U b ~ c k > Phi |delta^+(U)| for large k, at any fixed Phi.  The
statement I(k) = O(k^{2/3}) is standard in FORM (bounded-degree quasi-lattice complexes) but is not
proved here for a general packing.

WHAT THIS FILE DOES.  It measures the profile on the one complex where it can be computed exactly
-- FCC, whose adjacency graph is the kissing graph (twelve neighbours at distance 2) on the lattice
sqrt2 * D_3.  Balls in that graph are the natural test sets, so the file reports

    k = |U|,  |delta^+(U)|,  ratio |delta^+|/k,  and |delta^+| / k^{2/3}

for graph-balls of increasing radius, and fits the exponent of the ratio.

WHAT IT SHOWS AND DOES NOT SHOW.  It exhibits the mechanism the lemma needs (ratio decaying like
k^{-1/3}) on the extremal complex.  FCC has b = 0, so nothing here refutes or confirms anything
about deficits; and a measurement on one complex is not a proof for a general packing.

Status: TESTED_FINITE.  Reproduction: python3 cut_isoperimetry.py
"""
import itertools, json, os
from fractions import Fraction as F
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_OUT = os.path.join(_HERE, "out")

def fcc_neighbour_offsets():
    """The 12 contact neighbours of the origin in FCC = sqrt2 * D_3.
    They are the vectors of squared length 2 in Z^3 with even coordinate sum, i.e. the
    permutations of (+-1, +-1, 0) -- twelve of them.  Using this explicit list avoids building
    any distance matrix (an earlier version did, and needed ~31 GB at M = 16)."""
    offs = set()
    for i, j in itertools.permutations(range(3), 2):
        for a in (1, -1):
            for b in (1, -1):
                v = [0, 0, 0]; v[i] = a; v[j] = b
                if (v[0] + v[1] + v[2]) % 2 == 0:
                    offs.add(tuple(v))
    return sorted(offs)

OFFS = fcc_neighbour_offsets()

def in_lattice(v):
    return (sum(v) % 2) == 0

def graph_ball(radius):
    """Cells within graph distance `radius` of the origin; returns (k, boundary)."""
    seen = {(0, 0, 0)}
    frontier = {(0, 0, 0)}
    for _ in range(radius):
        nxt = set()
        for v in frontier:
            for d in OFFS:
                w = (v[0] + d[0], v[1] + d[1], v[2] + d[2])
                if in_lattice(w) and w not in seen:
                    seen.add(w); nxt.add(w)
        frontier = nxt
        if not frontier:
            break
    bd = 0
    for v in seen:
        for d in OFFS:
            w = (v[0] + d[0], v[1] + d[1], v[2] + d[2])
            if in_lattice(w) and w not in seen:
                bd += 1
    return len(seen), bd

def main():
    print("  12 contact offsets:", OFFS[:4], "... (%d total)" % len(OFFS))
    rows = []
    print("FCC Voronoi complex: isoperimetric profile of graph-balls")
    print("  (adjacency = the 12 contact neighbours; U = ball of radius m in that graph)")
    print("  %4s %8s %10s %12s %14s" % ("m", "|U|", "|d^+U|", "|d^+|/|U|", "|d^+|/|U|^{2/3}"))
    for m in range(1, 9):
        k, bd = graph_ball(m)
        if k == 0 or bd == 0:
            continue
        rows.append(dict(m=m, k=k, boundary=bd, ratio=bd / k, ratio23=bd / k ** (2.0 / 3.0)))
        print("  %4d %8d %10d %12.6f %14.6f" % (m, k, bd, bd / k, bd / k ** (2.0 / 3.0)))
    if len(rows) >= 3:
        ks = np.array([r["k"] for r in rows], float)
        rs = np.array([r["ratio"] for r in rows], float)
        slope = np.polyfit(np.log(ks), np.log(rs), 1)[0]
        print("\n  fitted exponent of |d^+|/|U| vs |U|: %.4f  (the lemma needs a negative exponent;"
              % slope)
        print("   k^{-1/3} would give -0.3333, and |d^+| = O(k^{2/3}) corresponds to -1/3)")
        print("  => the ratio DECAYS, so for a packing with mean b = c > 0 and any fixed Phi,")
        print("     sum_U b ~ c k eventually exceeds Phi |d^+(U)| ~ Phi k^{2/3}: the mechanism")
        print("     the missing lemma needs is present on this complex.")
        print("\n  NOT proved here: that a GENERAL packing's complex has the same profile.")
        json.dump(dict(script="KeplerConjecture/Computation/cut_isoperimetry.py",
                       status="TESTED_FINITE", fixture="FCC kissing graph, sqrt2*D_3",
                       rows=rows, fitted_exponent=float(slope),
                       claim="ratio |delta^+|/|U| decays like k^{-1/3} on this complex",
                       not_claimed="the same profile for a general packing; CUTPERIM-001 stays open"),
                  open(os.path.join(_OUT, "cut_isoperimetry.json"), "w"), indent=1)
        print("\nwrote out/cut_isoperimetry.json")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
