/-
  A6 palette producer -- **revision r2** of the accepted bridge
  `supervisor/simplify-lean/swarm-smwguinbz/A6-Bridge-m2.lean`
  (sha256 3ac02303c7112cdcfb9aea9f7b2febd0ee106087435c009547df126498a0cc9e).

  Lineage of the two source files merged here:
    * lane B, swarm `smwguinbz` -> `A6-Bridge-m2.lean`   (accepted) -- §1-§8
    * lane B, swarm `smwgwui56` -> `G1-Finish-mB.lean`   (accepted) -- §9
        sha256 2be419fa16f26b6f3fd1d16b20f9fa7993443e5804b9fcbbcc117f207c0482f6
        folded in at its r2 state, `G1-Finish-mB-r2.lean`, i.e. with the one
        `interval_cases` repair the parent's compile of r1 asked for.
  `smwgwui56` is closed (2 accepted, 0 running), so this revision is written by
  the coordinator directly; no successor member was started.

  G3 IS NOT GLUED HERE.  `G3-ArcCover-mA.lean` is being compiled standalone
  (Mathlib only) this cycle; per instruction nothing is glued until that result
  is in.  So this file still takes `ArcCover` as the hypothesis it was in m2
  (§8), and it contains no `arcCover`, no `badSet`, no `exists_arc_of_not_bad`.
  The splice is prepared and one flag away (`WITH_G3=1` in
  `.scratch/build_r2.py`): it is `G3-ArcCover-mA.lean` §2-§5 with its §0
  scaffold and its §1 duplicate `def arc` dropped, plus a §11 corollary
  discharging `hcover`.  It is not in this file.

  STATUS: **UNCOMPILED**.  No `lean`, no `lake`, no build of any kind has been
  run on this file, and nothing below is a compile claim.  The compile evidence
  in play is the parent's, on the two *previous* files, quoted next.

  WHY r2 EXISTS.  The parent compiled `A6-Bridge-m2.lean` locally, job
  `claude-lean-20261114t213711-0`; it FAILED with three defects, all in the
  bridge:

    (D1) `ae_restrictions` (m2 line 171) -- deterministic timeout at whnf,
         200000 heartbeats; the whole declaration was rejected.  Suspect: the
         implicit motive `p` of `QuasiMeasurePreserving.ae` had to be solved by
         higher-order unification against `p (t + sixAngle j)` in a context
         where `p` mentions `palette c hc x _`.
    (D2) m2 line 236, unknown constant `ae_restrictions` -- pure cascade of D1.
    (D3) `ae_canonical_subpalette_global` (m2 line 321) -- a genuine direction
         error.  `hθ j harc` wants `t + sixAngle j + sixAngle j ∈ arc` (the
         pullback along `· + sixAngle j` shifts the wrong way), and the palette
         it reports is the twice-shifted one.

  The parent's compile of `G1-Finish-mB.lean`, job
  `claude-lean-20261114t215215-1`, FAILED with exactly one error, at line 105
  in `cos_sign_strict`: `interval_cases h : m % 6` could not find an upper
  bound.  That file is folded in below at its repaired r2 state (§9).

  WHAT r2 CHANGES.

    §4   rewritten.  `ae_restrictions` is split into `ae_mem_resOut`,
         `ae_mem_resIn` (the pointwise `hJ`s, previously local `have`s), and one
         lemma per phase and side -- `outer_shift (j)`, `inner_shift (j)`,
         `disj_shift (j)` -- each a standalone theorem with the motive of `ae`
         passed explicitly as `(p := fun s : Angles => ...)`, and the three
         families joined by `ae_all_iff` only at the end.  `maxHeartbeats` is
         NOT raised.  The statement of `ae_restrictions` is unchanged, so §6
         still applies it verbatim.                                [D1, D2]
    §8   `ae_canonical_subpalette_global`: the global shift is now
         `· + -sixAngle j`, i.e. `· - sixAngle j`; the arc hypothesis is
         discharged at `t + sixAngle j + -sixAngle j = t`; the component
         reported is the same `j` that the cover produces, at the angle `θ`
         itself.  `ae_canonical_subpalette` is untouched.                [D3]
    §9   appended: all of `G1-Finish-mB.lean` except its §5 copies of
         `arc`/`pos`/`neg`/`SignTable` (the bridge already defines them), at its
         r2 state -- the one repair being, in `cos_sign_strict` and immediately
         before `interval_cases h : m % 6`,
             `have hm6 : m % 6 < 6 := Nat.mod_lt m (by norm_num)`
         which is the hypothesis `mod6_not_mem` already carried.  Renames:
             posT_char        -> pos_char'          (NOT `pos_char`: that name
             negT_char        -> neg_char'           already exists in §3 as the
             negT_char_alt    -> neg_char_alt        converse implication)
             negT_mem         -> dropped, the bridge's `neg_mem` is the same
                                 lemma and `neg_char_alt` now cites it
             signTableT_of_paired(_fin) -> signTable_of_paired(_fin)
             SignTableT -> SignTable,  arcT -> arc,  posT -> pos,  negT -> neg
         Closes G1: `SignTable v` follows from the pairing hypothesis
         `v i = direction (sixAngle (2*(i.val/2)))`.

  NOT CHANGED, verbatim from m2: §1 table, §2 `arc`, §3 closed combinatorial
  facts, §5 `SignTable`, §6 `ae_six_inputs`, §7 `ForcingLemma`, and all of
  `ae_canonical_subpalette`.  `SignTable`, `ForcingLemma` and `ArcCover` stay
  hypotheses exactly where m2 had them: §9 discharges `SignTable` from the
  pairing hypothesis, `ForcingLemma` remains the lane-A pure `Fin 6` input
  (`A6-Forcing-m1.lean`, `a6_canonical_pairs`, and that one PASSED locally,
  job `claude-lean-20261114t212205-0`), and `ArcCover` is still an input
  because G3 is held.

  RESIDUAL OBLIGATION (geometric, not Lean).  The pairing hypothesis of §9,
  `v i = direction (sixAngle (2*(i.val/2)))`, is A6 configuration data: it is
  NOT implied by `ApproachingContinuum`, which gives only `‖v i‖ = 1`.
  Nothing in this file removes it.

  API BASIS (pinned checkout `.scratch/mathlib4`, Lean 4.34.1 `5045d005`,
  Mathlib `d13f23b7`), the two signatures D1/D3 turn on:
    * `MeasureTheory.Measure.QuasiMeasurePreserving.ae`,
      `Mathlib/MeasureTheory/Measure/QuasiMeasurePreserving.lean:109`:
        `theorem ae (h : QuasiMeasurePreserving f μa μb) {p : β → Prop}
           (hg : ∀ᵐ x ∂μb, p x) : ∀ᵐ x ∂μa, p (f x)`
    * `measurePreserving_add_right` is the `to_additive` of
      `measurePreserving_mul_right`,
      `Mathlib/MeasureTheory/Group/Measure.lean:97`:
        `measurePreserving_mul_right (μ : Measure G) [IsMulRightInvariant μ] (g : G) :
           MeasurePreserving (· * g) μ μ`
      so the additive form acts by `· + g`.  It is the instance the repository
      already uses at `Exclusion.lean:152`.
    * the D3 pullback deliberately uses `· + -sixAngle j` and not
      `measurePreserving_sub_right` (the `to_additive` of
      `measurePreserving_div_right`, same file :229).  The latter additionally
      needs a `MeasurableAdd`/`MeasurableSub` instance for `AddCircle (2*pi)`,
      which I did not find in the pinned checkout, whereas
      `measurePreserving_add_right` needs only `IsAddRightInvariant
      angularMeasure`.  The tree itself does exactly this at
      `AngularBoundary.lean:363-368`: pull back by
      `measurePreserving_add_right angularMeasure (-(sixty : Angles))`, then
      `change s (q - (sixty : Angles)) = b` and
      `simpa only [← sub_eq_add_neg, sub_add_cancel, ...]`.

  No `sorry`, no `admit`, no `native_decide`, no `axiom`, no `@[implemented_by]`,
  and no assumption beyond the named hypotheses of §5, §7, §8 and §9.
