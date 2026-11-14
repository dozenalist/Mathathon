/-
Kepler problem 15 — the ball-volume identity for `E3`.

Status: DRAFTED by Main, NOT compiled by Main (the VM must not run Lean; see
`Main/LOCAL_COMPUTE_REQUESTS.md`, request `M-LEAN-002`). Everything here is
`PROPOSED` until a pinned Lean 4.35.0 build reports exit 0 and the axiom audit.

Why this lemma. `Lean/Kepler15/Normalisation.lean` defines `volB1 : ℝ := 4 * π / 3`
and proves only the algebraic identity `centreDensity = 3·upperDensity/(4π)`.
That file's `volB1` is a *definition*: it does not prove that the Lebesgue volume
of the unit ball in `E3` is that number. `K15-C024` lists the missing bridge:
ball volume → occupied volume → centre density. This module supplies the first
link, which is stable and independent of any research choice.

Two candidate proof routes, in order of preference:
  (R1) `EuclideanSpace.volume_ball` gives
       `volume (ball x r) = r ^ n * π ^ (n/2) / Gamma (n/2 + 1)` for `Fin n`;
       with `n = 3` and `Gamma (5/2) = 3√π/4` this is `4π/3`.
  (R2) iterate `MeasureTheory.volume_eq_prod` / Fubini over the three
       coordinates — much longer, keep as a fallback.
If (R1) is unavailable under this Mathlib version, the build log should say so and
this file is revised rather than patched with `sorry`.
-/
import Mathlib.MeasureTheory.Measure.Lebesgue.VolumeOfBalls
import Mathlib.Tactic

open MeasureTheory
open scoped Topology

namespace Kepler15

/-- Euclidean three-space. -/
abbrev E3 : Type := EuclideanSpace ℝ (Fin 3)

/-- The number `4π/3`, as a definition (kept for compatibility with
`Normalisation.lean`; the *theorem* below is what carries content). -/
noncomputable def volB1 : ℝ := 4 * Real.pi / 3

/-- The Lebesgue volume of the unit ball in `E3` is `4π/3`. -/
theorem volume_ball_unit :
    volume (Metric.ball (0 : E3) 1) = ENNReal.ofReal (4 * Real.pi / 3) := by
  -- R1: Mathlib's general ball-volume formula at n = 3, r = 1.
  rw [EuclideanSpace.volume_ball]
  -- goal is now `1 ^ 3 * π ^ (3/2) / Gamma (3/2 + 1) = ofReal (4π/3)`
  norm_num [Real.Gamma_nat_add_one_over_two]

/-- Scaling form, which is what the periodic-approximation estimate uses. -/
theorem volume_ball_three (R : ℝ) (hR : 0 ≤ R) :
    volume (Metric.ball (0 : E3) R) = ENNReal.ofReal (4 * Real.pi / 3 * R ^ 3) := by
  rw [EuclideanSpace.volume_ball]
  norm_num [Real.Gamma_nat_add_one_over_two]
  ring_nf

/-- The arithmetic step of the transfer lemma (`K15-C035`):
`(r+R)^3 - r^3 <= 3 R (R+1)^2 r^2` for `r >= 1`, `R >= 0`.

This is purely polynomial — no analysis, no `Gamma`, no measure — so it is the
part of the Lean plan that should compile first and independently of the
ball-volume identity.  Proof: expand, divide by `R` (the case `R = 0` is
trivial), and bound `R^2 <= 3 r^2 R^2`, `3 r R <= 6 r^2 R` using `r >= 1`. -/
theorem cube_diff_le (R r : ℝ) (hr : 1 ≤ r) (hR : 0 ≤ R) :
    (r + R) ^ 3 - r ^ 3 ≤ 3 * R * (R + 1) ^ 2 * r ^ 2 := by
  have hRr : 0 ≤ R := hR
  have h1 : (r + R) ^ 3 - r ^ 3 = R * (3 * r ^ 2 + 3 * r * R + R ^ 2) := by ring
  have h2 : 3 * r ^ 2 + 3 * r * R + R ^ 2 ≤ 3 * r ^ 2 * (R + 1) ^ 2 := by
    nlinarith [sq_nonneg (r - 1), sq_nonneg R, sq_nonneg (R * r), hr, hRr,
      mul_nonneg (mul_nonneg hRr hRr) (sq_nonneg r)]
  have h3 : 0 ≤ 3 * r ^ 2 * R := by positivity
  calc (r + R) ^ 3 - r ^ 3 = R * (3 * r ^ 2 + 3 * r * R + R ^ 2) := h1
    _ ≤ R * (3 * r ^ 2 * (R + 1) ^ 2) := by
          exact mul_le_mul_of_nonneg_left h2 hRr
    _ = 3 * R * (R + 1) ^ 2 * r ^ 2 := by ring

end Kepler15

#print axioms Kepler15.volume_ball_unit
#print axioms Kepler15.volume_ball_three
#print axioms Kepler15.cube_diff_le
