/-
  A6 palette producer -- **the GLUED bridge**, `A6-Bridge-r2-G3.lean`.

      supervisor/simplify-lean/A6-Bridge-r2.lean    §1-§9   (compiled clean)
    + G3-ArcCover-mA-r2.lean §2-§5, as §10          (compiled clean standalone)
    + §11 `ae_canonical_subpalette_unconditional`   (new)

  COMPILE EVIDENCE.  Both inputs were compiled locally by the parent; this ASSEMBLY
  has not been compiled, and nothing below is a compile claim about it.
    * `A6-Bridge-r2.lean` (sha256 74402da9ef754964e3a732c879e1b31fa3af419db1a465255e6a78b467f9b333):
      PASSED, exit 0, 66.9 s, no `sorry`; `#print axioms` on `ae_restrictions`,
      `ae_six_inputs`, `ae_canonical_subpalette`, `ae_canonical_subpalette_global`,
      `cos_sign_strict`, `sign_of_paired_fin`, `signTable_of_paired` and
      `signTable_of_paired_fin` gives only
      `[propext, Classical.choice, Quot.sound]`.
    * `G3-ArcCover-mA-r2.lean` (sha256 55c41b56eb82cffcc75248826501a0cf899f5208de6c6920c83fc0386aa012a5):
      PASSED standalone (Mathlib only), exit 0, 83 s, axioms
      `[propext, Classical.choice, Quot.sound]`, no `sorry`.

  SPLICE RECORD.
    * §1-§9 are BYTE-IDENTICAL to `A6-Bridge-r2.lean` lines 135-756 (here: see the
      manifest for the coinciding range).  No statement, body or section heading in
      §1-§9 was touched.
    * §10 is `G3-ArcCover-mA-r2.lean` §2-§5 with its section headings retitled
      `### G3 ...` so they cannot be confused with the bridge's own numbering.  G3's
      §0 scaffold (`Fact` instance, `Angles`, `angularMeasure`, `IsProbabilityMeasure`,
      `IsAddHaarMeasure`, `sixty`, `sixAngle`, `anglesNontrivial`,
      `angularMeasure_nullSingleton`) and its §1 duplicate `def arc` are DROPPED:
      every one of those names is already in scope in this file, and
      `BinaryPalettes.lean` -- reached through
      `AngularBoundary -> BoundaryTrace -> States -> BinaryPalettes` -- already declares
      the two instances, so pasting them would be a redeclaration error rather than a
      harmless redundancy.  `def arc` here is the bridge's §2 definition alone.
    * §11 is the only new statement in the file.

  THE SPLICE TAKES G3 FROM ITS r2, NOT FROM r1.  G3 r1 still contains `le_or_lt` at
  its lines 160 and 168, and that identifier is what failed its standalone compile
  (it no longer exists in the pinned Mathlib for a general `LinearOrder`).  An earlier
  draft of this assembly spliced r1 and therefore carried the defect into §10; the
  pre-publication audit caught it and the builder's G3 input was repointed at
  `G3-ArcCover-mA-r2.lean`.  This file contains no occurrence of `le_or_lt`.

  ENDING.  The file ends with `#print axioms ae_canonical_subpalette_unconditional`,
  preceded by `open OAI.EuclideanFiveColor.A6` so that the short name resolves after
  the namespaces are closed; compiling the file prints that axiom list.

  RULES KEPT.  No `sorry`, no `admit`, no `native_decide`, no `axiom`, no
  `@[implemented_by]`, no `set_option maxHeartbeats` -- the heartbeat budget is
  untouched everywhere, including §4.  No assumption beyond the named hypotheses of
  §5, §7, §8 and §9.
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

/-! ## 10. G3: `arcCover`

`G3-ArcCover-mA.lean` (swarm `smwgwui56`, lane A, accepted) §2-§5.  The source's
§0 scaffold and its §1 duplicate `def arc` are dropped -- see the header; every
name in the scaffold is already in scope here and the two instances it redeclares
(`anglesNontrivial`, `angularMeasure_nullSingleton`) would clash with
`BinaryPalettes.lean`, which is in the import closure.

§2 arithmetic of `sixty`, §3 the pointwise cover off the six exceptional points
`π/6 + m·sixty` (`m : ℤ`), §4 the nullity of those six points, §5 the theorem
`arcCover`: §8's `def ArcCover`, proved outright, with no hypothesis.
Section numbers below are the source file's, prefixed `G3`.
-/
/-! ### G3 2. Arithmetic of `sixty` and of `sixAngle` -/

lemma sixty_pos : (0 : ℝ) < sixty := by
  simp only [sixty]
  positivity

