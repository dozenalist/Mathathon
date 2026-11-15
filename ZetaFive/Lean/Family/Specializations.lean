module

public import ZetaFive.Lean.Family.Moments

@[expose] public section

/-! # Checked formulas for the four indices

These equalities specialize the same definition. In particular, the second
factor in weight four and the third factor in weight five must not be silently
retained when changing the zeta index in the arithmetic argument.
-/

namespace ZetaFive

theorem moment_two (e : ℕ) : moment 2 e = (-1 : ℚ) ^ e * bernoulli (2 * e + 2) := by
  simp [moment]

theorem moment_three (e : ℕ) :
    moment 3 e = (-1 : ℚ) ^ e * bernoulli (2 * e + 2) * (2 * e + 3) / 2 := by
  simp [moment, Nat.ascFactorial_succ, Nat.factorial_succ]

theorem moment_four (e : ℕ) :
    moment 4 e = (-1 : ℚ) ^ e * bernoulli (2 * e + 2) *
      (2 * e + 3) * (2 * e + 4) / 6 := by
  simp [moment, Nat.ascFactorial_succ, Nat.factorial_succ]
  ring

theorem moment_five (e : ℕ) :
    moment 5 e = (-1 : ℚ) ^ e * bernoulli (2 * e + 2) *
      (2 * e + 3) * (2 * e + 4) * (2 * e + 5) / 24 := by
  simp [moment, Nat.ascFactorial_succ, Nat.factorial_succ]
  ring

theorem moment_zero (k : ℕ) (hk : 2 ≤ k) : moment k 0 = (k : ℚ) / 12 := by
  rw [moment_factorial k 0 hk]
  norm_num
  have hfac : k.factorial = k * (k - 1).factorial := by
    have h : k = (k - 1) + 1 := by omega
    conv_lhs => rw [h, Nat.factorial_succ]
    congr 1
    omega
  rw [hfac]
  push_cast
  have h : ((k - 1).factorial : ℚ) ≠ 0 := by positivity
  field_simp
  ring

end ZetaFive

