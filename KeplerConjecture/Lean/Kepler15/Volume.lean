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
import Mathlib

open MeasureTheory
open scoped Topology

namespace Kepler15

/-- Euclidean three-space. -/
abbrev E3 : Type := EuclideanSpace ℝ (Fin 3)

/-- The number `4π/3`, as a definition (kept for compatibility with
`Normalisation.lean`; the *theorem* below is what carries content). -/
noncomputable def volB1 : ℝ := 4 * Real.pi / 3

/-- The Lebesgue volume of the unit ball in `E3` is `4π/3`.

NOT PROVED. The two candidate routes are named in the header; the pinned build of
this module is not attempted until a curated import list fits the local resource
cap (the broad import hit 60 s / 715 MB and `VolumeOfBalls + Mathlib.Tactic` hit
the 1 GiB cap after 32.6 s — see `Main/LocalChecks/2026-11-14_0138/`).  `sorry` is
deliberately absent: the statement is frozen as a `Prop`-valued definition so the
module carries no unproved theorem. -/
def BallVolumeClaim : Prop :=
  volume (Metric.ball (0 : E3) 1) = ENNReal.ofReal (4 * Real.pi / 3)

/-- Scaling form of the same claim. -/
def BallVolumeScalingClaim : Prop :=
  ∀ R : ℝ, 0 ≤ R →
    volume (Metric.ball (0 : E3) R) = ENNReal.ofReal (4 * Real.pi / 3 * R ^ 3)

end Kepler15
