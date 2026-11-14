/-
  Sharpness certificates for the four machine-checked cores audited in direction d8
  (swarm smwg1r9lg, member m7).

  An audit must answer not only "does it compile" but "is it vacuous, or weaker than the
  use made of it".  Each theorem below exhibits the hypothesis whose removal breaks the
  conclusion, i.e. proves the core is sharp:

  * `clique_le_two_sharp`      -- `card_le_two_of_isClique_of_acyclic` needs acyclicity:
                                  on three labels the complete graph carries a 3-clique.
  * `union_eq_three_disjoint_sharp`
                               -- `union_eq_of_three_disjoint` needs palettes of size >= 2:
                                  three singleton palettes in a six-element label set do not
                                  exhaust it, so the frozen-field core is not a triviality.
  * `no_free_label_triangle_sharp`
                               -- `no_free_label_triangle` needs the absent label: without it
                                  three pairwise disjoint palettes of size 2 exist in [6].
  * `sector_two_valued_is_sharp` -- `no_two_valued_sector_field` is a *two-valued* statement:
                                  at n = 6 sector positions with rotation shift m = 1 the
                                  three-valued field V i = i mod 3 satisfies the same (5.7) and
                                  transport hypotheses.  This is the finite form of the
                                  three-valued wall of REPORT.md §5c.
-/
import Mathlib.Data.Finset.Card
import Mathlib.Data.Fin.Basic
import Mathlib.Data.Fintype.Card
import Mathlib.Data.ZMod.Basic
import Mathlib.Combinatorics.SimpleGraph.Acyclic
import Mathlib.Tactic.NormNum

open Finset

/-! ### 1. The clique-in-a-forest step needs acyclicity -/

/-- On three labels the complete graph carries a clique of size three and is not acyclic,
so the acyclicity hypothesis of `card_le_two_of_isClique_of_acyclic` cannot be dropped. -/
theorem clique_le_two_sharp :
    ∃ (G : SimpleGraph (Fin 3)) (s : Finset (Fin 3)),
      ¬ G.IsAcyclic ∧ (∀ i ∈ s, ∀ j ∈ s, i ≠ j → G.Adj i j) ∧ 2 < s.card := by
  refine ⟨⊤, univ, ?_, ?_, by simp⟩
  · intro h
    have hcf : (⊤ : SimpleGraph (Fin 3)).CliqueFree 3 := h.cliqueFree (by norm_num)
    apply hcf univ
    rw [SimpleGraph.isNClique_iff]
    refine ⟨?_, by simp⟩
    rw [SimpleGraph.isClique_iff]
    intro a _ b _ hab
    simpa using hab
  · intro i _ j _ hij
    simpa using hij

/-! ### 2. The frozen-field finite core needs palettes of size two -/

/-- Three singleton palettes inside a six-element label set are pairwise disjoint and do not
exhaust it: the hypothesis `2 <= A.card` (and its two companions) in
`union_eq_of_three_disjoint` is essential. -/
theorem union_eq_three_disjoint_sharp :
    ∃ A B C U : Finset (Fin 6),
      A ⊆ U ∧ B ⊆ U ∧ C ⊆ U ∧ U.card = 6 ∧
        Disjoint A B ∧ Disjoint A C ∧ Disjoint B C ∧
        A.card = 1 ∧ B.card = 1 ∧ C.card = 1 ∧ A ∪ B ∪ C ≠ U := by
  refine ⟨{0}, {1}, {2}, univ, ?_⟩
  decide

/-! ### 3. The free-label counting step needs the free label -/

/-- In a six-element label set three pairwise disjoint palettes of size two exist, so the
hypothesis that a label is absent from all of them is what makes
`no_free_label_triangle` true. -/
theorem no_free_label_triangle_sharp :
    ∃ A B C : Finset (Fin 6),
      Disjoint A B ∧ Disjoint A C ∧ Disjoint B C ∧
        2 ≤ A.card ∧ 2 ≤ B.card ∧ 2 ≤ C.card := by
  refine ⟨{0, 1}, {2, 3}, {4, 5}, ?_⟩
  decide

/-! ### 4. The sector obstruction is two-valued, and only two-valued -/

/-- `V i = i mod 3` on six sector positions. -/
def V3 : ZMod 6 → Fin 3 := fun i => ⟨i.val % 3, Nat.mod_lt _ (by norm_num)⟩

/-- The three-valued sector field at `n = 6`, `m = 1` satisfies the two hypotheses of
`Repair31.no_two_valued_sector_field` (the sixty-degree exclusion `V (i+m) ≠ V i` and the
transport `V (i+m+1) ≠ V i`) with `≠` in place of `= !`.  Hence that theorem is exactly a
two-valued statement: the passage from two to three values is where it stops. -/
theorem sector_two_valued_is_sharp :
    (∀ i : ZMod 6, V3 (i + 1) ≠ V3 i) ∧ (∀ i : ZMod 6, V3 (i + 1 + 1) ≠ V3 i) := by
  constructor <;> decide

#print axioms clique_le_two_sharp
#print axioms union_eq_three_disjoint_sharp
#print axioms no_free_label_triangle_sharp
#print axioms sector_two_valued_is_sharp
