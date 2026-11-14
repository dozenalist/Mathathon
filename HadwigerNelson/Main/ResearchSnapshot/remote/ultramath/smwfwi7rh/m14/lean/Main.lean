/-
  Final assembly: the classical seven-colouring of the plane, modified inside a square of side
  `1/100` about `p₀ = (4√3/15) i` by three-sector gadgets on disjoint disks accumulating at
  `p₀`, is a *proper* colouring whose cyclic locus is not locally finite.
-/
import SevenColoring

open MeasureTheory Filter Topology Set
open scoped ENNReal

attribute [local instance] Classical.propDecidable

namespace SectorGadget

/-! ## 13. Numerical constants -/

lemma sqrt3_lt_173 : Real.sqrt 3 < 17321/10000 := by
  have h3 : (Real.sqrt 3) ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  have hnn := Real.sqrt_nonneg 3
  nlinarith

lemma near_lt : 4 * Real.sqrt 3 / 15 < 77/150 := by
  have := sqrt3_lt_173; have hnn := Real.sqrt_nonneg 3; nlinarith

lemma far_gt : 223/150 < 2 - 4 * Real.sqrt 3 / 15 := by
  have := sqrt3_lt_173; have hnn := Real.sqrt_nonneg 3; nlinarith

lemma near_gap : 77/150 < 1 - 1/100 - 4 * Real.sqrt 3 / 15 := by
  have := sqrt3_lt_173; have hnn := Real.sqrt_nonneg 3; nlinarith

lemma far_gap : 1 + 1/100 + 4 * Real.sqrt 3 / 15 < 223/150 := by
  have := sqrt3_lt_173; have hnn := Real.sqrt_nonneg 3; nlinarith

lemma cover_lt_one : 4 * Real.sqrt 3 / 15 * 2 < 1 := by
  have := sqrt3_lt_173; have hnn := Real.sqrt_nonneg 3; nlinarith

/-- `‖(r : ℂ)‖ = r` for `r ≥ 0`. -/
lemma norm_ofReal (r : ℝ) (hr : 0 ≤ r) : ‖(r : ℂ)‖ = r := by
  have hsq : ‖(r:ℂ)‖ ^ 2 = r ^ 2 := by
    rw [sq_norm_re_im]
    simp only [Complex.ofReal_re, Complex.ofReal_im]
    ring
  exact le_antisymm (le_of_sq_le_sq hr (le_of_eq hsq))
    (le_of_sq_le_sq (norm_nonneg _) (le_of_eq hsq.symm))

/-! ## 14. The annulus certificate -/

/-- **Annulus certificate.** Every lattice point of colour `0`, `2` or `3` is either within
`77/150` of `p₀` or beyond `223/150` from it. -/
theorem annulus_seven (a b : ℤ) (h : colFin a b ∈ ({0, 2, 3} : Set (Fin 7))) :
    ‖p0 - lat a b‖ < 77/150 ∨ 223/150 < ‖p0 - lat a b‖ := by
  have step : ∀ c d : ℤ, colFin a b = colFin c d → ‖p0 - lat c d‖ = 4 * Real.sqrt 3 / 15 →
      ‖p0 - lat a b‖ < 77/150 ∨ 223/150 < ‖p0 - lat a b‖ := by
    intro c d hc hdist
    by_cases hidx : (a, b) = (c, d)
    · left
      obtain ⟨ha, hb⟩ := (Prod.mk.injEq a b c d).mp hidx
      rw [ha, hb, hdist]
      exact near_lt
    · right
      have hcr : colr a b = colr c d := colFin_eq_iff.mp hc
      have hdvd : 7 ∣ (c + 3 * d) - (a + 3 * b) := colr_eq_iff.mp hcr
      have hdvd' : 7 ∣ (c - a) + 3 * (d - b) := by
        have he : (c - a) + 3 * (d - b) = (c + 3 * d) - (a + 3 * b) := by ring
        rw [he]; exact hdvd
      have hsep : (2:ℝ) < ‖lat c d - lat a b‖ :=
        lat_separation (hne := fun hh => hidx hh.symm) hdvd'
      have htri : ‖lat c d - lat a b‖ ≤ ‖lat c d - p0‖ + ‖p0 - lat a b‖ := by
        have h := norm_add_le (lat c d - p0) (p0 - lat a b)
        have he : (lat c d - p0) + (p0 - lat a b) = lat c d - lat a b := by ring
        rwa [he] at h
      rw [norm_sub_rev (lat c d) p0, hdist] at htri
      linarith [far_gt]
  have h0 : colFin a b = 0 ∨ colFin a b = 2 ∨ colFin a b = 3 := by
    simpa only [Set.mem_insert_iff, Set.mem_singleton_iff] using h
  rcases h0 with h0 | h0 | h0
  · exact step 0 0 (by rw [h0, colFin_zero]) dist_p0_zero
  · exact step (-1) 1 (by rw [h0, colFin_two]) dist_p0_neg
  · exact step 0 1 (by rw [h0, colFin_three]) dist_p0_one

