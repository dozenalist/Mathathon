import OAI.Analysis.PlaneSpectrum.Ergodicity
import OAI.Geometry.PlaneColoring.Coloring

namespace OAI

noncomputable section
open MeasureTheory Filter Topology
open scoped ENNReal NNReal InnerProductSpace
namespace PlaneFiveColor.LabelModel
open Spectral EuclideanFiveColor EuclideanFiveColor.ContinuousVectors
variable (k : ℕ) (ω : Space k)
def colorValue (i : Fin k) (η : Space k) : ℂ := if η.val 0 = i then 1 else 0
lemma color_memLp (i : Fin k) : MemLp (colorValue k i) 2 (measure k ω) := by
  refine MemLp.of_bound ?_ 1 ?_
  · apply Measurable.aestronglyMeasurable
    apply Measurable.ite _ measurable_const measurable_const
    exact (measurableSet_singleton i).preimage (show Measurable (fun η : Space k => η.val 0) from
      ((continuous_apply (0 : E)).comp continuous_subtype_val).measurable)
  · exact .of_forall fun η => by dsimp [colorValue]; split_ifs <;> simp
abbrev colorVector (i : Fin k) : Hilbert k ω := (color_memLp k ω i).toLp (colorValue k i)
lemma color_ae (i : Fin k) : colorVector k ω i =ᵐ[measure k ω] colorValue k i := (color_memLp k ω i).coeFn_toLp
lemma color_rotation_fixed (i : Fin k) (b : K) :
    (rotation k ω b : Hilbert k ω →L[ℂ] Hilbert k ω) (colorVector k ω i) = colorVector k ω i := by
  rw [rotation_apply]
  apply Lp.ext
  filter_upwards [Lp.coeFn_compMeasurePreserving (colorVector k ω i) (rotate_preserving k ω b),
    (rotate_preserving k ω b).quasiMeasurePreserving.ae (color_ae k ω i),color_ae k ω i] with η h1 h2 h3
  simp only [Function.comp_apply,h1,h2,h3,colorValue,rotate_apply,mul_zero]
lemma color_unit_correlation (i : Fin k) (b : K) :
    ⟪colorVector k ω i,op (representation k ω) (kCoeff b) (colorVector k ω i)⟫_ℂ = 0 := by
  rw [op_apply,L2.inner_def]
  apply integral_eq_zero_of_ae
  filter_upwards [color_ae k ω i,Lp.coeFn_compMeasurePreserving (colorVector k ω i) (trans_preserving k ω (kCoeff b)),
    (trans_preserving k ω (kCoeff b)).quasiMeasurePreserving.ae (color_ae k ω i)] with η h1 h2 h3
  simp only [h1,h2,Function.comp_apply,h3,colorValue,trans_apply,zero_add]
  have hp : η.val 0 ≠ η.val (kCoeff b) := η.property 0 (kCoeff b) (by
    change ‖(0 : ℂ)-(b.val:ℂ)‖ = 1
    rw [zero_sub,norm_neg]
    exact Circle.norm_coe b.val)
  by_cases hi : η.val 0 = i
  · have hj : η.val (kCoeff b) ≠ i := fun h => hp (hi.trans h.symm)
    simp [hi,hj]
  · simp [hi]
instance continuous_complete : CompleteSpace (space (A := E) (representation k ω)) :=
  (isClosed_space (A := E) (representation k ω)).completeSpace_coe
def projected (i : Fin k) : Hilbert k ω := (space (A := E) (representation k ω)).starProjection (colorVector k ω i)
lemma projected_range (i : Fin k) : ∀ᵐ η ∂measure k ω,
    ((projected k ω i) η).im = 0 ∧ 0 ≤ ((projected k ω i) η).re ∧ ((projected k ω i) η).re ≤ 1 := by
  apply projection_range (measure k ω) (representation k ω) (trans k) (trans_preserving k ω) (op_apply k ω)
  filter_upwards [color_ae k ω i] with η h
  rw [h]
  dsimp [colorValue]
  split_ifs <;> norm_num
lemma projected_rotation_fixed (i : Fin k) (b : K) :
    (rotation k ω b : Hilbert k ω →L[ℂ] Hilbert k ω) (projected k ω i) = projected k ω i := by
  exact projection_covariance_fixed (representation k ω) (rotation k ω b)
    (Homeomorph.mulLeft₀ (kCoeff b) (kCoeff_ne_zero b)) (mul_zero _)
    (rotation_covariance k ω b) _ (color_rotation_fixed k ω i b)
