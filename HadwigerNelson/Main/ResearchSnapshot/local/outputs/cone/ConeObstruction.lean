import OAI.Geometry.PlaneColoring.ConeGeometry

namespace OAI.EuclideanFiveColor

noncomputable section
open Set Filter Topology MeasureTheory
open scoped RealInnerProductSpace

/-- Two points of the same ambient essential colour cannot be a unit pair.
Only two fixed translation pullbacks of conull sets are used. -/
lemma essentialLocalSet_no_unit_pair {k : ℕ} {c : ℂ → Fin k}
    (hc : Measurable c) (hw : WeakColoring k c) {i : Fin k} {p q : ℂ}
    (hp : p ∈ essentialLocalSet c i) (hq : q ∈ essentialLocalSet c i)
    (hpq : ‖p-q‖ = 1) : False := by
  obtain ⟨U,hU,hpU,hUc⟩ := hp
  obtain ⟨V,hV,hqV,hVc⟩ := hq
  let T : Set ℂ := (fun u => u+p) ⁻¹' U ∩ (fun u => u+q) ⁻¹' V
  have hT : IsOpen T := (hU.preimage (continuous_id.add continuous_const)).inter
    (hV.preimage (continuous_id.add continuous_const))
  have h0 : (0:ℂ) ∈ T := by simpa only [T, mem_inter_iff, mem_preimage, zero_add] using And.intro hpU hqV
  have hpos := hT.measure_pos (volume : Measure ℂ) ⟨0,h0⟩
  have hu := (measurePreserving_add_right volume p).quasiMeasurePreserving.ae hUc
  have hv := (measurePreserving_add_right volume q).quasiMeasurePreserving.ae hVc
  have hn := ae_translated_unit_pair hc hw hpq
  obtain ⟨u,huT,huv⟩ := Measure.exists_mem_of_measure_ne_zero_of_ae hpos.ne'
    (ae_restrict_of_ae (hu.and (hv.and hn)))
  exact huv.2.2 ((huv.1 huT.1).trans (huv.2.1 huT.2).symm)

/-- Source rigidity turns pointwise geometric unit-neighbour existence into
a contradiction on any connected subset containing a unit pair. -/
lemma binary_connected_unit_neighbour_obstruction {k : ℕ} {c : ℂ → Fin k}
    (hc : Measurable c) (hw : WeakColoring k c) {a b : Fin k} {W S : Set ℂ}
    (hW : IsOpen W) (hWc : ∀ᵐ z : ℂ ∂volume, z ∈ W → c z = a ∨ c z = b)
    (hS : IsConnected S) (hSW : S ⊆ W)
    (hnear : ∀ p ∈ S, ∃ q ∈ W, ‖p-q‖ = 1)
    (hpair : ∃ p ∈ S, ∃ q ∈ S, ‖p-q‖ = 1) : False := by
  obtain ⟨i,hi,_⟩ := connected_local_ae_constant hS (fun p hp => by
    obtain ⟨q,hq,hpq⟩ := hnear p hp
    have hv : ‖q-p‖ = 1 := by simpa only [norm_sub_rev] using hpq
    have hpv : p+(q-p) ∈ W := by simpa only [show p+(q-p)=q by ring] using hq
    obtain ⟨w,hpw,hw',hd⟩ := open_two_unit_directions hW hv hpv
    obtain ⟨ε,hε,j,hj⟩ := binary_open_local_rigidity hc hw hW hW hWc hWc
      (hSW hp) hpv hpw hv hw' hd
    exact ⟨j,Metric.ball p ε,Metric.isOpen_ball,Metric.mem_ball_self hε,hj⟩)
  obtain ⟨p,hp,q,hq,hpq⟩ := hpair
  exact essentialLocalSet_no_unit_pair hc hw (hi hp) (hi hq) hpq

