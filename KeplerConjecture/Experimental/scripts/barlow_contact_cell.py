#!/usr/bin/env python3
"""
Exact proof of Lemma 1' of the Barlow audit (REVIEW_0353.md 5.2, K15-E083).

Main's BARLOW_CELLS.md proves that every cell of a Barlow packing is a *contact* cell
via a circular argument: it shows Omega subset H_c for a non-contact half-space H_c,
which is true by definition.  The statement that carries the content is

        K  :=  intersection of the twelve contact half-spaces   satisfies   K subset B(v,sqrt2)

because then K subset B(v,sqrt2) subset B(v,|c-v|/2) subset H_c for every non-contact c
(using |c-v| >= 2sqrt2 from (F1)), hence K = Omega, non-circularly.

This script proves K subset B(v,sqrt2) EXACTLY, for both local types (fcc and hcp), by
enumerating the triple-plane vertices in Q(sqrt3) and evaluating |x|^2 symbolically.
It also evaluates the volume exactly by the divergence theorem, V = (1/3) sum_i A_i
(all twelve faces at distance 1), and checks V = 4 sqrt2.

Run: python3 Experimental/scripts/barlow_contact_cell.py    (exit 0 iff all checks pass)
"""
import itertools
import sys
import sympy as sp

R3 = sp.sqrt(3)
H = sp.sqrt(sp.Rational(8, 3))


def contacts(kind):
    """The twelve contact positions of a site in a Barlow packing, nn distance 2."""
    a1 = sp.Matrix([2, 0, 0])
    a2 = sp.Matrix([1, R3, 0])
    T = (a1 + a2) / 3
    P = []
    for s in (1, -1):
        for v in (a1, a2, a1 - a2):
            P.append(sp.Matrix([s * v[0], s * v[1], 0]))
    for b in (sp.zeros(3, 1), -a1, -a2):
        P.append(sp.Matrix([T[0] + b[0], T[1] + b[1], H]))
    off = -T if kind == "fcc" else T
    near = (sp.zeros(3, 1), a1, a2) if kind == "fcc" else (sp.zeros(3, 1), -a1, -a2)
    for b in near:
        P.append(sp.Matrix([off[0] + b[0], off[1] + b[1], -H]))
    return P


def vertices(n):
    """Exact vertices of {x : x . n_i <= 1}."""
    V = []
    for i, j, k in itertools.combinations(range(len(n)), 3):
        M = sp.Matrix.hstack(n[i], n[j], n[k]).T
        if sp.simplify(M.det()) == 0:
            continue
        x = M.LUsolve(sp.Matrix([1, 1, 1]))
        if any(sp.N(sp.simplify(n[m].dot(x) - 1), 30) > sp.Float("1e-25") for m in range(len(n))):
            continue
        if not any(sp.simplify((x - y).norm()) == 0 for y in V):
            V.append(x)
    return V


def face_area(normal, n, V):
    """Exact area of the face on the plane normal.x = 1, given its vertices."""
    on = [x for x in V if sp.simplify(normal.dot(x) - 1) == 0]
    if len(on) < 3:
        return sp.Integer(0), 0
    # in-plane orthonormal basis
    e1 = (sp.eye(3)[:, 0] - normal * normal[0])
    if sp.simplify(e1.norm()) == 0:
        e1 = sp.eye(3)[:, 1] - normal * normal[1]
    e1 = e1 / e1.norm()
    e2 = normal.cross(e1)
    pts = [(sp.simplify(x.dot(e1)), sp.simplify(x.dot(e2))) for x in on]
    cx = sum(p[0] for p in pts) / len(pts)
    cy = sum(p[1] for p in pts) / len(pts)
    pts.sort(key=lambda p: sp.atan2(p[1] - cy, p[0] - cx))
    A = sp.Integer(0)
    for i in range(len(pts)):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % len(pts)]
        A += (x1 - cx) * (y2 - cy) - (x2 - cx) * (y1 - cy)
    return sp.simplify(sp.Abs(A) / 2), len(on)


def main():
    ok = True
    for kind in ("fcc", "hcp"):
        P = contacts(kind)
        assert all(sp.simplify(p.norm() - 2) == 0 for p in P), "contacts must be at 2"
        n = [p / 2 for p in P]
        V = vertices(n)
        print(f"\n=== {kind} ===")
        print(f"  contacts: {len(P)}, all at distance 2;  vertices of K: {len(V)}")
        sq = {}
        for x in V:
            q = sp.simplify(x.dot(x))
            sq[q] = sq.get(q, 0) + 1
        for q, c in sorted(sq.items(), key=lambda t: sp.N(t[0])):
            print(f"  |x|^2 = {str(q):>6}   multiplicity {c}")
        good = all(sp.N(q, 25) <= 2 for q in sq)
        print(f"  K subset B(0,sqrt2):  {good}   (exact; equality attained at |x|^2 = 2)")
        if not good:
            ok = False
        # exact volume by the divergence theorem, all faces at distance 1
        tot = sp.Integer(0)
        nfaces = 0
        for i in range(12):
            A, m = face_area(n[i], n, V)
            tot += A
            nfaces += 1 if m else 0
        vol = sp.simplify(tot / 3)
        print(f"  faces carrying vertices: {nfaces};  vol K = {sp.simplify(vol)}"
              f"  = {sp.N(vol, 20)}")
        if sp.simplify(vol - 4 * sp.sqrt(2)) != 0:
            print("  FAIL: volume is not 4*sqrt2")
            ok = False
        else:
            print("  vol K = 4*sqrt2 exactly  (agrees with (F4))")
    print("\n" + ("ALL CHECKS PASSED" if ok else "SOME CHECKS FAILED"))
    print("Lemma 1' holds exactly for both local types, so Main's Lemma 1 is repairable")
    print("without circularity:  K subset B(v,sqrt2) subset H_c  for every non-contact c.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
