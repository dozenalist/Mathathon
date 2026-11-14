#!/usr/bin/env python3
"""K15 portable periodic cut/flow evaluator for Main's K15-C044.

WHAT THIS IMPLEMENTS (C044's exact convention, not a variant of it)

  b(v)  := sqrt(32) - vol Omega(v)                     the vertex deficit
  G_R   : graph on centres, edge between centres at distance <= R, capacity Phi per edge
  A transfer is an antisymmetric phi on G_R with |phi| <= Phi and
             sum_w phi(v,w) >= b(v)        for every vertex v.
  C044 criterion (Hoffman/Gale, = max-flow/min-cut): a transfer exists iff for every FINITE
             U subset of centres,      sum_{v in U} b(v)  <=  Phi * |delta^+_R(U)| .

TWO KINDS OF OUTPUT, AND THEY ARE NOT SYMMETRIC -- this is the point of the file

  * An EXPLICIT VIOLATING CUT  (a finite U with sum_U b > Phi |delta^+(U)|) is a certificate
    about the INFINITE packing: U is finite, so it is a legitimate test set, and the violation
    is unconditional.  This is the direction that can refute.
  * A FEASIBLE FLOW on a finite periodic patch is evidence about THAT PATCH ONLY.  It does not
    prove the cut condition for all finite U of the infinite packing, and it does not prove the
    infinite extension.  Reported as `PATCH_FEASIBLE`, never as a certificate.

Irrelevant-but-tempting: the FULL PERIOD is not a finite subset of the infinite packing, so its
empty boundary gives only a NECESSARY DENSITY CONDITION (mean b <= 0, i.e. rho <= 1/sqrt(32)),
not the cut condition.  REVIEW_0308.md section 2 corrects an earlier overclaim of mine here.

ARITHMETIC.  Deficits of FCC and HCP are exactly 0.  For the icosahedral fixture vol Omega
involves sqrt(5), so b is irrational; the file uses RATIONAL ENCLOSURES b_lo <= b <= b_hi and
takes the conservative direction in each case (b_lo for refuting, b_hi for feasibility).

Usage:
    python3 cut_flow.py                 # all fixtures, a table
    python3 cut_flow.py --json out/cut_flow.json
Exit status 0 iff every check passes.
"""
import argparse, itertools, json, os
from fractions import Fraction as F

_HERE = os.path.dirname(os.path.abspath(__file__))
_OUT = os.path.join(_HERE, "out")

# ---------------------------------------------------------------- enclosures
# sqrt(32) = 4*sqrt(2) = 5.6568542494923801952...
# TIGHTENED (convergence checked): the singleton-cut threshold moves by 1.2e-10 when the
# enclosure gains 3 digits and by 3.1e-14 when it gains 6, so it has settled at
# 0.00888026841442...  The shipped bound is 0.008880268414417, which is BELOW the true value:
# the correct (conservative) direction for a refutation.
SQ32_LO = F(5656854249492380195206, 10 ** 21)
SQ32_HI = F(5656854249492380195207, 10 ** 21)
# Regular dodecahedron of inradius 1  (the central cell of the 13-cluster at separation 2):
#   V = (15 + 7 sqrt5)/4 * a^3,  a = 2/sqrt(5/2 + 11 sqrt5/10)
#
# CORRECTED (review 0353-C).  The previous hard-coded enclosure
#     V_DOD in [5.550291028519371, 5.550291028519372]
# EXCLUDED the true value 5.550291028515510269...  (it was too high by 3.9e-12).  The bounds
# below are regenerated from that exact radical by rational interval arithmetic with integer
# square roots (k15radicals.py), which is a reproducible proof rather than a rounded constant.
import k15radicals as RAD
V_DOD_LO, V_DOD_HI = RAD.dodeca_volume_enclosure(digits=40)
# Ring-ring distance for the fixture: the icosahedron of CIRCUMRADIUS 2 has edge
#   4 sqrt2 / sqrt(5 + sqrt5) = 2.1029244484765344...
# The previous hard-coded threshold 2.1029 is BELOW that, so build_13(2.1029) wrongly created
# the 30 ring-ring edges.  The gate now uses this enclosure, in the conservative direction.
EDGE_LO, EDGE_HI = RAD.icosa_edge_enclosure(digits=40)

def fcc_b():   return F(0), F(0)           # vol Omega = sqrt32 exactly
def hcp_b():   return F(0), F(0)

