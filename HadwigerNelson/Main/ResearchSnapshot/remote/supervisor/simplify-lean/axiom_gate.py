#!/usr/bin/env python3
"""Gate for AxiomRoots.lean output. Axiom sets must be SUBSETS of the three standard axioms.
Usage: lean AxiomRoots.lean > out.txt 2>&1 ; python3 axiom_gate.py out.txt
Exit 0 = every root within the standard set; 1 = a violation (sorryAx or a custom axiom);
2 = a root missing from the output.
Accepted: 'depends on axioms: [propext]', '[propext, Quot.sound]', '[...all three...]',
and Lean's line-wrapped multi-line form. Subsets are normal: not every theorem uses all three."""
import re, sys
ALLOWED = {"propext", "Classical.choice", "Quot.sound"}
# Part A: the affected surface. Missing = FAIL (the file did not elaborate).
REQUIRED = ["uniform_precision_contradiction",
         "finite_uniform_precision_contradiction",
         "ambient_uniform_precision_contradiction",
         "finite_uniform_successor_contradiction",
         "relative_singularity_successor",
         "relative_singularity_approximation",
         "no_proper_five_coloring"]
# Part B: unaffected upper-bound roots. Checked if present; absence is NOT a failure.
OPTIONAL = ["properColoring_seven", "weakMeasurableColoring_seven"]
ROOTS = REQUIRED + OPTIONAL
txt = open(sys.argv[1], errors="ignore").read()
# join Lean's wrapped axiom lists: "'name' depends on axioms: [a,\n  b]"
flat = re.sub(r"\n\s+", " ", txt)
found, bad, missing = {}, [], []
for r in ROOTS:
    m = re.search(r"'([^']*\.)?" + re.escape(r) + r"' depends on axioms: \[([^\]]*)\]", flat)
    if not m:
        if r in REQUIRED: missing.append(r)
        else: print(f"  absent (optional, unaffected)  {r}")
        continue
    ax = {a.strip() for a in m.group(2).split(",") if a.strip()}
    found[r] = sorted(ax)
    if "sorryAx" in ax: bad.append((r, "sorryAx present -- transplanted body not substituted"))
    elif not ax <= ALLOWED: bad.append((r, "non-standard: " + ", ".join(sorted(ax - ALLOWED))))
for r in ROOTS:
    if r in found: print(f"  {'PASS' if (set(found[r])<=ALLOWED and 'sorryAx' not in found[r]) else 'FAIL'}  {r}  {found[r]}")
for r in missing: print(f"  MISSING  {r}  (no 'depends on axioms' line -- did the file elaborate?)")
for r, why in bad: print(f"  FAIL  {r}: {why}")
ok = not bad and not missing
print("GATE:", "PASS" if ok else "FAIL", f"({len(found)}/{len(ROOTS)} roots, allowed={sorted(ALLOWED)})")
sys.exit(0 if ok else (2 if missing else 1))
