# R8 (Theorem 2.3) — measured verdict, and the module-level surgery budget

m8 / direction d8. Everything below is computed from `lean/OAI` by
`sprint/simplify/m8/costs.py`; residue ranges are quoted with line numbers and
were read off the files, so every number is checkable with `sed -n A,Bp FILE`.

Check command:

```bash
cd sprint/simplify/m8 && python3 costs.py
```

## 0. Tree as measured

| quantity | modules | lines |
|---|---|---|
| `lean/OAI` | 83 | 31277 |
| closure of the 5 headline roots (`Five`, `Seven`, `Transfer`, `Chromatic`, `NullSetRobust`) | 82 | 31204 |
| outside every headline closure | 1 | 73 (`PlaneColoring/ConnectedUnitFree.lean`) |

There is **no module-level dead weight**: the only module outside the asset
closure is `ConnectedUnitFree.lean` (73 lines), which is a kept asset result
("connected unit-free sets have diameter ≤ 1"). So no route can win by dropping
an unreachable module.

## 1. The rigidity block (Theorem 2.3) is half the tree

Define the rigidity block as the set of modules every path from the headline
theorem to which passes through `Analysis/PlaneSpectrum/Ergodicity.lean`
(`ergodic_wild_fourier` = Theorem 2.3 in the ergodic case, plus the ergodic
decomposition). Import-graph computation:

```
rigidity block = closure(Five) - closure(Five, banned = Ergodicity)
```

**30 modules, 15482 lines = 49.5% of the tree.** Composition:

* ingredient 1c, the `UniversalGood` / (2.6) propagation tower: 13 modules
  (`CompactFactors/{Centers,RelativeCenters,Approximation,ConditionalLimits,Factors,Stationary}`,
  `PlaneSpectrum/{ConditionalSpectrum,FourierTests,Multipliers,SmallArcs,PhaseCollision,PhaseEncoding}`,
  `CompactFactors/ConditionalSelection`);
* ingredient 1b: `InvariantMean` 1078, `Amenability` 411;
* ingredients 1d/1e: `Representations` 477, `Energy` 453, `RadialEnergy` 472,
  `Selections` 432, `NumberFields` 524, `SpectralMeasure` 388, `Ergodicity` 415;
* shared with 1d: `Basic` 735, `Functions` 884, `Kernels` 774,
  `BoundedFunctions` 223, `RelativeProducts` 472, `Separability` 573,
  `AlgebraModels` 664.

## 2. R8 verdict

Theorem A replaces ingredient 1c **only**. It therefore removes at most the
1c mass, and leaves ingredients 1b/1d/1e untouched:

| | lines |
|---|---|
| rigidity block | 15482 |
| removable by Theorem A (section 3) | 6088 |
| untouched by Theorem A | 9394 |

So a shorter proof of Theorem 2.3 built on Theorem A cannot halve the
development — the "halve" hope in the brief is wrong by roughly a factor 2.
The remaining 9394 lines are the radial-energy / number-field / invariant-mean
argument, and Theorem A says nothing about them. R8 has no cheaper route to
them: the radial inequality and the number-field propagation are the paper's
own analysis and there is no substitute in the tree.

Additional measured fat **inside** the rigidity block that a consumer-graph trim
cannot see (all of these declarations are used):

* `Energy.lean` lines 10–86 rebuild `PlaneFiveColor.InvariantMean`'s invariant
  mean from scratch — `approxAt`, `approx_norm_le`, `approx_has_limit`,
  `meanAt`, `tendsto_approx`, `mean_add`, `mean_smul`, `mean_const`,
  `mean_nonneg`, `mean_norm_le`, `mean_shift`, `meanCLM`, `meanCLM_apply`,
  `toMean` — as a structural copy of `InvariantMean.lean`'s
  `approx`(190), `approx_norm_le`(192), `averagingUF`, `approx_has_limit`,
  `mean`, `tendsto_approx`(218), `mean_add`(222), `mean_smul`(227),
  `mean_const`(232), `mean_nonneg`(238), `mean_norm_le`(242), `mean_shift`(273),
  `meanCLM`(284). `Energy.lean` already imports `InvariantMean` transitively
  (Energy → Representations → Stationary → … → Multipliers → InvariantMean).
  The copy has exactly **two** consumers, both of the form
  `MovingMean.toMean (fun _ => 0)`: `RadialEnergy.lean:87` and
  `Ergodicity.lean:338`. Replacement: one `def toMean (_ : Finset G × ℕ → G) :
  Amenable.Mean G := ⟨InvariantMean.meanCLM, …⟩` (≈5 lines) in place of 77.
  **Measured saving ≈ 72 lines.** `cubeSupport` / `cube_le_of_support` /
  `syndetic_of_all_means` (`Energy.lean` 91–131) are genuinely new and stay.
