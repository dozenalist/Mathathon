/-
Copyright (c) 2026 Mathathon contributors. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
-/
import Mathlib
import ZetaFive.Lean.Correspondences.Basic
import ZetaFive.Lean.Correspondences.Transport

/-!
# Target 2: one parameter controls one residue functional

Source: `zeta5_unified_framework.tex` §4.1, equation `eq:mastermu`:
`μ_X(R) = ∫ R(y²)w(y)dy + (X-ξ)[t^{-3}]_∞ R`.

We formalize only the *algebraic* half: the affine dependence on `X` together
with the identification of its slope with the residue functional
`Λ(R) = Σ_j c_j j⁴`. The analytic half (the positive integral and the identity
`μ_ξ(R) = ∫ R(y²)w(y)dy`) is a *separately named obligation* (`OBL-analytic`);
it is not assumed anywhere below.

The domain is represented explicitly: a polynomial part in `t` plus a finite
list of simple poles at `t = -j²` with positive integer `j`. Statements about
this representation data (`Rep.mu`, `Rep.Lambda`) are distinguished from the
rational-function reading, which is recorded through `laurent_pole_expansion`
and the semantic bridge noted in `ZetaFive/Lean/CORRESPONDENCES.md`.
-/

namespace ZetaFive.Correspondences

noncomputable section

open scoped BigOperators
open Polynomial

/-! ## The domain and the two functionals -/

/-- A member of the functional's domain: polynomial part in `t` plus finitely
many simple poles at `t = -j²`, `j ≥ 1`. `poles` is an association list
`(j, c)` for the term `c/(t + j²)`; repeated indices are harmless. -/
structure Rep where
  poly : PolyT
  poles : List (ℕ × ℚ)
  hpos : ∀ jc ∈ poles, 1 ≤ jc.1

/-- The residue functional `Λ(R) = Σ_j c_j j⁴`: the `j⁴` is the coefficient of
`t^{-3}` in `(t+j²)^{-1}`, and the polynomial part contributes nothing. -/
def Rep.Lambda (R : Rep) : ℚ := (R.poles.map (fun jc => jc.2 * ((jc.1 : ℚ) ^ 4))).sum

/-- `μ_X` on the domain, from the *independent* pole values
`μ_X((t+j²)^{-1}) = j⁴(X - H_j^{(5)}) - 1/4 + 1/(2j)` and the Bernoulli
moments on the polynomial part. -/
def Rep.mu (R : Rep) (u : ℚ) : ℚ :=
  μpoly R.poly +
    (R.poles.map (fun jc =>
      jc.2 * ((jc.1 : ℚ) ^ 4 * (u - H5 jc.1) - 1 / 4 + (2 * (jc.1 : ℚ))⁻¹))).sum

/-! ## The affine parameter identity -/

/-- The pole contribution to `μ_u - μ_v` is `(u-v)` times the `j⁴` weight. -/
theorem list_pole_affine (l : List (ℕ × ℚ)) (u v : ℚ) :
    (l.map (fun jc =>
        jc.2 * ((jc.1 : ℚ) ^ 4 * (u - H5 jc.1) - 1 / 4 + (2 * (jc.1 : ℚ))⁻¹))).sum
      = (l.map (fun jc =>
          jc.2 * ((jc.1 : ℚ) ^ 4 * (v - H5 jc.1) - 1 / 4 + (2 * (jc.1 : ℚ))⁻¹))).sum
        + (u - v) * (l.map (fun jc => jc.2 * ((jc.1 : ℚ) ^ 4))).sum := by
  induction l with
  | nil => simp
  | cons a l ih =>
      simp only [List.map_cons, List.sum_cons] at *
      rw [ih]; ring

/-- **Target 2, affine parameter identity.** For `R` in the domain and rational
parameters `u, v`:
`μ_u(R) = μ_v(R) + (u-v) Λ(R)`. -/
theorem mu_affine (R : Rep) (u v : ℚ) :
    R.mu u = R.mu v + (u - v) * R.Lambda := by
  unfold Rep.mu Rep.Lambda
  rw [show (R.poles.map (fun jc =>
        jc.2 * ((jc.1 : ℚ) ^ 4 * (u - H5 jc.1) - 1 / 4 + (2 * (jc.1 : ℚ))⁻¹))).sum
      = (R.poles.map (fun jc =>
          jc.2 * ((jc.1 : ℚ) ^ 4 * (v - H5 jc.1) - 1 / 4 + (2 * (jc.1 : ℚ))⁻¹))).sum
        + (u - v) * (R.poles.map (fun jc => jc.2 * ((jc.1 : ℚ) ^ 4))).sum
      from list_pole_affine R.poles u v]
  ring

/-- The same identity in the form used for matrices: the pencil is affine with
slope the residue matrix. -/
theorem mu_sub_eq (R : Rep) (u v : ℚ) : R.mu u - R.mu v = (u - v) * R.Lambda := by
  have h := mu_affine R u v
  linarith

/-! ## The Laurent-coefficient reading of `Λ` -/

/-- The explicit finite expansion of a single pole at infinity:
`(t+jj)^{-1} = t^{-1} - jj t^{-2} + jj² t^{-3} - jj³/(t³(t+jj))`.
All terms of order `≥ -3` are displayed; the remainder is `O(t^{-4})`, so the
coefficient of `t^{-3}` is `jj²`. Taking `jj = j²` gives the `j⁴` of `Λ`. -/
theorem laurent_pole_expansion {F : Type*} [Field F] [CharZero F] (t jj : F)
    (ht : t ≠ 0) (h : t + jj ≠ 0) :
    1 / (t + jj) = 1 / t - jj / t ^ 2 + jj ^ 2 / t ^ 3 - jj ^ 3 / (t ^ 3 * (t + jj)) := by
  field_simp
  ring

/-- The `t^{-3}` coefficient of one pole term, in the form used by `Λ`. -/
theorem laurent_pole_coeff {F : Type*} [Field F] [CharZero F] (t j : F)
    (ht : t ≠ 0) (h : t + j ^ 2 ≠ 0) :
    1 / (t + j ^ 2)
      = 1 / t - j ^ 2 / t ^ 2 + j ^ 4 / t ^ 3 - j ^ 6 / (t ^ 3 * (t + j ^ 2)) := by
  field_simp
  ring

end

end ZetaFive.Correspondences
