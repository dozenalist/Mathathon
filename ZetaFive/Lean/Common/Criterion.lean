module

/-
Adapted from `Apery/Criterion.lean` in mo271/Zeta5,
https://github.com/mo271/Zeta5, commit 7fe736760f4b96bfdb4334b68e3b3124ecbe10b0.
The upstream development is licensed under the Apache License, Version 2.0.
The degree slope and quadratic decay coefficient are arbitrary in this version.
-/
public import Mathlib.NumberTheory.Real.Irrational
public import Mathlib.Analysis.SpecialFunctions.Log.Basic
public import Mathlib.Algebra.Polynomial.Degree.Operations
public import Mathlib.Algebra.Polynomial.AlgebraMap
public import Mathlib.Tactic.FieldSimp
public import Mathlib.Tactic.Linarith
public import Mathlib.Tactic.NormNum
public import Mathlib.Tactic.Positivity
public import Mathlib.Tactic.Ring

@[expose] public section

/-!
# Integer-polynomial irrationality criterion

This is the common final step in the Hankel-determinant method. None of the
arguments in this file depends on a zeta weight, a moment functional, or a choice
of determinant parameters. The input is a supply of integer polynomials of
linearly bounded degree with positive, quadratically exponentially small values.
-/

open Polynomial Filter Topology

namespace ZetaFive.Common

