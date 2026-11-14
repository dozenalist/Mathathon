import OAI.Geometry.PlaneColoring.PlanarCovers

noncomputable section
open Set Metric MeasureTheory
open scoped Classical
namespace OAI
namespace PlanarCover

lemma hit_center_gen {F : ℂ → ℂ} {y : ℂ} {c d : ℝ} (hd : 0 ≤ d) (hdc : d < c)
    (hc : ContinuousOn F (Metric.ball y c))
    (hb : ∀ z ∈ Metric.ball y c, ‖F z - z‖ ≤ d) :
    y ∈ F '' Metric.ball y c := by
  have hcpos : 0 < c := lt_of_le_of_lt hd hdc
  by_contra hn
  have hzero : 0 ∉ (fun z => F z - y) '' Metric.ball y c := by
    rintro ⟨z, hz, he⟩
    exact hn ⟨z, hz, sub_eq_zero.mp he⟩
  obtain ⟨L, hLc, hL⟩ := Complex.exists_continuousOn_eqOn_exp_comp
    (ball_simplyConnected y hcpos) Metric.isOpen_ball
    (hc.sub continuousOn_const) hzero
  set ρ : ℝ := (d + c) / 2 with hρdef
  have hdρ : d < ρ := by simp only [hρdef]; linarith
  have hρc : ρ < c := by simp only [hρdef]; linarith
  have hρpos : 0 < ρ := lt_of_le_of_lt hd hdρ
  let e : ℝ → ℂ := fun t => Complex.exp (t * Complex.I)
  have ec : Continuous e := by fun_prop
  have en (t : ℝ) : ‖e t‖ = 1 := by simp [e, Complex.norm_exp]
  let γ : ℝ → ℂ := fun t => y + ρ * e t
  have γc : Continuous γ := by fun_prop
  have γmem (t : ℝ) : γ t ∈ Metric.ball y c := by
    rw [Metric.mem_ball, dist_eq_norm]
    have h1 : γ t - y = (ρ : ℂ) * e t := by simp [γ]
    rw [h1, norm_mul, en t, mul_one, Complex.norm_real, Real.norm_eq_abs, abs_of_pos hρpos]
    exact hρc
  let H : ℝ → ℂ := fun t => (F (γ t) - y) / e t
  have Hc : Continuous H :=
    (hc.comp_continuous γc γmem).sub continuous_const |>.div ec (fun t => Complex.exp_ne_zero _)
  have Hnear (t : ℝ) : ‖H t - ρ‖ ≤ d := by
    have he : e t ≠ 0 := Complex.exp_ne_zero _
    have h : H t - ρ = (F (γ t) - γ t) / e t := by
      dsimp only [H, γ]; field_simp; ring
    rw [h, norm_div, en t, div_one]
    exact hb _ (γmem t)
  have Hpos (t : ℝ) : 0 < (H t).re := by
    have h1 : |(H t - ρ).re| ≤ d := (Complex.abs_re_le_norm (H t - ρ)).trans (Hnear t)
    have h2 : -d ≤ (H t - ρ).re := (abs_le.mp h1).1
    have h3 : (H t).re = (H t - ρ).re + ρ := by simp [Complex.sub_re]
    rw [h3]; linarith
  have Hslit (t : ℝ) : H t ∈ Complex.slitPlane := Or.inl (Hpos t)
  have logHc : Continuous fun t => Complex.log (H t) := Hc.clog Hslit
  let Φ : ℝ → ℂ := fun t => L (γ t) - Complex.log (H t) - t * Complex.I
  have Φc : Continuous Φ :=
    ((hLc.comp_continuous γc γmem).sub logHc).sub (by fun_prop)
  have Φe (t : ℝ) : Complex.exp (Φ t) = 1 := by
    have hH : H t ≠ 0 := fun hz => by have := Hpos t; simp [hz] at this
    have hLe : Complex.exp (L (γ t)) = F (γ t) - y := hL (γmem t)
    simp only [Φ, Complex.exp_sub, Complex.exp_log hH, hLe]
    change (F (γ t) - y) / ((F (γ t) - y) / e t) / e t = 1
    have hF : F (γ t) - y ≠ 0 := fun hz => hzero ⟨γ t, γmem t, hz⟩
    have he : e t ≠ 0 := Complex.exp_ne_zero _
    field_simp
  have hconst : Φ 0 = Φ (2 * Real.pi) :=
    Complex.isCoveringMap_exp.constOn_of_comp isPreconnected_univ Φc.continuousOn
      (fun a _ b _ => Subtype.ext ((Φe a).trans (Φe b).symm)) (mem_univ _) (mem_univ _)
  have e0 : e 0 = 1 := by simp [e]
  have e2 : e (2 * Real.pi) = 1 := by simp [e, Complex.exp_two_pi_mul_I]
  have γeq : γ (2 * Real.pi) = γ 0 := by dsimp only [γ]; rw [e0, e2]
  have Heq : H (2 * Real.pi) = H 0 := by dsimp only [H]; rw [γeq, e0, e2]
  dsimp only [Φ] at hconst
  rw [γeq, Heq] at hconst
  have hi := congrArg Complex.im hconst
  norm_num at hi
  nlinarith [Real.pi_pos]

