/-
Combinatorial core of the k = 6 palette orbit bound (m6, direction d8).

If six 3-element subsets of Fin 6 are pairwise disjoint along the 6-cycle
(consecutive sets disjoint), then the sequence is forced to alternate with its
complement: P (j+1) = (P j)ᶜ and P (j+2) = P j.

Consequently an R-orbit at k = 6 whose six palettes are all ternary necessarily
puts a set and its complement on the same orbit, which is exactly what the
positive-measure pair-exclusion (Theorem 1 of proof.md) forbids.
-/
import Mathlib

open Finset

namespace PaletteOrbit

/-- In `Fin 6`, the complement of a 3-element set has 3 elements. -/
lemma card_compl_six (A : Finset (Fin 6)) (hA : A.card = 3) :
    (Finset.univ \ A).card = 3 := by
  rw [Finset.card_sdiff_of_subset (Finset.subset_univ A), Finset.card_univ,
    Fintype.card_fin, hA]

/-- Disjoint 3-sets in `Fin 6` are complementary. -/
lemma eq_compl_of_disjoint (A B : Finset (Fin 6))
    (hA : A.card = 3) (hB : B.card = 3) (hd : Disjoint A B) : B = Finset.univ \ A := by
  refine Finset.eq_of_subset_of_card_le ?_ ?_
  · intro x hx
    simp only [Finset.mem_sdiff, Finset.mem_univ, true_and]
    intro hxA
    exact (Finset.disjoint_left.mp hd hxA) hx
  · rw [card_compl_six A hA, hB]

/-- The alternation lemma (indexed by `ℕ`; use it on a periodic sequence). -/
lemma six_triples_alternate (P : ℕ → Finset (Fin 6))
    (h3 : ∀ j, (P j).card = 3)
    (hd : ∀ j, Disjoint (P j) (P (j + 1))) :
    ∀ j, P (j + 1) = Finset.univ \ P j ∧ P (j + 2) = P j := by
  intro j
  have h1 : P (j + 1) = Finset.univ \ P j :=
    eq_compl_of_disjoint (P j) (P (j + 1)) (h3 j) (h3 (j + 1)) (hd j)
  have h2 : P (j + 2) = Finset.univ \ P (j + 1) := by
    have h := eq_compl_of_disjoint (P (j + 1)) (P (j + 1 + 1)) (h3 (j + 1))
      (h3 (j + 1 + 1)) (hd (j + 1))
    simpa only [show j + 1 + 1 = j + 2 by ring] using h
  refine ⟨h1, ?_⟩
  rw [h2, h1]
  ext x
  simp only [Finset.mem_sdiff, Finset.mem_univ, true_and, not_not]

/-- All six palettes ternary forces the alternating complementary pattern. -/
theorem all_ternary_is_alternating (P : ℕ → Finset (Fin 6))
    (h3 : ∀ j, (P j).card = 3)
    (hd : ∀ j, Disjoint (P j) (P (j + 1))) :
    P 1 = Finset.univ \ P 0 ∧ P 2 = P 0 ∧ P 3 = Finset.univ \ P 0 ∧
      P 4 = P 0 ∧ P 5 = Finset.univ \ P 0 := by
  obtain ⟨h1, h2⟩ := six_triples_alternate P h3 hd 0
  obtain ⟨h3', h4⟩ := six_triples_alternate P h3 hd 1
  obtain ⟨h5', h6⟩ := six_triples_alternate P h3 hd 2
  obtain ⟨h7', h8⟩ := six_triples_alternate P h3 hd 3
  -- h1 : P 1 = univ \ P 0,  h2 : P 2 = P 0
  -- h3' : P 2 = univ \ P 1, h4 : P 3 = P 1
  -- h5' : P 3 = univ \ P 2, h6 : P 4 = P 2
  -- h7' : P 4 = univ \ P 3, h8 : P 5 = P 3
  refine ⟨h1, h2, ?_, ?_, ?_⟩
  · rw [h4, h1]
  · rw [h6, h2]
  · rw [h8, h4, h1]

end PaletteOrbit

#print axioms PaletteOrbit.all_ternary_is_alternating
#print axioms PaletteOrbit.six_triples_alternate
