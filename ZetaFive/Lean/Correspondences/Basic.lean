/-
Copyright (c) 2026 Mathathon contributors. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
-/
import Mathlib

/-!
# Shared definitions for the ζ(5) correspondence lemmas

This module freezes the objects that the correspondence lemmas
(`Transport.lean`, `AffineParameter.lean`, `Matrix.lean`) relate.
Source: `zeta5_unified_framework.tex` (14 November 2026), Sections 1–4.

We keep three variables strictly apart, as the source note requires:

* `PolyT` is the ring `ℚ[t]` carrying the moment functional `μ`;
* `PolyX` is the ring `ℚ[x]` carrying the Bernoulli functional `τ`;
* the boundary constant is a rational parameter `u : ℚ` (written `X` in the note).

`PolyT` and `PolyX` are definitionally the same ring; the two names are a
documentation device, and every statement below says explicitly which variable
it speaks about.

## Bernoulli convention

`bernoulli` is Mathlib's Bernoulli number, defined by `x/(e^x-1) = Σ B_n x^n/n!`,
hence `bernoulli 1 = -1/2`. The source note requires exactly this convention,
and it is the value `τ(x⁴) = -1/2` in `Transport.lean` that tests it: with
`B_1 = +1/2` that value would be `+1/2`. (`τ(x³) = 1/4` tests only `B_0 = 1`.)
-/

namespace ZetaFive.Correspondences

noncomputable section

open scoped BigOperators
open Polynomial

/-- `ℚ[t]`: the rational-function variable of the moment functional. -/
abbrev PolyT := Polynomial ℚ

/-- `ℚ[x]`: the pullback variable of the Bernoulli functional. -/
abbrev PolyX := Polynomial ℚ

/-! ## Fifth harmonic sums -/

/-- `H^{(5)}_j = 1^{-5} + 2^{-5} + ⋯ + j^{-5}`, with `H^{(5)}_0 = 0`. -/
def H5 (j : ℕ) : ℚ := ∑ i ∈ Finset.range j, (((i : ℕ) + 1 : ℚ))⁻¹ ^ 5

@[simp] lemma H5_zero : H5 0 = 0 := by simp [H5]

lemma H5_succ (j : ℕ) : H5 (j + 1) = H5 j + (((j : ℕ) + 1 : ℚ))⁻¹ ^ 5 := by
  simp [H5, Finset.sum_range_succ]

/-- The finite harmonic increment: `H_j^{(5)} - H_{j-1}^{(5)} = j^{-5}` for `j ≥ 1`. -/
lemma H5_increment {j : ℕ} (hj : 1 ≤ j) : H5 j - H5 (j - 1) = ((j : ℚ))⁻¹ ^ 5 := by
  obtain ⟨k, rfl⟩ : ∃ k, j = k + 1 := ⟨j - 1, by omega⟩
  rw [H5_succ]
  push_cast
  ring

/-! ## The Bernoulli functional `L` and its derivative transform `τ` -/

/-- The Bernoulli moment functional `L(P) = Σ_k [x^k]P · B_k`, extended
`ℚ`-linearly from monomials. -/
def L (P : PolyX) : ℚ := P.sum fun n c => c * _root_.bernoulli n

@[simp] lemma L_zero : L 0 = 0 := by simp [L]

lemma L_monomial (n : ℕ) (a : ℚ) : L (monomial n a) = a * _root_.bernoulli n := by
  simp [L]

lemma L_C_mul_X_pow (a : ℚ) (n : ℕ) : L (C a * X ^ n) = a * _root_.bernoulli n := by
  rw [C_mul_X_pow_eq_monomial]
  exact L_monomial n a

lemma L_add (P Q : PolyX) : L (P + Q) = L P + L Q := by
  simp only [L]
  rw [Polynomial.sum_add_index P Q _ (fun i => by simp) (fun a b c => by ring)]

lemma L_C_mul (c : ℚ) (Q : PolyX) : L (C c * Q) = c * L Q := by
  induction Q using Polynomial.induction_on' with
  | add p q hp hq => rw [mul_add, L_add, hp, hq, L_add, mul_add]
  | monomial n a => rw [C_mul_monomial, L_monomial, L_monomial]; ring

/-- `τ(P) = L(P''')/24`, the differentiated Bernoulli summation functional. -/
def τ (P : PolyX) : ℚ := L (derivative (derivative (derivative P))) / 24

lemma τ_add (P Q : PolyX) : τ (P + Q) = τ P + τ Q := by
  simp only [τ, derivative_add, L_add]
  ring

lemma τ_C_mul (c : ℚ) (P : PolyX) : τ (C c * P) = c * τ P := by
  simp only [τ, derivative_C_mul, L_C_mul]
  ring

/-- The derivative of `C c * X^(k+1)`; the step that computes `τ` on monomials. -/
lemma derivative_C_mul_X_pow_succ (c : ℚ) (k : ℕ) :
    derivative (C c * (X : PolyX) ^ (k + 1)) = C (c * ((k + 1 : ℕ) : ℚ)) * X ^ k := by
  rw [derivative_mul, derivative_X_pow, derivative_C]
  simp only [zero_mul, Nat.add_sub_cancel]
  rw [← mul_assoc, ← C_mul]
  simp

/-! ## The moment functional `μ` and the pullback `t ↦ -x²` -/

/-- The coefficient of `t^e` under `μ`:
`(-1)^e B_{2e+2}(2e+3)(2e+4)(2e+5)/24`. This is the *independent* definition of
`μ`; it is not obtained from `τ` by transport. -/
def μcoeff (e : ℕ) : ℚ :=
  (-1 : ℚ) ^ e * _root_.bernoulli (2 * e + 2) * ((2 * e + 3 : ℕ) : ℚ)
    * ((2 * e + 4 : ℕ) : ℚ) * ((2 * e + 5 : ℕ) : ℚ) / 24

/-- `μ` on `ℚ[t]`, extended `ℚ`-linearly from the monomial values `μcoeff`. -/
def μpoly (P : PolyT) : ℚ := P.sum fun e c => c * μcoeff e

lemma μpoly_monomial (e : ℕ) (a : ℚ) : μpoly (monomial e a) = a * μcoeff e := by
  simp [μpoly]

lemma μpoly_add (P Q : PolyT) : μpoly (P + Q) = μpoly P + μpoly Q := by
  simp only [μpoly]
  rw [Polynomial.sum_add_index P Q _ (fun i => by simp) (fun a b c => by ring)]

/-- The substitution `t ↦ -x²`, as a `ℚ`-algebra homomorphism `ℚ[t] → ℚ[x]`. -/
def pull : PolyT →ₐ[ℚ] PolyX := aeval (-(X ^ 2))

lemma pull_neg_X_sq_pow (n : ℕ) :
    (-(X ^ 2) : PolyX) ^ n = C ((-1 : ℚ) ^ n) * X ^ (2 * n) := by
  have h : -(X ^ 2 : PolyX) = C (-1) * X ^ 2 := by simp
  rw [h, mul_pow, ← C_pow, ← pow_mul]

lemma pull_monomial (n : ℕ) (a : ℚ) :
    pull (monomial n a) = C (a * (-1 : ℚ) ^ n) * X ^ (2 * n) := by
  have h : pull (monomial n a) = C a * (-(X ^ 2) : PolyX) ^ n := by
    rw [pull, aeval_monomial, C_eq_algebraMap]
  rw [h, pull_neg_X_sq_pow, ← mul_assoc, ← C_mul]

end

end ZetaFive.Correspondences
