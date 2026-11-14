/-
Copyright (c) 2026 Mathathon contributors. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
-/
import Mathlib
import ZetaFive.Lean.Correspondences.Basic

/-!
# Target 1: weighted transport `μ(P) = τ(x^5 P(-x^2))`

Source: `zeta5_unified_framework.tex` §2.1 (equation `eq:pullback`, the monomial
identity for `τ`, and the displayed partial fraction for `x^5/(j²-x²)`).

The two objects are defined independently in `Basic.lean`:

* `μ` from its monomial values `μ(t^e) = (-1)^e B_{2e+2}(2e+3)(2e+4)(2e+5)/24`;
* `τ(P) = L(P''')/24` with `L(x^k) = B_k`.

`μpoly_eq_τ_pull` proves that they agree on `ℚ[t]`. The pole values of the
singular extension come from the *independently* defined `τ_X` at simple
integer poles, and are compared with the independently defined `μ_X` pole
formula in `τX_single_pole_transport` (this is the finite harmonic increment
`H_j - H_{j-1} = j^{-5}` doing its work).
-/

namespace ZetaFive.Correspondences

noncomputable section

open scoped BigOperators
open Polynomial

/-! ## The general monomial calculation -/

/-- `τ(C c * x^(k+3)) = c (k+3)(k+2)(k+1) B_k / 24`. -/
lemma τ_C_mul_X_pow (c : ℚ) (k : ℕ) :
    τ (C c * (X : PolyX) ^ (k + 3))
      = c * ((k + 3 : ℕ) : ℚ) * ((k + 2 : ℕ) : ℚ) * ((k + 1 : ℕ) : ℚ)
          * _root_.bernoulli k / 24 := by
  have h1 : derivative (C c * (X : PolyX) ^ (k + 3))
      = C (c * ((k + 3 : ℕ) : ℚ)) * X ^ (k + 2) :=
    derivative_C_mul_X_pow_succ c (k + 2)
  have h2 : derivative (C (c * ((k + 3 : ℕ) : ℚ)) * (X : PolyX) ^ (k + 2))
      = C (c * ((k + 3 : ℕ) : ℚ) * ((k + 2 : ℕ) : ℚ)) * X ^ (k + 1) :=
    derivative_C_mul_X_pow_succ _ (k + 1)
  have h3 : derivative (C (c * ((k + 3 : ℕ) : ℚ) * ((k + 2 : ℕ) : ℚ))
        * (X : PolyX) ^ (k + 1))
      = C (c * ((k + 3 : ℕ) : ℚ) * ((k + 2 : ℕ) : ℚ) * ((k + 1 : ℕ) : ℚ)) * X ^ k :=
    derivative_C_mul_X_pow_succ _ k
  simp only [τ]
  rw [h1, h2, h3, L_C_mul_X_pow]

/-- `τ` vanishes on `x`. -/
@[simp] lemma τ_X : τ (X : PolyX) = 0 := by
  simp [τ]

/-- The transport theorem on `ℚ[t]`: `μ(P) = τ(x^5 P(-x^2))`. -/
theorem μpoly_eq_τ_pull (P : PolyT) : μpoly P = τ (X ^ 5 * pull P) := by
  induction P using Polynomial.induction_on' with
  | add p q hp hq => rw [μpoly_add, hp, hq, map_add, mul_add, τ_add]
  | monomial n a =>
      rw [μpoly_monomial, pull_monomial]
      have hmul : (X : PolyX) ^ 5 * (C (a * (-1 : ℚ) ^ n) * X ^ (2 * n))
          = C (a * (-1 : ℚ) ^ n) * X ^ (2 * n + 5) := by
        rw [← mul_assoc, mul_comm ((X : PolyX) ^ 5) (C (a * (-1 : ℚ) ^ n)), mul_assoc,
          ← pow_add]
        rw [Nat.add_comm 5 (2 * n)]
      rw [hmul, τ_C_mul_X_pow, μcoeff]
      push_cast
      ring

/-! ## Sanity checks with the stated Bernoulli convention -/

/-- `τ(x^3) = 1/4`. Requires `B_1 = -1/2` only through `B_0 = 1`. -/
theorem τ_X_pow_three : τ ((X : PolyX) ^ 3) = 1 / 4 := by
  have h := τ_C_mul_X_pow (c := 1) 0
  norm_num at h
  simpa using h

/-- `τ(x^4) = -1/2`. This is the explicit check of the `B_1 = -1/2` convention. -/
theorem τ_X_pow_four : τ ((X : PolyX) ^ 4) = -1 / 2 := by
  have h : τ ((X : PolyX) ^ 4) = -2⁻¹ := by
    have h' := τ_C_mul_X_pow (c := 1) 1
    norm_num at h'
    simpa using h'
  rw [h]; norm_num

