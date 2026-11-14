import OAI.Geometry.PlaneColoring.Basic

namespace OAI

noncomputable section

open MeasureTheory

namespace Problem160
instance normalizedAngleMeasure_isProbabilityMeasure :
    IsProbabilityMeasure normalizedAngleMeasure where
  measure_univ := by
    have hpos : 0 < (2 : ℝ) * Real.pi := by positivity
    simp only [normalizedAngleMeasure, Measure.smul_apply, Measure.restrict_apply_univ,
      Real.volume_Ico, sub_zero, smul_eq_mul]
    exact ENNReal.inv_mul_cancel (ne_of_gt (ENNReal.ofReal_pos.mpr hpos))
      ENNReal.ofReal_ne_top

instance circleMeasure_isProbabilityMeasure : IsProbabilityMeasure circleMeasure :=
  inferInstanceAs (IsProbabilityMeasure (Measure.map circleDir normalizedAngleMeasure))
end Problem160

end

end OAI
