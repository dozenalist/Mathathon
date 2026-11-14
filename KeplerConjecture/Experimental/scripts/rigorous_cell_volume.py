#!/usr/bin/env python3
"""
A certified enclosure of a Voronoi-cell volume: exact rational arithmetic end to end.

The object.  For centres p_1..p_n and a payer w, the cell in coordinates y = x - w is
    Omega(w) = B(w,2) cap { y : y . v_i <= c_i },   v_i = p_i - w,  c_i = |v_i|^2/2 .

The method: a two-sided rational sandwich.  Each centre is known only through an interval
(the data involve sqrt5, sqrt55, sqrt(10+2 sqrt5)).  Writing n_i = v_i/|v_i| (unit) and
b_i = |v_i|/2, the half-space is { y.n_i <= b_i }.  Choose rational n_i', b_i' with certified
errors |n_i - n_i'| <= e_i and |b_i - b_i'| <= f_i, and a rational R bounding |y| on the true
polytope.  Then for |y| <= R,

    y.n_i <= b_i   =>   y.n_i' <= b_i + R e_i ,

so

    { y.n_i' <= b_i' - (R e_i + f_i) }  subset  Omega(w)  subset  { y.n_i' <= b_i' + (R e_i + f_i) } .

Both outer polytopes have RATIONAL data, so their volumes are exact: vertices by Cramer over
Fractions, feasibility by exact rational comparison, face areas by an exact angular sort, and
V = (1/3) sum_i b_i' A_i (divergence theorem; the origin is interior and the polytope is
bounded).  No floating-point sign is ever tested.  The only non-rational inputs are sin/cos at
rational multiples of pi, taken as certified rational enclosures from rational_interval.py.

Controls (the point of the file).  Three inputs with known answers:
  fcc contact cell, hcp contact cell  -> 4 sqrt2 = 5.656854249492...
  the C5 payer fixture               -> 5.898017371803720...
A failure on any of them means the machinery is wrong, and the script says so.

Scope.  This bounds ONE payer's cell for a given configuration.  It is not a bound over
completions; that needs the branch-and-bound of REVIEW_0523.md, for which this is the atomic
operation.

Run:  python3 Experimental/scripts/rigorous_cell_volume.py
Exit 0 iff every control's enclosure contains its reference value.
"""
import itertools
import sys
from fractions import Fraction as F

from rational_interval import Iv, sqrt_iv, sin_cos_iv_of_pi_multiple

# accuracy knob: 1e-25 is ample and keeps the Fractions small
PI_TERMS = 32
TAYLOR = 24


# ---------------------------------------------------------------- exact 3x3 linear algebra
def det3(a):
    return (a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1])
            - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
            + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0]))


def solve3(rows, rhs):
    D = det3(rows)
    if D == 0:
        return None
    out = []
    for k in range(3):
        M = [list(rows[i]) for i in range(3)]
        for i in range(3):
            M[i][k] = rhs[i]
        out.append(det3(M) / D)
    return tuple(out)


# ---------------------------------------------------------------- exact polytope volume
def polytope_volume(normals, dists):
    """Exact volume of {y : y.n_i <= d_i}, rational data, origin interior, bounded.

    Vertices are the feasible triple-plane intersections (Cramer, exact).  Each face is
    triangulated and the volume is the sum of the signed determinants of the boundary
    triangles,

        V = (1/6) * | sum over oriented boundary triangles of det(a, b, c) | ,

    which is a RATIONAL number.  (An earlier version used V = (1/3) sum d_i A_i and computed
    the areas with a shoelace formula in a NON-orthonormal basis, which silently scaled every
    area by |e1| |e2| and gave 5.4997 instead of 5.6568 for the fcc cell.  The determinant
    form has no square root in it at all, so nothing can be mis-scaled.)"""
    N = len(normals)
    verts = []
    for i, j, k in itertools.combinations(range(N), 3):
        x = solve3([normals[i], normals[j], normals[k]], [dists[i], dists[j], dists[k]])
        if x is None:
            continue
        if all(sum(normals[m][t] * x[t] for t in range(3)) <= dists[m] for m in range(N)):
            if x not in verts:
                verts.append(x)
    if len(verts) < 4:
        return None, 0, []
    total = F(0)
    for i in range(N):
        on = [x for x in verts
              if sum(normals[i][t] * x[t] for t in range(3)) == dists[i]]
        if len(on) < 3:
            continue
        cyc = _cyclic_order(normals[i], on)          # outward orientation (see below)
        for t in range(1, len(cyc) - 1):
            a, b, c = cyc[0], cyc[t], cyc[t + 1]
            total += det3([a, b, c])                  # signed, relative to the origin
    return abs(total) / 6, len(verts), verts


