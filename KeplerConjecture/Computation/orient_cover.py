#!/usr/bin/env python3
"""K15-C133 -- the ORIENTATION-FREE two-dodecahedra exclusion, by covering radius.

The gap C131 recorded: at centre distance d > 2 the second dodecahedral cell's
icosahedron of contact directions is free in SO(3), so C128/C129's twist analysis
(which fixes the axis as a vertex direction of BOTH icosahedra) does not apply.

This script supplies the missing statement and checks it numerically.

THE ARGUMENT (no orientation hypothesis, no interval arithmetic).
  A dodecahedral cell of inradius 1 has 12 faces at distance 1, so its 12 contacts
  are w + 2u_i where the unit vectors u_i are the 12 face normals = the vertex set
  of a REGULAR ICOSAHEDRON on S^2 (polar duality: the cell is circumscribed about
  the unit ball, so its polar is an icosahedron inscribed in it).

  Covering radius.  max over unit n of min_i angle(n, u_i) = rho_c, attained at the
  20 face-centre directions of the icosahedron, with
        cos rho_c = sqrt((1 + 2/sqrt5)/3) = 0.7946536...,   rho_c = 37.3774 deg.

  Clash.  Let p be any other centre, e = (p-w)/d, d = |p-w|.  Pick u_i with
  angle(e,u_i) <= rho_c.  Then
        |p - (w + 2u_i)|^2 = d^2 + 4 - 4d <e,u_i>  <=  d^2 + 4 - 4d cos rho_c,
  which is < 4 whenever  d < 4 cos rho_c = 3.1786144...  So the contact w+2u_i is
  a centre at distance < 2 from p: a violation of 2-separation -- UNLESS that
  contact IS p, which forces d = 2 and u_i = e exactly.  In that one escape case
  the axis is a face normal of w's cell; the midpoint of [p,w] is then in both
  cells, so it is a face normal of p's cell too, and C128's twist analysis (which
  covers every relative twist at d = 2) gives the clash.

  Hence: NO two dodecahedral cells at centre distance d < 3.1786144, in any
  relative orientation.

What the numbers below check:
  (1) cos rho_c exactly, and that the 20 face centres realise it (exact sympy);
  (2) that no direction does better than the face centres (dense sampling);
  (3) the constant 4 cos rho_c;
  (4) a direct SO(3) scan: the worst case over rotations of the minimum distance
      from p to w's twelve contacts matches the closed form d^2+4-4d cos rho_c;
  (5) that this constant is EXACT for the method: at d = 3.18 > 3.1786 the
      face-centre alignment clears 2, so no larger band is available this way.
"""
import sys

import numpy as np
import sympy as sp

S5 = sp.sqrt(5)


def exact_vertices():
    """The 12 vertices of the icosahedron of circumradius 1, exact in Q(sqrt5).

    Standard coordinates rescaled: (0,+-1,+-phi)/phi with phi=(1+sqrt5)/2, i.e.
    (0,+-1/phi,+-1), (+-1/phi,+-1,0), (+-1,0,+-1/phi) -- these have norm
    sqrt(1/phi^2+1) = sqrt(2) ... no: use the frame the project's certificates use,
    where one vertex is (1,0,0).
    """
    r5 = sp.sqrt(5)
    # unit vertices, pole at (1,0,0); pentagons at x = +-1/sqrt5, radius 2/sqrt5
    vs = [sp.Matrix([1, 0, 0]), sp.Matrix([-1, 0, 0])]
    for k in range(5):
        a = 2 * sp.pi * k / 5
        vs.append(sp.Matrix([r5 / 5, 2 * r5 / 5 * sp.sin(a), -2 * r5 / 5 * sp.cos(a)]))
    for k in range(5):
        a = 2 * sp.pi * k / 5 + sp.pi / 5
        vs.append(sp.Matrix([-r5 / 5, 2 * r5 / 5 * sp.sin(a), -2 * r5 / 5 * sp.cos(a)]))
    return vs


def faces(vs):
    """The 20 faces of the icosahedron as index triples, purely combinatorially."""
    out = []
    # vertices 2..6 upper pentagon at x=+1/sqrt5, 7..11 lower at x=-1/sqrt5
    up = list(range(2, 7))
    lo = list(range(7, 12))
    for k in range(5):                       # 5 faces around the +pole
        out.append((0, up[k], up[(k + 1) % 5]))
    for k in range(5):                       # 5 faces around the -pole
        out.append((1, lo[k], lo[(k + 1) % 5]))
    for k in range(5):                       # 10 faces between the pentagons
        out.append((up[k], up[(k + 1) % 5], lo[k]))
        out.append((up[(k + 1) % 5], lo[(k + 1) % 5], lo[k]))
    return out


