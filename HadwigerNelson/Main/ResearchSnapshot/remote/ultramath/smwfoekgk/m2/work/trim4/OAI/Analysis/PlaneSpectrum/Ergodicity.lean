import OAI.Analysis.PlaneSpectrum.RadialEnergy
import OAI.Analysis.PlaneSpectrum.SpectralMeasure

namespace OAI

noncomputable section
open MeasureTheory ProbabilityTheory Filter EuclideanFiveColor
open scoped ENNReal NNReal ComplexConjugate BoundedContinuousFunction
namespace PlaneFiveColor.Spectral
open EuclideanFiveColor.BoundedMeasurable

def normF (z : E) : F := ⟨‖(z:ℂ)‖,mem_algebraicClosure_iff.mpr (by
  apply IsAlgebraic.of_pow (n := 2) (by decide)
  rw [← Complex.normSq_eq_norm_sq,Complex.normSq_apply]
  have hr := mem_algebraicClosure_iff.mp (reF z).property
  have hi := mem_algebraicClosure_iff.mp (imF z).property
  exact (hr.mul hr).add (hi.mul hi))⟩
@[simp] lemma normF_coe (z : E) : ((normF z : F):ℝ) = ‖(z:ℂ)‖ := rfl
lemma normF_pos {z : E} (hz : z ≠ 0) : 0 < normF z := by
  change 0 < ‖(z:ℂ)‖
  exact norm_pos_iff.mpr (fun h => hz (Subtype.ext h))

variable {Y : Type*} [MeasurableSpace Y] [StandardBorelSpace Y] [Nonempty Y]
variable (μ : Measure D) [IsProbabilityMeasure μ] [ErgodicSMul K D μ]
  (q : D → Y) (hq : Measurable q)
  [MulAction K Y] [MeasurableConstSMul K Y]
  (hqcov : ∀ k : K, ∀ᵐ d ∂μ, q (k • d) = k • q d)
  [ErgodicVAdd Rot (D×D) (RelativeProduct.law μ q hq)]
include hq hqcov in
lemma projectedMass_vanish (hw : IsWild (DifferenceFourier.differenceLaw (μ.map q) (condDistrib id q μ)))
    (z : E) (hz : z ≠ 0) : projectedMass μ q z = 0 := by
  have hn : ‖(z:ℂ)‖ = ‖((ofF (normF z):E):ℂ)‖ := by
    rw [norm_ofF,normF_coe,abs_of_nonneg (norm_nonneg _)]
  rw [projectedMass_radial μ q hq hqcov hn]
  exact massReal_vanish μ q hq hqcov hw (normF z) (normF_pos hz)
include hq hqcov in
lemma fourier_vanish_of_terminal (hw : IsWild (DifferenceFourier.differenceLaw (μ.map q) (condDistrib id q μ)))
    (z : E) (hz : z ≠ 0) : ∫ d, (eval z d : ℂ) ∂μ = 0 := by
  have hn : ‖l2 μ (project μ q hq (char z))‖ = 0 := by
    rw [norm_project_l2]
    have he := projectedMass_vanish μ q hq hqcov hw z hz
    change ‖l2 (μ.map q) (conditional μ q (char z))‖^2 = 0 at he
    nlinarith [norm_nonneg (l2 (μ.map q) (conditional μ q (char z)))]
  have he : project μ q hq (char z) =ᵐ[μ] (0:Func D) :=
    (l2_eq_iff μ _ _).mp (by rw [map_zero]; exact norm_eq_zero.mp hn)
  change (∫ d, char z d ∂μ) = 0
  rw [← project_integral μ q hq]
  calc
    _ = ∫ d, (0:Func D) d ∂μ := integral_congr_ae he
    _ = 0 := by simp

lemma ergodic_wild_fourier (μ : Measure D) [IsProbabilityMeasure μ] [ErgodicSMul K D μ]
    (hw : IsWild μ) (z : E) (hz : z ≠ 0) : ∫ d, (eval z d : ℂ) ∂μ = 0 := by
  obtain ⟨q,hq,hqc,hgood,hmix⟩ := exists_terminal_factor μ
  have := hmix
  have hd : IsWild (DifferenceFourier.differenceLaw (μ.map q) (condDistrib id q μ)) := by
    refine ⟨relative_difference_invariant μ id q measurable_id hq (fun k => Eventually.of_forall (fun d => rfl)) hqc,?_⟩
    exact hgood id measurable_id (fun k => Eventually.of_forall (fun d => rfl)) (by simpa using hw)
  exact fourier_vanish_of_terminal μ q hq hqc hd z hz
end PlaneFiveColor.Spectral
end

noncomputable section
open MeasureTheory Filter Topology
open scoped BoundedContinuousFunction RealInnerProductSpace
namespace EuclideanFiveColor.Amenable.Mean
variable {G H : Type*} [AddCommGroup G] [TopologicalSpace G] [DiscreteTopology G]
  [NormedAddCommGroup H] [InnerProductSpace ℝ H] [CompleteSpace H]
