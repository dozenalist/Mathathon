import OAI.MeasureTheory.CompactFactors.AlgebraModels
import OAI.MeasureTheory.CompactFactors.Stationary

namespace OAI

noncomputable section
open MeasureTheory ProbabilityTheory Filter
open scoped ENNReal NNReal BoundedContinuousFunction
namespace PlaneFiveColor.Spectral
/-- Discrete additive notation for the actual multiplicative algebraic rotation group. -/
def Rot := Additive K deriving AddCommGroup
instance : TopologicalSpace Rot := ⊥
instance : DiscreteTopology Rot := ⟨rfl⟩
def rotMul (g : Rot) : K := Additive.toMul g
def mulRot (k : K) : Rot := Additive.ofMul k
@[simp] lemma rotMul_mulRot (k : K) : rotMul (mulRot k) = k := rfl
@[simp] lemma mulRot_rotMul (g : Rot) : mulRot (rotMul g) = g := rfl
instance rotAction (X : Type*) [MulAction K X] : AddAction Rot X where
  vadd g x := rotMul g • x
  zero_vadd x := one_smul K x
  add_vadd g h x := mul_smul (rotMul g) (rotMul h) x
@[simp] lemma rot_vadd {X : Type*} [MulAction K X] (g : Rot) (x : X) :
    g +ᵥ x = rotMul g • x := rfl
instance rotMeasurable {X : Type*} [MeasurableSpace X] [MulAction K X]
    [MeasurableConstSMul K X] : MeasurableConstVAdd Rot X where
  measurable_const_vadd g := measurable_const_smul (rotMul g)
instance rotInvariant {X : Type*} [MeasurableSpace X] [MulAction K X]
    (μ : Measure X) [SMulInvariantMeasure K X μ] : VAddInvariantMeasure Rot X μ where
  measure_preimage_vadd g s _hs := measure_preimage_smul μ (rotMul g) s
instance rotErgodic {X : Type*} [MeasurableSpace X] [MulAction K X]
    (μ : Measure X) [ErgodicSMul K X μ] : ErgodicVAdd Rot X μ where
  aeconst_of_forall_preimage_vadd_ae_eq hm he :=
    ErgodicSMul.aeconst_of_forall_preimage_smul_ae_eq hm (fun k => he (mulRot k))
lemma rot_zsmul_surjective (n : ℤ) (hn : n ≠ 0) :
    Function.Surjective (EuclideanFiveColor.BoundedMeasurable.scaleHom (G := Rot) n) := by
  intro g
  obtain ⟨k,hk⟩ := K_pow_surjective n.natAbs (Int.natAbs_ne_zero.mpr hn) (rotMul g)
  rcases n with n | n
  · refine ⟨mulRot k, ?_⟩
    change Additive.ofMul (k^n) = g
    exact congrArg mulRot hk
  · refine ⟨mulRot k⁻¹, ?_⟩
    change Additive.ofMul (k⁻¹ ^ (Int.negSucc n)) = g
    have he : k⁻¹ ^ (Int.negSucc n) = k^(n+1) := by simp
    rw [he]
    exact congrArg mulRot hk
end PlaneFiveColor.Spectral
end

