module

public import Mathlib.Algebra.Polynomial.AlgebraMap

@[expose] public section

/-! # Linear extension of an arbitrary rational moment sequence -/

open Polynomial

namespace ZetaFive.Common

/-- A rational moment sequence determines a linear functional on polynomials. -/
noncomputable def momentFunctional (m : ℕ → ℚ) : ℚ[X] →ₗ[ℚ] ℚ where
  toFun P := P.sum fun e a => a * m e
  map_add' P Q := Polynomial.sum_add_index P Q _
    (fun _ => zero_mul _) (fun _ _ _ => add_mul _ _ _)
  map_smul' a P := by
    rw [Polynomial.sum_smul_index _ _ _ (fun _ => zero_mul _)]
    simp only [RingHom.id_apply, smul_eq_mul]
    simpa only [smul_eq_mul, mul_assoc] using
      (Polynomial.smul_sum P a (fun e c => c * m e)).symm

@[simp] theorem momentFunctional_monomial (m : ℕ → ℚ) (e : ℕ) (a : ℚ) :
    momentFunctional m (monomial e a) = a * m e := by
  exact Polynomial.sum_monomial_index a (fun e c => c * m e) (zero_mul _)

@[simp] theorem momentFunctional_X_pow (m : ℕ → ℚ) (e : ℕ) :
    momentFunctional m (X ^ e) = m e := by
  simpa only [monomial_one_right_eq_X_pow, one_mul] using
    momentFunctional_monomial m e 1

end ZetaFive.Common

