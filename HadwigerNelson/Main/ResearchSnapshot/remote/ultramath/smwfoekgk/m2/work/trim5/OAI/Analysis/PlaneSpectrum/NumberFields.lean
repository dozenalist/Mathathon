import Mathlib

namespace OAI

noncomputable section
open Polynomial
namespace EuclideanFiveColor.AlgebraicCayley
variable {L : Type*} [Field L] [Algebra ℚ L]

lemma minpoly_reverse_eval_ne_zero (b : L) (hb : IsAlgebraic ℚ b) (t : ℚ)
    (ht : 1-b*algebraMap ℚ L t ≠ 0) : (minpoly ℚ b).reverse.eval t ≠ 0 := by
  intro hz
  by_cases ht0 : t = 0
  · subst t
    rw [← coeff_zero_eq_eval_zero, coeff_zero_reverse, (minpoly.monic hb.isIntegral).leadingCoeff] at hz
    exact one_ne_zero hz
  let : Invertible (t⁻¹) := invertibleOfNonzero (inv_ne_zero ht0)
  have hp : (minpoly ℚ b).IsRoot t⁻¹ := by
    have he := (eval₂_reverse_eq_zero_iff (RingHom.id ℚ) t⁻¹ (minpoly ℚ b))
    simp only [invOf_eq_inv, inv_inv, eval₂_id] at he
    exact he.mp hz
  have he := minpoly.root hb.isIntegral hp
  apply ht
  rw [← he, ← map_mul, inv_mul_cancel₀ ht0, map_one, sub_self]

/-- A scalar-rational common denominator for an algebraic linear reciprocal. -/
lemma reciprocal_denominator (b : L) (hb : IsAlgebraic ℚ b) :
    ∃ (P : ℚ[X]) (R : L[X]), P.coeff 0 = 1 ∧
      (1-C b*X)*R = P.map (algebraMap ℚ L) ∧
      ∀ t : ℚ, 1-b*algebraMap ℚ L t ≠ 0 → P.eval t ≠ 0 := by
  by_cases hb0 : b = 0
  · subst b
    exact ⟨1,1,by simp,by simp,by simp⟩
  let p := minpoly ℚ b
  have hm : p.Monic := minpoly.monic hb.isIntegral
  let : Invertible b := invertibleOfNonzero hb0
  have hz : (p.reverse.map (algebraMap ℚ L)).IsRoot b⁻¹ := by
    rw [IsRoot, eval_map]
    have h := (eval₂_reverse_eq_zero_iff (algebraMap ℚ L) b p).mpr (minpoly.aeval ℚ b)
    simpa only [invOf_eq_inv] using h
  obtain ⟨R,hR⟩ := (dvd_iff_isRoot.mpr hz)
  refine ⟨p.reverse,C (-b⁻¹)*R,?_,?_,minpoly_reverse_eval_ne_zero b hb⟩
  · rw [coeff_zero_reverse, hm.leadingCoeff]
  · calc
      _ = (X-C b⁻¹)*R := by
        have he : (1-C b*X)*C (-b⁻¹) = X-C b⁻¹ := by
          have hc : C b*C b⁻¹ = (1 : L[X]) := by rw [← map_mul, mul_inv_cancel₀ hb0, map_one]
          rw [map_neg]
          calc
            _ = (C b*C b⁻¹)*X-C b⁻¹ := by ring
            _ = _ := by rw [hc, one_mul]
        rw [← mul_assoc, he]
      _ = _ := hR.symm

/-- Coefficientwise transport by a rational linear functional. -/
def polyLinear (ℓ : L →ₗ[ℚ] ℚ) (p : L[X]) : ℚ[X] :=
  Polynomial.ofFinsupp (AddMonoidAlgebra.ofCoeff (p.toFinsupp.coeff.mapRange ℓ (map_zero ℓ)))
@[simp] lemma coeff_polyLinear (ℓ : L →ₗ[ℚ] ℚ) (p : L[X]) (n : ℕ) :
    (polyLinear ℓ p).coeff n = ℓ (p.coeff n) := rfl