* `RelativeProducts.lean` 214–237 duplicates `BoundedFunctions.lean` 33–47
  lemma for lemma (`bound`, `norm_le_bound`, `ext`, `add_apply`, `mul_apply`,
  `sub_apply`, `zero_apply`, `one_apply`, `real_smul_apply`, `bmConj`,
  `conj_apply`); `RelativeProducts` imports `BoundedFunctions`. ≈ 24 lines.
* `InvariantMean.lean` 21–24 and 496–507 duplicate `Amenability.lean` 14–17 and
  50–61 (`shift`, `shift_apply`, `normFn`, `normFn_apply`, `pairing`,
  `pairing_apply`). ≈ 20 lines. (Overlaps d26/m14.)
* `Centers.lean` 394–430 duplicates `Basic.lean`'s `j`, `j_add`, `j_neg`,
  `j_sub`, `j_injective`, `j_zero`, `measurableSet_coset` ≈ 37 lines; `Centers`
  is deleted by the Theorem-A route anyway.

Total quantified duplication: **≈ 150 lines**, of which ≈ 72 is in the 1c-free
part of the rigidity block and therefore survives any Theorem-A route.

## 3. Module-level surgery certificate for the Theorem-A routes (R4 / R11)

If Theorem A is available *and* a factor with ergodic relative product is
supplied, the propagation tower becomes dead code. The deletable set computed
module by module, with the exact residue each partially-used module must keep:

| module | lines | kept | saved | kept range |
|---|---|---|---|---|
| `CompactFactors/Centers.lean` | 703 | 0 | 703 | — |
| `CompactFactors/Factors.lean` | 586 | 0 | 586 | — |
| `PlaneSpectrum/ConditionalSpectrum.lean` | 497 | 0 | 497 | — |
| `PlaneSpectrum/FourierTests.lean` | 295 | 0 | 295 | — |
| `PlaneSpectrum/Multipliers.lean` | 314 | 0 | 314 | — |
| `PlaneSpectrum/SmallArcs.lean` | 322 | 0 | 322 | — |
| `CompactFactors/ConditionalSelection.lean` | 442 | 0 | 442 | — |
| `PlaneSpectrum/PhaseCollision.lean` | 537 | 0 | 537 | — |
| `PlaneSpectrum/PhaseEncoding.lean` | 255 | 0 | 255 | — |
| `PlaneSpectrum/Characters.lean` | 560 | 0 | 560 | — (reachable only through `Multipliers`; every use of `lineCharacter`, `coeff`, `character_ae_ordinary`, `wild_continuous_coefficient_zero` is in `Multipliers.lean`) |
| `CompactFactors/RelativeCenters.lean` | 598 | 93 | 505 | 113–131 (`ErgodicSupport`), 136–209 (`KernelSupport`) |
| `CompactFactors/Approximation.lean` | 496 | 80 | 416 | 108–147 (`DifferenceInvariant`), 280–296 (`KernelSupport.factor_smul_preserving`), 298–320 (`relative_difference_invariant`) |
| `CompactFactors/ConditionalLimits.lean` | 701 | 138 | 563 | 40–177 (`EuclideanFiveColor.LimitDensity`) |
| `CompactFactors/Stationary.lean` | 201 | 108 | 93 | 1–108 (`EuclideanFiveColor.StationaryMean`) |
| **total** | **6507** | **419** | **6088** | |

**Gross saving 6088 lines = 19.5% of the tree**, before subtracting the cost of
Theorem A itself.

The certificate is only sound if three interface sites are re-pointed. These are
the *only* places where a kept module uses a deleted module:

1. `Kernels.lean:234` uses `LimitDensity.generated_factor_approximation`.
   Keep `ConditionalLimits.lean` 40–177 (138 lines) — that whole section is the
   only genuinely shared content of a 701-line module.
