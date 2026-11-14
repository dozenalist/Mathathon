import Mathlib
open MeasureTheory Filter Topology Set
open scoped ENNReal
#check @Measure.prod_prod
#check @MeasureTheory.volume_prod
#check @Complex.measurableEquivRealProd
example (z : ℂ) : Complex.measurableEquivRealProd z = (z.re, z.im) := rfl
#check @ENNReal.le_div_iff_mul_le
#check @ENNReal.le_div_iff_mul_le'
#check @ENNReal.mul_div_cancel
#check @ENNReal.ofReal_mul
#check @Complex.measurableEquivPi
#check @ENNReal.ofReal_pos
#check @Complex.dist_eq
#check @Complex.norm_def
#check @Complex.sq_abs
#check @Complex.abs_re_le_norm
#check @Complex.abs_im_le_norm
#check @Metric.mem_ball
#check @isOpen_lt
#check @SimpleGraph.Walk.IsCycle
#check @SimpleGraph.not_isAcyclic_iff
#check @SimpleGraph.IsAcyclic