lemma hit_center_subtype_gen {Q : Set ℂ} {y : ℂ} {c d : ℝ} (hd : 0 ≤ d) (hdc : d < c)
    (hQ : Metric.ball y c ⊆ Q) {F : Q → ℂ} (hF : Continuous F)
    (hb : ∀ z, ‖F z - z.val‖ ≤ d) : y ∈ Set.range F := by
  classical
  let g : ℂ → ℂ := fun z => if hz : z ∈ Q then F ⟨z, hz⟩ else 0
  have ge (z : ℂ) (hz : z ∈ Q) : g z = F ⟨z, hz⟩ := dite_eq_left hz
  have hgc : ContinuousOn g (Metric.ball y c) := by
    rw [continuousOn_iff_continuous_domRestrict]
    have hh := hF.comp (continuous_subtype_val.subtype_mk (fun z : Metric.ball y c => hQ z.property))
    convert hh using 1
    ext z
    exact ge _ (hQ z.property)
  obtain ⟨z, hz, he⟩ := hit_center_gen hd hdc hgc (fun z hz => by rw [ge _ (hQ hz)]; exact hb _)
  exact ⟨⟨z, hQ hz⟩, by rwa [ge _ (hQ hz)] at he⟩

lemma finite_partition_impossible_gen {ι : Type*} [Fintype ι] {Q : Set ℂ} {R d : ℝ}
    (hQ : Metric.ball (0 : ℂ) R ⊆ Q) (hd : 0 ≤ d) (hRd : d < R) (p : ι → ℂ) (w : ι → C(Q, ℝ))
    (hn : ∀ i z, 0 ≤ w i z) (hs : ∀ z, ∑ i, w i z = 1)
    (hm : ∀ z, (Finset.univ.filter (fun i => w i z ≠ 0)).card ≤ 2)
    (hpd : ∀ i z, w i z ≠ 0 → ‖p i - z.val‖ ≤ d) : False := by
  classical
  set c : ℝ := (d + R) / 2 with hcdef
  set r : ℝ := (R - d) / 2 with hrdef
  have hdc : d < c := by simp only [hcdef]; linarith
  have hrpos : 0 < r := by simp only [hrdef]; linarith
  let F : Q → ℂ := fun z => ∑ i, w i z • p i
  have Fc : Continuous F := by fun_prop
  have Fb (z : Q) : ‖F z - z.val‖ ≤ d := by
    have he : F z - z.val = ∑ i, w i z • (p i - z.val) := by
      simp only [smul_sub, Finset.sum_sub_distrib, ← Finset.sum_smul, hs, one_smul, F]
    rw [he]
    calc ‖∑ i, w i z • (p i - z.val)‖ ≤ ∑ i, ‖w i z • (p i - z.val)‖ := norm_sum_le _ _
      _ ≤ ∑ i, w i z * d := by
        apply Finset.sum_le_sum
        intro i _
        by_cases hi : w i z = 0
        · simp [hi]
        · rw [norm_smul, Real.norm_eq_abs, abs_of_nonneg (hn i z)]
          exact mul_le_mul_of_nonneg_left (hpd i z hi) (hn i z)
      _ = d := by rw [← Finset.sum_mul, hs]; ring
  have hsub : Metric.ball (0 : ℂ) r ⊆ Set.range F := by
    intro y hy
    have hy' : ‖y‖ < r := by simpa [Metric.mem_ball, dist_zero_right] using hy
    apply hit_center_subtype_gen hd hdc ?_ Fc Fb
    intro z hz
    apply hQ
    rw [Metric.mem_ball, dist_eq_norm] at hz
    rw [Metric.mem_ball, dist_zero_right]
    have h1 : ‖z‖ = ‖(z - y) + y‖ := by rw [sub_add_cancel]
    rw [h1]
    calc ‖(z - y) + y‖ ≤ ‖z - y‖ + ‖y‖ := norm_add_le _ _
      _ < c + r := add_lt_add hz hy'
      _ = R := by simp only [hcdef, hrdef]; ring
  have hnull : volume (⋃ a, ⋃ b, (affineSpan ℝ ({p a, p b} : Set ℂ) : Set ℂ)) = 0 :=
    measure_iUnion_null fun a => measure_iUnion_null fun b => affinePair_null _ _
  have hfsub : Set.range F ⊆ ⋃ a, ⋃ b, (affineSpan ℝ ({p a, p b} : Set ℂ) : Set ℂ) := by
    rintro _ ⟨z, rfl⟩
    exact barycenter_two p (fun i => w i z) (fun i => hn i z) (hs z) (hm z)
  have hz := measure_mono_null (hsub.trans hfsub) hnull
  exact (Metric.isOpen_ball.measure_pos volume (Metric.nonempty_ball.mpr hrpos)).ne' hz

