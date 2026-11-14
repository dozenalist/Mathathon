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
lemma clm_ae (f : X → ℂ) (hf : AEStronglyMeasurable f μ) {C : ℝ} (hbound : ∀ᵐ x ∂μ, ‖f x‖≤C)
    (g : Lp ℂ 2 μ) : clm μ f hf hbound g =ᵐ[μ] fun x => f x*g x := apply_ae μ f hf hbound g
end Multiplier
abbrev ComplexPlaneL2 := Lp (α := ℂ) ℂ 2 volume
def planeTranslate (h : ℂ) : ComplexPlaneL2 →ₗᵢ[ℂ] ComplexPlaneL2 :=
  Lp.compMeasurePreservingₗᵢ ℂ (fun x => x+h) (measurePreserving_add_right volume h)
lemma planeTranslate_ae (h : ℂ) (g : ComplexPlaneL2) :
    planeTranslate h g =ᵐ[volume] fun x => g (x+h) :=
  Lp.coeFn_compMeasurePreserving g (measurePreserving_add_right volume h)
def planePhase (h ξ : ℂ) : ℂ := Real.fourierChar (inner ℝ h ξ)
lemma planePhase_norm (h ξ : ℂ) : ‖planePhase h ξ‖=1 := Circle.norm_coe _
lemma planePhase_continuous (h : ℂ) : Continuous (planePhase h) := by
  unfold planePhase
  fun_prop

def phaseMultiplier (h : ℂ) : ComplexPlaneL2 →L[ℂ] ComplexPlaneL2 :=
  Multiplier.clm volume (planePhase h) (planePhase_continuous h).aestronglyMeasurable
    (Eventually.of_forall fun ξ => (planePhase_norm h ξ).le)
lemma phaseMultiplier_ae (h : ℂ) (g : ComplexPlaneL2) :
    phaseMultiplier h g =ᵐ[volume] fun ξ => planePhase h ξ*g ξ := Multiplier.clm_ae _ _ _ _ _
def schwartzTranslate (h : ℂ) : SchwartzMap ℂ ℂ →L[ℂ] SchwartzMap ℂ ℂ :=
  SchwartzMap.compCLMOfAntilipschitz ℂ
    (Function.HasTemperateGrowth.id.add (Function.HasTemperateGrowth.const h)) (isometry_add_right h).antilipschitzWith
lemma schwartzTranslate_apply (h : ℂ) (f : SchwartzMap ℂ ℂ) (x : ℂ) :
    schwartzTranslate h f x = f (x+h) := rfl
lemma schwartzTranslate_toLp (h : ℂ) (f : SchwartzMap ℂ ℂ) :
    (schwartzTranslate h f).toLp 2 = planeTranslate h (f.toLp 2) := by
  apply Lp.ext
  filter_upwards [(schwartzTranslate h f).coeFn_toLp 2,planeTranslate_ae h (f.toLp 2),
    (measurePreserving_add_right volume h).quasiMeasurePreserving.ae (f.coeFn_toLp 2 volume)] with x hx hy hz
  exact hx.trans ((schwartzTranslate_apply h f x).trans (hz.symm.trans hy.symm))
lemma fourier_schwartzTranslate (h : ℂ) (f : SchwartzMap ℂ ℂ) (ξ : ℂ) :
    𝓕 (schwartzTranslate h f) ξ = planePhase h ξ * 𝓕 f ξ := by
  have hh := congrFun (VectorFourier.fourierIntegral_comp_add_right Real.fourierChar volume
    (innerₗ ℂ) (f : ℂ → ℂ) h) ξ
  simpa only [SchwartzMap.fourier_coe,Real.fourier_eq,schwartzTranslate_apply,
    planePhase,Circle.smul_def,smul_eq_mul,VectorFourier.fourierIntegral,Function.comp_def,innerₗ_apply_apply] using hh
lemma fourier_planeTranslate (h : ℂ) (g : ComplexPlaneL2) :
    𝓕 (planeTranslate h g) = phaseMultiplier h (𝓕 g) := by
  apply DenseRange.induction_on (p := fun g : ComplexPlaneL2 => 𝓕 (planeTranslate h g) = phaseMultiplier h (𝓕 g))
    (SchwartzMap.denseRange_toLpCLM (E := ℂ) (F := ℂ) (p := 2) ENNReal.ofNat_ne_top) g
  · exact isClosed_eq ((Lp.fourierTransformₗᵢ ℂ ℂ).continuous.comp (planeTranslate h).continuous)
      ((phaseMultiplier h).continuous.comp (Lp.fourierTransformₗᵢ ℂ ℂ).continuous)
  intro f
  change 𝓕 (planeTranslate h (f.toLp 2)) = phaseMultiplier h (𝓕 (f.toLp 2))
  rw [← schwartzTranslate_toLp,SchwartzMap.toLp_fourier_eq,SchwartzMap.toLp_fourier_eq]
  apply Lp.ext
  filter_upwards [(𝓕 (schwartzTranslate h f)).coeFn_toLp 2,phaseMultiplier_ae h ((𝓕 f).toLp 2),
    (𝓕 f).coeFn_toLp 2] with ξ hξ hmul hf
  rw [hξ,hmul,hf]
  exact fourier_schwartzTranslate h f ξ
end EuclideanFiveColor
end

noncomputable section
open MeasureTheory Filter
namespace EuclideanFiveColor.ProbabilityL2
variable {X Ω : Type*} [MeasurableSpace X] [MeasurableSpace Ω]

variable (μ : Measure X) [SFinite μ] (ν : Measure Ω) [IsProbabilityMeasure ν]
def average (F : X × Ω → ℂ) (x : X) : ℂ := ∫ ω, F (x,ω) ∂ν
end EuclideanFiveColor.ProbabilityL2
end

end OAI
