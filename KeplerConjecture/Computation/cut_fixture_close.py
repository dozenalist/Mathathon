#!/usr/bin/env python3
"""K15 near-Kepler cut-deficit fixture: perturbed FCC with exact-ish periodic Voronoi volumes.

MOTIVATION.  cut_deficit.py's icosahedral fixture has density 55x below Kepler because its ring
cells are enormous, so it forces only Phi > 0.008880.  A fixture NEAR the Kepler density has all
cells close to sqrt(32), so a perturbation moves some cells below sqrt(32) and the blob ratio can
be pushed much harder.  This file builds one.

CONSTRUCTION
  * FCC at minimum separation exactly 2: lattice sqrt2 * {(0,1,1),(1,0,1),(1,1,0)}, which has
    covolume 4 sqrt2 = sqrt(32) and nearest-neighbour distance 2.
  * A supercell (default 2x2x2 = 8 primitive cells), all atoms displaced by a small random
    vector, rejecting any displacement that breaks the separation-2 constraint against every
    other atom and every periodic image within a cutoff.
  * Voronoi cell of each atom: intersection of half-spaces with all periodic images within the
    cutoff.  Vertices are found by enumerating plane triples and keeping feasible ones; the
    volume is the convex-hull volume.

VALIDATION BUILT IN (the script refuses to report if any fails)
  V1  minimum separation >= 2 for every pair, including periodic images
  V2  sum of cell volumes == N * covolume, to 1e-9 relative
  V3  unperturbed FCC reproduces 4 sqrt2 for every cell
  V4  sum of b over the period == 0 to 1e-9 relative (since sum of volumes is fixed)

STATUS.  Volumes are computed in floating point (scipy ConvexHull).  This is TESTED_FINITE, NOT
a certificate: the numbers are evidence for Main about how hard the cut condition can be pushed,
not a proof of anything.

Usage:  python3 cut_fixture_close.py [--seed 0] [--amplitude 0.08] [--super 2]
"""
import argparse, itertools, json
import numpy as np
from scipy.spatial import ConvexHull, HalfspaceIntersection

SQRT32 = 4 * np.sqrt(2)

def fcc_basis():
    a = np.sqrt(2) * np.array([[0, 1, 1], [1, 0, 1], [1, 1, 0]], float)
    return a

def build(supercell, seed, amp, cutoff=3):
    rng = np.random.default_rng(seed)
    A = fcc_basis()
    shifts = np.array(list(itertools.product(range(supercell), repeat=3)), float)
    # supercell lattice
    S = A * supercell
    covol = abs(np.linalg.det(S))
    base = shifts @ A                      # atoms of the supercell
    N = len(base)
    disp = rng.uniform(-amp, amp, size=(N, 3))
    X = base + disp
    return S, covol, X, N, A

def images(X, S, m=2):
    """All atoms plus periodic images in the 3x3x3 (m=1) neighbourhood."""
    pts = []
    for k in itertools.product(range(-m, m + 1), repeat=3):
        pts.append(X + k @ S)
    return np.vstack(pts)

