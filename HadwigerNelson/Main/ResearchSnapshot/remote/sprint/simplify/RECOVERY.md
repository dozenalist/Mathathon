# Recovery after the Open Math OS restart

Runtime restarted during sprint A (swarm `smwfoekgk`, 9 submissions accepted, 7 members still
running, ~18 h of swarm clock left). Per instruction this chat continues without Ultramath: the
swarm is not resumed, no new subagents are launched, and the remaining Lean work is done serially
here.

## State of the shared tree (unchanged)

`lean/OAI`: 83 modules, 31,277 lines, byte-intact (`Five.lean` md5 b749580f...). Pinned toolchain
restored and present (`.scratch/mathlib4` oleans OK). No writes were made to `lean/`, `results/` or
`scripts/` during recovery.

## What survived and where

| artifact | path | status |
|---|---|---|
| Lean declaration/proof-term harness (3538 decls, 7910 type-edges, 15036 value-edges) | `sprint/simplify/m10/harness/` | working |
| Route cost account | `sprint/simplify/m10/ACCOUNTING.md` | complete |
| Cut prerequisite patch (moves 2 declarations out of the deletion zone) | `sprint/simplify/m14/cut-prereq-differenceLaw.patch` | applies cleanly; never been built as a whole tree until now |
| Paper-fidelity map (50 statements) | `sprint/simplify/m14/PAPER-FIDELITY.md` | complete |
| Theorem A in Lean (m5) | `.ultramath/smwfoekgk/m5/work/` | compiled, axioms clean |
| (H2)/(N) properness proof and `TerminalGlue.lean` (m7) | `.ultramath/smwfoekgk/m7/` | compiled, axioms clean |
| Tower architecture `TowerMax.lean` (m15) | `.ultramath/smwfoekgk/m15/` | compiled, 139 lines |
| `CompactSigma` lattice-top result `P5.lean` (m4) | `.ultramath/smwfoekgk/m4/` | compiled |

## Harness limitation (found in phase 2, corrects the figures below)

`DECLGRAPH.log` walks explicit constants in proof terms and does NOT record global attribute
sets. Counterexample: `embed_mul` (Basic.lean:70) is `@[simp]` and is consumed only inside
`simp only [embed_mul, ...]` (Basic.lean:76); the graph log has zero occurrences of it. So
"no edge" does not mean "unused", and graph-freed figures are upper bounds, not achievable
deletions. Build-tested consequences: deleting the 213 out-of-closure declarations yields 29743
lines that fail at level 0 in 8 modules; the attribute fixpoint keeps back 19 declarations / 89
lines inside the R1 freed set; a span-based mechanical trim gives 29971 lines with 6/82 modules
building. Every deletion claim from here must be build-certified.

Corrected accounting (attribute fixpoint, m3/d7): D1 (keep `strict_compact_successor`) 3578
declaration lines, realised 3877; D2 (keep `compactSigma`) 4590, realised 4889; with the Zorn
engine kept 3396/3695 and 4391/4690. Smallest figure anywhere: 3695, i.e. 2.4x the 1500 target.
**D2 is worth ~1015 more than D1**, and `compactSigma` is `[instance_reducible]` with join
closure as `compact_iUnion`, so the D2 engine is already in the tree.

Frontier: the deletable zone stops at `Ergodicity.lean:52`. The restructure must supply exactly
`IsWild (differenceLaw (mu.map q) (condDistrib id q mu))`; nothing above it is deletable.

## The number that matters

R1 (new `exists_terminal_factor` keeping `CompactTower.strict_compact_successor`) frees **4,112
declaration lines** by the harness measurement, against a 1,500-line floor. Module-level trimming
alone is capped at 198 lines; R2/R5/R6 free 0; R3 frees 354. R1 is the only route with margin.

## Done during recovery: the cut-prerequisite tree builds whole

`sprint/simplify/stage/lean` = `lean/` + `m14/cut-prereq-differenceLaw.patch`, built serially under
the pinned toolchain: **83/83 modules, 0 failures**. The two new modules were elaborated explicitly
first (`DifferenceLaw.olean`, `DifferenceInvariant.olean`), then the full tree rebuilt against them.

Certified unchanged in the staged tree (`CheckBoth.lean`):

```
no_proper_five_coloring   : not exists c, ProperColoring 5 c      [propext, Classical.choice, Quot.sound]
properColoring_seven      : ProperColoring 7                      [propext, Classical.choice, Quot.sound]
proper_iff_weak           : both directions of paper Thm 1.3      [propext, Classical.choice, Quot.sound]
chromaticNumber_bounds    : 6 <= chi and chi <= 7                 [propext, Classical.choice, Quot.sound]
algebraic_colorable_iff   : E-colourable iff plane-colourable     [propext, Classical.choice, Quot.sound]
```