lemma polyLinear_add (ℓ : L →ₗ[ℚ] ℚ) (p q : L[X]) :
    polyLinear ℓ (p+q) = polyLinear ℓ p + polyLinear ℓ q := by
  ext n
  simp only [coeff_polyLinear, coeff_add, map_add]
lemma polyLinear_monomial (ℓ : L →ₗ[ℚ] ℚ) (n : ℕ) (a : L) :
    polyLinear ℓ (monomial n a) = monomial n (ℓ a) := by
  ext k
  simp only [coeff_polyLinear, coeff_monomial]
  split_ifs <;> simp
lemma eval_polyLinear (ℓ : L →ₗ[ℚ] ℚ) (p : L[X]) (t : ℚ) :
    (polyLinear ℓ p).eval t = ℓ (p.eval (algebraMap ℚ L t)) := by
  induction p using Polynomial.induction_on' with
  | add p q hp hq => simp only [polyLinear_add, eval_add, hp, hq, map_add]
  | monomial n a =>
    rw [polyLinear_monomial, eval_monomial, eval_monomial]
    have he : a*(algebraMap ℚ L t)^n = (t^n) • a := by
      rw [Algebra.smul_def, map_pow, mul_comm]
    rw [he, map_smul]
    exact mul_comm _ _

lemma polyLinear_eq_zero_iff (ℓ : L →ₗ[ℚ] ℚ) (p : L[X]) :
    polyLinear ℓ p = 0 ↔ ∀ t : ℚ, ℓ (p.eval (algebraMap ℚ L t)) = 0 := by
  simp_rw [← eval_polyLinear]
  exact ⟨fun he _ => by rw [he, eval_zero], fun h => Polynomial.funext fun t => by simpa using h t⟩

