module

public import ZetaFive.Lean.Family.Moments
public import ZetaFive.Lean.Common.Arithmetic.Bernoulli

@[expose] public section

/-! # Uniform arithmetic bounds for the polynomial moments

For primes larger than `k-1`, the factorial denominator is a unit. The
von Staudt--Clausen theorem therefore gives a uniform lower bound of -1.
Below the first uncancelled Bernoulli index the ascending factorial cancels
the possible prime denominator. This argument works for all zeta indices.
-/

open ZetaFive.Common.Arithmetic

namespace ZetaFive

variable {p : ℕ} [hp : Fact p.Prime]

theorem moment_valuation (k e : ℕ) (hkp : k - 1 < p) :
    VG p (moment k e) (-1) := by
  unfold moment
  rw [show 2 * e + 2 = 2 * (e + 1) by ring, div_eq_mul_inv]
  have hs : VG p ((-1 : ℚ) ^ e) 0 := by
    simpa using (VG.one (p := p)).neg.pow e
  have hn : VG p (((2 * e + 3).ascFactorial (k - 2) : ℕ) : ℚ) 0 := VG.natCast _
  have hd := VG.inv_factorial (p := p) hkp
  simpa using ((hs.mul (VG_bernoulli_even (e + 1))).mul hn).mul hd

/-- All four requested indices have the same denominator bound at primes `p ≥ 5`. -/
theorem moment_valuation_two_through_five (k e : ℕ)
    (_hk2 : 2 ≤ k) (hk5 : k ≤ 5) (hp5 : 5 ≤ p) :
    VG p (moment k e) (-1) :=
  moment_valuation k e (by omega)

/-- Integrality below the first uncancelled von Staudt--Clausen denominator. -/
theorem moment_integral_of_index_lt (k e : ℕ) (hk2 : 2 ≤ k) (hkp : k - 1 < p)
    (he : 2 * e + 2 < (k - 1) * (p - 1)) : VG p (moment k e) 0 := by
  have hs : VG p ((-1 : ℚ) ^ e) 0 := by
    simpa using (VG.one (p := p)).neg.pow e
  have hd := VG.inv_factorial (p := p) hkp
  by_cases hdiv : (p - 1) ∣ 2 * (e + 1)
  · obtain ⟨t, ht⟩ := hdiv
    have hm : 2 * e + 2 = t * (p - 1) := by nlinarith [ht]
    have ht1 : 1 ≤ t := by
      by_contra h
      have : t = 0 := by omega
      simp [this] at hm
    have htk : t ≤ k - 2 := by
      have hlt : t < k - 1 := by
        by_contra h
        have hmul := Nat.mul_le_mul_right (p - 1) (show k - 1 ≤ t by omega)
        omega
      omega
    have hnum : p ∣ (2 * e + 3).ascFactorial (k - 2) := by
      simpa [show 2 * e + 2 + 1 = 2 * e + 3 by omega] using
        (prime_dvd_ascFactorial_of_multiple (p := p) hm ht1 htk)
    have hn := VG.natCast_one_of_dvd hnum
    have hb : VG p (bernoulli (2 * e + 2)) (-1) := by
      simpa [Nat.mul_add] using VG_bernoulli_even (p := p) (e + 1)
    unfold moment
    rw [div_eq_mul_inv]
    simpa using ((hs.mul hb).mul hn).mul hd
  · have hb : VG p (bernoulli (2 * e + 2)) 0 := by
      simpa [Nat.mul_add] using VG_bernoulli_even_int (p := p) (e + 1) hdiv
    have hn : VG p (((2 * e + 3).ascFactorial (k - 2) : ℕ) : ℚ) 0 := VG.natCast _
    unfold moment
    rw [div_eq_mul_inv]
    simpa using ((hs.mul hb).mul hn).mul hd

theorem moment_integral_two_through_five (k e : ℕ)
    (hk2 : 2 ≤ k) (hk5 : k ≤ 5) (hp5 : 5 ≤ p)
    (he : 2 * e + 2 < (k - 1) * (p - 1)) : VG p (moment k e) 0 :=
  moment_integral_of_index_lt k e hk2 (by omega) he

end ZetaFive