-/
import OAI.Geometry.PlaneColoring.AngularBoundary
import OAI.Geometry.PlaneColoring.PaletteTransport
-- r2 addition: `direction_inner_real` (Interfaces.lean:198) is used by the G1 block in §9.
-- `Interfaces` imports `AngularBoundary`, so this is monotone and acyclic.
import OAI.Geometry.PlaneColoring.Interfaces

namespace OAI

noncomputable section
open Set Filter Topology MeasureTheory
open scoped RealInnerProductSpace
namespace EuclideanFiveColor
namespace A6

/-! ## 1. The A6 source table

`f`, `hit`, `g` are the three rows of the task's SHARED DATA; `pos`, `neg` are the
positive / negative sign index sets of the six approach directions at phase `j`,
and `resOut`, `resIn` are the label sets that survive the corresponding side's
exclusion, i.e. `univ \ ⋃_{i ∈ pos j} {i, i+1}` and `univ \ ⋃_{i ∈ neg j} {i, i+1}`
(they are tabulated, and proved equal to that description, in `resOut_spec` /
`resIn_spec`). -/

/-- The two labels carried by the exclusion edge at `i`: the source set `{i, i+1}`. -/
def eSet (i : Fin 6) : Finset (Fin 6) := {i, i + 1}

/-- Forced first label `f = (1,5,3,1,5,3)` of the A6 source table. -/
def f : Fin 6 → Fin 6 :=
  fun j => if j = 0 then 1 else if j = 1 then 5 else if j = 2 then 3 else
    if j = 3 then 1 else if j = 4 then 5 else 3

/-- Other hits `H = ({3,4,5},{1,2,3},{0,1,5},{3,4,5},{1,2,3},{0,1,5})`. -/
def hit : Fin 6 → Finset (Fin 6) :=
  fun j => if j = 0 then {3, 4, 5} else if j = 1 then {1, 2, 3} else
    if j = 2 then {0, 1, 5} else if j = 3 then {3, 4, 5} else
    if j = 4 then {1, 2, 3} else {0, 1, 5}

/-- Forcing second label (canonical partner) `g = (4,2,0,4,2,0)`. -/
def g : Fin 6 → Fin 6 :=
  fun j => if j = 0 then 4 else if j = 1 then 2 else if j = 2 then 0 else
    if j = 3 then 4 else if j = 4 then 2 else 0

/-- Labels with positive inner product at phase `j`. -/
def pos : Fin 6 → Finset (Fin 6) :=
  fun j => if j = 0 then {0, 1} else if j = 1 then {0, 1, 2, 3} else
    if j = 2 then {2, 3} else if j = 3 then {2, 3, 4, 5} else
    if j = 4 then {4, 5} else {0, 1, 4, 5}

/-- Labels with negative inner product at phase `j` (complement of `pos j`). -/
def neg (j : Fin 6) : Finset (Fin 6) := Finset.univ \ pos j

/-- Residual of the positive side at phase `j`. -/
def resOut : Fin 6 → Finset (Fin 6) :=
  fun j => if j = 0 then {3, 4, 5} else if j = 1 then {5} else
    if j = 2 then {0, 1, 5} else if j = 3 then {1} else
    if j = 4 then {1, 2, 3} else {3}

/-- Residual of the negative side at phase `j`. -/
def resIn : Fin 6 → Finset (Fin 6) :=
  fun j => if j = 0 then {1} else if j = 1 then {1, 2, 3} else
    if j = 2 then {3} else if j = 3 then {3, 4, 5} else
    if j = 4 then {5} else {0, 1, 5}

/-! ## 2. The fundamental arc

A6 works at `t + j · 60°` with `t` in the open arc `(-30°, 30°)`; the six
translates of that arc tile the circle off the six points `±30° mod 60°`. -/

/-- The open fundamental arc `(-π/6, π/6)` inside `Angles = AddCircle (2*Real.pi)`. -/
def arc : Set Angles := {t | ∃ s : ℝ, |s| < Real.pi / 6 ∧ (s : Angles) = t}

/-! ## 3. Closed combinatorial facts of the table

Every proof below is `decide` on a closed statement over `Fin 6`; there is no
`native_decide`, no axiom.  These are the only facts about the table that the
bridge uses. -/

/-- `pos j` is the residue rule of the six paired directions: at phase `j` the
angle is `s + j·60°` with `|s| < 30°`, and label `i` carries the direction
`exp(2πi⌊i/2⌋/3)`, so its inner product has the sign of `cos(s + (j-2⌊i/2⌋)·60°)`.
This lemma states that `pos j` is exactly that arithmetic rule. -/
lemma pos_char : ∀ (j i : Fin 6),
    (i ∈ pos j ↔ (j.val + 6 - 2 * (i.val / 2)) % 6 ∈ ({0, 1, 5} : Finset ℕ)) := by
  decide