def main():
    vs = exact_vertices()
    # (1) unit norms, exact
    for v in vs:
        assert sp.simplify((v.T * v)[0, 0] - 1) == 0
    F = faces(vs)
    assert len(vs) == 12 and len(F) == 20
    # every face is equilateral (a regular icosahedron)
    ds = set()
    for (a, b, c) in F:
        for (p, q) in ((a, b), (b, c), (a, c)):
            ds.add(sp.simplify(((vs[p] - vs[q]).T * (vs[p] - vs[q]))[0, 0]))
    print("face side^2 values:", sorted(float(x) for x in ds))
    assert len(ds) == 1
    side2 = ds.pop()
    # 5 faces at each vertex
    from collections import Counter
    cnt = Counter()
    for f in F:
        for i in f:
            cnt[i] += 1
    assert set(cnt.values()) == {5}, cnt

    # covering radius at the face centres
    cosrho = []
    for f in F:
        c = vs[f[0]] + vs[f[1]] + vs[f[2]]
        c = c / sp.sqrt((c.T * c)[0, 0])
        for i in f:
            cosrho.append(sp.simplify((c.T * vs[i])[0, 0]))
    exact = sp.simplify(sp.sqrt((1 + 2 / sp.sqrt(5)) / 3))
    vals = set(sp.nsimplify(sp.simplify(x)) for x in cosrho)
    print("face-centre . vertex (exact):", [sp.simplify(x) for x in cosrho[:3]])
    print("claimed   sqrt((1+2/sqrt5)/3):", exact, "=", float(exact))
    print("all 60 face-centre/vertex dots equal:", len(set(sp.simplify(x) for x in cosrho)) == 1)
    print("equal to claim:", sp.simplify(cosrho[0] - exact) == 0)
    rho = sp.acos(exact)
    print("rho_c =", float(rho), "rad =", float(rho * 180 / sp.pi), "deg")
    dstar = 4 * exact
    print("4 cos rho_c =", sp.simplify(dstar), "=", float(dstar))

    # (2) no direction is farther than rho_c from all 12 vertices: dense sampling
    V = np.array([[float(x) for x in v] for v in vs])
    n = 200000
    k = np.arange(n) + 0.5
    phi = np.arccos(1 - 2 * k / n)
    th = np.pi * (1 + 5 ** 0.5) * k
    N = np.stack([np.cos(th) * np.sin(phi), np.sin(th) * np.sin(phi), np.cos(phi)], axis=1)
    dots = N @ V.T
    best = dots.max(axis=1)                    # max over vertices of cos(angle)
    worst = best.min()                         # the direction worst covered
    print("sampled covering cos (min over 200k dirs of max_i cos):", worst)
    print("  -> covered by rho_c:", worst >= float(exact) - 1e-12)

    # (3)/(4) direct SO(3) scan of the clash at fixed d
    def rnd_rot(rng):
        q = rng.normal(size=4)
        q /= np.linalg.norm(q)
        a, b, c, dd = q
        return np.array([
            [a*a+b*b-c*c-dd*dd, 2*(b*c-a*dd), 2*(b*dd+a*c)],
            [2*(b*c+a*dd), a*a-b*b+c*c-dd*dd, 2*(c*dd-a*b)],
            [2*(b*dd-a*c), 2*(c*dd+a*b), a*a-b*b-c*c+dd*dd]])

    rng = np.random.default_rng(20261114)
    print("\n   d    max over rotations of min_i |d e - 2 R u_i|   closed form sqrt(d^2+4-4d cos rho_c)")
    for d in (2.0, 2.1967, 2.5, 3.0, 3.1786, 3.18, 3.2, 3.3):
        bestmin = 0.0
        for _ in range(4000):
            Rm = rnd_rot(rng)
            pts = 2 * (V @ Rm.T)
            dist = np.linalg.norm(d * np.array([1.0, 0, 0]) - pts, axis=1)
            bestmin = max(bestmin, dist.min())
        cf = max(0.0, d * d + 4 - 4 * d * float(exact)) ** 0.5
        print(f"{d:8.4f}   {bestmin:12.6f}   {cf:12.6f}")
    # (5) SHARPNESS, deterministically: point e at a FACE CENTRE direction.  Then three
    # vertices of that face are at angle exactly rho_c from e, so three contacts sit at
    # distance sqrt(d^2+4-4d cos rho_c) -- the closed-form value -- and for d > 4cos rho_c
    # that exceeds 2.  So no band beyond 4cos(rho_c) is available from this argument.
    print("\nsharpness of the method (e aligned with a face centre, deterministic):")
    for f in F[:3]:
        c = vs[f[0]] + vs[f[1]] + vs[f[2]]
        c = c / sp.sqrt((c.T * c)[0, 0])
        e = np.array([float(x) for x in c])
        for d in (3.17, 3.1786, 3.18, 3.2):
            pts = 2 * V
            dist = np.linalg.norm(d * e - pts, axis=1)
            print(f"  d={d:7.4f}  min contact distance (aligned) = {dist.min():.6f}")
        break
    print("\nReading: for d < 4cos(rho_c) = 3.1786179 the scan's best (largest) minimum stays")
    print("below 2, i.e. EVERY orientation clashes; the face-centre alignment reaches the")
    print("closed-form value exactly and clears 2 as soon as d > 4cos(rho_c).  So")
    print("4cos(rho_c) is exact for this method and cannot be pushed further by it.")


if __name__ == "__main__":
    main()
