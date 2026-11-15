/-
Copyright (c) 2026 Mathathon contributors. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
-/
import Mathlib
import ZetaFive.Lean.Correspondences.Basic
import ZetaFive.Lean.Correspondences.Transport

/-!
# The Euler–Maclaurin operator identities of §2.1 (candidate work, member m1)

Source: `zeta5_unified_framework.tex` (reviewed 14 Nov 2026), §2.1,
`eq:EM`, `eq:difference`.

With `L(x^k) = B_k` and `τ = L ∘ ∂³/24` frozen in `Basic.lean`, the forward
difference of a polynomial is measured by fourth derivatives only
(`eq:difference`):

  `τ(P(x+1) - P(x)) = P⁗(0)/24`.

The formal core is the coefficient identity

  `L(Q(x+1) - Q(x)) = Q'(0)   for all Q : ℚ[x]`,

which reduces, by `Polynomial.sum_eq_of_subset` and `coeff_X_add_one_pow`, to
Mathlib's `sum_bernoulli` (`∑_{k<n} C(n,k)B_k = 0` for `n ≠ 1`) — the
"multiplying the symbol by `e^u-1`" step of the note's proof of `prop:axioms`,
done at the level of coefficients, with no generating function or infinite sum.

NOTE (toolchain): prototype only. Elaborated with Lean 4.33.1 against the
`/opt/mathlib` snapshot; the repository pins 4.35.0, which is not installed.
-/

namespace ZetaFive.Correspondences.M1

noncomputable section

open scoped BigOperators
open Polynomial

/-! ## `L` as a finite sum and its value on `(x+1)^n` -/

/-- `L` is additive over finite sums. -/
lemma L_finset_sum {ι : Type*} (s : Finset ι) (f : ι → PolyX) :
    L (∑ i ∈ s, f i) = ∑ i ∈ s, L (f i) := by
  classical
  induction s using Finset.induction_on with
  | empty => simp
  | insert a s ha ih => rw [Finset.sum_insert ha, Finset.sum_insert ha, L_add, ih]

lemma L_neg (P : PolyX) : L (-P) = -L P := by
  have h := L_C_mul (-1) P
  simpa using h

lemma L_sub (P Q : PolyX) : L (P - Q) = L P - L Q := by
  rw [sub_eq_add_neg, L_add, L_neg, sub_eq_add_neg]

lemma L_X_pow (n : ℕ) : L ((X : PolyX) ^ n) = _root_.bernoulli n := by
  simpa using L_C_mul_X_pow (1 : ℚ) n

/-- `L` read off any truncation of the coefficient list. -/
lemma L_eq_sum_range (Q : PolyX) :
    L Q = ∑ k ∈ Finset.range (Q.natDegree + 1), Q.coeff k * _root_.bernoulli k := by
  rw [L, sum_eq_of_subset (fun m c => c * _root_.bernoulli m) (fun i => by simp)]
  intro k hk
  rw [Finset.mem_range, Nat.lt_succ_iff]
  by_contra h
  push_neg at h
  exact (mem_support_iff.1 hk) (coeff_eq_zero_of_natDegree_lt h)

/-- `L((x+1)^n) = ∑_{k ≤ n} C(n,k) B_k`: the binomial expansion of the shift,
evaluated coefficientwise. -/
lemma L_X_add_one_pow (n : ℕ) :
    L (((X : PolyX) + 1) ^ n)
      = ∑ k ∈ Finset.range (n + 1), (n.choose k : ℚ) * _root_.bernoulli k := by
  rw [L, sum_eq_of_subset (fun m c => c * _root_.bernoulli m) (fun i => by simp)]
  · refine Finset.sum_congr rfl fun k _ => ?_
    rw [coeff_X_add_one_pow]
  · intro k hk
    rw [Finset.mem_range]
    by_contra h
    rw [not_lt] at h
    have hcoe : (((X : PolyX) + 1) ^ n).coeff k = 0 := by
      rw [coeff_X_add_one_pow, Nat.choose_eq_zero_of_lt (by omega), Nat.cast_zero]
    exact (mem_support_iff.1 hk) hcoe

/-- The binomial–Bernoulli sum of the shift in the form needed for the
difference: `∑_{k ≤ n} C(n,k)B_k - B_n = 0` for `n ≠ 1`, and `= 1` for `n = 1`. -/
lemma sum_range_choose_bernoulli_sub (n : ℕ) :
    (∑ k ∈ Finset.range (n + 1), (n.choose k : ℚ) * _root_.bernoulli k)
        - _root_.bernoulli n
      = if n = 1 then 1 else 0 := by
  rw [Finset.sum_range_succ, ← _root_.sum_bernoulli]
  simp

/-! ## The difference identity `L(Q(x+1) - Q(x)) = Q'(0)` -/