end EuclideanFiveColor.Amenable.Mean
namespace EuclideanFiveColor
structure ConvexAverage (G : Type*) where
  n : ℕ
  pt : Fin n → G
  weight : Fin n → ℝ
  nonneg : ∀ i, 0 ≤ weight i
  total : ∑ i, weight i = 1
namespace ConvexAverage
variable {G H : Type*}
variable [NormedAddCommGroup H] [NormedSpace ℝ H]
def apply (A : ConvexAverage G) (f : G → H) : H := ∑ i, A.weight i • f (A.pt i)
end ConvexAverage
namespace Amenable.Mean
variable {G H : Type*} [AddCommGroup G] [TopologicalSpace G] [DiscreteTopology G]
  [NormedAddCommGroup H] [InnerProductSpace ℝ H] [CompleteSpace H]
end Amenable.Mean
end EuclideanFiveColor
end

noncomputable section
open MeasureTheory Filter Topology
open scoped BoundedContinuousFunction RealInnerProductSpace
namespace EuclideanFiveColor
namespace ConvexAverage
open BoundedMeasurable
variable {G X : Type*} [AddCommGroup G] [MeasurableSpace X]
  [AddAction G X] [MeasurableConstVAdd G X]
variable (μ : Measure X) [IsProbabilityMeasure μ] [VAddInvariantMeasure G X μ]
end ConvexAverage
namespace InvariantSequence
open BoundedMeasurable
variable {G X : Type*} [AddCommGroup G] [TopologicalSpace G] [DiscreteTopology G]
  [MeasurableSpace X] [AddAction G X] [MeasurableConstVAdd G X]
  (μ : Measure X) [IsProbabilityMeasure μ] [VAddInvariantMeasure G X μ]
  (M : Amenable.Mean G)
def limit (f : Func X) : Lp ℂ 2 μ := M.vector (Amenable.Mean.orbit (Amenable.Koopman.action μ) (l2 μ f))
end InvariantSequence
end EuclideanFiveColor
end

noncomputable section
open MeasureTheory ProbabilityTheory Filter Topology
namespace EuclideanFiveColor
open BoundedMeasurable
namespace ConvexAverage
variable {G X : Type*} [AddCommGroup G] [MeasurableSpace X]
  [AddAction G X] [MeasurableConstVAdd G X]
  (μ : Measure X) [IsProbabilityMeasure μ] [VAddInvariantMeasure G X μ]
end ConvexAverage
namespace ErgodicCriterion
variable (X : Type*) [MeasurableSpace X] [MeasurableSpace.CountablyGenerated X]
def test (s : Finset ℕ) : Func X :=
  ⟨(testSet X s).indicator (fun _ => 1),(measurable_const.indicator (measurable_testSet X s)),1,
    fun x => by by_cases hx : x ∈ testSet X s <;> simp [hx]⟩
variable {X}
variable {G : Type*} [AddCommGroup G] [AddAction G X] [MeasurableConstVAdd G X]
  (μ : Measure X) [IsProbabilityMeasure μ] [VAddInvariantMeasure G X μ]
end ErgodicCriterion
end EuclideanFiveColor
end

noncomputable section
open MeasureTheory ProbabilityTheory Filter Topology
namespace EuclideanFiveColor.InvariantDecomposition
open BoundedMeasurable ErgodicCriterion
variable {G X : Type*} [AddCommGroup G] [Countable G] [TopologicalSpace G] [DiscreteTopology G]
  [MeasurableSpace X] [StandardBorelSpace X] [Nonempty X]
  [AddAction G X] [MeasurableConstVAdd G X]
  (μ : Measure X) [IsProbabilityMeasure μ] [VAddInvariantMeasure G X μ]
  (M : Amenable.Mean G)
omit [Countable G] [Nonempty X] in
omit [Countable G] [Nonempty X] in
end EuclideanFiveColor.InvariantDecomposition
end

noncomputable section
open MeasureTheory ProbabilityTheory Filter
open EuclideanFiveColor
namespace PlaneFiveColor.Spectral
instance : Countable Rot := inferInstanceAs (Countable K)
/-- The arbitrary invariant wild case, obtained from actual conditional ergodic fibers. -/
end PlaneFiveColor.Spectral
end

noncomputable section
open MeasureTheory
open scoped ENNReal NNReal InnerProductSpace
namespace PlaneFiveColor.Spectral
open EuclideanFiveColor EuclideanFiveColor.VectorMeasure EuclideanFiveColor.CommutingSpectral
variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
  (U : DiscreteE →* unitary (H →L[ℂ] H)) (W : K → unitary (H →L[ℂ] H))
  (hcov : ∀ k z w, (W k : H →L[ℂ] H) (ContinuousVectors.op U z w) =
    ContinuousVectors.op U ((kCoeff k)*z) ((W k : H →L[ℂ] H) w))
include hcov
end PlaneFiveColor.Spectral
end

end OAI
