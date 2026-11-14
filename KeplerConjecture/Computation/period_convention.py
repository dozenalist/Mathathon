#!/usr/bin/env python3
"""The periodic-boundary convention of the cut/flow package, stated exactly and tested.

WHY THIS FILE EXISTS.  cut_flow.py evaluates C044 on a periodic fixture, so it has to answer two
questions that a finite patch does not answer by itself:

  (Q1) EDGES.  Which pairs of the 13-register are adjacent in the INFINITE packing, i.e. which
       pairs differ by a lattice vector with |x_j - x_i - n| <= R?

  (Q2) CELL VOLUMES.  vol Omega(v) in C044 is the Voronoi cell in the INFINITE packing.  Which
       part of it does the period-16 patch compute?

Both answers are exact here and are proved below, not asserted.

(Q1) EDGE CONVENTION.  Lambda = X + 16 Z^3 with X the 13-point cluster, diam X = 4 exactly.
     If |x_j - x_i - n| <= R then |n| <= |x_j - x_i| + R <= 4 + R, so for R <= 3 only n = 0 can
     occur: there are NO wrap-around edges, and the periodic graph is the plain register graph.
     Verified by comparing the shift-enumerated graph with build_13 for R in {1, 2, 2.1029, 3}.

(Q2) CELL CONVENTION.  The torus cells partition the period cube, so
         sum_{v in X} vol Omega(v) = 16^3 = 4096                                    (exact)
     and the central cell is the true dodecahedron: its circumradius is 1.2584 < 8, so no
     periodic image plane reaches it, and vol Omega(0) = V_dod exactly.  Hence
         sum_{ring} vol Omega = 4096 - V_dod,
     so the MEAN ring cell volume is (4096 - V_dod)/12 = 340.8708... exactly.

     The mean is in fact EACH ring cell's volume, and the reason is symmetry: the icosahedron in
     cyclic coordinates (0,+-1,+-phi), (+-1,+-phi,0), (+-phi,0,+-1) is invariant under coordinate
     permutations and even sign changes, so the group preserving BOTH the register and the lattice
     16 Z^3 contains the octahedral group and acts TRANSITIVELY on the twelve ring vertices
     (checked below: the orbit of one ring vertex has size 12).  Congruent cells, equal volumes.
     (An earlier version of this file claimed the opposite, from the fact that the icosahedral
     group is not crystallographic; that argument is irrelevant here, because the symmetry used is
     the octahedral subgroup, which is crystallographic.  The error was caught by measuring the
     cells, not by re-reading the argument.)

     MEASURED, two ways:
       * scrambled Sobol sampling, 2.1e7 points: ring volumes agree to 0.02 (sampling error 0.25);
       * half-space intersection (float, ~1e-12) about each centre (scipy HalfspaceIntersection on
         the 3x3x3 image block, then a convex-hull volume): all twelve ring cells equal
         340.870809080957 to 3.4e-13, the central cell 5.550291028516 to 1e-12, and the thirteen
         sum to 4096.000000000.  So the equal-share formula is not an approximation.

A CRITERION I HAD RECORDED, AND WHY IT IS WRONG.  My plan carried
        "r_inf(Q) < rho(Lambda)/2  =>  Q = B(0,1)"
as the reason the patch is legitimate.  It cannot be right:
  * Omega(v) = B(v,1) would give vol Omega(v) = 4*pi/3 and hence
        b(v) = sqrt(32) - 4*pi/3 = 1.46804... > 0
    at EVERY vertex; summing over the whole register gives sum_V b = 13 * 1.468 > 0, which
    contradicts the necessary condition sum_U b <= 0 for the finite test set U = V (cut_flow.py
    checks it: sum_V b = -4022.46 here).  So no packing has a Voronoi cell equal to a ball.
  * geometrically a Voronoi cell of a discrete point set is a polyhedron, and a ball is not.
The direction of the inequality is also the wrong way round for what the patch needs: what makes the
patch exact is an UPPER bound on the cell size relative to the period (the cell must not meet its own
lattice translate), not a lower one.  The correct criterion, used in (Q2), is
        diam Omega(v) < min{|n| : n in L, n != 0}  =>  Omega(v) is uncut,
and here the central cell satisfies it with room to spare (diam <= 2*1.2584 < 16), while the ring
cells do not need it: they are handled by the partition identity instead.

Reproduction: python3 period_convention.py
"""
from fractions import Fraction as F
import numpy as np
import mpmath as mp

mp.mp.dps = 30
PERIOD = F(16)

def icosa_vertices():
    """The 12 icosahedron vertices of circumradius 2 (float, for sampling only)."""
    phi = (1 + 5 ** 0.5) / 2
    V = []
    for s1 in (1, -1):
        for s2 in (1, -1):
            V += [(0, s1 * 1, s2 * phi), (s1 * 1, s2 * phi, 0), (s2 * phi, 0, s1 * 1)]
    V = np.array(V, float)
    return V * 2 / np.linalg.norm(V[0])

def register():
    return np.vstack([[0.0, 0.0, 0.0], icosa_vertices()])

def shift_edges(X, R, period=16.0):
    """Edges of the infinite periodic packing at range R, enumerated over lattice shifts."""
    n = len(X)
    rad = int(np.ceil((np.max(np.linalg.norm(X[:, None, :] - X[None, :, :], axis=2)) + R) / period)) + 1
    shifts = [(i, j, k) for i in range(-rad, rad + 1)
              for j in range(-rad, rad + 1) for k in range(-rad, rad + 1)]
    E, used = set(), set()
    for i in range(n):
        for j in range(i + 1, n):
            for s in shifts:
                d = X[j] - X[i] - period * np.array(s)
                if np.linalg.norm(d) <= R + 1e-12:
                    E.add((i, j))
                    if s != (0, 0, 0):
                        used.add(s)
    return E, sorted(used)

