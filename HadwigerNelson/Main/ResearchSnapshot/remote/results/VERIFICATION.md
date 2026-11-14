# Machine verification of the lower and upper bounds, in this VM

## Environment

The bundle was written for Lean 4.34.1 and mathlib commit
`d13f23b723b8a846827a245b89c10fc7d3f11612`. The VM's default toolchain is Lean 4.33.1, under
which 47 of the 78 modules fail with ordinary Mathlib API drift (`And.fun_mul`,
`MemLp.coeFn_toLp`, `isometry_add_right`, `ite_eq_left`, ...). None of those failures is
mathematical. Rather than port backwards, the exact environment was fetched and cached:

```
bash scripts/fetch_exact_env.sh      # Lean 4.34.1 + mathlib @ d13f23b, `lake exe cache get`
source scripts/env4341.sh            # PATH + LEAN_PATH
python3 scripts/build_lean.py        # 78 modules, topological order, oleans in lean/build/lib
```

`scripts/build4341.log` records **78 modules, all `OK`, zero patches, 2–14 s each**.

**Dual-toolchain.** A swarm member also ported the whole development, including the five modules
added here, to the VM's default Lean 4.33.1 + Mathlib (`.ultramath/smwfcr56i/m8/patches2/all.patch`,
38 files, 109 hunks). I ran its `reproduce.sh`: **83/83 modules, `failures: []`**, and the audit
prints the three standard axioms for both roots. The patch touches no declaration line (`theorem`,
`lemma`, `def`, `abbrev`) and adds three lemmas; the only statement-level change is nine dropped
`omit [MeasurableMul₂ G] [MeasurableInv G]` prefixes, which add instance hypotheses forced by the
older `frequencyLaw` and leave the roots unchanged. So the theorem is checkable in both the pinned
and the stock environment.

## Axiom certificate

```
source scripts/env4341.sh && lean results/lean/Check3.lean
```

```
'OAI.EuclideanFiveColor.no_proper_five_coloring'            [propext, Classical.choice, Quot.sound]
'OAI.EuclideanFiveColor.no_proper_five_coloring_algebraic'  [propext, Classical.choice, Quot.sound]
'OAI.Problem160.properColoring_seven'                       [propext, Classical.choice, Quot.sound]
'OAI.Problem160.chromaticNumber_bounds'                     [propext, Classical.choice, Quot.sound]
'OAI.EuclideanFiveColor.proper_iff_weak'                    [propext, Classical.choice, Quot.sound]
'OAI.EuclideanFiveColor.algebraic_colorable_iff'            [propext, Classical.choice, Quot.sound]
```

with

```
no_proper_five_coloring            : ¬ ∃ c : ℂ → Fin 5, ProperColoring 5 c
no_proper_five_coloring_algebraic  : ¬ ∃ c : E → Fin 5, LabelModel.Proper 5 c      (E = algebraicClosure ℚ ℂ)
properColoring_seven               : ProperColoring 7
chromaticNumber_bounds             : 6 ≤ planeChromaticNumber ∧ planeChromaticNumber ≤ 7
proper_iff_weak                    : (∃ c, ProperColoring k c) ↔ (∃ c, Measurable c ∧ WeakColoring k c)
algebraic_colorable_iff            : (∃ c : E → Fin k, Proper k c) ↔ (∃ c : ℂ → Fin k, ProperColoring k c)
```

No `sorry`, `axiom`, `native_decide`, `@[implemented_by]`, `opaque` or `admit` occurs in any of the
78 modules (textual scan). A swarm member independently ran `#print axioms` on 27 declarations of
the lower-bound chain with the same result.

## Statement fidelity

* `ProperColoring k c := ∀ x y : ℂ, ‖x - y‖ = 1 → c x ≠ c y` — the paper's Definition, no
  regularity, no boundedness, no period. ✓
* `WeakColoring k c := AEMeasurable c volume ∧ ∀ᵐ p ∂(volume.prod angularMeasure), c p.1 ≠ c (p.1 + direction p.2)`
  is **equivalent** to the paper's Definition 1.2 (`∀ R > 0, ∑_i ∫_{B(0,R)} ∫_{S¹} 1_{A_i}(x)1_{A_i}(x+u) dσ(u) dx = 0`).
  Machine-checked in `results/lean/Def12.lean` (swarm member m1), including
  `∑ i, 1_{c x = i} 1_{c y = i} = [c x = c y]`.
* `AEMeasurable` in place of "Lebesgue measurable" is exactly the null-set invariance the paper
  states after Definition 1.2.

## New modules added here

| module | statement |
|---|---|
| `lean/OAI/Geometry/PlaneColoring/Converse.lean` | `finite_config_proper`, `exists_properColoring_of_finset` (Tychonoff compactness), `properColoring_of_weak` (weak ⟹ proper) |
| `lean/OAI/Geometry/PlaneColoring/Transfer.lean` | `proper_iff_weak` (paper Theorem 1.3, both directions), `algebraic_colorable_iff` |
| `lean/OAI/Geometry/PlaneColoring/Chromatic.lean` | `chromaticNumber_bounds : 6 ≤ χ ∧ χ ≤ 7` (contributed by swarm member m1) |
| `lean/OAI/Geometry/PlaneColoring/NullSetRobust.lean` | `not_proper_five_coloring_compl_null : volume Z = 0 → ¬ 5-colourability of ℂ \ Z` |
| `lean/OAI/Geometry/PlaneColoring/ConnectedUnitFree.lean` | `diam_le_one_of_preconnected_unitFree`, `not_straddle_of_isPreconnected` (the connected-set exclusion of §7) |
| `lean/OAI/Geometry/PlaneColoring/BorelTransfer.lean` | `proper_to_borel_weak_algebraic` (hypothesis weakened from `ℂ` to `E`) |
| `lean/OAI/Geometry/PlaneColoring/Five.lean` | `no_proper_five_coloring_algebraic` |

## Independently checked finite core

* Seven-colouring: exact integer verification of every constant (`results/lean/verify_seven.py`
  from m1): covering radius `(4/5)/√3 ≤ 7/15 ⟺ 144 ≤ 147`; same-colour separation
  `(4/5)√7 > 1 + 14/15 ⟺ 1008 > 841`; the paper's own `r = 2/5` route:
  `2r = 4/5 < 1` and `(√21 − 2)(2/5) > 1 ⟺ 21 > 81/4`.
* Moser certificate of §8.5–8.6: exact arithmetic in `Q(√3, √11)` (m11, `exact2.py`): all eleven
  edges have squared length exactly 1; the non-3-colourability argument is the equilateral-triangle
  identification `c(0) = c(T) = c(uT)` versus `|T − uT| = 1`; all seven points satisfy the region
  inequality (8.4) with margins.
