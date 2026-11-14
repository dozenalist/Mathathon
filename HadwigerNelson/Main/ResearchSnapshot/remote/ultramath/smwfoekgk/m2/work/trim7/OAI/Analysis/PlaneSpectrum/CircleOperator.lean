import OAI.Analysis.PlaneSpectrum.CircleDecay
import OAI.Geometry.PlaneColoring.Compactness

namespace OAI

noncomputable section
open MeasureTheory Filter Topology FourierTransform
namespace EuclideanFiveColor
lemma planeTranslate_continuous (g : ComplexPlaneL2) : Continuous (fun h => planeTranslate h g) := by
  let f : C(ℂ,C(ℂ,ℂ)) := (ContinuousMap.mk (fun p : ℂ × ℂ => p.2+p.1) (by fun_prop)).curry
  exact continuous_const.compMeasurePreservingLp f.continuous (fun h => measurePreserving_add_right volume h) (by simp)
lemma circleTranslate_integrable (g : ComplexPlaneL2) : Integrable (fun t => planeTranslate (direction t) g) angularMeasure :=
  Integrable.of_bound ((planeTranslate_continuous g).comp direction_continuous).aestronglyMeasurable ‖g‖
    (Eventually.of_forall fun t => (planeTranslate (direction t)).norm_map g |>.le)
def circleOperator (g : ComplexPlaneL2) : ComplexPlaneL2 := ∫ t, planeTranslate (direction t) g ∂angularMeasure
lemma circleOperator_ae (g : ComplexPlaneL2) :
    circleOperator g =ᵐ[volume] fun x => ∫ t, g (x+direction t) ∂angularMeasure := by
  let F : ℂ × Angles → ℂ := fun p => g (p.1+direction p.2)
  have hF : StronglyMeasurable F := (Lp.stronglyMeasurable g).comp_measurable
    (measurable_fst.add (direction_continuous.measurable.comp measurable_snd))
  have hg2 : Integrable (fun x => ‖g x‖^2) volume :=
    (memLp_two_iff_integrable_sq_norm (Lp.aestronglyMeasurable g)).mp (Lp.memLp g)
  have hi : Integrable (fun p => ‖F p‖^2) (volume.prod angularMeasure) := by
    apply (integrable_prod_iff' (hF.norm.pow 2).aestronglyMeasurable).mpr
    constructor
    · exact Eventually.of_forall fun t => (measurePreserving_add_right volume (direction t)).integrable_comp_of_integrable hg2
    · have he : (fun t => ∫ x, ‖‖F (x,t)‖^2‖ ∂volume) = fun _ => ∫ x, ‖g x‖^2 ∂volume := by
        funext t
        simp only [Real.norm_eq_abs,abs_sq,F]
        change (∫ x : ℂ, (fun y => ‖g y‖^2) (x+direction t)) = _
        exact (measurePreserving_add_right volume (direction t)).integral_comp
          (Homeomorph.addRight (direction t)).measurableEmbedding (fun y : ℂ => ‖g y‖^2)
      simp only [Pi.pow_apply]
      rw [he]
      exact integrable_const _
  have h := ProbabilityL2.average_toLp_integral volume angularMeasure hF hi
    (fun t => planeTranslate (direction t) g) (circleTranslate_integrable g)
    (Eventually.of_forall fun t => planeTranslate_ae (direction t) g)
  have ha : circleOperator g = (ProbabilityL2.average_memLp volume angularMeasure hF hi).toLp (ProbabilityL2.average angularMeasure F) := h.symm
  rw [ha]
  exact MemLp.coeFn_toLp (ProbabilityL2.average_memLp volume angularMeasure hF hi)
lemma circleSymbol_stronglyMeasurable : StronglyMeasurable circleSymbol := by
  have h : Continuous (fun p : ℂ × Angles => planePhase (direction p.2) p.1) := by
    unfold planePhase
    exact (continuous_subtype_val.comp Real.continuous_fourierChar).comp
      ((direction_continuous.comp continuous_snd).inner continuous_fst)
  exact h.stronglyMeasurable.integral_prod_right'
def circleMultiplier : ComplexPlaneL2 →L[ℂ] ComplexPlaneL2 :=
  Multiplier.clm volume circleSymbol circleSymbol_stronglyMeasurable.aestronglyMeasurable
    (Eventually.of_forall circleSymbol_norm_le_one)
lemma circleMultiplier_ae (g : ComplexPlaneL2) :
    circleMultiplier g =ᵐ[volume] fun x => circleSymbol x*g x := Multiplier.clm_ae _ _ _ _ _
lemma fourier_circleOperator (g : ComplexPlaneL2) : 𝓕 (circleOperator g) = circleMultiplier (𝓕 g) := by
  let F : ℂ × Angles → ℂ := fun p => planePhase (direction p.2) p.1 * 𝓕 g p.1
  have hF : StronglyMeasurable F := by
    have h : Continuous (fun p : ℂ × Angles => planePhase (direction p.2) p.1) := by
      unfold planePhase
      exact (continuous_subtype_val.comp Real.continuous_fourierChar).comp
        ((direction_continuous.comp continuous_snd).inner continuous_fst)
    exact h.stronglyMeasurable.mul ((Lp.stronglyMeasurable (𝓕 g)).comp_measurable measurable_fst)
  have hi : Integrable (fun p => ‖F p‖^2) (volume.prod angularMeasure) := by
    have he : (fun p => ‖F p‖^2) = fun p => ‖𝓕 g p.1‖^2 := by
      funext p
      simp only [F,norm_mul,planePhase_norm,one_mul]
    rw [he]
    exact ((memLp_two_iff_integrable_sq_norm (Lp.aestronglyMeasurable (𝓕 g))).mp
      (Lp.memLp (𝓕 g))).comp_fst angularMeasure
  have hG : Integrable (fun t => 𝓕 (planeTranslate (direction t) g)) angularMeasure :=
    (Lp.fourierTransformₗᵢ ℂ ℂ).toContinuousLinearEquiv.toContinuousLinearMap.integrable_comp
      (circleTranslate_integrable g)
  have h := ProbabilityL2.average_toLp_integral volume angularMeasure hF hi
    (fun t => 𝓕 (planeTranslate (direction t) g)) hG (Eventually.of_forall fun t => by
      rw [fourier_planeTranslate]
      exact phaseMultiplier_ae (direction t) (𝓕 g))
  have hc := (Lp.fourierTransformₗᵢ ℂ ℂ).toContinuousLinearEquiv.toContinuousLinearMap.integral_comp_comm
    (circleTranslate_integrable g)
  change (∫ t, 𝓕 (planeTranslate (direction t) g) ∂angularMeasure) = 𝓕 (circleOperator g) at hc
  rw [← hc,← h]
  apply Lp.ext
  filter_upwards [MemLp.coeFn_toLp (ProbabilityL2.average_memLp volume angularMeasure hF hi),
    circleMultiplier_ae (𝓕 g)] with x hx hy
  rw [hx,hy]
  exact integral_mul_const (𝓕 g x) (fun t => planePhase (direction t) x)
end EuclideanFiveColor
end

noncomputable section
open MeasureTheory Filter Topology
namespace EuclideanFiveColor
end EuclideanFiveColor
end

noncomputable section
open MeasureTheory Filter Topology FourierTransform
namespace EuclideanFiveColor
end EuclideanFiveColor
end

noncomputable section
open MeasureTheory MeasureTheory.Measure Filter Topology Set
namespace EuclideanFiveColor
end EuclideanFiveColor
end

end OAI