/-- **The Bernoulli difference identity.** For every polynomial `Q`,
`L(Q(x+1) - Q(x)) = Q'(0)`: `L` of a forward difference is the `x`-coefficient. -/
theorem L_comp_X_add_one_sub (Q : PolyX) :
    L (Q.comp ((X : PolyX) + 1) - Q) = (derivative Q).eval 0 := by
  induction Q using Polynomial.induction_on' with
  | add p q hp hq =>
      have hd : (p + q).comp ((X : PolyX) + 1) - (p + q)
          = (p.comp ((X : PolyX) + 1) - p) + (q.comp ((X : PolyX) + 1) - q) := by
        rw [add_comp]
        ring
      rw [hd, L_add, hp, hq, derivative_add, eval_add]
  | monomial n a =>
      have hcomp : (monomial n a).comp ((X : PolyX) + 1)
          = C a * ((X : PolyX) + 1) ^ n := by
        rw [← C_mul_X_pow_eq_monomial, mul_comp, C_comp, pow_comp, X_comp]
      have hderiv : (derivative (C a * (X : PolyX) ^ n)).eval 0 = if n = 1 then a else 0 := by
        rcases n with _ | m
        · simp
        · rcases m with _ | m
          · rw [derivative_C_mul_X_pow_succ]
            simp
          · rw [derivative_C_mul_X_pow_succ]
            simp
      have hdiff : C a * ((X : PolyX) + 1) ^ n - C a * (X : PolyX) ^ n
          = C a * (((X : PolyX) + 1) ^ n - (X : PolyX) ^ n) := by ring
      rw [hcomp, ← C_mul_X_pow_eq_monomial, hdiff, L_C_mul, L_sub, L_X_add_one_pow,
        L_X_pow, sum_range_choose_bernoulli_sub, hderiv]
      rcases n with _ | m
      · simp
      · rcases m with _ | m
        · simp
        · simp

/-! ## Derivatives of the shift, and the fourth-derivative identity -/

lemma derivative_comp_X_add_one (Q : PolyX) :
    derivative (Q.comp ((X : PolyX) + 1)) = (derivative Q).comp ((X : PolyX) + 1) := by
  rw [derivative_comp]
  simp

lemma iterate_derivative_comp_X_add_one (k : ℕ) (Q : PolyX) :
    (derivative^[k]) (Q.comp ((X : PolyX) + 1))
      = ((derivative^[k]) Q).comp ((X : PolyX) + 1) := by
  induction k generalizing Q with
  | zero => simp
  | succ k ih =>
      rw [Function.iterate_succ_apply', ih, Function.iterate_succ_apply',
        derivative_comp_X_add_one]

lemma iterate_derivative_sub (k : ℕ) (A B : PolyX) :
    (derivative^[k]) (A - B) = (derivative^[k]) A - (derivative^[k]) B := by
  induction k with
  | zero => simp
  | succ k ih =>
      rw [Function.iterate_succ_apply', Function.iterate_succ_apply',
        Function.iterate_succ_apply', ih, derivative_sub]

lemma iterate_derivative_three (P : PolyX) :
    (derivative^[3]) P = derivative (derivative (derivative P)) := by
  rw [show (3 : ℕ) = 2 + 1 from rfl, Function.iterate_succ_apply',
    show (2 : ℕ) = 1 + 1 from rfl, Function.iterate_succ_apply',
    show (1 : ℕ) = 0 + 1 from rfl, Function.iterate_succ_apply']
  simp

lemma τ_eq_L_iterate_derivative (P : PolyX) :
    τ P = L ((derivative^[3]) P) / 24 := by
  rw [iterate_derivative_three]
  rfl

/-- **`eq:difference`, polynomial case.** `τ(P(x+1) - P(x)) = P⁗(0)/24`. -/
theorem τ_comp_X_add_one_sub (P : PolyX) :
    τ (P.comp ((X : PolyX) + 1) - P)
      = ((derivative^[4]) P).eval 0 / 24 := by
  have h3 : (derivative^[3]) (P.comp ((X : PolyX) + 1) - P)
      = ((derivative^[3]) P).comp ((X : PolyX) + 1) - (derivative^[3]) P := by
    rw [iterate_derivative_sub, iterate_derivative_comp_X_add_one]
  rw [τ_eq_L_iterate_derivative, h3, L_comp_X_add_one_sub]
  rfl

/-- The exceptional case of `sum_bernoulli`, visible in the difference
identity: `L(x+1 - x) = L(1) = B_0 = 1 = (x)'(0)`, whereas for every `n ≥ 2`
the binomial–Bernoulli sum vanishes. -/
theorem L_comp_X_add_one_sub_X : L (((X : PolyX) + 1) - X) = 1 := by
  have h := L_comp_X_add_one_sub (X : PolyX)
  simpa using h

end

end ZetaFive.Correspondences.M1