lemma sixty_ne : sixty ≠ 0 := sixty_pos.ne'

/-- `6 · 60° = 360°`. -/
lemma two_pi_eq_six_sixty : 2 * Real.pi = 6 * sixty := by
  simp only [sixty]
  ring

/-- `30° = π/6`. -/
lemma pi_six_eq : sixty / 2 = Real.pi / 6 := by
  simp only [sixty]
  ring

/-- `sixAngle j` is the circle point `j · 60°`, written as a real multiple of `sixty`. -/
lemma sixAngle_eq_coe (j : Fin 6) : sixAngle j = (((j.val : ℝ) * sixty : ℝ) : Angles) := by
  show j.val • (sixty : Angles) = (((j.val : ℝ) * sixty : ℝ) : Angles)
  rw [← AddCircle.coe_nsmul, nsmul_eq_mul]

/-- An integral multiple of `2π` is `0` in `Angles`. -/
lemma coe_period_mul (m : ℤ) : (((m : ℝ) * (2 * Real.pi) : ℝ) : Angles) = 0 := by
  rw [AddCircle.coe_eq_zero_iff]
  exact ⟨m, by rw [zsmul_eq_mul]⟩

/-- Euclidean division by `6`: every integer is `j.val + 6m` with `j : Fin 6`. -/
lemma mod_six_spec (n : ℤ) :
    ∃ j : Fin 6, ∃ m : ℤ, (n : ℝ) = (j.val : ℝ) + 6 * (m : ℝ) := by
  have h0 : 0 ≤ n % 6 := Int.emod_nonneg n (by norm_num)
  have h6 : n % 6 < 6 := Int.emod_lt_of_pos n (by norm_num)
  have hdiv : (n : ℝ) = (((n % 6).toNat : ℕ) : ℝ) + 6 * ((n / 6 : ℤ) : ℝ) := by
    have h : (n : ℤ) = ((n % 6).toNat : ℤ) + 6 * (n / 6) := by
      have h' := Int.emod_add_mul_ediv n 6
      rw [← Int.toNat_of_nonneg h0] at h'
      linarith
    exact_mod_cast h
  have hk : (n % 6).toNat < 6 := by omega
  exact ⟨⟨(n % 6).toNat, hk⟩, n / 6, hdiv⟩

/-! ### G3 3. The pointwise covering step off the six exceptional points -/

/-- **Real-level covering step.**  If `r : ℝ` is not one of the six points
`π/6 + m·sixty` (`m : ℤ`), then its image in `Angles` lies in one of the six translates
`arc + sixAngle j`.  This is `arcCover` with the a.e. statement replaced by its pointwise
form off the (countable) exceptional set. -/
lemma exists_arc_of_not_bad (r : ℝ)
    (hbad : ∀ m : ℤ, r ≠ Real.pi / 6 + (m : ℝ) * sixty) :
    ∃ t ∈ arc, ∃ j : Fin 6, ((r : ℝ) : Angles) = t + sixAngle j := by
  classical
  -- `n` is the nearest integer to `r / sixty`, obtained as `⌊(r + sixty/2)/sixty⌋`.
  obtain ⟨n, hn_le, hn_lt⟩ :
      ∃ n : ℤ, (n : ℝ) * sixty ≤ r + sixty / 2 ∧
        r + sixty / 2 < ((n : ℝ) + 1) * sixty := by
    refine ⟨⌊(r + sixty / 2) / sixty⌋, ?_, ?_⟩
    · rw [← le_div_iff₀ sixty_pos]
      exact Int.floor_le _
    · rw [← div_lt_iff₀ sixty_pos]
      exact Int.lt_floor_add_one _
  -- the fractional shift, in `[-π/6, π/6)`
  set s : ℝ := r - (n : ℝ) * sixty with hs
  have hs_expand : ((n : ℝ) + 1) * sixty = (n : ℝ) * sixty + sixty := by ring
  have hlow : -(Real.pi / 6) ≤ s := by
    rw [hs]
    linarith [pi_six_eq]
  have hhigh : s < Real.pi / 6 := by
    rw [hs]
    rw [hs_expand] at hn_lt
    linarith [pi_six_eq]
  have hs_le : |s| ≤ Real.pi / 6 := by
    rcases le_or_gt 0 s with hs0 | hs0
    · rw [abs_of_nonneg hs0]
      linarith
    · rw [abs_of_neg hs0]
      linarith
  -- the lower endpoint `s = -π/6` is exactly one of the six exceptional points
  have hs_ne : |s| ≠ Real.pi / 6 := by
    intro habs
    rcases le_or_gt 0 s with hs0 | hs0
    · -- `s = π/6` is excluded by the strict floor bound
      have hs1 : s = sixty / 2 := by
        rw [abs_of_nonneg hs0] at habs
        linarith [pi_six_eq]
      rw [hs] at hs1
      have h2 : ((n : ℝ) + 1) * sixty = (n : ℝ) * sixty + sixty := by ring
      rw [h2] at hn_lt
      linarith
    · -- `s = -π/6` forces `r = π/6 + (n-1)·sixty`
      have hs1 : s = -(sixty / 2) := by
        rw [abs_of_neg hs0] at habs
        linarith [pi_six_eq]
      refine hbad (n - 1) ?_
      rw [hs] at hs1
      push_cast
      linarith [pi_six_eq]
  have hs_lt : |s| < Real.pi / 6 := lt_of_le_of_ne hs_le hs_ne
  -- reduce `n` modulo `6` and absorb the difference as a period
  obtain ⟨j, m, hm⟩ := mod_six_spec n
  refine ⟨(s : Angles), ⟨s, hs_lt, rfl⟩, j, ?_⟩
  have hreal : r - (s + (j.val : ℝ) * sixty) = (m : ℝ) * (2 * Real.pi) := by
    rw [hs, hm, two_pi_eq_six_sixty]
    ring
  have hzero : (((r - (s + (j.val : ℝ) * sixty)) : ℝ) : Angles) = 0 := by
    rw [AddCircle.coe_eq_zero_iff]
    exact ⟨m, by rw [zsmul_eq_mul]; exact hreal.symm⟩
  have hEq : ((r : ℝ) : Angles) -
      (((s : ℝ) : Angles) + (((j.val : ℝ) * sixty : ℝ) : Angles)) = 0 := by
    rw [← AddCircle.coe_add, ← AddCircle.coe_sub]
    exact hzero
  have hfin : ((r : ℝ) : Angles) = ((s : ℝ) : Angles) +
      (((j.val : ℝ) * sixty : ℝ) : Angles) := sub_eq_zero.mp hEq
  rw [← sixAngle_eq_coe] at hfin
  exact hfin

