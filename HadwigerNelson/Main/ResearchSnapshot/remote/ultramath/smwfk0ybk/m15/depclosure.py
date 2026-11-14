#!/usr/bin/env python3
"""Import-closure of the transfer's Lean statement (route (e) diagnostics).

Computes, for a Lean module of lean/OAI, the transitive closure of its `import OAI.…`
lines, with line counts.  Used to quantify what route (e) could shrink and what it cannot:
the transfer enters the rigidity theorem exactly once, through

    PlaneColoring/BorelTransfer.projected_unit_correlation
        <- PlaneSpectrum/Ergodicity.residual_fourier
        <- PlaneSpectrum/Ergodicity.finite_wild_fourier
        <- PlaneSpectrum/Ergodicity.wild_fourier          (the rigidity input, in form (R))

Run:  python3 depclosure.py
"""
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
OAI = os.path.join(ROOT, "lean", "OAI")
IMPORT = re.compile(r"^import\s+OAI\.([A-Za-z0-9_.]+)", re.M)


def mod_path(name):
    return os.path.join(OAI, *name.split(".")) + ".lean"


def imports_of(path):
    with open(path, encoding="utf-8", errors="replace") as fh:
        src = fh.read()
    return IMPORT.findall(src)


def closure(root_module):
    seen, stack = set(), [root_module]
    while stack:
        m = stack.pop()
        if m in seen:
            continue
        p = mod_path(m)
        if not os.path.exists(p):
            print("  (missing module file: %s)" % m)
            continue
        seen.add(m)
        stack.extend(imports_of(p))
    return seen


def lines(m):
    with open(mod_path(m), encoding="utf-8", errors="replace") as fh:
        return sum(1 for _ in fh)


def total(members):
    return sum(lines(m) for m in members)


if __name__ == "__main__":
    all_mods = set()
    for dirpath, _, files in os.walk(OAI):
        for f in files:
            if f.endswith(".lean"):
                rel = os.path.relpath(os.path.join(dirpath, f), OAI)[:-5]
                all_mods.add(rel.replace(os.sep, "."))
    print("lean/OAI: %d modules, %d lines" % (len(all_mods), total(all_mods)))

    cf = {m for m in all_mods if m.startswith("MeasureTheory.CompactFactors")}
    print("MeasureTheory.CompactFactors: %d modules, %d lines" % (len(cf), total(cf)))
    ps = {m for m in all_mods if m.startswith("Analysis.PlaneSpectrum")}
    print("Analysis.PlaneSpectrum: %d modules, %d lines\n" % (len(ps), total(ps)))

    for target in ["Geometry.PlaneColoring.BorelTransfer",
                   "Geometry.PlaneColoring.WeakColoring",
                   "Analysis.PlaneSpectrum.Ergodicity"]:
        c = closure(target)
        inroot = c & all_mods
        print("%-45s closure %3d modules, %6d lines" % (target, len(inroot), total(inroot)))
        print("    CompactFactors in closure: %d modules, %d lines"
              % (len(inroot & cf), total(inroot & cf)))
        print("    PlaneSpectrum   in closure: %d modules, %d lines"
              % (len(inroot & ps), total(inroot & ps)))
        if target.endswith("BorelTransfer"):
            print("    transfer-only part (closure minus closure of Ergodicity): %d modules, %d lines"
                  % (len(inroot - closure("Analysis.PlaneSpectrum.Ergodicity")),
                     total(inroot - closure("Analysis.PlaneSpectrum.Ergodicity"))))
        print()

    # the rigidity chain, module by module
    print("rigidity chain:")
    for m, ln in [("Analysis.PlaneSpectrum.Basic", "IsWild, wild_coset_null"),
                  ("Analysis.PlaneSpectrum.Ergodicity", "wild_fourier, finite_wild_fourier, residual_fourier"),
                  ("Geometry.PlaneColoring.BorelTransfer", "projected_unit_correlation, proper_to_weak")]:
        print("  %-42s %4d lines   %s" % (m, lines(m), ln))
