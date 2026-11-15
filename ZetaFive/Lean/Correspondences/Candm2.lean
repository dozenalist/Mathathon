/-
Copyright (c) 2026 Mathathon contributors. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
-/
import Mathlib
import ZetaFive.Lean.Correspondences.Basic
import ZetaFive.Lean.Correspondences.Transport

/-!
# Nondegeneracy of the frozen functionals `L`, `τ`, `μ`

Member m2, swarm smwh2nngu.  Direction: *properties* of the frozen functionals
(nonvanishing / vanishing laws) rather than further value tables.

Nothing here is a new definition: `L`, `τ`, `μpoly`, `μcoeff`, `pull` and `H5`
are the frozen objects of `Basic.lean`, and the only numerical inputs are
Mathlib's Bernoulli facts (`bernoulli_zero`, `bernoulli_eq_zero_of_odd`)
together with `τ_C_mul_X_pow`, `μpoly_one`, `τ_X`, `τ_X_pow_three` from
`Transport.lean`.

## What is proved

* the `μ`-weight factors as `(sign/normalisation) * B_{2e+2}`, and the
  normalisation factor never vanishes, so `μcoeff e ≠ 0 ↔ bernoulli (2e+2) ≠ 0`;
* `L` vanishes on every odd monomial of degree `≥ 3`, while `τ` vanishes on all
  monomials of degree `≤ 2` and on all even monomials of degree `≥ 6`;
* `L`, `τ` and `μpoly` are *nonzero* functionals (`L 1 = 1`, `τ x³ = 1/4`,
  `μpoly 1 = 5/12`), and `μpoly` does not vanish on any monomial whose
  Bernoulli weight is nonzero.

The one arithmetic input deliberately *not* claimed here is `B_{2n} ≠ 0`
(von Staudt–Clausen); it enters only as a hypothesis, in
`mu_coeff_ne_zero_iff`.
-/

namespace ZetaFive.Correspondences.M2

noncomputable section

open scoped BigOperators
open Polynomial

open ZetaFive.Correspondences

/-! ## The `μ`-weight -/

/-- The `μ`-weight split into its sign/normalisation factor and `B_{2e+2}`. -/
lemma mu_coeff_eq_factor (e : ℕ) :
    μcoeff e = ((-1 : ℚ) ^ e * (((2 * e + 3 : ℕ) : ℚ) * ((2 * e + 4 : ℕ) : ℚ)
      * ((2 * e + 5 : ℕ) : ℚ)) / 24) * _root_.bernoulli (2 * e + 2) := by
  rw [μcoeff]
  ring

/-- The sign/normalisation factor of `μcoeff` is never zero. -/
lemma mu_factor_ne_zero (e : ℕ) :
    ((-1 : ℚ) ^ e * (((2 * e + 3 : ℕ) : ℚ) * ((2 * e + 4 : ℕ) : ℚ)
      * ((2 * e + 5 : ℕ) : ℚ)) / 24) ≠ 0 := by
  have h3 : ((2 * e + 3 : ℕ) : ℚ) ≠ 0 := by
    have : (2 * e + 3 : ℕ) ≠ 0 := by omega
    exact_mod_cast this
  have h4 : ((2 * e + 4 : ℕ) : ℚ) ≠ 0 := by
    have : (2 * e + 4 : ℕ) ≠ 0 := by omega
    exact_mod_cast this
  have h5 : ((2 * e + 5 : ℕ) : ℚ) ≠ 0 := by
    have : (2 * e + 5 : ℕ) ≠ 0 := by omega
    exact_mod_cast this
  have hs : (-1 : ℚ) ^ e ≠ 0 := pow_ne_zero e (by norm_num)
  have h24 : (24 : ℚ) ≠ 0 := by norm_num
  exact div_ne_zero (mul_ne_zero hs (mul_ne_zero (mul_ne_zero h3 h4) h5)) h24

/-- **Nonvanishing criterion for the `μ`-weights.** -/
theorem mu_coeff_ne_zero_iff (e : ℕ) :
    μcoeff e ≠ 0 ↔ _root_.bernoulli (2 * e + 2) ≠ 0 := by
  rw [mu_coeff_eq_factor, mul_ne_zero_iff]
  exact ⟨fun h => h.2, fun h => ⟨mu_factor_ne_zero e, h⟩⟩

