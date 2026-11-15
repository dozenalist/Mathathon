module

/-
The lemma `one_div_one_sub_exp_neg_le` is adapted from `Apery/Weight.lean`
in mo271/Zeta5, https://github.com/mo271/Zeta5,
commit 7fe736760f4b96bfdb4334b68e3b3124ecbe10b0 (Apache-2.0).
-/
public import Mathlib.Analysis.SpecialFunctions.Exp
public import Mathlib.Analysis.SpecificLimits.Normed
public import Mathlib.Data.Nat.Choose.Basic
public import Mathlib.Tactic.FieldSimp
public import Mathlib.Tactic.Linarith
public import Mathlib.Tactic.NormNum
public import Mathlib.Tactic.Positivity
public import Mathlib.Tactic.Ring

@[expose] public section

/-! # Exponential and geometric-series bounds independent of the zeta family -/

open Filter Topology

namespace ZetaFive.Common

/-- An elementary bound for the denominator of an exponential geometric series. -/
lemma one_div_one_sub_exp_neg_le {x : ℝ} (hx : 0 < x) :
    1 / (1 - Real.exp (-x)) ≤ 1 + 1 / x := by
  have h1 : x + 1 ≤ Real.exp x := Real.add_one_le_exp x
  have h2 : Real.exp (-x) = 1 / Real.exp x := by rw [Real.exp_neg, one_div]
  have h3 : 0 < Real.exp x := Real.exp_pos x
  have h4 : Real.exp (-x) < 1 := by rw [h2, div_lt_one h3]; linarith
  rw [div_le_iff₀ (by linarith), h2]
  have hid : (1 + 1 / x) * (1 - 1 / Real.exp x) =
      1 + (Real.exp x - x - 1) / (x * Real.exp x) := by
    field_simp
    ring
  rw [hid]
  have : 0 ≤ (Real.exp x - x - 1) / (x * Real.exp x) :=
    div_nonneg (by linarith) (by positivity)
  linarith

lemma div_one_sub_exp_neg_le_add_one {x : ℝ} (hx : 0 < x) :
    x / (1 - Real.exp (-x)) ≤ 1 + x := by
  calc
    x / (1 - Real.exp (-x)) = x * (1 / (1 - Real.exp (-x))) := by ring
    _ ≤ x * (1 + 1 / x) :=
      mul_le_mul_of_nonneg_left (one_div_one_sub_exp_neg_le hx) hx.le
    _ = 1 + x := by field_simp; ring

/-- Bound an ordinary power by an ascending factorial, expressed using a binomial coefficient. -/
lemma succ_pow_le_factorial_mul_choose (n m : ℕ) :
    ((n : ℝ) + 1) ^ m ≤ (m.factorial : ℝ) * ((n + m).choose m : ℝ) := by
  have h := Nat.pow_succ_le_ascFactorial (n + 1) m
  rw [Nat.ascFactorial_eq_factorial_mul_choose] at h
  exact_mod_cast h

/-- A geometric moment bounded by the binomial generating series. -/
theorem tsum_succ_pow_mul_geometric_le (m : ℕ) {q : ℝ} (hq0 : 0 ≤ q) (hq1 : q < 1) :
    (∑' n : ℕ, ((n : ℝ) + 1) ^ m * q ^ (n + 1)) ≤
      (m.factorial : ℝ) * q / (1 - q) ^ (m + 1) := by
  have hnorm : ‖q‖ < 1 := by rw [Real.norm_eq_abs, abs_of_nonneg hq0]; exact hq1
  have hs0 : Summable (fun n : ℕ => (n : ℝ) ^ m * q ^ n) :=
    summable_pow_mul_geometric_of_norm_lt_one (r := q) m hnorm
  have hs1 : Summable (fun n : ℕ => ((n + 1 : ℕ) : ℝ) ^ m * q ^ (n + 1)) :=
    (summable_nat_add_iff (f := fun n : ℕ => (n : ℝ) ^ m * q ^ n) 1).mpr hs0
  have hs : Summable (fun n : ℕ => ((n : ℝ) + 1) ^ m * q ^ (n + 1)) := by
    simpa only [Nat.cast_add, Nat.cast_one] using hs1
  have hb0 : Summable (fun n : ℕ => ((n + m).choose m : ℝ) * q ^ n) :=
    summable_choose_mul_geometric_of_norm_lt_one (r := q) m hnorm
  have hb := hb0.mul_left ((m.factorial : ℝ) * q)
  have hterm : ∀ n : ℕ, ((n : ℝ) + 1) ^ m * q ^ (n + 1) ≤
      ((m.factorial : ℝ) * q) * (((n + m).choose m : ℝ) * q ^ n) := by
    intro n
    calc
      ((n : ℝ) + 1) ^ m * q ^ (n + 1) ≤
          ((m.factorial : ℝ) * ((n + m).choose m : ℝ)) * q ^ (n + 1) :=
        mul_le_mul_of_nonneg_right (succ_pow_le_factorial_mul_choose n m)
          (pow_nonneg hq0 _)
      _ = _ := by rw [pow_succ]; ring
  calc
    (∑' n : ℕ, ((n : ℝ) + 1) ^ m * q ^ (n + 1)) ≤
        ∑' n : ℕ, ((m.factorial : ℝ) * q) * (((n + m).choose m : ℝ) * q ^ n) :=
      hs.tsum_le_tsum hterm hb
    _ = _ := by
      rw [tsum_mul_left, tsum_choose_mul_geometric_of_norm_lt_one (r := q) m hnorm]
      ring

end ZetaFive.Common

