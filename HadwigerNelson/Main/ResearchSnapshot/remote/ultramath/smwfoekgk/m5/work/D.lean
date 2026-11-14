import C

/-!
# Consequences of Theorem A

* `differenceLaw_id_C_eq_zero_of_ergodic`: Theorem A at `d = id`, i.e. exactly the
  C-nullity half of the `IsWild` conclusion that `ergodic_wild_fourier`
  (`Analysis/PlaneSpectrum/Ergodicity.lean`) currently obtains from `UniversalGood`.
  (The other half, `MeasurePreserving (u • ·)` of the difference law, is
  `relative_difference_invariant`, already in the tree.)
* `differenceLaw_C_eq_one_of_diag`: sharpness — the diagonal hypothesis (H2) cannot be
  dropped.
-/

namespace OAI
noncomputable section
open MeasureTheory ProbabilityTheory Filter
open scoped ENNReal NNReal Topology

namespace PlaneFiveColor.Spectral
namespace RelativeSingularity

variable {Y : Type*} [MeasurableSpace Y] [StandardBorelSpace Y] [Nonempty Y]
  {X : Type*} [MeasurableSpace X] [StandardBorelSpace X] [Nonempty X]

/-- **Theorem A at `d = id`.** -/
theorem differenceLaw_id_C_eq_zero_of_ergodic
    (μ : Measure D) [IsProbabilityMeasure μ]
    (q : D → Y) (hq : Measurable q)
    [ErgodicVAdd Rot (D × D) (EuclideanFiveColor.RelativeProduct.law μ q hq)]
    (hdiag : ¬ ∀ᵐ z ∂(EuclideanFiveColor.RelativeProduct.law μ q hq), z.1 = z.2) :
    EuclideanFiveColor.DifferenceFourier.differenceLaw (μ.map q) (condDistrib id q μ) C = 0 :=
  relative_singularity_of_ergodic (X := D) (Y := Y) μ q hq id measurable_id
    (fun k x => rfl) hdiag

/-- **Sharpness.**  If `d` is a.e. constant on the relative product, the conclusion of
Theorem A fails: the relative difference law gives `C` full mass. -/
theorem differenceLaw_C_eq_one_of_diag
    (μ : Measure X) [IsProbabilityMeasure μ]
    (q : X → Y) (hq : Measurable q) (d : X → D) (hd : Measurable d)
    (h : ∀ᵐ z ∂(EuclideanFiveColor.RelativeProduct.law μ q hq), d z.1 = d z.2) :
    EuclideanFiveColor.DifferenceFourier.differenceLaw (μ.map q) (condDistrib d q μ) C = 1 := by
  have hsub : {z : X × X | d z.1 = d z.2}
      ⊆ (fun z : X × X => d z.1 / d z.2) ⁻¹' (C : Set D) := by
    rintro z hz
    have h1 : d z.1 / d z.2 = (1 : D) := by rw [hz, div_eq_mul_inv, mul_inv_cancel]
    simp only [Set.mem_preimage, h1, C_eq_range]
    exact ⟨0, j_zero⟩
  have hcomp : EuclideanFiveColor.RelativeProduct.law μ q hq
      {z : X × X | d z.1 = d z.2}ᶜ = 0 := by
    rw [ae_iff] at h
    exact h
  have hone : EuclideanFiveColor.RelativeProduct.law μ q hq
      {z : X × X | d z.1 = d z.2} = 1 := by
    have hle : EuclideanFiveColor.RelativeProduct.law μ q hq {z : X × X | d z.1 = d z.2} ≤ 1 := by
      rw [← measure_univ (μ := EuclideanFiveColor.RelativeProduct.law μ q hq)]
      exact measure_mono (Set.subset_univ _)
    refine le_antisymm hle ?_
    have h2 := measure_union_le {z : X × X | d z.1 = d z.2}
      {z : X × X | d z.1 = d z.2}ᶜ (μ := EuclideanFiveColor.RelativeProduct.law μ q hq)
    rw [Set.union_compl_self, measure_univ, hcomp, add_zero] at h2
    exact h2
  have hratm : Measurable (fun z : X × X => d z.1 / d z.2) :=
    (hd.comp measurable_fst).div (hd.comp measurable_snd)
  rw [differenceLaw_eq_law μ q hq d hd, Measure.map_apply hratm measurableSet_C]
  exact le_antisymm prob_le_one (hone ▸ measure_mono hsub)

end RelativeSingularity
end PlaneFiveColor.Spectral
end
end OAI
