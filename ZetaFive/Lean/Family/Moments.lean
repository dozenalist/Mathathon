module

public import ZetaFive.Lean.Common.MomentFunctional
public import Mathlib.NumberTheory.Bernoulli
public import Mathlib.NumberTheory.LSeries.RiemannZeta
public import Mathlib.Tactic.ComputeDegree
public import Mathlib.Tactic.FieldSimp
public import Mathlib.Tactic.NormNum
public import Mathlib.Tactic.Positivity
public import Mathlib.Tactic.Ring

@[expose] public section

/-! # The zeta-index-dependent data

These are Calegari's formulas for all integer weights `k ≥ 2`. The ascending
factorial form avoids a quotient of large factorials; `moment_factorial` proves
that it equals the formula in the exposition. The definition is total, but the
interpretation as a zeta moment requires `2 ≤ k`.
-/

open Polynomial Finset

namespace ZetaFive

/-- Rational polynomial moment of degree `e` for zeta weight `k`. -/
def moment (k e : ℕ) : ℚ :=
  (-1) ^ e * bernoulli (2 * e + 2) *
    ((2 * e + 3).ascFactorial (k - 2) : ℚ) / ((k - 1).factorial : ℚ)

theorem moment_factorial (k e : ℕ) (hk : 2 ≤ k) :
    moment k e = (-1 : ℚ) ^ e * bernoulli (2 * e + 2) *
      ((2 * e + k).factorial : ℚ) /
        (((k - 1).factorial : ℚ) * ((2 * e + 2).factorial : ℚ)) := by
  have hnat := Nat.factorial_mul_ascFactorial (2 * e + 2) (k - 2)
  have hindex : 2 * e + 2 + (k - 2) = 2 * e + k := by omega
  rw [hindex] at hnat
  have hfact : ((2 * e + k).factorial : ℚ) =
      ((2 * e + 2).factorial : ℚ) * ((2 * e + 3).ascFactorial (k - 2) : ℚ) := by
    exact_mod_cast hnat.symm
  have h0 : ((2 * e + 2).factorial : ℚ) ≠ 0 := by positivity
  have h1 : ((k - 1).factorial : ℚ) ≠ 0 := by positivity
  rw [moment, hfact]
  field_simp

/-- Extension of the rational moments to polynomials in the input variable. -/
noncomputable def polynomialMoment (k : ℕ) (P : ℚ[X]) : ℚ :=
  Common.momentFunctional (moment k) P

theorem polynomialMoment_add (k : ℕ) (P Q : ℚ[X]) :
    polynomialMoment k (P + Q) = polynomialMoment k P + polynomialMoment k Q :=
  map_add (Common.momentFunctional (moment k)) P Q

theorem polynomialMoment_smul (k : ℕ) (a : ℚ) (P : ℚ[X]) :
    polynomialMoment k (a • P) = a * polynomialMoment k P := by
  exact map_smul (Common.momentFunctional (moment k)) a P

/-- The finite harmonic sum, with exponent `k` and upper endpoint `j`. -/
def harmonic (k j : ℕ) : ℚ := ∑ v ∈ Icc 1 j, 1 / (v : ℚ) ^ k

/-- Affine value assigned to the pole `1/(t+j²)`; `X` denotes the zeta value. -/
noncomputable def poleValue (k j : ℕ) : ℚ[X] :=
  C ((j : ℚ) ^ (k - 1)) * (X - C (harmonic k j)) -
    C (1 / ((k - 1 : ℕ) : ℚ)) + C (1 / (2 * (j : ℚ)))

theorem poleValue_affine (k j : ℕ) : poleValue k j =
    C ((j : ℚ) ^ (k - 1)) * X +
      C (-(j : ℚ) ^ (k - 1) * harmonic k j -
        1 / ((k - 1 : ℕ) : ℚ) + 1 / (2 * (j : ℚ))) := by
  simp only [poleValue, C_add, C_sub, C_mul, C_neg, C_pow]
  ring

theorem poleValue_natDegree_le (k j : ℕ) : (poleValue k j).natDegree ≤ 1 := by
  rw [poleValue_affine]
  compute_degree!

theorem poleValue_coeff_one (k j : ℕ) :
    (poleValue k j).coeff 1 = (j : ℚ) ^ (k - 1) := by
  rw [poleValue_affine]
  simp only [coeff_add, coeff_C_mul, coeff_X_one, coeff_C, mul_one,
    one_ne_zero, ite_false, add_zero]

/-- The target is the actual real Dirichlet series, not an abstract parameter. -/
noncomputable def zeta (k : ℕ) : ℝ := ∑' n : ℕ, 1 / (n : ℝ) ^ k

theorem riemannZeta_eq (k : ℕ) (hk : 2 ≤ k) :
    riemannZeta (k : ℂ) = (zeta k : ℂ) := by
  rw [zeta_nat_eq_tsum_of_gt_one (by omega : 1 < k), zeta, Complex.ofReal_tsum]
  push_cast
  rfl

end ZetaFive


