module

public import Mathlib.Analysis.SpecialFunctions.Exp
public import Mathlib.Analysis.SpecificLimits.Normed
public import Mathlib.Analysis.Real.Pi.Bounds
public import Mathlib.Analysis.Normed.Group.FunctionSeries
public import Mathlib.MeasureTheory.Constructions.Polish.Basic
public import Mathlib.Tactic.FunProp
public import Mathlib.Tactic.Linarith
public import Mathlib.Tactic.NormNum
public import Mathlib.Tactic.Positivity
public import Mathlib.Tactic.Ring

@[expose] public section

/-!
# The positive zeta weight

For a positive real argument the exponential series defining Calegari's weight
converges, is strictly positive, and varies continuously with the argument.
These statements are uniform in the natural weight index; its interpretation as
a zeta moment will require `2 ≤ k` in the moment-representation theorem.
-/

open Filter Topology MeasureTheory Set

namespace ZetaFive

/-- The term with positive integer index `n + 1` in the exponential series. -/
noncomputable def weightSummand (k n : ℕ) (y : ℝ) : ℝ :=
  ((n : ℝ) + 1) ^ (k - 1) * Real.exp (-2 * Real.pi * ((n : ℝ) + 1) * y)

/-- The series occurring in the positive density. -/
noncomputable def weightSeries (k : ℕ) (y : ℝ) : ℝ := ∑' n : ℕ, weightSummand k n y

/-- The positive density `w_k` of the general moment construction. -/
noncomputable def weight (k : ℕ) (y : ℝ) : ℝ :=
  (2 * (2 * Real.pi) ^ (k - 1) * y ^ k / ((k - 1).factorial : ℝ)) * weightSeries k y

lemma weightSummand_pos (k n : ℕ) (y : ℝ) : 0 < weightSummand k n y := by
  unfold weightSummand
  positivity

lemma weightSummand_eq_geometric (k n : ℕ) (y : ℝ) :
    weightSummand k n y = ((n + 1 : ℕ) : ℝ) ^ (k - 1) *
      Real.exp (-2 * Real.pi * y) ^ (n + 1) := by
  rw [weightSummand, ← Real.exp_nat_mul]
  push_cast
  congr 2
  ring

/-- Polynomial factors do not prevent convergence of the exponentially decaying series. -/
theorem summable_weightSummand (k : ℕ) {y : ℝ} (hy : 0 < y) :
    Summable (fun n : ℕ => weightSummand k n y) := by
  have hr : ‖Real.exp (-2 * Real.pi * y)‖ < 1 := by
    rw [Real.norm_eq_abs, abs_of_pos (Real.exp_pos _), Real.exp_lt_one_iff]
    nlinarith [Real.pi_pos]
  have hs := summable_pow_mul_geometric_of_norm_lt_one (k - 1) hr
  have hshift := (summable_nat_add_iff 1).mpr hs
  exact hshift.congr fun n => (weightSummand_eq_geometric k n y).symm

theorem weightSeries_pos (k : ℕ) {y : ℝ} (hy : 0 < y) : 0 < weightSeries k y := by
  exact (summable_weightSummand k hy).tsum_pos
    (fun n => (weightSummand_pos k n y).le) 0 (weightSummand_pos k 0 y)

theorem weightSeries_nonneg (k : ℕ) (y : ℝ) : 0 ≤ weightSeries k y :=
  tsum_nonneg fun n => (weightSummand_pos k n y).le

theorem weight_pos (k : ℕ) {y : ℝ} (hy : 0 < y) : 0 < weight k y := by
  unfold weight
  exact mul_pos (by positivity) (weightSeries_pos k hy)

theorem weight_nonneg (k : ℕ) {y : ℝ} (hy : 0 ≤ y) : 0 ≤ weight k y := by
  unfold weight
  exact mul_nonneg (by positivity) (weightSeries_nonneg k y)

lemma continuous_weightSummand (k n : ℕ) : Continuous (weightSummand k n) := by
  unfold weightSummand
  fun_prop

/-- Each summand decreases as the positive integration variable increases. -/
lemma weightSummand_antitone (k n : ℕ) : Antitone (weightSummand k n) := by
  intro a b hab
  unfold weightSummand
  apply mul_le_mul_of_nonneg_left _ (by positivity)
  apply Real.exp_le_exp.mpr
  have hc : 0 ≤ 2 * Real.pi * ((n : ℝ) + 1) := by positivity
  nlinarith [mul_le_mul_of_nonneg_left hab hc]

/-- The convergence is uniform on every interval bounded away from zero. -/
theorem continuousOn_weightSeries_Ici (k : ℕ) {a : ℝ} (ha : 0 < a) :
    ContinuousOn (weightSeries k) (Ici a) := by
  apply continuousOn_tsum (fun n => (continuous_weightSummand k n).continuousOn)
    (summable_weightSummand k ha)
  intro n y hy
  rw [Real.norm_eq_abs, abs_of_pos (weightSummand_pos k n y)]
  exact weightSummand_antitone k n hy

theorem continuousOn_weightSeries (k : ℕ) : ContinuousOn (weightSeries k) (Ioi 0) := by
  intro y hy
  have ha : 0 < y / 2 := by linarith [show 0 < y from hy]
  exact ((continuousOn_weightSeries_Ici k ha).continuousAt
    (Ici_mem_nhds (by linarith : y / 2 < y))).continuousWithinAt

