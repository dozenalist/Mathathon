#!/usr/bin/env python3
"""K15 attempted Frank-Kasper fixture: a MEASURED negative, with the reason.

WHY.  cut_fixture_close.py showed that FCC/HCP are jammed, so a near-Kepler fixture with
unequal cell volumes cannot be made by perturbation.  The next idea was a Frank-Kasper phase
(A15, Cr3Si type), which has unequal Voronoi cells by construction.  This file tests that idea
and REFUTES it for equal spheres.

WHAT IS MEASURED (nothing asserted; the crystallography is computed)
  A15 Wyckoff sites in the cubic cell of side a: 2a = (0,0,0), (1/2,1/2,1/2) and
  6c = (1/4,0,1/2), (1/2,1/4,0), (0,1/2,1/4), (3/4,0,1/2), (1/2,3/4,0), (0,1/2,3/4).
  With all eight sites occupied by equal spheres:

    * the shortest distance in the structure is a/2, between 6c chain atoms;
    * the 2a-6c distance is a*sqrt(5)/4 = 0.5590 a > a/2, so at the a/2 contact scale the 2a
      atoms are NOT touched;
    * scaling so that the contact distance is 2 gives cubic side 4, cell volume 64, and packing
      fraction  8 * (4 pi/3) * 1^3 / 64 = pi/6 = 0.523599,
      i.e. exactly the SIMPLE CUBIC value, far below Kepler 0.740480.

CONCLUSION.  A15 with equal spheres is not a dense packing; Frank-Kasper phases are dense for
polydisperse mixtures, not for congruent spheres.  So the hoped-for "near-Kepler periodic
packing with unequal Voronoi cells" does not come from this structure either.

This matters for Main/NEXT_PACKAGE.md item 3: between this file and K15-C-CUTJAM-001, the
near-Kepler regime appears to be populated only by the close-packed stackings, all of which have
EQUAL cell volumes, hence b = 0 identically and no discriminating power for the cut condition.
That is a third reason the near-Kepler regime looks locally close-packed.  NOTE: the earlier
reading of these three findings as "the cut condition is equivalent to Kepler"
(K15-C-CUTEQUIV-001) is WITHDRAWN -- C044 quantifies over finite U and a period is not finite;
what the three findings support is the difficulty of the CONVERSE direction, Kepler => a finite
Phi works (K15-C-CUTIMPLIES-003 proves only the other direction).

Output: out/cut_fixture_frank_kasper.json.  Reproduction: python3 cut_fixture_frank_kasper.py
"""
import itertools, json
import numpy as np

KEPLER = 0.7404804896930611

def measure(sites, label):
    S = np.eye(3)
    pts = []
    for k in itertools.product(range(-2, 3), repeat=3):
        pts.append(sites + np.array(k))
    pts = np.vstack(pts)
    d = np.linalg.norm(pts[:, None, :] - pts[None, :, :], axis=2)
    np.fill_diagonal(d, np.inf)
    dmin = d.min()
    scale = 2.0 / dmin                      # so the contact distance becomes 2
    side = scale
    vol = side ** 3
    n = len(sites)
    frac = n * (4 * np.pi / 3) * 1.0 ** 3 / vol
    # per-type distances
    a2 = sites[:2]; a6 = sites[2:]
    if len(a6) == 0:
        min26 = float("nan")
    else:
        min26 = float(np.linalg.norm(a2[:, None, :] - a6[None, :, :], axis=2).min())
    return dict(label=label, n=n, min_distance_cell_units=float(dmin),
                scale=float(scale), cubic_side=float(side), cell_volume=float(vol),
                packing_fraction=float(frac), kepler=KEPLER,
                ratio_to_kepler=float(frac / KEPLER),
                min_2a_6c_distance_cell_units=min26,
                note=("equal spheres: the 2a site is untouched at the a/2 contact scale, so the "
                      "structure is inefficient"))

def main():
    a15 = np.array([[0, 0, 0], [.5, .5, .5],
                    [.25, 0, .5], [.5, .25, 0], [0, .5, .25],
                    [.75, 0, .5], [.5, .75, 0], [0, .5, .75]], float)
    sc = np.array([[0, 0, 0]], float)
    fcc = np.array([[0, 0, 0], [0, .5, .5], [.5, 0, .5], [.5, .5, 0]], float)
    rows = [measure(sc, "simple cubic (control)"),
            measure(fcc, "FCC conventional cell (control)"),
            measure(a15, "A15 (Cr3Si) sites, equal spheres")]
    print("measured packing fractions (contact distance scaled to 2)\n")
    print("  %-38s %8s %12s %12s %10s" % ("structure", "n", "min dist", "packing", "vs Kepler"))
    for r in rows:
        print("  %-38s %8d %12.6f %12.6f %9.1f%%"
              % (r["label"], r["n"], r["min_distance_cell_units"], r["packing_fraction"],
                 100 * (r["ratio_to_kepler"] - 1)))
    print("\nA15 detail: min 2a-6c distance = %.6f (cell units) vs the a/2 = %.6f contact,"
          % (rows[2]["min_2a_6c_distance_cell_units"], rows[2]["min_distance_cell_units"]))
    print("so the 2a atoms are untouched and the structure rattles: equal-sphere A15 gives")
    print("packing fraction %.6f = pi/6 = the simple-cubic value, NOT a dense packing."
          % rows[2]["packing_fraction"])
    print("\nCONCLUSION (with K15-C-CUTJAM-001, a third reason the near-Kepler regime looks")
    print("  close-packed): the near-Kepler regime appears populated only by the close-packed")
    print("  stackings, all of which have EQUAL cell volumes, hence b = 0.  (The earlier")
    print("  'equivalent to Kepler' reading, K15-C-CUTEQUIV-001, is WITHDRAWN.)")
    json.dump(dict(script="KeplerConjecture/Computation/cut_fixture_frank_kasper.py",
                   status="TESTED_FINITE (negative, measured)",
                   finding=("A15 Wyckoff sites with equal spheres give packing fraction pi/6 = "
                            "0.523599, because the 2a site is at a*sqrt5/4 = 0.559a from 6c and is "
                            "untouched at the a/2 chain contact"),
                   implication=("no near-Kepler periodic fixture with unequal Voronoi cells from "
                                 "this structure either; consistent with K15-C-CUTJAM-001"),
                   rows=rows), open("out/cut_fixture_frank_kasper.json", "w"), indent=1)
    print("\nwrote out/cut_fixture_frank_kasper.json")

if __name__ == "__main__":
    main()
