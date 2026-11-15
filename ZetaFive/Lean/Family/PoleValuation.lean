module

/-
Adapted from Apery/Arith/PoleVal.lean in mo271/Zeta5,
commit 7fe736760f4b96bfdb4334b68e3b3124ecbe10b0, under Apache 2.0.
Generalized from the fifth zeta value to arbitrary integer indices.
See ZetaFive/Lean/LICENSES/mo271-Zeta5.txt.
-/
public import ZetaFive.Lean.Family.Moments
public import ZetaFive.Lean.Common.Arithmetic.NaturalValuation

@[expose] public section

/-! # Uniform valuation bounds for the harmonic sums and affine pole values

The first pole bound is integral below `p`. Below `p²` it loses at most `k`;
at a multiple of `p` the factor `j^(k-1)` recovers all but one power of `p`.
No parity-dependent congruence between the poles `j` and `p-j` is asserted here.
-/

open Polynomial Finset
open ZetaFive.Common.Arithmetic

namespace ZetaFive

variable {p : ℕ} [hp : Fact p.Prime]

theorem harmonic_valuation_lt (k j : ℕ) (hj : j < p) : VG p (harmonic k j) 0 := by
  unfold harmonic
  refine VG.sum _ fun u hu => ?_
  have hu' := Finset.mem_Icc.mp hu
  simpa [one_div, inv_pow] using (VG_inv_nat_lt (p := p) hu'.1 (by omega)).pow k

theorem harmonic_valuation_sq (k j : ℕ) (hj : j < p ^ 2) :
    VG p (harmonic k j) (-(k : ℚ)) := by
  unfold harmonic
  refine VG.sum _ fun u hu => ?_
  have hu' := Finset.mem_Icc.mp hu
  have h := VG_inv_nat_le (p := p) (by omega : u ≠ 0) (e := 1)
    (padicValNat_lt_sq hu'.1 (by omega))
  simpa [one_div, inv_pow] using h.pow k

theorem pole_constant_valuation (k : ℕ) (hk : 2 ≤ k) (hkp : k - 1 < p) :
    VG p (1 / ((k - 1 : ℕ) : ℚ)) 0 := by
  simpa [one_div] using VG_inv_nat_lt (p := p) (by omega : 1 ≤ k - 1) hkp

/-- The affine pole value is integral below the prime. -/
theorem poleValue_valuation_lt (k j : ℕ) (hk : 2 ≤ k)
    (hkp : max 2 (k - 1) < p) (hj : 1 ≤ j) (hjp : j < p) :
    GV p (poleValue k j) 0 := by
  have hp3 : 3 ≤ p := by omega
  have hkp' : k - 1 < p := lt_of_le_of_lt (le_max_right _ _) hkp
  unfold poleValue
  have h1 : GV p (C ((j : ℚ) ^ (k - 1)) * (X - C (harmonic k j))) 0 := by
    have := GV.C_mul (VG.natCast (p := p) (j ^ (k - 1)))
      (GV.X.sub (GV.C (harmonic_valuation_lt k j hjp)))
    simpa using this
  refine (h1.sub (GV.C (pole_constant_valuation k hk hkp'))).add (GV.C ?_)
  have := VG_inv_2j hp3 hj (e := 0) (by rw [padicValNat_lt_p hj hjp])
  simpa using this

/-- Below `p²`, the affine pole value has valuation at least `-k`. -/
theorem poleValue_valuation_sq (k j : ℕ) (hk : 2 ≤ k)
    (hkp : max 2 (k - 1) < p) (hj : 1 ≤ j) (hjp : j < p ^ 2) :
    GV p (poleValue k j) (-(k : ℚ)) := by
  have hp3 : 3 ≤ p := by omega
  have hkp' : k - 1 < p := lt_of_le_of_lt (le_max_right _ _) hkp
  have hk0 : -(k : ℚ) ≤ 0 := neg_nonpos.mpr (Nat.cast_nonneg _)
  have hk1 : -(k : ℚ) ≤ -1 :=
    neg_le_neg (by exact_mod_cast (by omega : 1 ≤ k))
  unfold poleValue
  have h1 : GV p (C ((j : ℚ) ^ (k - 1)) * (X - C (harmonic k j))) (-(k : ℚ)) := by
    have := GV.C_mul (VG.natCast (p := p) (j ^ (k - 1)))
      ((GV.X.mono hk0).sub (GV.C (harmonic_valuation_sq k j hjp)))
    simpa using this
  refine (h1.sub ((GV.C (pole_constant_valuation k hk hkp')).mono hk0)).add (GV.C ?_)
  exact (VG_inv_2j hp3 hj (e := 1) (padicValNat_lt_sq hj hjp)).mono hk1

/-- At a pole `j = p*a`, the factor `j^(k-1)` leaves at most one denominator power. -/
theorem poleValue_valuation_mul (k a : ℕ) (hk : 2 ≤ k)
    (hkp : max 2 (k - 1) < p) (ha : 1 ≤ a) (hap : a < p) :
    GV p (poleValue k (p * a)) (-1) := by
  have hp3 : 3 ≤ p := by omega
  have hkp' : k - 1 < p := lt_of_le_of_lt (le_max_right _ _) hkp
  have hj : 1 ≤ p * a := Nat.one_le_iff_ne_zero.mpr (by positivity)
  have hjp : p * a < p ^ 2 := by
    rw [sq]
    exact Nat.mul_lt_mul_of_pos_left hap hp.out.pos
  have hk0 : -(k : ℚ) ≤ 0 := neg_nonpos.mpr (Nat.cast_nonneg _)
  have hkcast : ((k - 1 : ℕ) : ℚ) = (k : ℚ) - 1 := by
    rw [Nat.cast_sub (by omega)]
    norm_num
  unfold poleValue
  have hpow : VG p (((p * a : ℕ) : ℚ) ^ (k - 1)) ((k - 1 : ℕ) : ℚ) := by
    right
    rw [padicValRat.pow, padicValRat.of_nat, padicValNat.mul (by omega) (by omega),
      padicValNat_self, padicValNat_lt_p ha hap]
    simp
  have h1 : GV p (C (((p * a : ℕ) : ℚ) ^ (k - 1)) *
      (X - C (harmonic k (p * a)))) (-1) := by
    have h := GV.C_mul hpow
      ((GV.X.mono hk0).sub (GV.C (harmonic_valuation_sq k (p * a) hjp)))
    refine h.mono ?_
    rw [hkcast]
    linarith
  refine (h1.sub ((GV.C (pole_constant_valuation k hk hkp')).mono (by norm_num))).add (GV.C ?_)
  exact VG_inv_2j hp3 hj (e := 1) (padicValNat_lt_sq hj hjp)

end ZetaFive