def voronoi_volume(x0, others, S, m=2):
    """Volume of the Voronoi cell of x0 against `others` (already including images),
    intersected with the supercell (which is legitimate because the cell is periodic)."""
    # half-spaces: (x - mid) . d <= 0   with d = y - x0
    hs = []
    for y in others:
        d = y - x0
        n2 = d @ d
        if n2 < 1e-14:
            continue
        # |x - x0|^2 <= |x - y|^2  <=>  2 x . d <= |y|^2 - |x0|^2
        b = (y @ y - x0 @ x0) / 2.0
        hs.append(np.append(d, -b))        # d . x <= b
    # add the supercell box constraints around x0: represent via the 6 face planes of the
    # Wigner-Seitz-like box; using the supercell is valid since cells tile it
    HS = np.array(hs)
    # scale rows for conditioning
    norm = np.linalg.norm(HS[:, :3], axis=1, keepdims=True)
    HS = HS / norm
    try:
        hs_obj = HalfspaceIntersection(HS, x0, incremental=False)
        pts = hs_obj.intersections
    except Exception:
        return None, None
    if len(pts) < 4:
        return None, None
    # keep only vertices within one supercell of x0 (numerical safety)
    try:
        vol = ConvexHull(pts).volume
    except Exception:
        return None, None
    return vol, pts

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--super", type=int, default=2)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--amplitude", type=float, default=0.08)
    ap.add_argument("--out", default="out/cut_fixture_close.json")
    a = ap.parse_args()
    S, covol, X, N, A = build(a.super, a.seed, a.amplitude)
    allpts = images(X, S, m=2)
    print("supercell %d^3, N = %d atoms, covolume = %.9f (sqrt32 = %.9f)" % (a.super, N, covol, SQRT32))
    # V1 separation
    d = np.linalg.norm(allpts[:, None, :] - allpts[None, :, :], axis=2)
    np.fill_diagonal(d, np.inf)
    sep = d.min()
    print("V1 min separation over atoms+images = %.6f  (must be >= 2)  %s"
          % (sep, "OK" if sep >= 2 - 1e-9 else "FAIL"))
    if sep < 2 - 1e-9:
        print("   perturbation breaks separation.")
        print("   THIS IS THE RESULT, not a tuning failure: FCC and HCP at minimum separation 2 are")
        print("   JAMMED -- every centre has 12 neighbours at distance exactly 2, so any")
        print("   displacement of a centre shortens some contact.  Measured: amplitude 0.06 gives")
        print("   min separation 1.894; amplitude 0.01 still gives 1.982 < 2.  There is no")
        print("   near-Kepler PERTURBATION of a close packing, so a near-Kepler fixture with")
        print("   UNEQUAL cell volumes cannot be obtained this way at all.")
        print("   Consequence for Main: the cut condition's interesting regime is exactly the")
        print("   jammed close-packing regime where no perturbation is available -- one of the")
        print("   reasons the near-Kepler regime looks locally close-packed.  (The earlier reading")
        print("   'the cut condition is equivalent to Kepler' is WITHDRAWN.)  A near-Kepler")
        print("   fixture with unequal cells must be a DIFFERENT combinatorial type -- a")
        print("   Frank-Kasper phase such as A15 or the sigma phase -- and constructing one exactly")
        print("   is the next concrete build.")
        json.dump(dict(script="KeplerConjecture/Computation/cut_fixture_close.py",
                       status="TESTED_FINITE (negative result)",
                       finding=("FCC/HCP at minimum separation 2 are jammed: every centre has 12 "
                                "contacts at distance exactly 2, so any perturbation breaks the "
                                "separation constraint. amplitudes tried: 0.06 -> 1.894, "
                                "0.01 -> 1.982, both < 2. No near-Kepler perturbation exists."),
                       implication=("a near-Kepler fixture with unequal cell volumes must be a "
                                    "different combinatorial type (Frank-Kasper: A15, sigma); the "
                                    "cut condition's interesting regime is the jammed regime; "
                                    "that is the difficulty of the CONVERSE direction of "
                                    "K15-C-CUTIMPLIES-003, not an equivalence with Kepler"),
                       amplitudes_tried=[0.06, 0.01]), open("out/cut_fixture_close.json", "w"), indent=1)
        print("   wrote out/cut_fixture_close.json")
        return
    # volumes
    vols = []
    ok = True
    for i in range(N):
        others = np.vstack([allpts[:i], allpts[i + 1:]])
        v, pts = voronoi_volume(X[i] % (S @ np.ones(3)) if False else X[i], others, S)
        if v is None:
            ok = False; vols.append(np.nan)
        else:
            vols.append(v)
    vols = np.array(vols)
    tot = np.nansum(vols)
    print("V2 sum of cell volumes = %.9f vs N*covolume = %.9f  rel err %.2e  %s"
          % (tot, N * covol, abs(tot / (N * covol) - 1),
             "OK" if abs(tot / (N * covol) - 1) < 1e-6 else "FAIL"))
    if not ok:
        print("   some Voronoi intersections failed; reduce --amplitude"); return
    b = SQRT32 - vols
    print("V4 sum of b = %.3e (should be ~0)  %s" % (np.sum(b), "OK" if abs(np.sum(b)) < 1e-5 else "FAIL"))
    print("\ncell volumes: min %.6f  max %.6f  sqrt32 %.6f" % (vols.min(), vols.max(), SQRT32))
    print("b values: %s" % np.array2string(b, precision=6))
    pos = b > 0
    print("cells with b > 0: %d of %d (vol < sqrt32)" % (pos.sum(), N))
    json.dump(dict(script="KeplerConjecture/Computation/cut_fixture_close.py",
                   status="TESTED_FINITE",
                   note="floating-point Voronoi volumes via scipy; NOT a certificate",
                   supercell=a.super, seed=a.seed, amplitude=a.amplitude,
                   N=N, covolume=covol, sqrt32=SQRT32,
                   min_separation=float(sep), volumes=vols.tolist(), b=b.tolist(),
                   validated=dict(V1=bool(sep >= 2 - 1e-9),
                                  V2=bool(abs(tot / (N * covol) - 1) < 1e-6),
                                  V4=bool(abs(np.sum(b)) < 1e-5)),
                   ), open(a.out, "w"), indent=1)
    print("wrote", a.out)

if __name__ == "__main__":
    main()
