/-
  Machine-checked finite core for `NOTE.md` (member `m4`, swarm `smwg1r9lg`, direction `d2`).

  On one `R`-orbit the printed axioms reduce (Observation 5.0 of the note) to: the state function
  `sigma_x : S -> O` is a proper colouring of the 6-cycle, i.e. `w (k+1) != w k` for all `k` in
  `ZMod 6`.  This file checks the finitary content of Theorem 2(d) / Lemma 5.1 of the note:

    * `two_valued_periodic` : every two-valued proper orbit word is invariant under the square of
      the rotation (hence the rigid alternation; each state then occupies exactly half the circle);
    * the exact counts `2 / 66 / 732` for `|O| = 2,3,4` and `60` words using all three values at
      `|O| = 3` (the `k = 5`, `6`, `7` calibrations of the record and the `k = 6` decision).

  Nothing here is analytic; the analytic content of the note is in `NOTE.md` §§3-4.
-/
import Mathlib

namespace Smwg1r9lg.M4

/-- orbit words: a state function on one `R`-orbit `{e, Re, ..., R^5 e}` -/
abbrev Word (m : ℕ) := ZMod 6 → Fin m

/-- the rule `(5.7)` at every orbit position: consecutive states differ -/
abbrev Proper {m : ℕ} (w : Word m) : Prop := ∀ k : ZMod 6, w (k + 1) ≠ w k

/-- **Lemma 5.1**: a two-valued proper orbit word is `2`-periodic, i.e. invariant under `R^2`. -/
theorem two_valued_periodic (w : Word 2) (h : Proper w) :
    ∀ k : ZMod 6, w (k + 1 + 1) = w k := by
  intro k
  have h1 : w (k + 1) ≠ w k := h k
  have h2 : w (k + 1 + 1) ≠ w (k + 1) := h (k + 1)
  revert h1 h2
  generalize w k = a
  generalize w (k + 1) = b
  generalize w (k + 1 + 1) = c
  revert a b c
  decide

/-- the count of proper orbit words with `|O| = 2` (the `k = 5` calibration: binarity forced) -/
theorem card_two : (Finset.univ.filter (fun w : Word 2 => Proper w)).card = 2 := by decide

/-- the count of proper orbit words with `|O| = 3` (the `k = 6` decision) -/
theorem card_three : (Finset.univ.filter (fun w : Word 3 => Proper w)).card = 66 := by decide

/-- of those, the ones that are genuinely three-valued -/
theorem card_three_valued :
    (Finset.univ.filter (fun w : Word 3 => Proper w ∧ ∀ i : Fin 3, ∃ k : ZMod 6, w k = i)).card
      = 60 := by decide

set_option maxRecDepth 1000000 in
/-- the count of proper orbit words with `|O| = 4` (the `k = 7` calibration) -/
theorem card_four : (Finset.univ.filter (fun w : Word 4 => Proper w)).card = 732 := by decide

set_option maxRecDepth 1000000 in
/-- the closed form of the count, for the three cases used in the note -/
theorem closed_form (m : ℕ) (hm : m ∈ [2, 3, 4]) :
    (Finset.univ.filter (fun w : Word m => Proper w)).card = (m - 1) ^ 6 + (m - 1) := by
  simp only [List.mem_cons, List.not_mem_nil, or_false] at hm
  rcases hm with rfl | rfl | rfl
  · exact card_two
  · exact card_three
  · exact card_four

end Smwg1r9lg.M4

#print axioms Smwg1r9lg.M4.two_valued_periodic
#print axioms Smwg1r9lg.M4.card_two
#print axioms Smwg1r9lg.M4.card_three
#print axioms Smwg1r9lg.M4.card_three_valued
#print axioms Smwg1r9lg.M4.card_four
#print axioms Smwg1r9lg.M4.closed_form
