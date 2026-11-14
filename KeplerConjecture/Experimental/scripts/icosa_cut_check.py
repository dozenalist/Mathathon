#!/usr/bin/env python3
"""
Cut/flow check for the icosahedral 13-cluster (K15-E070, K15-E045a/b, (H_R)).

Verifies, for the fixture in ICOSA_CUT_PACKAGE.md:
  (1) |N_R({c})| = 12 for R in {2.09, 2.11, 2.2}   -- the cut has twelve payers
  (2) the complete exact distance table                -- geometry is as documented
  (3) the certified surplus bracket on the cut         -- [-1.279, +inf)
  (4) the extent flag on a sample completion           -- provisional data is flagged

All distance checks are EXACT (sympy over Q(sqrt2,sqrt5)); numpy is used only for
the sample completion in (4), whose numbers are provisional by construction.

Run: python3 Experimental/scripts/icosa_cut_check.py
Exit 0 always; results printed and written to Experimental/evidence/.
"""
import json, sys
import sympy as sp
import numpy as np
sys.path.insert(0, "Experimental/scripts")

OUT = {}
def say(s):
    print(s); OUT.setdefault("log", []).append(s)

# ---------- exact construction in Q(sqrt2, sqrt5) ----------
phi = (1 + sp.sqrt(5)) / 2
scale = 2 * sp.sqrt(2) / sp.sqrt(5 + sp.sqrt(5))     # 2/sqrt(2+phi)
raw = []
for a in (1, -1):
    for b in (1, -1):
        raw += [(0, a, b*phi), (a, b*phi, 0), (a*phi, 0, b)]
V = [tuple(sp.simplify(scale*sp.sympify(t)) for t in v) for v in raw]
C = (sp.Integer(0), sp.Integer(0), sp.Integer(0))
assert len(V) == 12

def d2(p, q):
    return sp.simplify(sum((sp.sympify(p[i]) - sp.sympify(q[i]))**2 for i in range(3)))

say("=== (1) the cut: |N_R({c})| ===")
dc = [sp.sqrt(d2(C, v)) for v in V]
say(f"  distance centre->neighbour, exact: {sp.simplify(dc[0])}")
assert all(sp.simplify(x - 2) == 0 for x in dc), "centre-neighbour distance must be exactly 2"
say("  all twelve centre-neighbour distances are exactly 2 (tangency)")
for R in ("2.09", "2.11", "2.2"):
    n = sum(1 for x in dc if sp.nsimplify(R) >= x)
    say(f"  R = {R:>5} -> |N_R({{c}})| = {n}")
    assert n == 12
OUT["cut_size"] = {"2.09": 12, "2.11": 12, "2.2": 12}

# ---------- (2) exact distance table ----------
say("")
say("=== (2) exact distance table among the twelve outer centres ===")
buckets = {}
for i in range(12):
    for j in range(i+1, 12):
        d = sp.simplify(sp.sqrt(d2(V[i], V[j])))
        buckets.setdefault(str(sp.nsimplify(d)), 0)
        buckets[str(sp.nsimplify(d))] += 1
for k in sorted(buckets, key=lambda t: float(sp.sympify(t))):
    say(f"  distance {k}  (={float(sp.sympify(k)):.10f})  count {buckets[k]}")
total = sum(buckets.values())
say(f"  total pairs = {total} (must be 66)")
assert total == 66
OUT["distance_table"] = buckets

# ---------- (3) certified surplus bracket ----------
say("")
say("=== (3) certified surplus bracket on the cut ===")
R32 = sp.sqrt(32); Vd = (15 + 7*sp.sqrt(5))/4 * (4/sp.sqrt(10 + 22/sp.sqrt(5)))**3
deficit = sp.simplify(R32 - Vd)
lo = sp.simplify(12*(Vd - R32))
say(f"  deficit d(c) = sqrt32 - V_dodeca = {sp.N(deficit,12)}")
say(f"  certified LOWER bound on the cut surplus = 12*(V_dodeca - sqrt32) = {sp.N(lo,10)}")
say(f"  required: surplus >= d(c) = {sp.N(deficit,10)}")
say(f"  => the certified bound does NOT cover the deficit; gap = {sp.N(deficit - lo,10)}")
OUT["surplus_bracket"] = {"lower_certified": float(lo), "required": float(deficit),
                          "upper": "infinity (no certified upper bound)"}

# ---------- (4) extent flag on a sample completion ----------
say("")
say("=== (4) extent flag on a sample completion (PROVISIONAL) ===")
try:
    import block_evaluator as BE
    P = BE.fill(BE.icosa_cluster(), 7.0, seed=4)
    vol, touched = BE.vor_volumes(P)
    payers = list(range(1, 13))
    flagged = int(sum(touched[i] for i in payers))
    say(f"  completion n={len(P)}; payer cells flagged (extent > 2): {flagged} of 12")
    say(f"  => {'UNRELIABLE' if flagged else 'usable'} as surplus data (K15-E062)")
    OUT["sample_completion"] = {"n": int(len(P)), "payers_flagged": flagged,
                                "usable": bool(flagged == 0)}
except Exception as e:
    say(f"  sample completion skipped: {e!r}")
    OUT["sample_completion"] = {"error": repr(e)}

OUT["verdict"] = ("(1)-(2) exact and PASS; (3) certified lower bound is negative, so the "
                  "cut cannot be discharged by per-cell minima; (4) flagged if not saturated.")
say("")
say(OUT["verdict"])
with open("Experimental/evidence/icosa_cut_check.json", "w") as f:
    json.dump(OUT, f, indent=1, default=str)
say("written Experimental/evidence/icosa_cut_check.json")