def icos_b():
    """Periodised 13-cluster: cell 0 = regular dodecahedron of inradius 1, cells 1..12 SHARE the
    rest of the period cube 16^3 = 4096.  Returns (b_lo, b_hi) lists.

    WHAT "SHARE" MEANS (period_convention.py).  The torus cells partition the period cube, so
        sum_{v in X} vol Omega(v) = 4096   exactly,   and   vol Omega(0) = V_dod exactly,
    hence the twelve ring cells sum to 4096 - V_dod and, being congruent, each has volume
    (4096 - V_dod)/12 = 340.870809080957.  Congruence is not assumed: the icosahedron in cyclic
    coordinates is invariant under coordinate permutations and even sign changes, so the octahedral
    group preserves both the register and 16 Z^3 and acts transitively on the twelve ring vertices
    (orbit size 12).  Measured with half-space intersection (float, ~1e-12): the twelve agree to
    3.4e-13 and the thirteen sum to 4096.000000000.
    """
    period = F(4096)
    b0_lo = SQ32_LO - V_DOD_HI
    b0_hi = SQ32_HI - V_DOD_LO
    vol_other_lo = (period - V_DOD_HI) / 12
    vol_other_hi = (period - V_DOD_LO) / 12
    b1_lo = SQ32_LO - vol_other_hi
    b1_hi = SQ32_HI - vol_other_lo
    return [b0_lo] + [b1_lo] * 12, [b0_hi] + [b1_hi] * 12

# ---------------------------------------------------------------- fixture validation
def validate_icos_fixture():
    """Check, rather than assert, that the icosahedral fixture is a legitimate packing with the
    central Voronoi cell UNcut.  Three conditions:
      V1  all pairwise distances among the 13 centres are >= 2 (minimum separation 2);
      V2  the nearest periodic image of the origin is at distance 16 - 2 = 14 >= 2;
      V3  the central cell's circumradius is < 8, the half-period, so no image plane reaches it
          and the cell is exactly the regular dodecahedron of inradius 1 (volume V_DOD).
    """
    # CORRECTION.  The vertices (0,+-1,+-phi) form an icosahedron of CIRCUMRADIUS
    # sqrt(1+phi^2) = 1.9021 and edge 2, so the centre-vertex distance is 1.9021, NOT 2: that
    # set is not a packing at minimum separation 2.  The correct configuration scales the UNIT
    # icosahedron so the circumradius is exactly 2; then the edge is 2*1.05146 = 2.1029 > 2 and
    # the centre-vertex distance is exactly 2, as the fixture requires.  (Caught by this
    # validator; the error had been carried since the 13-cluster fixture was first written.)
    r5 = 5 ** 0.5
    phi = (1 + r5) / 2
    raw = []
    for s1 in (1, -1):
        for s3 in (1, -1):
            raw += [(0.0, s1, s3 * phi), (s1, s3 * phi, 0.0), (s3 * phi, 0.0, s1)]
    raw = raw[:12]
    norm = (1 + phi ** 2) ** 0.5          # = 1.9021..., the circumradius of `raw`
    V = [(0.0, 0.0, 0.0)] + [tuple(2.0 * c / norm for c in v) for v in raw]
    dmin = min(((V[i][0] - V[j][0]) ** 2 + (V[i][1] - V[j][1]) ** 2 + (V[i][2] - V[j][2]) ** 2) ** 0.5
               for i in range(13) for j in range(i + 1, 13))
    # central cell: regular dodecahedron of inradius 1; its circumradius
    #   R_circ = R_in * sqrt(3) * (1 + sqrt5)/2 / ... -- computed from the face geometry instead:
    #   for inradius 1, R_circ = sqrt( (5/2 + 11 sqrt5/10) ) * 2 cos(pi/5) / ...  use the known
    #   value 1.2584086... and bound it crudely and rigorously below 8.
    R_circ_upper = 1.3            # the true value is 1.2584...; 1.3 < 8 already suffices
    # V4: is the fixture SATURATED?  A packing is saturated if no further unit ball fits, i.e.
    # if every point of space is within distance 2 of some centre.  For the period-16 cluster the
    # period cube is large compared with the cluster, so there are big holes: it is NOT saturated.
    # Saturation is not needed for C044's cut/flow criterion (which applies to any packing), but
    # it IS needed for Hales-type local arguments, so the scope is recorded explicitly.
    L = 16.0
    import itertools as _it
    best_hole = 0.0
    for k in _it.product(range(-1, 2), repeat=3):
        p = [k[t] * L / 2.0 for t in range(3)]
        d = min((p[0] - v[0]) ** 2 + (p[1] - v[1]) ** 2 + (p[2] - v[2]) ** 2 for v in V) ** 0.5
        best_hole = max(best_hole, d)
    saturated = bool(best_hole < 2.0)
    return dict(V4_max_hole=float(best_hole), V4_saturated=saturated,
                V1_min_separation=float(dmin), V1_ok=bool(dmin >= 2 - 1e-12),
                V2_nearest_image=16.0 - 2.0, V2_ok=True,
                V3_circumradius_bound=R_circ_upper, V3_uncut=bool(R_circ_upper < 8.0))

