#!/usr/bin/env python3
"""Emit a PRUNE json for the route "reprove `ergodic_wild_fourier`".

Reuses m10's sound declaration graph (DECLGRAPH.log) + SPANS.json rather than
building a second harness.  The route keeps
  * `fourier_vanish_of_terminal` (the downstream Fourier machinery), and
  * `relative_difference_invariant` (needed for IsWild),
because the replacement proof (`Residual.lean`) uses exactly those, plus
m5's Theorem A and one hypothesis `TerminalObligation`.
"""
import json, pathlib, sys

H = pathlib.Path("sprint/simplify/m10/harness").resolve()
sys.path.insert(0, str(H))
_argv, sys.argv = sys.argv, ["analyze.py", "stats"]      # analyze.py runs main() on import
from analyze import load, closure, ROOTS, spans   # noqa: E402
sys.argv = _argv

TARGET = "OAI.PlaneFiveColor.Spectral.ergodic_wild_fourier"
KEEP = ["OAI.PlaneFiveColor.Spectral.fourier_vanish_of_terminal",
        "OAI.Analysis.PlaneSpectrum.relative_difference_invariant",
        # used by m5's Theorem A (TheoremA.lean), which the tree does not know about
        "OAI.PlaneFiveColor.Spectral.j_injective",
        "OAI.PlaneFiveColor.Spectral.scalarHom"]

nodes, et, ev = load()
sp = spans()
drop = {TARGET}
keep = set(KEEP)
drop = drop - keep
full = closure(nodes, et, ev)
red = closure(nodes, et, ev, drop_v=drop, roots=ROOTS + sorted(keep))
freed = full - red

prune = {"drop_decls": {}, "drop_modules": [], "drop_imports": {}}
lost = 0
for n in sorted(freed):
    if n in sp:
        prune["drop_decls"][n] = sp[n]
        lost += sp[n]["lines"]
    else:
        print("no span (kept in source):", n, file=sys.stderr)

out = pathlib.Path(".ultramath/smwg224wy/m6/PRUNE8.json")
out.write_text(json.dumps(prune, indent=1))
print(f"{len(prune['drop_decls'])} declarations, {lost} lines -> {out}")
names = set(prune["drop_decls"])
for k in ["OAI.EuclideanFiveColor.FactorLp.space", "OAI.EuclideanFiveColor.FactorLp.exists_rep",
          "OAI.EuclideanFiveColor.RelativeProduct.law",
          "OAI.EuclideanFiveColor.RelativeProduct.law_eq_mixture",
          "OAI.EuclideanFiveColor.RelativeProduct",
          "OAI.EuclideanFiveColor.IsWild",
          "OAI.PlaneFiveColor.Spectral.exists_terminal_factor",
          "OAI.PlaneFiveColor.Spectral.UniversalGood",
          "OAI.PlaneFiveColor.Spectral.ergodic_wild_fourier",
          "OAI.PlaneFiveColor.Spectral.fourier_vanish_of_terminal"]:
    print(("DROPPED " if k in names else "kept    ") + k)