/-! ## 15. The seven-colouring is proper -/

theorem sevenColor_proper : ∀ x y : ℂ, ‖x - y‖ = 1 → sevenColor x ≠ sevenColor y := by
  intro x y hxy hcol
  have hcx := coverPt_spec x
  have hcy := coverPt_spec y
  by_cases hsame : (coverPt x).1 = (coverPt y).1 ∧ (coverPt x).2 = (coverPt y).2
  · obtain ⟨h1, h2⟩ := hsame
    have hcy' : ‖lat (coverPt x).1 (coverPt x).2 - y‖ ≤ 4 * Real.sqrt 3 / 15 := by
      rw [norm_sub_rev, h1, h2]
      exact hcy
    have hyt : ‖x - y‖ ≤ ‖x - lat (coverPt x).1 (coverPt x).2‖ +
        ‖lat (coverPt x).1 (coverPt x).2 - y‖ := by
      have h := norm_add_le (x - lat (coverPt x).1 (coverPt x).2)
        (lat (coverPt x).1 (coverPt x).2 - y)
      have he : (x - lat (coverPt x).1 (coverPt x).2) +
          (lat (coverPt x).1 (coverPt x).2 - y) = x - y := by ring
      rwa [he] at h
    rw [hxy] at hyt
    linarith [cover_lt_one]
  · push Not at hsame
    have hidx : ((coverPt x).1, (coverPt x).2) ≠ ((coverPt y).1, (coverPt y).2) := by
      intro hc
      obtain ⟨ha, hb⟩ := (Prod.mk.injEq _ _ _ _).mp hc
      exact hsame ha hb
    have hcr : colr (coverPt x).1 (coverPt x).2 = colr (coverPt y).1 (coverPt y).2 :=
      colFin_eq_iff.mp hcol
    have hdvd : 7 ∣ ((coverPt y).1 + 3 * (coverPt y).2) -
        ((coverPt x).1 + 3 * (coverPt x).2) := colr_eq_iff.mp hcr
    have hdvd' : 7 ∣ ((coverPt y).1 - (coverPt x).1) +
        3 * ((coverPt y).2 - (coverPt x).2) := by
      have he : ((coverPt y).1 - (coverPt x).1) +
          3 * ((coverPt y).2 - (coverPt x).2) =
          ((coverPt y).1 + 3 * (coverPt y).2) - ((coverPt x).1 + 3 * (coverPt x).2) := by ring
      rw [he]; exact hdvd
    have hsep : (2:ℝ) < ‖lat (coverPt y).1 (coverPt y).2 - lat (coverPt x).1 (coverPt x).2‖ :=
      lat_separation (hne := fun hh => hidx hh.symm) hdvd'
    have htri : ‖lat (coverPt y).1 (coverPt y).2 - lat (coverPt x).1 (coverPt x).2‖ ≤
        ‖lat (coverPt y).1 (coverPt y).2 - y‖ + ‖y - x‖ +
        ‖x - lat (coverPt x).1 (coverPt x).2‖ := by
      have h1 : ‖lat (coverPt y).1 (coverPt y).2 - lat (coverPt x).1 (coverPt x).2‖ ≤
          ‖lat (coverPt y).1 (coverPt y).2 - y‖ + ‖y - lat (coverPt x).1 (coverPt x).2‖ := by
        have h := norm_add_le (lat (coverPt y).1 (coverPt y).2 - y)
          (y - lat (coverPt x).1 (coverPt x).2)
        have he : (lat (coverPt y).1 (coverPt y).2 - y) +
            (y - lat (coverPt x).1 (coverPt x).2) =
            lat (coverPt y).1 (coverPt y).2 - lat (coverPt x).1 (coverPt x).2 := by ring
        rwa [he] at h
      have h2 : ‖y - lat (coverPt x).1 (coverPt x).2‖ ≤ ‖y - x‖ +
          ‖x - lat (coverPt x).1 (coverPt x).2‖ := by
        have h := norm_add_le (y - x) (x - lat (coverPt x).1 (coverPt x).2)
        have he : (y - x) + (x - lat (coverPt x).1 (coverPt x).2) =
            y - lat (coverPt x).1 (coverPt x).2 := by ring
        rwa [he] at h
      linarith
    rw [norm_sub_rev y x, hxy] at htri
    have hcy' : ‖lat (coverPt y).1 (coverPt y).2 - y‖ ≤ 4 * Real.sqrt 3 / 15 := by
      rw [norm_sub_rev]; exact hcy
    linarith [cover_lt_one]