lemma finite_open_cover_impossible_gen {ι : Type*} [Fintype ι] {Q : Set ℂ} {R d : ℝ}
    (hQ : Metric.ball (0 : ℂ) R ⊆ Q) (hd : 0 ≤ d) (hRd : d < R) (U : ι → Set Q)
    (ho : ∀ i, IsOpen (U i)) (hcov : ∀ z : Q, ∃ i, z ∈ U i)
    (hm : ∀ z : Q, (Finset.univ.filter (fun i => z ∈ U i)).card ≤ 2)
    (hdi : ∀ i, ∀ x ∈ U i, ∀ y ∈ U i, ‖x.val - y.val‖ ≤ d) : False := by
  classical
  obtain ⟨w, hw⟩ := PartitionOfUnity.exists_isSubordinate isClosed_univ U ho (by
    intro z _
    exact mem_iUnion.mpr (hcov z))
  have hz0 : (0 : ℂ) ∈ Q := hQ (Metric.mem_ball_self (by linarith))
  let p : ι → Q := fun i => if h : (U i).Nonempty then h.choose else ⟨0, hz0⟩
  apply finite_partition_impossible_gen hQ hd hRd (fun i => (p i).val) w (w.nonneg) ?_ ?_ ?_
  · intro z
    rw [← w.sum_eq_one (mem_univ z), finsum_eq_sum_of_fintype]
  · intro z
    apply le_trans (Finset.card_le_card ?_) (hm z)
    intro i hi
    simp only [Finset.mem_filter, Finset.mem_univ, true_and] at hi ⊢
    exact hw i (subset_closure hi)
  · intro i z hz
    have hzu : z ∈ U i := hw i (subset_closure hz)
    have hp : p i ∈ U i := by
      dsimp only [p]
      rw [dite_eq_left ⟨z, hzu⟩]
      exact Classical.choose_spec _
    exact hdi i _ hp z hzu

