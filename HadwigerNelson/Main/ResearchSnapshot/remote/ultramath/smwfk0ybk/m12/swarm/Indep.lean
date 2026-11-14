import Mathlib

/-!
# (C5) is redundant given (C3) and (C4) at `k = 6`

Six palettes `P_0,…,P_5` at the six directions of a `π/3`-orbit, `k = 6` (labels `Fin 6`).
* `(C1)`  `|P_i| ≤ 3`                                   (general-`k` palette bound)
* `(C3)`  `P_i` and `P_{i+1}` are disjoint              (sixty-degree disjointness, (5.7))
* `(C4)`  no two palettes are complementary triples     (m6 Theorem 1 at `k = 6`)

Given `(C1)` and `|Fin 6| = 6`, "complementary triples" is the same relation as
"disjoint triples" (`union_univ_iff_disjoint_of_card_three` below), which is the form used
in `card_ternary_le_three`.  The conclusion `(C5)` — at most three ternary palettes in the
orbit — is then the statement that no four vertices of a `6`-cycle are pairwise
non-adjacent, proved by exhaustive decision (`indep_card_le_three`).
-/

namespace PaletteIndep

/-- Cyclic adjacency on `Fin 6`: `b` is `a + 1` or `a` is `b + 1`. -/
def Adj (a b : Fin 6) : Bool := (b == a + 1) || (a == b + 1)

/-- No four vertices of a `6`-cycle are pairwise non-adjacent: an independent set of `C_6`
has at most three elements.  (Exhaustive decision over the `64` subsets of `Fin 6`.) -/
theorem indep_card_le_three :
    ∀ S : Finset (Fin 6),
      (∀ a b : Fin 6, a ∈ S → b ∈ S → Adj a b = true → False) → S.card ≤ 3 := by
  decide

/-- **The combinatorial core.**  If the six palettes are consecutive-disjoint `(C3)` and no
two of them are disjoint triples `(C4)` in the `(C1)`-bounded sense, then at most three of
them are ternary `(C5)`.  Neither the palette bound `(C1)` nor the ray geometry is used: the
implication is carried by the six-cycle alone. -/
theorem card_ternary_le_three (P : Fin 6 → Finset (Fin 6))
    (h3 : ∀ i, Disjoint (P i) (P (i + 1)))
    (h4 : ∀ i j, ¬ (Disjoint (P i) (P j) ∧ (P i).card = 3 ∧ (P j).card = 3)) :
    (Finset.univ.filter (fun i => (P i).card = 3)).card ≤ 3 := by
  apply indep_card_le_three
  intro a b ha hb hab
  simp only [Finset.mem_filter, Finset.mem_univ, true_and] at ha hb
  simp only [Adj, Bool.or_eq_true, beq_iff_eq] at hab
  rcases hab with h | h
  · exact h4 a b ⟨by rw [h]; exact h3 a, ha, hb⟩
  · exact h4 a b ⟨by rw [h]; exact (h3 b).symm, ha, hb⟩

/-- At `k = 6` (labels `Fin 6`) and with `(C1)` in force, m6's form of `(C4)`
(`A ∪ B = univ`) is the same constraint as "`A` and `B` are not disjoint triples". -/
theorem union_univ_iff_disjoint_of_card_three (A B : Finset (Fin 6))
    (hA : A.card = 3) (hB : B.card = 3) : (A ∪ B = Finset.univ) ↔ Disjoint A B := by
  constructor
  · intro hun
    by_contra hdis
    have hne : A ∩ B ≠ ∅ := by
      simpa [Finset.disjoint_iff_inter_eq_empty] using hdis
    have hpos : 0 < (A ∩ B).card := Finset.card_pos.mpr (Finset.nonempty_iff_ne_empty.mpr hne)
    have h6 : (A ∪ B).card = 6 := by rw [hun]; simp
    have := Finset.card_union_add_card_inter A B
    omega
  · intro hdis
    have h6 : (A ∪ B).card = 6 := by
      rw [Finset.card_union_of_disjoint hdis, hA, hB]
    exact Finset.eq_of_subset_of_card_le (Finset.subset_univ _) (by simp [h6])

/-- The same conclusion from m6's literal form of `(C4)`: no two palettes exhaust `Fin 6`. -/
theorem card_ternary_le_three_union_form (P : Fin 6 → Finset (Fin 6))
    (h3 : ∀ i, Disjoint (P i) (P (i + 1)))
    (h4 : ∀ i j, P i ∪ P j ≠ Finset.univ) :
    (Finset.univ.filter (fun i => (P i).card = 3)).card ≤ 3 := by
  exact card_ternary_le_three P h3 (fun i j h =>
    h4 i j ((union_univ_iff_disjoint_of_card_three _ _ h.2.1 h.2.2).mpr h.1))

end PaletteIndep

#print axioms PaletteIndep.card_ternary_le_three
#print axioms PaletteIndep.card_ternary_le_three_union_form
