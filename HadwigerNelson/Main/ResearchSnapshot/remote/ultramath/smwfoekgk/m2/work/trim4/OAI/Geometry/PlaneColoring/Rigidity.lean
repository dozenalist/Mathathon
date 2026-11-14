import OAI.Geometry.PlaneColoring.PaletteTransport

namespace OAI

noncomputable section
open Set Filter Topology
namespace EuclideanFiveColor
/-- Common unit neighbor for the transverse chord of length `t`. -/
def evenOffset (v : ℂ) (t : ℝ) : ℂ :=
  ((Real.sqrt (1-t^2/4) : ℂ)+((t/2 : ℝ) : ℂ)*Complex.I)*v
lemma norm_even_wing {t : ℝ} (ht : |t|<2) :
    ‖(Real.sqrt (1-t^2/4) : ℂ)+((t/2 : ℝ) : ℂ)*Complex.I‖=1 := by
  have ht2 : t^2≤4 := by
    have hh := mul_self_le_mul_self (abs_nonneg t) ht.le
    nlinarith [sq_abs t]
  have hsq := Real.sq_sqrt (show 0≤1-t^2/4 by linarith)
  apply (sq_eq_sq₀ (norm_nonneg _) (by norm_num : 0≤(1:ℝ))).mp
  rw [Complex.sq_norm,Complex.normSq_apply]
  norm_num only [Complex.add_re,Complex.ofReal_re,Complex.mul_re,Complex.ofReal_im,
    Complex.I_re,Complex.I_im,Complex.add_im,Complex.mul_im,mul_zero,zero_mul,sub_zero,
    add_zero,zero_add,mul_one]
  nlinarith
lemma evenOffset_distances {v : ℂ} (hv : ‖v‖=1) {t : ℝ} (ht : |t|<2) :
    ‖evenOffset v t‖=1 ∧ ‖evenOffset v t-(t:ℂ)*(Complex.I*v)‖=1 := by
  constructor
  · rw [evenOffset,norm_mul,norm_even_wing ht,hv,mul_one]
  · have he : evenOffset v t-(t:ℂ)*(Complex.I*v)=evenOffset v (-t) := by
      simp only [evenOffset,neg_sq,neg_div,Complex.ofReal_neg,Complex.ofReal_div,Complex.ofReal_ofNat]
      ring
    rw [he,evenOffset,norm_mul,norm_even_wing (by simpa only [abs_neg] using ht),hv,mul_one]
@[fun_prop] lemma continuous_evenOffset (v : ℂ) : Continuous (evenOffset v) := by
  unfold evenOffset
  fun_prop
lemma evenOffset_zero (v : ℂ) : evenOffset v 0=v := by simp [evenOffset]
def transverseDet (v w : ℂ) : ℝ :=
  (Complex.I*v).re*(Complex.I*w).im-(Complex.I*w).re*(Complex.I*v).im
def transverseFirst (v w h : ℂ) : ℝ :=
  (h.re*(Complex.I*w).im-(Complex.I*w).re*h.im)/transverseDet v w
def transverseSecond (v w h : ℂ) : ℝ :=
  ((Complex.I*v).re*h.im-h.re*(Complex.I*v).im)/transverseDet v w
lemma transverse_decompose {v w : ℂ} (hd : transverseDet v w≠0) (h : ℂ) :
    (transverseFirst v w h : ℂ)*(Complex.I*v)+
      (transverseSecond v w h : ℂ)*(Complex.I*w)=h := by
  apply Complex.ext <;>
    simp only [Complex.add_re,Complex.mul_re,Complex.ofReal_re,Complex.ofReal_im,
      Complex.add_im,Complex.mul_im,zero_mul,sub_zero,add_zero,
      transverseFirst,transverseSecond] <;>
    field_simp <;> dsimp [transverseDet] <;>
    simp only [Complex.mul_re,Complex.mul_im,Complex.I_re,Complex.I_im,zero_mul,one_mul,zero_sub,zero_add] <;> ring
@[fun_prop] lemma continuous_transverseFirst (v w : ℂ) : Continuous (transverseFirst v w) := by
  unfold transverseFirst
  fun_prop
@[fun_prop] lemma continuous_transverseSecond (v w : ℂ) : Continuous (transverseSecond v w) := by
  unfold transverseSecond
  fun_prop
lemma transverseFirst_zero (v w : ℂ) : transverseFirst v w 0=0 := by simp [transverseFirst]
lemma transverseSecond_zero (v w : ℂ) : transverseSecond v w 0=0 := by simp [transverseSecond]
def evenPath (v w h : ℂ) : Fin 5 → ℂ := ![0,
  evenOffset v (transverseFirst v w h),
  (transverseFirst v w h : ℂ)*(Complex.I*v),
  (transverseFirst v w h : ℂ)*(Complex.I*v)+evenOffset w (transverseSecond v w h),h]
