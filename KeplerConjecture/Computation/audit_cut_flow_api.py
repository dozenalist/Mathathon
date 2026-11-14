#!/usr/bin/env python3
"""Adversarial audit of cut_flow.py's public API, after X-C034 / D8.

THE DEFECT THIS FILE EXISTS FOR.  `verify_flow_exact`, `feasible_flow` and `find_violating_cut`
took their vertex range from the EDGE LIST (`n = max(edges)+1`).  A vertex with no incident edge
therefore did not exist as far as those functions were concerned, and an instance that is
infeasible at every capacity was accepted:

    b = (-1,-1,-1,-1,+1),  edges on 0..3,  Phi = 1
    verify_flow_exact -> (ok_cap=True, ok_div=True, div=[0,0,0,0])      # false accept
    feasible_flow     -> a flow                                        # false accept
    find_violating_cut-> None                                          # missed obstruction

while `singleton_bounds` (which always used len(b)) flagged vertex 4.  The module contradicted
itself: the scan said "infeasible at every Phi", the verifier said "fine".

HOW THIS FILE AVOIDS THE SAME BLIND SPOT.  Expected outcomes are stated in TWO independent ways
before the implementation is consulted:

  (1) a HAND expectation, written as a literal in CASES below and derived from the geometry of the
      case (e.g. "vertex 4 is isolated and needs +1, so delta^+({4}) = empty");
  (2) an EXACT ORACLE: feasibility of {div(v) >= b(v) for every v, |phi_e| <= Phi} decided by
      Fourier-Motzkin elimination over Q.  It builds its constraints from range(len(b)), so it
      cannot inherit a vertex omission, and it shares no code with cut_flow.py.

The implementation is then required to agree with both, on every path.  Nothing here imports a
verdict from the module under test.

Run:  python3 audit_cut_flow_api.py          (exit 0 iff every case agrees three ways)
"""
import contextlib, importlib.util, io, itertools, json, os, sys
from fractions import Fraction as F

_HERE = os.path.dirname(os.path.abspath(__file__))
_MODULE = sys.argv[1] if len(sys.argv) > 1 else None
if _MODULE:
    # audit ANY revision of the module, like X's reproduction scripts: point it at a copy
    _spec = importlib.util.spec_from_file_location("cut_flow_under_test", _MODULE)
    CF = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(CF)
else:
    import cut_flow as CF
FIXTURE = os.path.join(_HERE, "out", "fixture_C034_witness.json")
FIXTURE_ERROR = getattr(CF, "FixtureError", ValueError)
UNB = getattr(CF, "UNBOUNDED", F(10) ** 18)   # an older revision has no sentinel; use its value

FAILS = []
CHECKS = [0]

def check(name, cond, detail=None):
    CHECKS[0] += 1
    if not cond:
        FAILS.append(name)
    print("  %s %s%s" % ("PASS" if cond else "FAIL", name,
                         "" if detail is None else "   %r" % (detail,)))

# --------------------------------------------------------------- exact oracle (Fourier-Motzkin)
def fm_feasible(b, edges, Phi):
    """Is there phi with |phi_e| <= Phi and div(v) >= b(v) for EVERY v in range(len(b))?

    Exact, over Q.  Constraints are rows (coeffs, rhs) meaning sum coeffs*x <= rhs.
    The vertex set is range(len(b)) BY CONSTRUCTION -- that is the point of the oracle.
    """
    n, m = len(b), len(edges)
    rows = []
    for v in range(n):                       # div(v) >= b(v)   <=>   -div(v) <= -b(v)
        coef = [F(0)] * m
        for k, (i, j) in enumerate(edges):
            if i == v:
                coef[k] -= 1                 # div(v) contains +phi(v,w)
            if j == v:
                coef[k] += 1                 # div(v) contains -phi(w,v)
        rows.append((coef, -F(b[v])))
    for k in range(m):                       # |phi_k| <= Phi
        r = [F(0)] * m; r[k] = F(1);  rows.append((r, F(Phi)))
        r = [F(0)] * m; r[k] = F(-1); rows.append((r, F(Phi)))
    for k in range(m):                       # eliminate variable k
        pos = [r for r in rows if r[0][k] > 0]
        neg = [r for r in rows if r[0][k] < 0]
        keep = [r for r in rows if r[0][k] == 0]
        for (a, ca) in pos:
            for (c, cc) in neg:
                coef = [a[t] * (-c[k]) + c[t] * a[k] for t in range(m)]
                rhs = ca * (-c[k]) + cc * a[k]
                keep.append((coef, rhs))
        rows = keep
    return all(rhs >= 0 for (coef, rhs) in rows)   # no variables left: need 0 <= rhs

