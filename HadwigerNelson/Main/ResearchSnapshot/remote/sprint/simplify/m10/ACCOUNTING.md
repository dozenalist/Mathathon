# Measured cost account of the routes (m10 / d4)

Method (all of it reproducible, none of it an opinion):

* `harness/declgraph.lean` — a Lean metaprogram that walks the **proof-term** closure of the
  7 headline declarations and prints `NODE <module> <name>`, `EDGET p c` (c in p's type),
  `EDGEV p c` (c in p's proof/value). Mathlib is not followed (it is compiled before `OAI`,
  so it cannot mention `OAI`), which makes it exact for `OAI` and cheap (24 s warm).
  Result: **3538 declarations, 7910 type-edges, 15036 value-edges**.
* `harness/spans.py` — namespace-aware declaration spans → `SPANS.json`
  (2575 declarations; 28539 of the 31277 lines are covered by a declaration span).
* `harness/analyze.py free NAME...` — route cost: delete the **value**-edges of the
  declarations a route reproves, keep all type-edges (their statements survive), recompute
  the closure, and add up the spans of everything that is no longer reached.

## Baseline

83 modules, **31277 raw lines / 29100 code lines**. All 7 headline declarations depend on
exactly `[propext, Classical.choice, Quot.sound]` (`BASELINE.cert`).

## Module-level deletion is capped at 198 lines

`graph.py reach` from the 5 headline modules covers 82/83 modules / 31204 lines. The sound
declaration walk is sharper: exactly **three** modules have no declaration in the closure —

| module | lines | verdict |
|---|---|---|
| `Geometry/PlaneColoring/ConnectedUnitFree` | 73 | no consumer at all; delete |
| `Geometry/PlaneColoring/MeasurableAssembly` | 57 | only `exists_measurable_proper_seven` (not a listed asset) |
| `Geometry/PlaneColoring/MeasurableProper` | 68 | same |

**Therefore no purely mechanical module-level trim can reach 1500.** Anything ≥1500 has to
change what is proved *inside* `exists_terminal_factor` (Stationary.lean:126).

## Route costs (value-edges deleted at the route's target, type-edges kept)

| route | value-edges deleted at | freed decl lines | modules emptied |
|---|---|---|---|
| R3 cheaper UniversalGood propagation | `relative_singularity_approximation` | **354** | — |
| R2/R5/R6 as mechanical Zorn replacements | `CodedMax.exists_maximal`, `ChainJoin.approximation` | **0** each | — |
| R1/R2 real: new `exists_terminal_factor`, keeping the compact-tower engine `CompactTower.strict_compact_successor` | that + `CodedMax.exists_maximal` | **4112** | `PhaseCollision` 537, `PhaseEncoding` 255, `SmallArcs` 322, `Centers` 703 |
| R1 absolute upper bound (nothing kept) | `exists_terminal_factor` | **5682** | + `Functions` 884 |
| R8 (Theorem 2.3 reproved) absolute upper bound | `ergodic_wild_fourier` | **12050** | the whole tower |

R1/R2 keep-engine detail (declaration lines freed):
`Centers` 660, `PhaseCollision` 445, `ConditionalSpectrum` 435, `ConditionalLimits` 396,
`RelativeCenters` 380, `Approximation` 373, `Factors` 356, `ConditionalSelection` 350,
`SmallArcs` 290, `PhaseEncoding` 233, `Basic` 194.  Full list: `harness/R1-FREED.txt`.

The closed import chain the sprint brief names is exactly
`PhaseEncoding 255 + PhaseCollision 537 + SmallArcs 322 + ConditionalSelection 442 +
ConditionalSpectrum 497 = **2053**`, and it hangs off the single declaration
`relative_singularity_approximation` (ConditionalLimits:622) — this measurement confirms
the 2053 figure and shows nothing else holds it up.

## Verdicts

* **R3 cannot reach 1500** (354). Certified dead as a standalone route.
* **R2/R5/R6 save nothing by themselves** (0): replacing Zorn by recursion or by a
  countable reduction frees no declaration line, and each adds code.
* **R1 and R2 carry the same prize (≈4100 freed)** and differ only in the engine
  (join-closure of compact extensions + Zorn vs ordinal recursion). Both need Theorem A
  formalised (d2/R4) and the (H2) supply for each wild `d`.
* Between 1500 and 4100 the margin is ~2500 lines, so R1 survives even if the replacement
  proof re-uses most of what it could have deleted.
