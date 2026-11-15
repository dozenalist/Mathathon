module

/-
Copyright (c) 2026 the mo271/Zeta5 contributors. All rights reserved.
Released under Apache 2.0 license as described in ZetaFive/Lean/LICENSES/mo271-Zeta5.txt.
Adapted from mo271/Zeta5, commit 7fe736760f4b96bfdb4334b68e3b3124ecbe10b0.
The square-node and affine-determinant arguments are independent of the zeta index.
-/
public import Mathlib.Algebra.BigOperators.Intervals
public import Mathlib.Algebra.Order.BigOperators.GroupWithZero.Finset
public import Mathlib.Algebra.Algebra.Rat
public import Mathlib.Algebra.Polynomial.AlgebraMap
public import Mathlib.Algebra.Polynomial.BigOperators
public import Mathlib.Algebra.Polynomial.Derivative
public import Mathlib.Basic.Real.Basic
public import Mathlib.Data.Fintype.BigOperators
public import Mathlib.Data.Rat.Cast.Lemmas
public import Mathlib.Tactic.Linarith
public import Mathlib.Tactic.LinearCombination
public import Mathlib.Tactic.NormNum
public import Mathlib.Tactic.Positivity
public import Mathlib.Tactic.Ring

@[expose] public section

/-! # The common square-node polynomial

The factor `D m = ∏ j ∈ Icc 1 m, (X + j²)` and all of its algebraic
properties below are independent of the zeta index and of the scaling parameters.
-/

open Polynomial Finset

namespace ZetaFive.Common

/-- The common denominator, with simple roots at the negative integer squares. -/
noncomputable def D (m : ℕ) : ℚ[X] := ∏ j ∈ Icc 1 m, (X + C ((j : ℚ) ^ 2))

/-- The coefficient of the simple pole at `-j²` of `P / D K`. -/
noncomputable def res (K : ℕ) (P : ℚ[X]) (j : ℕ) : ℚ :=
  P.eval (-(j : ℚ) ^ 2) / (derivative (D K)).eval (-(j : ℚ) ^ 2)
lemma D_monic (K : ℕ) : (D K).Monic := by
  unfold D; exact monic_prod_of_monic _ _ fun j _ => monic_X_add_C _

lemma natDegree_D (K : ℕ) : (D K).natDegree = K := by
  unfold D; rw [natDegree_prod_of_monic _ _ fun j _ => monic_X_add_C _]
  simp only [natDegree_X_add_C, Finset.sum_const, smul_eq_mul, mul_one, Nat.card_Icc]
  omega

lemma eval_D (m : ℕ) (x : ℚ) : (D m).eval x = ∏ j ∈ Icc 1 m, (x + (j : ℚ) ^ 2) := by
  simp [D, eval_prod]

lemma eval_D_eq_zero {m j : ℕ} (hj : j ∈ Icc 1 m) : (D m).eval (-(j : ℚ) ^ 2) = 0 := by
  rw [eval_D]
  exact Finset.prod_eq_zero hj (by ring)

lemma eval_D_ne_zero {m j : ℕ} (hj : m < j) : (D m).eval (-(j : ℚ) ^ 2) ≠ 0 := by
  rw [eval_D]
  refine Finset.prod_ne_zero_iff.mpr fun i hi => ?_
  rw [Finset.mem_Icc] at hi
  have h1 : (i : ℚ) < j := by exact_mod_cast (by omega : i < j)
  have h2 : (0 : ℚ) ≤ i := by positivity
  nlinarith

lemma eval_derivative_D {K j : ℕ} (hj : j ∈ Icc 1 K) :
    (derivative (D K)).eval (-(j : ℚ) ^ 2) = ∏ i ∈ (Icc 1 K).erase j, ((i : ℚ) ^ 2 - (j : ℚ) ^ 2) := by
  rw [D, derivative_prod_finset, eval_finsetSum, Finset.sum_eq_single j]
  · simp only [derivative_add, derivative_X, derivative_C, add_zero, mul_one,
      eval_prod, eval_add, eval_X, eval_C]
    exact Finset.prod_congr rfl fun i _ => by ring
  · intro b _ hb
    rw [eval_mul, eval_prod]
    exact mul_eq_zero_of_left (Finset.prod_eq_zero (Finset.mem_erase.mpr ⟨hb.symm, hj⟩) (by simp)) _
  · intro h; exact absurd hj h