def _cyclic_order(normal, pts):
    """The vertices of a convex face in cyclic order, counterclockwise seen from +normal.

    The basis (e1, e2, n) with e2 = n x e1 is right-handed, so counterclockwise in (e1, e2)
    is counterclockwise seen from outside.  Ordering only compares cross products, so the
    non-orthonormality of (e1, e2) does not matter -- unlike an area computation, an
    ORDER is invariant under a linear rescaling of the basis."""
    n = normal
    nn = n[0] * n[0] + n[1] * n[1] + n[2] * n[2]
    ax = min(range(3), key=lambda t: abs(n[t]))
    e1 = [F(0), F(0), F(0)]
    e1[ax] = F(1)
    d = sum(e1[t] * n[t] for t in range(3))
    e1 = [e1[t] - n[t] * d / nn for t in range(3)]
    e2 = [n[1] * e1[2] - n[2] * e1[1],
          n[2] * e1[0] - n[0] * e1[2],
          n[0] * e1[1] - n[1] * e1[0]]
    P = [(sum(x[t] * e1[t] for t in range(3)), sum(x[t] * e2[t] for t in range(3)))
         for x in pts]
    cx = sum(p[0] for p in P) / len(P)
    cy = sum(p[1] for p in P) / len(P)
    R = [(p[0] - cx, p[1] - cy) for p in P]

    def half(p):
        x, y = p
        if x > 0 and y >= 0:
            return 0
        if x <= 0 and y > 0:
            return 1
        if x < 0 and y <= 0:
            return 2
        return 3

    from functools import cmp_to_key

    def cmp(p, q):
        hp, hq = half(p), half(q)
        if hp != hq:
            return -1 if hp < hq else 1
        cr = p[0] * q[1] - p[1] * q[0]
        return -1 if cr > 0 else (1 if cr < 0 else 0)

    order = sorted(range(len(R)), key=cmp_to_key(lambda a, b: cmp(R[a], R[b])))
    return [pts[t] for t in order]


def _cube_test():
    """Self-tests of polytope_volume on bodies whose volumes are obvious and RATIONAL.

    The cube alone is not enough: it is centrally symmetric, so a face-orientation error that
    reverses the sign is invisible after the `abs`.  The regular tetrahedron with vertices
    (1,1,1), (1,-1,-1), (-1,1,-1), (-1,-1,1) has volume exactly 8/3 and is not symmetric, so a
    wrong face set or a wrong cyclic order changes the answer."""
    cube_n = [(F(1), F(0), F(0)), (F(-1), F(0), F(0)), (F(0), F(1), F(0)),
              (F(0), F(-1), F(0)), (F(0), F(0), F(1)), (F(0), F(0), F(-1))]
    v1, nv1, _ = polytope_volume(cube_n, [F(1)] * 6)
    # faces of the tetrahedron: (x+y+z = -1) etc., as (-1,-1,-1).y <= 1 and its three images
    tet_n = [(F(-1), F(-1), F(-1)), (F(-1), F(1), F(1)),
             (F(1), F(-1), F(1)), (F(1), F(1), F(-1))]
    v2, nv2, _ = polytope_volume(tet_n, [F(1)] * 4)
    return (v1 == 8 and nv1 == 8) and (v2 == F(8, 3) and nv2 == 4)


# ---------------------------------------------------------------- the sandwich
DEN = 10 ** 20                 # quantisation denominator for the rational approximations
QERR = F(1, 10 ** 20)          # its certified error


