/-
  A6 palette producer -- lane B of swarm smwguinbz (member m2).

  BRIDGE: from the repository's own continuum / angular restriction lemmas
  (`continuum_outer_restriction`, `continuum_inner_restriction`,
  `finite_support_exclusion_ae`, `palette_sixty_disjoint`) to

    (1) the SIX FINITE CONULL ANGULAR INPUTS: one `∀ᵐ`-statement, indexed by
        `Fin 6`, that carries all six inner hits, all six outer hits and all six
        adjacency disjointnesses at the single centre `x`  (`ae_restrictions`,
        raw form, no geometric hypothesis), and its table form
        (`ae_six_inputs`: forced label `f j`, other-hit set `H j`);
    (2) an A.E. CANONICAL SUBPALETTE: for angular-a.e. `t` in the fundamental
        arc, both `f j` and its canonical partner `f j + 3` lie in the palette
        at phase `j`  (`ae_canonical_subpalette`), and the corresponding
        statement for a.e. angle (`ae_canonical_subpalette_global`).

  Nothing here is proved about trig or about the pure `Fin 6` forcing; both are
  explicit hypotheses, named and documented (`SignTable`, `ForcingLemma`,
  `ArcCover`).  See NOTES-m2.md for the exact remains.

  Source declarations used (paths relative to the repository root; line numbers
  checked against the checkout in this workspace):

    lean/OAI/Geometry/PlaneColoring/AngularBoundary.lean
      :103  def sixAngle
      :104  lemma sixAngle_step
      :147  def Straddle
      :235  structure ApproachingContinuum
      :259  lemma continuum_outer_restriction
      :279  lemma continuum_inner_restriction
      :308  def spatialSupport
      :317  lemma finite_support_exclusion_ae
    lean/OAI/Geometry/PlaneColoring/PaletteTransport.lean
      :390  def sixty
      :450  lemma palette_sixty_disjoint
    lean/OAI/Geometry/PlaneColoring/Palettes.lean
      :35   def palette
      :38   lemma mem_palette
    lean/OAI/Geometry/PlaneColoring/Coloring.lean
      :16   abbrev Angles
      :17   def angularMeasure
      :18   def direction
    lean/OAI/Geometry/PlaneColoring/PaletteDensity.lean
      :158  lemma angleMk_quasiMeasurePreserving
-/

import OAI.Geometry.PlaneColoring.AngularBoundary
import OAI.Geometry.PlaneColoring.PaletteTransport

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
shifted angles `t + sixAngle j` simultaneously.  `finite_support_exclusion_ae`
stays in the *space* variable `z : ℂ` and only supplies the pointwise `hJ` that
`continuum_outer/inner_restriction` consume; the angular a.e. statements are
transported by the same rotation invariance the repository itself uses
(`(measurePreserving_add_right angularMeasure (sixAngle j)).quasiMeasurePreserving.ae`,
cf. `Exclusion.lean:152`). -/

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
  classical
  -- (S): the source common-support exclusion, verbatim at `F = eSet`.
  have hexc := finite_support_exclusion_ae c hc K eSet hsupp
  -- (H): the pointwise membership `hJ` consumed by the two restriction lemmas.
  have hJout (j : Fin 6) : ∀ᵐ z : ℂ ∂volume,
      (∀ i ∈ pos j, z ∈ Straddle (K i)) → c z ∈ resOut j := by
    filter_upwards [hexc] with z hz hzE
    exact (resOut_spec j (c z)).mpr fun i hi => hz i (hzE i hi)
  have hJin (j : Fin 6) : ∀ᵐ z : ℂ ∂volume,
      (∀ i ∈ neg j, z ∈ Straddle (K i)) → c z ∈ resIn j := by
    filter_upwards [hexc] with z hz hzE
    exact (resIn_spec j (c z)).mpr fun i hi => hz i (hzE i hi)
  -- (OUT)/(IN): the two source continuum restrictions.
  have hout (j : Fin 6) := continuum_outer_restriction c hc (pos j) hK (hJout j)
  have hin (j : Fin 6) := continuum_inner_restriction c hc (neg j) hK (hJin j)
  -- Rotate each of them to the six phases `t + sixAngle j`.
  have houtj (j : Fin 6) : ∀ᵐ t ∂angularMeasure,
      (∀ i ∈ pos j, 0 < ⟪direction (t + sixAngle j), v i⟫) →
        (palette c hc x (t + sixAngle j) ∩ resOut j).Nonempty :=
    (measurePreserving_add_right angularMeasure (sixAngle j)).quasiMeasurePreserving.ae
      (hout j)
  have hinj (j : Fin 6) : ∀ᵐ t ∂angularMeasure,
      (∀ i ∈ neg j, ⟪direction (t + sixAngle j), v i⟫ < 0) →
        (palette c hc x (t + sixAngle j) ∩ resIn j).Nonempty :=
    (measurePreserving_add_right angularMeasure (sixAngle j)).quasiMeasurePreserving.ae
      (hin j)
  -- (DIS): sixty-degree covariance of the palette, rotated to the same six phases.
  have hdisj (j : Fin 6) : ∀ᵐ t ∂angularMeasure,
      Disjoint (palette c hc x (t + sixAngle j))
        (palette c hc x (t + sixAngle (j + 1))) := by
    have h := (measurePreserving_add_right angularMeasure (sixAngle j)).quasiMeasurePreserving.ae
      (palette_sixty_disjoint c hc hw x)
    filter_upwards [h] with t ht
    rw [sixAngle_step, ← add_assoc]
    exact ht
  filter_upwards [ae_all_iff.mpr houtj, ae_all_iff.mpr hinj, ae_all_iff.mpr hdisj]
    with t ho hi hd
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
  have hshift (j : Fin 6) :=
    (measurePreserving_add_right angularMeasure (sixAngle j)).quasiMeasurePreserving.ae
      (ae_canonical_subpalette c hc hw hK hsupp hsign hforce)
  filter_upwards [ae_all_iff.mpr hshift, hcover] with θ hθ hcov
  obtain ⟨t, harc, j, rfl⟩ := hcov
  exact ⟨j, hθ j harc j⟩

end A6
end EuclideanFiveColor
end
end OAI
