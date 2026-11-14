/-
  Machine-checked counting step of the k = 6 free-label obstruction
  (swarm smwfwznwk, member m4, direction d3).

  At a 6-cycle centre of a weak measurable 6-colouring every palette has size 2 or 3
  (paper (6.2) + the palette bound).  If one label i0 is absent from every palette, then the
  three palettes at the vertices of a unit equilateral triangle are three pairwise disjoint
  nonempty subsets of the five labels [6] \ {i0}, and (TE) makes them pairwise disjoint.  Three
  pairwise disjoint subsets of a 5-set cannot all have at least two elements.

  Deliberately light imports: the full `Mathlib` import is very slow in this VM.
  `lean count_lemma.lean` (LEAN_PATH already points at the built Mathlib).
-/
import Mathlib.Data.Finset.Card
import Mathlib.Data.Fin.Basic
import Mathlib.Data.Fintype.Card

open Finset

/-- Three pairwise disjoint subsets of a 5-element set have total size at most 5. -/
theorem card_three_disjoint_le {α : Type*} [DecidableEq α] (U : Finset α) (hU : U.card = 5)
    (A B C : Finset α) (hA : A ⊆ U) (hB : B ⊆ U) (hC : C ⊆ U)
    (hAB : Disjoint A B) (hAC : Disjoint A C) (hBC : Disjoint B C) :
    A.card + B.card + C.card ≤ 5 := by
  have hdisj : Disjoint (A ∪ B) C := by
    refine Finset.disjoint_left.mpr ?_
    intro x hx hxC
    rcases Finset.mem_union.mp hx with h | h
    · exact (Finset.disjoint_left.mp hAC) h hxC
    · exact (Finset.disjoint_left.mp hBC) h hxC
  have e1 : (A ∪ B ∪ C).card = (A ∪ B).card + C.card :=
    Finset.card_union_of_disjoint hdisj
  have e2 : (A ∪ B).card = A.card + B.card := Finset.card_union_of_disjoint hAB
  have e3 : (A ∪ B ∪ C).card ≤ U.card := by
    refine Finset.card_le_card ?_
    intro x hx
    rcases Finset.mem_union.mp hx with hx' | hxC
    · rcases Finset.mem_union.mp hx' with h | h
      · exact hA h
      · exact hB h
    · exact hC hxC
  calc A.card + B.card + C.card = (A ∪ B).card + C.card := by rw [e2]
    _ = (A ∪ B ∪ C).card := e1.symm
    _ ≤ U.card := e3
    _ = 5 := hU

/-- At k = 6 a globally free label is incompatible with (TE) and palette size at least two at the
three vertices of a unit triangle: no such triple of palettes exists. -/
theorem no_free_label_triangle (i0 : Fin 6) (A B C : Finset (Fin 6))
    (hA : A ⊆ Finset.univ.erase i0) (hB : B ⊆ Finset.univ.erase i0)
    (hC : C ⊆ Finset.univ.erase i0)
    (hAB : Disjoint A B) (hAC : Disjoint A C) (hBC : Disjoint B C)
    (h1 : 2 ≤ A.card) (h2 : 2 ≤ B.card) (h3 : 2 ≤ C.card) : False := by
  have hU : (Finset.univ.erase i0).card = 5 := by
    rw [Finset.card_erase_of_mem (Finset.mem_univ i0), Finset.card_univ, Fintype.card_fin]
  have h := card_three_disjoint_le (Finset.univ.erase i0) hU A B C hA hB hC hAB hAC hBC
  have h6 : 2 + 2 + 2 ≤ A.card + B.card + C.card :=
    Nat.add_le_add (Nat.add_le_add h1 h2) h3
  have : 6 ≤ 5 := Nat.le_trans h6 h
  exact absurd this (by decide)

/-- Every label of `Fin 6` lies in an edge `{i, i+1}` of the six-cycle, so an admissible palette
(one contained in no edge) has at least two elements. -/
theorem admissible_card_ge_two (P : Finset (Fin 6))
    (h : ∀ i : Fin 6, ¬ P ⊆ ({i, i + 1} : Finset (Fin 6))) : 2 ≤ P.card := by
  have hne : P.Nonempty := by
    rcases Finset.eq_empty_or_nonempty P with hemp | hne
    · exfalso
      exact (h 0) (by rw [hemp]; exact Finset.empty_subset _)
    · exact hne
  obtain ⟨b, hb⟩ := hne
  have hnb : ¬ P ⊆ ({b, b + 1} : Finset (Fin 6)) := h b
  rw [Finset.not_subset] at hnb
  obtain ⟨c, hcP, hc⟩ := hnb
  have hbc : b ≠ c := by
    intro heq
    exact hc (by rw [heq]; exact Finset.mem_insert_self _ _)
  have h2 : ({b, c} : Finset (Fin 6)) ⊆ P := by
    intro x hx
    rcases Finset.mem_insert.mp hx with rfl | hx
    · exact hb
    · rw [Finset.mem_singleton] at hx
      rw [hx]
      exact hcP
  have := Finset.card_le_card h2
  rw [Finset.card_pair hbc] at this
  exact this

#print axioms card_three_disjoint_le
#print axioms no_free_label_triangle
#print axioms admissible_card_ge_two
