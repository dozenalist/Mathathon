/-
Copyright (c) 2026 Mathathon contributors. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
-/
import Mathlib
import ZetaFive.Lean.Correspondences.Basic
import ZetaFive.Lean.Correspondences.Transport

/-!
# Candidate module (member m4): the `H5` partial-sum calculus

Source: `zeta5_unified_framework.tex` (reviewed revision, 14 Nov 2026), §2.1:
"Bernoulli moments are the polynomial part of Euler summation, fifth harmonic
sums are its increments at simple poles, and `X` is the one free
pole-boundary value."

`Basic.lean` freezes `H5 j = ∑ i ∈ range j, ((i+1 : ℚ))⁻¹ ^ 5` together with
`H5_zero`, `H5_succ` and `H5_increment`. This module develops the calculus of
the *sequence* `H5` itself, i.e. the "fifth harmonic sums" half of the
framework (the Bernoulli/coefficient half is a different direction):

* elementary values (`H5 1 = 1`, `H5 2 = 33/32`), positivity, monotonicity and
  strict monotonicity of `j ↦ H5 j`;
* a telescoping bound: `H5 (j+1) ≤ 2 - (j+1)⁻¹`, hence `H5 j < 2` for all `j`;
* the tail bound `H5 (n+k) - H5 n ≤ n⁻¹ - (n+k)⁻¹` and the resulting explicit
  `ε`–`N` Cauchy statement for `H5` in `ℚ`;
* the **recursion characterisation** of `H5`: any `a : ℕ → ℚ` with `a 0 = c`
  and `a (r-1) - a r = -r⁻⁵` (`r ≥ 1`) satisfies `a j = c + H5 j`, and the
  corresponding two-sided statement on `ℤ`, where the index `d r` of
  `Transport.lean` is the reflection-symmetric extension. This is exactly the
  step "starting with `a_0 = -X` gives `a_r = H^{(5)}_r - X`" in the proof of
  the §2.1 pole formula (there `c = -X`, so `a_r = c + H5_r`).

Everything is in `ℚ`; no analysis, no new axioms.
-/

namespace ZetaFive.Correspondences.M4

open scoped BigOperators

noncomputable section

/-! ## 1. Elementary values, positivity, monotonicity -/

lemma H5_one : H5 1 = 1 := by
  norm_num [H5]

lemma H5_two : H5 2 = 33 / 32 := by
  norm_num [H5]

lemma H5_nonneg (j : ℕ) : 0 ≤ H5 j :=
  Finset.sum_nonneg fun i _ => by positivity

/-- The increments are strictly positive, so `H5` is strictly increasing. -/
lemma H5_lt_succ (j : ℕ) : H5 j < H5 (j + 1) := by
  have h : (0 : ℚ) < (((j : ℕ) + 1 : ℚ))⁻¹ ^ 5 := by positivity
  rw [H5_succ]
  linarith

lemma H5_le_succ (j : ℕ) : H5 j ≤ H5 (j + 1) := le_of_lt (H5_lt_succ j)

lemma H5_mono : Monotone H5 := monotone_nat_of_le_succ H5_le_succ

lemma H5_strictMono : StrictMono H5 := strictMono_nat_of_lt_succ H5_lt_succ

lemma H5_pos {j : ℕ} (hj : 1 ≤ j) : 0 < H5 j := by
  obtain ⟨k, rfl⟩ : ∃ k, j = k + 1 := ⟨j - 1, by omega⟩
  exact lt_of_le_of_lt (H5_nonneg k) (H5_lt_succ k)

lemma H5_ge_one {j : ℕ} (hj : 1 ≤ j) : 1 ≤ H5 j := by
  calc (1 : ℚ) = H5 1 := H5_one.symm
    _ ≤ H5 j := H5_mono hj

/-! ## 2. A telescoping bound, hence `H5 j < 2` -/

