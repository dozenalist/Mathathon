import OAI.Geometry.PlaneColoring.Basic

namespace OAI

noncomputable section

open MeasureTheory

namespace Problem160

@[continuity, fun_prop]
theorem continuous_circleDir : Continuous circleDir := by
  unfold circleDir
  fun_prop

@[fun_prop]
theorem measurable_circleDir : Measurable circleDir :=
  continuous_circleDir.measurable

instance normalizedAngleMeasure_isProbabilityMeasure :
    IsProbabilityMeasure normalizedAngleMeasure where
  measure_univ := by
    have hpos : 0 < (2 : ℝ) * Real.pi := by positivity
    simp only [normalizedAngleMeasure, Measure.smul_apply, Measure.restrict_apply_univ,
      Real.volume_Ico, sub_zero, smul_eq_mul]
    exact ENNReal.inv_mul_cancel (ne_of_gt (ENNReal.ofReal_pos.mpr hpos))
      ENNReal.ofReal_ne_top

instance circleMeasure_isProbabilityMeasure : IsProbabilityMeasure circleMeasure :=
  Measure.isProbabilityMeasure_map measurable_circleDir.aemeasurable

@[simp]
theorem norm_circleDir (t : ℝ) : ‖circleDir t‖ = 1 := by
  have h : ‖circleDir t‖ ^ 2 = 1 := by
    rw [EuclideanSpace.real_norm_sq_eq]
    simp [circleDir, Fin.sum_univ_two]
  nlinarith [norm_nonneg (circleDir t)]




end Problem160

end

end OAI
