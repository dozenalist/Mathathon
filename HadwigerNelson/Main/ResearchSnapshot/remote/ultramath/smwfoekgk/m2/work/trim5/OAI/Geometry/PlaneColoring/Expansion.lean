import Mathlib

namespace OAI

noncomputable section
open Filter Topology Set
open scoped NNReal
namespace EuclideanFiveColor
lemma positive_log_difference_bound {u v m C : ℝ} (hm : 0 < m)
    (hu : m ≤ u) (hv : m ≤ v) (hC : 0 ≤ C) (hd : |u-v| ≤ C) :
    |Real.log u-Real.log v| ≤ C/m := by
  have hu' : 0 < u := hm.trans_le hu
  have hv' : 0 < v := hm.trans_le hv
  have haux : ∀ a b : ℝ, m ≤ a → m ≤ b → a-b ≤ C → Real.log a-Real.log b ≤ C/m := by
    intro a b ha hb hab
    have ha' := hm.trans_le ha
    have hb' := hm.trans_le hb
    have h := Real.log_le_sub_one_of_pos (div_pos ha' hb')
    rw [Real.log_div ha'.ne' hb'.ne'] at h
    have he : a/b-1=(a-b)/b := by field_simp
    rw [he] at h
    exact h.trans ((div_le_div_of_nonneg_right hab hb'.le).trans
      (div_le_div_of_nonneg_left hC hm hb))
  exact abs_le.mpr ⟨by have h := haux v u hv hu (by linarith [neg_le_abs (u-v)]); linarith,
    haux u v hu hv (le_trans (le_abs_self _) hd)⟩
lemma controlled_interval_derivative {f' : ℝ → ℝ} {K : ℝ≥0} {a b e : ℝ}
    (hlip : LipschitzWith K f') (_hab : a ≤ b) (he : (K : ℝ)*(b-a) ≤ e)
    (hmid : 1+e ≤ f' ((a+b)/2)) {t : ℝ} (ht : t ∈ Icc a b) :
    1+e/2 ≤ f' t := by
  have hdist : |t-(a+b)/2| ≤ (b-a)/2 := by rw [abs_le]; constructor <;> linarith [ht.1,ht.2]
  have h := hlip.dist_le_mul t ((a+b)/2)
  rw [Real.dist_eq,Real.dist_eq] at h
  have hm := mul_le_mul_of_nonneg_left hdist K.2
  have hn := neg_le_abs (f' t-f' ((a+b)/2))
  nlinarith
lemma controlled_interval_expands {f f' : ℝ → ℝ} {K : ℝ≥0} {a b e : ℝ}
    (hd : ∀ x, HasDerivAt f (f' x) x) (hlip : LipschitzWith K f') (hab : a ≤ b)
    (he : (K : ℝ)*(b-a) ≤ e) (hmid : 1+e ≤ f' ((a+b)/2)) :
    (1+e/2)*(b-a) ≤ f b-f a := by
  apply (convex_Icc a b).mul_sub_le_image_sub_of_le_deriv
    (fun x _ => (hd x).continuousAt.continuousWithinAt)
    (fun x _ => (hd x).differentiableAt.differentiableWithinAt) _ a ⟨le_rfl,hab⟩ b ⟨hab,le_rfl⟩ hab
  intro t ht
  rw [(hd t).deriv]
  exact controlled_interval_derivative hlip hab he hmid (interior_subset ht)
end EuclideanFiveColor
end

noncomputable section
open Filter Topology Set
open scoped NNReal
namespace EuclideanFiveColor
variable {f D : ℕ → ℝ → ℝ}
end EuclideanFiveColor
end

noncomputable section
open Filter Topology Set
namespace EuclideanFiveColor
end EuclideanFiveColor
end

noncomputable section
open Filter Topology Set
open scoped NNReal
namespace EuclideanFiveColor
end EuclideanFiveColor
end

noncomputable section
open MeasureTheory Filter Topology Set
open scoped NNReal ENNReal
namespace EuclideanFiveColor
end EuclideanFiveColor
end

noncomputable section
open MeasureTheory Filter Topology Set
open scoped NNReal ENNReal
namespace EuclideanFiveColor
end EuclideanFiveColor
end

noncomputable section
open MeasureTheory Filter Topology
open scoped NNReal
namespace EuclideanFiveColor
variable {X Y : Type*} [MeasurableSpace X] [TopologicalSpace Y] [NormalSpace Y]
  [MeasurableSpace Y] [BorelSpace Y] {μ : Measure X} {ν : Measure Y}
omit [TopologicalSpace Y] [NormalSpace Y] [BorelSpace Y] in
omit [TopologicalSpace Y] [NormalSpace Y] [BorelSpace Y] in
end EuclideanFiveColor
end

noncomputable section
open MeasureTheory Filter Topology
open scoped NNReal
namespace EuclideanFiveColor
end EuclideanFiveColor
end

noncomputable section
open MeasureTheory Set Filter Topology
open scoped NNReal
namespace EuclideanFiveColor
end EuclideanFiveColor
end

noncomputable section
open MeasureTheory Filter Topology Set
open scoped NNReal ENNReal
namespace EuclideanFiveColor
end EuclideanFiveColor
end

noncomputable section
open MeasureTheory Filter Topology Set
namespace EuclideanFiveColor
end EuclideanFiveColor
end

noncomputable section
open MeasureTheory Filter Topology Set
open scoped ENNReal
namespace EuclideanFiveColor
end EuclideanFiveColor
end

noncomputable section
open MeasureTheory Filter Topology Set
open scoped NNReal ENNReal
namespace EuclideanFiveColor
end EuclideanFiveColor
end

noncomputable section
open MeasureTheory Filter Topology Set
open scoped NNReal ENNReal
namespace EuclideanFiveColor
end EuclideanFiveColor
end

end OAI