lemma projected_unit_correlation (i : Fin k) (b : K) :
    ⟪projected k ω i,op (representation k ω) (kCoeff b) (projected k ω i)⟫_ℂ = 0 := by
  have hb := residual_fourier (representation k ω) (rotation k ω) (rotation_covariance k ω)
    (colorVector k ω i-projected k ω i)
    ((space (A := E) (representation k ω)).sub_starProjection_mem_orthogonal (colorVector k ω i))
    (fun b => by rw [map_sub,color_rotation_fixed,projected_rotation_fixed]) (kCoeff b) (kCoeff_ne_zero b)
  exact (projection_coefficient (representation k ω) (colorVector k ω i) (kCoeff b) hb).trans (color_unit_correlation k ω i b)
end PlaneFiveColor.LabelModel
end

noncomputable section
open MeasureTheory Filter Topology
namespace PlaneFiveColor.LabelModel
open Spectral EuclideanFiveColor EuclideanFiveColor.ContinuousVectors
variable (k : ℕ) (ω : Space k)
end PlaneFiveColor.LabelModel
end

noncomputable section
open Filter Topology
open scoped ComplexConjugate
namespace PlaneFiveColor.Spectral
end PlaneFiveColor.Spectral
end

noncomputable section
open Filter Topology
open scoped InnerProductSpace
namespace PlaneFiveColor.Spectral
open EuclideanFiveColor.ContinuousVectors
variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
  (U : DiscreteE →* unitary (H →L[ℂ] H))
end PlaneFiveColor.Spectral
end

noncomputable section
open Filter Topology
namespace PlaneFiveColor.Spectral
end PlaneFiveColor.Spectral
end

noncomputable section
open MeasureTheory Filter Topology
open scoped InnerProductSpace
namespace PlaneFiveColor.LabelModel
open Spectral EuclideanFiveColor EuclideanFiveColor.ContinuousVectors
variable (k : ℕ) (ω : Space k)
end PlaneFiveColor.LabelModel
end

noncomputable section
open MeasureTheory Filter Topology TopologicalSpace
open scoped ENNReal
namespace EuclideanFiveColor
variable {T X : Type*} [TopologicalSpace T] [SeparableSpace T] [Nonempty T]
  [MeasurableSpace T] [BorelSpace T] [MeasurableSpace X] (μ : Measure X)
  (f : T → Lp ℂ 2 μ) (hf : Continuous f)
include hf
omit [MeasurableSpace T] [BorelSpace T] in
omit [MeasurableSpace T] [BorelSpace T] in
omit [MeasurableSpace T] [BorelSpace T] in
end EuclideanFiveColor
end

noncomputable section
open MeasureTheory
open scoped InnerProductSpace ComplexConjugate
namespace EuclideanFiveColor
variable {X : Type*} [MeasurableSpace X] (μ : Measure X)
end EuclideanFiveColor
end

noncomputable section
open MeasureTheory Filter Topology
namespace PlaneFiveColor.LabelModel
open Spectral EuclideanFiveColor EuclideanFiveColor.ContinuousVectors
variable (k : ℕ) (ω : Space k)
end PlaneFiveColor.LabelModel
end

noncomputable section
open MeasureTheory
namespace EuclideanFiveColor
variable {X : Type*} [MeasurableSpace X] {k : ℕ} [NeZero k]
omit [NeZero k] in
private def pickSupport (s : Finset (Fin k)) : Fin k := if h : s.Nonempty then h.choose else 0
omit [MeasurableSpace X] in
end EuclideanFiveColor
end

noncomputable section
open MeasureTheory Filter
namespace EuclideanFiveColor
variable {Ω S : Type*} [MeasurableSpace Ω] [MeasurableSpace S]
  (μ : Measure Ω) [IsProbabilityMeasure μ] (ν : Measure S) [SFinite ν]
  (d : S → ℂ) (hd : Measurable d) {k : ℕ} [NeZero k]
include hd
end EuclideanFiveColor
end

noncomputable section
open MeasureTheory
namespace EuclideanFiveColor
end EuclideanFiveColor
end

end OAI
