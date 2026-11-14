import OAI.Geometry.PlaneColoring.Expansion

namespace OAI

noncomputable section
open Set Filter Topology
namespace EuclideanFiveColor
def binaryQ (d t : ℝ) : ℝ := 1-2*d*Real.cos t+d^2
def binaryR (d t : ℝ) : ℝ := 2*Real.sqrt (binaryQ d t)*Real.sqrt (1-binaryQ d t/4)
def binaryB (d t : ℝ) : ℝ := (Real.cos t-d)/binaryQ d t+Real.sin t/binaryR d t
def binaryM (d t : ℝ) : ℝ := Real.sin t/binaryQ d t+(d-Real.cos t)/binaryR d t
def binaryCircleMap (d t : ℝ) : ℝ :=
  t+Real.pi/3+Real.arctan (d*Real.sin t/(1-d*Real.cos t))-Real.arccos (Real.sqrt (binaryQ d t)/2)
lemma binaryQ_range {d : ℝ} (hd : |d| < 1/2) (t : ℝ) :
    0 < binaryQ d t ∧ binaryQ d t < 4 ∧ 0 < 1-d*Real.cos t := by
  have hdc : |d*Real.cos t| ≤ |d| := by
    simpa only [abs_mul,mul_one] using mul_le_mul_of_nonneg_left (Real.abs_cos_le_one t) (abs_nonneg d)
  have hdc' := abs_le.mp hdc
  have hd' := abs_lt.mp hd
  dsimp [binaryQ]
  constructor
  · nlinarith [sq_nonneg d]
  constructor
  · nlinarith [sq_abs d,abs_nonneg d]
  · linarith
lemma binaryR_pos {d : ℝ} (hd : |d| < 1/2) (t : ℝ) : 0 < binaryR d t := by
  have h := binaryQ_range hd t
  unfold binaryR
  exact mul_pos (mul_pos (by norm_num) (Real.sqrt_pos.mpr h.1)) (Real.sqrt_pos.mpr (by linarith [h.2.1]))
lemma binary_arctan_identity (d t : ℝ) :
    (1-d*Real.cos t)^2+(d*Real.sin t)^2=binaryQ d t := by
  have h := Real.sin_sq_add_cos_sq t
  dsimp [binaryQ]
  nlinarith [sq_nonneg d]
