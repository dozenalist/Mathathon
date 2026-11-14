/-
Copyright (c) 2026 Mathathon contributors. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
-/
import Mathlib
import ZetaFive.Lean.Correspondences.AffineParameter

/-!
# Target 3: one matrix in different coordinates

Source: `zeta5_unified_framework.tex` §1 (`D_N^6/D_K = W_K/T_K`), §4.1
(`G_X(p,q) = μ_X(Wpq/T)`) and §5.2 (equation `eq:congruence`,
`G_new = Cᵀ G_old C`, `det G_new = (det C)² det G_old`).

What is proved here:

* the cancellation identity of the rational weight;
* the entrywise affine-pencil identity `G(u) = G(v) + (u-v)M`, stated for a
  domain-valued family of entries, so that each entry is known to lie in the
  functional's domain by construction;
* the change-of-basis identity for determinants;
* the invertible-shift factorization `det(A + δB) = det(A) det(I + δ A⁻¹B)`.

What is *not* proved here: that the specific weight `W_K p q / T_K` lies in the
domain of `μ` (it requires the division of `W p q D_N` by `D_K` and the
simplicity of the poles at `-j²`), and every p-adic, unit and valuation claim.
Those are recorded as obligations in `ZetaFive/Main/CORRESPONDENCES_STATUS.md`.
-/

namespace ZetaFive.Correspondences

noncomputable section

open scoped BigOperators
open Polynomial
open Matrix

/-! ## The rational weight -/

/-- **Cancellation identity.** With `W = D_N^5` and `T = D_K/D_N`,
`D_N^6/D_K = W/T`, for nonzero `D_N, D_K`. -/
theorem weight_cancellation {F : Type*} [Field F] (DN DK : F) (_hN : DN ≠ 0) (_hK : DK ≠ 0) :
    DN ^ 6 / DK = DN ^ 5 / (DK / DN) := by
  rw [div_div_eq_mul_div, ← pow_succ]

/-- The nonzero hypotheses are what makes `T = D_K/D_N` a nonzero rational
function; the equation itself would also hold with a zero denominator because
Lean's division is total, so the hypotheses are recorded here rather than used
in the proof of `weight_cancellation`. -/
theorem weight_denom_ne_zero {F : Type*} [Field F] (DN DK : F) (hN : DN ≠ 0) (hK : DK ≠ 0) :
    DK / DN ≠ 0 :=
  div_ne_zero hK hN

/-! ## The Gram pencil -/

/-- The matrix of the bilinear form `(p,q) ↦ μ_u(Wpq/T)`, given as a
domain-valued family of entries: `A i j` *is* the class of `W pᵢ pⱼ/T` in the
functional's domain. Membership is thus a hypothesis of the construction, not
an afterthought. -/
def gramMatrix {ι : Type*} (A : ι → ι → Rep) (u : ℚ) : Matrix ι ι ℚ :=
  fun i j => (A i j).mu u

/-- The residue matrix `M`, entrywise `Λ(Wpq/T)`. -/
def residueMatrix {ι : Type*} (A : ι → ι → Rep) : Matrix ι ι ℚ :=
  fun i j => (A i j).Lambda

/-- **Target 3, affine pencil.** `G(u) = G(v) + (u-v) M`, entrywise. -/
theorem gramMatrix_affine {ι : Type*} (A : ι → ι → Rep) (u v : ℚ) :
    gramMatrix A u = gramMatrix A v + (u - v) • residueMatrix A := by
  ext i j
  simp only [gramMatrix, residueMatrix, Matrix.add_apply, Matrix.smul_apply, smul_eq_mul]
  exact mu_affine (A i j) u v

/-! ## Change of basis -/

/-- **Change of basis.** `det(Cᵀ G C) = (det C)² det G` over a commutative ring,
for a finite index type. This is the identity that makes the determinant
invariant up to the square of the basis determinant; the p-adic unit and
valuation statements about `det C` for the three bases of the manuscript are a
separate obligation (`OBL-bases`). -/
theorem det_congruence {R : Type*} [CommRing R] {n : Type*} [Fintype n] [DecidableEq n]
    (C G : Matrix n n R) : (Cᵀ * G * C).det = C.det ^ 2 * G.det := by
  rw [Matrix.det_mul, Matrix.det_mul, Matrix.det_transpose, pow_two]
  ring

/-- **Invertible shift.** `det(A + δB) = det A · det(I + δ A⁻¹B)` for an
invertible matrix `A`; the factorization behind the eigenvalue product in §4.2
of the note. -/
theorem det_add_smul_eq_det_mul {R : Type*} [Field R] {n : Type*} [Fintype n]
    [DecidableEq n] (A B : Matrix n n R) (δ : R) (hA : IsUnit A.det) :
    (A + δ • B).det = A.det * (1 + δ • (A⁻¹ * B)).det := by
  have h : A + δ • B = A * (1 + δ • (A⁻¹ * B)) := by
    rw [Matrix.mul_add, Matrix.mul_one, Matrix.mul_smul, ← Matrix.mul_assoc,
      Matrix.mul_nonsing_inv _ hA, Matrix.one_mul]
  rw [h, Matrix.det_mul]

end

end ZetaFive.Correspondences
