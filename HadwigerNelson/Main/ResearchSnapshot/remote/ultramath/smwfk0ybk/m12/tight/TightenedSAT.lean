import InterfaceStates

/-! ### The tightened CSP at k = 6 is SATISFIABLE, for every sign matrix, at ell = 3 and 4.

`InterfaceStates.k6_ell3` / `k6_ell4` exhibit, for *every* sign matrix `σ`, the alternating
palette `altPal a b` = {a},{b},{a},{b},{a},{b} with a, b outsider labels.  Every palette is a
singleton, so the two orbit-level tightenings of the previous run hold trivially:

  (C4) pair exclusion: no two of the six palettes cover all k labels,
  (C5) orbit bound:    at most three of the six palettes are ternary.

Hence the answer to the brief's decisive question at k = 6 is YES: no UNSAT, so the tightened
interface CSP cannot yield chi(R^2) >= 7.  (The induction lemma is irrelevant to this: a model
of the tightened CSP exists whether or not the lemma is true.) -/

namespace InterfaceStates

/-- (C4) at the orbit level: no two of the six palettes cover all k labels. -/
def C4 (P : Fin 6 → Finset (Fin 6)) : Prop :=
  ∀ i j : Fin 6, i ≠ j → P i ∪ P j ≠ Finset.univ

/-- (C5) at the orbit level: at most three of the six palettes are ternary. -/
def C5 (P : Fin 6 → Finset (Fin 6)) : Prop :=
  ∀ S : Finset (Fin 6), (∀ i ∈ S, (P i).card = 3) → S.card ≤ 3

theorem altPal_card_one (a b : Fin 6) : ∀ i : Fin 6, (altPal a b i).card = 1 := by
  intro i; fin_cases i <;> simp [altPal]

theorem altPal_C4 (a b : Fin 6) (hab : a ≠ b) : C4 (altPal a b) := by
  intro i j hij h
  have hsub : (altPal a b i) ⊆ ({a, b} : Finset (Fin 6)) := by
    fin_cases i <;> simp [altPal]
  have hsub' : (altPal a b j) ⊆ ({a, b} : Finset (Fin 6)) := by
    fin_cases j <;> simp [altPal]
  have hunion : (altPal a b i) ∪ (altPal a b j) ⊆ ({a, b} : Finset (Fin 6)) :=
    Finset.union_subset hsub hsub'
  rw [h] at hunion
  have hc := Finset.card_le_card hunion
  simp [hab] at hc

theorem altPal_C5 (a b : Fin 6) : C5 (altPal a b) := by
  intro S hS
  have h : ∀ i : Fin 6, (altPal a b i).card = 1 := altPal_card_one a b
  have hzero : S.card = 0 := by
    rcases Finset.eq_empty_or_nonempty S with h0 | ⟨i, hi⟩
    · simp [h0]
    · have h3 := hS i hi
      rw [h i] at h3
      exact absurd h3 (by norm_num)
  omega

/-- **Decisive**: at k = 6, ell = 3, for EVERY sign matrix there is a model of (C1)-(C5). -/
theorem tightened_sat_k6_ell3 (σ : Sig 3) :
    ∃ P : Fin 6 → Finset (Fin 6), IsModel σ P ∧ C4 P ∧ C5 P :=
  ⟨altPal ⟨3, by norm_num⟩ ⟨4, by norm_num⟩, k6_ell3 σ,
   altPal_C4 _ _ (by decide), altPal_C5 _ _⟩

/-- **Decisive**: at k = 6, ell = 4, for EVERY sign matrix there is a model of (C1)-(C5). -/
theorem tightened_sat_k6_ell4 (σ : Sig 4) :
    ∃ P : Fin 6 → Finset (Fin 6), IsModel σ P ∧ C4 P ∧ C5 P :=
  ⟨altPal ⟨4, by norm_num⟩ ⟨5, by norm_num⟩, k6_ell4 σ,
   altPal_C4 _ _ (by decide), altPal_C5 _ _⟩

#print axioms tightened_sat_k6_ell3
#print axioms tightened_sat_k6_ell4

end InterfaceStates