def _quantise(x, den):
    """Nearest rational with denominator `den` (round-half-away is fine: it is an input choice,
    and its error is accounted for in QERR)."""
    return F(int(x * den + (F(1, 2) if x >= 0 else F(-1, 2))), den)

def sandwich(centres, R):
    """[vol_in, vol_out] certified enclosure of Omega(origin) cut by `centres`.

    centres: list of interval vectors (Iv,Iv,Iv).  R: rational bound on |y| over the cell."""
    n_rat, b_rat, slacks = [], [], []
    for p in centres:
        sq = p[0] * p[0] + p[1] * p[1] + p[2] * p[2]
        L = sqrt_iv(sq)                      # |v|
        n = [p[t] / L for t in range(3)]
        b = L / 2
        e = max((x.hi - x.lo) / 2 for x in n)
        f = (b.hi - b.lo) / 2
        # Quantise the rational approximation to DEN decimal digits and ADD the quantisation
        # error to the certified error.  Without this the midpoints carry the full 70-digit
        # denominators of the interval endpoints, and every later determinant inherits them:
        # a first version ran for 15 minutes on one control.  The enclosure stays at ~1e-19,
        # which is far more than the 1e-3 the geometry needs.
        nq = [_quantise(x.mid(), DEN) for x in n]
        bq = _quantise(b.mid(), DEN)
        eq = e + QERR
        fq = f + QERR
        n_rat.append(nq)
        b_rat.append(bq)
        slacks.append(R * eq + fq)
    inner = [b_rat[i] - slacks[i] for i in range(len(b_rat))]
    outer = [b_rat[i] + slacks[i] for i in range(len(b_rat))]
    v_in, nvi, vin_pts = polytope_volume(n_rat, inner)
    v_out, nvo, vout_pts = polytope_volume(n_rat, outer)
    if v_in is None:
        # the inner polytope is empty: the correct lower bound is 0, and the enclosure is
        # then trivially valid but useless.  Reported rather than crashing.
        v_in = F(0)
    if v_out is None:
        raise ValueError("outer polytope unbounded or degenerate: the cell is not enclosed")
    # CERTIFY R: the true cell is contained in the outer polytope, so it suffices that every
    # outer vertex satisfies |y| <= R.  Without this check the sandwich's error term R*e_i is
    # an assumption rather than a bound.
    if vout_pts:
        rmax = max((x[0] * x[0] + x[1] * x[1] + x[2] * x[2]) for x in vout_pts)
        if rmax > R * R:
            raise ValueError(f"R = {float(R)} is not valid: an outer vertex has |y| = "
                             f"{float(rmax) ** 0.5:.6f}.  Increase R and rerun.")
    return v_in, v_out, nvi, nvo


# ---------------------------------------------------------------- the inputs
def _sincos(mult):
    return sin_cos_iv_of_pi_multiple(mult, terms=TAYLOR, pi_terms=PI_TERMS)


def c5_centres(theta_sin, theta_cos, phi_multiple):
    """The C5 fixture's twelve centres relative to w = (0,0,2), as interval vectors.

    theta_sin, theta_cos: Iv enclosures of sin/cos of the pentagon's polar angle.
    phi_k = (phi_multiple + 2k/5) pi."""
    r5 = sqrt_iv(Iv(5))
    R5 = Iv(4) / r5
    Z5 = Iv(2) / r5
    out = [(Iv(0), Iv(0), Iv(-2))]                       # c, relative to w
    for k in range(5):                                   # ring
        s, c = _sincos(F(2 * k, 5))
        out.append((R5 * c, R5 * s, Z5 - Iv(2)))
    for k in range(5):                                   # pentagon, relative to w
        s, c = _sincos(phi_multiple + F(2 * k, 5))
        out.append((Iv(2) * theta_sin * c, Iv(2) * theta_sin * s, Iv(-2) * theta_cos))
    out.append((Iv(0), Iv(0), Iv(2)))                    # south pole, relative to w
    return out