lemma evenPath_edges {v w h : ℂ} (hv : ‖v‖=1) (hw : ‖w‖=1)
    (hd : transverseDet v w≠0) (h₁ : |transverseFirst v w h|<2)
    (h₂ : |transverseSecond v w h|<2) :
    ∀i : Fin 4, ‖evenPath v w h i.castSucc-evenPath v w h i.succ‖=1 := by
  have he₁ := evenOffset_distances hv h₁
  have he₂ := evenOffset_distances hw h₂
  have hdec := transverse_decompose hd h
  intro i
  fin_cases i
  · change ‖0-evenOffset v (transverseFirst v w h)‖=1
    simpa only [zero_sub,norm_neg] using he₁.1
  · exact he₁.2
  · change ‖(transverseFirst v w h : ℂ)*(Complex.I*v)-
        ((transverseFirst v w h : ℂ)*(Complex.I*v)+evenOffset w (transverseSecond v w h))‖=1
    simpa only [sub_add_cancel_left,norm_neg] using he₂.1
  · change ‖(transverseFirst v w h : ℂ)*(Complex.I*v)+evenOffset w (transverseSecond v w h)-h‖=1
    calc
      _ = ‖evenOffset w (transverseSecond v w h)-(transverseSecond v w h : ℂ)*(Complex.I*w)‖ :=
        congrArg norm (by linear_combination hdec)
      _ = 1 := he₂.2
/-- Actual four-unit-edge paths stay inside the prescribed two open sets for
all small starting-point and displacement perturbations. -/
lemma evenPath_local {U V : Set ℂ} (hU : IsOpen U) (hV : IsOpen V)
    {p v w : ℂ} (hp : p∈U) (hpv : p+v∈V) (hpw : p+w∈V) :
    ∃r>0,∃δ>0,∀q h : ℂ,q∈Metric.ball p r → ‖h‖<δ →
      |transverseFirst v w h|<2 ∧ |transverseSecond v w h|<2 ∧
      (∀i : Fin 5,(q+evenPath v w h i)∈if i.val%2=0 then U else V) := by
  let P : ℂ × ℂ → Prop := fun z => |transverseFirst v w z.2|<2 ∧
    |transverseSecond v w z.2|<2 ∧
    (∀i : Fin 5,(z.1+evenPath v w z.2 i)∈if i.val%2=0 then U else V)
  have hm : ∀ᶠz in 𝓝 (p,(0:ℂ)),P z := by
    have ha : ∀ᶠz : ℂ × ℂ in 𝓝 (p,(0:ℂ)), |transverseFirst v w z.2|<2 := by
      apply ((continuous_transverseFirst v w).comp continuous_snd).abs.continuousAt.eventually_lt continuousAt_const
      simp [transverseFirst_zero]
    have hb : ∀ᶠz : ℂ × ℂ in 𝓝 (p,(0:ℂ)), |transverseSecond v w z.2|<2 := by
      apply ((continuous_transverseSecond v w).comp continuous_snd).abs.continuousAt.eventually_lt continuousAt_const
      simp [transverseSecond_zero]
    have hc (i : Fin 5) : ∀ᶠz : ℂ × ℂ in 𝓝 (p,(0:ℂ)),
        (z.1+evenPath v w z.2 i)∈if i.val%2=0 then U else V := by
      have hco : Continuous (fun z : ℂ × ℂ => z.1+evenPath v w z.2 i) := by
        fin_cases i <;> dsimp [evenPath] <;> fun_prop
      apply hco.continuousAt.eventually
      fin_cases i <;> norm_num [evenPath,transverseFirst_zero,transverseSecond_zero,evenOffset_zero]
      · exact hU.mem_nhds hp
      · exact hV.mem_nhds hpv
      · exact hU.mem_nhds hp
      · exact hV.mem_nhds hpw
      · exact hU.mem_nhds hp
    exact ha.and (hb.and (eventually_all.mpr hc))
  obtain ⟨ε,hε,hb⟩ := Metric.mem_nhds_iff.mp hm
  refine ⟨ε,hε,ε,hε,?_⟩
  intro q h hq hh
  exact hb (show (q,h)∈Metric.ball (p,(0:ℂ)) ε by
    simpa only [Metric.mem_ball,Prod.dist_eq,dist_zero_right,max_lt_iff] using And.intro hq hh)
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology MeasureTheory
namespace EuclideanFiveColor
/-- Local invariance for every sufficiently small fixed translation forces
local essential constancy. This is the Fubini/shear step of angular-binary-local. -/
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology MeasureTheory
namespace EuclideanFiveColor
/-- Local essential constancy inside two-color open regions, from the source's
actual four-edge paths. The directions are genuine unit directions landing in V. -/
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology
namespace EuclideanFiveColor
/-- An open set meeting a unit circle contains two nonparallel unit directions
from its center. No regularity of the color classes is involved. -/
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology
namespace EuclideanFiveColor
/-- The unit circle from one endpoint penetrates either prescribed radial side
near its equilateral neighbor. This is the constructive version of the source IFT step. -/
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology
namespace EuclideanFiveColor
/-- Arbitrarily small connected polar boxes on either side of a unit circle. -/
/-- A polar box contains a complete one-sided radial strip, not just selected rays. -/
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology MeasureTheory
namespace EuclideanFiveColor
/-- Points having a fixed essential color on some ambient neighborhood. -/
/-- Local essential constancy on a connected set has one global essential value.
The connected set need not be open, which permits polar product images directly. -/
end EuclideanFiveColor
end

end OAI
