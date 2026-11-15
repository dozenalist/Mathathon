module

public import ZetaFive.Lean.Common.PartialFractions
public import ZetaFive.Lean.Common.AffineDeterminant
public import ZetaFive.Lean.Family.Parameters
public import ZetaFive.Lean.Family.Moments

@[expose] public section

/-! # A single Hankel construction for every zeta index

The polynomial-division presentation makes the functional explicit. All residue
and denominator arguments are in `Common`, independent of `k`.
-/

open Polynomial Finset
open ZetaFive.Common

namespace ZetaFive

/-- The affine functional applied to `P(t)/D_K(t)`. -/
noncomputable def mu (k K : ℕ) (P : ℚ[X]) : ℚ[X] :=
  C (polynomialMoment k (P /ₘ D K)) +
    ∑ j ∈ Icc 1 K, C (res K P j) * poleValue k j

theorem mu_affine (k K : ℕ) (P : ℚ[X]) : mu k K P =
    C (∑ j ∈ Icc 1 K, res K P j * (j : ℚ) ^ (k - 1)) * X +
      C (polynomialMoment k (P /ₘ D K) +
        ∑ j ∈ Icc 1 K, res K P j *
          (-(j : ℚ) ^ (k - 1) * harmonic k j -
            1 / ((k - 1 : ℕ) : ℚ) + 1 / (2 * (j : ℚ)))) := by
  simp only [mu, poleValue_affine, mul_add, ← mul_assoc, ← C_mul,
    Finset.sum_add_distrib, ← Finset.sum_mul, ← map_sum, C_add]
  ring

theorem mu_natDegree_le (k K : ℕ) (P : ℚ[X]) : (mu k K P).natDegree ≤ 1 := by
  rw [mu_affine]
  compute_degree!

theorem mu_coeff_one (k K : ℕ) (P : ℚ[X]) :
    (mu k K P).coeff 1 = ∑ j ∈ Icc 1 K, res K P j * (j : ℚ) ^ (k - 1) := by
  rw [mu_affine]
  simp only [coeff_add, coeff_C_mul, coeff_X_one, coeff_C, mul_one,
    one_ne_zero, ite_false, add_zero]

/-- Matrix size, pole cutoff and numerator are independent of the zeta index. -/
noncomputable def hankel (k : ℕ) (p : Parameters) : Matrix (Fin p.h) (Fin p.h) ℚ[X] :=
  fun i j => mu k p.K (D p.N ^ p.numeratorPower * X ^ ((i : ℕ) + (j : ℕ)))

noncomputable def delta (k : ℕ) (p : Parameters) : ℚ[X] := (hankel k p).det

noncomputable def normalized (k : ℕ) (p : Parameters) : ℚ[X] := C (scale p) * delta k p

theorem delta_natDegree_le (k : ℕ) (p : Parameters) : (delta k p).natDegree ≤ p.h := by
  exact (coeff_det_of_natDegree_le_one (hankel k p) fun i j =>
    mu_natDegree_le k p.K _).2

theorem delta_top_coefficient (k : ℕ) (p : Parameters) :
    (delta k p).coeff p.h =
      (Matrix.of fun i j : Fin p.h => (hankel k p i j).coeff 1).det := by
  exact (coeff_det_of_natDegree_le_one (hankel k p) fun i j =>
    mu_natDegree_le k p.K _).1

theorem normalized_natDegree_le (k : ℕ) (p : Parameters) :
    (normalized k p).natDegree ≤ p.h := by
  exact (natDegree_C_mul_le _ _).trans (delta_natDegree_le k p)

theorem lai_degree_bound (k n : ℕ) :
    (normalized k (laiParameters n)).natDegree ≤ 37 * n :=
  normalized_natDegree_le k (laiParameters n)

theorem calegari_degree_bound (k n : ℕ) :
    (normalized k (calegariParameters n)).natDegree ≤ 11 * n :=
  normalized_natDegree_le k (calegariParameters n)

end ZetaFive


