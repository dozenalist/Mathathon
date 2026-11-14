import Mathlib.Analysis.Complex.Basic
import Mathlib.Analysis.Real.Sqrt
import Mathlib.Data.ZMod.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.FinCases
open Complex
noncomputable section
def w : ℂ := ⟨-1 / 2, Real.sqrt 3 / 2⟩
example : normSq w = 1 := by
  rw [normSq_apply]
  simp only [w]
  nlinarith [Real.sq_sqrt (show (0:ℝ) ≤ 3 by norm_num)]
example (a : ℂ) (h : normSq a = 1) : ‖a‖ = 1 := by
  have h2 : ‖a‖ ^ 2 = 1 := by rw [← normSq_eq_norm_sq, h]
  nlinarith [norm_nonneg a]
example (v : ℂ) : normSq (1 + v) = normSq v + 2 * v.re + 1 := by
  rw [normSq_apply, normSq_apply]
  simp
  ring
example (a b c : Fin 2) (h1 : a ≠ b) (h2 : b ≠ c) (h3 : a ≠ c) : False := by
  fin_cases a <;> fin_cases b <;> fin_cases c <;> simp_all
example (n m : ℕ) (hm : 0 < m) (V : ZMod n → Bool)
    (h57 : ∀ i : ZMod n, V (i + (m : ZMod n)) = !(V i))
    (htr : ∀ (i : ZMod n) (k : ℤ),
      V (i + ((m : ℤ) : ZMod n) + ((k : ℤ) : ZMod n)) = !(V i)) : False := by
  have step : ∀ j : ZMod n, V (j + 1) = V j := by
    intro j
    have h1 := h57 (j - (m : ZMod n))
    have h2 := htr (j - (m : ZMod n)) 1
    rw [show j - (m : ZMod n) + (m : ZMod n) = j by ring] at h1
    rw [show j - (m : ZMod n) + ((m : ℤ) : ZMod n) + ((1 : ℤ) : ZMod n) = j + 1 by
      push_cast; ring] at h2
    rw [← h1] at h2
    exact h2
  have const : ∀ (t : ℕ) (j : ZMod n), V (j + (t : ZMod n)) = V j := by
    intro t
    induction t with
    | zero => intro j; simp
    | succ s ih =>
      intro j
      rw [show j + ((s + 1 : ℕ) : ZMod n) = (j + (s : ZMod n)) + 1 by push_cast; ring,
        step, ih]
  have h0 := const m 0
  rw [zero_add] at h0
  have h1 := h57 0
  rw [zero_add] at h1
  rw [← h0] at h1
  exact (by cases V (0 : ZMod n) <;> simp_all)
