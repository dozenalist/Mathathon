module

/-
Copyright (c) 2026 ZetaFive contributors. All rights reserved.
Released under Apache 2.0 license; see ZetaFive/Lean/LICENSES/mo271-Zeta5.txt.

The coefficient argument is adapted from `Apery/Positivity.lean` in
https://github.com/mo271/zeta5, commit 7fe736760f4b96bfdb4334b68e3b3124ecbe10b0,
released under the Apache 2.0 license. The functional formulation below is independent
of the zeta value, weight, and rational modifier.
-/
public import Mathlib.Algebra.Polynomial.BigOperators
public import Mathlib.Algebra.Polynomial.Eval.SMul
public import Mathlib.Algebra.Polynomial.Roots
public import Mathlib.Analysis.SpecialFunctions.Sqrt
public import Mathlib.LinearAlgebra.Matrix.PosDef
public import Mathlib.MeasureTheory.Integral.Bochner.Set
public import Mathlib.MeasureTheory.Measure.Lebesgue.Basic
public import Mathlib.Tactic.Ring

@[expose] public section

/-!
# Positive Hankel determinants from a positive polynomial functional

For any real linear functional `L` on real polynomials which is strictly positive on
nonzero squares, the Hankel matrix `L(X^(i+j))` is positive definite and has positive
determinant. The proof expands its quadratic form as `L(q^2)` and recovers the
coefficients of `q` to prove `q ≠ 0`.

The hypothesis on `L` must be supplied by a moment representation in applications.
This module does not assume a particular zeta value or a particular integral formula.
-/

open Polynomial Finset
open scoped Matrix

namespace ZetaFive.Common

/-- The polynomial with the given finite vector as its coefficients. -/
noncomputable def coefficientPolynomial {n : ℕ} (x : Fin n → ℝ) : ℝ[X] :=
  ∑ i : Fin n, C (x i) * X ^ (i : ℕ)

@[simp] theorem coefficientPolynomial_coeff {n : ℕ} (x : Fin n → ℝ) (i : Fin n) :
    (coefficientPolynomial x).coeff (i : ℕ) = x i := by
  classical
  simp only [coefficientPolynomial, finsetSum_coeff, coeff_C_mul_X_pow]
  rw [Finset.sum_eq_single i]
  · simp
  · intro b _ hb
    rw [ite_eq_right]
    exact fun h => hb (Fin.ext h.symm)
  · intro h
    exact absurd (Finset.mem_univ i) h

theorem coefficientPolynomial_ne_zero {n : ℕ} {x : Fin n → ℝ} (hx : x ≠ 0) :
    coefficientPolynomial x ≠ 0 := by
  intro h
  apply hx
  funext i
  have hc := coefficientPolynomial_coeff x i
  rw [h, coeff_zero] at hc
  exact hc.symm

/-- The Hankel matrix associated to a polynomial moment functional. -/
noncomputable def momentHankel (L : ℝ[X] →ₗ[ℝ] ℝ) (n : ℕ) :
    Matrix (Fin n) (Fin n) ℝ :=
  fun i j => L (X ^ ((i : ℕ) + (j : ℕ)))

/-- Expanding the square of the coefficient polynomial gives the Gram quadratic form. -/
theorem momentHankel_quadratic (L : ℝ[X] →ₗ[ℝ] ℝ) {n : ℕ} (x : Fin n → ℝ) :
    star x ⬝ᵥ (momentHankel L n *ᵥ x) = L ((coefficientPolynomial x) ^ 2) := by
  classical
  have hp : (coefficientPolynomial x) ^ 2 =
      ∑ i : Fin n, ∑ j : Fin n,
        (x i * x j) • (X ^ ((i : ℕ) + (j : ℕ)) : ℝ[X]) := by
    simp only [coefficientPolynomial, pow_two, Finset.sum_mul_sum]
    refine Finset.sum_congr rfl fun i _ => Finset.sum_congr rfl fun j _ => ?_
    rw [Polynomial.smul_eq_C_mul, map_mul, pow_add]
    ring
  rw [hp]
  simp only [map_sum, map_smul, smul_eq_mul, dotProduct, Matrix.mulVec,
    momentHankel, star_trivial, Finset.mul_sum]
  refine Finset.sum_congr rfl fun i _ => Finset.sum_congr rfl fun j _ => ?_
  ring

/-- Strict positivity on nonzero polynomial squares implies positive definiteness
of every finite moment Hankel matrix. This includes the empty matrix. -/
theorem momentHankel_posDef (L : ℝ[X] →ₗ[ℝ] ℝ)
    (hL : ∀ p : ℝ[X], p ≠ 0 → 0 < L (p ^ 2)) (n : ℕ) :
    (momentHankel L n).PosDef := by
  refine Matrix.PosDef.of_dotProduct_mulVec_pos ?_ ?_
  · refine Matrix.IsHermitian.ext fun i j => ?_
    simp only [momentHankel, star_trivial, Nat.add_comm]
  · intro x hx
    rw [momentHankel_quadratic]
    exact hL _ (coefficientPolynomial_ne_zero hx)

