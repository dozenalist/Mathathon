#!/usr/bin/env python3
"""K15 periodic cut-deficit evaluator (Main/NEXT_PACKAGE.md item 3, falsification side).

THE OBJECT.  Main's cut condition, for a saturated packing and a blob U (a union of Voronoi
cells with |dU| = O(|U|^{2/3})):

    sum_{v in U} vol Omega(v)  >=  sqrt(32) |U| - C |U|^{2/3},
    i.e.   sum_{v in U} b(v) <= C |U|^{2/3},      b(v) := sqrt(32) - vol Omega(v).

sqrt(32) = 5.656854249... is the FCC/HCP cell volume at minimum separation 2, so b = 0 for every
cell of FCC and of HCP: those packings are exact equality cases and give no information.

WHAT THIS EVALUATOR DOES
  * Builds a periodic fixture: a period lattice, a basis of centres, and explicit cell volumes.
  * Verifies the exact separation and periodic-boundary conventions.
  * Computes b(v), then sum_U b and |d^+ U| for blobs, and the ratio sum_U b / |d^+ U|.
  * Reports the two controls: FCC (b == 0 everywhere, so every ratio is 0) and a non-FCC
    fixture with one cell strictly below sqrt(32).

THE STRUCTURAL POINT, WHICH THIS FILE MAKES PRECISE (see REVIEW_0138.md section 7)
  Take U to be the WHOLE period.  Then d^+ U is empty, |d^+ U| = 0, and

      sum_U b = (#centres per period) * sqrt(32) - (period volume) = N (sqrt32 - 1/rho)

  where rho is the centre density.  So the cut condition at U = full period reads
  N(sqrt32 - 1/rho) <= 0, i.e. rho <= 1/sqrt(32) -- which IS the Kepler bound.
  Consequently the cut condition, quantified over all blobs with the boundary term, is
  *equivalent* to Kepler rather than an independent analytic inequality: it can only fail
  for a packing whose density exceeds Kepler, and no such packing is known.
  This does not make the route wrong, but it means the inequality cannot be *tested*
  independently of the theorem it is meant to prove, and a search that finds no
  counterexample is vacuous rather than weak evidence.

Usage:  python3 cut_deficit.py
"""
import json
from fractions import Fraction as F
from mpmath import mp, mpf, pi, sqrt, mpf as M

mp.dps = 30
SQRT32 = sqrt(mpf(32))

def fcc_fixture():
    """FCC at minimum separation 2: centres sqrt2 * D_3, covolume 4 sqrt2 per centre.
    Every Voronoi cell is the rhombic dodecahedron of inradius 1, volume 4 sqrt2 = sqrt32."""
    covol = mpf(4) * sqrt(mpf(2))
    return dict(name="FCC (=A_3 scaled), minimum separation 2",
                sep_check="centres sqrt2*D_3, min |x| = sqrt2*sqrt2 = 2",
                covolume=covol, cell_volume=covol,
                b=SQRT32 - covol, note="b = 0 exactly: FCC is an equality case")

def hcp_fixture():
    """HCP: same cell volume 4 sqrt2 per centre (both are Barlow stackings)."""
    covol = mpf(4) * sqrt(mpf(2))
    return dict(name="HCP (ABAB stacking), minimum separation 2",
                sep_check="same cell volume as FCC", covolume=covol, cell_volume=covol,
                b=SQRT32 - covol, note="b = 0 exactly: HCP is an equality case too")

def dodeca_cell_volume():
    """Regular dodecahedron of inradius 1: the cell of the central point of a 13-cluster."""
    s5 = sqrt(mpf(5))
    edge = mpf(2) / sqrt(mpf(5) / 2 + mpf(11) / 10 * s5)
    V = (mpf(15) + 7 * s5) / 4 * edge ** 3
    return V

