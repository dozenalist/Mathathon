# Porting the team's Lean results to Lean 4.35.0: handoff for Carter

Ledger item: [LEAN-435](../RESULTS-LEDGER.md#lean-435). Written 15 November 2026 by the results desk.

## Where things stand

Every Lean result in the [results ledger](../RESULTS-LEDGER.md) was checked with **Lean 4.34.1**
(commit `5045d0056413266e57c625dcd7c365b10e377c52`) and **Mathlib `d13f23b723b8a846827a245b89c10fc7d3f11612`**,
compiled module by module with `lean -o`, not `lake`. None has been built under 4.35.0.

The repository root targets the event toolchain:

- `lean-toolchain`: `leanprover/lean4:v4.35.0`;
- `lakefile.toml`: Mathlib `rev = "v4.35.0"`.

The simplification desk found the 4.35.0 toolchain and Mathlib v4.35.0 sources on the original machine, but no Mathlib
oleans or cache. Expect to fetch the cache (`lake exe cache get`, several GB) first. See
`Main/ResearchSnapshot/import-20261115/work/simplification-desk/lean435/FEASIBILITY.md`.

## Sources to port

All paths are relative to `HadwigerNelson/Main/ResearchSnapshot/`.

| What | Where | Notes |
| --- | --- | --- |
| Supplied proof after R1 (accepted baseline, 27 rebuilt modules + 56 unchanged) | `local/work/lean-queue/threecentre-r1/src/` (`OAI/…`, `AxiomRoots.lean`) | Module order and sha256 values are in `local/work/lean-queue/threecentre-r1/frozen-manifest.json`. |
| S1 (current verified tree, −265 lines vs R1) | R1 tree with the 14 files in `import-20261115/work/simplification-desk/s1/OAI/…` substituted | Full list and hashes are in `…/s1/MANIFEST.md`. Port **S1**, not R1: it is the tree the ledger's −415 total refers to. |
| S2 (CANDIDATE, gates pending) | R1 tree with the 41 files in `import-20261115/work/simplification-desk/s2/OAI/…` | Port only after its 4.34.1 gates pass. |
| Encoding-r4 baseline (unchanged modules) | `local/work/lean-queue/encoding-r4/src/` | Byte-identical to R1 outside the 27 rebuilt modules. |
| CC60 cone packet | `local/outputs/cone/` (`ConeGeometry`, `ConeObstruction`, `ConeSurvivor`, `ConeAudit`) | Compile in that order, on top of the supplied `AngularBoundary`. |
| Three-centre standalone modules | `local/outputs/three-centre/` | Superseded by R1's `AvoidingTrace`; low priority. |
| Standalone team files (A6 forcing and bridges, step-ban v2, EvenWalk, G1, G3) | `import-20261115/work/lean-queue/claude-admissions/*/Candidate.lean` and `import-20261115/work/research-desk/*/` | Each ledger entry gives the exact path and sha256. |

## What matters most (in order)

1. **The headline roots on the S1 tree**, the 14 printed in `…/s1/logs-r2/axiomroots-s1-r2.log`:
   - `no_proper_five_coloring`, `no_measurable_weak_five_coloring` and `no_proper_five_coloring_algebraic`;
   - `properColoring_seven` and `weakMeasurableColoring_seven`;
   - the six spectral roots (`uniform_precision_contradiction`, …);
   - `five_support_step_ban` (Lemma 6.7, branch-free), `five_state_forced_label` and `five_opposite_contacts_false`.
2. **CC60**: `closed60_exclusions_three_le` and `outer120_binary_impossible`.
3. **The A6 chain** (`A6-BRIDGE-R2-G3`, `A6-FORCING`, `G1-R2`, `G3-R2`) and **EvenWalk rev6**, if time allows.

## Gates to re-run under 4.35.0

These are the same gates that were used for 4.34.1.

- **Compile.** Every module exits 0 with no `sorry` and no errors.
- **Axioms.** `#print axioms` on every root prints exactly `[propext, Classical.choice, Quot.sound]`. Template:
  `AxiomRoots.lean` in the R1 and S1 trees. Note that the A6-forcing job never printed axioms for `a6_canonical_pair_subset`.
- **Statements.** A signature dump compared with the 4.34.1 tables (`import-20261115/work/simplification-desk/r1-gates/sigs-r1.tsv`
  and `…/s1/sigs-s1-r2.tsv`): type hash, nested binder flags, universe parameters and definition-value hash. The tool is
  `work/simplification-desk/tools/SigDump.lean` in the research workspace (not imported). Expr hashes may legitimately
  change across Mathlib versions, so at minimum compare `#check` outputs of the roots and of the public declarations.
- **Snapshot.** Record new logs under a dated import folder and re-run `node HadwigerNelson/Main/verify-snapshot.mjs`.

## Known traps from our 4.34.1 logs

- **Renamed lemmas.** `le_or_lt` → `le_or_gt` (G3 standalone r1 failed on this). Expect more renames and
  deprecations at 4.35.0: `dif_pos` → `dite_eq_left`, and `push_neg` → `push Not`, appear as warnings in the EvenWalk log.
- **`omit [..] in` / `include .. in` prefixes.** Deleting a declaration must delete its prefix too (S2 attempt 1 failed at
  `RelativeCenters`).
- **Qualified names inside `simp only [...]` lists.** These count as uses. An Open Math review found two S2 deletions still
  referenced this way.
- **`Decidable` synthesis on wrapped definitions.** `decide` over `fiveAdj` failed until it was stated as the bare
  disjunction `i + 1 = j ∨ j + 1 = i` (step-ban r1 and v3 r2).
- **`whnf` timeouts.** The A6 bridge m2 timed out in `ae_restrictions`; r2 avoided raising `maxHeartbeats` by splitting
  per phase.
- **Staging hygiene.** One job failed only because the staged file began with a stray `\` line; another, because a stopped
  shell re-ran gates after the build folder was deleted and overwrote passing logs. Write logs under new names and never overwrite them.
- **Module resolution.** Lean resolves the `OAI` package from one root. The desk used hard links to unchanged oleans,
  and runs fail with "unknown module prefix 'OAI'" if the build folder is missing.

## Reporting

When a module or root passes under 4.35.0, give the results ledger owner (now the exposition desk) the source sha256,
exit code, log path and axiom lines. The LEAN-435 entry and the `LEAN_VERIFIED` definition will then be updated.
