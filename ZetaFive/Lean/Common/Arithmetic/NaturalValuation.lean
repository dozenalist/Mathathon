module

/-
Adapted from Apery/Arith/PoleVal.lean in mo271/Zeta5,
commit 7fe736760f4b96bfdb4334b68e3b3124ecbe10b0, under Apache 2.0.
See ZetaFive/Lean/LICENSES/mo271-Zeta5.txt.
-/
public import ZetaFive.Lean.Common.Arithmetic.Val

@[expose] public section

/-! # Valuation bounds for natural denominators

These bounds concern only natural numbers and primes; they are independent of
the zeta index and of the Hankel family parameters.
-/

namespace ZetaFive.Common.Arithmetic

variable {p : ℕ} [hp : Fact p.Prime]

lemma VG_inv_nat_le {u : ℕ} (hu : u ≠ 0) {e : ℕ} (he : padicValNat p u ≤ e) :
    VG p ((u : ℚ)⁻¹) (-(e : ℚ)) := by
  refine VG.inv (by exact_mod_cast hu) ?_
  rw [padicValRat.of_nat]
  exact_mod_cast he

lemma padicValNat_lt_p {u : ℕ} (hu : 1 ≤ u) (hup : u < p) : padicValNat p u = 0 :=
  padicValNat.eq_zero_of_not_dvd fun h =>
    absurd (Nat.le_of_dvd (by omega) h) (by omega)

lemma padicValNat_lt_sq {u : ℕ} (hu : 1 ≤ u) (hup : u < p ^ 2) :
    padicValNat p u ≤ 1 := by
  by_contra h
  rw [not_le] at h
  have : p ^ 2 ∣ u := (padicValNat_dvd_iff_le (by omega)).mpr h
  exact absurd (Nat.le_of_dvd (by omega) this) (by omega)

lemma VG_inv_nat_lt {u : ℕ} (hu : 1 ≤ u) (hup : u < p) :
    VG p ((u : ℚ)⁻¹) 0 := by
  have h := VG_inv_nat_le (p := p) (by omega : u ≠ 0) (e := 0)
    (by rw [padicValNat_lt_p hu hup])
  simpa using h

lemma VG_inv_2j (hp3 : 3 ≤ p) {j e : ℕ} (hj : 1 ≤ j) (he : padicValNat p j ≤ e) :
    VG p (1 / (2 * (j : ℚ))) (-(e : ℚ)) := by
  rw [one_div, show (2 * (j : ℚ)) = ((2 * j : ℕ) : ℚ) by push_cast; ring]
  refine VG_inv_nat_le (by omega) ?_
  have := Fact.mk Nat.prime_two
  rw [padicValNat.mul (by norm_num) (by omega),
    padicValNat_primes (p := p) (q := 2) (by omega)]
  omega

end ZetaFive.Common.Arithmetic
