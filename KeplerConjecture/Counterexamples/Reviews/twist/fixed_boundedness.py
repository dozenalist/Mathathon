#!/usr/bin/env python3
"""K15-X-C080 fix: an exact decision of "is {y : y.n_i <= d_i} bounded?".

E's `origin_interior_certificate` decides "0 in the INTERIOR of conv{n_i}" by scanning planes through
triples of normals and testing whether the origin is strictly on the inner side. That is false: it
accepts [(1,0,0),(0,1,0),(0,0,1)] (hull is a triangle in x+y+z=1, origin not in it) and it accepts
[(1,0,0),(0,1,0),(0,0,1),(1,1,1)] where all four points have x+y+z = 1, so 0 is not even in the hull --
and that hull is 3-dimensional. Replacing b x c by (b-a) x (c-a) does not repair it (the triangle still
passes), because the missing ingredient is not the plane normal but the dimension of the hull.

The correct criterion, used here: the polyhedron P = {y : y.n_i <= d_i} is bounded iff its recession
cone R = {d : d.n_i <= 0 for all i} is {0}; and R = {0} iff 0 is in the interior of conv{n_i}. R is a
polyhedral cone, so if R != {0} it contains a nonzero direction that is either +-n_i (when R is a
halfspace) or +-(n_i x n_j) (an extreme ray, the intersection of two of the planes), or a line of that
form. Deciding R = {0} is therefore a finite exact check over those candidate directions -- rational
arithmetic, no planes through triples, no float.

Run: exit 0 iff every case below is decided as stated.
"""
import itertools
import sys
from fractions import Fraction as F


def recession_is_zero(normals):
    """True iff {d : d.n_i <= 0 for all i} = {0}, i.e. 0 in int conv{normals}."""
    cand = list(normals)
    for a, b in itertools.combinations(normals, 2):
        c = (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
        if c != (0, 0, 0):
            cand.append(c)
    cand = cand + [tuple(-x for x in v) for v in cand]
    for d in cand:
        if d == (0, 0, 0):
            continue
        if all(sum(d[t] * n[t] for t in range(3)) <= 0 for n in normals):
            return False, d
    return True, None


def bounded_gate(normals, dists):
    """(bounded?, n_vertices, ray/vertices). Refuses an unbounded polyhedron. Rational arithmetic.
    This is the gate only: E's volume formula on a bounded input is not what is in question."""
    ok, ray = recession_is_zero(normals)
    if not ok:
        return False, 0, ray
    N = len(normals)
    verts = []
    for i, j, k in itertools.combinations(range(N), 3):
        M = [normals[i], normals[j], normals[k]]
        D = (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1])
             - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
             + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))
        if D == 0:
            continue
        rhs = [dists[i], dists[j], dists[k]]
        x = []
        for c in range(3):
            Mc = [list(M[r]) for r in range(3)]
            for r in range(3):
                Mc[r][c] = rhs[r]
            x.append((Mc[0][0] * (Mc[1][1] * Mc[2][2] - Mc[1][2] * Mc[2][1])
                      - Mc[0][1] * (Mc[1][0] * Mc[2][2] - Mc[1][2] * Mc[2][0])
                      + Mc[0][2] * (Mc[1][0] * Mc[2][1] - Mc[1][1] * Mc[2][0])) / D)
        x = tuple(x)
        if all(sum(normals[m][t] * x[t] for t in range(3)) <= dists[m] for m in range(N)):
            if x not in verts:
                verts.append(x)
    return True, len(verts), verts


def main():
    e1, e2, e3 = (F(1), F(0), F(0)), (F(0), F(1), F(0)), (F(0), F(0), F(1))
    cases = [
        ("3 unit vectors: 0 NOT in hull (2-dim)", [e1, e2, e3], False),
        ("tetra e1,e2,e3,(1,1,1): 0 NOT in hull", [e1, e2, e3, (F(1), F(1), F(1))], False),
        ("tetra e1,e2,e3,(-1,-1,-1): 0 interior", [e1, e2, e3, (F(-1), F(-1), F(-1))], True),
        ("cube normals: 0 interior", [tuple(F(1) if t == i else F(0) for t in range(3))
                                      for i in range(3)]
         + [tuple(F(-1) if t == i else F(0) for t in range(3)) for i in range(3)], True),
        ("octahedron normals: 0 interior", [(F(1), F(0), F(0)), (F(-1), F(0), F(0)),
                                            (F(0), F(1), F(0)), (F(0), F(-1), F(0)),
                                            (F(0), F(0), F(1)), (F(0), F(0), F(-1))], True),
    ]
    bad = 0
    for name, N, want in cases:
        got, ray = recession_is_zero(N)
        flag = "ok" if got == want else "MISMATCH"
        if got != want:
            bad += 1
        print(f"  {name:45s} -> {got} (want {want}) {flag}" + (f"  ray {ray}" if ray else ""))
    # the consequence: the unbounded tetra must be refused where E's helper accepts it
    N = [e1, e2, e3, (F(1), F(1), F(1))]
    ok, nv, ray = bounded_gate(N, [F(1)] * 4)
    print(f"\n  unbounded tetra {{y.n_i <= 1}}: bounded? {ok} (want False), ray {ray}")
    if ok:
        bad += 1
    # and a bounded control must still be right: the cube {|y_i| <= 1} has volume 8
    N = [tuple(F(1) if t == i else F(0) for t in range(3)) for i in range(3)] \
        + [tuple(F(-1) if t == i else F(0) for t in range(3)) for i in range(3)]
    ok, nv, _ = bounded_gate(N, [F(1)] * 6)
    print(f"  cube {{|y_i| <= 1}}: bounded? {ok} with {nv} vertices (want True, 8)")
    if not ok or nv != 8:
        bad += 1
    print("\n" + ("ALL PASS -- recession-cone test decides all five cases and refuses the unbounded tetra"
                  if bad == 0 else f"{bad} FAILURES"))
    return 0 if bad == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
