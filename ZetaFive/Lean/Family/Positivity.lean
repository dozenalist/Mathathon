module

/-
Adapted from `Apery/Positivity.lean` in https://github.com/mo271/zeta5,
commit 7fe736760f4b96bfdb4334b68e3b3124ecbe10b0, under Apache 2.0.
See ZetaFive/Lean/LICENSES/mo271-Zeta5.txt.
-/
public import ZetaFive.Lean.Common.Gram
public import ZetaFive.Lean.Family.Construction
public import ZetaFive.Lean.Family.PolynomialMoments

@[expose] public section

/-!
# Moment representation and determinant positivity from the pole identity

The polynomial moments have already been proved for every `k ≥ 2`. This file
isolates the remaining analytic identity as the explicit proposition `PoleMoments`.
It is a hypothesis, not an axiom or an instance. From that identity we prove the
full rational-function moment representation and strict positivity of the actual
Hankel determinant. The Gram argument itself lives in `Common.Gram`.
-/

open Polynomial MeasureTheory Set Finset
open ZetaFive.Common

namespace ZetaFive

/-- The remaining pole-moment identity. A proof must be supplied separately;
this definition asserts no result about any particular exponent. -/
def PoleMoments (k : ℕ) : Prop :=
  ∀ j : ℕ, 1 ≤ j →
    (∫ y in Set.Ioi 0, weight k y / (y ^ 2 + (j : ℝ) ^ 2)) =
      (j : ℝ) ^ (k - 1) * (zeta k - (harmonic k j : ℝ)) -
        1 / ((k - 1 : ℕ) : ℝ) + 1 / (2 * (j : ℝ))