/-- The negative side is the complement of the positive side. -/
lemma neg_mem (j i : Fin 6) : (i ∈ neg j) ↔ ¬ (i ∈ pos j) := by
  simp [neg]

/-- `resOut j` is exactly the label set that survives exclusion along `pos j`. -/
lemma resOut_spec : ∀ (j a : Fin 6),
    (a ∈ resOut j ↔ ∀ i, i ∈ pos j → a ∉ eSet i) := by
  decide

/-- `resIn j` is exactly the label set that survives exclusion along `neg j`. -/
lemma resIn_spec : ∀ (j a : Fin 6),
    (a ∈ resIn j ↔ ∀ i, i ∈ neg j → a ∉ eSet i) := by
  decide

/-- At even phases the positive side keeps the other-hit set `H`; at odd phases it
keeps only the forced label `f`. -/
lemma resOut_even : ∀ j : Fin 6, j.val % 2 = 0 → resOut j = hit j := by decide

lemma resOut_odd : ∀ j : Fin 6, ¬ j.val % 2 = 0 → resOut j = ({f j} : Finset (Fin 6)) := by
  decide

/-- At even phases the negative side keeps only the forced label `f`; at odd phases
it keeps the other-hit set `H`. -/
lemma resIn_even : ∀ j : Fin 6, j.val % 2 = 0 → resIn j = ({f j} : Finset (Fin 6)) := by
  decide

lemma resIn_odd : ∀ j : Fin 6, ¬ j.val % 2 = 0 → resIn j = hit j := by decide

/-- The canonical partner is `f j + 3` (in `Fin 6`): `g j = f j + 3`. -/
lemma g_eq : ∀ j : Fin 6, g j = f j + 3 := by decide

/-! ## 4. The six conull angular inputs, raw form

This is the bridge proper: the three source a.e. statements are pushed to the six
shifted angles `t + sixAngle j`.

**r2 revision of m2's single `ae_restrictions`.**  In `A6-Bridge-m2.lean` all of
this was one declaration, and that declaration failed to elaborate (deterministic
timeout at whnf, 200000 heartbeats; local job `claude-lean-20261114t213711-0`).
The suspect is the implicit motive of the pullback

    MeasureTheory.Measure.QuasiMeasurePreserving.ae
      (Mathlib/MeasureTheory/Measure/QuasiMeasurePreserving.lean:109):
      theorem ae (h : QuasiMeasurePreserving f μa μb) {p : β → Prop}
        (hg : ∀ᵐ x ∂μb, p x) : ∀ᵐ x ∂μa, p (f x)

against the higher-order pattern `p (t + sixAngle j)`, with `p` mentioning
`palette c hc x _`: Lean has to *invent* `p`, and the whnf of that unification
problem does not terminate in the heartbeat budget.

The repair is the prescribed one: one standalone theorem per side, each passing
the motive explicitly as `(p := fun s : Angles => ...)`, so no higher-order
unification is attempted at all; the three are joined by `ae_all_iff` only at the
end.  `maxHeartbeats` is *not* raised, and the statement of `ae_restrictions` is
unchanged, so §6 consumes it exactly as before.

The pullback map is `· + sixAngle j`, i.e. the additive form of

    MeasureTheory.measurePreserving_add_right
      (`to_additive` of `measurePreserving_mul_right`,
       Mathlib/MeasureTheory/Group/Measure.lean:97):
      measurePreserving_mul_right (μ : Measure G) [IsMulRightInvariant μ] (g : G) :
        MeasurePreserving (· * g) μ μ

which is the same instance the repository already uses at `Exclusion.lean:152`.

`finite_support_exclusion_ae` stays in the *space* variable `z : ℂ` and only
supplies the pointwise `hJ` that `continuum_outer/inner_restriction` consume; it
needs neither `hK` nor `v`, so `ae_mem_resOut` / `ae_mem_resIn` do not take them.
-/

/-- Positive-side residue at phase `j`: at a.e. point that straddles every `K i`
with `i ∈ pos j`, the colour lies in `resOut j`.  (m2's local `hJout`, standalone;
`resOut_spec` is the conversion.) -/
theorem ae_mem_resOut (c : ℂ → Fin 6) (hc : Measurable c) {K : Fin 6 → Set ℂ}
    (hsupp : ∀ i, ∀ j ∈ eSet i, Disjoint (spatialSupport c j) (Straddle (K i))) (j : Fin 6) :
    ∀ᵐ z : ℂ ∂volume, (∀ i ∈ pos j, z ∈ Straddle (K i)) → c z ∈ resOut j := by
  filter_upwards [finite_support_exclusion_ae c hc K eSet hsupp] with z hz hzE
  exact (resOut_spec j (c z)).mpr fun i hi => hz i (hzE i hi)