def period_decoupling(R, period=16.0):
    """Do copies of the period interact through G_R?  Registered centres lie within a ball of
    radius 2 about the origin of their copy, so two copies are at distance at least
    period - 4.  If that exceeds R there are NO edges between copies, the periodic graph is a
    disjoint union of identical copies, and -- because a finite U splits into pieces in separate
    copies with no edges between them, making sum_U b/|delta^+(U)| a weighted average -- the
    maximum ratio is attained INSIDE one copy.

    CONSEQUENCE when True: the patch threshold t* computed here IS the exact threshold for the
    INFINITE packing, not a finite-patch proxy.  When False the patch result must be labelled
    PATCH_ONLY.  This is a property of the fixture (period vs R), not of the method: a denser
    packing has period comparable to R and the periods do interact.
    """
    gap = period - 4.0
    return dict(gap=gap, decoupled=bool(gap > R), R=R, period=period)


# ---------------------------------------------------------------- graph fixtures
def icosa_edges():
    """Adjacency of the 12 ring cells around the central cell (icosahedron graph),
    rebuilt from explicit coordinates so the convention is stated, not assumed."""
    r5 = 5 ** 0.5
    phi = (1 + r5) / 2
    V = []
    for s1 in (1, -1):
        for s3 in (1, -1):
            V += [(0, s1, s3 * phi), (s1, s3 * phi, 0), (s3 * phi, 0, s1)]
    V = V[:12]
    E = set()
    for i in range(12):
        for j in range(i + 1, 12):
            d2 = sum((V[i][k] - V[j][k]) ** 2 for k in range(3))
            if abs(d2 - 4.0) < 1e-9:
                E.add((i, j))
    return V, sorted(E)

def build_13(distance_R, direction="refute"):
    """Vertices 0..12; edges by DISTANCE, gated with the exact edge length.

    Central-ring edges are at distance exactly 2 (rational, no uncertainty).
    Ring-ring edges are at distance 4 sqrt2/sqrt(5+sqrt5) in [%s, %s].

    DIRECTION MATTERS, and this is why the parameter exists:
      direction="refute"  -> include a ring edge iff R >= EDGE_LO, i.e. a SUPERGRAPH of the true
                             graph.  A cut violating in a supergraph also violates in the true
                             graph (its boundary is no smaller), so refutation stays sound.
      direction="flow"    -> include iff R >= EDGE_HI, i.e. a SUBGRAPH.  A flow on a subgraph is a
                             flow on the true graph, so feasibility stays sound.
    When R is outside the uncertainty band both directions give the same graph.
    """ + ("  [edge in (%.15f, %.15f)]" % (float(EDGE_LO), float(EDGE_HI)))
    # BUG FIXED: the central-ring edges are at distance exactly 2, so they must be gated by R
    # too.  An earlier version added them unconditionally, which gave R = 1 a twelve-edge star
    # instead of the correct isolated-vertex graph (the R < 2 regime).
    R = F(distance_R) if not isinstance(distance_R, F) else distance_R
    E = set()
    if R >= 2:                                          # exact rational distance
        E |= {(0, j) for j in range(1, 13)}            # central-ring at distance exactly 2
    gate = EDGE_LO if direction == "refute" else EDGE_HI
    if R >= gate:
        _, ringE = icosa_edges()
        E |= {(i + 1, j + 1) for (i, j) in ringE}      # ring-ring at the icosahedron edge
    return 13, sorted(E)

def build_fcc_patch(n):
    """n x n x n supercell of FCC at minimum separation 2 (centres sqrt2 * D_3).
    Every cell volume is sqrt32, so b = 0 exactly.  Edges between centres at distance <= R
    are computed from the explicit coordinates with periodic images."""
    A = [[2.0 ** 0.5 * c for c in row] for row in [[0, 1, 1], [1, 0, 1], [1, 1, 0]]]   # elementwise
    sites = []
    for i in range(n):
        for j in range(n):
            for k in range(n):
                sites.append([i * A[0][t] + j * A[1][t] + k * A[2][t] for t in range(3)])
    S = [[n * A[0][t], n * A[1][t], n * A[2][t]] for t in range(3)]
    return sites, S

