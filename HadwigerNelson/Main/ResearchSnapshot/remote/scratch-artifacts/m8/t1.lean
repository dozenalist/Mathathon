import Mathlib.Data.Complex.Basic
import Mathlib.Data.ZMod.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.FinCases

example : (⟨(-1/2 : ℝ), Real.sqrt 3 / 2⟩ : ℂ).re = -1/2 := rfl
example : Complex.normSq (⟨(-1/2 : ℝ), Real.sqrt 3 / 2⟩ : ℂ)
    = (-1/2 : ℝ) * (-1/2) + (Real.sqrt 3 / 2) * (Real.sqrt 3 / 2) := by
  rw [Complex.normSq_apply]
example (w : ℂ) : Complex.normSq w = w.re * w.re + w.im * w.im := Complex.normSq_apply w
example : Real.sqrt 3 ^ 2 = 3 := Real.sq_sqrt (by norm_num)
example (a b c : Fin 2) (h1 : a ≠ b) (h2 : b ≠ c) (h3 : a ≠ c) : False := by
  fin_cases a <;> fin_cases b <;> fin_cases c <;> simp_all
