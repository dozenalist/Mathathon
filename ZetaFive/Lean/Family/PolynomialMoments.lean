module

/-
The Gamma-and-Euler argument is adapted from `Apery/Moments.lean` in
https://github.com/mo271/zeta5, commit 7fe736760f4b96bfdb4334b68e3b3124ecbe10b0
(Apache 2.0; see ZetaFive/Lean/LICENSES/mo271-Zeta5.txt).
Here the argument is uniform in every natural `k ≥ 2`.
-/
public import ZetaFive.Lean.Common.GammaIntegral
public import ZetaFive.Lean.Family.Moments
public import ZetaFive.Lean.Family.Weight
public import Mathlib.Algebra.Polynomial.Eval.Degree
public import Mathlib.MeasureTheory.Integral.DominatedConvergence
public import Mathlib.NumberTheory.ZetaValues

@[expose] public section

/-!
# Polynomial moments for every zeta weight

Termwise Gamma integration reduces the answer to the even zeta value `ζ(2e+2)`.
Euler's formula then gives the rational Bernoulli moment. Absolute summability of
the integrals proves the integral identity, and its strict positivity gives
integrability. No estimate specialized to `k = 5` is used.
-/

open Polynomial MeasureTheory Set Filter Topology Finset

namespace ZetaFive

/-- A term in the series for the polynomial moment of degree `e`. -/
noncomputable def momentTerm (k e ℓ : ℕ) (y : ℝ) : ℝ :=
  (2 * (2 * Real.pi) ^ (k - 1) / ((k - 1).factorial : ℝ)) *
    ((ℓ : ℝ) + 1) ^ (k - 1) *
      (y ^ (2 * e + k) * Real.exp (-(2 * Real.pi * ((ℓ : ℝ) + 1) * y)))

theorem momentTerm_eq (k e ℓ : ℕ) (y : ℝ) : momentTerm k e ℓ y =
    y ^ (2 * e) * (2 * (2 * Real.pi) ^ (k - 1) * y ^ k /
      ((k - 1).factorial : ℝ)) * weightSummand k ℓ y := by
  simp only [momentTerm, weightSummand, pow_add]
  rw [show -(2 * Real.pi * ((ℓ : ℝ) + 1) * y) =
    -2 * Real.pi * ((ℓ : ℝ) + 1) * y by ring]
  ring

theorem integrableOn_momentTerm (k e ℓ : ℕ) :
    IntegrableOn (momentTerm k e ℓ) (Ioi 0) := by
  unfold momentTerm
  exact (Common.integrableOn_pow_mul_exp_neg_mul (2 * e + k)
    (r := 2 * Real.pi * ((ℓ : ℝ) + 1)) (by positivity)).const_mul _

theorem integral_momentTerm (k e ℓ : ℕ) (hk : 2 ≤ k) :
    ∫ y in Ioi 0, momentTerm k e ℓ y =
      2 * ((2 * e + k).factorial : ℝ) /
        (((k - 1).factorial : ℝ) * (2 * Real.pi) ^ (2 * e + 2)) *
          (1 / ((ℓ : ℝ) + 1) ^ (2 * e + 2)) := by
  unfold momentTerm
  rw [integral_const_mul, Common.integral_pow_mul_exp_neg_mul _ (by positivity)]
  have hl : (0 : ℝ) < (ℓ : ℝ) + 1 := by positivity
  have hpi : (0 : ℝ) < 2 * Real.pi := by positivity
  have hfac : (0 : ℝ) < ((k - 1).factorial : ℝ) := by positivity
  have hsplit : 2 * e + k + 1 = (k - 1) + (2 * e + 2) := by omega
  rw [mul_pow (2 * Real.pi) ((ℓ : ℝ) + 1), hsplit]
  simp only [pow_add]
  field_simp

theorem momentTerm_nonneg (k e ℓ : ℕ) {y : ℝ} (hy : 0 < y) :
    0 ≤ momentTerm k e ℓ y := by
  unfold momentTerm
  positivity

