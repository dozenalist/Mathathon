# S1 banking manifest (simplification desk)

Generated 2026-11-15T03:45Z by `tools/make_manifest.py s1`. Lean 4.34.1 (commit 5045d005), Mathlib d13f23b; all desk runs are local, one Lean process at a time.

## Claim

Lemma 6.7 (`five_support_step_ban`) is proved branch-free under its original name and statement. `five_forced_label` (Exclusion) is replaced by `five_state_forced_label`, a one-call `decide` lemma in disjunction form. 25 declarations that no root theorem reaches are deleted from the 27-module R1 closure, and sections left empty are removed.

| Measure | vs accepted R1 | vs supplied original |
|---|---|---|
| physical lines | -265 | -415 |
| nonblank lines | -261 | -431 |
| code lines | -255 | -463 |

Files changed vs R1: 14. Declarations removed: 25 unreachable plus `five_forced_label` (replaced). Added: `five_state_forced_label`.

Public statements: every declaration surviving from R1 keeps its exact type, binder flags, universe parameters and definition-value hash. This is checked by the signature gate below.

## Files (changed vs R1)

| Module | R1 lines | new lines | delta | sha256 (raw = LF) |
|---|---|---|---|---|
| OAI.Geometry.PlaneColoring.AngularBoundary | 503 | 497 | -6 | `796414de07e4fb2ce5ae862530bc85742e6ba318ce6c12307644265d08e6c663` |
| OAI.Geometry.PlaneColoring.BoundaryTrace | 367 | 313 | -54 | `6bb884aa073edd320672ede4145b8488af533c82550606603ea3da49683ab017` |
| OAI.Geometry.PlaneColoring.ContinuumLimits | 353 | 337 | -16 | `cfa79b5f6d8e9449b0ef6beb8a8d40265cec5a9d939dfb14979389fed5081ca0` |
| OAI.Geometry.PlaneColoring.CyclicCore | 280 | 256 | -24 | `d55a1601a3d9d3679cc2ae6d16302f1eac71d71ace20a21c276c81e2e3d164ab` |
| OAI.Geometry.PlaneColoring.DiskExtension | 611 | 603 | -8 | `ef64358d8261d6a96c8b03469bee12f2ab0abd4647a9f1230b41059fc914ac64` |
| OAI.Geometry.PlaneColoring.Exclusion | 165 | 163 | -2 | `1613d1543f72813e05301a0e141e684bb4289e65a8d4905cc4f47b32057c8b67` |
| OAI.Geometry.PlaneColoring.FiveSupport | 354 | 337 | -17 | `b12dad93faddcbaf07dcb6e92a86c36ffb1e3a80f62192e64916ae936599eb65` |
| OAI.Geometry.PlaneColoring.FourContinuity | 509 | 503 | -6 | `46efa82aa091fd03ebe10a4d61142f96ad4f8a8533d7c84fa2d8117d5e18c6c9` |
| OAI.Geometry.PlaneColoring.GraphCuts | 314 | 310 | -4 | `9aa4f41d6e5ffc105ef0d1e416491e0c7dce2fd59735179545730098a4f06830` |
| OAI.Geometry.PlaneColoring.GraphRealization | 415 | 410 | -5 | `def12054e6260a4b85dfd13d19a06dc6355f39fb8cbeadbfe1ef1fa45f2e2d7a` |
| OAI.Geometry.PlaneColoring.HoleApproximation | 328 | 323 | -5 | `cbee4d2ae2fcf691333a7d21b274ddbb549cc30d39d00918f873e75b2c50176e` |
| OAI.Geometry.PlaneColoring.Interfaces | 528 | 517 | -11 | `c3348acdd555cc4196de9c9f14f1f32cb37f2f59dbfd54fccf591a3303b88e02` |
| OAI.Geometry.PlaneColoring.Sectors | 453 | 451 | -2 | `8acd47b52ea091d61506b8cbf529be6f59626812e90dddec6c7c1de7430e9e62` |
| OAI.Geometry.PlaneColoring.States | 566 | 461 | -105 | `7b411cc583485431fa957070a8d4c678ed35ba8cc7cec8b465925a0e03744520` |

The deleted declarations are listed in `s1/dead-deletions.json` (module, start, end, name).

## Expected gate outputs

1. Rebuild: 27 modules (the downstream closure of the changed files) compile, each `exit 0`, with the logged sha256 equal to the source above. Logs: `s1/logs-r2/NN-<Module>.log`.
2. Root axioms: `s1/logs-r2/axiomroots-s1-r2.log`. Every root prints exactly `[propext, Classical.choice, Quot.sound]` and none prints `sorryAx`. The 14 roots are: uniform_precision_contradiction, finite_uniform_precision_contradiction, ambient_uniform_precision_contradiction, finite_uniform_successor_contradiction, relative_singularity_successor, relative_singularity_approximation, no_proper_five_coloring, properColoring_seven, weakMeasurableColoring_seven, no_measurable_weak_five_coloring, no_proper_five_coloring_algebraic, five_support_step_ban, five_state_forced_label, five_opposite_contacts_false.
3. Signature dump: `s1/logs-r2/sigdump-s1-r2.log` writes `s1/sigs-s1-r2.tsv`; compared with `r1-gates/sigs-r1.tsv`. Expected: 0 changed common declarations; removed = the 25 listed names, plus `five_forced_label`, plus auto-generated equation lemmas of deleted declarations; added = `five_state_forced_label` only; `FORBIDDEN_ABSENT` for all 26 deleted names.

## Results

- Rebuild: 27/27 module logs have exit 0 with a sha256 that matches the current source (27 logs present).
- Root axioms (s1/logs-r2/axiomroots-s1-r2.log): exit 0; 14/14 roots standard-only; sorryAx present: False.
- Signature dump (s1/logs-r2/sigdump-s1-r2.log): exit 0; common 3094, changed 0, removed 28, added ['OAI.EuclideanFiveColor.five_state_forced_label']; FORBIDDEN_ABSENT 26, FORBIDDEN_PRESENT 0.