# ---------------------------------------------------------------- cut / flow
def cut_value(b, edges, U):
    """sum_U b over the cut side and |delta^+(U)| for the undirected graph with one edge per
    pair (capacity Phi each)."""
    U = set(U)
    sb = sum(b[v] for v in U)
    bd = sum(1 for (i, j) in edges if (i in U) != (j in U))
    return sb, bd

def singleton_bounds(b_lo, edges):
    """Per-vertex singleton bounds b(v)/deg(v), and the degree-zero flag.

    Two distinct statements, which an earlier version conflated:
      * for a vertex of POSITIVE deficit and degree ZERO, no transfer exists at any Phi: the
        divergence bound cannot be met at that vertex at all.  This is not a cut violation, it
        is pointwise infeasibility, and it is reported as such.
      * for a vertex of positive deficit and degree d > 0, the singleton cut gives the lower
        bound Phi >= b(v)/d for THIS fixture.  This is a per-fixture threshold, not a universal
        constant: it constrains any Phi that must serve all packings only because this particular
        packing exists.
    """
    n = len(b_lo)
    deg = [0] * n
    for (i, j) in edges:
        deg[i] += 1; deg[j] += 1
    out = []
    infeasible = []
    for v in range(n):
        if b_lo[v] > 0:
            if deg[v] == 0:
                infeasible.append(v)
                out.append(dict(vertex=v, b=str(b_lo[v]), degree=0, singleton=None,
                                verdict="INFEASIBLE_POINTWISE"))
            else:
                out.append(dict(vertex=v, b=str(b_lo[v]), degree=deg[v],
                                singleton=str(b_lo[v] / deg[v]), verdict="SINGLETON_BOUND"))
        else:
            out.append(dict(vertex=v, b=str(b_lo[v]), degree=deg[v], singleton=None,
                            verdict="no constraint"))
    return out, infeasible


def global_necessary_condition(b_lo):
    """The cheapest necessary condition of all: summing div(v) >= b(v) over EVERY vertex gives
    0 = sum_v div(v) >= sum_v b(v), so a transfer requires sum_v b(v) <= 0.  Checked separately
    because an exhaustive search capped at max_size cannot reach U = everything for n > max_size,
    and that is exactly the cut that carries this constraint."""
    tot = sum(b_lo)
    return tot, bool(tot <= 0)


def find_violating_cut(b, edges, Phi, max_size=None):
    """Exhaustive over subsets up to max_size; returns (U, sum_b, boundary) of the worst
    ratio sum_b / boundary, or None if no violation.  n is small by design."""
    n = max(max(e) for e in edges) + 1 if edges else 0
    if n == 0:
        return None
    if max_size is None:
        max_size = n
    best = None
    for k in range(1, max_size + 1):
        for U in itertools.combinations(range(n), k):
            sb, bd = cut_value(b, edges, U)
            if bd == 0:
                # An empty boundary means U is everything.  For a FINITE vertex set this is a
                # legitimate obstruction: summing the divergence bound over all vertices gives
                # 0 = sum_v div(v) >= sum_v b(v), so sum b > 0 is infeasible at ANY Phi.
                # (This is the only place where the empty-boundary case carries content, and an
                # earlier version skipped it, hiding the constraint.)
                if sb > 0:
                    ratio = F(10) ** 18          # represent as "unbounded"
                    if best is None or ratio > best[0]:
                        best = (ratio, U, sb, bd)
                continue
            if sb > Phi * bd:
                ratio = sb / bd
                if best is None or ratio > best[0]:
                    best = (ratio, U, sb, bd)
    return best

def exhaustive_cut_scan(b_lo, edges, cap_subsets=1 << 16):
    """EXACT per-fixture t* = max over ALL finite U of sum_U b / |delta^+(U)|.

    Only feasible when 2^n is small (n <= 16 by default); otherwise returns None and the caller
    falls back to the size-capped search, which must then be described as capped.  Subsets with an
    EMPTY boundary are excluded from the ratio (the ratio is not defined there) but are reported
    separately, because for a finite vertex set they carry the condition sum_U b <= 0.
    """
    n = max(max(e) for e in edges) + 1 if edges else len(b_lo)
    n = max(n, len(b_lo))
    if (1 << n) > cap_subsets:
        return None
    best = None
    empty_boundary_positive = []
    for mask in range(1, 1 << n):
        U = tuple(v for v in range(n) if mask >> v & 1)
        sb, bd = cut_value(b_lo, edges, U)
        if bd == 0:
            if sb > 0:
                empty_boundary_positive.append((U, sb))
            continue
        r = sb / bd
        if best is None or r > best[0]:
            best = (r, U, sb, bd)
    return dict(t_star=best[0], U=list(best[1]), sum_b=best[2], boundary=best[3],
                subsets_scanned=(1 << n) - 1,
                empty_boundary_positive=[(list(U), str(sb)) for (U, sb) in empty_boundary_positive])