/-- `μcoeff e` is nonzero as soon as the Bernoulli number it involves is. -/
theorem mu_coeff_ne_zero (e : ℕ) (h : _root_.bernoulli (2 * e + 2) ≠ 0) :
    μcoeff e ≠ 0 :=
  (mu_coeff_ne_zero_iff e).mpr h

/-- **`μ` is nondegenerate on a monomial with nonzero Bernoulli weight.** -/
theorem mu_poly_monomial_ne_zero {e : ℕ} {a : ℚ} (ha : a ≠ 0)
    (h : _root_.bernoulli (2 * e + 2) ≠ 0) : μpoly (monomial e a) ≠ 0 := by
  rw [μpoly_monomial]
  exact mul_ne_zero ha (mu_coeff_ne_zero e h)

/-- `μ(1) = μcoeff 0 = 5/12 ≠ 0`: the weight at `e = 0` really is nonzero
(this is `B_2 = 1/6` transported through the normalisation). -/
theorem mu_coeff_zero : μcoeff 0 = 5 / 12 := by
  have h : μpoly (1 : PolyT) = μcoeff 0 := by
    simpa using μpoly_monomial 0 1
  rw [← h, μpoly_one]

/-! ## Vanishing laws for `L` and `τ` -/

/-- `L(1) = B_0 = 1`. -/
theorem L_one : L (1 : PolyX) = 1 := by
  have h : L (1 : PolyX) = L (monomial 0 1) := by simp
  rw [h, L_monomial, _root_.bernoulli_zero, mul_one]

/-- **`L` kills every odd monomial of degree at least three.** -/
theorem L_X_pow_eq_zero_of_odd {n : ℕ} (hn : Odd n) (h1 : n ≠ 1) :
    L ((X : PolyX) ^ n) = 0 := by
  have hlt : 1 < n := by
    rcases hn with ⟨k, rfl⟩
    omega
  have h := L_C_mul_X_pow (a := 1) n
  rw [C_1, one_mul, one_mul] at h
  rw [h, bernoulli_eq_zero_of_odd hn hlt]

/-- `τ` kills the constant polynomial. -/
@[simp] theorem tau_one : τ (1 : PolyX) = 0 := by simp [τ]

/-- `τ` kills `x²`. -/
@[simp] theorem tau_X_pow_two : τ ((X : PolyX) ^ 2) = 0 := by simp [τ]

/-- `τ` kills `x` (restatement of `τ_X` of `Transport.lean`). -/
@[simp] theorem tau_X' : τ (X : PolyX) = 0 := τ_X

/-- **`τ` kills every even monomial of degree at least six**, since
`B_{2m+3} = 0` for `m ≥ 0`. -/
theorem tau_X_pow_eq_zero_of_even (m : ℕ) : τ ((X : PolyX) ^ (2 * m + 6)) = 0 := by
  have hexp : 2 * m + 6 = (2 * m + 3) + 3 := by omega
  have h := τ_C_mul_X_pow (c := 1) (k := 2 * m + 3)
  rw [C_1, one_mul] at h
  have hodd : Odd (2 * m + 3) := ⟨m + 1, by omega⟩
  rw [hexp, h, bernoulli_eq_zero_of_odd hodd (by omega)]
  ring

/-! ## Nonvanishing of the functionals themselves -/

/-- The Bernoulli summation functional is not the zero functional. -/
theorem L_ne_zero : L ≠ 0 := by
  intro h
  have h1 : L (1 : PolyX) = 0 := by
    simpa using congrFun h (1 : PolyX)
  rw [L_one] at h1
  exact one_ne_zero h1

/-- The differentiated functional `τ` is not the zero functional. -/
theorem tau_ne_zero : τ ≠ 0 := by
  intro h
  have h1 : τ ((X : PolyX) ^ 3) = 0 := by
    simpa using congrFun h ((X : PolyX) ^ 3)
  rw [τ_X_pow_three] at h1
  norm_num at h1

/-- The moment functional `μ` is not the zero functional. -/
theorem mu_poly_ne_zero : μpoly ≠ 0 := by
  intro h
  have h1 : μpoly (1 : PolyT) = 0 := by
    simpa using congrFun h (1 : PolyT)
  rw [μpoly_one] at h1
  norm_num at h1

/-! ## Axiom audit -/

#print axioms L_X_pow_eq_zero_of_odd
#print axioms tau_X_pow_eq_zero_of_even
#print axioms mu_coeff_ne_zero_iff
#print axioms mu_poly_monomial_ne_zero
#print axioms mu_poly_ne_zero

end

end ZetaFive.Correspondences.M2