/-- Positivity, hence nonvanishing, of the determinant is independent of `k`.
In the zeta construction, the analytic moment representation supplies `hL`. -/
theorem momentHankel_det_pos (L : ℝ[X] →ₗ[ℝ] ℝ)
    (hL : ∀ p : ℝ[X], p ≠ 0 → 0 < L (p ^ 2)) (n : ℕ) :
    0 < (momentHankel L n).det :=
  (momentHankel_posDef L hL n).det_pos

open MeasureTheory Set

/-- Integration against a weight on the positive half-line, with the square change
of variables used by the zeta construction. Integrability is required for every
polynomial so that this is a genuine linear functional. -/
noncomputable def polynomialIntegral (ν : ℝ → ℝ)
    (hint : ∀ p : ℝ[X], IntegrableOn (fun y => p.eval (y ^ 2) * ν y) (Set.Ioi 0)) :
    ℝ[X] →ₗ[ℝ] ℝ where
  toFun p := ∫ y in Set.Ioi 0, p.eval (y ^ 2) * ν y
  map_add' p q := by
    simp only [eval_add, add_mul]
    exact integral_add (hint p) (hint q)
  map_smul' c p := by
    simp only [eval_smul, smul_eq_mul, mul_assoc, RingHom.id_apply]
    exact integral_const_mul c _

/-- A weight strictly positive on `(0,∞)` integrates every nonzero polynomial
square to a positive number. The finite zero set cannot exhaust that interval. -/
theorem polynomialIntegral_square_pos (ν : ℝ → ℝ)
    (hint : ∀ p : ℝ[X], IntegrableOn (fun y => p.eval (y ^ 2) * ν y) (Set.Ioi 0))
    (hν : ∀ y : ℝ, 0 < y → 0 < ν y) (p : ℝ[X]) (hp : p ≠ 0) :
    0 < polynomialIntegral ν hint (p ^ 2) := by
  classical
  change 0 < ∫ y in Set.Ioi 0, (p ^ 2).eval (y ^ 2) * ν y
  simp only [eval_pow]
  have hsq : IntegrableOn (fun y => p.eval (y ^ 2) ^ 2 * ν y) (Set.Ioi 0) := by
    exact (hint (p ^ 2)).congr_fun
      (fun y _ => by
        change (p ^ 2).eval (y ^ 2) * ν y = p.eval (y ^ 2) ^ 2 * ν y
        rw [Polynomial.eval_pow]) measurableSet_Ioi
  have hnn : 0 ≤ᵐ[volume.restrict (Set.Ioi 0)] fun y => p.eval (y ^ 2) ^ 2 * ν y := by
    refine (ae_restrict_iff' measurableSet_Ioi).mpr
      (Filter.Eventually.of_forall fun y hy => ?_)
    exact mul_nonneg (sq_nonneg _) (hν y hy).le
  rw [setIntegral_pos_iff_support_of_nonneg_ae hnn hsq]
  have hroots : Set.Finite {t : ℝ | IsRoot p t} := Polynomial.finite_setOfPred_isRoot hp
  have hzeros : Set.Finite {y : ℝ | IsRoot p (y ^ 2)} := by
    refine (hroots.image Real.sqrt |>.union (hroots.image fun t => -Real.sqrt t)).subset ?_
    intro y hy
    simp only [Set.mem_ofPred_eq] at hy
    rcases le_or_gt 0 y with hy0 | hy0
    · exact Or.inl ⟨y ^ 2, hy, Real.sqrt_sq hy0⟩
    · exact Or.inr ⟨y ^ 2, hy, by
        show -Real.sqrt (y ^ 2) = y
        rw [Real.sqrt_sq_eq_abs, abs_of_neg hy0, neg_neg]⟩
  have hsub : Set.Ioi 0 \ {y : ℝ | IsRoot p (y ^ 2)} ⊆
      Function.support (fun y => p.eval (y ^ 2) ^ 2 * ν y) ∩ Set.Ioi 0 := by
    intro y hy
    obtain ⟨hy0, hyp⟩ := hy
    refine ⟨?_, hy0⟩
    exact mul_ne_zero (pow_ne_zero _ hyp) (hν y hy0).ne'
  calc (0 : ENNReal) < ⊤ := ENNReal.zero_lt_top
    _ = volume (Set.Ioi (0 : ℝ) \ {y : ℝ | IsRoot p (y ^ 2)}) := by
      rw [measure_sdiff_null (hzeros.measure_zero volume), Real.volume_Ioi]
    _ ≤ _ := measure_mono hsub

/-- The positive-weight integral matrix has a strictly positive determinant, for
every size, independently of the zeta exponent and rational modifier. -/
theorem integralHankel_det_pos (ν : ℝ → ℝ)
    (hint : ∀ p : ℝ[X], IntegrableOn (fun y => p.eval (y ^ 2) * ν y) (Set.Ioi 0))
    (hν : ∀ y : ℝ, 0 < y → 0 < ν y) (n : ℕ) :
    0 < (momentHankel (polynomialIntegral ν hint) n).det :=
  momentHankel_det_pos _ (polynomialIntegral_square_pos ν hint hν) n

end ZetaFive.Common

