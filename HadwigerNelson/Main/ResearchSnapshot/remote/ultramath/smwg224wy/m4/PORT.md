# D7 — stock-toolchain port, refreshed and measured

**Result.** A trim- and move-tolerant port harness that takes any OAI tree to Lean **4.33.1 +
/opt/mathlib**, verified end to end on the staged tree: **85/85 modules compile, `CheckBoth.lean`
re-certifies all five statements with `[propext, Classical.choice, Quot.sound]`**. The existing
`patches2/all.patch` does **not** do this: it fails 2 of its 109 hunks on the staged tree and is
context-shaped, so it cannot survive any deletion.

## 1. Why the old patch cannot be used on the winning tree

`patch -p1 < .ultramath/smwfcr56i/m8/patches2/all.patch` on a pristine copy of
`sprint/simplify/stage/lean` (log: `work/ref/patch.log`):

```
Hunk #1 FAILED at 238.   OAI/Analysis/PlaneSpectrum/FourierTests.lean.rej
Hunk #5 FAILED at 313.   OAI/MeasureTheory/CompactFactors/Approximation.lean.rej
```

Both are casualties of the m14 cut-prereq patch: `differenceLaw_probability` moved to
`OAI/Analysis/PlaneSpectrum/DifferenceLaw.lean:18` and the `DifferenceInvariant.invariant`
correction belongs to `OAI/MeasureTheory/CompactFactors/DifferenceInvariant.lean:89`. `patch(1)`
looks for them at the old file and old offsets. Independently, 20 of the 38 patched files are
inside the R1 deletion zone (Centers 13 hunks, ConditionalLimits 11, RelativeCenters 10, Functions 9,
Factors 7, Approximation 7, Kernels 5, ConditionalSelection 3, PhaseEncoding 2, SmallArcs 2,
Separability 2, Amenability 2, PhaseCollision 1, AlgebraModels 1, Ergodicity 2). Trim the tree and
every one of those hunks has to be dropped, not applied — which a hunk-based patcher cannot express.

## 2. What the harness does instead

`port.py` reads the same patch but discards the hunk's *location*: each hunk becomes an edit
`old block -> new block`, searched **by content over the whole tree**. Context is used only to make
a block unique and is shrunk automatically when the surrounding lines have drifted.

* block found once → `APPLIED` (wherever it now lives — this is how the two moved hunks get fixed);
* several hits, exactly one in the hunk's own file → `APPLIED-HELD` (reported, never silent);
* several hits, none in the hunk's own file → `SKIPPED-NO-SITE` (refuse: the text was deleted there
  and the other copies are somebody else's);
* no hit at all → `OBSOLETE` (the declaration is gone; a deleted declaration needs no back-port).

`--json` writes every hit, its file and its line. Exit status is non-zero only on a real defect.

## 3. Measurements

## 3.1 Port cost, module by module (staged tree)

85 modules, 31318 lines -> **31457 lines (+139)**. Modules whose text changes:

| module | lines | delta |
|---|---|---|
| Analysis/PlaneSpectrum/Basic | 735 -> 740 | +5 |
| Analysis/PlaneSpectrum/ConditionalSpectrum | 497 -> 498 | +1 |
| Analysis/PlaneSpectrum/Energy | 453 -> 454 | +1 |
| Analysis/PlaneSpectrum/Fourier | 163 -> 166 | +3 |
| Analysis/PlaneSpectrum/Multipliers | 314 -> 313 | -1 |
| Analysis/PlaneSpectrum/RadialEnergy | 472 -> 475 | +3 |
| Analysis/PlaneSpectrum/SpectralMeasure | 388 -> 390 | +2 |
| Geometry/PlaneColoring/BorelTransfer | 458 -> 459 | +1 |
| Geometry/PlaneColoring/ContinuumLimits | 353 -> 361 | +8 |
| Geometry/PlaneColoring/Interfaces | 527 -> 531 | +4 |
| MeasureTheory/CompactFactors/Amenability | 411 -> 448 | +37 |
| MeasureTheory/CompactFactors/Approximation | 425 -> 429 | +4 |
| MeasureTheory/CompactFactors/Centers | 703 -> 695 | -8 |
| MeasureTheory/CompactFactors/ConditionalLimits | 701 -> 702 | +1 |
| MeasureTheory/CompactFactors/ConditionalSelection | 442 -> 444 | +2 |
| MeasureTheory/CompactFactors/DifferenceInvariant | 98 -> 100 | +2 |
| MeasureTheory/CompactFactors/Factors | 586 -> 587 | +1 |
| MeasureTheory/CompactFactors/Kernels | 774 -> 813 | +39 |
| MeasureTheory/CompactFactors/RelativeCenters | 598 -> 630 | +32 |
| MeasureTheory/CompactFactors/Separability | 573 -> 575 | +2 |

**This is a real cost against the line budget.** The target "1500 shorter than 31277" means a ported
tree must be <= 29777 lines: the *pre-port* tree must be <= 29638.

