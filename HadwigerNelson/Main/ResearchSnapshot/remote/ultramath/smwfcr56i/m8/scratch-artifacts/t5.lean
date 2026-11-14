import Mathlib
open MeasureTheory
#check @MeasureTheory.Measure.map
#check @MeasureTheory.Measure.map_apply
example (μ : Measure ℂ) (v : ℂ) : Measure ℂ := μ.map (fun p => p + v)