/-- Clearing the denominator of a rational argument in an integer polynomial. -/
lemma pow_mul_aeval_div_eq_intCast (p : ℤ[X]) {d : ℕ} (hd : p.natDegree ≤ d)
    (a b : ℤ) (hb : b ≠ 0) :
    (b : ℝ) ^ d * aeval ((a : ℝ) / b) p =
      ((∑ k ∈ Finset.range (d + 1), p.coeff k * a ^ k * b ^ (d - k) : ℤ) : ℝ) := by
  have hbr : (b : ℝ) ≠ 0 := by exact_mod_cast hb
  have hlt : (p.map (algebraMap ℤ ℝ)).natDegree < d + 1 :=
    lt_of_le_of_lt natDegree_map_le (by omega)
  rw [aeval_def, eval₂_eq_eval_map, eval_eq_sum_range' hlt, Finset.mul_sum]
  push_cast
  refine Finset.sum_congr rfl fun k hk => ?_
  rw [Finset.mem_range] at hk
  have hpow : (b : ℝ) ^ d = (b : ℝ) ^ (d - k) * (b : ℝ) ^ k := by
    rw [← pow_add]
    congr 1
    omega
  rw [coeff_map, hpow, div_pow]
  simp only [algebraMap_int_eq, eq_intCast]
  field_simp

/-- A general criterion permitting a different polynomial at each index. -/
theorem irrational_of_eventually_exists_int_poly (ξ : ℝ) (d : ℕ → ℕ) (ε : ℕ → ℝ)
    (hε : ∀ b : ℕ, 0 < b → Tendsto (fun n => (b : ℝ) ^ d n * ε n) atTop (𝓝 0))
    (h : ∀ᶠ n in atTop, ∃ Q : ℤ[X],
      Q.natDegree ≤ d n ∧ 0 < aeval ξ Q ∧ aeval ξ Q ≤ ε n) :
    Irrational ξ := by
  rintro ⟨q, hq⟩
  have hξ : ξ = ((q.num : ℤ) : ℝ) / ((q.den : ℤ) : ℝ) := by
    rw [← hq, Rat.cast_def, Int.cast_natCast]
  have hb0 : 0 < q.den := q.den_pos
  have hbR : (0 : ℝ) < (q.den : ℝ) := by exact_mod_cast hb0
  have hsmall : ∀ᶠ n in atTop, (q.den : ℝ) ^ d n * ε n < 1 :=
    (hε q.den hb0).eventually (gt_mem_nhds one_pos)
  obtain ⟨n, ⟨Q, hdeg, hpos, hle⟩, hlt⟩ := (h.and hsmall).exists
  obtain ⟨m, hm⟩ : ∃ m : ℤ, (m : ℝ) = (q.den : ℝ) ^ d n * aeval ξ Q := by
    refine ⟨∑ k ∈ Finset.range (d n + 1),
      Q.coeff k * q.num ^ k * (q.den : ℤ) ^ (d n - k), ?_⟩
    have key := pow_mul_aeval_div_eq_intCast Q hdeg q.num (q.den : ℤ)
      (by exact_mod_cast hb0.ne')
    rw [hξ, ← key]
    simp only [Int.cast_natCast]
  have hm_pos : (0 : ℝ) < m := by
    rw [hm]
    exact mul_pos (pow_pos hbR _) hpos
  have hm_ge : (1 : ℝ) ≤ m := by
    have : (0 : ℤ) < m := by exact_mod_cast hm_pos
    exact_mod_cast this
  have hm_lt : (m : ℝ) < 1 := by
    rw [hm]
    calc (q.den : ℝ) ^ d n * aeval ξ Q ≤ (q.den : ℝ) ^ d n * ε n :=
        mul_le_mul_of_nonneg_left hle (pow_nonneg hbR.le _)
      _ < 1 := hlt
  linarith

/-- Any quadratic exponential decay beats the denominator cost for linear degree. -/
theorem tendsto_pow_mul_exp_neg_sq_of_pos {c : ℝ} (hc : 0 < c)
    (d b : ℕ) (hb : 0 < b) :
    Tendsto (fun n : ℕ => (b : ℝ) ^ (d * n) * Real.exp (-c * (n : ℝ) ^ 2))
      atTop (𝓝 0) := by
  have hbR : (0 : ℝ) < b := by exact_mod_cast hb
  have hrw : ∀ n : ℕ, (b : ℝ) ^ (d * n) * Real.exp (-c * (n : ℝ) ^ 2) =
      Real.exp ((d * n) * Real.log b - c * (n : ℝ) ^ 2) := by
    intro n
    have hbpow : (0 : ℝ) < (b : ℝ) ^ (d * n) := pow_pos hbR _
    rw [← Real.exp_log hbpow, ← Real.exp_add, Real.log_pow]
    congr 1
    push_cast
    ring
  simp_rw [hrw]
  have hexp : Tendsto (fun n : ℕ => Real.exp (-(n : ℝ))) atTop (𝓝 0) :=
    Real.tendsto_exp_neg_atTop_nhds_zero.comp tendsto_natCast_atTop_atTop
  refine squeeze_zero' (Eventually.of_forall fun n => (Real.exp_pos _).le) ?_ hexp
  filter_upwards [eventually_ge_atTop (⌈((d : ℝ) * Real.log b + 1) / c⌉₊)] with n hn
  apply Real.exp_le_exp.mpr
  have hn' : ((d : ℝ) * Real.log b + 1) / c ≤ (n : ℝ) :=
    le_trans (Nat.le_ceil _) (by exact_mod_cast hn)
  have hn'' : (d : ℝ) * Real.log b + 1 ≤ c * n := by
    rw [div_le_iff₀ hc] at hn'
    linarith
  have hn0 : (0 : ℝ) ≤ n := Nat.cast_nonneg n
  nlinarith [mul_le_mul_of_nonneg_left hn'' hn0]

/-- The common final theorem for determinants of degree at most `d * n`. -/
theorem irrational_of_eventually_exists_int_poly_exp (ξ : ℝ) (d : ℕ)
    {c : ℝ} (hc : 0 < c)
    (h : ∀ᶠ n in atTop, ∃ Q : ℤ[X], Q.natDegree ≤ d * n ∧
      0 < aeval ξ Q ∧ aeval ξ Q ≤ Real.exp (-c * (n : ℝ) ^ 2)) :
    Irrational ξ :=
  irrational_of_eventually_exists_int_poly ξ (fun n => d * n)
    (fun n => Real.exp (-c * (n : ℝ) ^ 2))
    (tendsto_pow_mul_exp_neg_sq_of_pos hc d) h

end ZetaFive.Common

