module

/-
Copyright (c) 2026 the mo271/Zeta5 contributors. All rights reserved.
Released under Apache 2.0 license as described in ZetaFive/Lean/LICENSES/mo271-Zeta5.txt.
Adapted from mo271/Zeta5, commit 7fe736760f4b96bfdb4334b68e3b3124ecbe10b0.
-/
public import ZetaFive.Lean.Common.Arithmetic.Val
public import Mathlib.NumberTheory.Bernoulli
public import Mathlib.Data.Nat.Factorial.BigOperators

@[expose] public section

/-! # The common Bernoulli denominator bounds

The von Staudt--Clausen theorem gives valuation at least -1 at every prime,
and valuation at least 0 when that prime is absent from the denominator sum.
-/

open Finset

namespace ZetaFive.Common.Arithmetic

variable {p : ℕ} [hp : Fact p.Prime]
lemma VG_bernoulli_even (k : ℕ) : VG p (_root_.bernoulli (2 * k)) (-1) := by
  obtain ⟨z, hz⟩ := Bernoulli.vonStaudt_clausen k
  have e : _root_.bernoulli (2 * k) = (z : ℚ) - ∑ q ∈ range (2 * k + 2) with q.Prime ∧ (q - 1) ∣ 2 * k,
      (1 : ℚ) / q := by rw [hz]; ring
  rw [e]
  refine ((VG.intCast (p := p) z).mono (by norm_num)).sub (VG.sum _ fun q hq => ?_)
  rw [Finset.mem_filter] at hq
  have hq0 : (q : ℚ) ≠ 0 := by exact_mod_cast hq.2.1.ne_zero
  rw [one_div]
  refine VG.inv hq0 ?_
  rw [padicValRat.of_nat]
  have : padicValNat p q ≤ 1 := by
    by_cases hpq : p = q
    · subst hpq; rw [padicValNat_self]
    · have := Fact.mk hq.2.1
      rw [padicValNat_primes hpq]; omega
  exact_mod_cast this

lemma VG_bernoulli_even_int (k : ℕ) (hk : ¬ (p - 1) ∣ 2 * k) :
    VG p (_root_.bernoulli (2 * k)) 0 := by
  obtain ⟨z, hz⟩ := Bernoulli.vonStaudt_clausen k
  have e : _root_.bernoulli (2 * k) = (z : ℚ) - ∑ q ∈ range (2 * k + 2) with q.Prime ∧ (q - 1) ∣ 2 * k,
      (1 : ℚ) / q := by rw [hz]; ring
  rw [e]
  refine (VG.intCast (p := p) z).sub (VG.sum _ fun q hq => ?_)
  rw [Finset.mem_filter] at hq
  have hq0 : (q : ℚ) ≠ 0 := by exact_mod_cast hq.2.1.ne_zero
  have hpq : p ≠ q := fun h => hk (h ▸ hq.2.2)
  rw [one_div]
  refine (VG.inv (r := 0) hq0 ?_).mono (by norm_num)
  have := Fact.mk hq.2.1
  rw [padicValRat.of_nat, padicValNat_primes hpq]; simp


/-- If `m = t(p-1)` with `1 ≤ t ≤ r`, the ascending product
`(m+1)...(m+r)` contains the multiple `tp` and cancels one Bernoulli denominator. -/
lemma prime_dvd_ascFactorial_of_multiple {m r t : ℕ}
    (hm : m = t * (p - 1)) (ht : 1 ≤ t) (htr : t ≤ r) :
    p ∣ (m + 1).ascFactorial r := by
  rw [hp.out.dvd_ascFactorial_iff]
  refine ⟨t - 1, by omega, ?_⟩
  have heq : m + 1 + (t - 1) = t * p := by
    calc
      m + 1 + (t - 1) = m + t := by omega
      _ = t * (p - 1) + t := by rw [hm]
      _ = t * ((p - 1) + 1) := by ring
      _ = t * p := by rw [Nat.sub_add_cancel hp.out.pos]
  rw [heq]
  exact dvd_mul_left p t

end ZetaFive.Common.Arithmetic