lemma eval_derivative_D_ne_zero {K j : ℕ} (hj : j ∈ Icc 1 K) :
    (derivative (D K)).eval (-(j : ℚ) ^ 2) ≠ 0 := by
  rw [eval_derivative_D hj]
  refine Finset.prod_ne_zero_iff.mpr fun i hi => ?_
  have hij : i ≠ j := (Finset.mem_erase.mp hi).1
  have : (i : ℚ) ≠ j := by exact_mod_cast hij
  have h0i : (0 : ℚ) ≤ i := by positivity
  have h0j : (0 : ℚ) ≤ j := by positivity
  intro h
  have hfac : ((i : ℚ) - j) * ((i : ℚ) + j) = 0 := by linear_combination h
  rcases mul_eq_zero.mp hfac with h' | h'
  · exact this (by linarith)
  · have hj1 : (1 : ℚ) ≤ j := by exact_mod_cast (Finset.mem_Icc.mp hj).1
    linarith

lemma aeval_D_pos (m : ℕ) {t : ℝ} (ht : 0 ≤ t) : 0 < aeval t (D m) := by
  simp only [D, map_prod, map_add, aeval_X, aeval_C, eq_ratCast, Rat.cast_pow, Rat.cast_natCast]
  refine Finset.prod_pos fun j hj => ?_
  have h1 : (1 : ℝ) ≤ j := by exact_mod_cast (Finset.mem_Icc.mp hj).1
  positivity

/-- The common denominator is never the zero polynomial, including at `m = 0`. -/
lemma D_ne_zero (m : ℕ) : D m ≠ 0 := (D_monic m).ne_zero

@[simp] lemma D_zero : D 0 = 1 := by simp [D]

/-- The `h` square nodes after the first `N` nodes have been cancelled. -/
noncomputable def squareNode (N h : ℕ) (i : Fin h) : ℚ :=
  -((N + 1 + (i : ℕ) : ℕ) : ℚ) ^ 2

lemma squareNode_injective (N h : ℕ) : Function.Injective (squareNode N h) := by
  intro i j hij
  simp only [squareNode, neg_inj] at hij
  have hnat : (N + 1 + (i : ℕ)) ^ 2 = (N + 1 + (j : ℕ)) ^ 2 := by
    exact_mod_cast hij
  have heq := Nat.pow_left_injective (by norm_num : 2 ≠ 0) hnat
  exact Fin.ext (by omega)

/-- Reindexing the remaining poles after the first `N` residues vanish. -/
lemma sum_Icc_eq_sum_fin (N K : ℕ) (hNK : N ≤ K) (f : ℕ → ℚ)
    (hf : ∀ j ∈ Icc 1 N, f j = 0) :
    ∑ j ∈ Icc 1 K, f j = ∑ k : Fin (K - N), f (N + 1 + k) := by
  rw [Fin.sum_univ_eq_sum_range (fun k => f (N + 1 + k)) (K - N)]
  have h1 := Finset.sum_Ico_eq_sum_range f (N + 1) (K + 1)
  rw [show K + 1 - (N + 1) = K - N by omega] at h1
  rw [← h1]
  have h2 : Icc 1 K = Ico 1 (K + 1) := by
    ext x; simp only [Finset.mem_Icc, Finset.mem_Ico]; omega
  rw [h2, ← Finset.sum_Ico_consecutive f (show 1 ≤ N + 1 by omega) (show N + 1 ≤ K + 1 by omega)]
  rw [Finset.sum_eq_zero (fun j hj => hf j ?_), zero_add]
  rw [Finset.mem_Ico] at hj
  rw [Finset.mem_Icc]; omega

end ZetaFive.Common

