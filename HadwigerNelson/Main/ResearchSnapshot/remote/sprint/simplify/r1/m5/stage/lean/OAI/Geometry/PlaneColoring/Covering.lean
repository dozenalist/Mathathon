import Mathlib

namespace OAI

noncomputable section

namespace Problem160


unit triangular lattice. The proof gives one of three explicit nearby centers. -/
theorem triangular_lattice_cover (x y : ℝ) :
    ∃ m n : ℤ,
      (x - ((m : ℝ) + (n : ℝ) / 2)) ^ 2 +
        (y - Real.sqrt 3 * (n : ℝ) / 2) ^ 2 ≤ 1 / 3 := by
  let s : ℝ := Real.sqrt 3
  have hs : 0 < s := Real.sqrt_pos.2 (by norm_num)
  have hsq : s ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  let n : ℤ := ⌊2 * y / s⌋
  let m : ℤ := ⌊x - (n : ℝ) / 2⌋
  let u : ℝ := x - ((m : ℝ) + (n : ℝ) / 2)
  let v : ℝ := y - s * (n : ℝ) / 2
  have hn0 : (n : ℝ) ≤ 2 * y / s := Int.floor_le _
  have hn1 : 2 * y / s < (n : ℝ) + 1 := Int.lt_floor_add_one _
  have hm0 : (m : ℝ) ≤ x - (n : ℝ) / 2 := Int.floor_le _
  have hm1 : x - (n : ℝ) / 2 < (m : ℝ) + 1 := Int.lt_floor_add_one _
  have hu0 : 0 ≤ u := by dsimp [u]; linarith
  have hu1 : u ≤ 1 := by dsimp [u]; linarith
  have hv0 : 0 ≤ v := by
    have h := (le_div_iff₀ hs).mp hn0
    dsimp [v]
    nlinarith
  have hv1 : v ≤ s / 2 := by
    have h := (div_lt_iff₀ hs).mp hn1
    dsimp [v]
    nlinarith
  rcases triangular_rectangle_cover s u v hs hsq hu0 hu1 hv0 hv1 with h | h | h
  · exact ⟨m, n, h⟩
  · refine ⟨m + 1, n, ?_⟩
    have hu : x - (((m + 1 : ℤ) : ℝ) + (n : ℝ) / 2) = u - 1 := by
      dsimp [u]
      push_cast
      ring
    rw [hu]
    exact h
  · refine ⟨m, n + 1, ?_⟩
    have hu : x - ((m : ℝ) + ((n + 1 : ℤ) : ℝ) / 2) = u - 1 / 2 := by
      dsimp [u]
      push_cast
      ring
    have hv : y - Real.sqrt 3 * ((n + 1 : ℤ) : ℝ) / 2 = v - s / 2 := by
      dsimp [v, s]
      push_cast
      ring
    rw [hu, hv]
    exact h

end Problem160

end

end OAI
