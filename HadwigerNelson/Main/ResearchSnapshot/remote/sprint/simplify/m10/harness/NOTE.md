# d4 status

Published: `graph.py` (module graph + line counting), `hbuild.py` (parallel
topological builder, env-script driven so the same script serves both toolchains),
`certify.py` + `frozen.lean` (statement freeze + axiom certificate),
`linecount.py` (before/after gate), `BASELINE.json`, `BASELINE.cert`.

Baseline facts, measured, not estimated:
* 83 modules, 31277 raw lines, 29100 code lines.
* `graph.py reach` from the five headline modules (`Five`, `Seven`, `Transfer`,
  `Chromatic`, `NullSetRobust`) already covers **82 of 83 modules / 31204 lines**.
  Module-level deletion is therefore worth at most ~73 lines; only
  declaration-level cutting or a restructure can reach 1500.
* Axioms of all 7 headline declarations: `[propext, Classical.choice, Quot.sound]`.
