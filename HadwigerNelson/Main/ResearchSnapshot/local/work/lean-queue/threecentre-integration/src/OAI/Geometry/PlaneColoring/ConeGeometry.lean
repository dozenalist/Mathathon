import OAI.Geometry.PlaneColoring.AngularBoundary
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Inverse

namespace OAI.EuclideanFiveColor

noncomputable section
open Set Filter Topology MeasureTheory

/-- An angularly parametrized outer strip, with one width at each angle. -/
def OuterAngularStrips (x : ℂ) (W : Set ℂ) (I : Set ℝ) : Prop :=
  ∀ θ ∈ I, ∃ δ > 0, ∀ β : ℝ, |β-θ| < δ →
    ∀ r : ℝ, 1 < r → r < 1+δ → x+(r:ℂ)*(Circle.exp β : ℂ) ∈ W

/-- The cosine law in the coordinates used by the outer-strip hypothesis. -/
lemma cone_polar_distance_sq (x : ℂ) (r s θ β : ℝ) :
    ‖(x+(r:ℂ)*(Circle.exp θ : ℂ))-
      (x+(s:ℂ)*(Circle.exp β : ℂ))‖^2 =
      r^2+s^2-2*r*s*Real.cos (θ-β) := by
  rw [add_sub_add_left_eq_sub, Complex.sq_norm, Complex.normSq_apply]
  simp only [Circle.coe_exp, Complex.exp_mul_I, ← Complex.ofReal_cos,
    ← Complex.ofReal_sin, Complex.sub_re, Complex.sub_im,
    Complex.add_re, Complex.add_im, Complex.mul_re, Complex.mul_im,
    Complex.ofReal_re, Complex.ofReal_im, Complex.I_re, Complex.I_im,
    mul_zero, zero_mul, sub_zero, add_zero, zero_add, mul_one]
  calc
    _ = r^2*(Real.cos θ^2+Real.sin θ^2) +
        s^2*(Real.cos β^2+Real.sin β^2) -
        2*r*s*(Real.cos θ*Real.cos β+Real.sin θ*Real.sin β) := by ring
    _ = _ := by rw [Real.cos_sq_add_sin_sq, Real.cos_sq_add_sin_sq, Real.cos_sub]; ring

/-- Cosine of the angle for an intersection of circles of radii `s` and `1`,
whose centers are at distance `r`. -/
def coneRadialCos (r s : ℝ) : ℝ := (r^2+s^2-1)/(2*r*s)

lemma coneRadialCos_one {r : ℝ} (hr : r ≠ 0) : coneRadialCos r 1 = r/2 := by
  dsimp [coneRadialCos]
  field_simp [hr]
  ring

lemma continuousAt_coneRadialCos_one {r : ℝ} (hr : r ≠ 0) :
    ContinuousAt (coneRadialCos r) 1 := by
  unfold coneRadialCos
  fun_prop (disch := simp [hr])

def coneNeighbourAngle (r θ : ℝ) (b : Bool) (s : ℝ) : ℝ :=
  if b then θ-Real.arccos (coneRadialCos r s)
  else θ+Real.arccos (coneRadialCos r s)

lemma continuousAt_coneNeighbourAngle_one {r : ℝ} (hr : r ≠ 0)
    (θ : ℝ) (b : Bool) : ContinuousAt (coneNeighbourAngle r θ b) 1 := by
  have ha := Real.continuous_arccos.continuousAt.comp
    (continuousAt_coneRadialCos_one hr)
  cases b
  · exact continuousAt_const.add ha
  · exact continuousAt_const.sub ha