/-! ## 16. The gadget data -/

/-- Gadget centres: on the real axis through `p₀`, tending to `p₀`. -/
noncomputable def gq (n : ℕ) : ℂ := p0 + (((1/400 : ℝ) * (1/2) ^ n : ℝ) : ℂ)

/-- Gadget radii. -/
noncomputable def gr (n : ℕ) : ℝ := (1/100 : ℝ) * (1/2) ^ (n + 6)

lemma gq_re (n : ℕ) : (gq n).re = (1/400 : ℝ) * (1/2) ^ n := by
  rw [gq]
  simp only [Complex.add_re, p0_re, Complex.ofReal_re, zero_add]

lemma gq_im (n : ℕ) : (gq n).im = 4 * Real.sqrt 3 / 15 := by
  rw [gq]
  simp only [Complex.add_im, p0_im, Complex.ofReal_im, add_zero]

lemma half_pow_pos (n : ℕ) : (0:ℝ) < (1/2) ^ n := by positivity

lemma half_pow_le_one (n : ℕ) : (1/2:ℝ) ^ n ≤ 1 := by
  have h : (1/2:ℝ) ^ n ≤ 1 ^ n :=
    pow_le_pow_left₀ (by norm_num) (by norm_num) n
  simpa using h

/-- `(1/2)^k ≤ (1/2)^j` for `j ≤ k`. -/
lemma half_pow_antitone {j k : ℕ} (h : j ≤ k) : (1/2:ℝ) ^ k ≤ (1/2) ^ j := by
  obtain ⟨t, rfl⟩ := Nat.exists_eq_add_of_le h
  rw [pow_add]
  have h1 : (0:ℝ) < (1/2)^j := half_pow_pos j
  have h2 : (1/2:ℝ)^t ≤ 1 := half_pow_le_one t
  nlinarith

lemma gq_diff (n m : ℕ) : gq n - gq m =
    (((1/400 : ℝ) * (1/2)^n - (1/400) * (1/2)^m : ℝ) : ℂ) := by
  rw [gq, gq]; push_cast; ring

lemma gq_sub_p0 (n : ℕ) : gq n - p0 = (((1/400 : ℝ) * (1/2)^n : ℝ) : ℂ) := by
  rw [gq]; ring

lemma gr_pos (n : ℕ) : 0 < gr n := by unfold gr; positivity

lemma gr_le (n : ℕ) : gr n ≤ 1/6400 := by
  unfold gr
  have h1 : (1/2:ℝ) ^ (n + 6) ≤ (1/2) ^ 6 := half_pow_antitone (by omega)
  calc (1/100 : ℝ) * (1/2) ^ (n + 6) ≤ (1/100) * (1/2)^6 :=
        mul_le_mul_of_nonneg_left h1 (by norm_num)
    _ = 1/6400 := by norm_num

