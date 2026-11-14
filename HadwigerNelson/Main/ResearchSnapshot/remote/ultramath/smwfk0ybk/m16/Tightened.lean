/-
  Tightened.lean  (member m16, swarm smwfk0ybk, direction d9)

  End-to-end machine-checked composition:
    m5's existence theorems for the (C1)-(C3) interface system at k = 6
    +  the shrink theorem of `PaletteShrink.lean`
    =>  the TIGHTENED system (C1)-(C5) (m6's pair exclusion (C4) and orbit bound (C5)
        added) is satisfiable at k = 6 for every interface length ell in {3,4,5,6}.

  Consequently no argument whose hypotheses are (C1)-(C5) at a cyclic centre can conclude
  a contradiction at k = 6: Step 1 of the brief is decision-negative, and (C4)/(C5) cannot
  be the constraints that yield chi(R^2) >= 7.
-/
import M5Interface
import PaletteShrink

namespace InterfaceStates

open PaletteShrink

variable {k ell : Nat}

/-- (C4) at the orbit level (m6, Theorem 1, general k): no two palettes of the six-position
orbit have union all of `Fin k`.  At `k = 6` this is exactly "no two palettes are
complementary 3-element sets". -/
def HasC4 (P : Fin 6 → Finset (Fin k)) : Prop := ∀ i j, P i ∪ P j ≠ Finset.univ

/-- (C5) at the orbit level (m6, Theorem 2, general k): at most three of the six palettes
have the maximal admissible size `k-3`. -/
def HasC5 (P : Fin 6 → Finset (Fin k)) : Prop :=
  ∀ S : Finset (Fin 6), (∀ i ∈ S, (P i).card = k - 3) → S.card ≤ 3

/-- The paper's `O(e)` as a finset: the labels that are not endpoints of a positive edge. -/
noncomputable def Oset (σ : Sig ell) (i : Fin 6) : Finset (Fin k) := by
  classical
  exact Finset.univ.filter (fun l => inO σ i l)

/-- The paper's `I(e)` as a finset. -/
noncomputable def Iset (σ : Sig ell) (i : Fin 6) : Finset (Fin k) := by
  classical
  exact Finset.univ.filter (fun l => inI σ i l)

lemma mem_Oset {σ : Sig ell} {i : Fin 6} {l : Fin k} : l ∈ Oset (k := k) σ i ↔ inO σ i l := by
  classical simp [Oset]

lemma mem_Iset {σ : Sig ell} {i : Fin 6} {l : Fin k} : l ∈ Iset (k := k) σ i ↔ inI σ i l := by
  classical simp [Iset]

lemma next6_eq_nxt (i : Fin 6) : next6 i = nxt i := rfl

/-- **Main composition.**  For `k ≥ 6`, any model of (C1)-(C3) at a cyclic centre can be
replaced by one that also satisfies (C4) and (C5). -/
theorem exists_tightened_of_isModel (hk : 6 ≤ k) (σ : Sig ell)
    (P : Fin 6 → Finset (Fin k)) (h : IsModel σ P) :
    ∃ Q : Fin 6 → Finset (Fin k), IsModel σ Q ∧ HasC4 Q ∧ HasC5 Q := by
  classical
  have hO : ∀ i, (P i ∩ Oset (k := k) σ i).Nonempty := by
    intro i
    obtain ⟨l, hlP, hlO⟩ := h.meets_O i
    exact ⟨l, by simp [mem_Oset, hlP, hlO]⟩
  have hI : ∀ i, (P i ∩ Iset (k := k) σ i).Nonempty := by
    intro i
    obtain ⟨l, hlP, hlI⟩ := h.meets_I i
    exact ⟨l, by simp [mem_Iset, hlP, hlI]⟩
  have h3' : ∀ i, Disjoint (P i) (P (next6 i)) := by
    intro i
    rw [next6_eq_nxt]
    exact h.disj i
  obtain ⟨Q, h1, h2, hO', hI', h3, hPhi⟩ :=
    neutral_of_pair_satisfied hk (Oset (k := k) σ) (Iset (k := k) σ)
      (fun Q => HasC4 Q ∧ HasC5 Q)
      (fun Q hQ => ⟨c4_of_pair hk Q hQ, c5_of_pair hk Q hQ⟩)
      P h.card_pos h.card_le hO hI h3'
  refine ⟨Q, ⟨h1, h2, ?_, ?_, ?_⟩, hPhi⟩
  · intro i
    obtain ⟨l, hl⟩ := hO' i
    exact ⟨l, (Finset.mem_inter.mp hl).1, (mem_Oset).mp (Finset.mem_inter.mp hl).2⟩
  · intro i
    obtain ⟨l, hl⟩ := hI' i
    exact ⟨l, (Finset.mem_inter.mp hl).1, (mem_Iset).mp (Finset.mem_inter.mp hl).2⟩
  · intro i
    rw [← next6_eq_nxt]
    exact h3 i

/-- **The tightened interface system is satisfiable at `k = 6` at every length.**
This is the machine-checked negation of the Step-1 hope: adding (C4) and (C5) to m5's
system produces no contradiction, at any interface length supplied by Proposition 7.1. -/
theorem tightened_silent_at_six :
    (∀ σ : Sig 3, ∃ P : Fin 6 → Finset (Fin 6), IsModel σ P ∧ HasC4 P ∧ HasC5 P) ∧
    (∀ σ : Sig 4, ∃ P : Fin 6 → Finset (Fin 6), IsModel σ P ∧ HasC4 P ∧ HasC5 P) ∧
    (∃ σ : Sig 5, ∃ P : Fin 6 → Finset (Fin 6), IsModel σ P ∧ HasC4 P ∧ HasC5 P) ∧
    (∃ σ : Sig 6, ∃ P : Fin 6 → Finset (Fin 6), IsModel σ P ∧ HasC4 P ∧ HasC5 P) :=
  ⟨fun σ => exists_tightened_of_isModel (k := 6) (ell := 3) (by norm_num) σ _ (k6_ell3 σ),
   fun σ => exists_tightened_of_isModel (k := 6) (ell := 4) (by norm_num) σ _ (k6_ell4 σ),
   ⟨cellSig c5, exists_tightened_of_isModel (k := 6) (ell := 5) (by norm_num) (cellSig c5) P5 k6_ell5⟩,
   ⟨cellSig c6, exists_tightened_of_isModel (k := 6) (ell := 6) (by norm_num) (cellSig c6) P6 k6_ell6⟩⟩

/-- The two constraints are both vacuous on m5's own `ell = 6` witness. -/
theorem P6_has_C4_C5 : HasC4 (P6) ∧ HasC5 (P6) := by
  have h2 : ∀ i, (P6 i).card ≤ 2 := by
    intro i; fin_cases i <;> simp [P6]
  exact ⟨c4_of_pair (k := 6) (by norm_num) P6 h2, c5_of_pair (k := 6) (by norm_num) P6 h2⟩

end InterfaceStates

#print axioms InterfaceStates.tightened_silent_at_six
#print axioms PaletteShrink.neutral_of_pair_satisfied
