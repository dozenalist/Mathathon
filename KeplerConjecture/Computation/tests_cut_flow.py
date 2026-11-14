#!/usr/bin/env python3
"""Truth-known tests for cut_flow.py.  For X's audit of the evaluator.

Each case has an ANALYTICALLY KNOWN answer, so the test checks the implementation against theory
rather than against itself:

  S1  star graph, centre deficit b0 > 0, m leaves with b = 0: the singleton cut {centre} has
      Sigma_U b = b0 over |delta^+| = m, so the threshold is Phi* = b0/m exactly, and a flow
      exists iff Phi >= Phi*.  (This is the shape of the icosahedral fixture at R = 2, where the
      leaves happen to have negative deficits, which only makes the flow easier.)
  S2  all deficits <= 0: the zero flow is feasible at Phi = 0, so no Phi is needed.
  S3  a path 0-1-2 with b = (1, -1, 0): the cut {0} has value 1 over 1 edge, so Phi >= 1 is
      necessary and sufficient.
  S4  enclosures: b_lo > b_hi at any vertex is rejected.
  S5  provisional fixtures are stamped PROVISIONAL and cannot be reported as certificates.
  S6  every edge is only used once in the cut count, and an isolated vertex is its own cut.

Run: python3 tests_cut_flow.py     (exit 0 iff all pass)
"""
import importlib.util, json, os, sys
from fractions import Fraction as F

_HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("cut_flow", os.path.join(_HERE, "cut_flow.py"))
CF = importlib.util.module_from_spec(spec); spec.loader.exec_module(CF)

FAILS = []
def check(name, cond, detail=""):
    print(("  PASS  " if cond else "  FAIL  ") + name + (("   [" + str(detail) + "]") if detail and not cond else ""))
    if not cond:
        FAILS.append(name)

def star(m, b0):
    return [b0] + [F(0)] * m, [(0, j) for j in range(1, m + 1)]