/-- The first three formal coefficients of the Cayley curve force annihilation
of 1, b and b². No analytic continuity is used. -/
lemma cayley_annihilation (b : L) (hb : IsAlgebraic ℚ b) (ℓ : L →ₗ[ℚ] ℚ)
    (hd : ∀ t : ℚ, 1-b*(algebraMap ℚ L t) ≠ 0)
    (h : ∀ t : ℚ, ℓ ((1+b*(algebraMap ℚ L t))/(1-b*(algebraMap ℚ L t))) = 0) :
    ℓ 1 = 0 ∧ ℓ b = 0 ∧ ℓ (b^2) = 0 := by
  obtain ⟨P,R,hP,hR,_hPreg⟩ := reciprocal_denominator b hb
  have hR' : R-(C b*R)*X = P.map (algebraMap ℚ L) := by
    convert hR using 1
    ring
  let T := R+(C b*R)*X
  have hT : polyLinear ℓ T = 0 := by
    apply (polyLinear_eq_zero_iff ℓ T).mpr
    intro t
    have hRt := congrArg (Polynomial.eval (algebraMap ℚ L t)) hR
    simp only [eval_mul, eval_sub, eval_one, eval_C, eval_X, eval_map, eval₂_at_apply] at hRt
    have he : T.eval (algebraMap ℚ L t) =
        (P.eval t) • ((1+b*(algebraMap ℚ L t))/(1-b*(algebraMap ℚ L t))) := by
      dsimp only [T]
      simp only [eval_add, eval_mul, eval_C, eval_X, Algebra.smul_def]
      rw [← hRt]
      rw [← mul_div_assoc, eq_div_iff (hd t)]
      ring
    rw [he, map_smul, h t, smul_zero]
  have h0 : R.coeff 0 = 1 := by
    have he := congrArg (fun p : L[X] => p.coeff 0) hR'
    simpa only [coeff_sub, coeff_mul_X_zero, sub_zero, coeff_map, hP, map_one] using he
  have h1 : R.coeff 1-b = algebraMap ℚ L (P.coeff 1) := by
    have he := congrArg (fun p : L[X] => p.coeff 1) hR'
    simpa only [coeff_sub, coeff_mul_X, coeff_C_mul, h0, mul_one, coeff_map] using he
  have h2 : R.coeff 2-b*R.coeff 1 = algebraMap ℚ L (P.coeff 2) := by
    have he := congrArg (fun p : L[X] => p.coeff 2) hR'
    simpa only [coeff_sub, coeff_mul_X, coeff_C_mul, coeff_map] using he
  have ht0 : ℓ 1 = 0 := by
    have he := congrArg (fun p : ℚ[X] => p.coeff 0) hT
    simpa only [coeff_polyLinear, T, coeff_add, coeff_mul_X_zero, add_zero, h0, coeff_zero] using he
  have ht1 : ℓ (R.coeff 1) + ℓ b = 0 := by
    have he := congrArg (fun p : ℚ[X] => p.coeff 1) hT
    simpa only [coeff_polyLinear, T, coeff_add, coeff_mul_X, coeff_C_mul, h0, mul_one,
      map_add, coeff_zero] using he
  have ht2 : ℓ (R.coeff 2) + ℓ (b*R.coeff 1) = 0 := by
    have he := congrArg (fun p : ℚ[X] => p.coeff 2) hT
    simpa only [coeff_polyLinear, T, coeff_add, coeff_mul_X, coeff_C_mul,
      map_add, coeff_zero] using he
  have hlQ (c : ℚ) : ℓ (algebraMap ℚ L c) = 0 := by
    have he : algebraMap ℚ L c = c • (1:L) := by rw [Algebra.smul_def, mul_one]
    rw [he, map_smul, ht0, smul_zero]
  have hh1 := congrArg ℓ h1
  rw [map_sub, hlQ] at hh1
  have hb0 : ℓ b = 0 := by linarith
  have hh2 := congrArg ℓ h2
  rw [map_sub, hlQ] at hh2
  have hbR : ℓ (b*R.coeff 1) = 0 := by linarith
  have hR1 : R.coeff 1 = algebraMap ℚ L (P.coeff 1)+b := sub_eq_iff_eq_add.mp h1
  rw [hR1, mul_add, map_add] at hbR
  have he : b*algebraMap ℚ L (P.coeff 1) = (P.coeff 1) • b := by
    rw [Algebra.smul_def, mul_comm]
  rw [he, map_smul, hb0, smul_zero, zero_add, ← sq] at hbR
  exact ⟨ht0,hb0,hbR⟩

end EuclideanFiveColor.AlgebraicCayley

end

noncomputable section
open Polynomial
namespace EuclideanFiveColor.AlgebraicCayley
variable {L : Type*} [Field L] [Algebra ℚ L]



end EuclideanFiveColor.AlgebraicCayley
end

noncomputable section
open Polynomial
open scoped ComplexConjugate
namespace EuclideanFiveColor.AlgebraicCayley
variable (N : IntermediateField ℚ ℂ)
@[simp] lemma coe_asN (a : realSlice N) : ((asN N a : N) : ℂ) = (a : ℝ) := rfl
variable (hi : Complex.I ∈ N)
@[simp] lemma coe_iN : ((iN N hi : N) : ℂ) = Complex.I := rfl


variable [FiniteDimensional ℚ N]

omit [FiniteDimensional ℚ N] in
@[simp] lemma realLine_zero (a b : realSlice N) : realLine N a b 0 = a := by simp [realLine]
omit [FiniteDimensional ℚ N] in
@[simp] lemma realLine_one (a b : realSlice N) : realLine N a b 1 = b := by simp [realLine]

end EuclideanFiveColor.AlgebraicCayley
end

noncomputable section
open Module
namespace EuclideanFiveColor.GeneralPosition
variable {V : Type*} [AddCommGroup V] [Module ℚ V] [FiniteDimensional ℚ V]


omit [FiniteDimensional ℚ V] in


end EuclideanFiveColor.GeneralPosition
end

noncomputable section
open Module
open scoped ComplexConjugate
namespace EuclideanFiveColor.AlgebraicCayley





end EuclideanFiveColor.AlgebraicCayley
end

end OAI