/-- OA120: an open region containing an outer strip at every point of an
open 120-degree unit-circle arc cannot be essentially two-coloured.
There is no trace-palette or binary-center hypothesis. -/
theorem outer120_binary_impossible {k : ℕ} {c : ℂ → Fin k}
    (hc : Measurable c) (hw : WeakColoring k c) {a b : Fin k}
    {x : ℂ} {φ : ℝ} {W : Set ℂ} (hW : IsOpen W)
    (hWc : ∀ᵐ z : ℂ ∂volume, z ∈ W → c z = a ∨ c z = b)
    (hstrip : OuterAngularStrips x W (Ioo (φ-Real.pi/3) (φ+Real.pi/3))) : False := by
  let J : Set ℝ := Icc (φ-Real.pi/6) (φ+Real.pi/6)
  have hJ : IsConnected J := isConnected_Icc (by linarith [Real.pi_pos])
  obtain ⟨r,hr1,hr2,hrW⟩ := outerAngularStrips_compact_radius hstrip isCompact_Icc
    (show J ⊆ Ioo (φ-Real.pi/3) (φ+Real.pi/3) from fun θ hθ =>
      ⟨by dsimp [J] at hθ; linarith [hθ.1,Real.pi_pos],
       by dsimp [J] at hθ; linarith [hθ.2,Real.pi_pos]⟩)
  let F : ℝ → ℂ := fun θ => x+(r:ℂ)*(Circle.exp θ : ℂ)
  let S : Set ℂ := F '' J
  have hF : Continuous F := by fun_prop
  have hS : IsConnected S := hJ.image F hF.continuousOn
  have hSW : S ⊆ W := by
    rintro p ⟨θ,hθ,rfl⟩
    exact hrW θ hθ
  have hnear : ∀ p ∈ S, ∃ q ∈ W, ‖p-q‖ = 1 := by
    rintro p ⟨θ,hθ,rfl⟩
    exact outer120_point_has_unit_neighbour hstrip hr1 hr2 hθ
  let p := F (φ-Real.pi/6)
  let q := F (φ+Real.pi/6)
  have hp : p ∈ S := ⟨φ-Real.pi/6,⟨le_rfl,by linarith [Real.pi_pos]⟩,rfl⟩
  have hq : q ∈ S := ⟨φ+Real.pi/6,⟨by linarith [Real.pi_pos],le_rfl⟩,rfl⟩
  have hpq : ‖p-q‖ = r := by
    apply (sq_eq_sq₀ (norm_nonneg _) (by linarith : 0 ≤ r)).mp
    change ‖(x+(r:ℂ)*(Circle.exp (φ-Real.pi/6) : ℂ))-
      (x+(r:ℂ)*(Circle.exp (φ+Real.pi/6) : ℂ))‖^2 = r^2
    rw [cone_polar_distance_sq,
      show (φ-Real.pi/6)-(φ+Real.pi/6) = -(Real.pi/3) by ring,
      Real.cos_neg,Real.cos_pi_div_three]
    ring
  have hnorm : Continuous (fun z : ℂ => ‖p-z‖) := by fun_prop
  obtain ⟨q',hq',hpq'⟩ := hS.isPreconnected.intermediate_value hp hq hnorm.continuousOn
    (show (1:ℝ) ∈ Icc ‖p-p‖ ‖p-q‖ from ⟨by simp,by rw [hpq]; exact hr1.le⟩)
  exact binary_connected_unit_neighbour_obstruction hc hw hW hWc hS hSW hnear
    ⟨p,hp,q',hq',hpq'⟩

lemma cone_exp_inner (θ α : ℝ) :
    ⟪(Circle.exp θ : ℂ),(Circle.exp α : ℂ)⟫ = Real.cos (θ-α) := by
  rw [Complex.inner]
  simp only [Circle.coe_exp,Complex.exp_mul_I,← Complex.ofReal_cos,
    ← Complex.ofReal_sin,Complex.mul_re,Complex.conj_re,Complex.conj_im,
    Complex.add_re,Complex.add_im,Complex.mul_im,Complex.ofReal_re,
    Complex.ofReal_im,Complex.I_re,Complex.I_im,Real.cos_sub]
  ring

/-- Every signed direction in a CLOSED sixty-degree cone supplies the same
outer side throughout the OPEN common 120-degree arc. -/
lemma closed60_continua_outer_strips {ι : Type*} [Fintype ι]
    {x : ℂ} {φ : ℝ} {K : ι → Set ℂ} {α : ι → ℝ}
    (hK : ∀ i, ApproachingContinuum x (K i) (Circle.exp (α i) : ℂ))
    (hα : ∀ i, α i ∈ Icc (φ-Real.pi/6) (φ+Real.pi/6)) :
    OuterAngularStrips x (⋂ i,Straddle (K i)) (Ioo (φ-Real.pi/3) (φ+Real.pi/3)) := by
  classical
  intro θ hθ
  have hex (i : ι) := (hK i).outer_strip (Circle.norm_coe (Circle.exp θ))
    (show 0 < ⟪(Circle.exp θ : ℂ),(Circle.exp (α i) : ℂ)⟫ from by
      rw [cone_exp_inner]
      exact Real.cos_pos_of_mem_Ioo ⟨by linarith [(hα i).2,hθ.1],
        by linarith [(hα i).1,hθ.2]⟩)
  choose d hd hs using hex
  obtain ⟨δ,hδ,_,hδd⟩ := finite_positive_lower_bound Finset.univ d (fun i _ => hd i)
  have hcont : Continuous (fun β : ℝ => dist (Circle.exp β : ℂ) (Circle.exp θ : ℂ)) := by fun_prop
  have hn : ∀ᶠ β in 𝓝 θ, dist (Circle.exp β : ℂ) (Circle.exp θ : ℂ) < δ :=
    hcont.continuousAt.eventually_lt_const (by simpa only [dist_self] using hδ)
  obtain ⟨η,hη,hηs⟩ := Metric.mem_nhds_iff.mp hn
  refine ⟨min δ η,lt_min hδ hη,?_⟩
  intro β hβ r hr hrδ
  apply mem_iInter.mpr
  intro i
  have hβη : |β-θ| < η := hβ.trans_le (min_le_right δ η)
  have hβball : β ∈ Metric.ball θ η := by
    simpa only [Metric.mem_ball,Real.dist_eq] using hβη
  have hdist : dist (Circle.exp β : ℂ) (Circle.exp θ : ℂ) < d i :=
    (hηs hβball).trans_le (hδd i (Finset.mem_univ _))
  have hbound : r < 1+d i := by linarith [min_le_left δ η,hδd i (Finset.mem_univ _)]
  exact hs i (Circle.exp β : ℂ) (Circle.norm_coe _) hdist r hr hbound

