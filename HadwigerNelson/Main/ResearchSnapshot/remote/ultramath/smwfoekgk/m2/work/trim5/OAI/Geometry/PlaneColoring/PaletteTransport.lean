import OAI.Geometry.PlaneColoring.PaletteDensity

namespace OAI

noncomputable section
open MeasureTheory Filter Topology Set
namespace EuclideanFiveColor
lemma angleRep_preserving (a : ℝ) :
    MeasurePreserving (fun t : Angles => (AddCircle.equivIoc (2*Real.pi) a t : ℝ))
      volume (volume.restrict (Ioc a (a+2*Real.pi))) :=
  (measurePreserving_subtype_coe measurableSet_Ioc).comp (AddCircle.measurePreserving_equivIoc _)
lemma weak_lift_Ioc {F : ℕ → Angles → ℝ} {b : Angles → ℝ}
    (hw : ∀ v : Angles → ℝ, Integrable v angularMeasure →
      Tendsto (fun n => ∫ t, F n t*v t ∂angularMeasure) atTop (𝓝 (∫ t, b t*v t ∂angularMeasure)))
    (a : ℝ) (v : ℝ → ℝ) (hv : Integrable v (volume.restrict (Ioc a (a+2*Real.pi)))) :
    Tendsto (fun n => ∫ t in Ioc a (a+2*Real.pi), F n (t : Angles)*v t) atTop
      (𝓝 (∫ t in Ioc a (a+2*Real.pi), b (t : Angles)*v t)) := by
  let V : Angles → ℝ := AddCircle.liftIoc (2*Real.pi) a v
  have hvi : Integrable V (volume : Measure Angles) := (angleRep_preserving a).integrable_comp_of_integrable hv
  have hva : Integrable V angularMeasure := by
    rw [AddCircle.volume_eq_smul_haarAddCircle] at hvi
    exact (integrable_smul_measure (by positivity : ENNReal.ofReal (2*Real.pi) ≠ 0) (ENNReal.ofReal_ne_top)).mp hvi
  have h := (hw V hva).const_mul (2*Real.pi)
  have he (f : Angles → ℝ) : (∫ t in Ioc a (a+2*Real.pi), f (t : Angles)*v t) =
      (2*Real.pi)*(∫ t, f t*V t ∂angularMeasure) := by
    have hpre := AddCircle.integral_preimage (2*Real.pi) a (fun t => f t*V t)
    have hi : (∫ t in Ioc a (a+2*Real.pi), f (t : Angles)*v t) =
        ∫ t in Ioc a (a+2*Real.pi), f (t : Angles)*V (t : Angles) := by
      apply setIntegral_congr_fun measurableSet_Ioc
      intro t ht
      change f (t : Angles)*v t=f (t : Angles)*V (t : Angles)
      rw [show V (t : Angles)=v t from AddCircle.liftIoc_coe_apply ht]
    rw [hi,hpre,AddCircle.volume_eq_smul_haarAddCircle,integral_smul_measure,
      ENNReal.toReal_ofReal (by positivity : 0 ≤ 2*Real.pi),smul_eq_mul]
    rfl
  simpa only [← he] using h
lemma weak_restrict {X : Type*} [MeasurableSpace X] {μ : Measure X}
    {F : ℕ → X → ℝ} {b : X → ℝ}
    (hw : ∀ v : X → ℝ, Integrable v μ →
      Tendsto (fun n => ∫ t, F n t*v t ∂μ) atTop (𝓝 (∫ t, b t*v t ∂μ)))
    {I : Set X} (hI : MeasurableSet I) :
    ∀ v : X → ℝ, Integrable v (μ.restrict I) →
      Tendsto (fun n => ∫ t, F n t*v t ∂μ.restrict I) atTop
        (𝓝 (∫ t, b t*v t ∂μ.restrict I)) := by
  intro v hv
  have hvi : Integrable (I.indicator v) μ := (integrable_indicator_iff hI).mpr hv
  have h := hw (I.indicator v) hvi
  have he (f : X → ℝ) : (fun t => f t*I.indicator v t)=I.indicator (fun t => f t*v t) := by
    funext t
    by_cases ht : t ∈ I <;> simp [ht]
  simpa only [he,integral_indicator hI] using h
lemma weak_lift_set {F : ℕ → Angles → ℝ} {b : Angles → ℝ}
    (hw : ∀ v : Angles → ℝ, Integrable v angularMeasure →
      Tendsto (fun n => ∫ t, F n t*v t ∂angularMeasure) atTop (𝓝 (∫ t, b t*v t ∂angularMeasure)))
    {I : Set ℝ} (hI : MeasurableSet I) {a : ℝ} (hIa : I ⊆ Ioc a (a+2*Real.pi)) :
    ∀ v : ℝ → ℝ, Integrable v (volume.restrict I) →
      Tendsto (fun n => ∫ t in I, F n (t : Angles)*v t) atTop
        (𝓝 (∫ t in I, b (t : Angles)*v t)) := by
  have h := weak_restrict (weak_lift_Ioc hw a) hI
  simpa only [Measure.restrict_restrict hI,inter_eq_left.mpr hIa] using h
end EuclideanFiveColor
end

noncomputable section
open MeasureTheory Filter Topology
namespace EuclideanFiveColor
end EuclideanFiveColor
end

noncomputable section
open MeasureTheory Filter Topology Set
open scoped NNReal
namespace EuclideanFiveColor
variable {k : ℕ} (c : ℂ → Fin k) (hc : Measurable c)
end EuclideanFiveColor
end

noncomputable section
open MeasureTheory Filter Topology Set
namespace EuclideanFiveColor
variable {k : ℕ} (c : ℂ → Fin k) (hc : Measurable c)
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology MeasureTheory
namespace EuclideanFiveColor
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology MeasureTheory
namespace EuclideanFiveColor
end EuclideanFiveColor
end

noncomputable section
open MeasureTheory Filter Topology Set
namespace EuclideanFiveColor
variable {k : ℕ} (c : ℂ → Fin k) (hc : Measurable c)
end EuclideanFiveColor
end

noncomputable section
open Filter Topology Set MeasureTheory
namespace EuclideanFiveColor
end EuclideanFiveColor
end

noncomputable section
open MeasureTheory Filter Topology Set
namespace EuclideanFiveColor
variable {k : ℕ} (c : ℂ → Fin k) (hc : Measurable c)
end EuclideanFiveColor
end

noncomputable section
open MeasureTheory Set Filter Topology
namespace EuclideanFiveColor
end EuclideanFiveColor
end

noncomputable section
open Filter Topology Set MeasureTheory
namespace EuclideanFiveColor
def sixty : ℝ := Real.pi/3
end EuclideanFiveColor
end

noncomputable section
open Filter Topology Set MeasureTheory
namespace EuclideanFiveColor
end EuclideanFiveColor
end

noncomputable section
open MeasureTheory Filter Topology Set
namespace EuclideanFiveColor
variable {k : ℕ} (c : ℂ → Fin k) (hc : Measurable c)
end EuclideanFiveColor
end

end OAI