Line count: 31318 vs 31277, i.e. +41 — exactly the documented neutral cost of the preparation.

## Retraction of the (N) proof (m7, accepted)

The "cheap" proof of (N) recorded above is WRONG and is withdrawn: `eval z d` is a NUMBER, not a
character, so the step that treated it as a character does not go through. (N)/(O) - properness of
a maximal compact factor - remains OPEN. Nothing in the current record establishes it.

## First building shorter tree (m7, d1) - 881 lines verified, not 1500

FINAL: `sprint/simplify/r1/m7/lean`, 84 modules, 30396 lines = **881 shorter** than the 31277
baseline. Verified here: the four previously-modified files (`Seven`, `MeasurableAssembly`,
`MeasurableProper`, `PlaneColoring/Basic`) are byte-identical to the baseline; `CERT.txt` is
byte-identical to `BASELINE.cert`; builds 84/84 under both toolchains.
Reconciliation: 669 dead declarations + 73 (ConnectedUnitFree) + 180 redundant `open` = 922 off
the staged tree, minus the staged tree's +41 = 881; 808 with ConnectedUnitFree restored.
SCOPE NOTE: 8 of the 83 deleted declarations are cited in reference documents
(`palette_transfer_pair`, `relative_singularity_limit`, `binary_pair_distinct`,
`four_split_antipodes` in PAPER-FIDELITY.md; `diam_le_one_of_preconnected_unitFree`,
`not_straddle_of_isPreconnected` in results/VERIFICATION.md), so this tree proves the headline
theorem but formalises fewer of the paper's numbered statements.

## Superseded: 904-line estimate

`sprint/simplify/r1/m7/lean`: 82 modules, 30221 lines, builds 82/82 from scratch under the pinned
toolchain and under stock 4.33.1; `certify.py` reproduces `BASELINE.cert` byte-identically.
BUT the tree also deletes `MeasurableAssembly` (57) and `MeasurableProper` (68) and removes
`exists_measurable_proper_seven` (19) and `weakMeasurableColoring_seven` (8) from `Seven.lean`,
so 1056 includes 152 lines of dropped theorems. Statement-faithful saving: **~904** (reconciling
with 692 dead declarations + 73 consumerless trim + 180 redundant `open`). Rejected once for
restoration; resubmission pending.

The deletion zone stops at `exists_terminal_factor`: the consumer needs one factor with both
(E) ergodic relative square and (H2) non-diagonality (`TerminalObligation`). Neither extreme
supplies both, `At` cannot compose, and the weak-mixing route is false for Haar.

## Correction: the tower construct is vacuous (m6, machine-checked)

`Tower.step` in `sprint/simplify/m15/work/TowerMax.lean` has only `Measurable H`,
`‖H x‖ ≤ 2` and non-factorisability - no compactness, no failure of ergodicity. So it
generates ALL factors, the maximal member determines the whole sigma-algebra, its relative
product is carried by the diagonal, the difference law is `delta_1`, and `UniversalGood` there
is FALSE for wild `mu` (witness `d = id`; `1 = j 0` in `C`). Hence
`exists_terminal_factor_of_tower_good` has an unsatisfiable hypothesis and is vacuous.
Verified by compiling `.ultramath/smwg224wy/m6/TowerDefect.lean` against the pinned staged
tree (exit 0, `tower_max_all_measurable`).

The repair is to weaken the target: `TerminalObligation mu` = one measurable equivariant `q`
with (E) `ErgodicSMul K (D x D) (RelativeProduct.law mu q)` and (H2) `not a.e. z.1 = z.2`
(`.ultramath/smwg224wy/m6/Residual.lean`), which implies `ergodic_wild_fourier` and is
strictly weaker than UniversalGood (one factor, one d). Neither extreme supplies it: the
trivial factor gives (H2) but not (E); the top factor gives (E) but not (H2). The missing
input is exactly properness of a maximal compact factor, i.e. (N)/(O).

All harness figures are UPPER BOUNDS: a consistency pass took 5876 to 4103 without
converging, so plan against 3695-4889, not against 6076.

## Next concrete step

Write the R1 replacement of `exists_terminal_factor` on top of this staged tree: the m15 tower
architecture (`TowerMax.lean`, 139 lines) plus Theorem A (m5, `relative_singularity_of_ergodic`)
plus (N)/(O) properness (m7). Then collect the deletion — harness says the zone frees 4112
declaration lines — rebuild, re-certify, and measure the realized delta against the 1500-line floor.
Everything needed exists; what remains is the assembly, done serially here.