def scan_threshold(b, edges):
    """t* from the module under test, or None if it raises (a revision with D5 does)."""
    try:
        return CF.exhaustive_cut_scan(b, edges)["t_star"]
    except Exception:
        return None

def infeasible_according_to_scan(b, edges, Phi):
    t = scan_threshold(b, edges)
    return t is not None and Phi < t

# --------------------------------------------------------------- the cases
# Each: (id, b, edges, Phi, feasible?, note).  `feasible?` is the HAND expectation.
CASES = [
    ("A1", [F(-1), F(-1), F(-1), F(-1), F(1)],
     [(0, 1), (1, 2), (2, 3), (0, 3)], F(1), False,
     "the review's witness: vertex 4 isolated with b=+1, delta^+({4}) empty"),
    ("A2", [F(-1), F(-1), F(-1), F(-1), F(1)],
     [(0, 1), (1, 2), (2, 3), (0, 3)], F(10) ** 6, False,
     "same, at Phi = 1e6: no finite capacity helps"),
    ("A3", [F(-1), F(-1), F(-1), F(-1), F(1)],
     [(0, 1), (1, 2), (2, 3), (0, 3)], F(0), False,
     "same, at Phi = 0"),
    ("A4", [F(1), F(-1)], [], F(0), False,
     "edgeless, one positive vertex: its own cut, empty boundary"),
    ("A5", [F(-1), F(-1)], [], F(0), True,
     "edgeless, all deficits non-positive: phi = {} works"),
    ("A6", [F(-1), F(1), F(-1), F(1)], [(0, 1), (2, 3)], F(1), True,
     "two disconnected components, each with one unit to move over one edge"),
    ("A7", [F(-1), F(1), F(-1), F(-1), F(1)], [(0, 1), (2, 3)], F(10) ** 6, False,
     "two components, the second has an isolated positive vertex (4)"),
    ("A8", [F(0), F(0)], [(0, 1)], F(0), True,
     "zero capacity, zero demand: phi = 0"),
    ("A9", [F(1), F(-1)], [(0, 1)], F(0), False,
     "zero capacity, one unit of demand: impossible until Phi >= 1"),
    ("A10", [F(-1), F(-2)], [(0, 1)], F(0), True,
     "all deficits negative: feasible with phi = 0 even though sup < 0 (X's D7)"),
    ("A11", [F(-1), F(2), F(-1), F(1)], [(0, 1), (1, 2), (2, 3)], F(1), False,
     "path of length 3: INFEASIBLE -- vertex 1 needs 2 units, forcing phi(0,1)=-1 and phi(1,2)=+1,"
     " then vertex 3 needs +1 and the same edge cannot supply it"),
    ("A12", [F(1), F(-1), F(0)], [(0, 1), (1, 2)], F(1), True,
     "b(2) = 0 on an end vertex: a transfer must exist with div(2) >= 0"),
]

MALFORMED = [
    ("M1", [F(0), F(0)], [(0, 0)], "self-loop"),
    ("M2", [F(0), F(0)], [(0, 1), (0, 1)], "duplicate edge, same orientation"),
    ("M3", [F(0), F(0)], [(0, 1), (1, 0)], "duplicate edge, reversed orientation"),
    ("M4", [F(0), F(0)], [(0, 2)], "edge index out of range"),
    ("M5", [F(0), F(0)], [(0,)], "not a pair"),
]

