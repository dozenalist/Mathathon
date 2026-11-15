/-
Copyright (c) 2026 Mathathon contributors. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.

# The reflection axiom of `zeta5_unified_framework.tex` §2.1 (eq:reflection)

VALIDATED (toolchain): compiles under the repository pin, Lean/Mathlib v4.35.0,
via `lake build ZetaFive`. Originally authored as a prototype on this VM's Lean
4.33.1; that history is superseded and all current validation is on v4.35.0.
This is still a statement about the `XRep` representation, not about `RatFunc`.

Source statements:

* `eq:reflection`, `τ_X(g(-1-x)) = -τ_X(g(x))` (`Proposition prop:axioms`), and
* the remark in its proof that "the polynomial reflection identity also follows
  from `e^{-u} τ(e^{-ux}) = -τ(e^{ux})`".

The formal content, in the frozen language of `Basic.lean`:

* `L` is *invariant* under the reflection `x ↦ -1-x` (`L_reflect`),
  equivalently the classical Bernoulli recursion `Σ_{k<n} C(n,k)B_k = 0` (for
  `n ≠ 1`) of Mathlib's `_root_.sum_bernoulli`;
* hence `τ = L(∂³·)/24` is *anti*-invariant (`τ_reflect`);
* on `Transport.lean`'s pole data `XRep` the reflection `r ↦ -1-r` of the pole
  index keeps the harmonic index (`d (-1-r) = d r`) and negates the pole
  coefficient, so `τ_X` is anti-invariant there too (`tauX_reflect`).
-/
import Mathlib
import ZetaFive.Lean.Correspondences.Basic
import ZetaFive.Lean.Correspondences.Transport

namespace ZetaFive.Correspondences.M3

noncomputable section

open scoped BigOperators
open Polynomial

/-! ## Additivity of the frozen functional `L` over finite sums -/

lemma natCast_polyX (c : ℕ) : ((c : ℕ) : PolyX) = C ((c : ℕ) : ℚ) := by
  simp

/-- `L` is additive over finite sums (the coefficient pairing is summed over
the support). -/
lemma L_sum {ι : Type*} (s : Finset ι) (f : ι → PolyX) :
    L (∑ i ∈ s, f i) = ∑ i ∈ s, L (f i) := by
  classical
  induction s using Finset.induction with
  | empty => simp
  | insert a s ha ih => rw [Finset.sum_insert ha, Finset.sum_insert ha, L_add, ih]

/-- `L (-P) = -L P`. -/
lemma L_neg (P : PolyX) : L (-P) = -L P := by
  have h : (-P : PolyX) = C (-1) * P := by simp
  rw [h, L_C_mul]
  ring

/-! ## The Bernoulli recursion `L((x+1)^n) = B_n + [n = 1]` -/

/-- `L((x+1)^n) = B_n + [n = 1]`, i.e. Mathlib's `_root_.sum_bernoulli`
`Σ_{k<n} C(n,k)B_k = [n=1]` together with the `k = n` term. -/
lemma L_X_add_one_pow (n : ℕ) :
    L ((X + 1 : PolyX) ^ n) = _root_.bernoulli n + if n = 1 then 1 else 0 := by
  have h : ((X + 1 : PolyX) ^ n)
      = ∑ k ∈ Finset.range (n + 1), C (((n.choose k : ℕ) : ℚ)) * X ^ k := by
    rw [add_pow]
    refine Finset.sum_congr rfl (fun k _ => ?_)
    rw [one_pow, mul_one, natCast_polyX, mul_comm]
  rw [h, L_sum]
  refine Eq.trans (Finset.sum_congr rfl (fun k _ => L_C_mul_X_pow _ k)) ?_
  rw [Finset.sum_range_succ, _root_.sum_bernoulli]
  simp only [Nat.choose_self, Nat.cast_one, one_mul]
  ring

/-- `L((-1-x)^n) = B_n`: the monomial form of the reflection invariance. -/
lemma L_neg_one_sub_X_pow (n : ℕ) :
    L ((-(1 + X) : PolyX) ^ n) = _root_.bernoulli n := by
  have h1 : (-(1 + X) : PolyX) = C (-1) * (X + 1) := by
    rw [C_neg, C_1]
    ring
  have h2 : (-(1 + X) : PolyX) ^ n = C ((-1 : ℚ) ^ n) * (X + 1) ^ n := by
    rw [h1, mul_pow, ← C_pow]
  rw [h2, L_C_mul, L_X_add_one_pow]
  by_cases hn : n = 1
  · subst hn
    norm_num [_root_.bernoulli_one]
  · rcases Nat.even_or_odd n with he | ho
    · rw [he.neg_one_pow, one_mul, if_neg hn, add_zero]
    · have hgt : 1 < n := by
        rcases ho with ⟨k, hk⟩
        omega
      rw [ho.neg_one_pow, if_neg hn, _root_.bernoulli_eq_zero_of_odd ho hgt]
      ring

/-! ## The reflection `reflect P = P(-1-X)` on `ℚ[x]` -/