/-- Euler's formula for the shifted positive-integer series. -/
private theorem even_zeta_series (e : ℕ) :
    ∑' ℓ : ℕ, 1 / ((ℓ : ℝ) + 1) ^ (2 * e + 2) =
      (-1 : ℝ) ^ (e + 2) * 2 ^ (2 * e + 1) * Real.pi ^ (2 * e + 2) *
        (bernoulli (2 * e + 2) : ℝ) / ((2 * e + 2).factorial : ℝ) := by
  have hz := hasSum_zeta_nat (k := e + 1) (by omega)
  have hz1 := (hasSum_nat_add_iff' 1).mpr hz
  simp only [Finset.range_one, Finset.sum_singleton, Nat.cast_zero, ne_eq,
    Nat.mul_eq_zero, OfNat.ofNat_ne_zero, Nat.add_eq_zero_iff, one_ne_zero, and_false,
    or_self, not_false_eq_true, zero_pow, div_zero, sub_zero] at hz1
  have hi : 2 * (e + 1) = 2 * e + 2 := by omega
  rw [hi, show 2 * e + 2 - 1 = 2 * e + 1 by omega] at hz1
  rw [← hz1.tsum_eq]
  refine tsum_congr fun ℓ => ?_
  push_cast
  ring_nf

/-- The polynomial moment identity, with integrability, for every `k ≥ 2`. -/
theorem mono_moment (k e : ℕ) (hk : 2 ≤ k) :
    IntegrableOn (fun y => y ^ (2 * e) * weight k y) (Ioi 0) ∧
      ∫ y in Ioi 0, y ^ (2 * e) * weight k y = (moment k e : ℝ) := by
  have hpt : ∀ y, y ^ (2 * e) * weight k y = ∑' ℓ, momentTerm k e ℓ y := by
    intro y
    simp_rw [momentTerm_eq]
    rw [tsum_mul_left]
    unfold weight weightSeries
    ring
  have hnorm : ∀ ℓ, ∫ y in Ioi 0, ‖momentTerm k e ℓ y‖ =
      ∫ y in Ioi 0, momentTerm k e ℓ y := by
    intro ℓ
    refine setIntegral_congr_fun measurableSet_Ioi fun y hy => ?_
    exact Real.norm_of_nonneg (momentTerm_nonneg k e ℓ hy)
  have hsum : Summable fun ℓ => ∫ y in Ioi 0, ‖momentTerm k e ℓ y‖ := by
    simp_rw [hnorm, integral_momentTerm k e _ hk]
    refine Summable.mul_left _ ?_
    have hs := (summable_nat_add_iff 1).mpr
      (Real.summable_one_div_nat_pow.mpr (by omega : 1 < 2 * e + 2))
    refine hs.congr fun ℓ => ?_
    push_cast
    ring
  have hswap : (∫ y in Ioi 0, y ^ (2 * e) * weight k y) =
      ∑' ℓ, ∫ y in Ioi 0, momentTerm k e ℓ y := by
    rw [setIntegral_congr_fun measurableSet_Ioi (fun y _ => hpt y)]
    exact (integral_tsum_of_summable_integral_norm
      (fun ℓ => integrableOn_momentTerm k e ℓ) hsum).symm
  constructor
  · apply Integrable.of_integral_ne_zero
    rw [hswap]
    have hs : Summable fun ℓ => ∫ y in Ioi 0, momentTerm k e ℓ y := by
      simpa only [hnorm] using hsum
    have hpos : ∀ ℓ, 0 < ∫ y in Ioi 0, momentTerm k e ℓ y := by
      intro ℓ
      rw [integral_momentTerm k e ℓ hk]
      positivity
    exact (hs.tsum_pos (fun ℓ => (hpos ℓ).le) 0 (hpos 0)).ne'
  · rw [hswap]
    simp_rw [integral_momentTerm k e _ hk]
    rw [tsum_mul_left, even_zeta_series, moment_factorial k e hk]
    push_cast
    have hfac : (0 : ℝ) < ((k - 1).factorial : ℝ) := by positivity
    have hfac2 : (0 : ℝ) < ((2 * e + 2).factorial : ℝ) := by positivity
    have hpi : 0 < Real.pi := Real.pi_pos
    field_simp
    ring

/-- Every real polynomial is integrable against the positive density after the
square substitution. This is the input required by the common Gram machinery. -/
theorem integrableOn_polynomial_weight (k : ℕ) (hk : 2 ≤ k) (p : ℝ[X]) :
    IntegrableOn (fun y => p.eval (y ^ 2) * weight k y) (Ioi 0) := by
  have hpt : ∀ y : ℝ, p.eval (y ^ 2) * weight k y =
      ∑ e ∈ Finset.range (p.natDegree + 1), p.coeff e * (y ^ (2 * e) * weight k y) := by
    intro y
    rw [Polynomial.eval_eq_sum_range, Finset.sum_mul]
    refine Finset.sum_congr rfl fun e _ => ?_
    rw [← pow_mul]
    ring
  have hsum : IntegrableOn (fun y =>
      ∑ e ∈ Finset.range (p.natDegree + 1), p.coeff e * (y ^ (2 * e) * weight k y)) (Ioi 0) :=
    integrable_finsetSum _ fun e _ => (mono_moment k e hk).1.const_mul _
  exact hsum.congr_fun (fun y _ => (hpt y).symm) measurableSet_Ioi

end ZetaFive

