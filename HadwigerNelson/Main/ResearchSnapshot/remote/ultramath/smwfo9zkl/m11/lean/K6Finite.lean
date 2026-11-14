/-
  K6Finite.lean -- finite label combinatorics at k = 6 (light imports).

  Companion to ../k6-ternary-palette.md.

  At k = 6 the general-k palette bound is |P| <= k - 3 = 3.  Two disjoint
  3-element palettes need 2 * (k - 3) = k labels, so they are exactly
  complementary: this is the label count special to k = 6, and it is why
  paper (5.2) (the union of two palettes is never all of Fin 6) obstructs two
  60-degree-separated ternary palettes.
-/
import Mathlib.Data.Finset.Card
import Mathlib.Data.Fintype.Powerset
import Mathlib.Data.Fin.Basic

namespace K6Ternary

/-- Two disjoint 3-element subsets of `Fin 6` are complementary. -/
theorem union_eq_univ_of_card_three {s t : Finset (Fin 6)}
    (hs : s.card = 3) (ht : t.card = 3) (hd : Disjoint s t) : s ∪ t = Finset.univ := by
  refine Finset.eq_of_subset_of_card_le (fun a _ => Finset.mem_univ a) ?_
  rw [Finset.card_union_of_disjoint hd, hs, ht]
  simp

/-- Contrapositive form: if the union of the two palettes is not all of `Fin 6`,
at most one of them has three labels. -/
theorem not_both_three {s t : Finset (Fin 6)}
    (hd : Disjoint s t) (hu : s ∪ t ≠ Finset.univ) : s.card ≠ 3 ∨ t.card ≠ 3 := by
  rcases eq_or_ne s.card 3 with h | h
  · rcases eq_or_ne t.card 3 with h' | h'
    · exact absurd (union_eq_univ_of_card_three h h' hd) hu
    · exact Or.inr h'
  · exact Or.inl h

/-- Discrete per-orbit form of the measure bound: in the six directions of one
`R`-orbit, the directions carrying a three-label palette form an independent
set of the six-cycle (paper (5.7) forbids two 60-degree-separated ternary
palettes), hence number at most three out of six. -/
theorem cycle_indep_card_le_three (A : Finset (Fin 6))
    (h : ∀ a ∈ A, a + 1 ∉ A) : A.card ≤ 3 := by
  decide +revert

/-- Sanity check: the bound is attained, by the three even residues. -/
theorem cycle_indep_attained :
    (Finset.univ.filter (fun a : Fin 6 => a.val % 2 = 0)).card = 3 := by
  decide

end K6Ternary
