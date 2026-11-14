/-
Kepler problem 15 — the polynomial step of the transfer lemma (`K15-C035`).

Status: DRAFTED by Main, NOT compiled. Narrow imports on purpose: the earlier
`Volume.lean` reached the 1 GiB cap with `import Mathlib` (60 s) and with
`VolumeOfBalls + Mathlib.Tactic` (32.6 s, 1 GiB), so this file imports only the
three tactics the proof uses. Request `M-LEAN-003`.

Statement:  (r + R)^3 - r^3 <= 3 R (R+1)^2 r^2   for  r >= 1, R >= 0.
Proof route (worked out in `Main/CLAIMS.md`, K15-C035): expand, divide by R, and
bound R^2 <= 3 r^2 R^2 and 3 r R <= 6 r^2 R using r >= 1.
-/
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

namespace Kepler15

theorem cube_diff_le (R r : ℝ) (hr : 1 ≤ r) (hR : 0 ≤ R) :
    (r + R) ^ 3 - r ^ 3 ≤ 3 * R * (R + 1) ^ 2 * r ^ 2 := by
  have h1 : (r + R) ^ 3 - r ^ 3 = R * (3 * r ^ 2 + 3 * r * R + R ^ 2) := by ring
  have h2 : 3 * r ^ 2 + 3 * r * R + R ^ 2 ≤ 3 * r ^ 2 * (R + 1) ^ 2 := by
    nlinarith [sq_nonneg (r - 1), sq_nonneg R, sq_nonneg (R * r), hr, hR,
      mul_nonneg hR (sq_nonneg r), mul_nonneg (mul_nonneg hR hR) (sq_nonneg r)]
  calc (r + R) ^ 3 - r ^ 3 = R * (3 * r ^ 2 + 3 * r * R + R ^ 2) := h1
    _ ≤ R * (3 * r ^ 2 * (R + 1) ^ 2) := by
          exact mul_le_mul_of_nonneg_left h2 hR
    _ = 3 * R * (R + 1) ^ 2 * r ^ 2 := by ring

end Kepler15
