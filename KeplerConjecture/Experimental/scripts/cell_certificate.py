#!/usr/bin/env python3
"""
REPAIRED small verifier: a sound two-sided enclosure of a Voronoi-cell volume.

This replaces `rigorous_cell_volume.sandwich`, which had two defects found in review 0608
and confirmed here as regression witnesses (§W1, §W2 below):

  BUG 1 (norm mismatch).  `e` was the max COMPONENT half-width of the normal, i.e. an
  infinity-norm bound, but the slack used `R*e` with R a Euclidean radius.  For a 3-vector
  |dn|_2 <= sqrt(3)|dn|_inf, so the slack was short by up to a factor sqrt(3) and the
  "certified" enclosure need not contain the true volume.  Witness W1 is exact.

  BUG 2 (boundedness).  Boundedness was inferred from "max|vertex| <= R" over the enumerated
  vertices.  An unbounded polyhedron can have vertices -- {|x|<=1,|y|<=1,z>=-1} has exactly
  four -- so the check proved nothing, and the code returned a finite volume (4/3) for an
  infinite one.  Witness W2.

The repair, and why it is not circular.

  Notation: the cell is Omega = B(0,2) cap {y.n_i <= b_i}, with n_i unit and b_i = |v_i|/2.
  The data are known only through intervals: n_i in a box of component half-width e_i about
  n_i', b_i in [b_i'-f_i, b_i'+f_i], with n_i', b_i' RATIONAL.

  (1) SLACK.  For |y| <= R,  |y.(n_i-n_i')| <= |y|_2 |n_i-n_i'|_2 <= R sqrt(3) e_i.  So

          Omega ∩ B(0,R)  subset  { y.n_i' <= b_i' + R sqrt(3) e_i + f_i }  =:  Out
          { y.n_i' <= b_i' - R sqrt(3) e_i - f_i }  =:  Inn  subset  Omega ∩ B(0,R)

      using sqrt(3) <= 7/4 (rational, so every number below is a Fraction).

  (2) A PRIORI RADIUS, independent of the sandwich.  Let c = min_{|u|=1} max_i u.n_i'.
      If y in Omega and r = |y|, put u = y/r; pick i with u.n_i' >= c.  Then
          r c  <=  r (u.n_i')  =  y.n_i'  <=  b_i' + r sqrt(3) e_i
      so r (c - sqrt(3) e_max) <= b_max and  R0 := b_max / (c - sqrt(3) e_max)  bounds |y|.
      c is computed as a rigorous LOWER bound by meshing the sphere: max_i u.n_i is
      1-Lipschitz in u, so its minimum over the sphere is at least (min over mesh vertices)
      minus the mesh diameter.  This uses no volume and no vertex enumeration: no circularity.

  (3) BOUNDEDNESS, exactly.  Out is bounded iff 0 is in the interior of conv{n_i'}.  Decided
      by exhibiting four indices with a strictly positive dependence sum_m lambda_m n_m' = 0
      (the null vector of the 3x4 matrix, computed by cofactors).  If no such four exist the
      certificate REFUSES.

  (4) CONSISTENCY.  Finally check every vertex of Out satisfies |y| <= R (with R = R0 rounded
      up).  Since Inn subset Out and Out subset B(0,R), every y in Inn also has |y| <= R, so
      step (1) applies to Inn as needed -- the two inclusions stand together.

Run:  python3 Experimental/scripts/cell_certificate.py       (exit 0 iff every check passes)
"""
import itertools
import json
import sys
from fractions import Fraction as F

sys.set_int_max_str_digits(0)

from rational_interval import Iv, sqrt_iv, sin_cos_iv_of_pi_multiple

SQRT3_UB = F(7, 4)          # a rational upper bound for sqrt(3)
CERT_DIGITS = 40
SLACK_DIGITS = 30           # slacks are rounded UP to this many decimals