/-- Exact unit distance along the radial circle-intersection family. -/
lemma coneNeighbourAngle_unit {r s : ℝ} (hr : r ≠ 0) (hs : s ≠ 0)
    (hg : -1 ≤ coneRadialCos r s ∧ coneRadialCos r s ≤ 1)
    (x : ℂ) (θ : ℝ) (b : Bool) :
    ‖(x+(r:ℂ)*(Circle.exp θ : ℂ))-
      (x+(s:ℂ)*(Circle.exp (coneNeighbourAngle r θ b s) : ℂ))‖ = 1 := by
  apply (sq_eq_sq₀ (norm_nonneg _) (by norm_num : 0 ≤ (1:ℝ))).mp
  rw [cone_polar_distance_sq]
  have hcos : Real.cos (θ-coneNeighbourAngle r θ b s) = coneRadialCos r s := by
    cases b
    · simpa only [coneNeighbourAngle, Bool.false_eq_true, ite_false,
        sub_add_cancel_left, Real.cos_neg] using Real.cos_arccos hg.1 hg.2
    · simpa only [coneNeighbourAngle, ite_true, sub_sub_cancel] using
        Real.cos_arccos hg.1 hg.2
  rw [hcos]
  dsimp [coneRadialCos]
  field_simp [hr, hs]
  ring

/-- The continuous radial family enters any prescribed OUTER angular strip.
The conclusion is an actual unit neighbour in the ambient set, not a limit point. -/
lemma outer_strip_actual_unit_neighbour {x : ℂ} {W : Set ℂ}
    {r θ δ : ℝ} (hr1 : 1 < r) (hr2 : r < 2) (hδ : 0 < δ) (b : Bool)
    (hstrip : ∀ β : ℝ, |β-coneNeighbourAngle r θ b 1| < δ →
      ∀ s : ℝ, 1 < s → s < 1+δ → x+(s:ℂ)*(Circle.exp β : ℂ) ∈ W) :
    ∃ q ∈ W, ‖(x+(r:ℂ)*(Circle.exp θ : ℂ))-q‖ = 1 := by
  have hr : r ≠ 0 := by linarith
  have hg1 : -1 < coneRadialCos r 1 ∧ coneRadialCos r 1 < 1 := by
    rw [coneRadialCos_one hr]
    constructor <;> linarith
  have hgc := continuousAt_coneRadialCos_one hr
  have hbc := continuousAt_coneNeighbourAngle_one hr θ b
  have hn : ∀ᶠ s in 𝓝 (1:ℝ),
      -1 < coneRadialCos r s ∧ coneRadialCos r s < 1 ∧
      |coneNeighbourAngle r θ b s-coneNeighbourAngle r θ b 1| < δ ∧ s < 1+δ := by
    have ha := continuousAt_const.eventually_lt hgc hg1.1
    have hb := hgc.eventually_lt continuousAt_const hg1.2
    have hdiff : ContinuousAt (fun s : ℝ =>
        coneNeighbourAngle r θ b s-coneNeighbourAngle r θ b 1) 1 :=
      hbc.sub continuousAt_const
    have hd : ∀ᶠ s in 𝓝 (1:ℝ),
        |coneNeighbourAngle r θ b s-coneNeighbourAngle r θ b 1| < δ :=
      hdiff.abs.eventually_lt_const (by simpa only [sub_self, abs_zero] using hδ)
    exact ha.and (hb.and (hd.and (eventually_lt_nhds (by linarith : (1:ℝ) < 1+δ))))
  obtain ⟨s,hs,hs1⟩ := ((hn.filter_mono nhdsWithin_le_nhds).and
    (self_mem_nhdsWithin : ∀ᶠ s in 𝓝[>] (1:ℝ), s ∈ Ioi 1)).exists
  refine ⟨x+(s:ℂ)*(Circle.exp (coneNeighbourAngle r θ b s) : ℂ),
    hstrip _ hs.2.2.1 s hs1 hs.2.2.2, ?_⟩
  exact coneNeighbourAngle_unit hr (by linarith) ⟨hs.1.le,hs.2.1.le⟩ x θ b

