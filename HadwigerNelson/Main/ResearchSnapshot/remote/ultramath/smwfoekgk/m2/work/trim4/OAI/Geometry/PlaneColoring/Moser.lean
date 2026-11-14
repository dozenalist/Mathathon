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
/-- Exact strict angular form of the manuscript's polynomial region. -/
end EuclideanFiveColor
end

noncomputable section
namespace EuclideanFiveColor
def moserA : ℂ := ((Real.sqrt 3 : ℂ)+Complex.I)/2
def moserB : ℂ := ((Real.sqrt 3 : ℂ)-Complex.I)/2
def moserT : ℂ := Real.sqrt 3
def moserU : ℂ := (5+Complex.I*(Real.sqrt 11 : ℂ))/6
def moserPoint : Fin 7 → ℂ := ![0,moserA,moserB,moserT,moserU*moserA,moserU*moserB,moserU*moserT]
@[simp] lemma moserPoint_0 : moserPoint 0=0 := rfl
@[simp] lemma moserPoint_1 : moserPoint 1=moserA := rfl
@[simp] lemma moserPoint_2 : moserPoint 2=moserB := rfl
@[simp] lemma moserPoint_3 : moserPoint 3=moserT := rfl
@[simp] lemma moserPoint_4 : moserPoint 4=moserU*moserA := rfl
@[simp] lemma moserPoint_5 : moserPoint 5=moserU*moserB := rfl
@[simp] lemma moserPoint_6 : moserPoint 6=moserU*moserT := rfl
end EuclideanFiveColor
end

noncomputable section
namespace EuclideanFiveColor
end EuclideanFiveColor
end

noncomputable section
namespace EuclideanFiveColor
/-- Exact rational interval certificate for the manuscript's seven placed vertices. -/
end EuclideanFiveColor
end

end OAI