theorem compact_cover_obstruction_gen {ι : Type*} {Q : Set ℂ} {R d : ℝ}
    (hQ : Metric.ball (0 : ℂ) R ⊆ Q) (hd : 0 ≤ d) (hRd : d < R) (hQc : IsCompact Q)
    (U : ι → Set Q) (ho : ∀ i, IsOpen (U i)) (hcov : ∀ z : Q, ∃ i, z ∈ U i)
    (hm : ∀ z : Q, ∀ i j l, z ∈ U i → z ∈ U j → z ∈ U l → i = j ∨ i = l ∨ j = l)
    (hdi : ∀ i, ∀ x ∈ U i, ∀ y ∈ U i, ‖x.val - y.val‖ ≤ d) : False := by
  classical
  have : CompactSpace Q := isCompact_iff_compactSpace.mp hQc
  obtain ⟨s, hs⟩ := isCompact_univ.elim_finite_subcover U ho (by
    intro z _
    exact mem_iUnion.mpr (hcov z))
  exact finite_open_cover_impossible_gen hQ hd hRd (fun i : s => U i.val) (fun i => ho i.val)
    (by
      intro z
      rcases mem_iUnion.mp (hs (mem_univ z)) with ⟨i, hi⟩
      rcases mem_iUnion.mp hi with ⟨his, hiz⟩
      exact ⟨⟨i, his⟩, hiz⟩)
    (by
      intro z
      by_contra! hcard
      obtain ⟨i, hi, j, hj, l, hl, hij, hil, hjl⟩ := Finset.two_lt_card.mp hcard
      simp only [Finset.mem_filter, Finset.mem_univ, true_and] at hi hj hl
      rcases hm z i.val j.val l.val hi hj hl with h | h | h
      · exact hij (Subtype.ext h)
      · exact hil (Subtype.ext h)
      · exact hjl (Subtype.ext h))
    (fun i => hdi i.val)

def square10 : Set ℂ := {z | |z.re| ≤ 5 ∧ |z.im| ≤ 5}

lemma isClosed_square10 : IsClosed square10 := by
  have h : square10 = {z : ℂ | |z.re| ≤ 5} ∩ {z : ℂ | |z.im| ≤ 5} := by
    ext z
    simp [square10]
  rw [h]
  exact (isClosed_le (continuous_abs.comp Complex.continuous_re) continuous_const).inter
    (isClosed_le (continuous_abs.comp Complex.continuous_im) continuous_const)

lemma isCompact_square10 : IsCompact square10 := by
  apply IsCompact.of_isClosed_subset (isCompact_closedBall (0 : ℂ) 10) isClosed_square10
  intro z hz
  obtain ⟨h1, h2⟩ := hz
  rw [Metric.mem_closedBall, dist_zero_right]
  have h3 : |z.re| ≤ 5 := h1
  have h4 : |z.im| ≤ 5 := h2
  linarith [Complex.norm_le_abs_re_add_abs_im z]

lemma ball_subset_square10 : Metric.ball (0 : ℂ) 5 ⊆ square10 := by
  intro z hz
  have hz' : ‖z‖ < 5 := by simpa [Metric.mem_ball, dist_zero_right] using hz
  exact ⟨(Complex.abs_re_le_norm z).trans hz'.le, (Complex.abs_im_le_norm z).trans hz'.le⟩

theorem paper_lemma_7_5 {ι : Type*} (U : ι → Set square10)
    (ho : ∀ i, IsOpen (U i)) (hcov : ∀ z : square10, ∃ i, z ∈ U i)
    (hm : ∀ z : square10, ∀ i j l, z ∈ U i → z ∈ U j → z ∈ U l → i = j ∨ i = l ∨ j = l)
    (hdi : ∀ i, ∀ x ∈ U i, ∀ y ∈ U i, ‖x.val - y.val‖ ≤ 2) : False :=
  compact_cover_obstruction_gen ball_subset_square10 (by norm_num) (by norm_num)
    isCompact_square10 U ho hcov hm hdi

theorem disk3_cover_obstruction {ι : Type*} (U : ι → Set (Metric.closedBall (0 : ℂ) 3))
    (ho : ∀ i, IsOpen (U i)) (hcov : ∀ z, ∃ i, z ∈ U i)
    (hm : ∀ z, ∀ i j l, z ∈ U i → z ∈ U j → z ∈ U l → i = j ∨ i = l ∨ j = l)
    (hdi : ∀ i, ∀ x ∈ U i, ∀ y ∈ U i, ‖x.val - y.val‖ ≤ 2) : False :=
  compact_cover_obstruction_gen (fun z hz => Metric.ball_subset_closedBall hz) (by norm_num)
    (by norm_num) (isCompact_closedBall (0 : ℂ) 3) U ho hcov hm hdi

end PlanarCover
end OAI
