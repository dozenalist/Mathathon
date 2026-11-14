/-
Candidate: `norm_integral_sq` exists twice in the tree, with *identical statements and
identical 17-line proofs*:
  * `OAI.EuclideanFiveColor.KernelCompact.norm_integral_sq`   (lean/OAI/MeasureTheory/CompactFactors/Kernels.lean:45)
  * `OAI.EuclideanFiveColor.Multiplier.norm_integral_sq`      (lean/OAI/Analysis/PlaneSpectrum/Fourier.lean:96)
Both statements are Jensen's inequality for the convex function `z ↦ ‖z‖^2`, which is
exactly `ConvexOn.map_integral_le` (Mathlib/Analysis/Convex/Integral.lean:197) instantiated at
`convexOn_univ_norm` plus `ConvexOn.pow`.
-/
import OAI.Analysis.PlaneSpectrum.Fourier
import OAI.MeasureTheory.CompactFactors.Kernels

noncomputable section
open MeasureTheory

-- signature of the mathlib lemma we instantiate
#check @ConvexOn.map_integral_le

namespace OAI.EuclideanFiveColor.KernelCompact

/-- Replacement for `KernelCompact.norm_integral_sq`: the same statement, proved from
mathlib's Jensen inequality instead of the 17-line variance computation. -/
theorem norm_integral_sq_jensen {X : Type*} [MeasurableSpace X] (μ : Measure X)
    [IsProbabilityMeasure μ] (f : X → ℂ) (hf : Integrable f μ)
    (hf₂ : Integrable (fun x => ‖f x‖^2) μ) :
    ‖∫ x, f x ∂μ‖^2 ≤ ∫ x, ‖f x‖^2 ∂μ := by
  have hconv : ConvexOn ℝ (univ : Set ℂ) (fun z : ℂ => ‖z‖ ^ 2) :=
    (convexOn_univ_norm (E := ℂ)).pow (fun _ _ => norm_nonneg _) 2
  have hcont : ContinuousOn (fun z : ℂ => ‖z‖ ^ 2) univ :=
    (continuous_norm.pow 2).continuousOn
  have key : (fun z : ℂ => ‖z‖ ^ 2) (∫ x, f x ∂μ) ≤
      ∫ x, (fun z : ℂ => ‖z‖ ^ 2) (f x) ∂μ :=
    ConvexOn.map_integral_le (μ := μ) (s := univ) (g := fun z : ℂ => ‖z‖ ^ 2) (f := f)
      hconv hcont isClosed_univ (Eventually.of_forall fun _ => mem_univ _) hf
      (by simpa [Function.comp_def] using hf₂)
  simpa using key

end OAI.EuclideanFiveColor.KernelCompact

namespace OAI.EuclideanFiveColor.Multiplier

/-- The *same* statement as `KernelCompact.norm_integral_sq` (criterion A: provable from it
in one line, and vice versa). -/
theorem norm_integral_sq_from_kernel {X : Type*} [MeasurableSpace X] (μ : Measure X)
    [IsProbabilityMeasure μ] (f : X → ℂ) (hf : Integrable f μ)
    (hf₂ : Integrable (fun x => ‖f x‖^2) μ) :
    ‖∫ x, f x ∂μ‖^2 ≤ ∫ x, ‖f x‖^2 ∂μ :=
  OAI.EuclideanFiveColor.KernelCompact.norm_integral_sq_jensen μ f hf hf₂

/-- Replacement for `Multiplier.norm_integral_sq` (Fourier.lean:96): same statement. -/
theorem norm_integral_sq_jensen {X : Type*} [MeasurableSpace X] (μ : Measure X)
    [IsProbabilityMeasure μ] (f : X → ℂ) (hf : Integrable f μ)
    (hf₂ : Integrable (fun x => ‖f x‖^2) μ) :
    ‖∫ x, f x ∂μ‖^2 ≤ ∫ x, ‖f x‖^2 ∂μ :=
  OAI.EuclideanFiveColor.KernelCompact.norm_integral_sq_jensen μ f hf hf₂

end OAI.EuclideanFiveColor.Multiplier

#print axioms OAI.EuclideanFiveColor.KernelCompact.norm_integral_sq_jensen
#print axioms OAI.EuclideanFiveColor.Multiplier.norm_integral_sq_from_kernel
#print axioms OAI.EuclideanFiveColor.Multiplier.norm_integral_sq_jensen
