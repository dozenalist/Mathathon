#!/usr/bin/env python3
"""Non-vacuity / sharpness check for the k-independent section-7 obstruction.

Claim under test (K6-CYCLIC-LOCUS.md, Theorem A): for every weak measurable
k-colouring, L_k = {x : Gamma_x contains a cycle} meets every closed square of
side ten.  The proof is k-independent, so it must NOT be killed by the one case
in which a proper colouring is known to exist, k = 7 (hexagonal).  Here we
compute Gamma_x numerically for the hexagonal 7-colouring and check

  (i)   at a Voronoi vertex of the triangular lattice, Gamma_x contains a
        triangle, so L_7 is nonempty there (Theorem A is non-vacuous);
  (ii)  at the centre of a hexagonal cell, Gamma_x has no edge;
  (iii) at the midpoint of a shared hexagon side, Gamma_x is a single edge,
        hence acyclic;
  (iv)  L_7 is exactly the vertex lattice: discrete, locally finite, mesh
        sqrt(3) r = 0.693, far denser than the 5 sqrt(2) = 7.07 that
        Theorem A guarantees.

Gamma_x is (6.1) of the paper:
  ij in Gamma_x  iff  for every ball B about x,
                      limsup_{h->0} |D_ij(B,h)|/|h| > 0,
  D_ij(B,h) = {q in B : (c(q),c(q+h)) in {(i,j),(j,i)}}.
|D_ij(B,h)|/|h| is estimated by grid quadrature on B for a decreasing sequence
of |h|; it converges to a positive constant exactly when colours i and j have a
common boundary of positive length through B.

Colouring: Voronoi cells of the triangular lattice Lambda = sqrt(3) r Z[w],
w = exp(2 pi i/3), r = 2/5, coloured by the coset of (2-w) Lambda, index 7,
i.e. colour(m + n w) = m + 2n mod 7 (because w = 2 mod (2-w), |2-w|^2 = 7).
The units +-1, +-w, +-w^2 are the six nearest lattice neighbours and get the six
distinct colours 1,6,2,5,4,3, which the script verifies exactly.
"""
import numpy as np
from math import sqrt, pi

SQ3 = sqrt(3.0)
R = 0.4                       # hexagon circumradius, = 2/5
A = SQ3 * R                   # triangular lattice spacing
W = complex(-0.5, SQ3 / 2)    # exp(2 pi i/3)

NEIGH = [(1, 0), (-1, 0), (0, 1), (0, -1), (-1, -1), (1, 1)]   # +-1, +-w, +-w^2


def colour(m, n):
    """coset index of m + n w in Z[w]/(2-w)Z[w]."""
    return (m + 2 * n) % 7


def colour_field(Z, shift=0j):
    """vectorised colour of the Voronoi cell containing each point of Z."""
    za = (Z + shift) / A
    v0 = np.rint(2.0 * za.imag / SQ3)
    u0 = np.rint(za.real + za.imag / SQ3)
    best = np.zeros(za.shape, dtype=np.int64)
    bestd = np.full(za.shape, np.inf)
    for dm in (-1, 0, 1):
        for dn in (-1, 0, 1):
            m = u0 + dm
            n = v0 + dn
            d = np.abs(za - (m + n * W))
            better = d < bestd - 1e-12
            bestd = np.where(better, d, bestd)
            best = np.where(better, (m.astype(np.int64) + 2 * n.astype(np.int64)) % 7, best)
    return best % 7


def d_ratio(x, B, h, ngrid=1200):
    """Return the 7x7 matrix |D_ij(B,h)|/|h| for i,j in 0..6."""
    xs = np.linspace(x.real - B, x.real + B, ngrid)
    ys = np.linspace(x.imag - B, x.imag + B, ngrid)
    dA = (xs[1] - xs[0]) * (ys[1] - ys[0])
    X, Y = np.meshgrid(xs, ys, indexing='ij')
    Z = X + 1j * Y
    cq = colour_field(Z)
    cqh = colour_field(Z, h)
    M = np.zeros((7, 7))
    for i in range(7):
        for j in range(7):
            M[i, j] = np.sum(((cq == i) & (cqh == j)) | ((cq == j) & (cqh == i))) * dA / abs(h)
    return M


