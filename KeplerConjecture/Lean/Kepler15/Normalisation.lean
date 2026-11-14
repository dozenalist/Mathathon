/-
Kepler problem 15 — frozen definitions and the density normalisation.

Status: DRAFTED by Main, awaiting a local build under the pinned toolchain
(Lean v4.35.0 / Mathlib v4.35.0). It has been elaborated once against the VM's
Lean 4.33.1 Mathlib as a syntax/type pre-check only; that is not the pinned
build and is not kernel evidence for the claim ledger.

This file contains no analysis. It fixes the objects that every later formal
statement about the Kepler bound must use, so that a future theorem cannot
silently change scale:

  * `IsPacking`            : minimum separation 2, unit balls (radius 1)
  * `localDensity`/`upperDensity` : occupied-volume upper density
  * `centreDensity`        : `upperDensity / (4 pi / 3)`, with the identity
                             `centreDensity = 3 * upperDensity / (4 pi)`
  * `HasContactNumber`     : the hypothesis `(LC(A,n))` of the truncated
                             two-point bound (K15-C003, Theorem B)

The Fourier transform is deliberately *not* defined here. The target statement
of K15-C003 requires `fhat t = integral f(x) exp(-2 pi i <x,t>) dx` with the
real-valued sign conditions `fhat >= 0` and `fhat 0 > 0`; that belongs in a
second module together with the admissibility class of Cohn-Elkies. Fixing the
scale first is what this file is for.

Scale convention (K15-C001, K15-C007): radius 1, separation 2. A configuration
quoted at radius 1/2 and separation 1 has `n` centres per unit volume; the same
configuration at radius 1 has centre density `n / 8` and occupied-volume density
`(pi / 6) * n`.
-/
import Mathlib

open MeasureTheory Filter
open scoped Topology

namespace Kepler15

/-- Euclidean three-space, the ambient space throughout. -/
abbrev E3 : Type := EuclideanSpace ℝ (Fin 3)

/-- A packing: a set of centres with pairwise distance at least 2.
The balls of radius 1 centred there are then pairwise disjoint. -/
def IsPacking (Λ : Set E3) : Prop :=
  ∀ x ∈ Λ, ∀ y ∈ Λ, x ≠ y → 2 ≤ dist x y

/-- Volume of the unit ball in `E3`, as a real number: `4 pi / 3`. -/
noncomputable def volB1 : ℝ := 4 * Real.pi / 3

/-- Occupied volume fraction in the ball of radius `R` about the origin:
the volume of the union of the unit balls centred at `Λ`, intersected with
`B(0,R)`, divided by the volume of `B(0,R)`. -/
noncomputable def localDensity (Λ : Set E3) (R : ℝ) : ℝ :=
  (volume (Metric.ball (0 : E3) R ∩ ⋃ x ∈ Λ, Metric.ball x 1)).toReal /
    (volume (Metric.ball (0 : E3) R)).toReal

/-- Upper occupied-volume density, `limsup` over `R → ∞`. -/
noncomputable def upperDensity (Λ : Set E3) : ℝ :=
  limsup (localDensity Λ) atTop

/-- Centre density: occupied-volume density divided by the volume of the unit
ball, i.e. the number of centres per unit volume in the limit. -/
noncomputable def centreDensity (Λ : Set E3) : ℝ :=
  upperDensity Λ / volB1

/-- `centreDensity = 3 * upperDensity / (4 pi)`: the normalisation bridge
between the two standard ways of quoting a packing bound. -/
theorem centreDensity_eq (Λ : Set E3) :
    centreDensity Λ = 3 * upperDensity Λ / (4 * Real.pi) := by
  unfold centreDensity volB1
  field_simp

/-- Number of points of a finite 2-separated set `X` whose difference from `x`
lies in `A`. This is the quantity bounded by a contact number. -/
noncomputable def countIn (X : Finset E3) (x : E3) (A : Set E3) : ℕ := by
  classical
  exact (X.filter (fun y => y - x ∈ A)).card

/-- `A` has contact number at most `n`: no 2-separated set sees more than `n`
`A`-differences from any one of its points. This is hypothesis `(LC(A,n))` of
K15-C003. -/
def HasContactNumber (A : Set E3) (n : ℕ) : Prop :=
  ∀ (X : Finset E3) (x : E3), x ∈ X →
    (∀ y ∈ X, ∀ z ∈ X, y ≠ z → 2 ≤ dist y z) → countIn X x A ≤ n

end Kepler15
