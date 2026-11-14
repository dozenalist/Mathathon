/-
  Shrink.lean  --  the combinatorial core of "the tightened interface CSP at k = 6 is
  vacuously satisfied", machine-checked.  Member m10, direction d2
  (see work/STEP1-VACUITY.md, Theorem B).

  Content.
  * `shrink` (Lemma B0): a palette meeting both allowed sets O, I contains a sub-palette of
    at most two labels meeting both.  No palette bound, no sign matrix, no cycle length and
    no colouring enters: O, I are arbitrary finite sets.
  * `binary_model`: any six palettes satisfying (C2) P_i meets O_i and I_i and
    (C3) P_i disjoint P_{i+1} can be replaced by six palettes satisfying (C1) 1 <= |Q_i| <= 3,
    (C2), (C3), and additionally |Q_i| <= 2 for every i.
  * `tightened_model`: with |Q_i| <= 2, (C4) (no two palettes cover Fin 6, hence no two are
    complementary 3-sets) and (C5) (at most three ternary positions) hold.

  So at k = 6:  (C1)-(C3) satisfiable  ==>  (C1)-(C5) satisfiable, for every cycle length
  and every sign matrix -- and the proof never uses the sign matrix, only that O_i and I_i
  are met.  Check:  lean work/Shrink.lean
-/
import Mathlib

open Finset

variable {α : Type*} [DecidableEq α]

/-- Lemma B0.  A palette meeting both `O` and `I` has a sub-palette of at most two labels
meeting both: either one label does the job, or two do.  (No upper palette bound needed.) -/
theorem shrink {O I P : Finset α} (hO : (P ∩ O).Nonempty) (hI : (P ∩ I).Nonempty) :
    ∃ Q : Finset α, Q ⊆ P ∧ Q.Nonempty ∧ (Q ∩ O).Nonempty ∧ (Q ∩ I).Nonempty ∧
      Q.card ≤ 2 := by
  obtain ⟨a, ha⟩ := hO
  obtain ⟨b, hb⟩ := hI
  rw [mem_inter] at ha hb
  by_cases hcommon : (P ∩ O ∩ I).Nonempty
  · obtain ⟨c, hc⟩ := hcommon
    obtain ⟨hcP, hcO, hcI⟩ : c ∈ P ∧ c ∈ O ∧ c ∈ I := by
      rw [mem_inter, mem_inter] at hc
      exact ⟨hc.1.1, hc.1.2, hc.2⟩
    refine ⟨{c}, ?_, ⟨c, mem_singleton_self c⟩, ?_, ?_, by simp⟩
    · intro x hx
      rw [mem_singleton] at hx
      exact hx ▸ hcP
    · exact ⟨c, by rw [mem_inter]; exact ⟨mem_singleton_self c, hcO⟩⟩
    · exact ⟨c, by rw [mem_inter]; exact ⟨mem_singleton_self c, hcI⟩⟩
  · -- no common label: `a` witnesses O only, `b` witnesses I only
    have hne_ab : a ≠ b := by
      intro hab
      apply hcommon
      exact ⟨a, by rw [mem_inter, mem_inter]; exact ⟨⟨ha.1, ha.2⟩, hab ▸ hb.2⟩⟩
    refine ⟨{a, b}, ?_, ?_, ?_, ?_, ?_⟩
    · intro x hx
      rw [mem_insert, mem_singleton] at hx
      exact hx.elim (fun h => h ▸ ha.1) (fun h => h ▸ hb.1)
    · exact ⟨a, mem_insert_self a {b}⟩
    · exact ⟨a, by rw [mem_inter]; exact ⟨mem_insert_self a {b}, ha.2⟩⟩
    · exact ⟨b, by rw [mem_inter]; exact ⟨mem_insert_of_mem (mem_singleton_self b), hb.2⟩⟩
    · rw [card_insert_of_notMem (by simpa using hne_ab), card_singleton]

section Six