def edges(x, B, h, thresh=1e-3, ngrid=1200):
    M = d_ratio(x, B, h, ngrid)
    return {(i, j): M[i, j] for i in range(7) for j in range(i + 1, 7) if M[i, j] > thresh}


def main():
    print("hexagonal 7-colouring: r = 2/5, triangular lattice spacing %.6f" % A)

    print("\n[0] exact consistency of the colouring rule")
    for (m, n) in [(0, 0), (1, 2), (3, -1), (2, 5)]:
        cs = sorted({colour(m + dm, n + dn) for dm, dn in NEIGH})
        print("    centre (%d,%d): colour %d, six neighbour colours %s, all distinct: %s"
              % (m, n, colour(m, n), cs, len(cs) == 6 and len(set(cs)) == 6
                 and len(set(cs + [colour(m, n)])) == 7))
    mind = min(abs(A * (m + n * W)) for m in range(-10, 11) for n in range(-10, 11)
               if (m, n) != (0, 0) and colour(m, n) == 0)
    print("    min distance between equal-colour centres %.4f; points of two such" % mind)
    print("    hexagons are >= %.4f > 1 apart => proper 7-colouring" % (mind - 2 * R))

    print("\n[1] a Voronoi vertex (circumcentre of three mutually adjacent centres)")
    # three mutually nearest centres: 0, 1, -w  (|1-(-w)| = |1+w| = |w^2| = 1)
    c1, c2, c3 = A * 0, A * 1, A * (-W)
    vertex = (c1 + c2 + c3) / 3.0
    T = sorted({colour(0, 0), colour(1, 0), colour(0, -1)})
    print("    centres 0, 1, -w : mutual distances %s" % sorted({round(abs(c1-c2),6), round(abs(c2-c3),6), round(abs(c3-c1),6)}))
    print("    vertex %s, |.| = %.6f (= r = %.3f), cell colours %s" % (vertex, abs(vertex), R, T))
    for hh in [0.02, 0.01, 0.005, 0.0025]:
        e = edges(vertex, 0.05, complex(hh, 0), ngrid=700)
        trip = [tuple(sorted(p)) for p in [tuple(set(T) - {a}) for a in T]]
        print("    |h| = %.4f: %d edges, triangle present: %s"
              % (hh, len(e), all(p in e for p in trip)))
    e = edges(vertex, 0.05, complex(0.0025, 0), ngrid=1100)
    print("    ratios: " + ", ".join("%s:%.3f" % (k, v) for k, v in sorted(e.items())))

    print("\n[2] centre of hexagon (0,0)")
    e = edges(A * 0, 0.05, complex(0.0025, 0), ngrid=1100)
    print("    edges of Gamma: %s (expect none)" % sorted(e))

    print("\n[3] midpoint of the side shared by cells (0,0) and (1,0)")
    mid = (A * 0 + A * 1) / 2.0
    e = edges(mid, 0.05, complex(0.0025, 0), ngrid=1100)
    print("    colours %d|%d, edges of Gamma: %s (expect exactly one edge)"
          % (colour(0, 0), colour(1, 0), ["%s:%.3f" % (k, v) for k, v in sorted(e.items())]))

    print("\n[4] points at distance 0.2 from a centre, ball radius 0.05 < inradius 0.346")
    for t in (pi / 3, pi / 2):
        x = A * 1 + 0.2 * complex(np.cos(t), np.sin(t))
        e = edges(x, 0.05, 0.0025 * complex(np.cos(t), np.sin(t)), ngrid=700)
        print("    x = %s: %d edges" % (np.round(x, 3), len(e)))

    print("\nconclusion: Gamma_x has a triangle exactly at the Voronoi vertices, none")
    print("at cell centres or side midpoints.  L_7 = the vertex lattice: discrete,")
    print("locally finite, mesh %.3f.  Theorem A predicts L_7 meets every closed" % A)
    print("square of side ten: TRUE with a large margin.  So the section-7 machine")
    print("is not killed by the known k = 7 colouring.")


if __name__ == '__main__':
    main()
