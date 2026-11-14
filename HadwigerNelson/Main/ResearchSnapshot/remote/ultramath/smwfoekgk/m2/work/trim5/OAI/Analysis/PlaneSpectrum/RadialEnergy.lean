import OAI.Analysis.PlaneSpectrum.Energy
import OAI.Analysis.PlaneSpectrum.Selections

namespace OAI

noncomputable section
open scoped ComplexConjugate
namespace PlaneFiveColor.Spectral
lemma equal_moduli_quadratic (A B L : ℝ) (hL : L^2 = A*B) (u : Circle) :
    ‖(A : ℂ) - B*(u : ℂ)^2‖ =
      ‖-(L : ℂ) + (A-B : ℝ)*(u : ℂ) + L*(u : ℂ)^2‖ := by
  have hu : (u : ℂ) * conj (u : ℂ) = 1 := by
    rw [Complex.mul_conj, Circle.normSq_coe, Complex.ofReal_one]
  have hreal : (u : ℂ).re^2 + (u : ℂ).im^2 = 1 := by
    simpa only [Complex.normSq_apply, sq] using Circle.normSq_coe u
  have hleft : (A : ℂ) - B*(u : ℂ)^2 =
      (u : ℂ) * ((A : ℂ)*conj (u : ℂ) - B*(u : ℂ)) := by
    calc
      _ = A*((u : ℂ)*conj (u : ℂ)) - B*(u : ℂ)^2 := by rw [hu, mul_one]
      _ = _ := by ring
  have hright : -(L : ℂ) + (A-B : ℝ)*(u : ℂ) + L*(u : ℂ)^2 =
      (u : ℂ) * (((A-B : ℝ) : ℂ) + L*((u : ℂ)-conj (u : ℂ))) := by
    calc
      _ = -L*((u : ℂ)*conj (u : ℂ)) + (A-B : ℝ)*(u : ℂ) + L*(u : ℂ)^2 := by rw [hu, mul_one]
      _ = _ := by ring
  rw [hleft, hright, norm_mul, norm_mul, Circle.norm_coe, one_mul, one_mul]
  apply (sq_eq_sq₀ (norm_nonneg _) (norm_nonneg _)).mp
  rw [← Complex.normSq_eq_norm_sq, ← Complex.normSq_eq_norm_sq]
  simp only [Complex.normSq_apply, Complex.sub_re, Complex.mul_re, Complex.ofReal_re,
    Complex.ofReal_im, Complex.conj_re, Complex.conj_im, Complex.sub_im, Complex.mul_im,
    Complex.add_re, Complex.add_im, zero_mul, sub_zero, zero_add, add_zero]
  nlinarith [mul_self_nonneg (A-B), mul_self_nonneg (A+B),
    congrArg (fun x : ℝ => (A-B)^2*x) hreal,
    congrArg (fun x : ℝ => 4*x*(u : ℂ).im^2) hL]
end PlaneFiveColor.Spectral
end

noncomputable section
open MeasureTheory ProbabilityTheory Filter EuclideanFiveColor
open scoped ENNReal NNReal ComplexConjugate BoundedContinuousFunction
namespace PlaneFiveColor.Spectral
open EuclideanFiveColor.BoundedMeasurable
variable {Y : Type*} [MeasurableSpace Y] [StandardBorelSpace Y] [Nonempty Y]
variable (μ : Measure D) [IsProbabilityMeasure μ] [ErgodicSMul K D μ]
  (q : D → Y) (hq : Measurable q)
  [MulAction K Y] [MeasurableConstSMul K Y]
  (hqcov : ∀ k : K, ∀ᵐ d ∂μ, q (k • d) = k • q d)
  [ErgodicVAdd Rot (D×D) (RelativeProduct.law μ q hq)]

include hq hqcov in


include hq hqcov in
end PlaneFiveColor.Spectral
end