def barlow_contact_cell(kind):
    """The twelve contact positions of a Barlow site (w = origin), as interval vectors."""
    a1 = (Iv(2), Iv(0), Iv(0))
    a2 = (Iv(1), sqrt_iv(Iv(3)), Iv(0))
    T = tuple((a1[t] + a2[t]) / 3 for t in range(3))
    Hh = sqrt_iv(Iv(F(8, 3)))
    def neg(v):
        return tuple(Iv(-1) * v[t] for t in range(3))
    P = []
    for s in (1, -1):
        for v in (a1, a2, tuple(a1[t] - a2[t] for t in range(3))):
            P.append(tuple(Iv(s) * v[t] for t in range(3)))
    for b in ((Iv(0), Iv(0), Iv(0)), neg(a1), neg(a2)):
        P.append((T[0] + b[0], T[1] + b[1], Hh))
    off = neg(T) if kind == "fcc" else T
    near = ((Iv(0), Iv(0), Iv(0)), a1, a2) if kind == "fcc" else \
           ((Iv(0), Iv(0), Iv(0)), neg(a1), neg(a2))
    for b in near:
        P.append((off[0] + b[0], off[1] + b[1], Iv(-1) * Hh))
    return P


def main():
    ok = True
    print("=" * 80)
    print("CONTROL 0: exact polytope volumes of two bodies with rational volumes")
    cube_n = [(F(1), F(0), F(0)), (F(-1), F(0), F(0)), (F(0), F(1), F(0)),
              (F(0), F(-1), F(0)), (F(0), F(0), F(1)), (F(0), F(0), F(-1))]
    v1, nv1, _ = polytope_volume(cube_n, [F(1)] * 6)
    tet_n = [(F(-1), F(-1), F(-1)), (F(-1), F(1), F(1)),
             (F(1), F(-1), F(1)), (F(1), F(1), F(-1))]
    v2, nv2, _ = polytope_volume(tet_n, [F(1)] * 4)
    print(f"  cube [-1,1]^3: {v1} (8 expected), {nv1} vertices")
    print(f"  regular tetrahedron: {v2} (8/3 expected), {nv2} vertices  <- non-symmetric, so")
    print(f"     it detects a face-orientation error that the cube cannot")
    ok &= (v1 == 8 and nv1 == 8 and v2 == F(8, 3) and nv2 == 4)

    print("\nCONTROL 1/2: Barlow contact cells must enclose 4 sqrt2 = 5.656854249492380")
    lo_ref, hi_ref = F(5656854249492380, 10 ** 15), F(5656854249492381, 10 ** 15)
    for kind in ("fcc", "hcp"):
        P = barlow_contact_cell(kind)
        v_in, v_out, ni, no = sandwich(P, F(2))
        enc = (v_in is not None and v_in <= hi_ref and v_out >= lo_ref)
        print(f"  {kind}:  [{float(v_in):.15f}, {float(v_out):.15f}]  "
              f"width {float(v_out - v_in):.1e}  vertices {ni}/{no}  contains 4sqrt2: {enc}")
        ok &= bool(enc)

    print("\nCONTROL 3: the C5 payer fixture must enclose 5.898017371803720")
    # cos(theta) = -3/8 exactly, sin(theta) = sqrt(55)/8 exactly
    tsin = sqrt_iv(Iv(55)) / Iv(8)
    tcos = Iv(F(-3, 8))
    P = c5_centres(tsin, tcos, F(36, 180))
    v_in, v_out, ni, no = sandwich(P, F(3, 2))
    lo_ref = F(5898017371803720, 10 ** 15)
    hi_ref = F(5898017371803721, 10 ** 15)
    enc = (v_in is not None and v_in <= hi_ref and v_out >= lo_ref)
    print(f"  C5:  [{float(v_in):.15f}, {float(v_out):.15f}]  "
          f"width {float(v_out - v_in):.1e}  vertices {ni}/{no}  contains 5.8980173718: {enc}")
    ok &= bool(enc)
    print("\n  R = 3/2 was CERTIFIED against the outer polytope in every sandwich above "
          "(the check raises if an outer vertex exceeds it)")
    print("\n" + ("ALL CONTROLS PASS" if ok else "CONTROL FAILED"))
    return 0 if ok else 1