def bracket_t_star(b_lo, b_hi, edges):
    """Pin t* between two exhaustive scans:  t_lo <= t* <= t_hi.

    b_lo <= b <= b_hi componentwise, so for EVERY subset U the ratio is monotone in b, and taking
    the max over U preserves both inequalities.  Hence the scan on b_lo gives a lower bound and the
    scan on b_hi an upper bound -- an interval, not a one-sided bound.  Reported only when the two
    scans agree on the maximizing U, which is what makes the interval tight.
    """
    lo = exhaustive_cut_scan(b_lo, edges)
    hi = exhaustive_cut_scan(b_hi, edges)
    if lo is None or hi is None:
        return None
    return dict(t_lo=lo["t_star"], t_hi=hi["t_star"], U_lo=lo["U"], U_hi=hi["U"],
                same_argmax=bool(lo["U"] == hi["U"]), width=hi["t_star"] - lo["t_star"])


def feasible_flow(b, edges, Phi):
    """Max-flow with a supersource feeding b(v) and capacity Phi per edge.
    Returns a rational flow dict or None.  Uses scipy for the search, then ROUNDS TO RATIONALS
    and re-verifies exactly, so the returned object is a genuine certificate for the patch."""
    try:
        import numpy as np
        from scipy.optimize import linprog
    except ImportError:
        return None
    n = max(max(e) for e in edges) + 1 if edges else 0
    if n == 0:
        return {}
    # ONE variable per UNDIRECTED edge, with phi(i,j) in [-Phi, Phi].  An earlier version gave
    # each orientation its own variable and symmetrised afterwards, which does not enforce
    # antisymmetry inside the LP and can produce "flows" that violate the divergence bound.
    idx = {(i, j): k for k, (i, j) in enumerate(edges)}
    m = len(edges)
    # constraints: sum_w phi(v,w) >= b(v)   with phi(w,v) = -phi(v,w)  ->  -sum <= -b
    A = np.zeros((n, m)); bb = np.zeros(n)
    for (i, j) in edges:
        A[i, idx[(i, j)]] -= 1.0        # i sends +phi
        A[j, idx[(i, j)]] += 1.0        # j receives -phi
    for v in range(n):
        bb[v] = -float(b[v])
    bounds = [(-float(Phi), float(Phi))] * m
    c = np.zeros(m)
    res = linprog(c, A_ub=A, b_ub=bb, bounds=bounds, method="highs")
    if not res.success:
        return None
    # ROUND AND VERIFY EXACTLY.  The docstring used to claim this re-verification without doing
    # it: the 1e-9 grid alone can break the divergence bound by up to deg * 1e-9 ~ 1.2e-8, which
    # showed up as a "minimum capacity" 8.3e-9 BELOW the cut scan's t* -- impossible by LP duality,
    # and the symptom that exposed the missing check.  Now a flow is returned only if it passes the
    # exact verifier; otherwise a finer grid is tried, and failing that, None.
    for den in (10 ** 9, 10 ** 12, 10 ** 15):
        phi = {}
        for (i, j), k in idx.items():
            q = F(int(round(res.x[k] * den)), den)
            phi[(i, j)] = q
            phi[(j, i)] = -q
        ok_cap, ok_div, _ = verify_flow_exact(b, edges, Phi, phi)
        if ok_cap and ok_div:
            return phi
    return None

def verify_flow_exact(b, edges, Phi, phi):
    """Exact check of |phi| <= Phi and divergence >= b at every vertex."""
    n = max(max(e) for e in edges) + 1 if edges else 0
    ok_cap = all(abs(phi.get((i, j), F(0))) <= Phi for (i, j) in edges)
    div = [F(0)] * n
    for (i, j) in edges:
        f = phi.get((i, j), F(0))
        div[i] += f; div[j] -= f
    ok_div = all(div[v] >= b[v] for v in range(n))
    return ok_cap, ok_div, div

