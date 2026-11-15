module

public import ZetaFive.Lean.Common.Criterion

@[expose] public section

/-! # Combining arithmetic cost with real decay

This theorem is independent of zeta values. Its hypotheses are the separate
arithmetical and analytical estimates that must actually be proved for a given
family. There is no assumption of the resulting irrationality statement.
-/

open Polynomial Filter Topology

namespace ZetaFive.Common

/-- Clearing denominators and combining two quadratic exponential bounds. -/
theorem irrational_of_normalized_estimates
    (ξ : ℝ) (d : ℕ) (F : ℕ → ℚ[X]) (m : ℕ → ℚ) (Q : ℕ → ℤ[X])
    (A U : ℝ) (hmargin : A + U < 0)
    (hdegree : ∀ n, (F n).natDegree ≤ d * n)
    (hintegral : ∀ᶠ n in atTop, (Q n).map (Int.castRingHom ℚ) = C (m n) * F n)
    (hm : ∀ᶠ n in atTop, 0 < m n)
    (hpos : ∀ᶠ n in atTop, 0 < (F n).eval₂ (Rat.castHom ℝ) ξ)
    (harithmetic : ∀ᶠ n in atTop, (m n : ℝ) ≤ Real.exp (A * (n : ℝ) ^ 2))
    (hanalytic : ∀ᶠ n in atTop,
      (F n).eval₂ (Rat.castHom ℝ) ξ ≤ Real.exp (U * (n : ℝ) ^ 2)) :
    Irrational ξ := by
  apply irrational_of_eventually_exists_int_poly_exp ξ d (c := -(A + U)) (by linarith)
  filter_upwards [hintegral, hm, hpos, harithmetic, hanalytic] with n hi hm hp ha hu
  refine ⟨Q n, ?_, ?_, ?_⟩
  · have hdeg := congrArg Polynomial.natDegree hi
    rw [natDegree_map_eq_of_injective
      (show Function.Injective (Int.castRingHom ℚ) from Int.cast_injective)] at hdeg
    rw [hdeg]
    exact (natDegree_C_mul_le _ _).trans (hdegree n)
  all_goals
    have heval : aeval ξ (Q n) = (m n : ℝ) * (F n).eval₂ (Rat.castHom ℝ) ξ := by
      have h := congrArg (Polynomial.eval₂ (Rat.castHom ℝ) ξ) hi
      have hcomp : (Rat.castHom ℝ).comp (Int.castRingHom ℚ) = Int.castRingHom ℝ :=
        RingHom.ext_int _ _
      simpa [Polynomial.eval₂_map, Polynomial.eval₂_mul, Polynomial.aeval_def,
        RingHom.comp_apply, hcomp] using h
    rw [heval]
  · exact mul_pos (by exact_mod_cast hm) hp
  · calc
      (m n : ℝ) * (F n).eval₂ (Rat.castHom ℝ) ξ ≤
          Real.exp (A * (n : ℝ) ^ 2) * Real.exp (U * (n : ℝ) ^ 2) :=
        mul_le_mul ha hu hp.le (Real.exp_pos _).le
      _ = Real.exp (- -(A + U) * (n : ℝ) ^ 2) := by
        rw [← Real.exp_add]
        congr 1
        ring

end ZetaFive.Common

