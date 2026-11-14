/-
  K6Ternary.lean -- machine-checked core of the k = 6 palette theorem.

  Companion to ../k6-ternary-palette.md.  K6Finite.lean is the same finite
  part with light imports; it is duplicated here so that this file is
  self-contained.

  Analytic input, supplied by the paper for a weak measurable six-colouring at
  every fixed centre `x` (labels `Fin 6`, directions `e` on the unit circle,
  `R` = rotation by pi/3):

    (P2)  P e ∩ P (R e) = ∅  for a.e. e        paper (5.7)
    (P3)  P e ∪ P v ≠ Finset.univ for a.e. (e,v)   paper (5.2): the point
                                               x + e + v carries a colour
                                               outside P e ∪ P v
  and `R` preserves angular measure.  Proposition 5.6 at k = 6 (K6-BARRIER §1)
  gives the palette bound |P e| <= 3 used implicitly by (P3)'s analysis.

  Conclusions checked here:
    * two disjoint 3-element palettes in Fin 6 are complementary (the label
      count 2 * (k - 3) = k that is special to k = 6);
    * hence |P e| = 3 and |P (R e)| = 3 cannot both hold, so `R` carries the
      ternary set essentially into its complement;
    * hence the ternary set has measure at most 1/2;
    * for any nonempty label set T, the palette cannot contain T a.e.
-/
import Mathlib.MeasureTheory.Measure.MeasureSpace
import Mathlib.MeasureTheory.Measure.Typeclasses.Probability
import Mathlib.Data.Finset.Card
import Mathlib.Data.Fintype.Powerset
import Mathlib.Data.Fin.Basic

open MeasureTheory
open scoped ENNReal

namespace K6Ternary

/-- Two disjoint 3-element subsets of `Fin 6` are complementary. -/
theorem union_eq_univ_of_card_three {s t : Finset (Fin 6)}
    (hs : s.card = 3) (ht : t.card = 3) (hd : Disjoint s t) : s ∪ t = Finset.univ := by
  refine Finset.eq_of_subset_of_card_le (fun a _ => Finset.mem_univ a) ?_
  rw [Finset.card_union_of_disjoint hd, hs, ht]
  simp

/-- **Main theorem.**  A palette function on a probability space of directions
satisfying (P2) and (P3) has its ternary set of measure at most one half. -/
theorem two_mul_measure_ternary_le_one
    {α : Type*} [MeasurableSpace α] {μ : Measure α} [IsProbabilityMeasure μ]
    (P : α → Finset (Fin 6)) (R : α → α)
    (hRμ : ∀ s, MeasurableSet s → μ (R ⁻¹' s) = μ s)
    (hAm : MeasurableSet {e | (P e).card = 3})
    (hdisj : ∀ᵐ e ∂μ, Disjoint (P e) (P (R e)))
    (hunc : ∀ᵐ e ∂μ, P e ∪ P (R e) ≠ Finset.univ) :
    2 * μ {e | (P e).card = 3} ≤ 1 := by
  set A : Set α := {e | (P e).card = 3} with hA
  -- no direction and its 60-degree rotation are both ternary
  have hAB : ∀ᵐ e ∂μ, e ∈ A → e ∉ R ⁻¹' A := by
    filter_upwards [hdisj, hunc] with e hd hu
    intro heA heRA
    simp only [hA, Set.mem_setOf_eq] at heA
    simp only [Set.mem_preimage, hA, Set.mem_setOf_eq] at heRA
    exact hu (union_eq_univ_of_card_three heA heRA hd)
  have hnull : μ (A ∩ R ⁻¹' A) = 0 := by
    refine measure_mono_null ?_ (ae_iff.mp hAB)
    intro e he
    simp only [Set.mem_inter_iff, Set.mem_preimage, Set.mem_setOf_eq] at he ⊢
    exact fun h => (h he.1) he.2
  -- additivity with a null intersection
  have hkey : μ A + μ (R ⁻¹' A) = μ (A ∪ R ⁻¹' A) + μ (A ∩ R ⁻¹' A) :=
    (measure_union_add_inter' hAm (R ⁻¹' A)).symm
  have hmono : μ (A ∪ R ⁻¹' A) ≤ 1 := by
    calc μ (A ∪ R ⁻¹' A) ≤ μ Set.univ := measure_mono (Set.subset_univ _)
      _ = 1 := measure_univ
  have hsum : μ A + μ A ≤ 1 := by
    have h : μ A + μ (R ⁻¹' A) = μ (A ∪ R ⁻¹' A) := by
      rw [hkey, hnull, add_zero]
    rw [hRμ A hAm] at h
    rw [h]
    exact hmono
  calc 2 * μ A = μ A + μ A := two_mul _
    _ ≤ 1 := hsum

/-- **No almost-everywhere constant palette.**  For any nonempty label set `T`
the directions whose palette contains `T` are not all directions: (P2) would
force `T` to meet `∅`. -/
theorem not_ae_subset_palette {α : Type*} [MeasurableSpace α] {μ : Measure α}
    [IsProbabilityMeasure μ]
    (P : α → Finset (Fin 6)) (R : α → α) {T : Finset (Fin 6)} (hT : T.Nonempty)
    (hRT : ∀ᵐ e ∂μ, T ⊆ P e → T ⊆ P (R e))
    (hdisj : ∀ᵐ e ∂μ, Disjoint (P e) (P (R e)))
    (hae : ∀ᵐ e ∂μ, T ⊆ P e) : False := by
  have h2 : ∀ᵐ e ∂μ, T ⊆ P (R e) := by
    filter_upwards [hae, hRT] with e h1 h2
    exact h2 h1
  have hfalse : ∀ᵐ e ∂μ, False := by
    filter_upwards [hae, h2, hdisj] with e h1e h2e h3e
    have hsub : ∀ i, i ∈ T → i ∈ P e ∩ P (R e) :=
      fun i hi => Finset.mem_inter.mpr ⟨h1e hi, h2e hi⟩
    have hemp : ((P e) ∩ (P (R e)) : Finset (Fin 6)) = ∅ :=
      Finset.disjoint_iff_inter_eq_empty.mp h3e
    rw [hemp] at hsub
    obtain ⟨i, hi⟩ := hT
    simpa using hsub i hi
  obtain ⟨e, he⟩ := hfalse.exists
  exact he

end K6Ternary