noncomputable section
open MeasureTheory ProbabilityTheory Filter EuclideanFiveColor
open scoped ENNReal NNReal ComplexConjugate BoundedContinuousFunction
namespace PlaneFiveColor.Spectral
open EuclideanFiveColor.BoundedMeasurable


variable {Y : Type*} [MeasurableSpace Y] [StandardBorelSpace Y] [Nonempty Y]
variable (μ : Measure D) [IsProbabilityMeasure μ] [ErgodicSMul K D μ]
  (q : D → Y) (hq : Measurable q)
  [MulAction K Y] [MeasurableConstSMul K Y]
  (hqcov : ∀ k : K, ∀ᵐ d ∂μ, q (k • d) = k • q d)
  [ErgodicVAdd Rot (D×D) (RelativeProduct.law μ q hq)]
include hq hqcov in
omit [StandardBorelSpace Y] [Nonempty Y] [ErgodicVAdd Rot (D×D) (RelativeProduct.law μ q hq)] in
include hq hqcov in
omit [StandardBorelSpace Y] [Nonempty Y] [ErgodicVAdd Rot (D×D) (RelativeProduct.law μ q hq)] in
include hq hqcov in
end PlaneFiveColor.Spectral
end

noncomputable section
open scoped ComplexConjugate
namespace PlaneFiveColor.Spectral
open EuclideanFiveColor EuclideanFiveColor.Arithmetic


end PlaneFiveColor.Spectral
end

noncomputable section
namespace PlaneFiveColor.Spectral
open EuclideanFiveColor EuclideanFiveColor.Arithmetic


/-- Arithmetic propagation: one syndetic positive mass level forces uniformly
positive mass at every sufficiently small positive algebraic radius. -/
end PlaneFiveColor.Spectral
end

noncomputable section
open MeasureTheory ProbabilityTheory Filter EuclideanFiveColor
open scoped ENNReal NNReal ComplexConjugate BoundedContinuousFunction
namespace PlaneFiveColor.Spectral
open EuclideanFiveColor.BoundedMeasurable

variable {Y : Type*} [MeasurableSpace Y] [StandardBorelSpace Y] [Nonempty Y]
variable (μ : Measure D) [IsProbabilityMeasure μ] [ErgodicSMul K D μ]
  (q : D → Y) (hq : Measurable q)
  [MulAction K Y] [MeasurableConstSMul K Y]
  (hqcov : ∀ k : K, ∀ᵐ d ∂μ, q (k • d) = k • q d)
  [ErgodicVAdd Rot (D×D) (RelativeProduct.law μ q hq)]
omit [StandardBorelSpace Y] [Nonempty Y] [ErgodicSMul K D μ]
  [MulAction K Y] [MeasurableConstSMul K Y]
  [ErgodicVAdd Rot (D×D) (RelativeProduct.law μ q hq)] in
@[simp] lemma radiusFamily_apply (r : F) (g : Rot) :
    radiusFamily μ q hq r g = massReal μ q (2*r*reF (kCoeff (rotMul g))) := rfl
include hq hqcov in
include hq hqcov in
end PlaneFiveColor.Spectral
end

noncomputable section
open MeasureTheory ProbabilityTheory Filter EuclideanFiveColor
open scoped ENNReal NNReal ComplexConjugate BoundedContinuousFunction
namespace PlaneFiveColor.Spectral
open EuclideanFiveColor.BoundedMeasurable
variable {Y : Type*} [MeasurableSpace Y] [StandardBorelSpace Y] [Nonempty Y]
variable (μ : Measure D) [IsProbabilityMeasure μ] [ErgodicSMul K D μ]
  (q : D → Y) (hq : Measurable q)
  [MulAction K Y] [MeasurableConstSMul K Y]
  (hqcov : ∀ k : K, ∀ᵐ d ∂μ, q (k • d) = k • q d)
  [ErgodicVAdd Rot (D×D) (RelativeProduct.law μ q hq)]

include hq hqcov in

include hq hqcov in
end PlaneFiveColor.Spectral
end

end OAI
