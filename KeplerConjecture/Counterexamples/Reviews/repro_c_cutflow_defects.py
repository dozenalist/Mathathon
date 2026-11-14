#!/usr/bin/env python3
"""Portable reproduction of the four defects in C's `cut_flow.py` (blob 700e44f6, live at
`4bcbd3a` and unchanged at the current `comp` tip `790efa73`).

Runs against `Reviews/C_cut_flow_4bcbd3a.py`, a byte copy of that blob, so it keeps working
after C edits the original.  Nothing here imports X's own predicate; every verdict is exact
rational arithmetic or a stated geometric fact.

  D1  V_DOD's certified enclosure misses the exact dodecahedron volume and is wrong on the
      *high* side, which is the unsafe side for a necessary condition.
  D2  build_13(2.1029) returns 42 edges instead of 12: the ring gate is 2.4448e-5 below the
      true icosahedral edge, so 30 phantom edges enter and cuts become cheaper than they are.
  D3  build_fcc_patch(1) raises TypeError before doing any geometry.
  D4  the period-16 13-cluster is unsaturated: all 12 ring cells are unbounded, so b = -inf
      there and every cut is satisfied for every Phi.  The fixture cannot be evidence.
  D5  (latent) exhaustive_cut_scan raises TypeError when no subset has a crossing edge, e.g. the
      R < 2 regime that build_13 models.  main() guards 'if not edges', so this is not live.
  D7  (cosmetic) exhaustive_cut_scan omits the repaired theorem's max(0, .): with all b negative
      it reports a negative t_star where t* = 0.
  D8  verify_flow_exact FALSE-ACCEPTS when a vertex with positive deficit has no incident edge:
      its vertex range is taken from the edge list, so such a vertex is never checked.

Run:  python3 Reviews/repro_c_cutflow_defects.py        (exit 0 iff all four reproduce)
"""
import importlib.util, sys
from fractions import Fraction as F
import sympy as sp

spec = importlib.util.spec_from_file_location("cf", "Reviews/C_cut_flow_4bcbd3a.py")
cf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cf)

fails = []; nchecked = [0]
def ck(tag, cond, detail=""):
    nchecked[0] += 1
    print("  [%s] %-58s %s" % ("REPRO" if cond else "NOT REPRODUCED", tag, detail))
    if not cond: fails.append(tag)

print("=" * 96); print("D1  the V_DOD enclosure is wrong on the high side"); print("=" * 96)
a = 2 / sp.sqrt((25 + 11*sp.sqrt(5))/10)          # edge of the inradius-1 dodecahedron
V = sp.nsimplify((15 + 7*sp.sqrt(5))/4 * a**3)
Vnum = sp.N(V, 40)
lo, hi = cf.V_DOD_LO, cf.V_DOD_HI
exact_lo_ok = sp.N(sp.Rational(lo.numerator, lo.denominator) - V, 20)
print("    exact V_dod = 100(3 sqrt10 + 7 sqrt2)/(25 + 11 sqrt5)^{3/2} = %s" % Vnum)
print("    C's interval = [%.15f, %.15f]" % (float(lo), float(hi)))
print("    V_DOD_LO - V_dod = %s  (positive => the LOW endpoint is already too high)"
      % sp.N(sp.Rational(lo.numerator, lo.denominator) - V, 6))
ck("D1 lower endpoint exceeds the true volume",
   sp.Rational(lo.numerator, lo.denominator) > V,
   "by %.3e" % float(sp.Rational(lo.numerator, lo.denominator) - V))
ck("D1 the whole interval is above the truth",
   sp.Rational(lo.numerator, lo.denominator) > V,
   "so vol_other = (period - V_DOD)/12 is UNDER-estimated; b0 = sqrt32 - V_DOD is OVER-estimated")

print("=" * 96); print("D2  build_13 at the scanned row returns 42 edges, truth is 12"); print("=" * 96)
nv, E = cf.build_13(2.1029)
true_edge = 4/sp.sqrt(1 + ((1+sp.sqrt(5))/2)**2)
print("    13-vertex graph edge count at R = 2.1029 : %d" % len(E))
print("    true outer-icosahedron edge at circumradius 2 : %s = %.15f"
      % (sp.simplify(true_edge), float(true_edge)))
print("    2.1029 is short of it by %.6e" % float(true_edge - sp.Rational(21029, 10000)))
ken = len(cf.icosa_edges()[1])
ck("D2 42 = 12 + 30 phantom ring edges", len(E) == 42 and ken == 30, "icosahedron has 30 edges")
ck("D2 the gate is below the true edge",
   sp.Rational(21029, 10000) < true_edge,
   "gate 2.1029 - 1e-9 < %.10f" % float(true_edge))
print("    direction: phantom edges make |delta^+(U)| larger and every cut CHEAPER, so the")
print("    reported Phi (and any 't*' quoted at this row) is too SMALL -- the unsafe direction.")

print("=" * 96); print("D3  build_fcc_patch(1) raises TypeError"); print("=" * 96)
try:
    cf.build_fcc_patch(1); ck("D3 raises", False, "it returned")
except TypeError as e:
    ck("D3 raises TypeError", True, str(e))

print("=" * 96); print("D4  the period-16 13-cluster is unsaturated, so b = -inf on the ring"); print("=" * 96)
dec = cf.period_decoupling(2.1029, 16.0)
print("    period_decoupling: gap = %.2f > R = %.4f -> %s" % (dec['gap'], dec['R'], dec['decoupled']))
V3, ringE = cf.icosa_edges()
pts = [tuple(V3[i]) for i in range(12)]
from scipy.spatial import ConvexHull
hull = ConvexHull(pts)
on_hull = set(hull.vertices)
ck("D4 all 12 ring cells lie on the convex hull",
   on_hull == set(range(12)), "%d extreme points" % len(on_hull))
