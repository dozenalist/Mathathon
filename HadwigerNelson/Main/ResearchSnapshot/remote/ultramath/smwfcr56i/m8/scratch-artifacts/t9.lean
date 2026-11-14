import Mathlib
open MeasureTheory
example (ν : ProbabilityMeasure ℂ) (v : ℂ) : ProbabilityMeasure ℂ :=
  ν.map (f := fun p => p + v) (continuous_id.add_const v).aemeasurable
example (ν : ProbabilityMeasure ℂ) (v : ℂ) : ProbabilityMeasure ℂ :=
  ProbabilityMeasure.map ν (f := fun p => p + v) (continuous_id.add_const v).aemeasurable
