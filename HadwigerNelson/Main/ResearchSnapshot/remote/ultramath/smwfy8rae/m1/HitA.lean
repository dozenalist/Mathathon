/-
  Hit-A witness for swarm smwfy8rae / m1.

  The two declarations
    OAI.EuclideanFiveColor.ProbabilityL2.norm_integral_sq   (lean/OAI/Analysis/PlaneSpectrum/Fourier.lean:96)
    OAI.EuclideanFiveColor.KernelCompact.norm_integral_sq   (lean/OAI/MeasureTheory/CompactFactors/Kernels.lean:45)
  have the same statement up to namespace and a *verbatim* 17-line proof.
  Below: each is derived from the other in one line, and the axioms of the
  resulting declarations are printed.
-/
import OAI.Analysis.PlaneSpectrum.Fourier
import OAI.MeasureTheory.CompactFactors.Kernels

open MeasureTheory

namespace HitA

/-- The `KernelCompact` statement, obtained from the `ProbabilityL2` copy in one line. -/
theorem norm_integral_sq_from_probabilityL2 {X : Type*} [MeasurableSpace X]
    (μ : Measure X) [IsProbabilityMeasure μ] (f : X → ℂ) (hf : Integrable f μ)
    (hf₂ : Integrable (fun x => ‖f x‖ ^ 2) μ) :
    ‖∫ x, f x ∂μ‖ ^ 2 ≤ ∫ x, ‖f x‖ ^ 2 ∂μ :=
  OAI.EuclideanFiveColor.ProbabilityL2.norm_integral_sq μ f hf hf₂

/-- The `ProbabilityL2` statement, obtained from the `KernelCompact` copy in one line. -/
theorem norm_integral_sq_from_kernelCompact {X : Type*} [MeasurableSpace X]
    (μ : Measure X) [IsProbabilityMeasure μ] (f : X → ℂ) (hf : Integrable f μ)
    (hf₂ : Integrable (fun x => ‖f x‖ ^ 2) μ) :
    ‖∫ x, f x ∂μ‖ ^ 2 ≤ ∫ x, ‖f x‖ ^ 2 ∂μ :=
  OAI.EuclideanFiveColor.KernelCompact.norm_integral_sq μ f hf hf₂

#print axioms norm_integral_sq_from_probabilityL2
#print axioms norm_integral_sq_from_kernelCompact

end HitA