/-! ### G3 4. The six exceptional points are null -/

/-- The six points `π/6 + m·60°` of the circle (`m : ℤ`; only `m mod 6` matters). -/
def badSet : Set Angles :=
  Set.range fun m : ℤ => ((Real.pi / 6 + (m : ℝ) * sixty : ℝ) : Angles)

lemma badSet_countable : badSet.Countable := Set.countable_range _

lemma badSet_measure_zero : angularMeasure badSet = 0 :=
  badSet_countable.measure_zero angularMeasure

/-! ### G3 5. `arcCover` — the bridge's `ArcCover`, verbatim -/

/-- **The six translates of the open fundamental arc cover the circle off a null set.**
This is exactly the bridge's `def ArcCover` (`A6-Bridge-m2.lean`, section 8). -/
theorem arcCover : ∀ᵐ θ ∂angularMeasure, ∃ t ∈ arc, ∃ j : Fin 6, θ = t + sixAngle j := by
  filter_upwards [measure_eq_zero_iff_ae_notMem.mp badSet_measure_zero] with θ hθ
  obtain ⟨r, rfl⟩ := QuotientAddGroup.mk_surjective θ
  refine exists_arc_of_not_bad r fun m hrm => hθ ⟨m, ?_⟩
  rw [hrm]


/-! ## 11. The angle-form subpalette with the cover discharged

§8 states the angle form before §10 is available, so it takes the geometric cover
as a hypothesis.  With `arcCover` proved in §10 that hypothesis can be dropped;
this is the form a caller should use.  This declaration has no ancestor in m2 and
is the only new statement in r2.
-/

/-- **A.e. canonical subpalette for a.e. angle, unconditional in the cover.** -/
theorem ae_canonical_subpalette_unconditional (c : ℂ → Fin 6) (hc : Measurable c)
    (hw : WeakColoring 6 c) {x : ℂ} {K : Fin 6 → Set ℂ} {v : Fin 6 → ℂ}
    (hK : ∀ i, ApproachingContinuum x (K i) (v i))
    (hsupp : ∀ i, ∀ j ∈ eSet i, Disjoint (spatialSupport c j) (Straddle (K i)))
    (hsign : SignTable v) (hforce : ForcingLemma) :
    ∀ᵐ θ ∂angularMeasure, ∃ j : Fin 6,
      f j ∈ palette c hc x θ ∧ f j + 3 ∈ palette c hc x θ :=
  ae_canonical_subpalette_global c hc hw hK hsupp hsign hforce arcCover

end A6
end EuclideanFiveColor
end
end OAI

open OAI.EuclideanFiveColor.A6

#print axioms ae_canonical_subpalette_unconditional
