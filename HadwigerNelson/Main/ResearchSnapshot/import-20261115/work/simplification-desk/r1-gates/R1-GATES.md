# R1 (threecentre-r1) contract and dependency gates: re-run by the simplification desk

2026-11-15, about 01:30Z. Lean 4.34.1 (commit 5045d005), Mathlib d13f23b. All runs are local desk runs, one Lean process at a time.

## Verdict

**PASS.** R1's 3,116 declarations that also exist in the encoding-r4 baseline are identical to it in every
compared field. The 8 removed declarations are exactly the strict-state branch, and none of them exists in the R1 environment. The 6 added
declarations are exactly the three-centre machinery. The manifest is complete. All 27 rebuilt modules
have passing compile records whose sources match the frozen manifest. The 9 root theorems use only standard axioms.

## 1. Exact types and binder flags: whole-closure signature dump

Tool: `tools/SigDump.lean` (sha256 below). It imports the three root modules plus the spectral roots. For
every non-internal constant declared in an `OAI.*` module, it records:
- kind;
- module;
- universe parameters;
- the structural hash of the type (`Expr.hash`);
- binder infos of the statement telescope, with each hypothesis's own forall-telescope nested (so
  implicitness inside hypotheses is compared as well);
- for definitions, the structural hash of the value. A changed definition body would change the meaning of every statement mentioning it.

| Run | Build | Log | Exit | Constants |
|---|---|---|---|---|
| baseline | `lean-queue/encoding-r4/build` | `r1-gates/sigdump-r4.log` | 0 (185 s) | 3,126 rows (3,124 names; 2 on-demand `eq_1` lemmas appear in two modules each, identically in both runs) |
| R1 | `lean-queue/threecentre-r1/build` | `r1-gates/sigdump-r1.log` | 0 (94 s) | 3,124 rows (3,122 names) |

Comparison (`r1-gates/sig-compare-r4-r1.json`):

- **Common: 3,116.** Kind, universe parameters, type hash, binder flags and value hash are identical for all of them.
  Two common declarations changed only their module, from `FiveSupport` to the new `AvoidingTrace`, with identical signatures:
  `palette_neighbor_real` and `palette_neighbor_disjoint`. These were moved, not changed.
- **Removed: 8,** exactly the strict-state branch. States: `nonparallel_neighborhood`,
  `strict_state_sequence_local_false`, `positive_state_support_point`, `support_density_direction`,
  `support_density_sequence`, `strict_state_sequence_false`, `strict_state_no_unit_support`.
  FourContinuity: `strict_state_uniform_on_compact`.
- **Added: 6,** all in AvoidingTrace: `avoidingTraceCentre`, `avoidingTraceCentre_seqClosed`,
  `isClosed_avoidingTraceCentre`, `triangle_no_unit_of_avoiding_traces`,
  `fixed_state_no_unit_three_centres`, `strict_state_sequence_no_unit_three_centres`.

Hash caveat: `Expr.hash` is a structural hash. A collision is theoretically possible. The binder-flag
string and value hash are compared independently.

## 2. Transitive forbidden-dependency gate

The 8 strict-state names were passed as the forbidden set (`SIGDUMP_FORBIDDEN`):
- R1: `FORBIDDEN_ABSENT` for all 8. They are not in the R1 environment at all, so no R1 declaration can
  depend on them transitively. This is stronger than the earlier per-root traversal, which visited 51k–61k
  constants for the two three-centre roots (`outputs/three-centre/MOVING-VALIDATION.txt`).
- Baseline: `FORBIDDEN_PRESENT` for all 8, as expected.

`sorryAx`: the root `#print axioms` below shows no `sorryAx`.

## 3. Manifest completeness (PaletteTransport)

See `r1-gates/MANIFEST-COMPLETENESS.md`. The frozen manifest is exactly the 27-module downstream closure of the 5 changed
files. PaletteTransport and the other 55 upstream modules are byte-identical to encoding-r4 in both
source and olean. PaletteTransport's compile evidence is `encoding-r4-full-44.log`, exit 0.

## 4. Build records and root axioms

`tools/r1_build_records.py` cross-checked the queue records: **27 of 27** affected modules have a passed compile
record (exit 0) whose source sha256 equals the frozen-manifest sha256. The root job
`threecentre-r1-axiomroots`, exit 0 at 20:48Z, prints `[propext, Classical.choice, Quot.sound]` for 9
roots:
- the spectral roots `uniform_precision_contradiction`, `finite_uniform_precision_contradiction`,
  `ambient_uniform_precision_contradiction`, `finite_uniform_successor_contradiction`,
  `relative_singularity_successor`, `relative_singularity_approximation`;
- `no_proper_five_coloring`;
- `properColoring_seven`;
- `weakMeasurableColoring_seven`.

Both signature dumps above loaded every one of the 83 R1 oleans in one process, which also checks that the
build is import-consistent.

**Clean rebuild:** this is not a separate R1 re-run. The desk's S1 rebuild recompiles the same 27-module
closure from R1-plus-S1 sources, followed by the root axiom check. See `s1/`.
