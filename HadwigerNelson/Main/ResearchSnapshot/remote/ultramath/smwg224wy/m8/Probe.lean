import OAI.Analysis.PlaneSpectrum.Energy

namespace OAI
open MeasureTheory
namespace PlaneFiveColor.Spectral
open EuclideanFiveColor.BoundedMeasurable

#check @char
#check @eval
#check @kCoeff
#check @K
#check @IsWild
#check @j_zero
#check @scalar_mul
#check @Circle.coe_inv_eq_conj

example (u : K) : kCoeff u ≠ 0 := kCoeff_ne_zero u

end PlaneFiveColor.Spectral
end OAI