/-- `μ(1) = 5/12`. -/
theorem μpoly_one : μpoly (1 : PolyT) = 5 / 12 := by
  have h : μpoly (1 : PolyT) = μcoeff 0 := by
    simpa using μpoly_monomial 0 1
  rw [h]; norm_num [μcoeff]

/-! ## The partial fraction for the pole, as a rational-function identity -/

/-- `x^5/(j²-x²) = -x³ - j²x - (j⁴/2)(1/(x-j) + 1/(x+j))` in any field in which
the displayed denominators are nonzero. This is a rational-function identity:
stated over an arbitrary field, it holds in `ℚ(x)` after substituting `x ↦ X`. -/
theorem rat_pole_identity {F : Type*} [Field F] [CharZero F] (x j : F)
    (h1 : x - j ≠ 0) (h2 : x + j ≠ 0) (h3 : j ^ 2 - x ^ 2 ≠ 0) :
    x ^ 5 / (j ^ 2 - x ^ 2)
      = -(x ^ 3) - j ^ 2 * x - j ^ 4 / 2 * ((x - j)⁻¹ + (x + j)⁻¹) := by
  field_simp
  ring

/-! ## The singular extension `τ_X` at simple integer poles -/

/-- `d(r) = r` for `r ≥ 0` and `d(r) = -r-1` for `r < 0`: the index of the
harmonic sum attached to the simple pole at `x = r`. -/
def d (r : ℤ) : ℕ := if 0 ≤ r then r.toNat else (-r - 1).toNat

@[simp] lemma d_natCast (j : ℕ) : d (j : ℤ) = j := by
  simp [d]

@[simp] lemma d_neg_natCast (j : ℕ) : d (-(j : ℤ)) = j - 1 := by
  rcases j with _ | j
  · simp [d]
  · simp only [d]
    have h : ¬ ((0 : ℤ) ≤ -((j + 1 : ℕ) : ℤ)) := by omega
    rw [if_neg h]
    have h2 : (-(-((j + 1 : ℕ) : ℤ)) - 1) = ((j : ℕ) : ℤ) := by omega
    rw [h2, Int.toNat_natCast]
    omega

/-- The domain of `τ_X`: polynomial part plus finitely many simple poles at
integers. `poles` is an association list `(r, c)` meaning `c/(x-r)`; repeated
indices are harmless because the pole functional is additive. -/
structure XRep where
  poly : PolyX
  poles : List (ℤ × ℚ)

/-- `τ_X` on its domain, defined from the *independent* pole data
`τ_X((x-r)^{-1}) = H_{d(r)}^{(5)} - X` and the Bernoulli functional on the
polynomial part. -/
def XRep.tauX (u : ℚ) (R : XRep) : ℚ :=
  τ R.poly + (R.poles.map (fun rc => rc.2 * (H5 (d rc.1) - u))).sum

/-- **Target 1, pole case.** The `τ_X`-value of the transported simple pole
`c/(t+j²)` equals the independently defined `μ_X` pole formula
`j⁴(X - H_j^{(5)}) - 1/4 + 1/(2j)`, multiplied by `c`.

The `-1/4` is the Bernoulli part `τ(-x³) = -1/4`; the harmonic increment
`H_j - H_{j-1} = j^{-5}` turns the two half-pole terms into `1/(2j)`. -/
theorem τX_single_pole_transport (u : ℚ) {j : ℕ} (hj : 1 ≤ j) (c : ℚ) :
    XRep.tauX u
        ⟨C (-c) * (X ^ 3 + C ((j : ℚ) ^ 2) * X),
          [((j : ℤ), -(c * (j : ℚ) ^ 4) / 2), (-((j : ℤ)), -(c * (j : ℚ) ^ 4) / 2)]⟩
      = c * ((j : ℚ) ^ 4 * (u - H5 j) - 1 / 4 + (2 * (j : ℚ))⁻¹) := by
  have hj0 : (j : ℚ) ≠ 0 := Nat.cast_ne_zero.mpr (by omega)
  have hH : H5 (j - 1) = H5 j - ((j : ℚ))⁻¹ ^ 5 := by
    have := H5_increment hj
    linarith
  have hτ : τ (C (-c) * ((X : PolyX) ^ 3 + C ((j : ℚ) ^ 2) * X)) = -c / 4 := by
    rw [τ_C_mul, τ_add, τ_C_mul, τ_X, mul_zero, add_zero, τ_X_pow_three]
    ring
  simp only [XRep.tauX, List.map_cons, List.map_nil, List.sum_cons, List.sum_nil,
    d_natCast, d_neg_natCast, hH, hτ]
  field_simp
  ring

end

end ZetaFive.Correspondences