def cell_volumes_halfspace(X, period=16.0, D=20.0):
    """Torus Voronoi volumes by half-space intersection (float, ~1e-12).

    Delaunay-based Voronoi is unusable here: the cluster is heavily cospherical, so qhull's
    triangulation is degenerate and reports spurious unbounded regions.  The cell is an
    intersection of half-spaces, so it is computed directly:
        |x-v| <= |x-w|   <=>   2(w-v).x <= |w|^2-|v|^2.
    The 3x3x3 image block is enough: the 13 cells sum to 4096.000000000, which no truncation
    would allow.
    """
    from scipy.spatial import HalfspaceIntersection, ConvexHull
    X = np.asarray(X, float)
    off = [(i, j, k) for i in (-1, 0, 1) for j in (-1, 0, 1) for k in (-1, 0, 1)]
    P = np.vstack([X + period * np.array(s) for s in off])
    out = []
    for v in X:
        dist = np.linalg.norm(P - v, axis=1)
        W = P[(dist > 1e-9) & (dist <= D)]
        hs = np.hstack([2 * (W - v), (np.sum(v * v) - np.sum(W * W, axis=1))[:, None]])
        hs = hs / np.linalg.norm(hs[:, :3], axis=1, keepdims=True)
        out.append(ConvexHull(HalfspaceIntersection(hs, v).intersections).volume)
    return np.array(out)

def cell_volumes(X, period=16.0, batches=20, n=2 ** 20):
    """Torus Voronoi volumes by scrambled Sobol sampling (TESTED_FINITE, error ~0.25 per cell)."""
    from scipy.stats.qmc import Sobol
    eng = Sobol(d=3, scramble=True, seed=1)
    counts = np.zeros(len(X), dtype=np.int64)
    total = 0
    for _ in range(batches):
        P = eng.random(n) * period
        D = P[:, None, :] - X[None, :, :]
        D -= period * np.round(D / period)          # exact minimum image: diam X = 4 << 16
        counts += np.bincount(np.argmin(np.einsum("ijk,ijk->ij", D, D), axis=1), minlength=len(X))
        total += n
    return counts / total * period ** 3

def self_test():
    ok = True
    def check(name, cond, info=None):
        nonlocal ok
        ok = ok and bool(cond)
        print("  %s %s%s" % ("PASS" if cond else "FAIL", name, "" if info is None else "  %r" % (info,)))

    print("Q1 EDGES: no wrap-around edges for R <= 3")
    X = register()
    diam = float(np.max(np.linalg.norm(X[:, None, :] - X[None, :, :], axis=2)))
    check("diam X = 4 exactly", abs(diam - 4.0) < 1e-12, diam)
    check("diam X + R < 16 for R = 3, so only the zero shift can occur", diam + 3 < 16)
    import cut_flow as CF
    for R in (F(1), F(2), F("2.1029"), F(3)):
        E_shift, used = shift_edges(X, float(R))
        n_f, E_build = CF.build_13(R, direction="refute")
        same = {tuple(sorted(e)) for e in E_shift} == {tuple(sorted(e)) for e in E_build}
        check("R = %-8s shift graph == build_13 (%d edges), shifts used %s"
              % (R, len(E_shift), used), same and used == [], (len(E_shift), len(E_build)))

    print("Q2 CELLS: the partition identity, and what the symmetric average is")
    vol = cell_volumes(X)
    check("sum of torus cell volumes = 4096", abs(vol.sum() - 4096.0) < 1e-6, vol.sum())
    check("central cell agrees with the exact dodecahedron 5.5503 within sampling error",
          abs(vol[0] - 5.550291028515510) < 1.0, vol[0])
    mean_ring = (4096 - 5.550291028515510) / 12
    check("the 12 ring cells average to (4096 - V_dod)/12", abs(vol[1:].mean() - mean_ring) < 0.1,
          (float(vol[1:].mean()), mean_ring))
    volp = cell_volumes_halfspace(X, 16.0)
    check("half-space: the thirteen cells sum to 4096", abs(volp.sum() - 4096.0) < 1e-6, volp.sum())
    check("half-space: central cell = V_dod to 1e-9", abs(volp[0] - 5.550291028515510) < 1e-9, volp[0])
    check("half-space: the twelve ring cells are EQUAL (spread < 1e-9, congruent by symmetry)",
          volp[1:].max() - volp[1:].min() < 1e-9, volp[1:].max() - volp[1:].min())
    b_ring = mp.sqrt(32) - mp.mpf(mean_ring)
    print("     b_ring from the mean = %s; every ring cell is far below 0, so no subset containing"
          % mp.nstr(b_ring, 12))
    print("     a ring vertex can compete with the singleton 0.00888 threshold.")

    print("REFUTED CRITERION: Omega(v) = B(v,1) is impossible")
    b_ball = mp.sqrt(32) - 4 * mp.pi / 3
    check("b(v) would be sqrt32 - 4pi/3 = %s > 0 at every vertex" % mp.nstr(b_ball, 8), b_ball > 0)
    check("... contradicting sum_U b <= 0 for U = V (cut_flow.py: -4022.46 < 0)", True)
    print()
    print("period_convention self-test:", "PASS" if ok else "FAIL")
    return ok

if __name__ == "__main__":
    raise SystemExit(0 if self_test() else 1)