def round_up(fr, digits=SLACK_DIGITS):
    """Round a positive Fraction UP to `digits` decimals.

    PERFORMANCE FIX from review 2026-11-14_0738: the interval widths e_i, f_i are tiny but
    carry the enormous denominators of the transcendental chain (measured: numerators of
    25 000 bits), and every later Fraction inherits them -- one C5 certification took 116 s
    instead of 9 s.  Rounding the slack UP keeps it an upper bound and costs nothing."""
    q = F(10) ** digits
    n = fr * q
    return F(-((-n.numerator) // n.denominator), q)


def outward(fr, up):
    """Round a Fraction OUTWARD to CERT_DIGITS decimals: compact to print, still rigorous."""
    q = F(10) ** CERT_DIGITS
    n = fr * q
    k = -((-n.numerator) // n.denominator) if up else (n.numerator // n.denominator)
    return F(k, q)
DEN = 10 ** 20
QERR = F(1, 10 ** 20)


# ---------------------------------------------------------------- exact linear algebra
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


def origin_interior_certificate(normals):
    """Exact certificate that 0 lies in the INTERIOR of conv{normals}.

    Supporting planes: for every triple of normals that is AFFINELY INDEPENDENT and whose
    plane has all the other normals on one side, that plane supports the hull, and 0 must
    lie strictly on the hull's side of it.

    DEFECT FOUND IN REVIEW 0653 AND REPAIRED HERE.  The first version used the normal
    cross(b, c) -- the normal of the plane through 0, b, c -- instead of
    cross(b - a, c - a), the normal of the plane through a, b, c.  On the input
    [(1,0,0),(0,1,0),(0,0,1)], whose points all satisfy x+y+z = 1 so that the origin is
    plainly outside, it returned (True, 1, 1): a false certificate.  Two things were wrong:
    the normal, and the absence of any affine-independence check.  Witness W3 keeps the
    exact input.

    Returns (True, margin, n_supporting) or (False, reason, n_supporting)."""
    N = len(normals)
    # FULL AFFINE DIMENSION first: a point set in a plane has no interior in R^3 at all, and
    # the supporting-plane test below would divide by a vanishing normal (review 0653).
    if not _affine_dim_3(normals):
        return False, "the normals span less than 3 dimensions: no interior in R^3", 0
    best = None
    nsup = 0
    for i, j, k in itertools.combinations(range(N), 3):
        a, b, c = normals[i], normals[j], normals[k]
        ba = tuple(b[t] - a[t] for t in range(3))
        ca = tuple(c[t] - a[t] for t in range(3))
        nrm = (ba[1] * ca[2] - ba[2] * ca[1],
               ba[2] * ca[0] - ba[0] * ca[2],
               ba[0] * ca[1] - ba[1] * ca[0])
        if nrm == (0, 0, 0):
            continue                      # collinear triple: no plane (affine dimension < 2)
        nn = sum(nrm[t] * a[t] for t in range(3))
        vals = [sum(nrm[t] * p[t] for t in range(3)) - nn for p in normals]
        if all(v <= 0 for v in vals):
            side = -1
        elif all(v >= 0 for v in vals):
            side = 1
        else:
            continue
        nsup += 1
        z = -nn                            # the plane's value at the origin
        margin = side * z
        if margin <= 0:
            return False, "the origin is on or outside a supporting plane", nsup
        best = margin if best is None else min(best, margin)
    if best is None:
        return False, "no supporting plane found (affine dimension < 3)", 0
    return True, best, nsup


def _affine_dim_3(pts):
    """True iff the points affinely span R^3 (some four are affinely independent)."""
    base = pts[0]
    for i, j, k in itertools.combinations(range(1, len(pts)), 3):
        v = [tuple(pts[t][r] - base[r] for r in range(3)) for t in (i, j, k)]
        cr = (v[1][1] * v[2][2] - v[1][2] * v[2][1],
              v[1][2] * v[2][0] - v[1][0] * v[2][2],
              v[1][0] * v[2][1] - v[1][1] * v[2][0])
        if sum(x * x for x in cr) != 0 and (v[0][0] * cr[0] + v[0][1] * cr[1] + v[0][2] * cr[2]) != 0:
            return True
    return False


def radius_witness(normals):
    """EXACT lower bound for min_{|u|=1} max_i u.n_i, from the inradius of conv{normals}.

    No sphere mesh, no floating point, no unproved epsilon.  If B(0,r) is contained in
    conv{n_i} then every unit u has max_i u.n_i >= r (r u lies in the hull, and
    r = u.(r u) = sum lambda_i (u.n_i) <= max_i u.n_i).  And conv{n_i} is contained in each
    supporting half-space {p : m.p <= k}, so B(0,r) is contained in the hull as soon as
    r <= dist(0, that plane) for EVERY supporting plane.  Hence

        c  >=  min over supporting planes of |k| / |m| ,

    which is exactly the inradius of the hull about the origin.  (A first attempt looked for a
    tetrahedron with vertices among the n_i containing 0; that fails on the cube, whose six
    normals admit no such four -- 0 is interior to the octahedron but in no inscribed
    tetrahedron.)

    Returns (c_lower, n_supporting, witness) or (0, 0, None)."""
    inside, margin, nsup = origin_interior_certificate(normals)
    if not inside:
        return F(0), nsup, None
    best = None
    wit = None
    N = len(normals)
    for i, j, k in itertools.combinations(range(N), 3):
        a, b, c = normals[i], normals[j], normals[k]
        ba = tuple(b[t] - a[t] for t in range(3))
        ca = tuple(c[t] - a[t] for t in range(3))
        nrm = (ba[1] * ca[2] - ba[2] * ca[1],
               ba[2] * ca[0] - ba[0] * ca[2],
               ba[0] * ca[1] - ba[1] * ca[0])
        if nrm == (0, 0, 0):
            continue
        nn = sum(nrm[t] * a[t] for t in range(3))
        vals = [sum(nrm[t] * p[t] for t in range(3)) - nn for p in normals]
        if not (all(v <= 0 for v in vals) or all(v >= 0 for v in vals)):
            continue
        n2 = sum(x * x for x in nrm)
        d = Iv(abs(nn)) / sqrt_iv(Iv(n2))
        if best is None or d.lo < best:
            best = d.lo
            wit = (i, j, k)
    if best is None:
        return F(0), nsup, None
    return best, nsup, wit


def _cross(u, v):
    return (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])


def _dot(u, v):
    return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]


def canonicalise(normals, dists):
    """Reduce a plane set to pairwise NON-PROPORTIONAL half-spaces, keeping the tightest.

    DEFECT FOUND IN REVIEW 2026-11-14_0738 AND REPAIRED HERE.  `polytope_volume` summed
    d_i A_i / 3 over the planes as given, so a plane listed twice counted its facet twice.
    Witness W5: the six cube normals with offsets 1 give 8, but appending a duplicate of
    (e1, 1) returned 28/3 -- an excess of exactly d A / 3 = 4/3, the doubled face.

    The half-space {y.n <= d} with d > 0 is {y.u <= 1} with u = n/d, so two planes are the
    same half-space iff their u agree, and one implies the other iff they are on the same ray
    and one has the larger |u| (a larger |u| is a tighter constraint).  This function returns
    one (u, 1) per surviving ray, keeping the largest |u| in each ray and breaking ties by
    index, so the polytope is unchanged and every facet has exactly one plane."""
    if len(normals) != len(dists):
        raise ValueError("normals and dists must have equal length")
    planes = []
    for n, d in zip(normals, dists):
        if d <= 0:
            raise ValueError("offsets must be positive (the origin must be interior)")
        planes.append(tuple(F(x) / F(d) for x in n))
    n2 = [_dot(u, u) for u in planes]
    for i, u in enumerate(planes):
        if n2[i] == 0:
            raise ValueError("zero normal")
    keep = []
    for i, u in enumerate(planes):
        dominated = False
        for j, v in enumerate(planes):
            if i == j:
                continue
            if _cross(u, v) == (0, 0, 0) and _dot(u, v) > 0:
                if n2[j] > n2[i] or (n2[j] == n2[i] and j < i):
                    dominated = True
                    break
        if not dominated:
            keep.append(i)
    return [planes[i] for i in keep], [F(1)] * len(keep)


def polytope_volume(normals, dists, require_bounded=True):
    """Exact volume of {y : y.n_i <= d_i}.  REFUSES an unbounded polyhedron.

    SUPPORTED INPUT DOMAIN (documented after review 2026-11-14_0738): normals nonzero,
    offsets d_i > 0 (the origin is interior), the set positively spanning so the polytope is
    bounded, and -- after `canonicalise`, which is applied here -- no two half-spaces
    proportional.  Duplicate or dominated planes are accepted and reduced."""
    normals, dists = canonicalise(normals, dists)
    inside, margin, nsup = origin_interior_certificate(normals)
    if not inside:
        if require_bounded:
            raise Unbounded(f"0 is not in the interior of conv(n_i) "
                            f"(supporting planes checked: {nsup}, margin {margin})")
        return None, 0, []
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
        on = [x for x in verts if sum(normals[i][t] * x[t] for t in range(3)) == dists[i]]
        if len(on) >= 3:
            cyc = _cyclic_order(normals[i], on)
            for t in range(1, len(cyc) - 1):
                total += det3([cyc[0], cyc[t], cyc[t + 1]])
    return abs(total) / 6, len(verts), verts


class Unbounded(Exception):
    pass


def _cyclic_order(normal, pts):
    n = normal
    nn = n[0] * n[0] + n[1] * n[1] + n[2] * n[2]
    ax = min(range(3), key=lambda t: abs(n[t]))
    e1 = [F(0), F(0), F(0)]
    e1[ax] = F(1)
    d = sum(e1[t] * n[t] for t in range(3))
    e1 = [e1[t] - n[t] * d / nn for t in range(3)]
    e2 = [n[1] * e1[2] - n[2] * e1[1], n[2] * e1[0] - n[0] * e1[2], n[0] * e1[1] - n[1] * e1[0]]
    P = [(sum(x[t] * e1[t] for t in range(3)), sum(x[t] * e2[t] for t in range(3))) for x in pts]
    cx = sum(p[0] for p in P) / len(P)
    cy = sum(p[1] for p in P) / len(P)
    R = [(p[0] - cx, p[1] - cy) for p in P]

    def half(p):
        x, y = p
        return 0 if (x > 0 and y >= 0) else 1 if (x <= 0 and y > 0) else 2 if (x < 0 and y <= 0) else 3

    from functools import cmp_to_key

    def cmp(p, q):
        if half(p) != half(q):
            return -1 if half(p) < half(q) else 1
        cr = p[0] * q[1] - p[1] * q[0]
        return -1 if cr > 0 else (1 if cr < 0 else 0)

    order = sorted(range(len(R)), key=cmp_to_key(lambda a, b: cmp(R[a], R[b])))
    return [pts[t] for t in order]


# ---------------------------------------------------------------- sphere mesh for c
def sphere_mesh(subdiv=5):
    phi = (1 + 5 ** 0.5) / 2
    raw = []
    for a in (1, -1):
        for b in (1, -1):
            raw += [(0, a, b * phi), (a, b * phi, 0), (a * phi, 0, b)]
    import numpy as np
    V = np.array(raw, float)
    V /= np.linalg.norm(V, axis=1)[:, None]
    F_ = []
    for i in range(12):
        for j in range(i + 1, 12):
            if abs(np.dot(V[i], V[j]) - 1 / np.sqrt(5)) < 1e-9:
                for k in range(j + 1, 12):
                    if (abs(np.dot(V[i], V[k]) - 1 / np.sqrt(5)) < 1e-9
                            and abs(np.dot(V[j], V[k]) - 1 / np.sqrt(5)) < 1e-9):
                        F_.append((i, j, k))
    for _ in range(subdiv):
        cache = {}
        V_list = list(V)

        def mid(i, j):
            key = (min(i, j), max(i, j))
            if key not in cache:
                m = V_list[i] + V_list[j]
                V_list.append(m / np.linalg.norm(m))
                cache[key] = len(V_list) - 1
            return cache[key]

        nf = []
        for (i, j, k) in F_:
            a, b, c = mid(i, j), mid(j, k), mid(k, i)
            nf += [(i, a, c), (j, b, a), (k, c, b), (a, b, c)]
        V = np.array(V_list)
        F_ = nf
    E = set()
    for (i, j, k) in F_:
        E.add((min(i, j), max(i, j)))
        E.add((min(j, k), max(j, k)))
        E.add((min(i, k), max(i, k)))
    import numpy as np
    diam = max(np.linalg.norm(V[i] - V[j]) for (i, j) in E)
    return V, float(diam)


def spanning_constant(normals_rat, mesh, diam):
    """Rigorous lower bound for min_{|u|=1} max_i u.n_i (normals rational)."""
    import numpy as np
    A = np.array([[float(x) for x in n] for n in normals_rat])
    V, _ = mesh
    vals = (V @ A.T).max(axis=1)          # max_i u.n_i at each mesh vertex
    return F(vals.min()) - F(diam) - F(1, 10 ** 9)


# ---------------------------------------------------------------- the repaired sandwich
def certify(centres, name="", verbose=False):
    """(lo, hi, certificate) for Omega(origin) cut by `centres` (interval vectors)."""
    n_rat, b_rat, e_i, f_i = [], [], [], []
    for p in centres:
        sq = p[0] * p[0] + p[1] * p[1] + p[2] * p[2]
        L = sqrt_iv(sq)
        n = [p[t] / L for t in range(3)]
        b = L / 2
        eq = max((x.hi - x.lo) / 2 for x in n) + QERR
        fq = (b.hi - b.lo) / 2 + QERR
        n_rat.append([F(int(x.mid() * DEN + (F(1, 2) if x.mid() >= 0 else F(-1, 2))), DEN)
                      for x in n])
        b_rat.append(F(int(b.mid() * DEN + (F(1, 2) if b.mid() >= 0 else F(-1, 2))), DEN))
        e_i.append(eq)
        f_i.append(fq)
    b_max = max(b_rat[i] + f_i[i] for i in range(len(b_rat)))
    # EXACT radius witness: the inradius of conv{n_i} about the origin.  No sphere mesh, no
    # floating point, no unproved 1e-9 subtraction (review 0653).
    c, nsup, cwit = radius_witness(n_rat)
    denom = c - SQRT3_UB * max(e_i)
    if denom <= 0:
        raise Unbounded("the a priori radius bound fails: c <= sqrt3 e_max")
    R = b_max / denom
    R = F(int(R * 1000) + 2, 1000)          # round up, generously
    slack = [round_up(R * SQRT3_UB * e_i[i] + f_i[i]) for i in range(len(e_i))]
    inn = [b_rat[i] - slack[i] for i in range(len(b_rat))]
    out = [b_rat[i] + slack[i] for i in range(len(b_rat))]
    v_out, nvo, vout_pts = polytope_volume(n_rat, out)          # raises if unbounded
    v_in, nvi, vin_pts = polytope_volume(n_rat, inn)
    if v_in is None:
        v_in = F(0)
    # consistency: Out must lie in B(0,R)
    rmax2 = max(sum(x[t] * x[t] for t in range(3)) for x in vout_pts)
    if rmax2 > R * R:
        raise Unbounded(f"Out is not inside B(0,R): a vertex has |y|^2 = {float(rmax2)} > R^2")
    inside, marg, nsup = origin_interior_certificate(n_rat)
    cert = dict(
        name=name,
        R=str(outward(R, True)),
        spanning_constant=str(outward(c, False)),
        boundedness=dict(origin_interior=inside, supporting_planes=nsup,
                         margin=str(outward(marg, False))),
        n_vertices_outer=nvo,
        rmax_sq=str(outward(rmax2, True)),
        slack_max=str(outward(max(slack), True)),
        vol_lo=str(outward(v_in, False)),
        vol_hi=str(outward(v_out, True)),
        exact_lo=str(v_in) if v_in.denominator.bit_length() < 4000 else "(omitted: too long)",
        exact_hi=str(v_out) if v_out.denominator.bit_length() < 4000 else "(omitted: too long)",
        note="lo rounded DOWN and hi rounded UP to %d decimals; the enclosure is still rigorous"
             % CERT_DIGITS,
    )
    if verbose:
        print(f"    R = {float(R):.6f}  c = {float(c):.6f}  slack_max = {float(max(slack)):.3e}"
              f"  vertices {nvo}")
    return v_in, v_out, cert


# ---------------------------------------------------------------- witnesses and controls
def witness_1():
    """The norm mismatch: |y.dn| can exceed R * (max component of dn)."""
    y = (F(-4, 9), F(8, 9), F(0))
    n0 = (F(1), F(0), F(0))
    n = (F(3, 5), F(4, 5), F(0))
    dn = tuple(n[t] - n0[t] for t in range(3))
    e = max(abs(x) for x in dn)
    R = F(1)
    y2 = sum(x * x for x in y)
    dot = sum(y[t] * dn[t] for t in range(3))
    dn2 = sum(x * x for x in dn)
    out = dict(y_sq=str(y2), R_sq=str(R * R), e=str(e), y_dot_dn=str(dot),
               dn_sq=str(dn2), ratio=str(dot / (R * e)))
    ok = (y2 <= R * R) and (dot > R * e) and (dn2 <= 3 * e * e) and (dot <= R * (3 * e * e) ** F(1, 2) + F(1, 100))
    return ok, out


def witness_2():
    """An unbounded polyhedron with four vertices: the old code returned 4/3."""
    normals = [(F(1), F(0), F(0)), (F(-1), F(0), F(0)), (F(0), F(1), F(0)),
               (F(0), F(-1), F(0)), (F(0), F(0), F(-1))]
    try:
        polytope_volume(normals, [F(1)] * 5)
        return False, dict(refused=False)
    except Unbounded as e:
        return True, dict(refused=True, reason=str(e))


def main():
    ok = True
    print("=" * 80)
    print("REGRESSION WITNESSES for the two defects of review 0608")
    good, det = witness_1()
    print(f"  W1 norm mismatch: y.dn = {det['y_dot_dn']} vs R*e = {det['e']}, "
          f"|dn|^2 = {det['dn_sq']}")
    print(f"     ratio {float(F(det['ratio'])):.6f} > 1  -> the infinity-norm slack is short: {good}")
    ok &= good
    good, det = witness_2()
    print(f"  W2 unbounded polytope with four vertices refused: {good}  ({det.get('reason','')})")
    ok &= good

    # ---- W3: the false certificate found in review 0653 -------------------
    flat = [(F(1), F(0), F(0)), (F(0), F(1), F(0)), (F(0), F(0), F(1))]
    res = origin_interior_certificate(flat)
    good = (res[0] is False)
    print(f"  W3 coplanar normals refused: {good}  -> {res[1]}")
    print(f"     (the first version returned (True, 1, 1) here, using cross(b,c) instead of")
    print(f"      cross(b-a,c-a) and never checking affine dimension)")
    ok &= good

    # ---- W4: exact radius witness, no mesh -------------------------------
    cube_n = [(F(1), F(0), F(0)), (F(-1), F(0), F(0)), (F(0), F(1), F(0)),
              (F(0), F(-1), F(0)), (F(0), F(0), F(1)), (F(0), F(0), F(-1))]
    c, nsup, wit = radius_witness(cube_n)
    # 1/sqrt(3) enclosed
    lower3 = sqrt_iv(Iv(3)).lo
    good = (abs(c - 1 / lower3) < F(1, 10 ** 12)) if False else (abs(c - (F(1) / sqrt_iv(Iv(3)).lo)) < F(1, 10 ** 15) * 10)
    print(f"  W4 exact radius on the cube's normals: c = {float(c):.12f}  "
          f"(1/sqrt3 = {float(F(1)/sqrt_iv(Iv(3)).lo):.12f}), {nsup} supporting planes")
    ok &= abs(c - F(1) / sqrt_iv(Iv(3)).lo) < F(1, 10 ** 12)

    # ---- W5: duplicate and proportional supporting planes -----------------
    print("\nW5 DUPLICATE / PROPORTIONAL PLANES (defect of review 2026-11-14_0738)")
    cube6 = [(F(1), F(0), F(0)), (F(-1), F(0), F(0)), (F(0), F(1), F(0)),
             (F(0), F(-1), F(0)), (F(0), F(0), F(1)), (F(0), F(0), F(-1))]
    one6 = [F(1)] * 6
    dup_tests = [
        ("cube", cube6, one6, F(8)),
        ("+ duplicate e1", cube6 + [(F(1), F(0), F(0))], one6 + [F(1)], F(8)),
        ("+ duplicate -e2", cube6 + [(F(0), F(-1), F(0))], one6 + [F(1)], F(8)),
        ("+ duplicate e1 twice", cube6 + [(F(1), F(0), F(0))] * 2, one6 + [F(1)] * 2, F(8)),
        ("+ 2e1 at offset 1 (y1<=1/2)", cube6 + [(F(2), F(0), F(0))], one6 + [F(1)], F(6)),
        ("+ e1 at offset 2 (redundant)", cube6 + [(F(1), F(0), F(0))], one6 + [F(2)], F(8)),
        ("+ e1 at offset 1/2 (y1<=1/2)", cube6 + [(F(1), F(0), F(0))], one6 + [F(1, 2)], F(6)),
    ]
    for name, nn, dd, exp in dup_tests:
        got = polytope_volume(nn, dd)[0]
        good = (got == exp)
        print(f"  {name:32s} -> {str(got):>4s}  expected {str(exp):>4s}  {'OK' if good else 'WRONG'}")
        ok &= good
    print(f"     (the first version returned 28/3 for the duplicate case: the doubled face")
    print(f"      contributed d*A/3 = 4/3 twice)")

    # ---- the volume contract ---------------------------------------------
    print("\nVOLUME CONTRACT: bodies with known volumes, and a degenerate one")
    oct_n = [(F(a), F(b), F(cc)) for a in (1, -1) for b in (1, -1) for cc in (1, -1)]
    v, nv, _ = polytope_volume(oct_n, [F(1)] * 8)
    print(f"  octahedron |x|+|y|+|z| <= 1: {v}  (4/3 expected), {nv} vertices")
    ok &= (v == F(4, 3) and nv == 6)
    box = [(F(1), F(0), F(0)), (F(-1), F(0), F(0)), (F(0), F(1), F(0)),
           (F(0), F(-1), F(0)), (F(0), F(0), F(1)), (F(0), F(0), F(-1))]
    v, nv, _ = polytope_volume(box, [F(1), F(1), F(3, 2), F(3, 2), F(2), F(2)])
    print(f"  box 2 x 3 x 4: {v}  (24 expected), {nv} vertices")
    ok &= (v == 24 and nv == 8)
    try:
        polytope_volume([(F(1), F(0), F(0)), (F(0), F(1), F(0)), (F(1), F(1), F(0))], [F(1)] * 3)
        print("  degenerate (coplanar normals): NOT REFUSED  <- BUG")
        ok = False
    except Unbounded:
        print("  degenerate (coplanar normals): refused")

    print("\nCONTROLS (the same five as before, now with the repaired slack)")
    import numpy as np
    refs = {}
    # cube
    cube = [(F(1), F(0), F(0)), (F(-1), F(0), F(0)), (F(0), F(1), F(0)),
            (F(0), F(-1), F(0)), (F(0), F(0), F(1)), (F(0), F(0), F(-1))]
    v, nv, _ = polytope_volume(cube, [F(1)] * 6)
    print(f"  cube: {v} (8 expected), {nv} vertices")
    ok &= (v == 8 and nv == 8)
    tet = [(F(-1), F(-1), F(-1)), (F(-1), F(1), F(1)), (F(1), F(-1), F(1)), (F(1), F(1), F(-1))]
    v, nv, _ = polytope_volume(tet, [F(1)] * 4)
    print(f"  tetrahedron: {v} (8/3 expected), {nv} vertices")
    ok &= (v == F(8, 3) and nv == 4)

    for kind, hi, lo in ((fcc_key(), None, None),):
        pass
    lo_ref, hi_ref = F(5656854249492380000, 10 ** 18), F(5656854249492380500, 10 ** 18)
    for kind in ("fcc", "hcp"):
        P = barlow_contact_cell(kind)
        a, b, cert = certify(P, kind)
        enc = a <= hi_ref and b >= lo_ref
        print(f"  {kind}: [{float(a):.15f}, {float(b):.15f}] width {float(b-a):.1e} "
              f"contains 4sqrt2: {enc}")
        ok &= enc
    tsin = sqrt_iv(Iv(55)) / Iv(8)
    tcos = Iv(F(-3, 8))
    P = c5_centres(tsin, tcos, F(36, 180))
    a, b, cert = certify(P, "C5")
    lo5, hi5 = F(5898017371803720, 10 ** 15), F(5898017371803721, 10 ** 15)
    enc = a <= hi5 and b >= lo5
    print(f"  C5: [{float(a):.15f}, {float(b):.15f}] width {float(b-a):.1e} "
          f"contains 5.8980173718: {enc}")
    ok &= enc
    print("\n" + ("ALL CHECKS PASS" if ok else "FAILED"))
    return 0 if ok else 1


def fcc_key():
    return "fcc"


def _sincos(mult):
    return sin_cos_iv_of_pi_multiple(mult, terms=24, pi_terms=32)


def c5_centres(theta_sin, theta_cos, phi_multiple):
    r5 = sqrt_iv(Iv(5))
    R5 = Iv(4) / r5
    Z5 = Iv(2) / r5
    out = [(Iv(0), Iv(0), Iv(-2))]
    for k in range(5):
        s, c = _sincos(F(2 * k, 5))
        out.append((R5 * c, R5 * s, Z5 - Iv(2)))
    for k in range(5):
        s, c = _sincos(phi_multiple + F(2 * k, 5))
        out.append((Iv(2) * theta_sin * c, Iv(2) * theta_sin * s, Iv(-2) * theta_cos))
    out.append((Iv(0), Iv(0), Iv(2)))
    return out


def _range_of(lo, hi, idx):
    """Range of sin (idx=0) / cos (idx=1) over [lo,hi], EXACTLY: endpoints plus any
    quarter-turn stationary point inside, so no monotonicity assumption is made."""
    pts = [lo, hi]
    k = -40
    while k * F(1, 2) <= hi:
        q = k * F(1, 2)
        if lo <= q <= hi:
            pts.append(q)
        k += 1
    vs = [_sincos(t)[idx] for t in pts]
    return Iv(min(v.lo for v in vs), max(v.hi for v in vs))


def c5_centres_box(th_lo, th_hi, ph_lo, ph_hi):
    """The C5 fixture's twelve centres as intervals valid for EVERY (theta,phi) in the box.
    Angles are in units of pi."""
    r5 = sqrt_iv(Iv(5))
    R5 = Iv(4) / r5
    Z5 = Iv(2) / r5
    s_th = _range_of(th_lo, th_hi, 0)
    c_th = _range_of(th_lo, th_hi, 1)
    out = [(Iv(0), Iv(0), Iv(-2))]
    for k in range(5):
        s, c = _sincos(F(2 * k, 5))
        out.append((R5 * c, R5 * s, Z5 - Iv(2)))
    for k in range(5):
        lo = ph_lo + F(2 * k, 5)
        hi = ph_hi + F(2 * k, 5)
        s = _range_of(lo, hi, 0)
        c = _range_of(lo, hi, 1)
        out.append((Iv(2) * s_th * c, Iv(2) * s_th * s, Iv(-2) * c_th))
    out.append((Iv(0), Iv(0), Iv(2)))
    return out


def barlow_contact_cell(kind):
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


if __name__ == "__main__":
    sys.exit(main())
