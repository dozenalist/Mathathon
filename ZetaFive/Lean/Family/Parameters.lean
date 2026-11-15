module

public import Mathlib.Data.Nat.Factorial.BigOperators
public import Mathlib.Order.Interval.Finset.Nat
public import Mathlib.Data.Rat.Cast.Order
public import Mathlib.Algebra.Order.BigOperators.Group.Finset
public import Mathlib.Tactic.Positivity

@[expose] public section

/-! # Parameters shared by every zeta weight

The family parameters are separate from the integer `k`. Both the original
40/3/37 family and the 12/1/11 family in Calegari's exposition are available.
-/

namespace ZetaFive

structure Parameters where
  K : ℕ
  N : ℕ
  numeratorPower : ℕ
  h : ℕ

def laiParameters (n : ℕ) : Parameters := ⟨40 * n, 3 * n, 6, 37 * n⟩

def calegariParameters (n : ℕ) : Parameters := ⟨12 * n, n, 6, 11 * n⟩

theorem laiParameters_size (n : ℕ) :
    (laiParameters n).h = (laiParameters n).K - (laiParameters n).N := by
  simp only [laiParameters]; omega

theorem calegariParameters_size (n : ℕ) :
    (calegariParameters n).h = (calegariParameters n).K - (calegariParameters n).N := by
  simp only [calegariParameters]; omega

/-- The parameter-independent normalizing factor, before clearing arithmetic denominators. -/
noncomputable def scale (p : Parameters) : ℚ :=
  (p.K.factorial : ℚ) ^ (2 * p.h) * 4 ^ (p.h - 1) /
    ((p.N.factorial : ℚ) ^ (2 * p.numeratorPower * p.h) *
      ∏ i ∈ Finset.Icc 1 (p.h - 1), ((2 * i).factorial : ℚ) ^ 2)

theorem scale_pos (p : Parameters) : 0 < scale p := by
  unfold scale
  apply div_pos
  · positivity
  · apply mul_pos
    · positivity
    · exact Finset.prod_pos fun i _ => by positivity

end ZetaFive

