import Mathlib
import Mathlib.Tactic.MinImports

#min_imports in
example : (1:ℕ) + 1 = 2 := by omega

#min_imports in
example (h : ¬ (∀ n : ℕ, n = 0)) : ∃ n : ℕ, n ≠ 0 := by push_neg at h; exact h

#min_imports in
example : ((3:ℕ):ℤ) = 3 := by norm_cast

#min_imports in
example : True ∧ True := by aesop

#min_imports in
example : Measurable (fun x : ℝ => x) := by measurability

#min_imports in
example (h : ∀ n : ℕ, n = 0) : (fun n => n) = fun _ => 0 := by funext; exact h
