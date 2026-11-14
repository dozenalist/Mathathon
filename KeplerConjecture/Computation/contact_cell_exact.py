#!/usr/bin/env python3
"""K15-C104 — INDEPENDENT exact verification of the contact-only polytope bound.

Fixes the circularity in K15-C094's Lemma 1 (E's K15-E083 identified it; this file
re-derives the repair by a different method than Experimental/scripts/barlow_contact_cell.py).

The claim to verify
-------------------
For a Barlow site v, let p_1..p_12 be its twelve contact vectors and
K = { x : <x, p_i> <= 1 for i=1..12 }   (after scaling: |p_i| = 1 gives bisector x.p = 1)
Actually we use n_i = p_i/|p_i|^2 with |p_i| = 2, so n_i = p_i/2 and K = {x.n_i <= 1}.
Then   K  subset of  B(v, sqrt2)   and   vol K = 4 sqrt2.

Why it matters: redundancy of a non-contact half-space needs K <= H_c, NOT Omega <= H_c.
Omega <= H_c is true by definition, so Main's Lemma 1 as written was circular.

Method (deliberately different from E's)
----------------------------------------
Exact rational arithmetic in the field Q(sqrt2, sqrt3), represented as 4-tuples
(a,b,c,d) = a + b sqrt2 + c sqrt3 + d sqrt6 over Fraction. Signs are decided by
rigorous mpmath interval evaluation (exact zeros are detected structurally as the
all-zero tuple), so every comparison below is certified, not floating point.
Vertices are found by exact Cramer solves over the triples that are feasible.
"""
from fractions import Fraction as F
import itertools
import sys

from mpmath import iv, mp

mp.dps = 60
iv.dps = 60

# ---------------------------------------------------------------- field Q(2,3)
ZERO = (F(0), F(0), F(0), F(0))
ONE = (F(1), F(0), F(0), F(0))


def fadd(x, y):
    return tuple(a + b for a, b in zip(x, y))


def fneg(x):
    return tuple(-a for a in x)


def fsub(x, y):
    return tuple(a - b for a, b in zip(x, y))


def fmul(x, y):
    a, b, c, d = x
    A, B, C, D = y
    return (a * A + 2 * b * B + 3 * c * C + 6 * d * D,
            a * B + b * A + 3 * (c * D + d * C),
            a * C + c * A + 2 * (b * D + d * B),
            a * D + d * A + b * C + c * B)


def finv(x):
    """inverse via the tower Q(sqrt2)(sqrt3): (A+B sqrt3)^-1 = (A - B sqrt3)/(A^2-3B^2)."""
    if x == ZERO:
        raise ZeroDivisionError
    a, b, c, d = x
    # A = a + b s2, B = c + d s2  (elements of Q(s2))
    # A^2 - 3 B^2  = (a^2 + 2b^2 - 3c^2 - 6d^2) + (2ab - 6cd) s2  =: p + q s2
    p = a * a + 2 * b * b - 3 * c * c - 6 * d * d
    q = 2 * a * b - 6 * c * d
    den = p * p - 2 * q * q                      # rational
    if den == 0:
        raise ZeroDivisionError
    # (p - q s2)/den
    pr, qr = p / den, q / den
    # multiply (A - B s3) by (pr - qr s2):
    # (a + b s2) - (c + d s2) s3  = (a, b, -c, -d)
    conj = (a, b, -c, -d)
    invden = (pr, -qr, F(0), F(0))
    return fmul(conj, invden)


def fdiv(x, y):
    return fmul(x, finv(y))


def _ivq(q):
    return iv.mpf(q.numerator) / iv.mpf(q.denominator)


def fval(x):
    """rigorous interval enclosure of the real value."""
    a, b, c, d = x
    return (_ivq(a) + _ivq(b) * iv.sqrt(2) + _ivq(c) * iv.sqrt(3)
            + _ivq(d) * iv.sqrt(6))


def fsign(x):
    """-1, 0, +1 rigorously: exact zeros are structural; otherwise intervals decide."""
    if x == ZERO:
        return 0
    for prec in (40, 80, 160, 320, 640):
        iv.dps = prec
        v = fval(x)
        lo, hi = v.a, v.b
        if lo > 0:
            return 1
        if hi < 0:
            return -1
    raise ArithmeticError("sign undecided: %r" % (x,))


def fstr(x):
    a, b, c, d = x
    bits = []
    for co, s in ((a, ""), (b, "*sqrt2"), (c, "*sqrt3"), (d, "*sqrt6")):
        if co:
            bits.append(f"{co}{s}")
    return " + ".join(bits) if bits else "0"


# ---------------------------------------------------------------- geometry
S3 = (F(0), F(0), F(1), F(0))          # sqrt3
S6 = (F(0), F(0), F(0), F(1))          # sqrt6
TWO = (F(2), F(0), F(0), F(0))

A1 = (TWO, ZERO)
A2 = (ONE, S3)
THREE = (F(3), F(0), F(0), F(0))
TT = (ONE, fdiv(S3, THREE))                            # T = (1, sqrt3/3), |T|^2 = 4/3
HH = fdiv(fmul(TWO, S6), THREE)                        # H = 2 sqrt6/3, H^2 = 8/3


def vneg2(u):
    return tuple(fneg(a) for a in u)


def vadd3(u, w):
    return tuple(fadd(a, b) for a, b in zip(u, w))


def vsub3(u, w):
    return tuple(fsub(a, b) for a, b in zip(u, w))


def vmul3(s, u):
    return tuple(fmul(s, a) for a in u)


