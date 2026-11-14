import Mathlib
namespace OAI

noncomputable section
open MeasureTheory Filter Topology FourierTransform
namespace EuclideanFiveColor
namespace Multiplier
variable {X : Type*} [MeasurableSpace X] (μ : Measure X)
def apply (f : X → ℂ) (hf : AEStronglyMeasurable f μ) {C : ℝ} (hbound : ∀ᵐ x ∂μ, ‖f x‖≤C)
    (g : Lp ℂ 2 μ) : Lp ℂ 2 μ :=
  ((memLp_top_of_bound hf C hbound).fun_mul (Lp.memLp g)).toLp (fun x => f x*g x)
lemma apply_ae (f : X → ℂ) (hf : AEStronglyMeasurable f μ) {C : ℝ} (hbound : ∀ᵐ x ∂μ, ‖f x‖≤C)
    (g : Lp ℂ 2 μ) : apply μ f hf hbound g =ᵐ[μ] fun x => f x*g x := MemLp.coeFn_toLp _
def linear (f : X → ℂ) (hf : AEStronglyMeasurable f μ) {C : ℝ} (hbound : ∀ᵐ x ∂μ, ‖f x‖≤C) :
    Lp ℂ 2 μ →ₗ[ℂ] Lp ℂ 2 μ where
  toFun := apply μ f hf hbound
  map_add' g h := by
    apply Lp.ext
    filter_upwards [apply_ae μ f hf hbound (g+h),apply_ae μ f hf hbound g,apply_ae μ f hf hbound h,
      Lp.coeFn_add g h,Lp.coeFn_add (apply μ f hf hbound g) (apply μ f hf hbound h)] with x ha hb hc hd he
    simp only [ha,he,Pi.add_apply,hb,hc,hd,mul_add]
  map_smul' c g := by
    apply Lp.ext
    filter_upwards [apply_ae μ f hf hbound (c • g),apply_ae μ f hf hbound g,
      Lp.coeFn_smul c g,Lp.coeFn_smul c (apply μ f hf hbound g)] with x ha hb hc hd
    simp only [RingHom.id_apply,ha,hd,Pi.smul_apply,hb,hc,smul_eq_mul]
    ring
lemma apply_norm_le (f : X → ℂ) (hf : AEStronglyMeasurable f μ) {C : ℝ} (hbound : ∀ᵐ x ∂μ, ‖f x‖≤C)
    (g : Lp ℂ 2 μ) : ‖apply μ f hf hbound g‖ ≤ C*‖g‖ := by
  apply Lp.norm_le_mul_norm_of_ae_le_mul
  filter_upwards [apply_ae μ f hf hbound g,hbound] with x hx hf
  rw [hx,norm_mul]
  exact mul_le_mul_of_nonneg_right hf (norm_nonneg _)
def clm (f : X → ℂ) (hf : AEStronglyMeasurable f μ) {C : ℝ} (hbound : ∀ᵐ x ∂μ, ‖f x‖≤C) :
    Lp ℂ 2 μ →L[ℂ] Lp ℂ 2 μ :=
  (linear μ f hf hbound).mkContinuous C (apply_norm_le μ f hf hbound)
end Multiplier
end EuclideanFiveColor
end

noncomputable section
open MeasureTheory Filter
namespace EuclideanFiveColor.ProbabilityL2
variable {X Ω : Type*} [MeasurableSpace X] [MeasurableSpace Ω]
lemma norm_integral_sq (μ : Measure X) [IsProbabilityMeasure μ]
    (f : X → ℂ) (hf : Integrable f μ)
    (hf₂ : Integrable (fun x => ‖f x‖^2) μ) :
    ‖∫ x, f x ∂μ‖^2 ≤ ∫ x, ‖f x‖^2 ∂μ := by
  let a := ∫ x, ‖f x‖ ∂μ
  have ha : 0 ≤ a := integral_nonneg fun _ => norm_nonneg _
  have hvar : 0 ≤ (∫ x, ‖f x‖^2 ∂μ) - a^2 := by
    have h : (0 : ℝ) ≤ ∫ x, (‖f x‖-a)^2 ∂μ :=
      integral_nonneg (fun x => sq_nonneg (‖f x‖-a))
    have he : (fun x => (‖f x‖-a)^2) = fun x => ‖f x‖^2 - (2*a)*‖f x‖ + a^2 := by
      funext x; ring
    rw [he, integral_add (f := fun x => ‖f x‖^2 - (2*a)*‖f x‖) (g := fun _ => a^2) (hf₂.sub (hf.norm.const_mul (2*a))) (integrable_const (a^2)),
      integral_sub (f := fun x => ‖f x‖^2) (g := fun x => (2*a)*‖f x‖) hf₂ (hf.norm.const_mul (2*a)), integral_const_mul] at h
    simp only [integral_const, probReal_univ, one_smul] at h
    change 0 ≤ (∫ x, ‖f x‖^2 ∂μ) - (2*a)*a + a^2 at h
    nlinarith
  have hn : ‖∫ x, f x ∂μ‖ ≤ a := norm_integral_le_integral_norm f
  nlinarith [norm_nonneg (∫ x, f x ∂μ)]

variable (μ : Measure X) [SFinite μ] (ν : Measure Ω) [IsProbabilityMeasure ν]
def average (F : X × Ω → ℂ) (x : X) : ℂ := ∫ ω, F (x,ω) ∂ν
end EuclideanFiveColor.ProbabilityL2
end

end OAI