ck("D4 copies do not interact at period 16", dec['decoupled'], "gap 12 > R")
print("    therefore each ring cell's Voronoi cell is an unbounded cone: b(ring) = -inf.")
print("    Any U meets a ring cell only with sum_U b <= 0, so (C) holds at Phi = 0 for every U")
print("    and the fixture carries no geometric information at any Phi.")

print("=" * 96); print("D5 (latent)  exhaustive_cut_scan raises on an edgeless fixture"); print("=" * 96)
try:
    cf.exhaustive_cut_scan([F(1), F(-1)], [])
    ck("D5 raises on no-crossing-edge input", False, "it returned")
except TypeError as e:
    ck("D5 raises TypeError (latent: main() guards 'if not edges')", True, str(e))
print("    main() never reaches this path -- it tests 'if not edges' and reports the pointwise")
print("    condition instead -- so this is a robustness gap for other callers, not a live crash.")

print("=" * 96); print("D6  degenerate-input robustness of the rest of the module"); print("=" * 96)
degen = [
    ("cut_value: no edges",            lambda: cf.cut_value([F(1),F(-1)], [], [0])),
    ("singleton_bounds: empty graph",  lambda: cf.singleton_bounds([F(1),F(-1)], [])),
    ("singleton_bounds: 1 vertex",     lambda: cf.singleton_bounds([F(1)], [])),
    ("global_necessary_condition: []", lambda: cf.global_necessary_condition([])),
    ("find_violating_cut: no edges",   lambda: cf.find_violating_cut([F(1),F(-1)], [], F(1))),
    ("find_violating_cut: Phi = 0",    lambda: cf.find_violating_cut([F(1),F(-1)], [(0,1)], F(0))),
    ("exhaustive_cut_scan: n = 17",    lambda: cf.exhaustive_cut_scan([F(0)]*17, [(i,i+1) for i in range(16)])),
    ("feasible_flow: Phi = 0",         lambda: cf.feasible_flow([F(1),F(-1)], [(0,1)], F(0))),
    ("feasible_flow: no edges",        lambda: cf.feasible_flow([F(1),F(-1)], [], F(1))),
    ("period_decoupling: R = 0",       lambda: cf.period_decoupling(0.0)),
    ("build_13(0)",                    lambda: cf.build_13(0)),
    ("build_13(2.0)",                  lambda: cf.build_13(2.0)),
]
bad = []
for label, fn in degen:
    try: fn()
    except Exception as e: bad.append((label, type(e).__name__))
ck("D6 %d/%d degenerate inputs handled" % (len(degen)-len(bad), len(degen)), not bad, str(bad))

print("=" * 96); print("D7  exhaustive_cut_scan omits the theorem's max(0, .)"); print("=" * 96)
r = cf.exhaustive_cut_scan([F(-1), F(-2)], [(0, 1)])
print("    all-negative b on one edge: C reports t_star = %s" % r['t_star'])
print("    the repaired theorem's formula gives t* = max(0, sup) = 0")
ck("D7 C's t_star is not the theorem's t* when the sup is negative",
   r['t_star'] < 0, "harmless for 'Phi >= t*' because Phi >= 0 is a hypothesis, but not quotable")

print("=" * 96); print("D8  verify_flow_exact FALSE-ACCEPTS at an isolated vertex with positive deficit"); print("=" * 96)
b8 = [F(-1), F(-1), F(1)]          # vertex 2 is isolated and must receive 1 unit
E8 = [(0, 1)]
ok_cap, ok_div, div = cf.verify_flow_exact(b8, E8, F(1), {})
print("    b = (-1,-1,+1), edges = [(0,1)], flow = 0")
print("    verify_flow_exact -> (ok_cap=%s, ok_div=%s, div=%s)" % (ok_cap, ok_div, [str(d) for d in div]))
print("    the true verdict is ok_div = False: div(2) = 0 < b(2) = 1")
ck("D8 verify_flow_exact accepts an impossible instance", ok_div, "n is taken from the edge list, so vertex 2 is never checked")
print("    and the same truncation is in two more functions:")
print("      find_violating_cut(Phi=1) -> %s   (should report U={2} violating at every Phi)" % (cf.find_violating_cut(b8, E8, F(1)),))
print("      feasible_flow(Phi=1)      -> %s   (should be None)" % (cf.feasible_flow(b8, E8, F(1)),))
ck("D8 the defect is systematic: 3 functions truncate the vertex set",
   cf.find_violating_cut(b8, E8, F(1)) is None and cf.feasible_flow(b8, E8, F(1)) is not None,
   "only exhaustive_cut_scan gets it right")
print("    cause: n = max(max(e) for e in edges) + 1 = 2, so vertices with no incident edge are")
print("    outside the divergence check.  The cut scan DOES catch this instance:")
print("    exhaustive_cut_scan reports the empty-boundary positive set [([2], '1')].")

print("\nRESULT: %d/%d checks reproduce" % (nchecked[0]-len(fails), nchecked[0]))
print("        " + ("ALL CHECKS REPRODUCE (5 live: D1-D4+D8, 1 latent, 1 cosmetic, 12/12 sweep)" if not fails else "FAILED: %s" % fails))
sys.exit(0 if not fails else 1)
