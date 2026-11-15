module

public import ZetaFive.Lean.Family.Weight
public import ZetaFive.Lean.Common.ExponentialBounds

@[expose] public section

/-!
# Uniform bounds for the zeta densities

The binomial generating series bounds the defining series of `weight k`. The
result retains the rate `exp (-2πy)` and is uniform for `2 ≤ k ≤ 5`, including
near zero. The underlying geometric-series estimates live in `Common`.
-/

namespace ZetaFive

/-- The series bound before cancelling the factorial normalization in the density. -/
theorem weightSeries_le_geometric (k : ℕ) (hk : 1 ≤ k) {y : ℝ} (hy : 0 < y) :
    weightSeries k y ≤ ((k - 1).factorial : ℝ) * Real.exp (-2 * Real.pi * y) /
      (1 - Real.exp (-2 * Real.pi * y)) ^ k := by
  have hq0 : 0 ≤ Real.exp (-2 * Real.pi * y) := (Real.exp_pos _).le
  have hq1 : Real.exp (-2 * Real.pi * y) < 1 := by
    rw [Real.exp_lt_one_iff]
    nlinarith [Real.pi_pos]
  have hkm : k - 1 + 1 = k := Nat.sub_add_cancel hk
  have h := Common.tsum_succ_pow_mul_geometric_le (k - 1) hq0 hq1
  simpa only [weightSeries, weightSummand_eq_geometric, Nat.cast_add, Nat.cast_one, hkm]
    using h

/-- A bound for every positive integer weight, proved from its defining series. -/
theorem weight_le_exp_bound (k : ℕ) (hk : 1 ≤ k) {y : ℝ} (hy : 0 < y) :
    weight k y ≤ (1 / Real.pi) * (1 + 2 * Real.pi * y) ^ k *
      Real.exp (-2 * Real.pi * y) := by
  have hpi : Real.pi ≠ 0 := Real.pi_pos.ne'
  have hf : ((k - 1).factorial : ℝ) ≠ 0 := by positivity
  have hq : Real.exp (-2 * Real.pi * y) < 1 := by
    rw [Real.exp_lt_one_iff]
    nlinarith [Real.pi_pos]
  have hden : 0 < 1 - Real.exp (-2 * Real.pi * y) := by linarith
  have hkm : k - 1 + 1 = k := Nat.sub_add_cancel hk
  have hpower : (2 * Real.pi) ^ k = 2 * Real.pi * (2 * Real.pi) ^ (k - 1) := by
    conv_lhs => rw [← hkm, pow_succ']
  have hratio : (2 * Real.pi * y) / (1 - Real.exp (-2 * Real.pi * y)) ≤
      1 + 2 * Real.pi * y := by
    simpa only [neg_mul] using
      Common.div_one_sub_exp_neg_le_add_one (by positivity : 0 < 2 * Real.pi * y)
  have hpow : ((2 * Real.pi * y) / (1 - Real.exp (-2 * Real.pi * y))) ^ k ≤
      (1 + 2 * Real.pi * y) ^ k :=
    pow_le_pow_left₀ (div_nonneg (by positivity) hden.le) hratio k
  calc
    weight k y ≤ (2 * (2 * Real.pi) ^ (k - 1) * y ^ k /
        ((k - 1).factorial : ℝ)) *
        (((k - 1).factorial : ℝ) * Real.exp (-2 * Real.pi * y) /
          (1 - Real.exp (-2 * Real.pi * y)) ^ k) :=
      mul_le_mul_of_nonneg_left (weightSeries_le_geometric k hk hy) (by positivity)
    _ = (1 / Real.pi) *
        ((2 * Real.pi * y) / (1 - Real.exp (-2 * Real.pi * y))) ^ k *
          Real.exp (-2 * Real.pi * y) := by
      rw [div_pow, mul_pow (2 * Real.pi) y, hpower]
      field_simp
    _ ≤ _ := mul_le_mul_of_nonneg_right
      (mul_le_mul_of_nonneg_left hpow (by positivity)) (Real.exp_pos _).le

/-- A single bound on the entire positive half-line for the requested range. -/
theorem weight_le_uniform_exp_bound {k : ℕ} (hk1 : 1 ≤ k) (hk5 : k ≤ 5)
    {y : ℝ} (hy : 0 < y) :
    weight k y ≤ (1 / Real.pi) * (1 + 2 * Real.pi * y) ^ 5 *
      Real.exp (-2 * Real.pi * y) := by
  apply (weight_le_exp_bound k hk1 hy).trans
  apply mul_le_mul_of_nonneg_right _ (Real.exp_pos _).le
  apply mul_le_mul_of_nonneg_left _ (by positivity)
  have hbase : 1 ≤ 1 + 2 * Real.pi * y := by
    have hpositive : 0 < 2 * Real.pi * y := by positivity
    linarith
  exact pow_le_pow_right₀ hbase hk5

end ZetaFive

