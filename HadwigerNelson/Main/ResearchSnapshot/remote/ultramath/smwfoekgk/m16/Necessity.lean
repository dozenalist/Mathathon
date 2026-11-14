/-
Necessity certificate for hypothesis (H2) of "Theorem A" / for the missing side condition (N).

At the TOP factor `p = id` the two conditionally independent samples coincide, so the
conditional difference law is `delta_1`; since `1 = j 0` lies in the closed subgroup `C` of
continuous characters, its `C`-mass is `1`, not `0`.  Consequences, all machine-checked below:

* `differenceLaw_apply_C_of_ae_id` : any Markov kernel that is a.e. the identity kernel has
  conditional difference law of `C`-mass 1.
* `differenceLaw_self_apply_C`       : the instance for `condDistrib id id mu`, for an arbitrary
  standard Borel space (no group structure beyond `D`).
* `not_universalGood_id`             : `UniversalGood mu (id : D -> D)` is FALSE for every wild
  probability `mu`.  Hence the existing maximality over `UniversalGood` (CodedMax) can never
  return the top factor, and no maximality/ergodicity/compactness argument can replace the
  non-measurability hypothesis: printed Lemma 2.7 is false at `Y = X`.
-/
import OAI.MeasureTheory.CompactFactors.ConditionalLimits

noncomputable section
open MeasureTheory ProbabilityTheory
open scoped ENNReal

namespace OAI
namespace PlaneFiveColor.Spectral

/-- A Markov kernel that agrees a.e. with the identity kernel has conditional difference law
concentrated on `1`: conditionally on `y` both samples equal `y`. -/
theorem differenceLaw_apply_C_of_ae_id {ν : Measure D} [IsProbabilityMeasure ν]
    (κ : Kernel D D) [IsMarkovKernel κ] (h : κ =ᵐ[ν] Kernel.id) :
    EuclideanFiveColor.DifferenceFourier.differenceLaw ν κ (C : Set D) = 1 := by
  classical
  have hae : ∀ᵐ y ∂ν, κ y = Measure.dirac y := by
    filter_upwards [h] with y hy
    rw [hy, Kernel.id_apply]
  have hm : MeasurableSet {p : D × D | p.1 / p.2 ∈ (C : Set D)} :=
    measurableSet_C.preimage (measurable_fst.div measurable_snd)
  have hfib : ∀ᵐ y ∂ν, (κ ×ₖ κ) y {p : D × D | p.1 / p.2 ∈ (C : Set D)} = 1 := by
    filter_upwards [hae] with y hy
    rw [Kernel.prod_apply, hy, Measure.dirac_prod_dirac]
    rw [Measure.dirac_apply' _ hm]
    simp [C.one_mem]
  rw [EuclideanFiveColor.DifferenceFourier.differenceLaw,
    Measure.map_apply (f := fun p : D × D => p.1 / p.2)
      (measurable_fst.div measurable_snd) measurableSet_C]
  change (Measure.bind ν (κ ×ₖ κ)) {p : D × D | p.1 / p.2 ∈ (C : Set D)} = 1
  rw [Measure.bind_apply hm (Kernel.measurable _).aemeasurable]
  calc ∫⁻ y, (κ ×ₖ κ) y {p : D × D | p.1 / p.2 ∈ (C : Set D)} ∂ν
      = ∫⁻ _y, (1 : ℝ≥0∞) ∂ν := lintegral_congr_ae hfib
    _ = 1 := by simp

/-- The conditional difference law of the identity map over itself has `C`-mass one. -/
theorem differenceLaw_self_apply_C (μ : Measure D) [IsProbabilityMeasure μ] :
    EuclideanFiveColor.DifferenceFourier.differenceLaw (μ.map (id : D → D))
      (condDistrib (id : D → D) (id : D → D) μ) (C : Set D) = 1 :=
  differenceLaw_apply_C_of_ae_id _
    (condDistrib_self (μ := μ) (Y := (id : D → D)) measurable_id.aemeasurable)

/-- `UniversalGood` fails at the top factor of any system with wild law: the maximality of
`CodedMax` cannot return the identity factor, and (H2) is not removable. -/
theorem not_universalGood_id (μ : Measure D) [IsProbabilityMeasure μ] (hw : IsWild μ) :
    ¬ UniversalGood μ (id : D → D) := by
  intro hgood
  have h0 : EuclideanFiveColor.DifferenceFourier.differenceLaw (μ.map (id : D → D))
      (condDistrib (id : D → D) (id : D → D) μ) (C : Set D) = 0 :=
    hgood id measurable_id (fun _ => Filter.Eventually.of_forall fun _ => rfl) (by simpa using hw)
  rw [differenceLaw_self_apply_C] at h0
  exact one_ne_zero h0

end PlaneFiveColor.Spectral
end OAI

#print axioms OAI.PlaneFiveColor.Spectral.differenceLaw_apply_C_of_ae_id
#print axioms OAI.PlaneFiveColor.Spectral.differenceLaw_self_apply_C
#print axioms OAI.PlaneFiveColor.Spectral.not_universalGood_id
#check @OAI.PlaneFiveColor.Spectral.not_universalGood_id
#check @OAI.PlaneFiveColor.Spectral.differenceLaw_self_apply_C