/-- Negative-side residue at phase `j`.  (m2's local `hJin`, standalone.) -/
theorem ae_mem_resIn (c : ℂ → Fin 6) (hc : Measurable c) {K : Fin 6 → Set ℂ}
    (hsupp : ∀ i, ∀ j ∈ eSet i, Disjoint (spatialSupport c j) (Straddle (K i))) (j : Fin 6) :
    ∀ᵐ z : ℂ ∂volume, (∀ i ∈ neg j, z ∈ Straddle (K i)) → c z ∈ resIn j := by
  filter_upwards [finite_support_exclusion_ae c hc K eSet hsupp] with z hz hzE
  exact (resIn_spec j (c z)).mpr fun i hi => hz i (hzE i hi)

/-- **Outer (positive) side at phase `j`.**  `continuum_outer_restriction`, rotated
by `sixAngle j`, with the motive of `ae` supplied explicitly. -/
theorem outer_shift (c : ℂ → Fin 6) (hc : Measurable c) {x : ℂ} {K : Fin 6 → Set ℂ}
    {v : Fin 6 → ℂ} (hK : ∀ i, ApproachingContinuum x (K i) (v i))
    (hsupp : ∀ i, ∀ j ∈ eSet i, Disjoint (spatialSupport c j) (Straddle (K i))) (j : Fin 6) :
    ∀ᵐ t ∂angularMeasure,
      (∀ i ∈ pos j, 0 < ⟪direction (t + sixAngle j), v i⟫) →
        (palette c hc x (t + sixAngle j) ∩ resOut j).Nonempty := by
  have hout : ∀ᵐ t ∂angularMeasure,
      (∀ i ∈ pos j, 0 < ⟪direction t, v i⟫) → (palette c hc x t ∩ resOut j).Nonempty :=
    continuum_outer_restriction c hc (pos j) hK (ae_mem_resOut c hc hsupp j)
  exact (measurePreserving_add_right angularMeasure (sixAngle j)).quasiMeasurePreserving.ae
    (p := fun s : Angles =>
      (∀ i ∈ pos j, 0 < ⟪direction s, v i⟫) → (palette c hc x s ∩ resOut j).Nonempty) hout

/-- **Inner (negative) side at phase `j`.**  `continuum_inner_restriction`, rotated
by `sixAngle j`, with the motive of `ae` supplied explicitly. -/
theorem inner_shift (c : ℂ → Fin 6) (hc : Measurable c) {x : ℂ} {K : Fin 6 → Set ℂ}
    {v : Fin 6 → ℂ} (hK : ∀ i, ApproachingContinuum x (K i) (v i))
    (hsupp : ∀ i, ∀ j ∈ eSet i, Disjoint (spatialSupport c j) (Straddle (K i))) (j : Fin 6) :
    ∀ᵐ t ∂angularMeasure,
      (∀ i ∈ neg j, ⟪direction (t + sixAngle j), v i⟫ < 0) →
        (palette c hc x (t + sixAngle j) ∩ resIn j).Nonempty := by
  have hin : ∀ᵐ t ∂angularMeasure,
      (∀ i ∈ neg j, ⟪direction t, v i⟫ < 0) → (palette c hc x t ∩ resIn j).Nonempty :=
    continuum_inner_restriction c hc (neg j) hK (ae_mem_resIn c hc hsupp j)
  exact (measurePreserving_add_right angularMeasure (sixAngle j)).quasiMeasurePreserving.ae
    (p := fun s : Angles =>
      (∀ i ∈ neg j, ⟪direction s, v i⟫ < 0) → (palette c hc x s ∩ resIn j).Nonempty) hin

/-- **Sixty-degree covariance of the palette at phase `j`.**  `palette_sixty_disjoint`,
rotated by `sixAngle j`; `sixAngle_step` turns `sixAngle (j+1)` into
`sixAngle j + sixty`, so the source statement at `t + sixAngle j` is exactly the
conclusion. -/
theorem disj_shift (c : ℂ → Fin 6) (hc : Measurable c) (hw : WeakColoring 6 c) (x : ℂ)
    (j : Fin 6) :
    ∀ᵐ t ∂angularMeasure, Disjoint (palette c hc x (t + sixAngle j))
      (palette c hc x (t + sixAngle (j + 1))) := by
  have hsrc : ∀ᵐ f ∂angularMeasure,
      Disjoint (palette c hc x f) (palette c hc x (f + (sixty : Angles))) :=
    palette_sixty_disjoint c hc hw x
  have hshift := (measurePreserving_add_right angularMeasure (sixAngle j)).quasiMeasurePreserving.ae
    (p := fun s : Angles => Disjoint (palette c hc x s) (palette c hc x (s + (sixty : Angles))))
    hsrc
  filter_upwards [hshift] with t ht
  rw [sixAngle_step, ← add_assoc]
  exact ht

/-- **The six conull angular inputs, raw form.**  At angular-a.e. `t` and for every
phase `j`: the positive restriction, the negative restriction, and the
sixty-degree disjointness, all at the single angle `t + sixAngle j`.  Statement
verbatim from m2; only the proof is reassembled from the four lemmas above. -/
theorem ae_restrictions (c : ℂ → Fin 6) (hc : Measurable c) (hw : WeakColoring 6 c) {x : ℂ}
    {K : Fin 6 → Set ℂ} {v : Fin 6 → ℂ} (hK : ∀ i, ApproachingContinuum x (K i) (v i))
    (hsupp : ∀ i, ∀ j ∈ eSet i, Disjoint (spatialSupport c j) (Straddle (K i))) :
    ∀ᵐ t ∂angularMeasure, ∀ j : Fin 6,
      ((∀ i ∈ pos j, 0 < ⟪direction (t + sixAngle j), v i⟫) →
        (palette c hc x (t + sixAngle j) ∩ resOut j).Nonempty) ∧
      ((∀ i ∈ neg j, ⟪direction (t + sixAngle j), v i⟫ < 0) →
        (palette c hc x (t + sixAngle j) ∩ resIn j).Nonempty) ∧
      Disjoint (palette c hc x (t + sixAngle j))
        (palette c hc x (t + sixAngle (j + 1))) := by
  filter_upwards [ae_all_iff.mpr (fun j => outer_shift c hc hK hsupp j),
    ae_all_iff.mpr (fun j => inner_shift c hc hK hsupp j),
    ae_all_iff.mpr (fun j => disj_shift c hc hw x j)] with t ho hi hd
  exact fun j => ⟨ho j, hi j, hd j⟩
/-! ## 5. The A6 sign table (geometric input, NOT derived here)

The content is the sign of `cos(s + (j - 2⌊i/2⌋)·π/3)` for `|s| < π/6`; by
`pos_char` this is exactly `pos j` / `neg j`.  Discharging `SignTable v` from
`v i = direction (sixAngle (2·⌊i/2⌋))` needs only the repository's
`direction_inner_real` (`Interfaces.lean:196`) and one cosine lemma; see
NOTES-m2.md, item G1. -/

/-- The A6 sign table on the fundamental arc. -/
def SignTable (v : Fin 6 → ℂ) : Prop :=
  ∀ (j : Fin 6) (t : Angles), t ∈ arc →
    (∀ i : Fin 6, (0 < ⟪direction (t + sixAngle j), v i⟫) ↔ i ∈ pos j) ∧
    (∀ i : Fin 6, (⟪direction (t + sixAngle j), v i⟫ < 0) ↔ i ∈ neg j)

/-! ## 6. The same six inputs in table form -/

theorem ae_six_inputs (c : ℂ → Fin 6) (hc : Measurable c) (hw : WeakColoring 6 c) {x : ℂ}
    {K : Fin 6 → Set ℂ} {v : Fin 6 → ℂ} (hK : ∀ i, ApproachingContinuum x (K i) (v i))
    (hsupp : ∀ i, ∀ j ∈ eSet i, Disjoint (spatialSupport c j) (Straddle (K i)))
    (hsign : SignTable v) :
    ∀ᵐ t ∂angularMeasure, t ∈ arc → ∀ j : Fin 6,
      f j ∈ palette c hc x (t + sixAngle j) ∧
      (palette c hc x (t + sixAngle j) ∩ hit j).Nonempty ∧
      Disjoint (palette c hc x (t + sixAngle j))
        (palette c hc x (t + sixAngle (j + 1))) := by
  classical
  filter_upwards [ae_restrictions c hc hw hK hsupp] with t hres
  intro harc j
  obtain ⟨houtj, hinj, hdisj⟩ := hres j
  obtain ⟨hpos, hneg⟩ := hsign j t harc
  have hOut := houtj fun i hi => (hpos i).mpr hi
  have hIn := hinj fun i hi => (hneg i).mpr hi
  refine ⟨?_, ?_, hdisj⟩
  · by_cases hj : j.val % 2 = 0
    · have hres' : resIn j = ({f j} : Finset (Fin 6)) := resIn_even j hj
      rw [hres'] at hIn
      obtain ⟨a, ha⟩ := hIn
      rw [Finset.mem_inter, Finset.mem_singleton] at ha
      rw [← ha.2]
      exact ha.1
    · have hres' : resOut j = ({f j} : Finset (Fin 6)) := resOut_odd j hj
      rw [hres'] at hOut
      obtain ⟨a, ha⟩ := hOut
      rw [Finset.mem_inter, Finset.mem_singleton] at ha
      rw [← ha.2]
      exact ha.1
  · by_cases hj : j.val % 2 = 0
    · have hres' : resOut j = hit j := resOut_even j hj
      rw [hres'] at hOut
      exact hOut
    · have hres' : resIn j = hit j := resIn_odd j hj
      rw [hres'] at hIn
      exact hIn

/-! ## 7. The pure `Fin 6` forcing lemma (lane A of the task), as an input -/

/-- No palette-cardinality premise anywhere: the forcing removes the two
neighbouring forced labels from `Q j ∩ H j`. -/
def ForcingLemma : Prop :=
  ∀ Q : Fin 6 → Finset (Fin 6), (∀ j, f j ∈ Q j) → (∀ j, (Q j ∩ hit j).Nonempty) →
    (∀ j, Disjoint (Q j) (Q (j + 1))) → ∀ j, f j + 3 ∈ Q j

/-! ## 8. A.e. canonical subpalette -/

theorem ae_canonical_subpalette (c : ℂ → Fin 6) (hc : Measurable c) (hw : WeakColoring 6 c)
    {x : ℂ} {K : Fin 6 → Set ℂ} {v : Fin 6 → ℂ} (hK : ∀ i, ApproachingContinuum x (K i) (v i))
    (hsupp : ∀ i, ∀ j ∈ eSet i, Disjoint (spatialSupport c j) (Straddle (K i)))
    (hsign : SignTable v) (hforce : ForcingLemma) :
    ∀ᵐ t ∂angularMeasure, t ∈ arc → ∀ j : Fin 6,
      f j ∈ palette c hc x (t + sixAngle j) ∧ f j + 3 ∈ palette c hc x (t + sixAngle j) := by
  classical
  filter_upwards [ae_six_inputs c hc hw hK hsupp hsign] with t ht
  intro harc j
  have hf : ∀ j, f j ∈ palette c hc x (t + sixAngle j) := fun j => (ht harc j).1
  have hH : ∀ j, (palette c hc x (t + sixAngle j) ∩ hit j).Nonempty :=
    fun j => (ht harc j).2.1
  have hd : ∀ j, Disjoint (palette c hc x (t + sixAngle j))
      (palette c hc x (t + sixAngle (j + 1))) := fun j => (ht harc j).2.2
  exact ⟨hf j, hforce (fun j => palette c hc x (t + sixAngle j)) hf hH hd j⟩

/-- The six translates of the fundamental arc cover the circle off a null set
(geometric input, NOT derived here; pure statement about `sixty` and `sixAngle`). -/
def ArcCover : Prop :=
  ∀ᵐ θ ∂angularMeasure, ∃ t ∈ arc, ∃ j : Fin 6, θ = t + sixAngle j

/-- **A.e. canonical subpalette, angle form**: for angular-a.e. `θ` the palette at
`θ` contains `f j` together with its canonical partner `f j + 3` for the phase `j`
of `θ`. -/
theorem ae_canonical_subpalette_global (c : ℂ → Fin 6) (hc : Measurable c)
    (hw : WeakColoring 6 c) {x : ℂ} {K : Fin 6 → Set ℂ} {v : Fin 6 → ℂ}
    (hK : ∀ i, ApproachingContinuum x (K i) (v i))
    (hsupp : ∀ i, ∀ j ∈ eSet i, Disjoint (spatialSupport c j) (Straddle (K i)))
    (hsign : SignTable v) (hforce : ForcingLemma) (hcover : ArcCover) :
    ∀ᵐ θ ∂angularMeasure, ∃ j : Fin 6,
      f j ∈ palette c hc x θ ∧ f j + 3 ∈ palette c hc x θ := by
  classical
  -- r2 fix of D3.  The cover writes `θ = t + sixAngle j` with `t ∈ arc`, and the
  -- subpalette statement has to be read at that same `t`.  So the pullback is
  -- along `· - sixAngle j` -- written `· + -sixAngle j` to stay with
  -- `measurePreserving_add_right`, see the header -- and NOT along `· + sixAngle j`
  -- as in m2, which needed `t + sixAngle j + sixAngle j ∈ arc` and reported the
  -- palette at the twice-shifted angle.
  have hshift (j : Fin 6) : ∀ᵐ θ ∂angularMeasure,
      θ + -sixAngle j ∈ arc → ∀ k : Fin 6,
        f k ∈ palette c hc x (θ + -sixAngle j + sixAngle k) ∧
        f k + 3 ∈ palette c hc x (θ + -sixAngle j + sixAngle k) :=
    (measurePreserving_add_right angularMeasure (-sixAngle j)).quasiMeasurePreserving.ae
      (p := fun s : Angles => s ∈ arc → ∀ k : Fin 6,
        f k ∈ palette c hc x (s + sixAngle k) ∧ f k + 3 ∈ palette c hc x (s + sixAngle k))
      (ae_canonical_subpalette c hc hw hK hsupp hsign hforce)
  filter_upwards [ae_all_iff.mpr hshift, hcover] with θ hθ hcov
  obtain ⟨t, harc, j, rfl⟩ := hcov
  -- (i) the arc hypothesis, at the phase the cover produced
  have hmem : t + sixAngle j + -sixAngle j ∈ arc := by
    have hcancel : t + sixAngle j + -sixAngle j = t := by abel
    rwa [hcancel]
  -- (ii) the component at the *same* `j`, which puts the palette at
  --      `(t + sixAngle j) + -sixAngle j + sixAngle j = t + sixAngle j`
  have h := hθ j hmem j
  have harg : t + sixAngle j + -sixAngle j + sixAngle j = t + sixAngle j := by abel
  rw [harg] at h
  exact ⟨j, h⟩


/-! ## 9. G1: `SignTable` from the paired approach directions

This is the whole of `G1-Finish-mB.lean` (swarm `smwgwui56`, lane B, accepted),
minus its §5 copies of `arc`, `pos`, `neg` and `SignTable` -- §2 and §5 above
already define those, and re-defining them in the same namespace is an error.
The renames are listed in the header.  Section numbers below are the source
file's, prefixed `G1`: §0 residue bookkeeping, §1 the strict cosine sign table,
§2 the `direction` interface, §3 the label geometry, §4 the sign of the inner
product at phase `j`, §6 the `decide` bridge between the residue rule and the
bridge's table, §7 the closing lemma `SignTable v`.

The one hypothesis that cannot be removed: the pairing of the six approach
directions.  `ApproachingContinuum` gives `‖v i‖ = 1` only; that the six
directions are the three palette directions with each taken twice is A6
configuration data.  See `signTable_of_paired_fin`.
-/
/-! ### G1 0.  The residue bookkeeping

`{0,1,5}` and `{2,3,4}` are complementary among the residues mod 6; that is all
the negative side needs, and it is used only by the fallback `neg_char_alt`.
`aspect` of `decide` here: `interval_cases h : m % 6` generalises the expression
`m % 6` (Mathlib/Tactic/IntervalCases.lean:382 `generalizeHyp`), so after the
case split the goal really does contain the literal `0, ..., 5` and `decide`
is evaluating a closed `Nat` proposition. -/

lemma mod6_not_mem (m : ℕ) :
    ((m % 6 ∈ ({2, 3, 4} : Finset ℕ)) ↔ ¬ (m % 6 ∈ ({0, 1, 5} : Finset ℕ))) := by
  have hm6 : m % 6 < 6 := Nat.mod_lt m (by norm_num)
  interval_cases h : m % 6 <;> decide

/-! ### G1 1.  G1b1: the strict cosine sign lemma -/

/-- **The strict sign table of `cos` at the six multiples of `pi/3`.**

For `|s| < pi/6` the six cosines `cos (s + m * pi/3)` have the sign of the residue
`m % 6`: positive for `0, 1, 5` and negative for `2, 3, 4`.  Both sides are strict
(no zero case is reachable): the margin `pi/6` keeps every shifted argument off
the zeros `pi/2 + k pi` of `cos`. -/
lemma cos_sign_strict (s : ℝ) (m : ℕ) (hs : |s| < Real.pi / 6) :
    (0 < Real.cos (s + m * (Real.pi / 3)) ↔ (m % 6 ∈ ({0, 1, 5} : Finset ℕ))) ∧
    (Real.cos (s + m * (Real.pi / 3)) < 0 ↔ (m % 6 ∈ ({2, 3, 4} : Finset ℕ))) := by
  have hpi : 0 < Real.pi := Real.pi_pos
  have hs1 : -(Real.pi / 6) < s := (abs_lt.mp hs).1
  have hs2 : s < Real.pi / 6 := (abs_lt.mp hs).2
  -- (i) reduce `m` modulo 6:  `m * (pi/3) = (m % 6) * (pi/3) + (m / 6) * (2 * pi)`
  have hper : Real.cos (s + (m : ℝ) * (Real.pi / 3))
      = Real.cos (s + ((m % 6 : ℕ) : ℝ) * (Real.pi / 3)) := by
    have hdecomp : (m : ℝ) = ((m % 6 : ℕ) : ℝ) + ((m / 6 : ℕ) : ℝ) * 6 := by
      have h0 : ((m % 6 + 6 * (m / 6) : ℕ) : ℝ) = (m : ℝ) := by
        rw [Nat.mod_add_div]
      rw [← h0] <;> push_cast <;> ring
    have harg : s + (m : ℝ) * (Real.pi / 3)
        = (s + ((m % 6 : ℕ) : ℝ) * (Real.pi / 3))
          + ((m / 6 : ℕ) : ℝ) * (2 * Real.pi) := by
      rw [hdecomp]
      ring
    rw [harg, Real.cos_add_nat_mul_two_pi]
  rw [hper]
  -- (ii) the six residues, one interval computation each
  have hm6 : m % 6 < 6 := Nat.mod_lt m (by norm_num)
  interval_cases h : m % 6
  · -- residue 0 :  s in (-pi/2, pi/2)
    have hp : 0 < Real.cos (s + ((0 : ℕ) : ℝ) * (Real.pi / 3)) := by
      simpa using (Real.cos_pos_of_mem_Ioo (x := s) ⟨by linarith, by linarith⟩)
    exact ⟨iff_of_true hp (by decide), iff_of_false (not_lt.mpr hp.le) (by decide)⟩
  · -- residue 1 :  s + pi/3 in (pi/6, pi/2)
    have hp : 0 < Real.cos (s + ((1 : ℕ) : ℝ) * (Real.pi / 3)) := by
      simpa using
        (Real.cos_pos_of_mem_Ioo (x := s + Real.pi / 3) ⟨by linarith, by linarith⟩)
    exact ⟨iff_of_true hp (by decide), iff_of_false (not_lt.mpr hp.le) (by decide)⟩
  · -- residue 2 :  s + 2 pi/3 in (pi/2, 5 pi/6)
    have hn : Real.cos (s + ((2 : ℕ) : ℝ) * (Real.pi / 3)) < 0 := by
      simpa using
        (Real.cos_neg_of_pi_div_two_lt_of_lt (x := s + 2 * (Real.pi / 3))
          (by linarith) (by linarith))
    exact ⟨iff_of_false (not_lt.mpr hn.le) (by decide), iff_of_true hn (by decide)⟩
  · -- residue 3 :  s + pi in (5 pi/6, 7 pi/6)
    have hn : Real.cos (s + ((3 : ℕ) : ℝ) * (Real.pi / 3)) < 0 := by
      simpa using
        (Real.cos_neg_of_pi_div_two_lt_of_lt (x := s + 3 * (Real.pi / 3))
          (by linarith) (by linarith))
    exact ⟨iff_of_false (not_lt.mpr hn.le) (by decide), iff_of_true hn (by decide)⟩
  · -- residue 4 :  s + 4 pi/3 in (7 pi/6, 3 pi/2)
    have hn : Real.cos (s + ((4 : ℕ) : ℝ) * (Real.pi / 3)) < 0 := by
      simpa using
        (Real.cos_neg_of_pi_div_two_lt_of_lt (x := s + 4 * (Real.pi / 3))
          (by linarith) (by linarith))
    exact ⟨iff_of_false (not_lt.mpr hn.le) (by decide), iff_of_true hn (by decide)⟩
  · -- residue 5 :  shift by -2 pi  first,  then s - pi/3 in (-pi/2, -pi/6)
    have hp : 0 < Real.cos (s + ((5 : ℕ) : ℝ) * (Real.pi / 3)) := by
      have harg : s + ((5 : ℕ) : ℝ) * (Real.pi / 3)
          = (s - Real.pi / 3) + 2 * Real.pi := by
        push_cast
        ring
      rw [harg, Real.cos_add_two_pi]
      exact Real.cos_pos_of_mem_Ioo ⟨by linarith, by linarith⟩
    exact ⟨iff_of_true hp (by decide), iff_of_false (not_lt.mpr hp.le) (by decide)⟩

/-! ### G1 2.  The `direction` / angle interface

`direction (t : Angles) = Circle.exp t` as a complex unit, so `direction (x : Angles)`
for a real `x` is the unit vector `(cos x, sin x)`; the repository's own
`direction_inner_real` (`Interfaces.lean:198`, hence the §0 import) is the inner
product with it. -/

lemma direction_re_coe (x : ℝ) : (direction ((x : ℝ) : Angles)).re = Real.cos x := by
  rw [direction_real, Circle.coe_exp, Complex.exp_ofReal_mul_I_re]

lemma direction_im_coe (x : ℝ) : (direction ((x : ℝ) : Angles)).im = Real.sin x := by
  rw [direction_real, Circle.coe_exp, Complex.exp_ofReal_mul_I_im]

/-- Inner product of two unit directions: `cos` of the difference of the angles. -/
lemma inner_coe_coe (a b : ℝ) :
    ⟪direction ((a : ℝ) : Angles), direction ((b : ℝ) : Angles)⟫ = Real.cos (a - b) := by
  rw [direction_inner_real a, direction_re_coe b, direction_im_coe b, Real.cos_sub]

/-- `sixAngle j` is the real angle `j * pi/3`. -/
lemma sixAngle_coe (j : Fin 6) :
    sixAngle j = (((j.val : ℝ) * (Real.pi / 3) : ℝ) : Angles) := by
  have hsix : sixAngle j = j.val • (sixty : Angles) := rfl
  have hns : j.val • sixty = (j.val : ℝ) * (Real.pi / 3) := by
    simp only [nsmul_eq_mul, sixty]
  rw [hsix, ← AddCircle.coe_nsmul, hns]

/-- The real representative of `(s : Angles) + sixAngle j`. -/
lemma add_sixAngle_coe (s : ℝ) (j : Fin 6) :
    (s : Angles) + sixAngle j = ((s + (j.val : ℝ) * (Real.pi / 3) : ℝ) : Angles) := by
  rw [sixAngle_coe j, ← AddCircle.coe_add]

/-- The inner product at phase `j` against the unit direction of phase `k`. -/
lemma inner_sixAngle (s : ℝ) (j k : Fin 6) :
    ⟪direction ((s : Angles) + sixAngle j), direction (sixAngle k)⟫
      = Real.cos (s + ((j.val : ℝ) - (k.val : ℝ)) * (Real.pi / 3)) := by
  rw [add_sixAngle_coe s j, sixAngle_coe k, inner_coe_coe]
  congr 1
  ring

/-! ### G1 3.  The label geometry of A6

Label `i : Fin 6` of a paired six-tuple carries the direction of phase
`2 * (i.val / 2)`: `i = 0,1` give phase `0`, `i = 2,3` phase `2`, `i = 4,5`
phase `4`. -/

lemma two_mul_div_two_le_add_six (i j : Fin 6) : 2 * (i.val / 2) ≤ j.val + 6 := by
  have hi : i.val < 6 := i.isLt
  have h1 : 2 * (i.val / 2) ≤ i.val := by
    rw [Nat.mul_comm]
    exact Nat.div_mul_le_self i.val 2
  exact Nat.le_trans h1 (Nat.le_trans (Nat.le_of_lt hi) (Nat.le_add_left 6 j.val))

lemma two_mul_div_two_lt_six (i : Fin 6) : 2 * (i.val / 2) < 6 := by
  have h1 : 2 * (i.val / 2) ≤ i.val := by
    rw [Nat.mul_comm]
    exact Nat.div_mul_le_self i.val 2
  exact lt_of_le_of_lt h1 i.isLt

/-! ### G1 4.  G1b2: the sign of the inner product at phase `j`

The residue is written exactly as in the bridge's `pos_char`,
`(j.val + 6 - 2 * (i.val / 2)) % 6`:  shifting `j.val` by `+6` costs a full turn
`2 * pi`, which `cos` does not see, and lets the natural-number subtraction
`j.val + 6 - 2 * (i.val / 2)` stay in `NN`. -/

theorem sign_of_paired (v : Fin 6 → ℂ) (k : Fin 6 → Fin 6)
    (hk : ∀ i : Fin 6, (k i).val = 2 * (i.val / 2))
    (hv : ∀ i : Fin 6, v i = direction (sixAngle (k i)))
    (j : Fin 6) (s : ℝ) (hs : |s| < Real.pi / 6) (i : Fin 6) :
    (0 < ⟪direction ((s : Angles) + sixAngle j), v i⟫ ↔
        (j.val + 6 - 2 * (i.val / 2)) % 6 ∈ ({0, 1, 5} : Finset ℕ)) ∧
      (⟪direction ((s : Angles) + sixAngle j), v i⟫ < 0 ↔
        (j.val + 6 - 2 * (i.val / 2)) % 6 ∈ ({2, 3, 4} : Finset ℕ)) := by
  have hle : 2 * (i.val / 2) ≤ j.val + 6 := two_mul_div_two_le_add_six i j
  have hcast : ((j.val + 6 - 2 * (i.val / 2) : ℕ) : ℝ)
      = (j.val : ℝ) + 6 - ((2 * (i.val / 2) : ℕ) : ℝ) := by
    rw [Nat.cast_sub hle] <;> push_cast <;> ring
  have hinner : ⟪direction ((s : Angles) + sixAngle j), v i⟫
      = Real.cos (s + ((j.val + 6 - 2 * (i.val / 2) : ℕ) : ℝ) * (Real.pi / 3)) := by
    have hred : ⟪direction ((s : Angles) + sixAngle j), v i⟫
        = Real.cos (s + ((j.val : ℝ) - ((2 * (i.val / 2) : ℕ) : ℝ)) * (Real.pi / 3)) := by
      rw [hv i, inner_sixAngle, hk i]
    rw [hred]
    have harg : s + ((j.val + 6 - 2 * (i.val / 2) : ℕ) : ℝ) * (Real.pi / 3)
        = (s + ((j.val : ℝ) - ((2 * (i.val / 2) : ℕ) : ℝ)) * (Real.pi / 3))
          + 2 * Real.pi := by
      rw [hcast]
      ring
    rw [harg, Real.cos_add_two_pi]
  rw [hinner]
  exact cos_sign_strict s (j.val + 6 - 2 * (i.val / 2)) hs

/-- G1b2 with the task's literal hypothesis shape: the paired six-tuple
`v i = direction (sixAngle <.2 * (i.val / 2), _>.)`. -/
theorem sign_of_paired_fin (v : Fin 6 → ℂ)
    (hv : ∀ i : Fin 6,
      v i = direction (sixAngle ⟨2 * (i.val / 2), two_mul_div_two_lt_six i⟩))
    (j : Fin 6) (s : ℝ) (hs : |s| < Real.pi / 6) (i : Fin 6) :
    (0 < ⟪direction ((s : Angles) + sixAngle j), v i⟫ ↔
        (j.val + 6 - 2 * (i.val / 2)) % 6 ∈ ({0, 1, 5} : Finset ℕ)) ∧
      (⟪direction ((s : Angles) + sixAngle j), v i⟫ < 0 ↔
        (j.val + 6 - 2 * (i.val / 2)) % 6 ∈ ({2, 3, 4} : Finset ℕ)) :=
  sign_of_paired v (fun i => ⟨2 * (i.val / 2), two_mul_div_two_lt_six i⟩)
    (fun _ => rfl) hv j s hs i

/-! ### G1 6.  B1: the residue rule *is* the bridge's table

Both proofs are a single `decide` over `Fin 6 x Fin 6`: the quantifier is inside
the proposition (`∀ (j i : Fin 6), ...`, the bridge's own `pos_char` shape), so
after typeclass search `decide` sees a closed 36-case `Finset`/`Nat` computation,
and every ingredient (`pos`, `Finset.univ \ ·`, `%`, `Finset` membership) is
computable.  This is the same `decide` the bridge itself already uses for
`pos_char`, `resOut_spec`, `resIn_spec`, `g_eq`; see NOTES-mB.md §4 for the check
that `decide` can reduce `Finset.univ : Finset (Fin 6)`, and for why the
quantifier must be inside the proposition rather than a binder.

Note the orientation: residue first, table second -- exactly the shape the sign
table is consumed in (`sign_of_paired`'s residue gives *the* table member, so
one `Iff.trans` per side closes `SignTable`). -/

/-- **B1, positive side.**  At phase `j`, the residue rule of the six paired
directions names exactly the bridge's `pos j`.

The `∀` is *inside* the proposition, not in the binder, because `decide` has to
see a closed statement: with `pos` applied to a free variable `j` nothing
reduces.  This is the same shape as the bridge's own `pos_char`. -/
lemma pos_char' : ∀ (j i : Fin 6),
    ((j.val + 6 - 2 * (i.val / 2)) % 6 ∈ ({0, 1, 5} : Finset ℕ)) ↔ i ∈ pos j := by
  decide

/-- **B1, negative side.**  At phase `j`, the negative residue rule names
exactly the bridge's `neg j`. -/
lemma neg_char' : ∀ (j i : Fin 6),
    ((j.val + 6 - 2 * (i.val / 2)) % 6 ∈ ({2, 3, 4} : Finset ℕ)) ↔ i ∈ neg j := by
  decide

/-- **B1, negative side, `decide`-free fallback.**  Same statement as
`neg_char'`, proved from `pos_char'` and `mod6_not_mem` instead of by deciding
over `neg` directly.  If `neg_char'`'s `decide` does not reduce on the parent's
toolchain, delete it and use this one -- nothing else changes. -/
lemma neg_char_alt : ∀ (j i : Fin 6),
    ((j.val + 6 - 2 * (i.val / 2)) % 6 ∈ ({2, 3, 4} : Finset ℕ)) ↔ i ∈ neg j := by
  intro j i
  rw [neg_mem j i, ← pos_char' j i]
  exact mod6_not_mem (j.val + 6 - 2 * (i.val / 2))

/-! ### G1 7.  The closing lemma: `SignTable` from the pairing hypothesis

The only real hypothesis is the one the A6 configuration supplies:
**the six approach directions are the six A6 palette directions, paired**, i.e.
label `i` carries `direction (sixAngle (2 * (i.val / 2)))` -- `i = 0,1` the same
direction, `i = 2,3` the next, `i = 4,5` the last.  Under it, `SignTable v` is
unconditional. -/

/-- **The bridge's `SignTable` from the paired approach directions.**  (In
`G1-Finish-mB.lean` this carried a paste instruction; it is now in the bridge's
own namespace, so `SignTable`, `pos`, `neg` and `arc` are §5, §1 and §2's
definitions themselves.) -/
theorem signTable_of_paired (v : Fin 6 → ℂ) (k : Fin 6 → Fin 6)
    (hk : ∀ i : Fin 6, (k i).val = 2 * (i.val / 2))
    (hv : ∀ i : Fin 6, v i = direction (sixAngle (k i))) :
    SignTable v := by
  intro j t ht
  obtain ⟨s, hs, hst⟩ := ht
  subst hst
  exact ⟨fun i => ((sign_of_paired v k hk hv j s hs i).1).trans (pos_char' j i),
    fun i => ((sign_of_paired v k hk hv j s hs i).2).trans (neg_char' j i)⟩

/-- **The same, with the canonical pairing and no `k` to supply.** -/
theorem signTable_of_paired_fin (v : Fin 6 → ℂ)
    (hv : ∀ i : Fin 6,
      v i = direction (sixAngle ⟨2 * (i.val / 2), two_mul_div_two_lt_six i⟩)) :
    SignTable v :=
  signTable_of_paired v (fun i => ⟨2 * (i.val / 2), two_mul_div_two_lt_six i⟩)
    (fun _ => rfl) hv


end A6
end EuclideanFiveColor
end
end OAI
