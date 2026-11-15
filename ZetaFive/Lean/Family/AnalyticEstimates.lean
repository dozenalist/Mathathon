module

public import ZetaFive.Lean.Family.DetIntegral
public import ZetaFive.Lean.Family.WeightBound
public import Mathlib.Algebra.Order.BigOperators.GroupWithZero.Finset

@[expose] public section

/-!
# Uniform analytic inputs for the determinant estimate

These are the pointwise density and multiple-integrand estimates needed before
applying a logarithmic-energy inequality. They hold for arbitrary determinant
parameters. This file does not assert the remaining configuration-energy bound
or a negative quadratic exponent for the normalized determinant.
-/

open Polynomial Finset
open ZetaFive.Common

namespace ZetaFive

/-- The logarithmic weight estimate used by the configuration argument. -/
theorem log_weight_le (k : ℕ) (hk1 : 1 ≤ k) (hk5 : k ≤ 5) {y : ℝ} (hy : 0 < y) :
    Real.log (weight k y) ≤ 5 * Real.log (1 + 2 * Real.pi * y) - 2 * Real.pi * y := by
  have hweight := weight_pos k hy
  have hlogpi : Real.log (1 / Real.pi) ≤ 0 := by
    rw [one_div, Real.log_inv]
    linarith [Real.log_nonneg (by linarith [Real.pi_gt_three] : (1 : ℝ) ≤ Real.pi)]
  calc
    Real.log (weight k y) ≤
        Real.log ((1 / Real.pi) * (1 + 2 * Real.pi * y) ^ 5 *
          Real.exp (-2 * Real.pi * y)) :=
      Real.log_le_log hweight (weight_le_uniform_exp_bound hk1 hk5 hy)
    _ = Real.log (1 / Real.pi) +
        5 * Real.log (1 + 2 * Real.pi * y) - 2 * Real.pi * y := by
      rw [Real.log_mul (by positivity) (by positivity),
        Real.log_mul (by positivity) (by positivity), Real.log_exp, Real.log_pow]
      norm_num <;> ring
    _ ≤ _ := by linarith

/-- The zeta-independent modifier can be retained unchanged in the uniform bound. -/
theorem modifiedWeight_le_uniform_bound (k : ℕ) (hk1 : 1 ≤ k) (hk5 : k ≤ 5)
    (p : Parameters) {y : ℝ} (hy : 0 < y) :
    modifiedWeight k p y ≤
      (aeval (y ^ 2) (D p.N) ^ p.numeratorPower / aeval (y ^ 2) (D p.K)) *
        ((1 / Real.pi) * (1 + 2 * Real.pi * y) ^ 5 * Real.exp (-2 * Real.pi * y)) := by
  apply mul_le_mul_of_nonneg_left (weight_le_uniform_exp_bound hk1 hk5 hy)
  exact div_nonneg (pow_nonneg (aeval_D_pos p.N (by positivity)).le _)
    (aeval_D_pos p.K (by positivity)).le

/-- The corresponding bound for the actual multiple-integral integrand. -/
theorem determinantIntegrand_le_uniform_bound (k : ℕ) (hk1 : 1 ≤ k) (hk5 : k ≤ 5)
    (p : Parameters) (y : Fin p.h → ℝ) (hy : ∀ i, 0 < y i) :
    determinantIntegrand k p y ≤
      (Matrix.vandermonde fun j => y j ^ 2).det ^ 2 *
        ∏ i, (aeval (y i ^ 2) (D p.N) ^ p.numeratorPower /
          aeval (y i ^ 2) (D p.K)) *
          ((1 / Real.pi) * (1 + 2 * Real.pi * y i) ^ 5 *
            Real.exp (-2 * Real.pi * y i)) := by
  apply mul_le_mul_of_nonneg_left _ (sq_nonneg _)
  exact Finset.prod_le_prod₀ (fun i _ => (modifiedWeight_pos k p (hy i)).le)
    (fun i _ => modifiedWeight_le_uniform_bound k hk1 hk5 p (hy i))

end ZetaFive