lemma gq_ball (n : ℕ) : ‖gq n - p0‖ ≤ 1 := by
  rw [gq_sub_p0, norm_ofReal _ (by positivity)]
  have h1 := half_pow_le_one n
  nlinarith

lemma gr_ball_subset (n : ℕ) : Metric.ball (gq n) (gr n) ⊆ square p0 (1/100) := by
  intro x hx
  have hxd : ‖x - gq n‖ < gr n := by simpa [Metric.mem_ball, Complex.dist_eq] using hx
  have hxd' : ‖x - gq n‖ < 1/6400 := lt_of_lt_of_le hxd (gr_le n)
  have hc0 : (0:ℝ) ≤ (1/400 : ℝ) * (1/2)^n := by positivity
  have hc1 : (1/400 : ℝ) * (1/2)^n ≤ 1/400 := by
    have h := half_pow_le_one n; nlinarith
  have hsplit : x - p0 = (x - gq n) + (((1/400 : ℝ) * (1/2)^n : ℝ) : ℂ) := by
    rw [gq]; ring
  constructor
  · have h1 : (x - p0).re = (x - gq n).re + (1/400 : ℝ) * (1/2)^n := by
      rw [hsplit]
      simp only [Complex.add_re, Complex.ofReal_re]
    rw [h1, abs_le]
    have h2 := abs_le.mp (Complex.abs_re_le_norm (x - gq n))
    constructor <;> linarith
  · have h1 : (x - p0).im = (x - gq n).im := by
      rw [hsplit]
      simp only [Complex.add_im, Complex.ofReal_im, add_zero]
    rw [h1, abs_le]
    have h2 := abs_le.mp (Complex.abs_im_le_norm (x - gq n))
    constructor <;> linarith

lemma gq_gap {n m : ℕ} (hnm : n < m) : gr n + gr m < ‖gq n - gq m‖ := by
  have hP : (0:ℝ) < (1/2)^n := half_pow_pos n
  have hm : (1/2:ℝ)^m ≤ (1/2)^n / 2 := by
    have h := half_pow_antitone (show n + 1 ≤ m by omega)
    rw [pow_succ] at h
    have he : (1/2:ℝ)^n * (1/2) = (1/2)^n / 2 := by ring
    linarith
  have hpos : (0:ℝ) ≤ (1/400 : ℝ) * (1/2)^n - (1/400) * (1/2)^m := by nlinarith
  have hdist : ‖gq n - gq m‖ = (1/400 : ℝ) * (1/2)^n - (1/400) * (1/2)^m := by
    rw [gq_diff, norm_ofReal _ hpos]
  rw [hdist]
  unfold gr
  have h6 : (1/2:ℝ)^(n+6) = (1/2)^n * (1/2)^6 := by rw [pow_add]
  have hm6 : (1/2:ℝ)^(m+6) ≤ (1/2)^(n+6) := half_pow_antitone (by omega)
  have hval : (1/2:ℝ)^6 = 1/64 := by norm_num
  rw [h6, hval] at *
  nlinarith

lemma gq_injective : Function.Injective gq := by
  intro n m hnm
  by_contra hne
  have h1 : gr n + gr m < ‖gq n - gq m‖ := by
    rcases lt_or_gt_of_ne hne with h | h
    · exact gq_gap h
    · have h2 := gq_gap h
      rw [add_comm (gr m) (gr n), norm_sub_rev] at h2
      exact h2
  rw [hnm] at h1
  have h0 : ‖gq m - gq m‖ = 0 := by simp
  rw [h0] at h1
  have hp1 := gr_pos n
  have hp2 := gr_pos m
  linarith