/-- Strict radius greater than one is what keeps the neighbour inside the
OPEN 120-degree arc even when the approach cone has its closed endpoints. -/
lemma outer120_point_has_unit_neighbour {x : ℂ} {W : Set ℂ} {φ r θ : ℝ}
    (hstrip : OuterAngularStrips x W (Ioo (φ-Real.pi/3) (φ+Real.pi/3)))
    (hr1 : 1 < r) (hr2 : r < 2)
    (hθ : θ ∈ Icc (φ-Real.pi/6) (φ+Real.pi/6)) :
    ∃ q ∈ W, ‖(x+(r:ℂ)*(Circle.exp θ : ℂ))-q‖ = 1 := by
  have hr : r ≠ 0 := by linarith
  have ha0 : 0 < Real.arccos (r/2) := Real.arccos_pos.mpr (by linarith)
  have ha3 : Real.arccos (r/2) < Real.pi/3 := by
    have hh := Real.arccos_lt_arccos (by norm_num : (-1:ℝ) ≤ 1/2)
      (by linarith : (1:ℝ)/2 < r/2) (by linarith : r/2 ≤ 1)
    have he : Real.arccos ((1:ℝ)/2) = Real.pi/3 := by
      rw [← Real.cos_pi_div_three]
      exact Real.arccos_cos (by positivity) (by linarith [Real.pi_pos])
    simpa only [he] using hh
  by_cases hθφ : φ ≤ θ
  · have hb : coneNeighbourAngle r θ true 1 ∈ Ioo (φ-Real.pi/3) (φ+Real.pi/3) := by
      simp only [coneNeighbourAngle, ite_true, coneRadialCos_one hr]
      constructor <;> linarith [hθ.1,hθ.2,Real.pi_pos]
    obtain ⟨δ,hδ,hd⟩ := hstrip _ hb
    exact outer_strip_actual_unit_neighbour hr1 hr2 hδ true hd
  · have hb : coneNeighbourAngle r θ false 1 ∈ Ioo (φ-Real.pi/3) (φ+Real.pi/3) := by
      simp only [coneNeighbourAngle, Bool.false_eq_true, ite_false, coneRadialCos_one hr]
      constructor <;> linarith [hθ.1,hθ.2,Real.pi_pos]
    obtain ⟨δ,hδ,hd⟩ := hstrip _ hb
    exact outer_strip_actual_unit_neighbour hr1 hr2 hδ false hd

/-- Compactness supplies a single radius on any compact subarc. No lower
bound on strip widths at the endpoints of the original open arc is assumed. -/
lemma outerAngularStrips_compact_radius {x : ℂ} {W : Set ℂ} {I J : Set ℝ}
    (hstrip : OuterAngularStrips x W I) (hJ : IsCompact J) (hJI : J ⊆ I) :
    ∃ r : ℝ, 1 < r ∧ r < 2 ∧ ∀ θ ∈ J, x+(r:ℂ)*(Circle.exp θ : ℂ) ∈ W := by
  classical
  have hex (t : J) := hstrip t.1 (hJI t.2)
  choose d hd hs using hex
  obtain ⟨E,hE⟩ := hJ.elim_finite_subcover (fun t : J => Metric.ball t.1 (d t))
    (fun _ => Metric.isOpen_ball) (fun t ht =>
      mem_iUnion.mpr ⟨⟨t,ht⟩,Metric.mem_ball_self (hd ⟨t,ht⟩)⟩)
  obtain ⟨δ,hδ,hδ1,hδd⟩ := finite_positive_lower_bound E d (fun t _ => hd t)
  refine ⟨1+δ/2,by linarith,by linarith,?_⟩
  intro θ hθ
  obtain ⟨t,ht,hθt⟩ := mem_iUnion₂.mp (hE hθ)
  apply hs t θ (by simpa only [Metric.mem_ball, Real.dist_eq] using hθt)
    (1+δ/2) (by linarith)
  linarith [hδd t ht]

end
end OAI.EuclideanFiveColor