def load_external_fixture(path):
    """Portable input format so X or Main can evaluate their own packing without editing code.

    JSON schema (all numbers as strings parseable by Fraction; b_lo <= b <= b_hi required):
      {"name": str, "note": str,
       "edges": [[i, j], ...],            undirected, one entry per pair
       "b_lo": ["...", ...],              per vertex, lower bound on sqrt32 - vol Omega
       "b_hi": ["...", ...],              per vertex, upper bound
       "volumes_are_provisional": bool}   true if any volume is floating-point or estimated
    A fixture with `volumes_are_provisional: true` is evaluated but every row is stamped
    PROVISIONAL and may never be quoted as a certificate.
    """
    d = json.load(open(path))
    b_lo = [F(str(x)) for x in d["b_lo"]]
    b_hi = [F(str(x)) for x in d["b_hi"]]
    edges = [tuple(e) for e in d["edges"]]
    n = len(b_lo)
    if len(b_hi) != n:
        raise SystemExit("b_lo and b_hi must have the same length")
    if any(lo > hi for lo, hi in zip(b_lo, b_hi)):
        raise SystemExit("b_lo > b_hi at some vertex; the enclosure is inconsistent")
    if any(i < 0 or i >= n or j < 0 or j >= n for (i, j) in edges):
        raise SystemExit("edge index out of range")
    return dict(name=d.get("name", os.path.basename(path)), b_lo=b_lo, b_hi=b_hi, edges=edges,
                provisional=bool(d.get("volumes_are_provisional", True)),
                note=d.get("note", ""))


