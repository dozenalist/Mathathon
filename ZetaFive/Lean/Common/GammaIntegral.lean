module

/-
Adapted from `Apery/Moments.lean` in https://github.com/mo271/zeta5,
commit 7fe736760f4b96bfdb4334b68e3b3124ecbe10b0 (Apache 2.0).
See ZetaFive/Lean/LICENSES/mo271-Zeta5.txt for the license.
-/
public import Mathlib.Analysis.SpecialFunctions.Gamma.Basic
public import Mathlib.MeasureTheory.Integral.Bochner.Set
public import Mathlib.Tactic.FieldSimp
public import Mathlib.Tactic.NormNum
public import Mathlib.Tactic.Positivity
public import Mathlib.Tactic.Ring

@[expose] public section

/-! # Elementary exponential moments, independent of the zeta index -/

open MeasureTheory Set

namespace ZetaFive.Common

/-- The scaled Gamma integral at a nonnegative integer. -/
theorem integral_pow_mul_exp_neg_mul (m : ℕ) {r : ℝ} (hr : 0 < r) :
    ∫ y in Ioi 0, y ^ m * Real.exp (-(r * y)) = (m.factorial : ℝ) / r ^ (m + 1) := by
  have h := Real.integral_rpow_mul_exp_neg_mul_Ioi (a := (m : ℝ) + 1) (by positivity) hr
  rw [Real.Gamma_nat_eq_factorial, add_sub_cancel_right] at h
  have hL : ∫ y in Ioi 0, y ^ m * Real.exp (-(r * y)) =
      ∫ t in Ioi 0, t ^ (m : ℝ) * Real.exp (-(r * t)) := by
    refine setIntegral_congr_fun measurableSet_Ioi fun t _ => ?_
    simp only [Real.rpow_natCast]
  rw [hL, h]
  have hpow : (1 / r) ^ ((m : ℝ) + 1) = (1 / r) ^ (m + 1) := by
    rw [show ((m : ℝ) + 1) = ((m + 1 : ℕ) : ℝ) by push_cast; ring, Real.rpow_natCast]
  rw [hpow, one_div_pow, div_mul_eq_mul_div, one_mul]

/-- Polynomial factors are integrable against a decreasing exponential. -/
theorem integrableOn_pow_mul_exp_neg_mul (m : ℕ) {r : ℝ} (hr : 0 < r) :
    IntegrableOn (fun y : ℝ => y ^ m * Real.exp (-(r * y))) (Ioi 0) := by
  have h := Real.GammaIntegral_convergent (s := (m : ℝ) + 1) (by positivity)
  rw [add_sub_cancel_right] at h
  have h2 : IntegrableOn (fun x : ℝ => Real.exp (-(r * x)) * (r * x) ^ (m : ℝ)) (Ioi 0) := by
    have hcomp := (integrableOn_Ioi_comp_mul_left_iff
      (fun x : ℝ => Real.exp (-x) * x ^ (m : ℝ)) 0 hr).mpr (by simpa using h)
    simpa using hcomp
  have h3 : IntegrableOn
      (fun x : ℝ => (1 / r ^ m) * (Real.exp (-(r * x)) * (r * x) ^ (m : ℝ)))
      (Ioi 0) := h2.const_mul _
  refine h3.congr_fun (fun x _hx => ?_) measurableSet_Ioi
  simp only
  rw [Real.rpow_natCast, mul_pow]
  field_simp

end ZetaFive.Common

