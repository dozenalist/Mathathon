# Hadwiger–Nelson: verified lower bound, sharpenings, and the six-colour barrier

This repository contains the work of a session that combined three sources — the standing problem
statement, the 62-page proof that the plane is not five-colourable (OpenAI, 23 Sep 2026), and its
78-module Lean development — and produced the following.

## Read this first

* **[results/REPORT.md](results/REPORT.md)** — the full report: what was verified, what is new,
  where the method stops, and what would be needed to settle `chi(R^2) = 6` or `7`.
* **[results/SPINE.md](results/SPINE.md)** — the proof in twelve steps, with the Lean module for each.

## The theorem, machine-checked here

`OAI.EuclideanFiveColor.no_proper_five_coloring` (no proper 5-colouring of the plane) and
`OAI.Problem160.properColoring_seven` (a proper 7-colouring) compile under Lean 4.34.1 with mathlib
`d13f23b`, 78/78 modules, zero patches, and depend only on `[propext, Classical.choice, Quot.sound]`.

```bash
bash scripts/fetch_exact_env.sh     # Lean 4.34.1 + pinned mathlib, cached
source scripts/env4341.sh
python3 scripts/build_lean.py       # 78 modules in topological order
lean results/lean/Check3.lean       # axiom certificate
```

## New results proved here

* **T1** ([results/T1-algebraic-plane.md](results/T1-algebraic-plane.md)): `chi(E) = chi(C)` where
  `E` is the countable algebraic plane. Machine-checked
  (`Transfer.lean`, `algebraic_colorable_iff`); it also locates any finite witness in `E`.
* **T2** ([results/T2-null-sets.md](results/T2-null-sets.md)): deleting any Lebesgue-null set does
  not make the plane 5-colourable. Machine-checked (`NullSetRobust.lean`).
* **The connected-set exclusion** of §7 is pure connectedness: connected unit-free sets have
  diameter at most one. Machine-checked in a general normed space (`ConnectedUnitFree.lean`).
* **`6 <= chi <= 7`** as a theorem about the development's own `planeChromaticNumber`
  (`Chromatic.lean`, contributed by a swarm member and integrated).
* **The six-colour barrier** ([results/K6-BARRIER.md](results/K6-BARRIER.md)): the printed
  architecture is a `k <= 5` argument; the three exact failures at `k = 6`.
* **A referee-checkable compression** of the whole proof, with a dependency DAG and an explicit list
  of accepted steps: [results/COMPRESSED-PROOF.md](results/COMPRESSED-PROOF.md).
* **Errata triage** ([results/ERRATA-TRIAGE.md](results/ERRATA-TRIAGE.md)): five reported defects
  in the paper are artifacts of `pdftotext`; each was checked against the rendered page.

## Layout

| path | contents |
|---|---|
| `attachments/` | the three sources |
| `lean/OAI/` | the 78-module development, plus the new modules |
| `results/` | the report and all supporting documents |
| `scripts/` | exact-environment fetch, build script, logs |
| `.ultramath/` | the twelve-member swarm's own directories |