2. `Ergodicity.lean:412` uses `relative_difference_invariant`; keep
   `Approximation.lean` 298–320. `Ergodicity.lean` also uses
   `condDistrib_equivariant`, keep `RelativeCenters.lean` 136–209.
   `RelativeProducts.lean` uses `condDistrib_equivariant` too.
3. `Representations.lean` needs only `EuclideanFiveColor.StationaryMean` from
   `Stationary.lean`; re-point its import from `Factors` to `InvariantMean`
   (the `StationaryMean` section uses `mean`, `mean_add`, `mean_smul`,
   `mean_const`, `mean_nonneg`, `mean_norm_le`, `mean_shift` only).
4. After deleting `Characters.lean`, the modules that used to reach `Basic`
   through it (`Energy`, `RadialEnergy`, `Ergodicity`, `SpectralMeasure`,
   `Representations`, `Selections`, `NumberFields`) need an explicit
   `import OAI.Analysis.PlaneSpectrum.Basic`; `Energy` and `Stationary` need
   `import OAI.Analysis.PlaneSpectrum.InvariantMean`. Measured cost: import lines
   only, ~0 lines.

   Nothing else outside the deleted set mentions `OrbitSpace`, `FactorCode`,
   `FactorLp`, `ChainJoin`, `CodedMax`, `SeparableZorn` or
   `strict_compact_successor` — checked by whole-tree grep.

## 4. R2 / R5 / R6: measured ceiling

`Factors.lean` is the sole home of the maximality device:

| block | lines | range |
|---|---|---|
| `OrbitSpace` | 39 | 44–82 |
| `OrbitFactor` | 81 | 84–164 |
| `KernelCompact` | 32 | 165–196 |
| `CompactTower.strict_compact_successor` | 39 | 197–235 |
| `FactorCode` | 63 | 237–299 |
| `FactorLp` | 52 | 300–351 |
| `CountableApprox` | 43 | 352–394 |
| `ChainJoin` | 101 | 395–495 |
| `SeparableZorn` | 50 | 496–545 |
| `CodedMax` | 37 | 546–582 |

R2, R5 and R6 all propose to replace the **maximality device only** —
`SeparableZorn` + `CodedMax` = **87 lines (0.28% of the tree)**. Each then has to
write an ordinal recursion / a countable reduction / a fixed-point operator of
comparable size, and each keeps `relative_singularity_approximation`
(`ConditionalLimits.lean` 622–668), `ChainJoin.approximation`
(`Factors.lean` 455–494) and `strict_compact_successor` unchanged, because the
propagation of `UniversalGood` across a chain join and a strict successor is not
what those routes change.

**Verdict: R2, R5, R6 have a gross ceiling of 87 lines and a net of O(0). None
of them can contribute to the 1500-line target.** They are neutral rewrites, not
reductions.

R1 alone is the same story unless Theorem A is available: the join-closure
obligation for "compact extension" is exactly what the tree already proves as
the `ha` hypothesis of `relative_singularity_approximation`
(`ConditionalLimits.lean` 622–668) fed by `ChainJoin.approximation`
(`Factors.lean` 455–494), so re-predicating maximality on compactness does not
remove any of that material; it re-derives it. With Theorem A, R1 collapses into
R4 and inherits the 6088 lines of §3 — but then it also inherits Theorem A's
(H2) obligation, which is what d3/m12 and d24/m16 attack.

## 5. Summary

| route | gross lines available | note |
|---|---|---|
| R4 / R11 (Theorem A replaces the tower) | **6088** | needs Theorem A + a factor with ergodic relative product; exact residue 419 lines, 4 interface sites |
| R7 (fat trim) | 1771 (m12's independent count) | not mine; cross-checks with §0: no *module* is dead |
| R8 (shorter Theorem 2.3) | 6088 above + ≈72 duplication | Theorem A is 1c; 1d/1e (9394 lines) is untouched |
| R2 / R5 / R6 | 87 | net O(0); cannot reach the target |
| R1 without Theorem A | 87 | re-derives the join-closure it would need to gain |

No route available without Theorem A reaches 1500 lines. The 1500-line target is
reachable only through Theorem A, and then only to 6088 lines gross.