/-- For `a ≥ 2`: `a⁻¹ ^ 5 ≤ (a-1)⁻¹ - a⁻¹`, whose right-hand side telescopes. -/
lemma inv_pow_five_le_sub_inv {a : ℚ} (ha : 2 ≤ a) :
    a⁻¹ ^ 5 ≤ (a - 1)⁻¹ - a⁻¹ := by
  have ha0 : (0 : ℚ) < a := by linarith
  have ham0 : (0 : ℚ) < a - 1 := by linarith
  have ha1 : (1 : ℚ) ≤ a := by linarith
  have hsq : a ^ 2 ≤ a ^ 5 := pow_le_pow_right₀ ha1 (by norm_num)
  have hmul : (a - 1) * a ≤ a ^ 5 := by
    have h1 : (a - 1) * a ≤ a * a :=
      mul_le_mul_of_nonneg_right (by linarith) (le_of_lt ha0)
    nlinarith [h1, hsq]
  have key : (a ^ 5)⁻¹ ≤ ((a - 1) * a)⁻¹ :=
    (inv_le_inv₀ (pow_pos ha0 5) (mul_pos ham0 ha0)).mpr hmul
  have hdiff : ((a - 1) * a)⁻¹ = (a - 1)⁻¹ - a⁻¹ := by
    have h1 : a - 1 ≠ 0 := ne_of_gt ham0
    have h2 : a ≠ 0 := ne_of_gt ha0
    rw [mul_inv]
    field_simp
    ring
  rw [hdiff] at key
  rw [inv_pow]
  exact key

/-- The telescoping form of the same estimate, indexed so that the summands are
`((i+1)+1)⁻¹ ^ 5`; this is the shape produced by `Finset.sum_range_succ'`. -/
lemma inv_five_le_telescope (i : ℕ) :
    ((i : ℚ) + 1 + 1)⁻¹ ^ 5 ≤ ((i : ℚ) + 1)⁻¹ - ((i : ℚ) + 1 + 1)⁻¹ := by
  have hi : (0 : ℚ) ≤ (i : ℚ) := Nat.cast_nonneg i
  have h := inv_pow_five_le_sub_inv (a := (i : ℚ) + 1 + 1) (by linarith)
  have h2 : (i : ℚ) + 1 + 1 - 1 = (i : ℚ) + 1 := by ring
  rw [h2] at h
  exact h

