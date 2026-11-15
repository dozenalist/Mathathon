module

/-
Adapted from `Apery/DetIntegral.lean` in https://github.com/mo271/Zeta5,
commit 7fe736760f4b96bfdb4334b68e3b3124ecbe10b0, under Apache 2.0.
See ZetaFive/Lean/LICENSES/mo271-Zeta5.txt.
-/
public import ZetaFive.Lean.Common.Andreief
public import ZetaFive.Lean.Family.Positivity

@[expose] public section

/-!
# The actual Hankel determinant as a multiple integral

The parameters and zeta index are arbitrary. The pole identity is an explicit
hypothesis, as in `Family.Positivity`; this file does not assert that missing
identity. Andréief's identity itself is proved once in the common library.
-/

open Polynomial MeasureTheory Set Finset
open ZetaFive.Common

namespace ZetaFive

/-- The squared Vandermonde times the product of the modified densities. -/
noncomputable def determinantIntegrand (k : ℕ) (p : Parameters) (y : Fin p.h → ℝ) : ℝ :=
  (Matrix.vandermonde fun j => y j ^ 2).det ^ 2 * ∏ j, modifiedWeight k p (y j)

theorem determinantIntegrand_nonneg (k : ℕ) (p : Parameters) (y : Fin p.h → ℝ)
    (hy : ∀ i, 0 < y i) : 0 ≤ determinantIntegrand k p y := by
  exact mul_nonneg (sq_nonneg _) (Finset.prod_nonneg fun i _ =>
    (modifiedWeight_pos k p (hy i)).le)

/-- Andréief's formula for the actual determinant, uniformly in all parameters. -/
theorem delta_eq_integral (k : ℕ) (hk : 2 ≤ k) (hPole : PoleMoments k) (p : Parameters) :
    aeval (zeta k) (delta k p) = (1 / (p.h.factorial : ℝ)) *
      ∫ y : Fin p.h → ℝ, determinantIntegrand k p y
        ∂(Measure.pi fun _ : Fin p.h => positiveRayMeasure) := by
  have hdet : aeval (zeta k) (delta k p) =
      ((hankel k p).map (aeval (zeta k))).det := by
    have hmap := RingHom.map_det (aeval (zeta k) : ℚ[X] →ₐ[ℚ] ℝ).toRingHom (hankel k p)
    simpa [delta, RingHom.mapMatrix_apply] using hmap
  let f : Fin p.h → ℝ → ℝ := fun i y => (y ^ 2) ^ (i : ℕ)
  let g : Fin p.h → ℝ → ℝ := fun j y => (y ^ 2) ^ (j : ℕ) * modifiedWeight k p y
  have hentry : (hankel k p).map (aeval (zeta k)) =
      Matrix.of fun i j => ∫ y, f i y * g j y ∂positiveRayMeasure := by
    ext i j
    change aeval (zeta k)
      (mu k p.K (D p.N ^ p.numeratorPower * X ^ ((i : ℕ) + (j : ℕ)))) = _
    rw [(moment_rep k hk hPole _ _).2]
    refine setIntegral_congr_fun measurableSet_Ioi fun y _ => ?_
    dsimp [f, g]
    rw [integrand_monomial, pow_add]
    ring
  have hfg : ∀ i j, Integrable (fun y => f i y * g j y) positiveRayMeasure := by
    intro i j
    have hint := (moment_rep k hk hPole p.K
      (D p.N ^ p.numeratorPower * X ^ ((i : ℕ) + (j : ℕ)))).1
    refine hint.congr_fun (fun y _ => ?_) measurableSet_Ioi
    dsimp [f, g]
    rw [integrand_monomial, pow_add]
    ring
  rw [hdet, hentry, andreief f g hfg]
  congr 1
  refine integral_congr_ae (Filter.Eventually.of_forall fun y => ?_)
  have h1 : (Matrix.of fun i j => f i (y j)).det =
      (Matrix.vandermonde fun j => y j ^ 2).det := by
    rw [← Matrix.det_transpose (Matrix.vandermonde _)]
    refine congrArg Matrix.det ?_
    ext i j
    simp [f, Matrix.vandermonde, Matrix.transpose_apply]
  have h2 : (Matrix.of fun i j => g i (y j)).det =
      (∏ j, modifiedWeight k p (y j)) * (Matrix.vandermonde fun j => y j ^ 2).det := by
    have hmatrix : (Matrix.of fun i j => g i (y j)) =
        Matrix.of fun i j => modifiedWeight k p (y j) *
          (Matrix.of fun i j => f i (y j)) i j := by
      ext i j
      simp [f, g]
      ring
    rw [hmatrix, Matrix.det_mul_row, h1]
  change (Matrix.of fun i j => f i (y j)).det *
    (Matrix.of fun i j => g i (y j)).det = determinantIntegrand k p y
  rw [h1, h2]
  unfold determinantIntegrand
  ring

end ZetaFive
