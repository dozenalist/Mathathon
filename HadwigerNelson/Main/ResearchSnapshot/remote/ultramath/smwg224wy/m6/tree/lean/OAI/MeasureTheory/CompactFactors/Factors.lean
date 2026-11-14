import OAI.MeasureTheory.CompactFactors.Functions

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
open MeasureTheory Filter
open scoped Topology ENNReal NNReal
open MeasureTheory
open scoped ENNReal
open MeasureTheory ProbabilityTheory
open scoped ENNReal
open MeasureTheory ProbabilityTheory
open MeasureTheory ProbabilityTheory
open MeasureTheory ProbabilityTheory
open scoped ENNReal
namespace EuclideanFiveColor
open MeasureTheory
structure OrbitSpace (K : Type*) where
  val : K → ℂ

namespace OrbitSpace
variable {K : Type*}
def equiv (K : Type*) : OrbitSpace K ≃ (K → ℂ) where
  toFun := val
  invFun := mk
  left_inv _ := rfl
  right_inv _ := rfl

instance : Inhabited (OrbitSpace K) := ⟨⟨fun _ => 0⟩⟩
instance : TopologicalSpace (OrbitSpace K) := (equiv K).topologicalSpace
instance : MeasurableSpace (OrbitSpace K) := borel _
instance : BorelSpace (OrbitSpace K) := ⟨rfl⟩
instance [Countable K] : PolishSpace (OrbitSpace K) := (equiv K).polishSpace_induced



instance [Monoid K] : MulAction K (OrbitSpace K) where
  smul k f := ⟨fun l => f.val (l*k)⟩
  one_smul f := by ext l; exact congrArg f.val (mul_one l)
  mul_smul a b f := by ext l; exact congrArg f.val (mul_assoc l a b).symm

@[simp] lemma smul_val [Monoid K] (k : K) (f : OrbitSpace K) (l : K) :
    (k • f).val l = f.val (l*k) := rfl

instance [Monoid K] : ContinuousConstSMul K (OrbitSpace K) where
  continuous_const_smul k := continuous_mk.comp
    (continuous_pi fun l => (continuous_apply (l*k)).comp continuous_val)
instance [Monoid K] : MeasurableConstSMul K (OrbitSpace K) where
  measurable_const_smul k := (continuous_const_smul k).measurable

end OrbitSpace

namespace OrbitFactor
variable {K X Y : Type*} [Monoid K] [MulAction K X] [MulAction K Y]
  [MeasurableSpace X] [MeasurableSpace Y]








end OrbitFactor
end EuclideanFiveColor


namespace EuclideanFiveColor.FactorCode
open MeasureTheory
variable {K X Y : Type*} [Group K] [Countable K]
  [MeasurableSpace X] [MeasurableSpace Y] [StandardBorelSpace Y]
  [MulAction K X] [MeasurableConstSMul K X]

def scalar (Y : Type*) [MeasurableSpace Y] [StandardBorelSpace Y] (y : Y) : ℂ :=
  Real.arctan (embeddingReal Y y)




lemma scalar_bound (y : Y) : ‖scalar Y y‖ ≤ 2 := by
  rw [scalar, Complex.norm_real, Real.norm_eq_abs]
  apply abs_le.mpr
  constructor
  · have := Real.neg_pi_div_two_lt_arctan (embeddingReal Y y)
    linarith [Real.pi_lt_four]
  · have := Real.arctan_lt_pi_div_two (embeddingReal Y y)
    linarith [Real.pi_lt_four]




lemma encode_bound (p : X → Y) (x : X) (k : K) : ‖(encode p x).val k‖ ≤ 2 := scalar_bound _

variable [Nonempty Y]




end EuclideanFiveColor.FactorCode

end

end OAI
