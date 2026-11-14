import Mathlib

namespace OAI

noncomputable section
namespace EuclideanFiveColor
def ThreeLabelRegion (x y : ℝ) : Prop :=
  0<x^2+y^2 ∧ x^2+y^2<4 ∧
    y^2*(3*x^2-y^2)^2 < (x^2+y^2)^3*(1-(x^2+y^2)/4)*(x^2+y^2-1)^2
lemma square_coordinate_bounds {x c h : ℝ} (_hh : 0≤h) (hc : h≤|c|) (hx : |x-c|≤h) :
    (|c|-h)^2≤x^2 ∧ x^2≤(|c|+h)^2 := by
  have hu : |x|≤|c|+h := by
    calc |x|=|c+(x-c)| := by congr 1; ring
         _≤|c|+|x-c| := abs_add_le _ _
         _≤|c|+h := by linarith
  have hl : |c|-h≤|x| := by
    have ht : |c|≤|x|+|x-c| := by
      calc |c|=|x-(x-c)| := by congr 1; ring
           _≤|x|+|x-c| := abs_sub _ _
    linarith
  constructor
  · simpa only [sq_abs] using pow_le_pow_left₀ (sub_nonneg.mpr hc) hl 2
  · simpa only [sq_abs] using pow_le_pow_left₀ (abs_nonneg x) hu 2
lemma region_of_rational_bounds {x y a b Y H d : ℝ}
    (ha : 0<a) (hb : b<4) (hY : 0≤Y) (_hH : 0≤H) (hd : 0≤d)
    (hl : a≤x^2+y^2) (hu : x^2+y^2≤b)
    (hy : y^2≤Y) (habs : |3*x^2-y^2|≤H) (hg : d≤|x^2+y^2-1|)
    (hnum : Y*H^2<a^3*(1-b/4)*d^2) : ThreeLabelRegion x y := by
  refine ⟨lt_of_lt_of_le ha hl,lt_of_le_of_lt hu hb,?_⟩
  calc y^2*(3*x^2-y^2)^2 ≤ Y*H^2 := by
         have hpow : (3*x^2-y^2)^2≤H^2 := by
           simpa only [sq_abs] using pow_le_pow_left₀ (abs_nonneg _) habs 2
         exact mul_le_mul hy hpow (sq_nonneg _) hY
       _ < a^3*(1-b/4)*d^2 := hnum
       _ ≤ (x^2+y^2)^3*(1-(x^2+y^2)/4)*(x^2+y^2-1)^2 := by
         have hnonneg : 0≤1-b/4 := by linarith
         have hgap : d^2≤(x^2+y^2-1)^2 := by
           simpa only [sq_abs] using pow_le_pow_left₀ hd hg 2
         have hpos : 0≤(x^2+y^2)^3*(1-(x^2+y^2)/4) :=
           mul_nonneg (pow_nonneg (le_trans ha.le hl) _) (by linarith)
         gcongr
end EuclideanFiveColor
end

noncomputable section
namespace EuclideanFiveColor
end EuclideanFiveColor
end

noncomputable section
namespace EuclideanFiveColor
end EuclideanFiveColor
end

noncomputable section
namespace EuclideanFiveColor
end EuclideanFiveColor
end

noncomputable section
namespace EuclideanFiveColor
end EuclideanFiveColor
end

end OAI