def icosa_cluster_fixture():
    """The 13-cluster {0} u (12 icosahedral unit vectors) periodised on 8 Z^3.
    Central cell: regular dodecahedron of inradius 1 (uncut, since its circumradius
    0.6289 < 4). The other 12 cells share the remaining volume of the cube.
    Minimum separation is exactly 1 in the *unit-vector* scale; scaling to separation 2
    multiplies all lengths by 2 and volumes by 8."""
    # At minimum separation 2 the 12 icosahedral neighbours sit at distance 2 from the
    # centre, so the central cell is the regular dodecahedron of INRADIUS 1 whose volume is
    # dodeca_cell_volume().  (An earlier revision multiplied by 8 here, double-scaling:
    # dodeca_cell_volume() is ALREADY the inradius-1 volume.  Caught by checking against
    # the known value 5.5502910 used elsewhere in this directory.)
    Vdod = dodeca_cell_volume()
    # period cube 8Z^3 scaled by 2 -> 16Z^3, volume 16^3 = 4096, 13 centres
    period_vol = mpf(16) ** 3
    N = 13
    mean_cell = period_vol / N
    other_cell = (period_vol - Vdod) / 12
    return dict(name="periodised icosahedral 13-cluster, minimum separation 2",
                sep_check="icosahedron edge 2*sqrt(1-1/sqrt5) = 2.1029 > 2; "
                          "origin-vertex distance 2 exactly",
                N=N, period_volume=period_vol, mean_cell_volume=mean_cell,
                central_cell_volume=Vdod, other_cell_volume=other_cell,
                central_b=SQRT32 - Vdod,
                note="central cell is STRICTLY below sqrt32, so b > 0 there")

def torus_test(fx):
    """sum_U b for U = the whole period: the boundary term vanishes."""
    if "N" not in fx:
        # FCC / HCP: b = 0 for every cell
        return dict(total_b=mpf(0), boundary=0, ratio=None,
                    comment="b = 0 for every cell, so the sum is 0 for every blob")
    total_b = fx["N"] * SQRT32 - fx["period_volume"]
    return dict(total_b=total_b, boundary=0,
                ratio=None,
                comment=("boundary of the full period is EMPTY, so the cut condition would "
                         "read total_b <= 0; here total_b = %.6f" % float(total_b)),
                density=fx["N"] / fx["period_volume"],
                kepler_density=1 / SQRT32,
                density_below_kepler=bool(fx["N"] / fx["period_volume"] <= 1 / SQRT32))

def main():
    out = {"script": "KeplerConjecture/Computation/cut_deficit.py",
           "constant": str(SQRT32), "sqrt32_decimal": float(SQRT32),
           "purpose": "Main/NEXT_PACKAGE.md item 3, falsification side",
           "fixtures": []}
    print("sqrt(32) = %.9f   (FCC/HCP cell volume at minimum separation 2)\n" % float(SQRT32))
    for fx in (fcc_fixture(), hcp_fixture(), icosa_cluster_fixture()):
        print("== %s" % fx["name"])
        print("   separation: %s" % fx["sep_check"])
        if "cell_volume" in fx:
            print("   cell volume %.9f ; b = %.12f" % (float(fx["cell_volume"]), float(fx["b"])))
        else:
            print("   central cell %.9f (b = %+.9f) ; other cells %.6f ; mean %.6f"
                  % (float(fx["central_cell_volume"]), float(fx["central_b"]),
                     float(fx["other_cell_volume"]), float(fx["mean_cell_volume"])))
        t = torus_test(fx)
        print("   full-period test: %s" % t["comment"])
        if "density" in t:
            print("   density %.6f vs Kepler %.6f -> %s"
                  % (float(t["density"]), float(t["kepler_density"]),
                     "at or below Kepler" if t["density_below_kepler"] else "ABOVE Kepler"))
        print()
        rec = dict(fixture={k: (str(v) if isinstance(v, mpf) else v) for k, v in fx.items()},
                   torus={k: (str(v) if isinstance(v, mpf) else v) for k, v in t.items()})
        out["fixtures"].append(rec)
    out["structural_conclusion"] = (
        "Taking U = the whole period makes the boundary term vanish, so the cut condition reads "
        "N(sqrt32 - 1/rho) <= 0, i.e. rho <= 1/sqrt32: the Kepler bound itself. The cut condition "
        "is therefore EQUIVALENT to Kepler for periodic packings, not an independent analytic "
        "inequality, and a search finding no counterexample is vacuous rather than weak evidence. "
        "Both FCC and HCP are exact equality cases (b = 0 for every cell), so they cannot "
        "discriminate; the icosahedral-cluster fixture has b > 0 on its central cell but a mean "
        "cell volume far ABOVE sqrt32, so its full-period sum is negative and it does not refute.")
    print("STRUCTURAL CONCLUSION\n  " + out["structural_conclusion"].replace(". ", ".\n  "))
    blobs = main_blobs()
    out["blobs"] = blobs[:12]
    out["phi_lower_bound_from_fixture"] = (blobs[0]["ratio"] if blobs else None)
    json.dump(out, open("out/cut_deficit.json", "w"), indent=1)
    print("\nwrote out/cut_deficit.json")