/-- Pole integrability follows from the zeroth polynomial moment, independently
of the pole identity. -/
theorem integrableOn_pole (k : ℕ) (hk : 2 ≤ k) (j : ℕ) (hj : 1 ≤ j) :
    IntegrableOn (fun y => weight k y / (y ^ 2 + (j : ℝ) ^ 2)) (Set.Ioi 0) := by
  have hw : IntegrableOn (weight k) (Set.Ioi 0) := by
    simpa using (mono_moment k 0 hk).1
  have hj' : (1 : ℝ) ≤ j := by exact_mod_cast hj
  refine hw.mono' ((measurable_weight k).aemeasurable.div
    (by fun_prop : Measurable fun y : ℝ => y ^ 2 + (j : ℝ) ^ 2).aemeasurable).aestronglyMeasurable ?_
  refine (ae_restrict_iff' measurableSet_Ioi).mpr
    (Filter.Eventually.of_forall fun y hy => ?_)
  have hpos := weight_pos k hy
  have hden : (1 : ℝ) ≤ y ^ 2 + (j : ℝ) ^ 2 := by nlinarith
  rw [Real.norm_of_nonneg (div_nonneg hpos.le (by positivity))]
  exact div_le_self hpos.le hden

/-- The integrand associated with the rational function `P(t)/D_K(t)`. -/
noncomputable def integrand (k K : ℕ) (P : ℚ[X]) (y : ℝ) : ℝ :=
  aeval (y ^ 2) P / aeval (y ^ 2) (D K) * weight k y

theorem integrand_eq_sum (k K : ℕ) (P : ℚ[X]) {y : ℝ} (hy : 0 < y) :
    integrand k K P y =
      (∑ e ∈ Finset.range ((P /ₘ D K).natDegree + 1),
          ((P /ₘ D K).coeff e : ℝ) * (y ^ (2 * e) * weight k y)) +
        ∑ j ∈ Finset.Icc 1 K,
          (res K P j : ℝ) * (weight k y / (y ^ 2 + (j : ℝ) ^ 2)) := by
  unfold integrand
  rw [partial_fractions K P (t := y ^ 2) (by positivity), aeval_eq_sum_range,
    add_mul, Finset.sum_mul, Finset.sum_mul]
  congr 1
  · refine Finset.sum_congr rfl fun e _ => ?_
    simp only [Rat.smul_def, ← pow_mul]
    ring
  · refine Finset.sum_congr rfl fun j _ => ?_
    ring

theorem aeval_mu (k K : ℕ) (P : ℚ[X]) :
    aeval (zeta k) (mu k K P) =
      (∑ e ∈ Finset.range ((P /ₘ D K).natDegree + 1),
          ((P /ₘ D K).coeff e : ℝ) * (moment k e : ℝ)) +
        ∑ j ∈ Finset.Icc 1 K, (res K P j : ℝ) *
          ((j : ℝ) ^ (k - 1) * (zeta k - (harmonic k j : ℝ)) -
            1 / ((k - 1 : ℕ) : ℝ) + 1 / (2 * (j : ℝ))) := by
  simp only [mu, map_add, aeval_C, map_sum, map_mul, poleValue, map_sub,
    aeval_X, eq_ratCast]
  congr 1
  · change (((P /ₘ D K).sum fun e c => c * moment k e : ℚ) : ℝ) = _
    rw [Polynomial.sum_over_range' _ (fun _ => by simp) _ (Nat.lt_succ_self _)]
    push_cast
    rfl
  · refine Finset.sum_congr rfl fun j _ => ?_
    push_cast
    ring

/-- Polynomial and pole moments imply the moment representation for every
rational function with the allowed square-node denominator. -/
theorem moment_rep (k : ℕ) (hk : 2 ≤ k) (hPole : PoleMoments k)
    (K : ℕ) (P : ℚ[X]) :
    IntegrableOn (integrand k K P) (Set.Ioi 0) ∧
      aeval (zeta k) (mu k K P) = ∫ y in Set.Ioi 0, integrand k K P y := by
  set Q := P /ₘ D K with hQ
  have hint1 : ∀ e ∈ Finset.range (Q.natDegree + 1),
      IntegrableOn (fun y => (Q.coeff e : ℝ) * (y ^ (2 * e) * weight k y)) (Set.Ioi 0) :=
    fun e _ => (mono_moment k e hk).1.const_mul _
  have hint2 : ∀ j ∈ Finset.Icc 1 K,
      IntegrableOn (fun y => (res K P j : ℝ) *
        (weight k y / (y ^ 2 + (j : ℝ) ^ 2))) (Set.Ioi 0) :=
    fun j hj => (integrableOn_pole k hk j (Finset.mem_Icc.mp hj).1).const_mul _
  have hsumint : IntegrableOn (fun y =>
      (∑ e ∈ Finset.range (Q.natDegree + 1), (Q.coeff e : ℝ) *
        (y ^ (2 * e) * weight k y)) +
      ∑ j ∈ Finset.Icc 1 K, (res K P j : ℝ) *
        (weight k y / (y ^ 2 + (j : ℝ) ^ 2))) (Set.Ioi 0) :=
    (integrable_finsetSum _ hint1).add (integrable_finsetSum _ hint2)
  have hEq : EqOn (fun y =>
      (∑ e ∈ Finset.range (Q.natDegree + 1), (Q.coeff e : ℝ) *
        (y ^ (2 * e) * weight k y)) +
      ∑ j ∈ Finset.Icc 1 K, (res K P j : ℝ) *
        (weight k y / (y ^ 2 + (j : ℝ) ^ 2))) (integrand k K P) (Set.Ioi 0) :=
    fun y hy => (integrand_eq_sum k K P hy).symm
  refine ⟨hsumint.congr_fun hEq measurableSet_Ioi, ?_⟩
  rw [← setIntegral_congr_fun measurableSet_Ioi hEq,
    integral_add (integrable_finsetSum _ hint1) (integrable_finsetSum _ hint2),
    integral_finsetSum _ hint1, integral_finsetSum _ hint2, aeval_mu]
  congr 1
  · refine Finset.sum_congr rfl fun e _ => ?_
    rw [integral_const_mul, (mono_moment k e hk).2]
  · refine Finset.sum_congr rfl fun j hj => ?_
    rw [integral_const_mul, hPole j (Finset.mem_Icc.mp hj).1]

/-- The density after multiplication by the rational modifier. -/
noncomputable def modifiedWeight (k : ℕ) (p : Parameters) (y : ℝ) : ℝ :=
  aeval (y ^ 2) (D p.N) ^ p.numeratorPower /
    aeval (y ^ 2) (D p.K) * weight k y

theorem modifiedWeight_pos (k : ℕ) (p : Parameters) {y : ℝ} (hy : 0 < y) :
    0 < modifiedWeight k p y := by
  unfold modifiedWeight
  exact mul_pos (div_pos (pow_pos (aeval_D_pos p.N (by positivity)) _)
    (aeval_D_pos p.K (by positivity))) (weight_pos k hy)

theorem integrand_monomial (k : ℕ) (p : Parameters) (e : ℕ) (y : ℝ) :
    integrand k p.K (D p.N ^ p.numeratorPower * X ^ e) y =
      (y ^ 2) ^ e * modifiedWeight k p y := by
  simp only [integrand, modifiedWeight, map_mul, map_pow, aeval_X]
  ring

/-- Every real polynomial is integrable against the modified density. This uses
finite expansion into monomials; no bound specific to `k` is required. -/
theorem modifiedWeight_integrable_polynomial (k : ℕ) (hk : 2 ≤ k)
    (hPole : PoleMoments k) (p : Parameters) (q : ℝ[X]) :
    IntegrableOn (fun y => q.eval (y ^ 2) * modifiedWeight k p y) (Set.Ioi 0) := by
  have hmono : ∀ e : ℕ, IntegrableOn
      (fun y => (y ^ 2) ^ e * modifiedWeight k p y) (Set.Ioi 0) := by
    intro e
    exact (moment_rep k hk hPole p.K (D p.N ^ p.numeratorPower * X ^ e)).1.congr_fun
      (fun y _ => integrand_monomial k p e y) measurableSet_Ioi
  have hpt : ∀ y : ℝ, q.eval (y ^ 2) * modifiedWeight k p y =
      ∑ e ∈ Finset.range (q.natDegree + 1),
        q.coeff e * ((y ^ 2) ^ e * modifiedWeight k p y) := by
    intro y
    rw [Polynomial.eval_eq_sum_range, Finset.sum_mul]
    exact Finset.sum_congr rfl fun _ _ => by ring
  have hsum : IntegrableOn (fun y =>
      ∑ e ∈ Finset.range (q.natDegree + 1),
        q.coeff e * ((y ^ 2) ^ e * modifiedWeight k p y)) (Set.Ioi 0) :=
    integrable_finsetSum _ fun e _ => (hmono e).const_mul _
  exact hsum.congr_fun (fun y _ => (hpt y).symm) measurableSet_Ioi

/-- The actual determinant is strictly positive at `ζ(k)`, provided the explicitly
stated pole identity has been proved. Positivity is not an additional hypothesis. -/
theorem delta_pos (k : ℕ) (hk : 2 ≤ k) (hPole : PoleMoments k) (p : Parameters) :
    0 < aeval (zeta k) (delta k p) := by
  have hdet : aeval (zeta k) (delta k p) =
      ((hankel k p).map (aeval (zeta k))).det := by
    have hmap := RingHom.map_det (aeval (zeta k) : ℚ[X] →ₐ[ℚ] ℝ).toRingHom (hankel k p)
    simpa [delta, RingHom.mapMatrix_apply] using hmap
  rw [hdet]
  let hint := modifiedWeight_integrable_polynomial k hk hPole p
  have hmatrix : (hankel k p).map (aeval (zeta k)) =
      momentHankel (polynomialIntegral (modifiedWeight k p) hint) p.h := by
    ext i j
    change aeval (zeta k)
      (mu k p.K (D p.N ^ p.numeratorPower * X ^ ((i : ℕ) + (j : ℕ)))) =
      ∫ y in Set.Ioi 0,
        (X ^ ((i : ℕ) + (j : ℕ)) : ℝ[X]).eval (y ^ 2) * modifiedWeight k p y
    rw [(moment_rep k hk hPole p.K _).2]
    refine setIntegral_congr_fun measurableSet_Ioi fun y _ => ?_
    simp only [eval_pow, eval_X, integrand_monomial]
  rw [hmatrix]
  exact integralHankel_det_pos _ hint (fun y hy => modifiedWeight_pos k p hy) p.h

/-- The common rational normalization preserves positivity. -/
theorem normalized_pos (k : ℕ) (hk : 2 ≤ k) (hPole : PoleMoments k) (p : Parameters) :
    0 < aeval (zeta k) (normalized k p) := by
  unfold normalized
  rw [map_mul, aeval_C]
  apply mul_pos
  · change (0 : ℝ) < (scale p : ℝ)
    exact_mod_cast scale_pos p
  · exact delta_pos k hk hPole p

end ZetaFive