noncomputable section
open MeasureTheory
namespace PlaneFiveColor.LabelModel
open Spectral
variable (k : ℕ)
abbrev Space := {ω : E → Fin k // Proper k ω}
lemma closed_proper : IsClosed {ω : E → Fin k | Proper k ω} := by
  unfold Proper
  simp only [Set.ofPred_forall]
  refine isClosed_iInter fun (x:E) => isClosed_iInter fun (y:E) => isClosed_iInter fun _ => ?_
  have hc : Continuous (fun ω : E → Fin k => (ω x,ω y)) := (continuous_apply x).prodMk (continuous_apply y)
  exact (isClosed_discrete {p : Fin k × Fin k | p.1 ≠ p.2}).preimage hc
instance : CompactSpace (Space k) := isCompact_iff_compactSpace.mp (closed_proper k).isCompact
def trans (a : E) (ω : Space k) : Space k := ⟨fun x => ω.val (x+a),by
  intro x y h
  apply ω.property (x+a) (y+a)
  change ‖(x:ℂ)+(a:ℂ)-((y:ℂ)+(a:ℂ))‖ = 1
  simpa only [add_sub_add_right_eq_sub] using h⟩
def rotate (b : K) (ω : Space k) : Space k := ⟨fun x => ω.val (kCoeff b * x),by
  intro x y h
  apply ω.property (kCoeff b*x) (kCoeff b*y)
  change ‖(b.val:ℂ)*(x:ℂ)-(b.val:ℂ)*(y:ℂ)‖ = 1
  rw [← mul_sub,norm_mul,Circle.norm_coe,one_mul,h]⟩
@[simp] lemma trans_apply (a : E) (ω : Space k) (x : E) : (trans k a ω).val x = ω.val (x+a) := rfl
@[simp] lemma rotate_apply (b : K) (ω : Space k) (x : E) : (rotate k b ω).val x = ω.val (kCoeff b*x) := rfl
@[simp] lemma trans_zero (ω : Space k) : trans k 0 ω = ω := by apply Subtype.ext; funext x; simp
@[simp] lemma rotate_one (ω : Space k) : rotate k 1 ω = ω := by
  apply Subtype.ext
  funext x
  have h1 : kCoeff 1 = 1 := rfl
  simp [h1]
lemma covariance (a : E) (b : K) (ω : Space k) : trans k a (rotate k b ω) = rotate k b (trans k (kCoeff b*a) ω) := by
  apply Subtype.ext
  funext x
  simp only [trans_apply,rotate_apply,mul_add]
def tr (a : Trans) : Space k → Space k := trans k (Multiplicative.toAdd (Additive.toMul a))
def ro (b : Rot) : Space k → Space k := rotate k (rotMul b)
def measure (ω : Space k) : Measure (Space k) := EuclideanFiveColor.StationaryMean.measure (tr k) (ro k) ω
instance (ω : Space k) : IsProbabilityMeasure (measure k ω) := inferInstanceAs (IsProbabilityMeasure (EuclideanFiveColor.StationaryMean.measure (tr k) (ro k) ω))
end PlaneFiveColor.LabelModel
end

noncomputable section
open MeasureTheory
open scoped ENNReal NNReal
namespace EuclideanFiveColor.Koopman
variable {X : Type*} [MeasurableSpace X] (μ : Measure X)
def isometry (s : X ≃ᵐ X) (hs : MeasurePreserving s μ μ) : Lp ℂ 2 μ ≃ₗᵢ[ℂ] Lp ℂ 2 μ where
  __ := Lp.compMeasurePreservingₗᵢ ℂ s hs
  invFun := Lp.compMeasurePreserving s.symm (hs.symm s)
  left_inv v := by
    change Lp.compMeasurePreserving s.symm (hs.symm s) (Lp.compMeasurePreserving s hs v) = v
    rw [← Lp.compMeasurePreserving_comp_apply]
    have he : (s : X → X) ∘ s.symm = id := funext s.apply_symm_apply
    simp only [he,Lp.compMeasurePreserving_id_apply]
  right_inv v := by
    change Lp.compMeasurePreserving s hs (Lp.compMeasurePreserving s.symm (hs.symm s) v) = v
    rw [← Lp.compMeasurePreserving_comp_apply]
    have he : (s.symm : X → X) ∘ s = id := funext s.symm_apply_apply
    simp only [he,Lp.compMeasurePreserving_id_apply]
def unitary (s : X ≃ᵐ X) (hs : MeasurePreserving s μ μ) : unitary (Lp ℂ 2 μ →L[ℂ] Lp ℂ 2 μ) :=
  Unitary.linearIsometryEquiv.symm (isometry μ s hs)
end EuclideanFiveColor.Koopman
end

noncomputable section
open Filter Topology
namespace EuclideanFiveColor.ContinuousVectors
variable {A H : Type*} [AddCommGroup A]
  [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
  (U : Multiplicative A →* unitary (H →L[ℂ] H))
def op (a : A) : H →L[ℂ] H := U (Multiplicative.ofAdd a)
@[simp] lemma op_zero (v : H) : op U 0 v = v := by simp [op]
variable [TopologicalSpace A]
def space : Submodule ℂ H where
  carrier := {v | Tendsto (fun a => op U a v) (𝓝 0) (𝓝 v)}
  zero_mem' := by simp
  add_mem' := by
    intro v w hv hw
    change Tendsto (fun a => op U a (v+w)) (𝓝 0) (𝓝 (v+w))
    simpa only [map_add] using hv.add hw
  smul_mem' := by
    intro c v hv
    change Tendsto (fun a => op U a (c • v)) (𝓝 0) (𝓝 (c • v))
    simpa only [map_smul] using hv.const_smul c
lemma isClosed_space : IsClosed (space U : Set H) := by
  apply isClosed_of_closure_subset
  intro v hv
  apply Metric.tendsto_nhds.mpr
  intro ε hε
  obtain ⟨w,hw,hd⟩ := Metric.mem_closure_iff.mp hv (ε/4) (by positivity)
  have ht := Metric.tendsto_nhds.mp hw (ε/2) (by positivity)
  filter_upwards [ht] with a ha
  have he : dist (op U a v) v ≤ 2 * dist v w + dist (op U a w) w := by
    calc
      _ ≤ dist (op U a v) (op U a w) + dist (op U a w) v := dist_triangle _ _ _
      _ ≤ dist (op U a v) (op U a w) + (dist (op U a w) w + dist w v) :=
        by linarith [dist_triangle (op U a w) w v]
      _ = _ := by rw [dist_op,dist_comm w v]; ring
  linarith
instance : CompleteSpace (space U) := (isClosed_space U).completeSpace_coe
variable [IsTopologicalAddGroup A]
end EuclideanFiveColor.ContinuousVectors
end

noncomputable section
open MeasureTheory
namespace PlaneFiveColor.LabelModel
open Spectral EuclideanFiveColor EuclideanFiveColor.ContinuousVectors
variable (k : ℕ) (ω : Space k)
abbrev Hilbert := Lp ℂ 2 (measure k ω)
def translation (a : E) : unitary (Hilbert k ω →L[ℂ] Hilbert k ω) :=
  Koopman.unitary (measure k ω) (transHomeo k a).toMeasurableEquiv (trans_preserving k ω a)
def rotation (b : K) : unitary (Hilbert k ω →L[ℂ] Hilbert k ω) :=
  Koopman.unitary (measure k ω) (rotateHomeo k b).toMeasurableEquiv (rotate_preserving k ω b)
def representation : DiscreteE →* unitary (Hilbert k ω →L[ℂ] Hilbert k ω) where
  toFun a := translation k ω (Multiplicative.toAdd a)
  map_one' := by
    apply Subtype.ext
    apply ContinuousLinearMap.ext
    intro v
    change Lp.compMeasurePreserving (trans k 0) (trans_preserving k ω 0) v = v
    have he : trans k 0 = id := funext (trans_zero k)
    simp only [he,Lp.compMeasurePreserving_id_apply]
  map_mul' a b := by
    apply Subtype.ext
    apply ContinuousLinearMap.ext
    intro v
    change Lp.compMeasurePreserving (trans k (Multiplicative.toAdd a+Multiplicative.toAdd b)) _ v =
      Lp.compMeasurePreserving (trans k (Multiplicative.toAdd a)) _ (Lp.compMeasurePreserving (trans k (Multiplicative.toAdd b)) _ v)
    rw [← Lp.compMeasurePreserving_comp_apply]
    congr 2
    funext x
    exact (congrArg (fun c => trans k c x) (add_comm _ _)).trans (trans_add k _ _ x).symm
end PlaneFiveColor.LabelModel
end

noncomputable section
open scoped InnerProductSpace
namespace EuclideanFiveColor
variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
end EuclideanFiveColor
end

noncomputable section
open MeasureTheory Filter Topology
open scoped ENNReal NNReal
namespace EuclideanFiveColor.ContinuousVectors
variable {A X : Type*} [AddCommGroup A] [TopologicalSpace A] [MeasurableSpace X]
  (μ : Measure X) (U : Multiplicative A →* unitary (Lp ℂ 2 μ →L[ℂ] Lp ℂ 2 μ))
  (s : A → X → X) (hs : ∀ a, MeasurePreserving (s a) μ μ)
  (hU : ∀ a v, op U a v = Lp.compMeasurePreserving (s a) (hs a) v)
include hU
omit hU
def clamp (z : ℂ) : ℂ := (max 0 (min 1 z.re) : ℝ)
@[simp] lemma clamp_zero : clamp 0 = 0 := by simp [clamp]
include hU
end EuclideanFiveColor.ContinuousVectors
end

noncomputable section
open Filter Topology
open scoped InnerProductSpace
namespace EuclideanFiveColor.ContinuousVectors
variable {A H : Type*} [AddCommGroup A] [TopologicalSpace A]
  [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
  (U : Multiplicative A →* unitary (H →L[ℂ] H))
end EuclideanFiveColor.ContinuousVectors
end

noncomputable section
open MeasureTheory
open scoped ComplexConjugate InnerProductSpace
namespace EuclideanFiveColor.VectorMeasure
variable {X H : Type*} [TopologicalSpace X]
  [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
  (Φ : C(X,ℂ) →⋆ₐ[ℂ] (H →L[ℂ] H)) (v : H)
def realCM (f : C(X,ℝ)) : C(X,ℂ) := ⟨fun x => (f x : ℂ),by fun_prop⟩
@[simp] lemma realCM_apply (f : C(X,ℝ)) (x : X) : realCM f x = (f x : ℂ) := rfl
@[simp] lemma realCM_add (f g : C(X,ℝ)) : realCM (f+g) = realCM f+realCM g := by ext; simp
@[simp] lemma realCM_sub (f g : C(X,ℝ)) : realCM (f-g) = realCM f-realCM g := by ext; simp
@[simp] lemma realCM_smul (c : ℝ) (f : C(X,ℝ)) : realCM (c • f) = (c:ℂ) • realCM f := by ext; simp
@[simp] lemma realCM_one : realCM (1:C(X,ℝ)) = 1 := by ext; simp
variable [CompactSpace X] [T2Space X] [MeasurableSpace X] [BorelSpace X]
omit [CompactSpace X] [T2Space X] [MeasurableSpace X] [BorelSpace X] in

def functional : CompactlySupportedContinuousMap X ℝ →ₚ[ℝ] ℝ where
  toFun f := (⟪v,Φ (realCM f.toContinuousMap) v⟫_ℂ).re
  map_add' f g := by
    change (⟪v,Φ (realCM (f.toContinuousMap+g.toContinuousMap)) v⟫_ℂ).re = _
    simp
  map_smul' c f := by
    change (⟪v,Φ (realCM (c • f.toContinuousMap)) v⟫_ℂ).re = c * _
    rw [realCM_smul,map_smul]
    simp only [FunLike.coe_smul,Pi.smul_apply,inner_smul_right,Complex.mul_re,Complex.ofReal_re,Complex.ofReal_im,zero_mul,sub_zero]
  monotone' f g hfg := by
    have he := real_nonneg Φ v (g.toContinuousMap-f.toContinuousMap) (sub_nonneg.mpr hfg)
    simpa [inner_sub_right] using he

def measure : Measure X := RealRMK.rieszMeasure (functional Φ v)
instance : IsFiniteMeasure (measure Φ v) := by dsimp [measure]; infer_instance
instance : (measure Φ v).Regular := by dsimp [measure]; infer_instance
lemma measure_univ : (measure Φ v).real Set.univ = ‖v‖^2 := by
  have he := integral_real Φ v (1:C(X,ℝ))
  simp only [ContinuousMap.one_apply,integral_const,smul_eq_mul,mul_one,realCM_one,map_one,one_apply_eq_self] at he
  exact he.trans (inner_self_eq_norm_sq (𝕜 := ℂ) v)
end EuclideanFiveColor.VectorMeasure
end

end OAI
