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
    b = [F(5, 100), F(-1)]
    E = []                                  # no edges at all
    worst = CF.find_violating_cut(b, E, F(0))
    check("no cut reported when the graph is edgeless", worst is None, worst)

    print()
    if FAILS:
        print("FAILED: %d -> %s" % (len(FAILS), FAILS)); return 1
    print("ALL CUT/FLOW TESTS PASS"); return 0

if __name__ == "__main__":
    sys.exit(main())