/-- The reflection `P ↦ P(-1-x)` of `Proposition prop:axioms` (eq:reflection). -/
def reflect (P : PolyX) : PolyX := P.comp (-(1 + X))

lemma reflect_add (P Q : PolyX) : reflect (P + Q) = reflect P + reflect Q := by
  simp [reflect]

lemma reflect_neg (P : PolyX) : reflect (-P) = -reflect P := by
  simp [reflect]

lemma reflect_monomial (n : ℕ) (a : ℚ) :
    reflect (monomial n a) = C a * (-(1 + X) : PolyX) ^ n := by
  rw [← C_mul_X_pow_eq_monomial, reflect, mul_comp, C_comp, X_pow_comp]

/-- **eq:reflection, polynomial part.** `L` is invariant under `x ↦ -1-x`. -/
theorem L_reflect (P : PolyX) : L (reflect P) = L P := by
  induction P using Polynomial.induction_on' with
  | add p q hp hq => rw [reflect_add, L_add, hp, hq, L_add]
  | monomial n a => rw [reflect_monomial, L_C_mul, L_neg_one_sub_X_pow, L_monomial]

/-- `L` vanishes on polynomials antisymmetric under the reflection. -/
theorem L_eq_zero_of_reflect_eq_neg {P : PolyX} (h : reflect P = -P) : L P = 0 := by
  have h2 : L P = L (reflect P) := (L_reflect P).symm
  rw [h, L_neg] at h2
  linarith

lemma derivative_reflect (P : PolyX) : derivative (reflect P) = -reflect (derivative P) := by
  simp only [reflect]
  rw [derivative_comp]
  have hr : derivative (-(1 + X) : PolyX) = -1 := by
    rw [derivative_neg, derivative_add, derivative_X, derivative_one]
    ring
  rw [hr]
  ring

lemma derivative3_reflect (P : PolyX) :
    derivative (derivative (derivative (reflect P)))
      = -reflect (derivative (derivative (derivative P))) := by
  simp only [derivative_reflect, derivative_neg, neg_neg]

/-- **eq:reflection, `τ` form.** `τ(P(-1-x)) = -τ(P)`. -/
theorem τ_reflect (P : PolyX) : τ (reflect P) = -τ P := by
  have h := derivative3_reflect P
  simp only [τ, h, L_neg, L_reflect]
  ring

/-! ## The reflection at simple integer poles (`Transport.lean`'s `XRep`) -/

/-- The reflection sends the pole at `r` to the pole at `-1-r`.
(Statement duplicated as `d_reflect` in `Candm4.lean`; both are kept because each
candidate file is preserved verbatim as delivered by its swarm member. The
statements are identical, so a future integration should keep one and delete the
other. `M4.H5Z_reflect` is the only consumer.) -/
lemma d_neg_one_sub (r : ℤ) : d (-1 - r) = d r := by
  simp only [d]
  split_ifs with h1 h2
  · exfalso
    omega
  · congr 1
    omega
  · congr 1
    omega
  · congr 1
    omega

/-- The pole contribution of a finite pole list. -/
def poleSum (u : ℚ) (l : List (ℤ × ℚ)) : ℚ :=
  (l.map (fun rc => rc.2 * (H5 (d rc.1) - u))).sum

lemma list_sum_neg_map (l : List ℚ) : (l.map Neg.neg).sum = -l.sum := by
  induction l with
  | nil => simp
  | cons a t ih => simp [ih]; ring

lemma poleSum_reflect (u : ℚ) (l : List (ℤ × ℚ)) :
    poleSum u (l.map (fun rc => (-1 - rc.1, -rc.2))) = -poleSum u l := by
  have key : ∀ l : List (ℤ × ℚ),
      (l.map (fun rc => (-1 - rc.1, -rc.2))).map
          (fun rc => rc.2 * (H5 (d rc.1) - u))
        = (l.map (fun rc => rc.2 * (H5 (d rc.1) - u))).map Neg.neg := by
    intro l
    induction l with
    | nil => rfl
    | cons a t ih =>
        simp only [List.map_cons, List.cons.injEq]
        refine ⟨?_, ih⟩
        simp only [d_neg_one_sub]
        ring
  simp only [poleSum, key, list_sum_neg_map]

/-- Reflection of pole data: the polynomial part is reflected, the poles move
`r ↦ -1-r` and their coefficients change sign. -/
def reflectRep (R : XRep) : XRep :=
  ⟨reflect R.poly, R.poles.map (fun rc => (-1 - rc.1, -rc.2))⟩

/-- **eq:reflection on the pole domain.** `τ_X(g(-1-x)) = -τ_X(g(x))`. -/
theorem tauX_reflect (u : ℚ) (R : XRep) :
    XRep.tauX u (reflectRep R) = -XRep.tauX u R := by
  have hp := poleSum_reflect u R.poles
  simp only [XRep.tauX, reflectRep, poleSum, List.map_map] at hp ⊢
  rw [τ_reflect, hp]
  ring

end

end ZetaFive.Correspondences.M3