lemma gq_disjoint (n m : ℕ) (hnm : n ≠ m) :
    Disjoint (Metric.ball (gq n) (gr n)) (Metric.ball (gq m) (gr m)) := by
  refine Set.disjoint_left.mpr (fun z hz1 hz2 => ?_)
  have h1 : ‖z - gq n‖ < gr n := by simpa [Metric.mem_ball, Complex.dist_eq] using hz1
  have h2 : ‖z - gq m‖ < gr m := by simpa [Metric.mem_ball, Complex.dist_eq] using hz2
  have hgap : gr n + gr m < ‖gq n - gq m‖ := by
    rcases lt_or_gt_of_ne hnm with h | h
    · exact gq_gap h
    · have h2 := gq_gap h
      rw [add_comm (gr m) (gr n), norm_sub_rev] at h2
      exact h2
  have h3 : ‖gq n - gq m‖ ≤ ‖gq n - z‖ + ‖z - gq m‖ := by
    have h := norm_add_le (gq n - z) (z - gq m)
    have he : (gq n - z) + (z - gq m) = gq n - gq m := by ring
    rwa [he] at h
  rw [norm_sub_rev (gq n) z] at h3
  linarith

/-! ## 17. The theorem -/

/-- The seven-colouring of §11, modified inside the square of side `1/100` about
`p₀ = (4√3/15) i` by three-sector gadgets on the disks `B(gq n, gr n)`, is a proper colouring
whose cyclic locus is not locally finite. -/
theorem exists_proper_seven_not_locallyFinite :
    ∃ c : ℂ → Fin 7, (∀ x y : ℂ, ‖x - y‖ = 1 → c x ≠ c y) ∧
      ¬ LocallyFinite (CyclicLocus c) := by
  have hL : (0:ℝ) < 1/100 := by norm_num
  have hL1 : (1/100 : ℝ) * Real.sqrt 2 < 1 := by
    have h2 : (Real.sqrt 2)^2 = 2 := Real.sq_sqrt (by norm_num)
    have hnn := Real.sqrt_nonneg 2
    nlinarith
  have hEps : (1/100 : ℝ) * Real.sqrt 2 / 2 < 1/100 := by
    have h2 : (Real.sqrt 2)^2 = 2 := Real.sq_sqrt (by norm_num)
    have hnn := Real.sqrt_nonneg 2
    nlinarith
  have hsh : ∀ x : ℂ, x ∉ square p0 (1/100) → 1 - 1/100 ≤ ‖x - p0‖ →
      ‖x - p0‖ ≤ 1 + 1/100 → sevenColor x ∉ ({0, 2, 3} : Set (Fin 7)) := by
    intro x _hx h1 h2 hcol
    have hcx : ‖x - lat (coverPt x).1 (coverPt x).2‖ ≤ 4 * Real.sqrt 3 / 15 :=
      coverPt_spec x
    have hfar : ‖p0 - lat (coverPt x).1 (coverPt x).2‖ ≤ ‖p0 - x‖ +
        ‖x - lat (coverPt x).1 (coverPt x).2‖ := by
      have h := norm_add_le (p0 - x) (x - lat (coverPt x).1 (coverPt x).2)
      have he : (p0 - x) + (x - lat (coverPt x).1 (coverPt x).2) =
          p0 - lat (coverPt x).1 (coverPt x).2 := by ring
      rwa [he] at h
    have hnear : 1 - 1/100 - 4 * Real.sqrt 3 / 15 ≤
        ‖p0 - lat (coverPt x).1 (coverPt x).2‖ := by
      have ht : ‖x - p0‖ ≤ ‖x - lat (coverPt x).1 (coverPt x).2‖ +
          ‖lat (coverPt x).1 (coverPt x).2 - p0‖ := by
        have h := norm_add_le (x - lat (coverPt x).1 (coverPt x).2)
          (lat (coverPt x).1 (coverPt x).2 - p0)
        have he : (x - lat (coverPt x).1 (coverPt x).2) +
            (lat (coverPt x).1 (coverPt x).2 - p0) = x - p0 := by ring
        rwa [he] at h
      rw [norm_sub_rev (lat (coverPt x).1 (coverPt x).2) p0] at ht
      linarith
    rcases annulus_seven (coverPt x).1 (coverPt x).2 hcol with hcase | hcase
    · linarith [near_gap]
    · have hnx : ‖p0 - x‖ = ‖x - p0‖ := norm_sub_rev p0 x
      linarith [far_gap]
  exact exists_cyclicLocus_not_locallyFinite sevenColor sevenColor_proper p0 hL hL1 hEps hsh
    gq gr gr_pos gr_ball_subset gq_disjoint gq_ball gq_injective

end SectorGadget
