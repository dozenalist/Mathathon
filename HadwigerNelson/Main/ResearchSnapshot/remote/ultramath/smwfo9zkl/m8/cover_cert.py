#!/usr/bin/env python3
"""Exact certificates for the covering step of Section 7 of the five-colour paper.

CERTIFIED STATEMENT A.  For the closed square Q = [-5,5]^2 there is an explicit
finite family of OPEN axis-parallel rectangles with
   (i)   Q contained in their union,
   (ii)  no point of Q lying in more than three of them,
   (iii) every member of Euclidean diameter at most 1.
Scaling by t > 0 turns this into the same statement for the side-10t square and
mesh t, so multiplicity-3 covers exist at EVERY mesh.

CERTIFIED STATEMENT B (sharpness control).  The maximum multiplicity is exactly
3, so the family is not a multiplicity-2 cover.  That is the right control: at
multiplicity two the mesh bound is a genuine obstruction (Lemma 7.5 of the paper,
which improves from "mesh at most two" to "mesh below half the side"), while at
multiplicity three nothing obstructs at any mesh.

Why this matters at k = 6.  Section 7 of the paper turns a weak measurable
colouring into a continuous map into the 1-skeleton of the simplex on the labels
and then contradicts the multiplicity-2 cover obstruction.  At k = 6 a palette can
have three labels, so the cover that arises before the transition-graph argument
can have multiplicity three.  Statement A shows that no cover-theoretic argument
can repair that: multiplicity three obstructs nothing, at any mesh.  The paper's
Lemma 7.4 is therefore not a convenience but the only place where the reduction to
the 1-skeleton can come from (see S7-K6-TRANSFER.md, Theorem 2).

All arithmetic is exact integer arithmetic: lengths are scaled by SC, diameters
are compared squared, and no floating point enters either verifier.

Verifier V1 (arrangement).  The x- and y-edges of the members together with the
square's sides cut Q into strata (relatively open 2-cells, open vertical and
horizontal segments, vertices).  Every member either contains a whole stratum or
is disjoint from it, so covering and multiplicity reduce to finitely many exact
integer tests.  Multiplicity is maximal on 2-cells; all strata are checked.

Verifier V2 (sweep), an independent algorithm.  For every abscissa in the finite
set of slab midpoints and edge abscissae it recomputes the active family and
solves, exactly, a 1-dimensional open-interval covering problem for [-5,5] and an
open-interval maximum-depth problem.

Run: python3 cover_cert.py     (exit code 0 iff every instance is certified)
"""
import sys
from fractions import Fraction as Fr

