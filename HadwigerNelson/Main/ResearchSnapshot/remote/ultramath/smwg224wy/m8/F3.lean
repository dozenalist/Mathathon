import OAI.Analysis.PlaneSpectrum.ConditionalSpectrum

/-!
# (F3): every element of the algebraic plane is a finite sum of unit-modulus algebraics

`K` is the group of *all* unit-modulus algebraic numbers.  The step "`K` additively
generates `E`" is what makes the (N)/(O) argument of `.ultramath/smwfoekgk/m7/N-proof.md`
work at one point (`v` running over all of `E`), and it is also what makes the
"`{a : Re μ̂(a) > 1 − ε}ᵢ` generates `E`" step of the sharpened version work.  The tree
has only the *real* two-term case (`ConditionalSpectrum.lean:116`,
`real_algebraic_sum_two_rotations`); this file gives the general statement.

Main result: `exists_list_sum_kCoeff : ∀ z : E, ∃ l : List K, z = (l.map kCoeff).sum`.
-/

namespace OAI

noncomputable section

open MeasureTheory
namespace PlaneFiveColor.Spectral

/-- The `K`-element with `kCoeff iK = imagUnit` (`i` is algebraic of modulus one). -/
def iK : K where
  val := ⟨Complex.I, mem_sphere_zero_iff_norm.mpr (by simp)⟩
  property := isAlgebraic_iff_isIntegral.mpr (Complex.isIntegral_I ℚ)

@[simp] theorem kCoeff_iK : kCoeff iK = imagUnit := Subtype.ext rfl

/-- Scalar distribution for list sums, used to push `imagUnit` inside a sum. -/
theorem list_sum_map_mul_left (a : E) (f : K → E) (l : List K) :
    (l.map (fun x => a * f x)).sum = a * (l.map f).sum := by
  induction l with
  | nil => simp
  | cons x xs ih => simp [List.map_cons, List.sum_cons, ih, mul_add]

/-- Pointwise form of `kCoeff_mul` at `iK`, used to push `iK` through a `kCoeff`. -/
theorem kCoeff_iK_mul (w : K) : kCoeff (iK * w) = imagUnit * kCoeff w := by
  rw [kCoeff_mul, kCoeff_iK]

/-- The `K`-side congruence: mapping `iK * ·` and then `kCoeff` is `imagUnit *` a `kCoeff`. -/
theorem map_map_kCoeff_mul_iK (l : List K) :
    ((l.map (fun w : K => iK * w)).map kCoeff).sum
      = (l.map (fun w : K => imagUnit * kCoeff w)).sum := by
  induction l with
  | nil => simp
  | cons a as ih =>
    simp only [List.map_cons, List.sum_cons, ih, kCoeff_iK_mul]

/-- **(F3)**, real case: every real algebraic number is a finite sum of unit-modulus
algebraic numbers.  Reduces to `real_algebraic_sum_two_rotations` by scaling. -/
theorem exists_list_sum_kCoeff_ofF (t : F) :
    ∃ l : List K, ofF t = (l.map kCoeff).sum := by
  classical
  rcases eq_or_ne t 0 with h | h
  · exact ⟨[], by simp [h]⟩
  have ht : (0:ℝ) < |(t : ℝ)| := abs_pos.mpr (by simpa using h)
  obtain ⟨n, hn⟩ : ∃ n : ℕ, 0 < n ∧ |(t : ℝ)| < 2 * n := by
    obtain ⟨m, hm⟩ := exists_nat_gt (|(t:ℝ)| / 2)
    refine ⟨m + 1, Nat.succ_pos m, ?_⟩
    have : |(t:ℝ)| / 2 < (m : ℝ) := hm
    have : (m : ℝ) < ((m + 1 : ℕ) : ℝ) := by push_cast; linarith
    nlinarith
  obtain ⟨hnpos, hnlt⟩ := hn
  have hnR : (0:ℝ) < (n : ℝ) := by exact_mod_cast hnpos
  set x : F := t / (n : F) with hx
  have hxval : (x : ℝ) = (t : ℝ) / (n : ℝ) := by
    rw [hx]; push_cast; rfl
  have hxabs : |(x : ℝ)| < 2 := by
    rw [hxval, abs_div, abs_of_pos hnR, div_lt_iff₀ hnR]
    linarith
  obtain ⟨u, v, huv⟩ := real_algebraic_sum_two_rotations x hxabs
  have ht_eq : t = (n : F) * x := by
    rw [hx, mul_div_cancel₀]
    exact Nat.cast_ne_zero.mpr hnpos.ne'
  refine ⟨List.replicate n u ++ List.replicate n v, ?_⟩
  rw [List.map_append, List.sum_append, List.map_replicate, List.map_replicate,
    List.sum_replicate, List.sum_replicate]
  rw [ht_eq, map_mul, map_natCast, huv, mul_add, nsmul_eq_mul, nsmul_eq_mul]

/-- **(F3)**, general case. -/
theorem exists_list_sum_kCoeff (z : E) : ∃ l : List K, z = (l.map kCoeff).sum := by
  obtain ⟨l₁, hl₁⟩ := exists_list_sum_kCoeff_ofF (reF z)
  obtain ⟨l₂, hl₂⟩ := exists_list_sum_kCoeff_ofF (imF z)
  refine ⟨l₁ ++ l₂.map (fun w : K => iK * w), ?_⟩
  rw [List.map_append, List.sum_append, map_map_kCoeff_mul_iK,
    list_sum_map_mul_left, ← hl₁, ← hl₂, reF_add_imF]

end PlaneFiveColor.Spectral

end

end OAI