lemma binary_arctan_recip {d : ℝ} (hd : |d| < 1/2) (t : ℝ) :
    1/(1+(d*Real.sin t/(1-d*Real.cos t))^2)/(1-d*Real.cos t)^2=1/binaryQ d t := by
  have hq := binaryQ_range hd t
  have hi := binary_arctan_identity d t
  field_simp [hq.1.ne',hq.2.2.ne']
  simp only [mul_pow] at hi
  rw [hi,div_self hq.1.ne']
lemma binaryCircleMap_hasDeriv_t {d : ℝ} (hd : |d| < 1/2) (t : ℝ) :
    HasDerivAt (binaryCircleMap d) (1+d*binaryB d t) t := by
  have hq := binaryQ_range hd t
  have hsq := Real.sq_sqrt hq.1.le
  have hs : 0 < Real.sqrt (binaryQ d t) := Real.sqrt_pos.mpr hq.1
  have hc : Real.sqrt (binaryQ d t)/2 ≠ -1 := by linarith
  have hc' : Real.sqrt (binaryQ d t)/2 ≠ 1 := by intro h; nlinarith [hq.2.1]
  have hqd : HasDerivAt (binaryQ d) (2*d*Real.sin t) t := by
    convert (((Real.hasDerivAt_cos t).const_mul (2*d)).const_sub 1).add_const (d^2) using 1 <;>
      first | rfl | ring
  have hat := (((Real.hasDerivAt_sin t).const_mul d).div
    (((Real.hasDerivAt_cos t).const_mul d).const_sub 1) hq.2.2.ne').arctan
  have hac := (Real.hasDerivAt_arccos hc hc').comp t ((hqd.sqrt hq.1.ne').div_const 2)
  have hh := (((hasDerivAt_id t).add_const (Real.pi/3)).add hat).sub hac
  change HasDerivAt (binaryCircleMap d) _ t at hh
  convert hh using 1
  dsimp [binaryB,binaryR]
  have hss : 1-(Real.sqrt (binaryQ d t)/2)^2=1-binaryQ d t/4 := by nlinarith [hsq]
  rw [hss]
  have hrec := binary_arctan_recip hd t
  have hnum : d*Real.cos t*(1-d*Real.cos t)-d*Real.sin t*-(d*-Real.sin t)=
      d*(Real.cos t-d) := by linear_combination -d^2*(Real.sin_sq_add_cos_sq t)
  rw [hnum]
  have hrearr : 1/(1+(d*Real.sin t/(1-d*Real.cos t))^2)*
      (d*(Real.cos t-d)/(1-d*Real.cos t)^2) = d*(Real.cos t-d)/binaryQ d t := by
    calc
      _ = (1/(1+(d*Real.sin t/(1-d*Real.cos t))^2)/(1-d*Real.cos t)^2)*(d*(Real.cos t-d)) := by ring
      _ = d*(Real.cos t-d)/binaryQ d t := by rw [hrec]; ring
  rw [hrearr]
  ring
lemma binaryCircleMap_hasDeriv_d {d : ℝ} (hd : |d| < 1/2) (t : ℝ) :
    HasDerivAt (fun s => binaryCircleMap s t) (binaryM d t) d := by
  have hq := binaryQ_range hd t
  have hsq := Real.sq_sqrt hq.1.le
  have hs : 0 < Real.sqrt (binaryQ d t) := Real.sqrt_pos.mpr hq.1
  have hc : Real.sqrt (binaryQ d t)/2 ≠ -1 := by linarith
  have hc' : Real.sqrt (binaryQ d t)/2 ≠ 1 := by intro h; nlinarith [hq.2.1]
  have hqd : HasDerivAt (fun s => binaryQ s t) (2*(d-Real.cos t)) d := by
    convert (((hasDerivAt_id d).mul_const (2*Real.cos t)).const_sub 1).add ((hasDerivAt_id d).pow 2) using 1 <;>
      first | rfl | (funext s; dsimp only [binaryQ,Pi.add_apply,Pi.pow_apply,id_eq]; ring) |
        (try dsimp only [id_eq]; ring)
  have hat := (((hasDerivAt_id d).mul_const (Real.sin t)).div
    (((hasDerivAt_id d).mul_const (Real.cos t)).const_sub 1) hq.2.2.ne').arctan
  have hac := (Real.hasDerivAt_arccos hc hc').comp d ((hqd.sqrt hq.1.ne').div_const 2)
  have hh := (hat.const_add (t+Real.pi/3)).sub hac
  change HasDerivAt (fun s => binaryCircleMap s t) _ d at hh
  convert hh using 1
  dsimp [binaryM,binaryR]
  have hss : 1-(Real.sqrt (binaryQ d t)/2)^2=1-binaryQ d t/4 := by nlinarith [hsq]
  rw [hss]
  have hrec := binary_arctan_recip hd t
  simp only [one_mul]
  have hnum : Real.sin t*(1-d*Real.cos t)-d*Real.sin t*-(Real.cos t)=Real.sin t := by ring
  rw [hnum]
  have hrearr : 1/(1+(d*Real.sin t/(1-d*Real.cos t))^2)*
      (Real.sin t/(1-d*Real.cos t)^2) = Real.sin t/binaryQ d t := by
    calc
      _ = (1/(1+(d*Real.sin t/(1-d*Real.cos t))^2)/(1-d*Real.cos t)^2)*Real.sin t := by ring
      _ = Real.sin t/binaryQ d t := by rw [hrec]; ring
  rw [hrearr]
  ring
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology
namespace EuclideanFiveColor
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology
namespace EuclideanFiveColor
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology
namespace EuclideanFiveColor
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology
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
open Set Filter Topology MeasureTheory
open scoped NNReal ENNReal
namespace EuclideanFiveColor
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology MeasureTheory
namespace EuclideanFiveColor
end EuclideanFiveColor
end

end OAI
