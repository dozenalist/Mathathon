module

/-
Copyright (c) 2026 the mo271/Zeta5 contributors. All rights reserved.
Released under Apache 2.0 license as described in ZetaFive/Lean/LICENSES/mo271-Zeta5.txt.
Adapted from mo271/Zeta5, commit 7fe736760f4b96bfdb4334b68e3b3124ecbe10b0.
The square-node and affine-determinant arguments are independent of the zeta index.
-/
public import Mathlib.Algebra.Polynomial.BigOperators
public import Mathlib.LinearAlgebra.Vandermonde
public import Mathlib.Tactic.Ring

@[expose] public section

/-! # Determinants of affine polynomial matrices -/

open Polynomial Matrix Finset

namespace ZetaFive.Common

lemma coeff_det_of_natDegree_le_one {R : Type*} [CommRing R] {n : ℕ}
    (M : Matrix (Fin n) (Fin n) R[X]) (hM : ∀ i j, (M i j).natDegree ≤ 1) :
    (M.det).coeff n = (Matrix.of fun i j => (M i j).coeff 1).det ∧ M.det.natDegree ≤ n := by
  constructor
  · rw [det_apply', det_apply', finsetSum_coeff]
    refine Finset.sum_congr rfl fun σ _ => ?_
    have hc := coeff_prod_of_natDegree_le (s := Finset.univ) (f := fun i => M (σ i) i) (n := 1)
      (fun i _ => hM _ _)
    simp only [Finset.card_univ, Fintype.card_fin, mul_one] at hc
    rw [← C_eq_intCast, coeff_C_mul, hc]
    simp
  · rw [det_apply']
    refine natDegree_sum_le_of_forall_le _ _ fun σ _ => ?_
    refine (natDegree_mul_le).trans ?_
    rw [natDegree_intCast, zero_add]
    refine (natDegree_prod_le _ _).trans ?_
    calc ∑ i : Fin n, (M (σ i) i).natDegree ≤ ∑ i : Fin n, 1 := Finset.sum_le_sum fun i _ => hM _ _
      _ = n := by simp


/-- An affine polynomial matrix has full determinant degree when its matrix of
linear coefficients is nonsingular. This criterion is independent of any moments. -/
theorem natDegree_det_eq_of_coeff_det_ne_zero {R : Type*} [CommRing R] {n : ℕ}
    (M : Matrix (Fin n) (Fin n) R[X])
    (hM : ∀ i j, (M i j).natDegree ≤ 1)
    (hcoeff : (Matrix.of fun i j => (M i j).coeff 1).det ≠ 0) :
    M.det.natDegree = n := by
  obtain ⟨hc, hd⟩ := coeff_det_of_natDegree_le_one M hM
  exact natDegree_eq_of_le_of_coeff_ne_zero hd (hc ▸ hcoeff)

/-- Distinct nodes and nonzero weights make the weighted Vandermonde Gram matrix
nonsingular. No positivity of the weights is required for this algebraic fact. -/
theorem det_vandermonde_gram_ne_zero {R : Type*} [CommRing R] [IsDomain R] {n : ℕ}
    (x w : Fin n → R) (hx : Function.Injective x) (hw : ∀ i, w i ≠ 0) :
    ((vandermonde x)ᵀ * diagonal w * vandermonde x).det ≠ 0 := by
  rw [det_mul, det_mul, det_transpose, det_diagonal]
  have hV : (vandermonde x).det ≠ 0 := det_vandermonde_ne_zero_iff.mpr hx
  exact mul_ne_zero (mul_ne_zero hV (Finset.prod_ne_zero_iff.mpr fun i _ => hw i)) hV

/-- The moment matrix of finitely many weighted nodes is a Vandermonde product. -/
theorem power_sum_matrix_eq_vandermonde {R : Type*} [CommRing R] {n : ℕ}
    (x w : Fin n → R) :
    (Matrix.of fun i j : Fin n => ∑ a : Fin n, w a * x a ^ (i.val + j.val)) =
      (vandermonde x)ᵀ * diagonal w * vandermonde x := by
  ext i j
  rw [Matrix.of_apply, Matrix.mul_apply]
  refine Finset.sum_congr rfl fun a _ => ?_
  simp only [Matrix.mul_diagonal, Matrix.transpose_apply, vandermonde_apply, pow_add]
  ring

/-- The determinant factors into the squared Vandermonde and the product of weights. -/
theorem det_power_sum_matrix {R : Type*} [CommRing R] {n : ℕ} (x w : Fin n → R) :
    (Matrix.of fun i j : Fin n => ∑ a : Fin n, w a * x a ^ (i.val + j.val)).det =
      (vandermonde x).det ^ 2 * ∏ i, w i := by
  rw [power_sum_matrix_eq_vandermonde, det_mul, det_mul, det_transpose, det_diagonal]
  ring

/-- A finite power-sum moment matrix at distinct nodes has nonzero determinant
when every weight is nonzero. This also covers the empty matrix. -/
theorem det_power_sum_matrix_ne_zero {R : Type*} [CommRing R] [IsDomain R] {n : ℕ}
    (x w : Fin n → R) (hx : Function.Injective x) (hw : ∀ i, w i ≠ 0) :
    (Matrix.of fun i j : Fin n => ∑ a : Fin n, w a * x a ^ (i.val + j.val)).det ≠ 0 := by
  rw [power_sum_matrix_eq_vandermonde]
  exact det_vandermonde_gram_ne_zero x w hx hw

end ZetaFive.Common