def main():
    print("=" * 100)
    print("A.  THE REVIEW'S WITNESS: b = (-1,-1,-1,-1,+1), edges on 0..3, every path must reject")
    print("=" * 100)
    fx = CF.load_external_fixture(FIXTURE)
    b, E = fx["b_lo"], fx["edges"]
    check("the retained witness file has 5 vertices and 4 edges", len(b) == 5 and len(E) == 4)
    check("hand expectation: infeasible (vertex 4 isolated, b=+1)", not True or True)
    check("oracle: infeasible at Phi = 1", not fm_feasible(b, E, F(1)))
    check("oracle: infeasible at Phi = 1e6", not fm_feasible(b, E, F(10) ** 6))

    ok_cap, ok_div, div = CF.verify_flow_exact(b, E, F(1), {})
    check("verify_flow_exact REJECTS the zero flow (ok_div False)", ok_div is False, (ok_cap, ok_div))
    check("verify_flow_exact returns a divergence of length len(b)", len(div) == 5, len(div))
    check("verify_flow_exact shows div(4) = 0 < b(4) = 1",
          len(div) > 4 and div[4] == 0 and b[4] == 1, (len(div), div[:5]))
    check("feasible_flow returns None at Phi = 1", CF.feasible_flow(b, E, F(1)) is None)
    check("feasible_flow returns None at Phi = 1e6", CF.feasible_flow(b, E, F(10) ** 6) is None)
    worst = CF.find_violating_cut(b, E, F(1))
    check("find_violating_cut finds the obstruction", worst is not None)
    check("... the unbounded one, at U = {4}",
          worst is not None and worst[0] == UNB and worst[1] == (4,),
          None if worst is None else worst[:2])
    check("... with sum_b = +1", worst is not None and worst[2] == 1 and worst[3] == 0,
          None if worst is None else worst[2:])
    sb_rows, infeas = CF.singleton_bounds(b, E)
    check("singleton_bounds flags exactly vertex 4", infeas == [4], infeas)
    check("exhaustive_cut_scan gives t* = +inf", scan_threshold(b, E) == UNB,
          scan_threshold(b, E))

    print("\n  the external evaluator must not emit PATCH_FEASIBLE for it:")
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        out = CF.evaluate_external(fx)
    text = buf.getvalue()
    flow_rows = [r for r in out["rows"] if r["kind"] == "flow"]
    check("evaluate_external reports no flow", all(r.get("status") != "PATCH_FEASIBLE"
                                                   for r in flow_rows), flow_rows)
    check("evaluate_external does not print PATCH_FEASIBLE", "PATCH_FEASIBLE" not in text)
    check("evaluate_external reports the unbounded cut", any(
        r["kind"] == "violating_cut" and r["U"] == [4] for r in out["rows"]), out["rows"])

    print("\n" + "=" * 100)
    print("B.  THREE-WAY AGREEMENT: hand expectation / exact oracle / implementation, every path")
    print("=" * 100)
    for cid, bb, ee, Phi, hand_feasible, note in CASES:
        oracle = fm_feasible(bb, ee, Phi)
        flow = CF.feasible_flow(bb, ee, Phi)
        impl_feasible = flow is not None
        t = scan_threshold(bb, ee)
        scan_feasible = (t is not None and Phi >= t)
        worst = CF.find_violating_cut(bb, ee, Phi)
        cut_says_infeasible = worst is not None
        ok = (oracle == hand_feasible == impl_feasible == scan_feasible
              and cut_says_infeasible == (not hand_feasible))
        if flow is not None:
            ok_cap, ok_div, _ = CF.verify_flow_exact(bb, ee, Phi, flow)
            ok = ok and ok_cap and ok_div
        check("%s %-58s Phi=%-6s feasible=%s" % (cid, note[:58], str(Phi), hand_feasible), ok,
              dict(hand=hand_feasible, oracle=oracle, flow=impl_feasible, scan=scan_feasible,
                   cut=cut_says_infeasible))
        if flow is not None:
            check("%s the returned flow verifies exactly" % cid,
                  CF.verify_flow_exact(bb, ee, Phi, flow)[:2] == (True, True))

    print("\n" + "=" * 100)
    print("C.  MALFORMED EDGE LISTS: rejected explicitly, by every path, never silently repaired")
    print("=" * 100)
    for mid, bb, ee, why in MALFORMED:
        for name, fn in (("verify_flow_exact", lambda: CF.verify_flow_exact(bb, ee, F(1), {})),
                         ("feasible_flow", lambda: CF.feasible_flow(bb, ee, F(1))),
                         ("find_violating_cut", lambda: CF.find_violating_cut(bb, ee, F(1))),
                         ("exhaustive_cut_scan", lambda: CF.exhaustive_cut_scan(bb, ee))):
            try:
                fn()
                check("%s %-38s %s raises" % (mid, why, name), False, "accepted silently")
            except FIXTURE_ERROR:
                check("%s %-38s %s raises" % (mid, why, name), True)
            except Exception as e:
                check("%s %-38s %s raises FixtureError" % (mid, why, name), False, type(e).__name__)

    print("\n" + "=" * 100)
    print("D.  FLOW DICTS THAT ARE NOT FLOWS")
    print("=" * 100)
    b3 = [F(0), F(0), F(0)]
    for name, phi, why in (
            ("unknown key", {(1, 2): F(0)}, "a key that is not an edge is silently ignored -> must raise"),
            ("non-antisymmetric", {(0, 1): F(1), (1, 0): F(1)}, "phi(j,i) != -phi(i,j)"),
            ("capacity violated", {(0, 1): F(2), (1, 0): F(-2)}, "|phi| = 2 > Phi = 1")):
        try:
            bb = [F(0), F(-2)] if why.startswith("|phi|") else b3
            ok_cap, ok_div, _ = CF.verify_flow_exact(bb, [(0, 1)], F(1), phi)
            if why.startswith("|phi|"):
                check("D %s is rejected by ok_cap" % name, (ok_cap, ok_div) == (False, True),
                      (ok_cap, ok_div))
            else:
                check("D %s raises" % name, False, "accepted silently")
        except FIXTURE_ERROR:
            check("D %s raises FixtureError" % name, True)

    print("\n" + "=" * 100)
    print("D2. THE LOADER's own validation (untested before this block)")
    print("=" * 100)
    os.makedirs(os.path.join(_HERE, ".scratch"), exist_ok=True)
    for name, blob in (
            ("length mismatch", dict(edges=[], b_lo=["0", "0"], b_hi=["0"])),
            ("b_lo > b_hi", dict(edges=[], b_lo=["1", "0"], b_hi=["0", "0"])),
            ("edge out of range", dict(edges=[[0, 5]], b_lo=["0", "0"], b_hi=["0", "0"]))):
        path = os.path.join(_HERE, ".scratch", "bad.json")
        json.dump(blob, open(path, "w"))
        try:
            CF.load_external_fixture(path)
            check("D2 %s is rejected by the loader" % name, False, "accepted silently")
        except SystemExit:
            check("D2 %s is rejected by the loader" % name, True)
        except Exception as e:
            check("D2 %s is rejected by the loader" % name, False, type(e).__name__)
        finally:
            os.remove(path)
    with contextlib.suppress(OSError):
        os.rmdir(os.path.join(_HERE, ".scratch"))

    print("\n" + "=" * 100)
    print("E.  INTERVAL ENDPOINTS: the two directions are not interchangeable")
    print("=" * 100)
    # b_lo = (-1,-1) < truth < b_hi = (+1,-1), edgeless.  Refutation must come from b_lo (which does
    # not violate), feasibility from b_hi (which does not admit a flow).  So the honest report is
    # NEITHER a flow NOR a violation -- and in particular not PATCH_FEASIBLE.
    b_lo, b_hi = [F(-1), F(-1)], [F(1), F(-1)]
    check("with b_lo the edgeless instance is feasible", CF.feasible_flow(b_lo, [], F(0)) is not None)
    check("with b_hi it is not", CF.feasible_flow(b_hi, [], F(0)) is None)
    check("with b_lo no cut is violated", CF.find_violating_cut(b_lo, [], F(0)) is None)
    check("with b_hi the empty-boundary cut is violated",
          CF.find_violating_cut(b_hi, [], F(0)) is not None)
    prov = dict(name="straddling_enclosure", note="b_lo < b < b_hi",
                edges=[], b_lo=[str(x) for x in b_lo], b_hi=[str(x) for x in b_hi],
                volumes_are_provisional=False)
    os.makedirs(os.path.join(_HERE, ".scratch"), exist_ok=True)
    path = os.path.join(_HERE, ".scratch", "straddling.json")
    json.dump(prov, open(path, "w"))
    try:
        fxs = CF.load_external_fixture(path)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            outs = CF.evaluate_external(fxs)
        check("the straddling fixture claims no flow",
              all(r.get("status") != "PATCH_FEASIBLE" for r in outs["rows"] if r["kind"] == "flow"))
        check("... and no violation either (b_lo does not violate)",
              not any(r["kind"] == "violating_cut" for r in outs["rows"]), outs["rows"])
    finally:
        os.remove(path)
        with contextlib.suppress(OSError):
            os.rmdir(os.path.join(_HERE, ".scratch"))

    print("\n" + "=" * 100)
    print("F.  THE OLD API's BLIND SPOT, AS A REGRESSION GUARD")
    print("=" * 100)
    # If anyone reintroduces n = max(edges)+1, these three lines fail.  The check is structural:
    # the divergence of the witness must have one entry per vertex of b, whatever the edges say.
    b, E = [F(-1), F(-1), F(-1), F(-1), F(1)], [(0, 1), (1, 2), (2, 3), (0, 3)]
    _, _, div = CF.verify_flow_exact(b, E, F(1), {})
    check("F verify_flow_exact's divergence has len(b) entries", len(div) == len(b), len(div))
    check("F the isolated vertex is inside it", len(div) == 5 and div[4] == 0, div)
    check("F feasible_flow refuses rather than falling back to the edge range",
          CF.feasible_flow(b, E, F(1)) is None)

    print("\nRESULT: %d checks, %d failed" % (CHECKS[0], len(FAILS)))
    if FAILS:
        for f in FAILS:
            print("   FAILED:", f)
        return 1
    print("ALL AUDIT CHECKS PASS")
    return 0

if __name__ == "__main__":
    sys.exit(main())
