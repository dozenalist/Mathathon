import OAI.Analysis.PlaneSpectrum.FourierTests
import OAI.Analysis.PlaneSpectrum.SmallArcs
import OAI.MeasureTheory.CompactFactors.ConditionalSelection

namespace OAI

noncomputable section

open scoped ComplexConjugate
open scoped BigOperators
open scoped BigOperators BoundedContinuousFunction
open Filter Topology
open MeasureTheory Filter
open scoped ENNReal ComplexConjugate
open MeasureTheory ProbabilityTheory
open scoped ComplexConjugate
open scoped BigOperators
open scoped BigOperators
open Polynomial
open MeasureTheory
open scoped BigOperators
open MeasureTheory
open scoped BigOperators
open MeasureTheory
open MeasureTheory ProbabilityTheory
open scoped BigOperators
open MeasureTheory
open scoped BigOperators ComplexConjugate
open MeasureTheory ProbabilityTheory
open scoped ENNReal BigOperators
namespace PlaneFiveColor.Spectral

section
open MeasureTheory ProbabilityTheory
open EuclideanFiveColor
open scoped BigOperators ComplexConjugate

instance dualPolishSpace : PolishSpace D := by
  have : TopologicalSpace.SeparableSpace (DiscreteE → Circle) := inferInstance
  have : TopologicalSpace.IsCompletelyMetrizableSpace (DiscreteE → Circle) := inferInstance
  exact ContinuousMonoidHom.isClosedEmbedding_coe.polishSpace

local instance : MeasurableSpace Circle := borel Circle
local instance : BorelSpace Circle := ⟨rfl⟩

/-- Evaluation at the exact algebraic argument. -/
def eval (a : E) : D →* Circle where
  toFun d := d (Multiplicative.ofAdd a)
  map_one' := rfl
  map_mul' _ _ := rfl

lemma continuous_eval (a : E) : Continuous (eval a) :=
  (continuous_apply (Multiplicative.ofAdd a)).comp
    ContinuousMonoidHom.isClosedEmbedding_coe.continuous

lemma measurable_eval_coe (a : E) : Measurable (fun d => (eval a d : ℂ)) :=
  ((show Continuous (fun z : Circle => (z : ℂ)) from continuous_subtype_val).comp
    (continuous_eval a)).measurable

@[simp] lemma eval_zero (d : D) : eval 0 d = 1 := map_one d
lemma eval_add (a b : E) (d : D) : eval (a+b) d = eval a d * eval b d :=
  map_mul d (Multiplicative.ofAdd a) (Multiplicative.ofAdd b)
lemma eval_scalar (a b : E) (d : D) : eval a (scalar b d) = eval (b*a) d := rfl
lemma lineFourier_eq (ν : Measure D) (a : E) (t : F) :
    lineFourier ν a t = ∫ d, (eval (a * ofF t) d : ℂ) ∂ν := rfl

variable {X W : Type*} [MeasurableSpace X] [StandardBorelSpace X] [Nonempty X]
  [MeasurableSpace W]



end


end PlaneFiveColor.Spectral

namespace EuclideanFiveColor.PhaseEncoding
open MeasureTheory ProbabilityTheory
variable {Y G : Type*} [MeasurableSpace Y] [MeasurableSpace G]
/-- Covariance of the *actual* Newton-symmetric conditional encoding. -/
theorem kernelEncoding_covariance (ν : Measure Y) (β : Kernel Y G)
    (R : Y → Y) (T : G → G) (hT : Measurable T)
    (χ : G → ℂ) (hχ : Measurable χ) (m : ℕ)
    (hβ : ∀ᵐ y ∂ν, β (R y) = (β y).map T) :
    ∀ᵐ y ∂ν, kernelEncoding β χ m (R y) = kernelEncoding β (χ ∘ T) m y := by
  filter_upwards [hβ] with y hy
  have he (n : ℕ) : (∫ d, χ d ^ n ∂β (R y)) = ∫ d, χ (T d)^n ∂β y := by
    rw [hy, integral_map hT.aemeasurable (hχ.pow_const n).aestronglyMeasurable]
  funext i
  simp only [kernelEncoding, he, Function.comp_def]
end EuclideanFiveColor.PhaseEncoding


end

end OAI