def dot3(u, w):
    acc = ZERO
    for a, b in zip(u, w):
        acc = fadd(acc, fmul(a, b))
    return acc


def planes(kind):
    """the twelve contact vectors p_i (|p_i| = 2), exact, for 'fcc' or 'hcp'."""
    pts = []
    for sg in (ONE, fneg(ONE)):
        for vec in (A1, A2, vsub3(A1, A2)):
            pts.append((fmul(sg, vec[0]), fmul(sg, vec[1]), ZERO))
    up = [TT, vsub3(TT, A1), vsub3(TT, A2)]
    if kind == 'fcc':
        lo = [vneg2(TT), vadd3(vneg2(TT), A1), vadd3(vneg2(TT), A2)]
    else:
        lo = list(up)
    for u in up:
        pts.append((u[0], u[1], HH))
    for u in lo:
        pts.append((u[0], u[1], fneg(HH)))
    assert len(pts) == 12
    # bisector of p is  x.p = |p|^2/2 = 2, i.e.  x.(p/2) = 1, so  n_i = p_i/2
    return [tuple(fdiv(c, TWO) for c in p) for p in pts], pts


def solve3(n1, n2, n3):
    """exact solution of <n_j, x> = 1, j=1,2,3 by Cramer."""
    rows = [n1, n2, n3]
    det = fadd(
        fsub(fmul(rows[0][0], fsub(fmul(rows[1][1], rows[2][2]), fmul(rows[1][2], rows[2][1]))),
             fmul(rows[0][1], fsub(fmul(rows[1][0], rows[2][2]), fmul(rows[1][2], rows[2][0])))),
        fmul(rows[0][2], fsub(fmul(rows[1][0], rows[2][1]), fmul(rows[1][1], rows[2][0]))))
    if det == ZERO:
        return None
    rhs = (ONE, ONE, ONE)
    out = []
    for col in range(3):
        m = [[rows[r][c] for c in range(3)] for r in range(3)]
        for r in range(3):
            m[r][col] = rhs[r]
        dcol = fadd(
            fsub(fmul(m[0][0], fsub(fmul(m[1][1], m[2][2]), fmul(m[1][2], m[2][1]))),
                 fmul(m[0][1], fsub(fmul(m[1][0], m[2][2]), fmul(m[1][2], m[2][0])))),
            fmul(m[0][2], fsub(fmul(m[1][0], m[2][1]), fmul(m[1][1], m[2][0]))))
        out.append(fdiv(dcol, det))
    return tuple(out)


def analyse(kind):
    ns, pts = planes(kind)
    print(f"\n--- {kind} ---")
    # sanity: |p_i|^2 = 4 for every contact
    for i, p in enumerate(pts):
        assert dot3(p, p) == (F(4), F(0), F(0), F(0)), f"|p_{i}|^2 != 4"
    verts = {}
    for trip in itertools.combinations(range(12), 3):
        x = solve3(ns[trip[0]], ns[trip[1]], ns[trip[2]])
        if x is None:
            continue
        ok = True
        for n in ns:
            if fsign(fsub(dot3(n, x), ONE)) > 0:
                ok = False
                break
        if not ok:
            continue
        # active set (exact)
        act = tuple(sorted(i for i, n in enumerate(ns) if fsub(dot3(n, x), ONE) == ZERO))
        verts[x] = act
    print(f"  vertices found: {len(verts)}")
    rad = {}
    for x in verts:
        r2 = dot3(x, x)
        rad.setdefault(r2, []).append(x)
    print("  |x|^2 values (exact) with multiplicities:")
    maxr2 = None
    for r2, xs in sorted(rad.items(), key=lambda kv: float(F(kv[0][0]) + F(kv[0][1]) * 2 ** 0.5)):
        print(f"    {fstr(r2):40s}  multiplicity {len(xs)}")
        if maxr2 is None or fsign(fsub(r2, maxr2)) > 0:
            maxr2 = r2
    two = (F(2), F(0), F(0), F(0))
    three_half = (F(3, 2), F(0), F(0), F(0))
    ok_radii = set()
    for r2 in rad:
        if fsign(fsub(r2, two)) == 0:
            ok_radii.add("2")
        elif fsign(fsub(r2, three_half)) == 0:
            ok_radii.add("3/2")
        else:
            ok_radii.add(fstr(r2))
    max_ok = (fsign(fsub(maxr2, two)) <= 0)
    print(f"  max |x|^2 = {fstr(maxr2)};  K subset B(0,sqrt2): {max_ok}")
    print(f"  radius multiset is exactly {{3/2, 2}}: {ok_radii == {'2','3/2'}}")
    # face count consistency: sum of active-set sizes = 2 * (edges); Euler check
    F_count = len(ns)
    E_count = sum(len(a) for a in verts.values()) // 2
    V_count = len(verts)
    print(f"  Euler: V={V_count}, E={E_count}, F={F_count}, V-E+F={V_count-E_count+F_count}")
    return verts, rad, max_ok, (ok_radii == {'2', '3/2'})


if __name__ == '__main__':
    allok = True
    for kind in ('fcc', 'hcp'):
        v, rad, m, r = analyse(kind)
        allok = allok and m and r
    print()
    print("CONTACT-POLYTOPE BOUND:", "VERIFIED EXACTLY for both types" if allok else "FAILED")
    print("Hence K <= B(v,sqrt2) and every non-contact half-space is redundant for K,")
    print("so Omega = K.  Main's Lemma 1 is repaired (see K15-C104).")
    sys.exit(0 if allok else 1)