theorem continuousOn_weight (k : ℕ) : ContinuousOn (weight k) (Ioi 0) := by
  unfold weight
  exact (by fun_prop : ContinuousOn
    (fun y : ℝ => 2 * (2 * Real.pi) ^ (k - 1) * y ^ k /
      ((k - 1).factorial : ℝ)) (Ioi 0)).mul (continuousOn_weightSeries k)

/-- Measurability holds globally, including the totalized sum outside the positive axis. -/
theorem measurable_weightSeries (k : ℕ) : Measurable (weightSeries k) := by
  exact Measurable.tsum fun n => (continuous_weightSummand k n).measurable

theorem measurable_weight (k : ℕ) : Measurable (weight k) := by
  unfold weight
  exact (by fun_prop : Measurable
    (fun y : ℝ => 2 * (2 * Real.pi) ^ (k - 1) * y ^ k /
      ((k - 1).factorial : ℝ))).mul (measurable_weightSeries k)

/-- One constant suffices for the exponential tails of all four requested weights. -/
noncomputable def weightTailConstant : ℝ :=
  2 * (2 * Real.pi) ^ 4 * Real.exp (2 * Real.pi) * weightSeries 5 1

theorem weightTailConstant_pos : 0 < weightTailConstant := by
  unfold weightTailConstant
  exact mul_pos (by positivity) (weightSeries_pos 5 (by norm_num))

lemma weightSummand_le_uniform_tail {k : ℕ} (hk : k ≤ 5) (n : ℕ)
    {y : ℝ} (hy : 1 ≤ y) :
    weightSummand k n y ≤ Real.exp (2 * Real.pi) * weightSummand 5 n 1 *
      Real.exp (-2 * Real.pi * y) := by
  have hp : ((n : ℝ) + 1) ^ (k - 1) ≤ ((n : ℝ) + 1) ^ 4 :=
    pow_le_pow_right₀ (by have hn : (0 : ℝ) ≤ n := Nat.cast_nonneg n; linarith) (by omega)
  have hny : 0 ≤ (n : ℝ) * (y - 1) :=
    mul_nonneg (Nat.cast_nonneg _) (sub_nonneg.mpr hy)
  have he : Real.exp (-2 * Real.pi * ((n : ℝ) + 1) * y) ≤
      Real.exp (2 * Real.pi) * Real.exp (-2 * Real.pi * ((n : ℝ) + 1) * 1) *
        Real.exp (-2 * Real.pi * y) := by
    rw [← Real.exp_add, ← Real.exp_add]
    apply Real.exp_le_exp.mpr
    nlinarith [mul_nonneg (by positivity : 0 ≤ 2 * Real.pi) hny]
  calc
    weightSummand k n y ≤ ((n : ℝ) + 1) ^ 4 *
        (Real.exp (2 * Real.pi) * Real.exp (-2 * Real.pi * ((n : ℝ) + 1) * 1) *
          Real.exp (-2 * Real.pi * y)) :=
      mul_le_mul hp he (Real.exp_pos _).le (by positivity)
    _ = _ := by norm_num [weightSummand]; ring

theorem weightSeries_le_uniform_tail {k : ℕ} (hk : k ≤ 5) {y : ℝ} (hy : 1 ≤ y) :
    weightSeries k y ≤ Real.exp (2 * Real.pi) * weightSeries 5 1 *
      Real.exp (-2 * Real.pi * y) := by
  have hs := Summable.tsum_le_tsum (fun n => weightSummand_le_uniform_tail hk n hy)
    (summable_weightSummand k (by linarith))
    (((summable_weightSummand 5 (by norm_num : (0 : ℝ) < 1)).mul_left
      (Real.exp (2 * Real.pi))).mul_right (Real.exp (-2 * Real.pi * y)))
  simpa only [weightSeries, tsum_mul_left, tsum_mul_right] using hs

/-- A proved common tail bound, retaining the exact exponential rate `2π`. -/
theorem weight_le_uniform_tail {k : ℕ} (hk : k ≤ 5) {y : ℝ} (hy : 1 ≤ y) :
    weight k y ≤ weightTailConstant * y ^ 5 * Real.exp (-2 * Real.pi * y) := by
  have hy0 : 0 < y := by linarith
  have hfactorial : (1 : ℝ) ≤ ((k - 1).factorial : ℝ) := by
    exact_mod_cast Nat.one_le_iff_ne_zero.mpr (Nat.factorial_ne_zero (k - 1))
  have hp : (2 * Real.pi) ^ (k - 1) ≤ (2 * Real.pi) ^ 4 :=
    pow_le_pow_right₀ (by linarith [Real.pi_gt_three]) (by omega)
  have hc : 2 * (2 * Real.pi) ^ (k - 1) * y ^ k / ((k - 1).factorial : ℝ) ≤
      2 * (2 * Real.pi) ^ 4 * y ^ 5 := by
    apply (div_le_self (by positivity) hfactorial).trans
    exact mul_le_mul (mul_le_mul_of_nonneg_left hp (by norm_num))
      (pow_le_pow_right₀ hy hk) (by positivity) (by positivity)
  calc
    weight k y ≤ (2 * (2 * Real.pi) ^ 4 * y ^ 5) *
        (Real.exp (2 * Real.pi) * weightSeries 5 1 * Real.exp (-2 * Real.pi * y)) :=
      mul_le_mul hc (weightSeries_le_uniform_tail hk hy) (weightSeries_pos k hy0).le
        (by positivity)
    _ = _ := by unfold weightTailConstant; ring

end ZetaFive