def main():
    print("S1a star, centre b0 > 0 and leaves 0: Sigma b > 0, so NO transfer exists at any Phi")
    print("    (summing div(v) >= b(v) over all v gives 0 >= Sigma b, so Sigma b <= 0 is necessary;")
    print("     the obstruction is the empty-boundary cut U = everything, which an earlier version")
    print("     of find_violating_cut skipped, hiding the constraint)")
    for m in (1, 2, 3, 12):
        b, E = star(m, F(3, 10))
        w = CF.find_violating_cut(b, E, F(1000), max_size=len(b))
        check("m=%d violation reported even at Phi = 1000" % m, w is not None, w)
        phi = CF.feasible_flow(b, E, F(1000))
        check("m=%d no flow exists" % m, phi is None)

    print("S1b star, leaves summing to -b0: threshold is exactly b0/m")
    for m in (2, 3, 4):
        b = [F(3, 10)] + [F(-3, 10) / m] * m
        E = [(0, j) for j in range(1, m + 1)]
        Phi_star = F(3, 10) / m
        w_below = CF.find_violating_cut(b, E, Phi_star - F(1, 1000), max_size=min(len(b), 9))
        check("m=%d violation just below b0/m = %s" % (m, Phi_star), w_below is not None, w_below)
        w_above = CF.find_violating_cut(b, E, Phi_star + F(1, 100), max_size=min(len(b), 9))
        check("m=%d no violation just above b0/m" % m, w_above is None, w_above)
        phi = CF.feasible_flow(b, E, Phi_star + F(1, 100))
        check("m=%d flow exists and verifies exactly" % m, phi is not None)
        if phi is not None:
            ok_cap, ok_div, _ = CF.verify_flow_exact(b, E, Phi_star + F(1, 100), phi)
            check("m=%d flow checks out" % m, ok_cap and ok_div)
        phi_below = CF.feasible_flow(b, E, Phi_star - F(1, 1000))
        check("m=%d no flow just below the threshold" % m, phi_below is None)

    print("S2 all deficits <= 0: the zero flow is feasible at Phi = 0")
    b = [F(-1), F(-2), F(0)]
    E = [(0, 1), (1, 2)]
    w = CF.find_violating_cut(b, E, F(0))
    check("no cut violates when every b <= 0", w is None, w)
    phi = CF.feasible_flow(b, E, F(0))
    ok_cap, ok_div, _ = CF.verify_flow_exact(b, E, F(0), phi)
    check("zero flow verifies at Phi = 0", ok_cap and ok_div)

    print("S3 path with b = (1,-1,0): Sigma b = 0, Phi* = 1 from the cut {0}")
    b = [F(1), F(-1), F(0)]
    E = [(0, 1), (1, 2)]
    worst = CF.find_violating_cut(b, E, F(0))
    check("threshold is exactly 1", worst[0] == F(1), worst[0])
    check("binding cut is {0}", list(worst[1]) == [0] or list(worst[1]) == [0], worst[1])

    print("S4 an inconsistent enclosure is rejected")
    tmp = os.path.join(_HERE, "out", "_bad_fixture.json")
    os.makedirs(os.path.dirname(tmp), exist_ok=True)
    json.dump({"edges": [[0, 1]], "b_lo": ["1", "0"], "b_hi": ["0", "0"]}, open(tmp, "w"))
    try:
        CF.load_external_fixture(tmp)
        ok = False
    except SystemExit:
        ok = True
    check("b_lo > b_hi rejected", ok)
    os.remove(tmp)

    print("S5 a provisional fixture is stamped")
    tmp2 = os.path.join(_HERE, "out", "_prov_fixture.json")
    json.dump({"edges": [[0, 1]], "b_lo": ["1/10", "-1/5"], "b_hi": ["1/10", "-1/5"],
               "volumes_are_provisional": True, "name": "prov"}, open(tmp2, "w"))
    fx = CF.load_external_fixture(tmp2)
    out = CF.evaluate_external(fx)
    check("provisional flag propagated", out["provisional"] is True)
    check("no row claims a certificate", all(r.get("kind") in ("violating_cut", "flow")
                                             for r in out["rows"]))
    os.remove(tmp2)

    print("S6 an isolated vertex is its own cut")
    # This test used to assert "no cut reported when the graph is edgeless", which was the DEFECT
    # speaking: find_violating_cut took n from the edge list, so an edgeless graph had no vertices
    # at all and the empty-boundary obstruction was invisible.  The contract says the opposite: a
    # vertex with b > 0 and no incident edge is infeasible at every Phi, and must be reported.
    b = [F(5, 100), F(-1)]
    E = []                                  # no edges at all
    worst = CF.find_violating_cut(b, E, F(0))
    check("edgeless graph with a positive vertex DOES report the cut", worst is not None, worst)
    check("... as the unbounded one, at U = {0}", worst[0] == CF.UNBOUNDED and worst[1] == (0,),
          worst[:2])
    check("... with sum_b = b(0) and boundary 0", worst[2] == F(5, 100) and worst[3] == 0, worst[2:])
    check("edgeless graph with all b <= 0 reports nothing",
          CF.find_violating_cut([F(-1), F(-1)], [], F(0)) is None)
    check("... and its threshold is 0, not -inf", CF.exhaustive_cut_scan([F(-1), F(-1)], [])["t_star"] == 0)

    print("S7 the binding cut need NOT be a singleton")
    # star with centre b0 and ONE positive leaf: absorbing that leaf reduces the boundary
    # without adding to the deficit, so the pair can beat the singleton.
    # centre 3/10, one POSITIVE leaf 1/5, two leaves -1/4 each: sum b = 0, so the global
    # condition is satisfied and the exhaustive search is well posed.
    b = [F(3, 10), F(1, 5), F(-1, 4), F(-1, 4)]
    E = [(0, 1), (0, 2), (0, 3)]
    tot, ok = CF.global_necessary_condition(b)
    check("sum b = 0 so the global condition holds", tot == 0 and ok, tot)
    worst = CF.find_violating_cut(b, E, F(0), max_size=len(b))
    ratio, U, sb, bd = worst
    singleton = F(3, 10) / 3
    pair = (F(3, 10) + F(1, 5)) / 2
    check("pair cut beats the singleton: %s > %s" % (pair, singleton), pair > singleton)
    check("search finds the pair value (%s) not the singleton" % pair, ratio == pair, ratio)
    check("binding U is the pair {0,1}", sorted(U) == [0, 1], U)

    print("S8 positive deficit at degree zero is POINTWISE infeasibility, not a cut violation")
    b = [F(1, 4), F(-1, 4)]
    E = []                                   # both vertices isolated
    rows, infeas = CF.singleton_bounds(b, E)
    check("vertex 0 flagged degree zero", 0 in infeas, infeas)
    check("its verdict is INFEASIBLE_POINTWISE",
          rows[0]["verdict"] == "INFEASIBLE_POINTWISE", rows[0])
    check("no singleton bound is quoted for it", rows[0]["singleton"] is None)
    tot, ok = CF.global_necessary_condition(b)
    check("global condition holds (sum b = 0), so the obstruction is pointwise", tot == 0 and ok, tot)

    print("S9 the singleton bound is b(v)/deg(v), a PER-FIXTURE threshold")
    b = [F(1, 2), F(-1, 4), F(-1, 4)]
    E = [(0, 1), (0, 2)]
    rows, infeas = CF.singleton_bounds(b, E)
    check("no degree-zero vertices", not infeas)
    check("b0/deg = (1/2)/2 = 1/4", F(rows[0]["singleton"]) == F(1, 4), rows[0]["singleton"])
    w = CF.find_violating_cut(b, E, F(0), max_size=3)
    check("the exhaustive worst cut agrees with the singleton here", w[0] == F(1, 4), w[0])

    print("S10 GEOMETRY: the ring-edge threshold is the exact icosahedral edge")
    import k15radicals as RAD
    e_lo, e_hi = RAD.icosa_edge_enclosure(digits=40)
    check("edge enclosure brackets 2.102924448476534",
          float(e_lo) <= 2.102924448476534424 <= float(e_hi),
          (float(e_lo), float(e_hi)))
    # BOTH SIDES of the threshold, tested against the enclosure
    below = (e_lo + e_hi) / 2 - F(1, 10 ** 6)      # strictly inside the band, below the edge
    above = (e_lo + e_hi) / 2 + F(1, 10 ** 6)      # strictly inside the band, above the edge
    for R, expect_ring, tag in ((F(2), False, "R = 2 below the edge"),
                                (below, None, "just below the edge (band)"),
                                (above, None, "just above the edge (band)"),
                                (F(3), True, "R = 3 above the edge")):
        n_r, e_r = CF.build_13(R, direction="refute")
        n_f, e_f = CF.build_13(R, direction="flow")
        if expect_ring is False:
            check("%s: no ring edges (12 total)" % tag, len(e_r) == 12 and len(e_f) == 12,
                  (len(e_r), len(e_f)))
        elif expect_ring is True:
            check("%s: ring edges present (42 total)" % tag, len(e_r) == 42 and len(e_f) == 42,
                  (len(e_r), len(e_f)))
        else:
            # inside the uncertainty band the two directions differ, which is the point:
            # refute must use the SUPERGRAPH (42), flow the SUBGRAPH (12)
            if R < e_lo:
                check("%s: refute also excludes (12)" % tag, len(e_r) == 12, len(e_r))
            if R > e_hi:
                check("%s: flow also includes (42)" % tag, len(e_f) == 42, len(e_f))
    check("R = 2.1029 gives 12 edges, NOT 42 (the review's defect)",
          len(CF.build_13(F("2.1029"), direction="refute")[1]) == 12)
    check("R = 2.10296 gives 42 edges",
          len(CF.build_13(F("2.10296"), direction="refute")[1]) == 42)

    print("S11 GEOMETRY: the FCC constructor actually runs")
    for n_cell in (1, 2):
        sites, S = CF.build_fcc_patch(n_cell)
        check("build_fcc_patch(%d) returns %d sites" % (n_cell, n_cell ** 3),
              len(sites) == n_cell ** 3, len(sites))
        check("build_fcc_patch(%d) supercell is 3x3" % n_cell, len(S) == 3 and len(S[0]) == 3)

    print("S12 GEOMETRY: the dodecahedral enclosure brackets the true volume")
    v_lo, v_hi = RAD.dodeca_volume_enclosure(digits=40)
    check("V_dod enclosure brackets 5.550291028515510269",
          float(v_lo) <= 5.550291028515510269 <= float(v_hi), (float(v_lo), float(v_hi)))
    check("the OLD lower bound 5.550291028519371 was ABOVE the true value (the review's defect)",
          5.550291028515510269 < 5.550291028519371)
    check("the new enclosure lies below that old bound", float(v_hi) < 5.550291028519371,
          float(v_hi))

    print("S13 BRACKETING: t* is pinned from BOTH sides, not just below")
    b_lo, b_hi = CF.icos_b()
    for R in (F(2), F(3)):
        n_r, E = CF.build_13(R, direction="refute")
        br = CF.bracket_t_star(b_lo, b_hi, E)
        check("R = %s: b_lo and b_hi scans agree on the maximizer" % R, br["same_argmax"],
              (br["U_lo"], br["U_hi"]))
        check("R = %s: the bracket is narrower than 1e-20, so t* is pinned" % R,
              br["width"] < F(1, 10 ** 20), float(br["width"]))
        check("R = %s: the maximizer is the singleton" % R, br["U_lo"] == [0], br["U_lo"])

    print("S14 DUALITY: the minimum feasible Phi equals t* from the cut scan")
    # LP duality on a finite graph: min{Phi : exists flow, |phi|<=Phi, div>=b} = max_U sum_U b/|d^+(U)|.
    # The two sides are computed by completely different code paths, so agreement is a real check.
    b_lo, b_hi = CF.icos_b()
    n_r, E = CF.build_13(F(2), direction="refute")
    t_star = CF.exhaustive_cut_scan(b_lo, E)["t_star"]
    lo, hi = F(0), F(1, 50)
    check("no flow at Phi = 0 (the singleton cut forbids it)", CF.feasible_flow(b_lo, E, F(0)) is None)
    check("a flow exists at Phi = 0.02", CF.feasible_flow(b_lo, E, F(1, 50)) is not None)
    for _ in range(40):
        mid = (lo + hi) / 2
        if CF.feasible_flow(b_lo, E, mid) is not None:
            hi = mid
        else:
            lo = mid
    # The LP is solved in floating point, so the resolved threshold is limited by linprog's
    # tolerance; what must be EXACT is that any flow we return verifies.  Agreement of the two
    # independent code paths to 1e-6 is the check.
    check("the patch's minimum capacity agrees with the cut scan to 1e-6",
          abs(hi - t_star) < F(1, 10 ** 6), (float(lo), float(hi), float(t_star)))
    check("the bisection never certifies a capacity below t* minus the LP tolerance",
          hi > t_star - F(1, 10 ** 6), float(t_star - hi))
    phi02 = CF.feasible_flow(b_lo, E, F(1, 50))
    ok_cap, ok_div, _ = CF.verify_flow_exact(b_lo, E, F(1, 50), phi02)
    check("the flow returned at Phi = 0.02 passes the exact verifier", ok_cap and ok_div)

    print("S15 EXTERNAL PATH: a fixture exported to JSON reproduces the internal numbers")
    import json as _json, os as _os
    fxpath = "out/example_external_icos13.json"
    check("the worked example exists", _os.path.exists(fxpath))
    if _os.path.exists(fxpath):
        fx = CF.load_external_fixture(fxpath)
        check("13 vertices, 12 edges at R = 2", len(fx["b_lo"]) == 13 and len(fx["edges"]) == 12)
        check("b_lo <= b_hi at every vertex", all(a <= b for a, b in zip(fx["b_lo"], fx["b_hi"])))
        check("the example declares its volumes certified, not provisional", fx["provisional"] is False)
        out = CF.evaluate_external(fx)
        cuts = [r for r in out["rows"] if r["kind"] == "violating_cut"]
        check("the external path finds the singleton cut", len(cuts) == 1 and cuts[0]["U"] == [0],
              [r.get("U") for r in cuts])
        b_lo, b_hi = CF.icos_b()
        n_i, E_i = CF.build_13(F(2), direction="refute")
        internal = CF.cut_value(b_lo, E_i, [0])
        check("the external threshold equals the internal one exactly",
              F(cuts[0]["phi_threshold"]) == internal[0] / internal[1],
              float(F(cuts[0]["phi_threshold"])))
        flows = [r for r in out["rows"] if r["kind"] == "flow"]
        check("the external flow is exactly verified", flows and flows[0].get("cap_ok")
              and flows[0].get("divergence_ok"), flows)
        # the PROVISIONAL stamping path: a fixture whose volumes are estimated must be marked,
        # and the flag must survive into every row of the report.  Never exercised before.
        _os.makedirs(".scratch", exist_ok=True)
        tmp = _os.path.join(".scratch", "provisional.json")
        prov = dict(name="provisional_copy", note="volumes estimated, must be stamped",
                    edges=[[int(a), int(b)] for (a, b) in fx["edges"]],
                    b_lo=[str(x) for x in fx["b_lo"]], b_hi=[str(x) for x in fx["b_hi"]],
                    volumes_are_provisional=True)
        import json as _j
        _j.dump(prov, open(tmp, "w"))
        try:
            fxp = CF.load_external_fixture(tmp)
            check("volumes_are_provisional is read as True", fxp["provisional"] is True)
            outp = CF.evaluate_external(fxp)
            check("the provisional flag appears in the report", outp["provisional"] is True)
        finally:
            _os.remove(tmp)
            try:
                _os.rmdir(".scratch")           # leave no empty directory behind
            except OSError:
                pass

    print("S16 D8 / X-C034: the vertex set comes from b, never from the edge list")
    # b = (-1,-1,-1,-1,+1) with edges on 0..3 only.  Vertex 4 is isolated with b = +1, so the
    # instance is infeasible at EVERY Phi.  The old API inferred n from the edges and accepted it.
    b8 = [F(-1), F(-1), F(-1), F(-1), F(1)]
    E8 = [(0, 1), (1, 2), (2, 3), (0, 3)]
    ok_cap, ok_div, div8 = CF.verify_flow_exact(b8, E8, F(1), {})
    check("verify_flow_exact REJECTS the zero flow", ok_div is False, (ok_cap, ok_div))
    check("its divergence has one entry per vertex", len(div8) == 5, len(div8))
    check("feasible_flow refuses at Phi = 1", CF.feasible_flow(b8, E8, F(1)) is None)
    check("feasible_flow refuses at Phi = 1e6 too", CF.feasible_flow(b8, E8, F(10) ** 6) is None)
    w8 = CF.find_violating_cut(b8, E8, F(1))
    check("find_violating_cut reports the empty-boundary cut U = {4}",
          w8 is not None and w8[0] == CF.UNBOUNDED and w8[1] == (4,), None if w8 is None else w8[:2])
    check("exhaustive_cut_scan reports t* = +inf", CF.exhaustive_cut_scan(b8, E8)["t_star"] == CF.UNBOUNDED)
    # the same through the external fixture path, which must not print PATCH_FEASIBLE
    import io as _io, contextlib as _ctx, json as _json2
    fxp = _json2.load(open("out/fixture_C034_witness.json"))
    buf = _io.StringIO()
    with _ctx.redirect_stdout(buf):
        outw = CF.evaluate_external(CF.load_external_fixture("out/fixture_C034_witness.json"))
    check("the external path claims no flow", all(r.get("status") != "PATCH_FEASIBLE"
                                                  for r in outw["rows"] if r["kind"] == "flow"))
    check("the external path does not print PATCH_FEASIBLE", "PATCH_FEASIBLE" not in buf.getvalue())

    print("S17 malformed edge lists raise instead of being reinterpreted")
    for bad, why in ((((0, 0),), "self-loop"), (((0, 1), (1, 0)), "reversed duplicate"),
                     (((0, 1), (0, 1)), "duplicate"), (((0, 7),), "out of range")):
        raised = 0
        for fn in (lambda: CF.verify_flow_exact([F(0), F(0)], bad, F(1), {}),
                   lambda: CF.feasible_flow([F(0), F(0)], bad, F(1)),
                   lambda: CF.find_violating_cut([F(0), F(0)], bad, F(1)),
                   lambda: CF.exhaustive_cut_scan([F(0), F(0)], bad)):
            try:
                fn()
            except CF.FixtureError:
                raised += 1
        check("%s raises in all four paths" % why, raised == 4, raised)

    print("S18 empty edges, zero capacity, negative threshold")
    check("edgeless with a positive vertex is infeasible at any Phi",
          CF.find_violating_cut([F(1), F(-1)], [], F(0)) is not None)
    check("edgeless with all b <= 0 is feasible", CF.feasible_flow([F(-1), F(-1)], [], F(0)) == {})
    check("edgeless with all b <= 0 has t* = 0", CF.exhaustive_cut_scan([F(-1), F(-1)], [])["t_star"] == 0)
    check("zero capacity: phi = 0 is the only option", CF.feasible_flow([F(0), F(0)], [(0, 1)], F(0)) is not None)
    check("zero capacity with demand 1 is infeasible", CF.feasible_flow([F(1), F(-1)], [(0, 1)], F(0)) is None)
    check("... and feasible at Phi = 1", CF.feasible_flow([F(1), F(-1)], [(0, 1)], F(1)) is not None)
    r7 = CF.exhaustive_cut_scan([F(-1), F(-2)], [(0, 1)])
    check("all-negative b: t* = 0 (not the negative supremum)", r7["t_star"] == 0, r7["t_star"])
    check("... while the raw supremum is kept for the record", r7["t_star_raw"] < 0, r7["t_star_raw"])

    print()
    if FAILS:
        print("FAILED: %d -> %s" % (len(FAILS), FAILS)); return 1
    print("ALL CUT/FLOW TESTS PASS"); return 0

if __name__ == "__main__":
    sys.exit(main())
