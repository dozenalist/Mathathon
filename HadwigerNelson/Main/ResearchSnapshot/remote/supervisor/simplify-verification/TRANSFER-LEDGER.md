# Transfer ledger: what is compiled, what is only source-read

Two supervisor documents feed the §6–§7 half of the argument:
`supervisor/simplify-topology/SECTION7-TOPOLOGY-SUBSTITUTION.md` (Lemma 7.5) and
`supervisor/simplify-exposition/PALETTE-BRIDGE.md` (Proposition 5.6). This ledger is what a referee
should be able to hand to someone else without re-reading either. Grades: **[K]** compiled with a
recorded exit status, **[K?]** claimed compiled, log present, **not re-run by me**, **[S]** source
read only, **[E]** exact finite computation, **[P]** paper argument.

## Environment both documents assume (taken from the actual files, not from prose)

* `lean-toolchain` = `leanprover/lean4:v4.34.1`;
  `.scratch/toolchain/bin/lean --version` = `Lean (version 4.34.1, …, commit 5045d0056413266e57c625dcd7c365b10e377c52)`.
* mathlib = `.scratch/mathlib4` at `d13f23b723b8a846827a245b89c10fc7d3f11612` (`.git` HEAD).
* pinned dependencies from `.scratch/mathlib4/lake-manifest.json`: batteries `f2effa3d`, Qq
  `6a489d9a`, aesop `355695d5`, proofwidgets `106ff4fa`, importGraph `e928b725`,
  LeanSearchClient `ddf04cf3`, plausible `118aa17e`, Cli `e92c9f15`.
* entry point `scripts/env4341.sh` sets `PATH`, `LEAN_PATH` (`lean/build/lib` + mathlib + packages).

## A. Lemma 7.5 (topology)

| item | grade | evidence |
|---|---|---|
| the repo's own `OAI.PlanarCover.compact_open_cover_impossible` (`lean/OAI/Geometry/PlaneColoring/PlanarCovers.lean:374`), the machine form of the paper's Lemma 7.5 (closed square of side 10, relatively open cover, multiplicity ≤ 2, member diameter ≤ 2) | **[K]** prior build | part of the 78-module build recorded in `scripts/build4341.log`; I read the statement, did not re-run |
| the substitution `supervisor/simplify-topology/lean/CoverObstruction.lean`: `paper_lemma_7_5` (the paper's statement as an instance), `compact_cover_obstruction_gen` (compact `Q ⊇ ball 0 R`, diameter bound `d < R`), `hit_center_gen`, `disk3_cover_obstruction` | **[K?]** | owner's log `checks/lean-build3.log` = `BUILD_EXIT=0` under their `env4341.sh`; `checks/axioms.log` = `[propext, Classical.choice, Quot.sound]` for all four (**my** re-run pending, see queue item 3) |
| the topological input actually used: mathlib `Complex.exists_continuousOn_eqOn_exp_comp` (`Mathlib/Analysis/Complex/BranchLogRoot.lean:37`) replacing the printed proof's Brouwer fixed point | **[S]** | owner's dependency audit; dependency chain `compact_open_cover_impossible → finite_open_cover_impossible → finite_partition_impossible → {hit_center_subtype, barycenter_two, affinePair_null}` |
| generalisation: **no convexity, no square** — ball `B(0,R)` with member diameter `≤ d < R` suffices, so "side 10, mesh 2" is not sharp | **[K?]** + **[P]** | theorem statement `CoverObstruction.lean:163`; the *use* of sharpened constants by §7.4 is **[S]**, not checked |
| consumer interface: §7.4's graph map supplies multiplicity ≤ 2 via two positive barycentric coordinates and mesh bounds via `Mesh.no_large_positive_sequence` | **[S]** | claim only; no compiled link between the mesh bound and `d < R` was exhibited |
| import footprint of the substitution | **[S]** | `CoverObstruction.lean` imports `OAI.Geometry.PlaneColoring.PlanarCovers`, whose transitive OAI cone is **25 modules + Mathlib** (computed: Accumulation, AngularBoundary, BinaryDynamics, BinaryPalettes, BoundaryTrace, CircleMaps, CircleTransport, Coloring, Compactness, DiskAverages, Exclusion, Expansion, FourContinuity, FourTransport, PaletteDensity, PaletteTransport, Palettes, PlanarCovers, Rigidity, States, Transitions, WeakColoring, plus PlaneSpectrum CircleDecay, CircleOperator, Fourier). **It is not a Mathlib-only artifact.** The 25 sources are enumerated with paths, line counts and sha256 in `TOPOLOGY-CONE-MANIFEST.json` (9,369 lines), so a machine without the cloud build can elaborate them from source; do not transfer oleans. |

## B. Proposition 5.6, the palette bridge (exposition)

| item | grade | evidence |
|---|---|---|
| `1 ≤ |P_x(e)| ≤ 2` a.e. for a weak measurable 5-colouring | **[K]** prior build | `OAI.EuclideanFiveColor.palette_cardinality`, `BinaryPalettes.lean:260`; part of the prior 78-module build |
| `palette_cardinality` has exactly **five** consumers | **[S]** re-verified by me | `rg -n palette_cardinality lean/OAI` = 6 hits = definition + `Accumulation.lean:161,361`, `Interfaces.lean:78`, `Exclusion.lean:130`, `States.lean:319` ✓ matches their claim |
| "binary" = *meets* a fixed pair (not "is contained in") | **[S]** | their read of `BinaryPalettes.lean:9`; I did not re-read |
| the formal Lemma 5.5 takes a **different proof route** from the paper's six-map expansion, so the paper's constants `δ_*`, `c₀`, `C₀` are **not** certified | **[S]** | their hypothesis audit; this is a fidelity gap, not an error |
| their own block compiled nothing | — | `lean/run_axioms.sh` returned **rc 124 (timeout at 600 s)** with no output: no evidence either way from that block |
| exact finite results: with `T` a pair and `k = 5` the palette field is rigid (2 fields = the paper's alternation (5.8)); with `T` a triple at `k = 6`, `N = 6` gives 234/132/6 and `N = 12` gives 54756/50880/36 | **[E]** | `checks/triple_dichotomy.py` rc 0, `checks/triple_dichotomy.json`; they retracted their own "triple forces a 3-cycle" claim on this evidence |
| the sharpened `k = 6` hole is a *single-centre* lemma (their "M6") | **[C]/[S]** | not audited by me |

## C. What my own block adds or corrects

* **[E]** the §6.3.4 finite core is *not* derivable from the paper's licensed hypotheses: (V) is
  proved only at positions 0 and 3, and eight configurations satisfy everything else
  (`AUDIT-FIVE-CYCLE.md`, `checks/five_cycle_licence.py`). (N) *is* pointwise and sound.
* **[K]** `supervisor/simplify-verification/lean/ConnectedSetExclusion.lean` — the §7 exclusion as one
  principle (Mathlib only, rc 0, axioms `[propext, Classical.choice, Quot.sound]`).
* **[S]** m6 trim and m14 move audits (`trim_audit.py`, `move_audit.py`): deletion-only/verbatim at
  the **source** level. This does **not** prove identical elaborated signatures or axiom
  dependencies — that requires a rebuild plus a `#check`/`#print axioms` comparison (queue items 4–5).

## D. One-line transfer summary

For §7 the compiled content is: the cover obstruction (repo build, and topology's sharper instance
pending my re-run) and the palette bound (prior build). Everything else in both documents — the
constants' fidelity, the mesh-to-`d < R` hand-off, the six-colour sharpening — is source-read or
paper-level, and §6.3.4's advertised simplification is not transferable as stated.