/-- CC60 in its direct consumer form: the residual labels cannot be covered
by a fixed pair, including the possibility that the pair repeats a label. -/
theorem closed60_exclusions_not_binary {k : ℕ} {c : ℂ → Fin k}
    (hc : Measurable c) (hw : WeakColoring k c)
    {ι : Type*} [Fintype ι] {x : ℂ} {φ : ℝ}
    {K : ι → Set ℂ} {α : ι → ℝ} (F : ι → Finset (Fin k))
    (hK : ∀ i, ApproachingContinuum x (K i) (Circle.exp (α i) : ℂ))
    (hα : ∀ i, α i ∈ Icc (φ-Real.pi/6) (φ+Real.pi/6))
    (hexcl : ∀ i, ∀ j ∈ F i, Disjoint (spatialSupport c j) (Straddle (K i)))
    {a b : Fin k} (hres : ∀ j : Fin k, (∀ i, j ∉ F i) → j = a ∨ j = b) : False := by
  apply outer120_binary_impossible hc hw
    (isOpen_iInter_of_finite fun i => straddle_isOpen (K i))
    (W := ⋂ i,Straddle (K i)) (x := x) (φ := φ)
  · filter_upwards [finite_support_exclusion_ae c hc K F hexcl] with z hz hzW
    exact hres (c z) (fun i => hz i (mem_iInter.mp hzW i))
  · exact closed60_continua_outer_strips hK hα

/-- The accepted generic finite-continuum theorem: at least three colours
remain after all exclusions in a closed sixty-degree signed cone. -/
theorem closed60_exclusions_three_le {k : ℕ} {c : ℂ → Fin k}
    (hc : Measurable c) (hw : WeakColoring k c)
    {ι : Type*} [Fintype ι] {x : ℂ} {φ : ℝ}
    {K : ι → Set ℂ} {α : ι → ℝ} (F : ι → Finset (Fin k))
    (hK : ∀ i, ApproachingContinuum x (K i) (Circle.exp (α i) : ℂ))
    (hα : ∀ i, α i ∈ Icc (φ-Real.pi/6) (φ+Real.pi/6))
    (hexcl : ∀ i, ∀ j ∈ F i, Disjoint (spatialSupport c j) (Straddle (K i))) :
    3 ≤ (Finset.univ.filter (fun j : Fin k => ∀ i, j ∉ F i)).card := by
  classical
  let R := Finset.univ.filter (fun j : Fin k => ∀ i, j ∉ F i)
  have hR (j : Fin k) : j ∈ R ↔ ∀ i, j ∉ F i := by simp [R]
  by_contra h
  have hle : R.card ≤ 2 := by dsimp [R]; omega
  have hpair : ∃ a b : Fin k, ∀ j ∈ R, j = a ∨ j = b := by
    by_cases h2 : R.card = 2
    · obtain ⟨a,b,_,hab⟩ := Finset.card_eq_two.mp h2
      exact ⟨a,b,fun j hj => by simpa only [hab,Finset.mem_insert,Finset.mem_singleton] using hj⟩
    · have h1 : R.card ≤ 1 := by omega
      by_cases hne : R.Nonempty
      · obtain ⟨a,ha⟩ := hne
        exact ⟨a,a,fun j hj => Or.inl (Finset.card_le_one.mp h1 j hj a ha)⟩
      · exact ⟨c x,c x,fun j hj => (hne ⟨j,hj⟩).elim⟩
  obtain ⟨a,b,hab⟩ := hpair
  exact closed60_exclusions_not_binary hc hw F hK hα hexcl
    (fun j hj => hab j ((hR j).mpr hj))

end
end OAI.EuclideanFiveColor