/-- Theorem B at the model level, `k = 6`: palettes meeting their allowed sets with
consecutive disjointness can be shrunk so that every palette has at most two labels, keeping
`(C1)`, `(C2)` and `(C3)`. -/
theorem binary_model {O I P : Fin 6 → Finset (Fin 6)}
    (hO : ∀ i, ((P i) ∩ O i).Nonempty)
    (hI : ∀ i, ((P i) ∩ I i).Nonempty)
    (h3 : ∀ i : Fin 6, Disjoint (P i) (P (i + 1))) :
    ∃ Q : Fin 6 → Finset (Fin 6),
      (∀ i, 1 ≤ (Q i).card) ∧ (∀ i, (Q i).card ≤ 3) ∧ (∀ i, (Q i).card ≤ 2) ∧
      (∀ i, ((Q i) ∩ O i).Nonempty) ∧ (∀ i, ((Q i) ∩ I i).Nonempty) ∧
      (∀ i : Fin 6, Disjoint (Q i) (Q (i + 1))) := by
  choose Q hQsub hQne hQO hQI hQ2 using fun i => shrink (hO i) (hI i)
  refine ⟨Q, fun i => card_pos.mpr (hQne i), fun i => by have := hQ2 i; omega, hQ2, hQO, hQI,
    fun i => (h3 i).mono (hQsub i) (hQsub (i + 1))⟩

/-- (C4) at `k = 6`: with all palettes of size at most two, no two of them cover the six
labels, so no two are complementary 3-sets. -/
theorem no_complementary {Q : Fin 6 → Finset (Fin 6)} (h : ∀ i, (Q i).card ≤ 2)
    (i j : Fin 6) : Q i ∪ Q j ≠ univ := by
  intro hU
  have hc := card_union_le (Q i) (Q j)
  rw [hU, card_univ, Fintype.card_fin] at hc
  have hi := h i
  have hj := h j
  omega

/-- (C5) at `k = 6`: with all palettes of size at most two, at most three of the six orbit
palettes are ternary (in fact none is). -/
theorem ternary_count_le_three {Q : Fin 6 → Finset (Fin 6)} (h : ∀ i, (Q i).card ≤ 2) :
    (univ.filter (fun i => (Q i).card = 3)).card ≤ 3 := by
  have hempty : univ.filter (fun i => (Q i).card = 3) = ∅ := by
    apply filter_eq_empty_iff.mpr
    intro i _ hi
    have := h i
    omega
  rw [hempty]
  simp

/-- **Theorem B, machine-checked form.**  At `k = 6`, from any palette assignment meeting
`(C2)` at each of the six orbit positions and `(C3)` between consecutive ones, there is an
assignment satisfying `(C1)`, `(C2)`, `(C3)`, `(C4)` and `(C5)` simultaneously. -/
theorem tightened_model {O I P : Fin 6 → Finset (Fin 6)}
    (hO : ∀ i, ((P i) ∩ O i).Nonempty)
    (hI : ∀ i, ((P i) ∩ I i).Nonempty)
    (h3 : ∀ i : Fin 6, Disjoint (P i) (P (i + 1))) :
    ∃ Q : Fin 6 → Finset (Fin 6),
      (∀ i, 1 ≤ (Q i).card ∧ (Q i).card ≤ 3) ∧
      (∀ i, ((Q i) ∩ O i).Nonempty ∧ ((Q i) ∩ I i).Nonempty) ∧
      (∀ i : Fin 6, Disjoint (Q i) (Q (i + 1))) ∧
      (∀ i j : Fin 6, Q i ∪ Q j ≠ univ) ∧
      (univ.filter (fun i => (Q i).card = 3)).card ≤ 3 := by
  obtain ⟨Q, hcard1, hcard3, hcard2, hQO, hQI, hdisj⟩ := binary_model hO hI h3
  exact ⟨Q, fun i => ⟨hcard1 i, hcard3 i⟩, fun i => ⟨hQO i, hQI i⟩, hdisj,
    fun i j => no_complementary hcard2 i j, ternary_count_le_three hcard2⟩

end Six