def bricks(L, H, EPS, half):
    """Open rectangles (a,b)x(c,d), a brick-wall pattern with opening EPS."""
    out = []
    jlo, jhi = -int(half // H) - 2, int(half // H) + 2
    ilo, ihi = -int(half // L) - 2, int(half // L) + 2
    for j in range(jlo, jhi + 1):
        y0, y1 = j * H, (j + 1) * H
        off = 0 if (j % 2 == 0) else L // 2
        for i in range(ilo, ihi + 1):
            x0, x1 = off + i * L, off + (i + 1) * L
            a, b, c, d = x0 - EPS, x1 + EPS, y0 - EPS, y1 + EPS
            if b > -half and a < half and d > -half and c < half:
                out.append((a, b, c, d))
    return out

def grid(coords, half):
    s = {-half, half}
    for t in coords:
        if -half < t < half:
            s.add(t)
    return sorted(s)

def in_cell2(r, u1, u2, v1, v2):
    a, b, c, d = r
    return a <= u1 and u2 <= b and c <= v1 and v2 <= d
def in_vseg(r, x, v1, v2):
    a, b, c, d = r
    return a < x < b and c <= v1 and v2 <= d
def in_hseg(r, u1, u2, y):
    a, b, c, d = r
    return a <= u1 and u2 <= b and c < y < d
def in_point(r, x, y):
    a, b, c, d = r
    return a < x < b and c < y < d

def V1(rects, half):
    xs = grid([t for r in rects for t in (r[0], r[1])], half)
    ys = grid([t for r in rects for t in (r[2], r[3])], half)
    actx = [[r for r in rects if r[0] <= xs[ix] and xs[ix + 1] <= r[1]]
            for ix in range(len(xs) - 1)]
    fail, mmax, wit = [], 0, None
    for ix in range(len(xs) - 1):
        x0, x1, mx2 = xs[ix], xs[ix + 1], xs[ix] + xs[ix + 1]
        for iy in range(len(ys) - 1):
            y0, y1, my2 = ys[iy], ys[iy + 1], ys[iy] + ys[iy + 1]
            cov, cnt = False, 0
            for r in actx[ix]:
                if in_cell2(r, x0, x1, y0, y1):
                    cov = True
                if 2 * r[2] < my2 < 2 * r[3]:
                    cnt += 1
            if cnt > mmax:
                mmax, wit = cnt, ('2cell', x0, x1, y0, y1)
            if not cov:
                fail.append(('2cell', x0, x1, y0, y1))
    for x in xs:
        act = [r for r in rects if r[0] < x < r[1]]
        for iy in range(len(ys) - 1):
            y0, y1, my2 = ys[iy], ys[iy + 1], ys[iy] + ys[iy + 1]
            if not any(in_vseg(r, x, y0, y1) for r in act):
                fail.append(('vseg', x, y0, y1))
            cnt = sum(1 for r in act if 2 * r[2] < my2 < 2 * r[3])
            if cnt > mmax:
                mmax, wit = cnt, ('vseg', x, y0, y1)
    for y in ys:
        act = [r for r in rects if r[2] < y < r[3]]
        for ix in range(len(xs) - 1):
            x0, x1 = xs[ix], xs[ix + 1]
            if not any(in_hseg(r, x0, x1, y) for r in act):
                fail.append(('hseg', x0, x1, y))
            cnt = sum(1 for r in act if 2 * r[0] < x0 + x1 < 2 * r[1])
            if cnt > mmax:
                mmax, wit = cnt, ('hseg', x0, x1, y)
    for x in xs:
        act = [r for r in rects if r[0] < x < r[1]]
        for y in ys:
            if not any(in_point(r, x, y) for r in act):
                fail.append(('vertex', x, y))
            cnt = sum(1 for r in act if r[2] < y < r[3])
            if cnt > mmax:
                mmax, wit = cnt, ('vertex', x, y)
    return dict(covered=not fail, fail=fail[:4], multiplicity=mmax, wit=wit,
                nx=len(xs), ny=len(ys))

def V2(rects, half):
    raw = sorted({t for r in rects for t in (r[0], r[1])})
    inr = sorted({-half, half} | {t for t in raw if -half < t < half})
    tests = set(Fr(t) for t in inr)
    for u, v in zip(inr, inr[1:]):
        tests.add(Fr(u + v, 2))
    fail, mmax, wit = [], 0, None
    for x in sorted(tests):
        active = [(r[2], r[3]) for r in rects if r[0] < x < r[1]]
        pts = sorted({Fr(-half), Fr(half)} | {Fr(c) for c, _ in active} | {Fr(d) for _, d in active})
        cov = True
        for u in pts:
            if -half <= u <= half and not any(c < u < d for c, d in active):
                cov = False; break
        if cov:
            for u, v in zip(pts, pts[1:]):
                m = (u + v) / 2
                if -half <= m <= half and not any(c < m < d for c, d in active):
                    cov = False; break
        if not cov:
            fail.append(x)
        cand = sorted({Fr(-half), Fr(half)} | {Fr(c) for c, _ in active}
                      | {Fr(d) for _, d in active} | {Fr(c + d, 2) for c, d in active})
        for y in cand:
            if -half <= y <= half:
                k = sum(1 for c, d in active if c < y < d)
                if k > mmax:
                    mmax, wit = k, (x, y)
    return dict(covered=not fail, fail=fail[:4], multiplicity=mmax, wit=wit, n=len(tests))

def instance(L, H, EPS, half, mu):
    """one parameter setting; mu is an integer multiple of 1/SC."""
    rects = bricks(L, H, EPS, half)
    mu2 = mu * mu
    over = [r for r in rects if (r[1]-r[0])**2 + (r[3]-r[2])**2 > mu2]
    a = V1(rects, half); b = V2(rects, half)
    ok = (a['covered'] and b['covered'] and not over
          and a['multiplicity'] <= 3 and b['multiplicity'] <= 3
          and a['multiplicity'] == b['multiplicity'])
    print("L=%3d h=%3d eps=%3d half=%4d mu=%3d | members=%4d maxdiam^2=%5d mu^2=%5d | "
          "V1 cov=%s mult=%d | V2 cov=%s mult=%d | %s"
          % (L, H, EPS, half, mu, len(rects),
             max((r[1]-r[0])**2 + (r[3]-r[2])**2 for r in rects), mu2,
             a['covered'], a['multiplicity'], b['covered'], b['multiplicity'],
             "OK" if ok else "FAIL"), flush=True)
    return ok, a['multiplicity'], b['multiplicity'], len(rects)

def main():
    print("Section 7 covering step: multiplicity-3 open covers at bounded diameter")
    print("all lengths are integers in units of 1/20 of the plane length", flush=True)
    print()
    cases = [
        # (L, h, eps, half, mu):  diameter of a member is sqrt((L+2eps)^2+(h+2eps)^2)
        (10,  5, 1, 100,  20),   # the certified instance: side 10, mesh 1
        (20, 10, 1, 100,  40),   # same square, coarser mesh 2
        (20, 10, 1, 200,  40),   # side 20 square, mesh 2
        (10,  5, 1, 200,  40),   # side 20 square, mesh 2, fine bricks
        (40, 20, 2, 100,  80),   # side 10 square, mesh 4 (< 5 = half the side)
    ]
    results = [instance(*c) for c in cases]
    ok = all(r[0] for r in results)
    print()
    print("every instance certified:", ok)
    print("multiplicities found:", sorted({r[1] for r in results} | {r[2] for r in results}))
    print("Statement A (multiplicity-3 open cover, mesh < half the side):", ok)
    print("Statement B (the cover is not of multiplicity 2):",
          all(r[1] == 3 and r[2] == 3 for r in results))
    return 0 if ok else 1

if __name__ == '__main__':
    sys.exit(main())