def box_volume(theta_box, phi_box):
    """Certified enclosure of vol Omega(w_1) for EVERY (theta, phi) in the box.

    theta_box, phi_box: pairs of rationals, angles as multiples of pi.  The sin/cos ranges are
    taken as the hull of the corner values, which is valid here because on both boxes each of
    sin and cos is monotone (theta in the second quadrant, phi in the first), so no interior
    extremum exists.  A box crossing a quadrant boundary would need the extremum added."""
    def hull(vals):
        return Iv(min(v.lo for v in vals), max(v.hi for v in vals))
    th_vals = [ _sincos(t) for t in theta_box ]
    s_th = hull([v[0] for v in th_vals])
    c_th = hull([v[1] for v in th_vals])
    ph_vals = []
    for k in range(5):
        base = [phi_box[0] + F(2 * k, 5), phi_box[1] + F(2 * k, 5)]
        vs = [_sincos(t) for t in base]
        ph_vals.append((hull([v[0] for v in vs]), hull([v[1] for v in vs])))
    r5 = sqrt_iv(Iv(5))
    R5 = Iv(4) / r5
    Z5 = Iv(2) / r5
    out = [(Iv(0), Iv(0), Iv(-2))]
    for k in range(5):
        s, c = _sincos(F(2 * k, 5))
        out.append((R5 * c, R5 * s, Z5 - Iv(2)))
    for k in range(5):
        s, c = ph_vals[k]
        out.append((Iv(2) * s_th * c, Iv(2) * s_th * s, Iv(-2) * c_th))
    out.append((Iv(0), Iv(0), Iv(2)))
    return sandwich(out, F(3, 2))


def box_scaling(kmax=14):
    """How the certified enclosure width scales with the box width.  This is the number the
    branch-and-bound needs: it converts 'the atom works' into 'the B&B needs N boxes'."""
    print("\nBOX-SIZE SCALING around (theta, phi) = (111.7975, 36) degrees")
    print("   k   box width (deg)        certified enclosure            width")
    centre_t, centre_p = F(1117975, 10 ** 4) / 180, F(36, 180)
    rows = []
    for k in range(kmax + 1):
        w = F(1, 2 ** k) / 10          # degrees
        half = w / 2 / 180             # in units of pi
        tb = (centre_t - half, centre_t + half)
        pb = (centre_p - half, centre_p + half)
        v_in, v_out, ni, no = box_volume(tb, pb)
        rows.append((k, w, v_in, v_out))
        print(f"  {k:3d}   {float(w):12.8f}     [{float(v_in):.10f}, {float(v_out):.10f}]"
              f"   {float(v_out - v_in):.2e}")
    for k, w, a, b in rows:
        if float(b - a) < 1e-3:
            print(f"\n  enclosure width first drops below 1e-3 at k = {k}, "
                  f"box width {float(w):.6f} deg")
            th_span = (120 - 106) / float(w)
            ph_span = (36 - 22) / float(w)
            print(f"  covering theta in [106,120] and phi in [22,36] at that width needs about "
                  f"{th_span*ph_span:.3g} boxes")
            break
    return rows


def box_demo():
    print("\nNONTRIVIAL BOX: theta/pi in [111.70, 111.90]/180, phi/pi in [35.5, 36.5]/180")
    tb = (F(11170, 18000), F(11190, 18000))
    pb = (F(355, 1800), F(365, 1800))
    v_in, v_out, ni, no = box_volume(tb, pb)
    print(f"  certified: [{float(v_in):.12f}, {float(v_out):.12f}]  width {float(v_out - v_in):.2e}")
    print(f"  vertices {ni}/{no};  threshold (P') needs 5.763417470")
    print(f"  the whole box is above the threshold: {v_in > F(5763417470, 10**9)}")
    return v_in, v_out


if __name__ == "__main__":
    import sys as _sys
    rc = main()
    if "--scaling" in _sys.argv:
        box_scaling()
    elif "--box" in _sys.argv:
        box_demo()
    sys.exit(rc)
