import Mathlib

namespace OAI

noncomputable section
open scoped ComplexConjugate

open MeasureTheory ProbabilityTheory scoped ComplexConjugate
namespace EuclideanFiveColor.DifferenceFourier

variable {G Y : Type*} [MeasurableSpace G] [MeasurableSpace Y]
  [CommGroup G] [MeasurableMul₂ G] [MeasurableInv G]

noncomputable def differenceLaw (ν : Measure Y) (κ : Kernel Y G) [IsMarkovKernel κ] :
    Measure G := ((κ ×ₖ κ) ∘ₘ ν).map (fun p : G × G => p.1 / p.2)

instance differenceLaw_probability (ν : Measure Y) [IsProbabilityMeasure ν]
    (κ : Kernel Y G) [IsMarkovKernel κ] : IsProbabilityMeasure (differenceLaw ν κ) := by
  unfold differenceLaw
  infer_instance

variable (χ : G →* Circle)

omit [MeasurableSpace G] [MeasurableMul₂ G] [MeasurableInv G] in
lemma coe_character_div (d e : G) :
    (χ (d / e) : ℂ) = (χ d : ℂ) * conj (χ e : ℂ) := by
  rw [map_div, div_eq_mul_inv, Circle.coe_mul, Circle.coe_inv_eq_conj]

omit [MeasurableMul₂ G] [MeasurableInv G] in
lemma independent_coefficient (κ : Measure G) [IsProbabilityMeasure κ] :
    (∫ p : G × G, (χ (p.1 / p.2) : ℂ) ∂κ.prod κ) =
      (‖∫ d, (χ d : ℂ) ∂κ‖ ^ 2 : ℝ) := by
  calc
    _ = ∫ p : G × G, (χ p.1 : ℂ) * conj (χ p.2 : ℂ) ∂κ.prod κ :=
      integral_congr_ae (Filter.Eventually.of_forall (fun p => coe_character_div χ p.1 p.2))
    _ = (∫ d, (χ d : ℂ) ∂κ) * (∫ d, conj (χ d : ℂ) ∂κ) := by
      convert integral_prod_mul (fun d => (χ d : ℂ)) (fun d => conj (χ d : ℂ)) using 1 <;> infer_instance
    _ = _ := by rw [integral_conj, Complex.mul_conj, Complex.normSq_eq_norm_sq]

lemma difference_coefficient (hχ : Measurable (fun d => (χ d : ℂ))) (ν : Measure Y) [IsProbabilityMeasure ν]
    (κ : Kernel Y G) [IsMarkovKernel κ] :
    (∫ d, (χ d : ℂ) ∂differenceLaw ν κ) =
      ((∫ y, (‖∫ d, (χ d : ℂ) ∂κ y‖ ^ 2 : ℝ) ∂ν : ℝ) : ℂ) := by
  have hm := hχ
  have hdiv : Measurable (fun p : G × G => p.1 / p.2) :=
    measurable_fst.div measurable_snd
  rw [differenceLaw, integral_map hdiv.aemeasurable hm.aestronglyMeasurable,
    Measure.comp_eq_comp_const_apply]
  rw [Kernel.integral_comp]
  · simp only [Kernel.const_apply, Kernel.prod_apply]
    change (∫ y, (∫ p : G × G, (χ (p.1 / p.2) : ℂ) ∂(κ y).prod (κ y)) ∂ν) = _
    rw [← integral_complex_ofReal]
    apply integral_congr_ae
    exact Filter.Eventually.of_forall (fun y => independent_coefficient χ (κ y))
  · exact Integrable.of_bound (hm.comp hdiv).aestronglyMeasurable 1
      (Filter.Eventually.of_forall (fun _ => (Circle.norm_coe _).le))

end EuclideanFiveColor.DifferenceFourier

end

end OAI