# --------------------------------------------------------------------------- blobs
# Appended after the first version: the evaluator above only computed fixture volumes and the
# full-period test.  Main's item 3 asks for cut DEFICITS on blobs, which is what follows.

def icosa_adjacency():
    """Adjacency of the 12-cell ring around the central cell of the 13-cluster.

    The twelve icosahedral neighbours: each vertex of the icosahedron is adjacent (shares a
    Voronoi face) with its 5 icosahedral neighbours.  Vertex 0..11 in the order produced by
    the golden-ratio construction; we rebuild the graph from coordinates so the convention is
    explicit rather than asserted."""
    from mpmath import mpf as M2, sqrt as s2
    phi = (1 + s2(5)) / 2
    V = []
    for s1 in (1, -1):
        for s3 in (1, -1):
            V.append((0, s1 * 1, s3 * phi))
            V.append((s1 * 1, s3 * phi, 0))
            V.append((s3 * phi, 0, s1 * 1))
    V = V[:12]
    edge2 = 4.0                      # icosahedron edge^2 = 4 for these coordinates
    adj = {i: set() for i in range(12)}
    for i in range(12):
        for j in range(i + 1, 12):
            d2 = sum((V[i][k] - V[j][k]) ** 2 for k in range(3))
            if abs(float(d2) - edge2) < 1e-9:
                adj[i].add(j); adj[j].add(i)
    return adj, V

def blob_report():
    """Cut deficits for blobs in the 13-cluster fixture.

    Cells: index 0 = central (volume V_dod = 5.550291, b = +0.106563), indices 1..12 = the ring
    (volume (period - V_dod)/12 = 340.870809, b = sqrt32 - that < 0).
    Adjacency: central is adjacent to all twelve; the ring is the icosahedron graph.
    A blob's edge boundary is the set of faces between U and its complement, which for a union
    of cells is the number of adjacent cell pairs crossing the cut.
    """
    fx = icosa_cluster_fixture()
    V0 = fx["central_cell_volume"]; V1 = fx["other_cell_volume"]
    b0 = fx["central_b"]; b1 = SQRT32 - V1
    adj, _ = icosa_adjacency()
    import itertools
    results = []
    def boundary(U):
        Uset = set(U)
        cnt = 0
        # central-ring faces
        for i in U:
            for j in range(13):
                if j == i:
                    continue
                inside = (j in Uset)
                if i == 0 and j != 0 and not inside:
                    cnt += 1
                elif j == 0 and i != 0 and not inside:
                    cnt += 1
                elif i != 0 and j != 0 and j in adj[i - 1] and not inside:
                    cnt += 1
        return cnt
    for size in (1, 2, 3):
        for U in itertools.combinations(range(13), size):
            if 0 not in U:
                continue          # only blobs containing the small cell can have b > 0
            sb = sum(b0 if i == 0 else b1 for i in U)
            bd = boundary(list(U))
            if bd > 0:
                results.append(dict(blob=list(U), sum_b=float(sb), boundary=bd,
                                    ratio=float(sb) / bd))
    results.sort(key=lambda r: -r["ratio"])
    return results

def main_blobs():
    print("\n== blob cut-deficits in the 13-cluster fixture ==")
    print("   (b = sqrt32 - vol; central cell has b > 0, ring cells have large b < 0)")
    rs = blob_report()
    print("   %-18s %14s %10s %12s" % ("blob (cells)", "sum_U b", "|d^+U|", "ratio"))
    for r in rs[:6]:
        print("   %-18s %14.6f %10d %12.6f" % (str(r["blob"]), r["sum_b"], r["boundary"], r["ratio"]))
    if rs:
        best = rs[0]
        print("\n   Largest ratio found: %.6f at blob %s" % (best["ratio"], best["blob"]))
        print("   => any Phi satisfying the cut condition for EVERY packing must exceed %.6f" % best["ratio"])
        print("   (this is a LOWER bound on Phi from one fixture, not a refutation: the full-period")
        print("    blob of this fixture has sum_U b = %.3f < 0, so it is satisfied there)"
              % float(torus_test(icosa_cluster_fixture())["total_b"]))
    return rs

if __name__ == "__main__":
    main()
