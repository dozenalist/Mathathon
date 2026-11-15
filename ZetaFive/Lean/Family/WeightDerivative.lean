module

public import ZetaFive.Lean.Family.Weight
public import Mathlib.Analysis.Calculus.Deriv.Pow
public import Mathlib.Analysis.Calculus.SmoothSeries
public import Mathlib.Tactic.Convert
public import Mathlib.Tactic.FieldSimp

@[expose] public section

/-!
# The differential recurrence for the positive weights

The exponential series can be differentiated locally uniformly. In particular,
`w'_k(y) = (k/y) (w_k(y) - w_(k+1)(y))` for `y > 0` and `k ≥ 1`.

This file does **not** assert `PoleMoments k`. A remaining route to that identity
is to set `I_k(a) = ∫₀∞ w_k(y)/(y²+a²) dy` for `a > 0` and prove the base formula
`I_2(a) = a * ∑_{n≥1} (a+n)^(-2) - 1 + 1/(2a)`. Integration by parts and
differentiation under the integral would then give
`I_(k+1)(a) = ((k-1)/k) I_k(a) - (a/k) I'_k(a)`. Differentiating the convergent
series on the right gives the general formula
`I_k(a) = a^(k-1) * ∑_{n≥1} (a+n)^(-k) - 1/(k-1) + 1/(2a)`.
At `a = j`, the sum is `zeta k - harmonic k j`, exactly `PoleMoments k`.
The derivative statements below are unconditional prerequisites for that route;
none of these remaining integral or series identities is assumed or asserted here.
-/

open Filter Topology Set

namespace ZetaFive

/-- Differentiating one term increments the power of its positive integer index. -/
theorem hasDerivAt_weightSummand (k : ℕ) (hk : 1 ≤ k) (n : ℕ) (y : ℝ) :
    HasDerivAt (weightSummand k n)
      (-(2 * Real.pi) * weightSummand (k + 1) n y) y := by
  have hd := (((hasDerivAt_id y).const_mul
    (-2 * Real.pi * ((n : ℝ) + 1))).exp).const_mul (((n : ℝ) + 1) ^ (k - 1))
  apply hd.congr_deriv
  simp only [weightSummand, id, mul_one, Nat.add_sub_cancel]
  have hp : ((n : ℝ) + 1) ^ k = ((n : ℝ) + 1) ^ (k - 1) * ((n : ℝ) + 1) := by
    simpa only [Nat.sub_add_cancel hk] using (pow_succ ((n : ℝ) + 1) (k - 1))
  rw [hp]
  ring

/-- Differentiation of the entire series is justified on every interval bounded
away from zero by the summable next-weight series. -/
theorem hasDerivAt_weightSeries (k : ℕ) (hk : 1 ≤ k) {y : ℝ} (hy : 0 < y) :
    HasDerivAt (weightSeries k)
      (-(2 * Real.pi) * weightSeries (k + 1) y) y := by
  let a := y / 2
  have ha : 0 < a := by dsimp [a]; linarith
  have hay : a < y := by dsimp [a]; linarith
  have hu : Summable (fun n : ℕ => 2 * Real.pi * weightSummand (k + 1) n a) :=
    (summable_weightSummand (k + 1) ha).mul_left _
  have hbound : ∀ n z, z ∈ Ioi a →
      ‖-(2 * Real.pi) * weightSummand (k + 1) n z‖ ≤
        2 * Real.pi * weightSummand (k + 1) n a := by
    intro n z hz
    rw [norm_mul, norm_neg, Real.norm_of_nonneg (by positivity : 0 ≤ 2 * Real.pi),
      Real.norm_of_nonneg (weightSummand_pos (k + 1) n z).le]
    exact mul_le_mul_of_nonneg_left (weightSummand_antitone (k + 1) n hz.le)
      (by positivity)
  have hs := hasDerivAt_tsum_of_isPreconnected
    (g := weightSummand k)
    (g' := fun n z => -(2 * Real.pi) * weightSummand (k + 1) n z)
    (t := Ioi a) (y₀ := y) (y := y)
    hu isOpen_Ioi isPreconnected_Ioi
    (fun n z _ => hasDerivAt_weightSummand k hk n z)
    hbound hay (summable_weightSummand k hy) hay
  convert! hs using 1
  simp only [weightSeries, tsum_mul_left]

/-- The adjacent positive densities satisfy one differential recurrence. -/
theorem hasDerivAt_weight (k : ℕ) (hk : 1 ≤ k) {y : ℝ} (hy : 0 < y) :
    HasDerivAt (weight k)
      ((k : ℝ) / y * (weight k y - weight (k + 1) y)) y := by
  have hd := (((hasDerivAt_pow k y).const_mul (2 * (2 * Real.pi) ^ (k - 1))).div_const
    ((k - 1).factorial : ℝ)).mul (hasDerivAt_weightSeries k hk hy)
  apply hd.congr_deriv
  have hkR : (0 : ℝ) < k := by exact_mod_cast (by omega : 0 < k)
  have hfactR : (0 : ℝ) < ((k - 1).factorial : ℝ) := by positivity
  have hfac : (k.factorial : ℝ) = (k : ℝ) * ((k - 1).factorial : ℝ) := by
    have hf := Nat.factorial_succ (k - 1)
    simp only [Nat.sub_add_cancel hk] at hf
    exact_mod_cast hf
  have hpi : 0 < 2 * Real.pi := by positivity
  have hp : (2 * Real.pi) ^ k = (2 * Real.pi) ^ (k - 1) * (2 * Real.pi) := by
    simpa only [Nat.sub_add_cancel hk] using (pow_succ (2 * Real.pi) (k - 1))
  have hyp : y ^ k = y ^ (k - 1) * y := by
    simpa only [Nat.sub_add_cancel hk] using (pow_succ y (k - 1))
  simp only [weight, Nat.add_sub_cancel, hfac, hp, hyp, pow_succ]
  field_simp
  ring

end ZetaFive
