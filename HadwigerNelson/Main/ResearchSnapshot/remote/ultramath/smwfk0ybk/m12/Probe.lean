import Mathlib
open MeasureTheory
#check @LinearIsometryEquiv.measurePreserving
#check @AEMeasurable.mk
#check @Measure.iUnion_null_iff
#check @Measure.restrict_prod
#check @Measure.map_prod_map
#check @Complex.measurableEquivRealProd
example : Measure.map (fun z : ℂ => (WithLp.toLp 2 ![z.re, z.im] : EuclideanSpace ℝ (Fin 2))) volume = volume := by
  sorry