lemma H5_succ_le_two_sub_inv (j : ℕ) : H5 (j + 1) ≤ 2 - (((j : ℕ) + 1 : ℚ))⁻¹ := by
  have hstep : (∑ i ∈ Finset.range j, ((i : ℚ) + 1 + 1)⁻¹ ^ 5)
      ≤ ∑ i ∈ Finset.range j, (((i : ℚ) + 1)⁻¹ - ((i : ℚ) + 1 + 1)⁻¹) :=
    Finset.sum_le_sum fun i _ => inv_five_le_telescope i
  have htel : (∑ i ∈ Finset.range j, (((i : ℚ) + 1)⁻¹ - ((i : ℚ) + 1 + 1)⁻¹))
      = 1 - ((j : ℚ) + 1)⁻¹ := by
    have := Finset.sum_range_sub' (fun i : ℕ => ((i : ℚ) + 1)⁻¹) j
    simpa only [Nat.cast_add, Nat.cast_one, Nat.cast_zero, zero_add, inv_one] using this
  have hsplit : H5 (j + 1) = (∑ i ∈ Finset.range j, ((i : ℚ) + 1 + 1)⁻¹ ^ 5) + 1 := by
    rw [H5, Finset.sum_range_succ']
    simp only [Nat.cast_add, Nat.cast_one, Nat.cast_zero, zero_add, inv_one, one_pow]
  have hcast : (((j : ℕ) + 1 : ℚ)) = (j : ℚ) + 1 := by ring
  rw [hsplit, hcast]
  linarith

lemma H5_lt_two (j : ℕ) : H5 j < 2 := by
  rcases j with _ | k
  · rw [H5_zero]; norm_num
  · have h := H5_succ_le_two_sub_inv k
    have hpos : (0 : ℚ) < (((k : ℕ) + 1 : ℚ))⁻¹ := by
      rw [inv_pos]
      have : (0 : ℚ) ≤ (k : ℚ) := Nat.cast_nonneg k
      linarith
    linarith

lemma H5_le_two (j : ℕ) : H5 j ≤ 2 := le_of_lt (H5_lt_two j)

/-! ## 3. The tail bound and the Cauchy property in `ℚ` -/

/-- Splitting identity: `H5 (n+k) = H5 n + ∑_{i<k} (n+i+1)⁻⁵`. -/
lemma H5_add (n k : ℕ) :
    H5 (n + k) = H5 n + ∑ i ∈ Finset.range k, (((n + i + 1 : ℕ)) : ℚ)⁻¹ ^ 5 := by
  induction k with
  | zero => simp
  | succ k ih =>
      have hs : n + (k + 1) = n + k + 1 := by ring
      rw [hs, H5_succ, ih, Finset.sum_range_succ]
      push_cast
      ring

/-- Tail estimate: the `k`-term tail after `n ≥ 1` is at most `n⁻¹ - (n+k)⁻¹`. -/
lemma H5_tail_le (n k : ℕ) (hn : 1 ≤ n) :
    H5 (n + k) - H5 n ≤ ((n : ℚ))⁻¹ - (((n + k : ℕ)) : ℚ)⁻¹ := by
  have hstep : (∑ i ∈ Finset.range k, (((n + i + 1 : ℕ)) : ℚ)⁻¹ ^ 5)
      ≤ ∑ i ∈ Finset.range k, ((((n + i : ℕ)) : ℚ)⁻¹ - (((n + i + 1 : ℕ)) : ℚ)⁻¹) := by
    apply Finset.sum_le_sum
    intro i _
    have h2 : (2 : ℚ) ≤ (((n + i + 1 : ℕ)) : ℚ) := by
      have h2' : (2 : ℕ) ≤ n + i + 1 := by omega
      exact_mod_cast h2'
    have h := inv_pow_five_le_sub_inv h2
    have hsub : (((n + i + 1 : ℕ)) : ℚ) - 1 = (((n + i : ℕ)) : ℚ) := by push_cast; ring
    rw [hsub] at h
    exact h
  have htel : (∑ i ∈ Finset.range k, ((((n + i : ℕ)) : ℚ)⁻¹ - (((n + i + 1 : ℕ)) : ℚ)⁻¹))
      = ((n : ℚ))⁻¹ - (((n + k : ℕ)) : ℚ)⁻¹ := by
    have := Finset.sum_range_sub' (fun i : ℕ => (((n + i : ℕ)) : ℚ)⁻¹) k
    simpa only [Nat.add_zero, Nat.add_assoc] using this
  rw [H5_add]
  linarith

lemma H5_tail_le_inv (n k : ℕ) (hn : 1 ≤ n) :
    H5 (n + k) - H5 n ≤ ((n : ℚ))⁻¹ := by
  have h := H5_tail_le n k hn
  have hnn : (0 : ℚ) ≤ (((n + k : ℕ)) : ℚ)⁻¹ := by positivity
  linarith

/-- `H5` is Cauchy in `ℚ`, with an explicit `ε`–`N` modulus (the quantitative
content of "the free pole-boundary value `X = ζ(5)`"). -/
theorem H5_cauchy (ε : ℚ) (hε : 0 < ε) :
    ∃ N : ℕ, ∀ n ≥ N, ∀ k : ℕ, |H5 (n + k) - H5 n| ≤ ε := by
  obtain ⟨N₀, hN₀⟩ := exists_nat_gt ε⁻¹
  refine ⟨N₀ + 1, ?_⟩
  intro n hn k
  have hn1 : 1 ≤ n := by omega
  have hNn : ((N₀ : ℕ) : ℚ) ≤ (n : ℚ) := by
    have : N₀ ≤ n := by omega
    exact_mod_cast this
  have hεinv : ε⁻¹ < (n : ℚ) := by linarith
  have hprod : 1 < ε * (n : ℚ) := by
    have h := mul_lt_mul_of_pos_left hεinv hε
    rw [mul_inv_cancel₀ (ne_of_gt hε)] at h
    exact h
  have hinv : ((n : ℚ))⁻¹ ≤ ε := by
    have hnpos : (0 : ℚ) < (n : ℚ) := by
      have h1 : (1 : ℚ) ≤ (n : ℚ) := by exact_mod_cast hn1
      linarith
    have hnne : (n : ℚ) ≠ 0 := ne_of_gt hnpos
    have hone : (1 : ℚ) ≤ ε * (n : ℚ) := le_of_lt hprod
    calc ((n : ℚ))⁻¹ = 1 * ((n : ℚ))⁻¹ := by ring
      _ ≤ (ε * (n : ℚ)) * ((n : ℚ))⁻¹ :=
          mul_le_mul_of_nonneg_right hone (le_of_lt (inv_pos.mpr hnpos))
      _ = ε := by field_simp
  have hnonneg : (0 : ℚ) ≤ H5 (n + k) - H5 n := by
    have := H5_mono (Nat.le_add_right n k)
    linarith
  rw [abs_of_nonneg hnonneg]
  have h := H5_tail_le_inv n k hn1
  linarith

/-! ## 4. `H5` as the solution of the pole-difference recursion -/

/-- **Recursion characterisation on `ℕ`.** If `a 0 = c` and
`a (r-1) - a r = -r⁻⁵` for `r ≥ 1`, then `a j = c + H5 j`: the pole data
`a_r = τ_X(1/(x-r))` is determined by the harmonic increments and one boundary
value. -/
theorem eq_sub_H5_of_nat (a : ℕ → ℚ) (c : ℚ) (h0 : a 0 = c)
    (hrec : ∀ r : ℕ, 1 ≤ r → a (r - 1) - a r = - ((r : ℚ))⁻¹ ^ 5) :
    ∀ j : ℕ, a j = c + H5 j := by
  intro j
  induction j with
  | zero => rw [h0, H5_zero, add_zero]
  | succ j ih =>
      have h := hrec (j + 1) (by omega)
      have hj : j + 1 - 1 = j := by omega
      rw [hj] at h
      push_cast at h
      rw [H5_succ]
      linarith

/-- The index `d` of `Transport.lean` is symmetric under `r ↦ -1-r`. -/
lemma d_reflect (r : ℤ) : d (-1 - r) = d r := by
  unfold d
  by_cases h : (0 : ℤ) ≤ r
  · have h' : ¬ (0 : ℤ) ≤ -1 - r := by omega
    rw [if_neg h', if_pos h]
    have h2 : -(-1 - r) - 1 = r := by ring
    rw [h2]
  · have h' : ¬ (0 : ℤ) ≤ r := by omega
    have h'' : (0 : ℤ) ≤ -1 - r := by omega
    rw [if_pos h'', if_neg h']
    have h2 : -1 - r = -r - 1 := by ring
    rw [h2]

/-- The harmonic index `H5 ∘ d` as a function on `ℤ`. -/
def H5Z (r : ℤ) : ℚ := H5 (d r)

@[simp] lemma H5Z_zero : H5Z 0 = 0 := by simp [H5Z, d]

@[simp] lemma H5Z_natCast (j : ℕ) : H5Z (j : ℤ) = H5 j := by simp [H5Z]

lemma H5Z_reflect (r : ℤ) : H5Z (-1 - r) = H5Z r := by simp [H5Z, d_reflect]

/-- The positive-index difference law for `H5Z`. -/
lemma H5Z_diff_pos (j : ℕ) :
    H5Z (((j : ℤ) + 1) - 1) - H5Z ((j : ℤ) + 1) = - ((((j : ℤ) + 1) : ℤ) : ℚ)⁻¹ ^ 5 := by
  have h1 : ((j : ℤ) + 1 - 1) = (j : ℤ) := by ring
  rw [h1, H5Z_natCast]
  have h2 : ((j : ℤ) + 1) = ((j + 1 : ℕ) : ℤ) := by push_cast; ring
  rw [h2, H5Z_natCast, H5_succ]
  push_cast
  ring

/-- **The difference law on `ℤ`.** For `r ≠ 0`,
`H5Z (r-1) - H5Z r = -r⁻⁵`. -/
lemma H5Z_diff {r : ℤ} (hr : r ≠ 0) :
    H5Z (r - 1) - H5Z r = - ((r : ℚ))⁻¹ ^ 5 := by
  rcases lt_or_gt_of_ne hr with h | h
  · obtain ⟨j, hj⟩ : ∃ j : ℕ, -r = (j : ℤ) + 1 := by
      refine ⟨(-r - 1).toNat, ?_⟩
      have h2 : (0 : ℤ) ≤ -r - 1 := by omega
      have h3 := Int.toNat_of_nonneg h2
      omega
    have hr' : r = -((j : ℤ) + 1) := by omega
    rw [hr']
    have e1 : H5Z (-((j : ℤ) + 1) - 1) = H5 ((j + 1 : ℕ)) := by
      rw [← H5Z_reflect (-((j : ℤ) + 1) - 1)]
      have hy : -1 - (-((j : ℤ) + 1) - 1) = ((j + 1 : ℕ) : ℤ) := by omega
      rw [hy, H5Z_natCast]
    have e2 : H5Z (-((j : ℤ) + 1)) = H5 j := by
      rw [← H5Z_reflect (-((j : ℤ) + 1))]
      have hy : -1 - (-((j : ℤ) + 1)) = (j : ℤ) := by ring
      rw [hy, H5Z_natCast]
    rw [e1, e2, H5_succ]
    push_cast
    rw [inv_neg, Odd.neg_pow (by norm_num : Odd 5)]
    ring
  · obtain ⟨j, rfl⟩ : ∃ j : ℕ, r = (j : ℤ) + 1 := by
      refine ⟨(r - 1).toNat, ?_⟩
      have h2 : (0 : ℤ) ≤ r - 1 := by omega
      have h3 := Int.toNat_of_nonneg h2
      omega
    exact H5Z_diff_pos j

/-- **Recursion characterisation on `ℤ`.** The pole values `a_r = τ_X(1/(x-r))`
satisfy the difference law `a_{r-1} - a_r = -r⁻⁵` for `r ≠ 0` and the reflection
law `a_{-1-r} = a_r`; together with `a_0 = c` this forces `a_r = c + H5Z r`,
where `H5Z r = H5^{(5)}_{d(r)}` and `d` is the index of `Transport.lean`. -/
theorem eq_sub_H5Z (a : ℤ → ℚ) (c : ℚ) (h0 : a 0 = c)
    (hrec : ∀ r : ℤ, 1 ≤ r → a (r - 1) - a r = - ((r : ℚ))⁻¹ ^ 5)
    (hrefl : ∀ r : ℤ, a (-1 - r) = a r) :
    ∀ r : ℤ, a r = c + H5Z r := by
  have hnat : ∀ j : ℕ, a (j : ℤ) = c + H5 j := by
    refine eq_sub_H5_of_nat (fun j : ℕ => a (j : ℤ)) c ?_ ?_
    · simpa using h0
    · intro r hr
      have h1 : (1 : ℤ) ≤ (r : ℤ) := by exact_mod_cast hr
      have h := hrec (r : ℤ) h1
      have hc : ((r : ℤ) - 1) = ((r - 1 : ℕ) : ℤ) := by omega
      have hc2 : (((r : ℤ)) : ℚ) = ((r : ℕ) : ℚ) := by push_cast; ring
      rw [hc, hc2] at h
      exact h
  intro r
  by_cases h : (0 : ℤ) ≤ r
  · have hr : ((r.toNat : ℕ) : ℤ) = r := Int.toNat_of_nonneg h
    rw [← hr, hnat r.toNat, H5Z_natCast]
  · obtain ⟨m, hm⟩ : ∃ m : ℕ, -1 - r = (m : ℤ) :=
      ⟨(-1 - r).toNat, (Int.toNat_of_nonneg (by omega)).symm⟩
    have hr : r = -1 - (m : ℤ) := by omega
    rw [hr]
    have h1 : a (-1 - (m : ℤ)) = a (m : ℤ) := by
      have := hrefl (m : ℤ)
      simpa using this
    rw [h1, hnat m]
    congr 1
    rw [H5Z_reflect (m : ℤ), H5Z_natCast]

/-- The function `r ↦ c + H5^{(5)}_{d(r)}` satisfies the difference law, so the
hypotheses of `eq_sub_H5Z` are consistent. -/
lemma H5Z_satisfies_diff (c : ℚ) {r : ℤ} (hr : r ≠ 0) :
    (c + H5Z (r - 1)) - (c + H5Z r) = - ((r : ℚ))⁻¹ ^ 5 := by
  have h := H5Z_diff hr
  linarith

lemma H5Z_satisfies_refl (c : ℚ) (r : ℤ) : c + H5Z (-1 - r) = c + H5Z r := by
  rw [H5Z_reflect]

/-- **Uniqueness of the pole values**, in bundled form: `a` is exactly
`r ↦ c + H5^{(5)}_{d(r)}`. -/
theorem pole_values_unique (a : ℤ → ℚ) (c : ℚ) (h0 : a 0 = c)
    (hrec : ∀ r : ℤ, 1 ≤ r → a (r - 1) - a r = - ((r : ℚ))⁻¹ ^ 5)
    (hrefl : ∀ r : ℤ, a (-1 - r) = a r) :
    a = fun r => c + H5Z r := by
  funext r
  exact eq_sub_H5Z a c h0 hrec hrefl r

end

end ZetaFive.Correspondences.M4
