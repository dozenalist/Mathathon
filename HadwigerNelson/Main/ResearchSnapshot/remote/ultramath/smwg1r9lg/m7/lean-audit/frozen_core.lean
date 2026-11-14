/-
  The finite combinatorial core of the frozen-field obstruction at six colours.

  Swarm smwfwi7rh, member m11.  See `RESULTS.md` §4.

  Lemma 5.2(3) of the paper, applied at centre separation 1 with the representation
  that the paper itself writes out in Remark 5.3, says that for every unit vector `a`

      P_{x+a}(f) ∩ P_x(f) = ∅      for almost every direction `f`.

  A palette field that does not depend on the centre (a "frozen" field: every
  countermodel of the previous swarm's report is of this form) therefore satisfies
  `P(f) ∩ P(f+δ) = ∅` for every shift `δ` in its shift set.  This file records the
  purely finite consequence used in `RESULTS.md` §4: in a six-element label set three
  pairwise disjoint palettes of size at least two exhaust the labels, so

  * a fourth non-empty palette cannot be disjoint from all three, and
  * if some label belongs to no palette, three such palettes cannot exist at all.

  Build:  lean frozen_core.lean
-/
import Mathlib.Data.Finset.Card
import Mathlib.Tactic.Linarith

open Finset

variable {ι : Type*} [DecidableEq ι]

/-- Three pairwise disjoint palettes of size at least two, inside a six-element label
set `U`, exhaust `U`. -/
theorem union_eq_of_three_disjoint
    {A B C U : Finset ι} (hAU : A ⊆ U) (hBU : B ⊆ U) (hCU : C ⊆ U) (hU : U.card = 6)
    (hAB : Disjoint A B) (hAC : Disjoint A C) (hBC : Disjoint B C)
    (hA : 2 ≤ A.card) (hB : 2 ≤ B.card) (hC : 2 ≤ C.card) :
    A ∪ B ∪ C = U := by
  have hsub : A ∪ B ∪ C ⊆ U := by
    intro x hx
    simp only [mem_union] at hx
    rcases hx with (hx | hx) | hx
    · exact hAU hx
    · exact hBU hx
    · exact hCU hx
  have h1 : Disjoint (A ∪ B) C := Finset.disjoint_union_left.mpr ⟨hAC, hBC⟩
  have hcard : (A ∪ B ∪ C).card = A.card + B.card + C.card := by
    rw [card_union_of_disjoint h1, card_union_of_disjoint hAB]
  have hA6 : A.card ≤ 6 := by rw [← hU]; exact card_le_card hAU
  have hB6 : B.card ≤ 6 := by rw [← hU]; exact card_le_card hBU
  have hC6 : C.card ≤ 6 := by rw [← hU]; exact card_le_card hCU
  apply Finset.eq_of_subset_of_card_le hsub
  rw [hcard, hU]
  linarith

/-- A fourth non-empty palette cannot be disjoint from all three. -/
theorem not_disjoint_fourth
    {A B C D U : Finset ι} (hAU : A ⊆ U) (hBU : B ⊆ U) (hCU : C ⊆ U) (hU : U.card = 6)
    (hAB : Disjoint A B) (hAC : Disjoint A C) (hBC : Disjoint B C)
    (hA : 2 ≤ A.card) (hB : 2 ≤ B.card) (hC : 2 ≤ C.card)
    (hD : D.Nonempty) (hDU : D ⊆ U)
    (hDA : Disjoint D A) (hDB : Disjoint D B) (hDC : Disjoint D C) :
    False := by
  have huniv := union_eq_of_three_disjoint hAU hBU hCU hU hAB hAC hBC hA hB hC
  obtain ⟨x, hx⟩ := hD
  have hx' : x ∈ A ∪ B ∪ C := by rw [huniv]; exact hDU hx
  rw [Finset.mem_union, Finset.mem_union] at hx'
  rcases hx' with (hxA | hxB) | hxC
  · exact (Finset.disjoint_left.mp hDA hx) hxA
  · exact (Finset.disjoint_left.mp hDB hx) hxB
  · exact (Finset.disjoint_left.mp hDC hx) hxC

/-- If some label of the six-element label set belongs to none of three pairwise
disjoint palettes, then one of the three has at most one element. -/
theorem exists_card_le_one_of_free_label
    {A B C U : Finset ι} (hAU : A ⊆ U) (hBU : B ⊆ U) (hCU : C ⊆ U) (hU : U.card = 6)
    (hAB : Disjoint A B) (hAC : Disjoint A C) (hBC : Disjoint B C)
    (hfree : ∃ i ∈ U, i ∉ A ∧ i ∉ B ∧ i ∉ C) :
    A.card ≤ 1 ∨ B.card ≤ 1 ∨ C.card ≤ 1 := by
  by_contra h
  push_neg at h
  obtain ⟨hA, hB, hC⟩ := h
  have huniv := union_eq_of_three_disjoint hAU hBU hCU hU hAB hAC hBC hA hB hC
  obtain ⟨i, hiU, hiA, hiB, hiC⟩ := hfree
  have : i ∈ A ∪ B ∪ C := by rw [huniv]; exact hiU
  rw [Finset.mem_union, Finset.mem_union] at this
  tauto

#print axioms union_eq_of_three_disjoint
#print axioms not_disjoint_fourth
#print axioms exists_card_le_one_of_free_label

#print axioms union_eq_of_three_disjoint
#print axioms not_disjoint_fourth
#print axioms exists_card_le_one_of_free_label
