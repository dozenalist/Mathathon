# Measured deletion budget of lean/OAI (83 modules, 31277 lines)

Method (scripts in this directory):

* `graph.py`/`graph3.py`/`graph4.py`: module import graph and importers.
* `reach2.py`: declaration-level consumer analysis. Parses every top-level
  `theorem|lemma|def|abbrev|instance|structure|class|inductive|opaque` with its
  line span, collects the identifier tokens of the body **including every dot-suffix**
  (so `EuclideanFiveColor.ChainJoin.code` counts as a use of `code`), and does forward
  reachability from the four root modules (`Chromatic`, `ConnectedUnitFree`,
  `NullSetRobust`, `Transfer`). Always kept (conservative): all `instance`, `structure`,
  `class`, `inductive`, every declaration carrying an `@[...]` attribute at its line
  (covers `@[simp]`), and every anonymous declaration.
* `budget.py`: same, after deleting a named set of declarations first (the restructure
  being costed), so what falls out of the tree afterwards is measured, not guessed.

The analysis can only *under*-count deletions (a name that is not mentioned at all is
certainly not used by a term), but it can over-count in one specific way: a declaration
used through an attribute effect we do not model (`simp` sets whose lemmas do not carry
`@[simp]` on their own `have`-line, `norm_num` extensions). Everything reported below was
spot-checked against grep; the largest items (`relative_singularity_limit`,
`bounded_phase_encoding`, `ambient_encoding_of_at`, `exists_simultaneous_moment_parameter`,
`collision_from_measurable_encodings`) are used only inside the module that defines them.

## 1. Plain dead weight, nothing removed

181 declarations, **1771 lines**. This is the ceiling of R7 (mechanical consumer-graph
trimming) on its own: it does clear 1500, with no margin.

    PaletteDensity 188 | Centers 165 | ConditionalLimits 113 | AngularBoundary 102
    PhaseCollision 67 | Basic 64 | SpectralMeasure 64 | States 63 | InvariantMean 53
    Compactness 52 | GraphCuts 51 | BoundaryTrace 50 | MeasurableAssembly 48 ...

## 2. Any architecture that removes UniversalGood / (2.6)

Delete: `exists_terminal_factor`, `UniversalGood`, `universalGood_of_factor`,
`relative_singularity_approximation`, `relative_singularity_successor`.
Keep (R1 still needs them): `strict_compact_successor` and its whole support
(`centered_kernel`, `exists_nonzero_image`, `applyKernel*`, `compact_applyKernel`,
`bounded_range_approximation`), `ChainJoin`, `SeparableZorn`, `CodedMax`, `FactorLp`,
`FactorCode`, `strict_compact_successor`'s consumer chain.

Result: 359 declarations, **5224 lines** die, of which **3453 lines (178 declarations) are
specific to this restructure** (the remaining 1771 are the pre-existing dead weight of §1).

R1-specific, per module (lines / declarations):

    PhaseCollision        446 / 18
    ConditionalSpectrum   423 / 20
    ConditionalLimits     401 / 11
    RelativeCenters       393 / 23
    Approximation         388 / 10
    ConditionalSelection  351 / 11
    SmallArcs             291 / 17
    Centers               255 / 31
    PhaseEncoding         213 / 18
    Factors               117 / 11
    Basic                  98 /  7
    Stationary             77 /  1
                          ----
                         3453 / 178

So an architecture that lands this may spend up to ~1900 lines of new Lean and still reach
the -2000 target, or ~2450 and still clear -1500. The brief's "~2053 lines in a closed
import chain" understates the prize by a factor of three.

## 3. Whole-module deletion is WRONG: count declarations

The module-level single-consumer chain

    Approximation (496) -> RelativeCenters (598), ConditionalSpectrum (497)
    ConditionalSpectrum -> ConditionalSelection (442) -> PhaseCollision (537)
                                             -> PhaseEncoding (255)
    ConditionalSpectrum -> SmallArcs (322), FourierTests (295)

sums to 3442 lines, but `eval`, `measurable_eval_coe`, `differenceLaw` are defined in
ConditionalSpectrum/FourierTests and are used by `Energy`, `Ergodicity`, `SpectralMeasure`,
`NumberFields`, `ConditionalLimits`, i.e. by the retained main chain, and
`exists_small_wild_parameter` is used by `RadialEnergy`. Deleting those modules whole
breaks the main chain. 1689 of the 3442 lines are genuinely R1-specific; the rest stays.

## 4. Size of the machinery that R2 / R5 / R6 would modify (Factors.lean, 586 lines)

    OrbitSpace        44- 82   39 | FactorCode        237-299  63
    OrbitFactor       84-164   81 | FactorLp          300-351  52
    KernelCompact    165-196   32 | CountableApprox   352-394  43
    CompactTower     197-235   39 | ChainJoin         395-495 101
    (strict_compact_successor)    | SeparableZorn     496-545  50
                                  | CodedMax          546-582  37
    exists_terminal_factor (Stationary.lean 126-201) = 76 lines

* **R2 (transfinite recursion instead of Zorn)**: the maximality machinery to replace is
  `SeparableZorn` + `CodedMax` = **87 lines**. Ordinal recursion must be added
  (`WellFounded`/`Ordinal` recursion, a terminal-factor limit case, and the same
  successor/join closure obligations), so R2's best case is -87 + (its recursion cost).
  Certified: R2 cannot be a line-saving route; it is strictly worse than R1.
* **R5 (countable reduction instead of maximality)**: already done. `SeparableZorn.countable_cover`
  extracts a countable dense sequence from the class of closed subspaces and reduces Zorn
  to a countable chain condition (`hseq`), which is exactly what `CodedMax.exists_maximal`
  consumes. Upside of R5 <= 87 lines, with the identical join-closure obligation. Dead.
* **R6 (fixed point of an explicit operator)**: same 87 lines available, and the operator's
  limit stage is a chain join, i.e. the same obligation as R1's. Cannot beat R1.
* **R1/R3**: the only routes whose prize (3453 lines) is much larger than their fixed cost
  (87 lines of maximality that stays useful). Both must pay the closure obligations below.

## 5. Check command

    cd lean && python3 ../.ultramath/smwfoekgk/m12/reach2.py            # §1
    cd lean && python3 ../.ultramath/smwfoekgk/m12/budget.py \
      "exists_terminal_factor,UniversalGood,universalGood_of_factor,relative_singularity_approximation,relative_singularity_successor" \
      strict_compact_successor                                          # §2
