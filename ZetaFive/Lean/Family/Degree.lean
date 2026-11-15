module

/-
Copyright (c) 2026 the mo271/Zeta5 contributors. All rights reserved.
Released under Apache 2.0 license as described in ZetaFive/Lean/LICENSES/mo271-Zeta5.txt.
Adapted from Apery/Degree.lean in mo271/Zeta5,
commit 7fe736760f4b96bfdb4334b68e3b3124ecbe10b0.
Generalized to arbitrary zeta index and family parameters.
-/
public import ZetaFive.Lean.Family.Construction

@[expose] public section

/-! # Exact degree of the whole Hankel family

The rational moments contribute only to the constant matrix. The leading
coefficient is the determinant of a power-sum matrix at distinct square nodes.
The common Vandermonde argument therefore proves the degree for every `k`.
-/

open Polynomial Matrix Finset
open ZetaFive.Common

namespace ZetaFive

/-- Weights of the discrete measure giving the linear coefficient matrix. -/
noncomputable def residueWeight (k : ℕ) (p : Parameters) (i : Fin p.h) : ℚ :=
  (D p.N).eval (squareNode p.N p.h i) ^ p.numeratorPower *
      ((p.N + 1 + (i : ℕ) : ℕ) : ℚ) ^ (k - 1) /
    (derivative (D p.K)).eval (squareNode p.N p.h i)

theorem coefficient_matrix_eq_power_sum (k : ℕ) (p : Parameters)
    (hNK : p.N ≤ p.K) (hsize : p.h = p.K - p.N) (hr : 1 ≤ p.numeratorPower) :
    (Matrix.of fun i j : Fin p.h => (hankel k p i j).coeff 1) =
      (Matrix.of fun i j : Fin p.h =>
        ∑ a : Fin p.h, residueWeight k p a * squareNode p.N p.h a ^ (i.val + j.val)) := by
  ext i j
  simp only [Matrix.of_apply, hankel, mu_coeff_one, res]
  rw [sum_Icc_eq_sum_fin p.N p.K hNK
    (fun a => eval (-(a : ℚ) ^ 2) (D p.N ^ p.numeratorPower * X ^ (i.val + j.val)) /
      eval (-(a : ℚ) ^ 2) (derivative (D p.K)) * (a : ℚ) ^ (k - 1))
    (fun a ha => by
      rw [eval_mul, eval_pow, eval_D_eq_zero ha, zero_pow (by omega : p.numeratorPower ≠ 0)]
      simp)]
  rw [← hsize]
  refine Finset.sum_congr rfl fun a _ => ?_
  simp only [residueWeight, squareNode, eval_mul, eval_pow, eval_X]
  ring

theorem residueWeight_ne_zero (k : ℕ) (p : Parameters)
    (hsize : p.h = p.K - p.N) (i : Fin p.h) : residueWeight k p i ≠ 0 := by
  have hi := i.isLt
  have hnum : (D p.N).eval (squareNode p.N p.h i) ≠ 0 :=
    eval_D_ne_zero (by omega)
  have hden : (derivative (D p.K)).eval (squareNode p.N p.h i) ≠ 0 :=
    eval_derivative_D_ne_zero (by rw [Finset.mem_Icc]; omega)
  have hnode : ((p.N + 1 + (i : ℕ) : ℕ) : ℚ) ≠ 0 := by positivity
  unfold residueWeight
  exact div_ne_zero (mul_ne_zero (pow_ne_zero _ hnum) (pow_ne_zero _ hnode)) hden

theorem delta_top_coefficient_ne_zero (k : ℕ) (p : Parameters)
    (hNK : p.N ≤ p.K) (hsize : p.h = p.K - p.N) (hr : 1 ≤ p.numeratorPower) :
    (delta k p).coeff p.h ≠ 0 := by
  rw [delta_top_coefficient, coefficient_matrix_eq_power_sum k p hNK hsize hr]
  exact det_power_sum_matrix_ne_zero (squareNode p.N p.h) (residueWeight k p)
    (squareNode_injective p.N p.h) (residueWeight_ne_zero k p hsize)

/-- The determinant has degree exactly the number of surviving poles. -/
theorem delta_natDegree (k : ℕ) (p : Parameters)
    (hNK : p.N ≤ p.K) (hsize : p.h = p.K - p.N) (hr : 1 ≤ p.numeratorPower) :
    (delta k p).natDegree = p.h :=
  natDegree_eq_of_le_of_coeff_ne_zero (delta_natDegree_le k p)
    (delta_top_coefficient_ne_zero k p hNK hsize hr)

theorem normalized_natDegree (k : ℕ) (p : Parameters)
    (hNK : p.N ≤ p.K) (hsize : p.h = p.K - p.N) (hr : 1 ≤ p.numeratorPower) :
    (normalized k p).natDegree = p.h := by
  rw [normalized, natDegree_C_mul (scale_pos p).ne', delta_natDegree k p hNK hsize hr]

theorem lai_degree (k n : ℕ) :
    (normalized k (laiParameters n)).natDegree = 37 * n := by
  exact normalized_natDegree k (laiParameters n) (by simp [laiParameters]; omega)
    (laiParameters_size n) (by simp [laiParameters])

theorem calegari_degree (k n : ℕ) :
    (normalized k (calegariParameters n)).natDegree = 11 * n := by
  exact normalized_natDegree k (calegariParameters n) (by simp only [calegariParameters]; omega)
    (calegariParameters_size n) (by simp [calegariParameters])

end ZetaFive

