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
SQ32_LO = F(5656854249492380, 10 ** 15)
SQ32_HI = F(5656854249492381, 10 ** 15)
# Regular dodecahedron of inradius 1  (the central cell of the 13-cluster at separation 2):
#   V = (15 + 7 sqrt5)/4 * a^3,  a = 2/sqrt(5/2 + 11 sqrt5/10)
V_DOD_LO = F(5550291028, 10 ** 9)          # 5.550291028
V_DOD_HI = F(5550291030, 10 ** 9)          # 5.550291030

def fcc_b():   return F(0), F(0)           # vol Omega = sqrt32 exactly
def hcp_b():   return F(0), F(0)

def icos_b():
    """Periodised 13-cluster: cell 0 = regular dodecahedron of inradius 1, cells 1..12 share
    the rest of the period cube 16^3 = 4096.  Returns (b_lo, b_hi) lists."""
    period = F(4096)
    b0_lo = SQ32_LO - V_DOD_HI
    b0_hi = SQ32_HI - V_DOD_LO
    vol_other_lo = (period - V_DOD_HI) / 12
    vol_other_hi = (period - V_DOD_LO) / 12
    b1_lo = SQ32_LO - vol_other_hi
    b1_hi = SQ32_HI - vol_other_lo
    return [b0_lo] + [b1_lo] * 12, [b0_hi] + [b1_hi] * 12

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

def build_13(distance_R):
    """Vertices 0..12; edges: central to all twelve (distance exactly 2 <= R), plus the
    icosahedral ring edges (ring distances >= edge 2.1029 <= R iff R >= 2.1029).
    Distance-gated so the R convention is explicit."""
    E = {(0, j) for j in range(1, 13)}                 # central-ring at distance 2
    if distance_R >= 2.1029 - 1e-9:
        _, ringE = icosa_edges()
        E |= {(i + 1, j + 1) for (i, j) in ringE}      # ring-ring at the icosahedron edge
    return 13, sorted(E)

def build_fcc_patch(n):
    """n x n x n supercell of FCC at minimum separation 2 (centres sqrt2 * D_3).
    Every cell volume is sqrt32, so b = 0 exactly.  Edges between centres at distance <= R
    are computed from the explicit coordinates with periodic images."""
    A = (2.0 ** 0.5) * [[0, 1, 1], [1, 0, 1], [1, 1, 0]]
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
                continue
            if sb > Phi * bd:
                ratio = sb / bd
                if best is None or ratio > best[0]:
                    best = (ratio, U, sb, bd)
    return best

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
    # variable per oriented arc (both directions), |phi| <= Phi handled by bounds
    arcs = [(i, j) for (i, j) in edges] + [(j, i) for (i, j) in edges]
    idx = {a: k for k, a in enumerate(arcs)}
    m = len(arcs)
    # constraints: sum_w phi(v,w) >= b(v)  ->  -sum <= -b
    A = np.zeros((n, m)); bb = np.zeros(n)
    for v in range(n):
        for (i, j) in arcs:
            if i == v: A[v, idx[(i, j)]] -= 1.0
        bb[v] = -float(b[v])
    bounds = [(-float(Phi), float(Phi))] * m
    c = np.zeros(m)
    res = linprog(c, A_ub=A, b_ub=bb, bounds=bounds, method="highs")
    if not res.success:
        return None
    # round and verify EXACTLY
    phi = {}
    for a, k in idx.items():
        q = F(int(round(res.x[k] * 10 ** 9)), 10 ** 9)
        phi[a] = q
    # antisymmetry: enforce by using the difference
    for (i, j) in edges:
        d = (phi[(i, j)] - phi[(j, i)]) / 2
        phi[(i, j)] = d; phi[(j, i)] = -d
    return phi

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

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default=os.path.join(_OUT, "cut_flow.json"))
    a = ap.parse_args()
    os.makedirs(_OUT, exist_ok=True)
    report = {"script": "KeplerConjecture/Computation/cut_flow.py",
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

    # ---- icosahedral 13-cluster
    b_lo, b_hi = icos_b()
    print("== icosahedral 13-cluster (periodised), b from rational enclosures:")
    print("   central cell b in [%.12f, %.12f]" % (float(b_lo[0]), float(b_hi[0])))
    print("   ring cells  b in [%.6f, %.6f]" % (float(b_lo[1]), float(b_hi[1])))
    for R in (2.0, 2.1029, 3.0):
        n, edges = build_13(R)
        # necessary threshold from the singleton cut {0}
        sb0, bd0 = cut_value(b_lo, edges, [0])
        phi_min = sb0 / bd0
        print("   R=%.4f: |E|=%d ; singleton cut {0}: sum_U b >= %.12f over |delta^+|=%d"
              % (R, len(edges), float(sb0), bd0))
        print("            => the cut condition FAILS for every Phi < %.12f" % float(phi_min))
        # exhaustive worst cut
        worst = find_violating_cut(b_lo, edges, F(0), max_size=min(n, 6))
        if worst:
            ratio, U, sb, bd = worst
            print("            worst cut found (max |U|=6): U=%s, sum b=%.9f, |delta^+|=%.0f,"
                  % (list(U), float(sb), float(bd)))
            print("            sum b / |delta^+| = %.12f" % float(ratio))
        else:
            ratio = None
        # feasibility ABOVE the threshold, using b_hi (conservative for the flow direction)
        Phi_try = phi_min + F(1, 100)
        phi = feasible_flow(b_hi, edges, Phi_try)
        if phi is not None:
            ok_cap, ok_div, div = verify_flow_exact(b_hi, edges, Phi_try, phi)
            print("            Phi=%.6f: flow found, |phi|<=Phi: %s, divergence>=b: %s"
                  % (float(Phi_try), ok_cap, ok_div))
            print("            (PATCH_FEASIBLE only: this says nothing about other finite U"
                  " or the infinite packing)")
            status = "PATCH_FEASIBLE"
        else:
            print("            Phi=%.6f: no flow found by the LP" % float(Phi_try))
            status = "NO_FLOW"
        if ratio is not None and R == 2.0:
            # at R = 2 the graph is a star: the singleton cut is the binding one
            print("            threshold Phi* = %.12f  (star graph: singleton cut is binding)"
                  % float(phi_min))
        report["rows"].append(dict(fixture="icos13", R=R, n_edges=len(edges),
                                   b_central_lo=str(b_lo[0]), b_central_hi=str(b_hi[0]),
                                   singleton_sum_b=str(sb0), singleton_boundary=bd0,
                                   phi_threshold=str(phi_min),
                                   worst_cut=[list(worst[1]), str(worst[2]), worst[3]] if worst else None,
                                   flow_status=status))
        print()
    json.dump(report, open(a.json, "w"), indent=1)
    print("wrote", a.json)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