## 3.2 Trim tolerance (measured, not argued)

* Three modules deleted (`ConnectedUnitFree`, `MeasurableAssembly`, `MeasurableProper`):
  `APPLIED=107, APPLIED-HELD=1, OBSOLETE=1` — the single `OBSOLETE` is exactly the hunk whose file
  no longer exists. `patch(1)` on the same tree leaves 3 `.rej` files.
* R1-shaped cut (the last 131 lines of `Centers.lean`, covering 6 of its 13 hunks):
  `APPLIED=102, APPLIED-HELD=1, OBSOLETE=2, SKIPPED-NO-SITE=4`. Every surviving line of the cut
  file is byte-identical to the certified port: `diff p3/Centers.lean cut_p/Centers.lean` is one
  contiguous 128-line deletion and nothing else. `patch(1)` leaves `Centers.lean.rej` there.

## 3.3 A realised, certified tree (acceptance-criterion (b) figure)

`work/trim_p`: staged tree minus `OAI/Geometry/PlaneColoring/ConnectedUnitFree.lean`, ported,
built under stock 4.33.1.

* **84/84 modules compile**, `CheckBoth.lean`: all five statements, axioms
  `[propext, Classical.choice, Quot.sound]`.
* **31384 lines** = 31318 - 73 (deleted module) + 139 (port). Realised deletion: **73 lines**.

**Correction to the plan's 198-line module-trim figure.** `MeasurableAssembly` and
`MeasurableProper` are *not* removable while `properColoring_seven` is kept:
`Seven.lean` uses `exists_measurable_unit_distance_coloring_of_center_cover` (from
MeasurableAssembly) and `weakMeasurableColoring_of_aemeasurable_proper` (from MeasurableProper) —
deleting them gives

```
Seven.lean:42: unknownIdentifier `exists_measurable_unit_distance_coloring_of_center_cover`
Seven.lean:60: unknownIdentifier `weakMeasurableColoring_of_aemeasurable_proper`
```

so only `ConnectedUnitFree` (73 lines, nothing imports it) is realisable, not 198.

## 4. Use it

```bash
bash .ultramath/smwg224wy/m4/d7.sh SPRINT_TREE  OUT_TREE  3
# copies OUT, ports, builds 4.33.1 oleans, runs #print axioms, prints module/line counts
```

Two trees are unavoidable: the pinned 4.34.1 tree (`scripts/env4341.sh`) is the one that needs no
port, and the ported copy is the one that builds on stock 4.33.1. Port the *pre-port* tree; do not
port twice.

## 5. Not verified

* The ported tree is **not** re-checked under 4.34.1 — the port targets 4.33.1 only, and the
  pinned-tree build of the same sources is m10's business.
* The one `APPLIED-HELD` hunk (`@@ -401,6 +405,8 @@` of Approximation.lean) is applied at
  `Approximation.lean:333` and not at the byte-identical duplicate in `ConditionalLimits.lean:296`;
  `ConditionalLimits` compiles without it, so the choice is sound for this tree, but a tree that
  trims the Approximation copy would need that hunk re-aimed by hand.

## 6. The new modules the winning tree will add (checked under stock 4.33.1)

Compiled with `LEAN_PATH=<ported tree>/build/lib:$LEAN_PATH lean <file>`:

| file | under stock 4.33.1 |
|---|---|
| `sprint/simplify/m15/work/TowerMax.lean` | **compiles unchanged** (1 unused-variable linter warning) |
| `.ultramath/smwfoekgk/m7/TerminalGlue.lean` | **compiles unchanged** (2 `haveI` style linter warnings) |
| `.ultramath/smwfoekgk/m5/work/C.lean` | **4 errors** — `condDistrib_comp` arity (4.34 takes `hX`, 4.33 takes the function `X`), and three missing `IsProbabilityMeasure` instances that 4.34 synthesises but 4.33 does not |

`C.lean` is Theorem A, i.e. the one file every architecture consumes, so this mattered. It is
ported: `work/newmods/C_433.lean`, patch `C-433.patch` (4 hunks, proof-internal only — no statement
changes):

1. after `set ν : Measure Y := μ.map q with hν`, add
   `haveI hνp : IsProbabilityMeasure ν := by rw [hν]; exact Measure.isProbabilityMeasure_map hq.aemeasurable`
   (twice, in `differenceLaw_eq_law` and `relative_singularity_of_ergodic`);
2. after `set κ : Kernel Y X := condDistrib id q μ with hκ`, add
   `haveI hκmk : IsMarkovKernel κ := by rw [hκ]; infer_instance` — `set` hides the instance, and
   without it `κ.prod κ` is not a Markov kernel, so `(κ.prod κ) ∘ₘ ν` is not a probability measure;
3. `condDistrib_comp ... hq.aemeasurable aemeasurable_id hd` -> give the `have` its type and call
   `condDistrib_comp (X := q) (Y := (id : X → X)) (f := d) aemeasurable_id hd`;