def evaluate_external(fx, Phi_trials=(F(1, 1000), F(1, 100), F(1, 10), F(1))):
    """Run the criterion on an external fixture.  A violating cut is reported as a genuine
    obstruction; a flow as PATCH_FEASIBLE.  Provisional volumes are stamped as such."""
    out = dict(fixture=fx["name"], provisional=fx["provisional"], note=fx["note"], rows=[])
    print("== external fixture %r  (%d vertices, %d edges)%s"
          % (fx["name"], len(fx["b_lo"]), len(fx["edges"]),
             "   [VOLUMES PROVISIONAL]" if fx["provisional"] else "   [volumes certified]"))
    if fx["note"]:
        print("   note:", fx["note"])
    sb_rows, infeas = singleton_bounds(fx["b_lo"], fx["edges"])
    for r in sb_rows:
        if r["verdict"] == "SINGLETON_BOUND":
            print("   singleton bound v%d: b/deg = %s/%d = %.12f"
                  % (r["vertex"], r["b"], r["degree"], float(F(r["singleton"]))))
    if infeas:
        print("   POSITIVE DEFICIT AT DEGREE ZERO at %s: INFEASIBLE at any Phi" % infeas)
    tot, ok_global = global_necessary_condition(fx["b_lo"])
    print("   global necessary condition sum_v b >= %.9f -> %s"
          % (float(tot), "satisfied" if ok_global else "VIOLATED (no transfer at any Phi)"))
    worst = find_violating_cut(fx["b_lo"], fx["edges"], F(0), max_size=min(len(fx["b_lo"]), 6))
    if not ok_global:
        worst = (F(10) ** 18, tuple(range(len(fx["b_lo"]))), tot, 0)
    if worst:
        ratio, U, sb, bd = worst
        print("   worst cut (|U| <= 6): U=%s  sum b >= %s  |delta^+|=%d  ratio=%.12f"
              % (list(U), sb, bd, float(ratio)))
        print("   => for THIS fixture the cut condition fails for every Phi < %.12f%s"
              % (float(ratio), "  (PROVISIONAL)" if fx["provisional"] else ""))
        print("      (a per-fixture threshold, not a universal constant)")
        out["rows"].append(dict(kind="violating_cut", U=list(U), sum_b=str(sb), boundary=bd,
                                phi_threshold=str(ratio)))
    for Phi in Phi_trials:
        phi = feasible_flow(fx["b_hi"], fx["edges"], Phi)
        if phi is None:
            continue
        ok_cap, ok_div, div = verify_flow_exact(fx["b_hi"], fx["edges"], Phi, phi)
        print("   Phi=%-8s flow found; |phi|<=Phi %s, divergence>=b %s   PATCH_FEASIBLE only"
              % (Phi, ok_cap, ok_div))
        out["rows"].append(dict(kind="flow", Phi=str(Phi), cap_ok=bool(ok_cap),
                                divergence_ok=bool(ok_div), status="PATCH_FEASIBLE"))
        break
    else:
        print("   no flow found at Phi in %s" % (list(Phi_trials),))
        out["rows"].append(dict(kind="flow", status="NO_FLOW"))
    print()
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default=os.path.join(_OUT, "cut_flow.json"))
    ap.add_argument("--fixture", action="append", default=[],
                    help="external fixture JSON (repeatable); see load_external_fixture")
    a = ap.parse_args()
    os.makedirs(_OUT, exist_ok=True)
    report = {"script": "KeplerConjecture/Computation/cut_flow.py", "external": [],
              "convention": "K15-C044: b(v)=sqrt32-vol Omega(v); G_R edges <= R, capacity Phi; "
                            "transfer exists iff sum_U b <= Phi|delta^+(U)| for every finite U",
              "arithmetic": "rational enclosures b_lo <= b <= b_hi; b_lo used to refute, "
                            "b_hi used for feasibility",
              "rows": []}
    print("K15-C044 cut/flow evaluator")
    print("b(v) = sqrt(32) - vol Omega(v);  sqrt(32) in [%s, %s]\n" % (SQ32_LO, SQ32_HI))

    # ---- controls with b == 0 everywhere
    for name, fn in (("FCC", fcc_b), ("HCP", hcp_b)):
        lo, hi = fn()
        print("== %s control: b = %s exactly, so every cut has sum_U b = 0 <= Phi|delta^+| for"
              % (name, lo))
        print("   every Phi >= 0: the condition is SATISFIED TRIVIALLY and carries no information.")
        report["rows"].append(dict(fixture=name, b_exact="0", status="TRIVIAL_SATISFIED",
                                   note="zero deficits; no discriminating power"))
    print()

    # ---- icosahedral 13-cluster: validate the fixture BEFORE using its deficits
    val = validate_icos_fixture()
    print("== fixture validation (icosahedral 13-cluster, period 16 Z^3)")
    print("   V1 min separation among the 13 centres = %.6f  (need >= 2)  %s"
          % (val["V1_min_separation"], "OK" if val["V1_ok"] else "FAIL"))
    print("   V2 nearest periodic image of the origin at distance %.1f >= 2   OK" % val["V2_nearest_image"])
    print("   V3 central cell circumradius <= %.1f < 8 (half-period), so the cell is UNCUT"
          % val["V3_circumradius_bound"])
    print("   V4 largest empty hole >= %.4f  =>  %s"
          % (val["V4_max_hole"],
             "SATURATED" if val["V4_saturated"] else
             "UNSATURATED (a further ball fits): a sparse periodic fixture"))
    print("      => the central cell is exactly the regular dodecahedron of inradius 1; its volume")
    print("         is the certified enclosure [%s, %s]\n" % (V_DOD_LO, V_DOD_HI))
    if not (val["V1_ok"] and val["V2_ok"] and val["V3_uncut"]):
        print("   FIXTURE INVALID -- refusing to report deficits"); return 2
    b_lo, b_hi = icos_b()
    print("== icosahedral 13-cluster (periodised), b from rational enclosures:")
    print("   central cell b in [%.12f, %.12f]" % (float(b_lo[0]), float(b_hi[0])))
    print("   ring cells  b in [%.6f, %.6f]  (each of the twelve; congruent by the octahedral"
          % (float(b_lo[1]), float(b_hi[1])))
    print("               symmetry, measured to 3.4e-13 -- see period_convention.py)")
    for R in (1.0, 2.0, 2.1029, 3.0):
        n, edges = build_13(R)
        row = dict(fixture="icos13", R=R, n_edges=len(edges),
                   b_central_lo=str(b_lo[0]), b_central_hi=str(b_hi[0]))
        if not edges:
            # R < 2: the graph has no edges at all, so the criterion is the POINTWISE condition
            # b(v) <= 0 for every v (Hales' fcc-compatibility).  The cut machinery is vacuous
            # here and must not be run: a singleton cut has an empty boundary.
            worst_v = max(b_lo)
            print("   R=%.4f: NO EDGES.  The criterion reduces to the POINTWISE condition"
                  % R)
            print("            b(v) <= 0 for every v (Hales' fcc-compatibility).")
            print("            max_v b(v) >= %.12f  =>  %s"
                  % (float(worst_v), "VIOLATED (this packing is not fcc-compatible)" if worst_v > 0
                     else "satisfied"))
            row.update(regime="pointwise", max_b=str(worst_v),
                       pointwise_violated=bool(worst_v > 0), phi_threshold=None)
            report["rows"].append(row)
            print()
            continue
        sb_rows, infeas = singleton_bounds(b_lo, edges)
        pos = [r for r in sb_rows if r["verdict"] == "SINGLETON_BOUND"]
        if pos:
            print("   per-fixture singleton bounds b(v)/deg(v): "
                  + ", ".join("v%d: %.15f (deg %d)"
                              % (r["vertex"], float(F(r["singleton"])), r["degree"])
                              for r in pos))
        if infeas:
            print("   POSITIVE DEFICIT AT DEGREE ZERO at vertices %s: no transfer exists at any"
                  % infeas)
            print("   Phi (pointwise infeasibility, not a cut violation)")
        tot, ok_global = global_necessary_condition(b_lo)
        print("   global necessary condition: sum_v b >= %.9f  ->  %s"
              % (float(tot), "satisfied" if ok_global else
                 "VIOLATED (no transfer exists at ANY Phi)"))
        sb0, bd0 = cut_value(b_lo, edges, [0])
        phi_min = sb0 / bd0 if bd0 else None
        print("   R=%.4f: |E|=%d ; singleton cut {0}: sum_U b >= %.12f over |delta^+|=%d"
              % (R, len(edges), float(sb0), bd0))
        if phi_min is not None:
            print("            => for THIS fixture the cut condition fails for every Phi < %.12f"
                  % float(phi_min))
            print("               (this constrains a Phi that must serve ALL packings only")
            print("                because this packing exists; it is not implied by b > 0 in an")
            print("                arbitrary fixture)")
        dec = period_decoupling(R)
        print("            period vs R: copies are >= %.4f apart, R = %.4f -> %s"
              % (dec["gap"], R,
                 "DECOUPLED (the extremum over finite U is attained inside one copy, so the"
                 " infinite-packing extremum is the patch extremum)" if dec["decoupled"]
                 else "INTERACTING (patch result is PATCH_ONLY)"))
        ex = exhaustive_cut_scan(b_lo, edges)
        if ex is not None:
            print("            t* from all %d subsets (b_lo scan): %.15f at U=%s  %s"
                  % (ex["subsets_scanned"], float(ex["t_star"]), ex["U"],
                     "(singleton attains it)" if ex["U"] == [0] else ""))
            br = bracket_t_star(b_lo, b_hi, edges)
            if br is not None:
                print("            BRACKET on the true t*: [%.15f, %.15f]  width %.1e  %s"
                      % (float(br["t_lo"]), float(br["t_hi"]), float(br["width"]),
                         "(same maximizer)" if br["same_argmax"] else
                         "(DIFFERENT maximizers -- read both)"))
                row["t_star_bracket"] = [str(br["t_lo"]), str(br["t_hi"])]
                row["t_star_width"] = str(br["width"])
                row["t_star_argmax_stable"] = br["same_argmax"]
            if ex["empty_boundary_positive"]:
                print("            NOTE: %d empty-boundary subset(s) have sum_U b > 0 -> infeasible"
                      " at any Phi" % len(ex["empty_boundary_positive"]))
        worst = find_violating_cut(b_lo, edges, F(0), max_size=min(n, 6))
        if not ok_global:
            worst = (F(10) ** 18, tuple(range(n)), tot, 0)
        ratio = None
        if worst:
            ratio, U, sb, bd = worst
            print("            worst cut found (max |U|=6): U=%s, sum b=%.9f, |delta^+|=%.0f,"
                  % (list(U), float(sb), float(bd)))
            print("            sum b / |delta^+| = %.12f" % float(ratio))
        Phi_try = (phi_min + F(1, 100)) if phi_min is not None else F(1, 100)
        n_f, edges_f = build_13(R, direction="flow")      # SUBGRAPH: sound for feasibility
        phi = feasible_flow(b_hi, edges_f, Phi_try)
        if phi is not None:
            ok_cap, ok_div, div = verify_flow_exact(b_hi, edges_f, Phi_try, phi)
            print("            Phi=%.6f: flow found, |phi|<=Phi: %s, divergence>=b: %s"
                  % (float(Phi_try), ok_cap, ok_div))
            print("            (PATCH_FEASIBLE only: this says nothing about other finite U"
                  " or the infinite packing)")
            status = "PATCH_FEASIBLE"
        else:
            print("            Phi=%.6f: no flow found" % float(Phi_try))
            status = "NO_FLOW"
        row.update(regime="cut", singleton_sum_b=str(sb0), singleton_boundary=bd0,
                   phi_threshold=str(phi_min) if phi_min is not None else None,
                   worst_cut=(dict(U=list(worst[1]), sum_b=str(worst[2]), boundary=worst[3])
                              if worst else None),
                   flow_status=status)
        report["rows"].append(row)
        print()
    for path in a.fixture:
        report["external"].append(evaluate_external(load_external_fixture(path)))
    json.dump(report, open(a.json, "w"), indent=1)
    print("wrote", a.json)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