4. `haveI hlamP : IsProbabilityMeasure lam := by rw [hlam]; infer_instance` ->
   `... exact Measure.isProbabilityMeasure_map hd.aemeasurable`.

Verified:

```
$ LEAN_PATH=".:<ported tree>/build/lib:$LEAN_PATH" lean Cert433.lean
'OAI.PlaneFiveColor.Spectral.RelativeSingularity.relative_singularity_of_ergodic'
  depends on axioms: [propext, Classical.choice, Quot.sound]
'OAI.PlaneFiveColor.Spectral.RelativeSingularity.differenceLaw_eq_law'
  depends on axioms: [propext, Classical.choice, Quot.sound]
```

So Theorem A is available on the stock toolchain; the tower side (`TowerMax`) and the glue
(`TerminalGlue`) need no port at all. What remains on stock 4.33.1 is only the baseline port, which
`d7.sh` does in one command.

## 7. In-tree integration of Theorem A (drop-in for D1/D2)

`work/substrate` = the ported staged tree **plus** Theorem A as three real OAI modules, built from
scratch under stock 4.33.1: **88/88 modules, 0 failures**.

| module | content |
|---|---|
| `OAI/Analysis/PlaneSpectrum/RelativeSingularityInput.lean` | m5 `A.lean` (Mathlib only) |
| `OAI/Analysis/PlaneSpectrum/RelativeSingularityMeasure.lean` | m5 `B.lean` |
| `OAI/Analysis/PlaneSpectrum/RelativeSingularityTheorem.lean` | m5 `C.lean`, ported (`C-433.patch`) |

`A`/`B` stay in the root namespace `RelativeSingularity` because `C` calls
`_root_.RelativeSingularity.measure_eq_zero_or_univ_of_ae_invariant` etc. explicitly; only the
`import` lines were retargeted. Certificate (stock 4.33.1):

```
$ cd work/substrate && LEAN_PATH=build/lib:$LEAN_PATH lean CheckSubstrate.lean
'OAI.PlaneFiveColor.Spectral.RelativeSingularity.relative_singularity_of_ergodic'
  depends on axioms: [propext, Classical.choice, Quot.sound]
'OAI.PlaneFiveColor.Spectral.RelativeSingularity.differenceLaw_eq_law'
  depends on axioms: [propext, Classical.choice, Quot.sound]
```

and the checked statement is (H1)+(H2) -> conclusion, with no `IsWild` hypothesis:

```
relative_singularity_of_ergodic : ∀ (μ : Measure X) [IsProbabilityMeasure μ] (q : X → Y)
  (hq : Measurable q) (d : X → D), Measurable d → (∀ k x, d (k • x) = k • d x) →
  ∀ [ErgodicVAdd Rot (X × X) (RelativeProduct.law μ q hq)],
  (¬ ∀ᵐ z ∂(RelativeProduct.law μ q hq), d z.1 = d z.2) →
  differenceLaw (μ.map q) (condDistrib d q μ) C = 0
```

So a winning tree can `import OAI.Analysis.PlaneSpectrum.RelativeSingularityTheorem` on either
toolchain (4.34.1 needs the original `C.lean`; 4.33.1 needs the ported one — the two differ only in
proof internals, never in a statement).

## 8. R1-ready substrate: 90 modules, all building on stock 4.33.1

`work/substrate` = ported staged tree + the three ready-made components as real OAI modules:
**90/90 modules, 0 failures, 32329 lines**.

| module | source | lines | axioms |
|---|---|---|---|
| `OAI/MeasureTheory/CompactFactors/TowerMax.lean` | m15 `TowerMax.lean` | 139 | clean |
| `OAI/Analysis/PlaneSpectrum/RelativeSingularity{Input,Measure,Theorem}.lean` | m5 `A/B/C.lean`, C ported | 111+131+407 | clean |
| `OAI/Analysis/PlaneSpectrum/TerminalGlue.lean` | m7 `TerminalGlue.lean` | 84 | clean |

plus the untouched head line `no_proper_five_coloring`, `properColoring_seven`. Certificate
(`work/substrate/Check90.lean`, stock 4.33.1):

```
exists_terminal_factor_of_tower_good          [propext, Classical.choice, Quot.sound]
exists_ergodic_factor                         [propext, Classical.choice, Quot.sound]
terminalObligation_of_exists_terminal_factor  [propext, Classical.choice, Quot.sound]
no_proper_five_coloring                       [propext, Classical.choice, Quot.sound]
properColoring_seven                          [propext, Classical.choice, Quot.sound]
```

Nothing in this tree was weakened: no statement was edited, `TowerMax`/`TerminalGlue` are byte-copies
of m15/m7's files, and `A`/`B` differ from m5's only in the two `import` lines. What is *not* done
here is the rest: the successor step, the rewiring of `exists_terminal_factor`, and the deletion of
the propagation zone. That is D1/D2/D4's work; this tree only guarantees that whatever they produce
starts from a base that already builds on both toolchains.
