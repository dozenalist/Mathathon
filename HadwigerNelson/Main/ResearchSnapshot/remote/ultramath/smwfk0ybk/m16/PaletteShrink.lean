/-
  PaletteShrink.lean  (member m16, swarm smwfk0ybk, direction d9)

  Machine-checked core of the calibration finding:

  * (C4) of m6 (complementary-palette exclusion, general k) and
  * (C5) of m6 (at most three palettes of size k-3)
  are SATISFIABILITY-NEUTRAL over the m5 interface system (C1)-(C3) for every k >= 6:
  any model can be shrunk, palette by palette, so that every palette has at most
  two elements, and on that stratum both (C4) and (C5) are vacuous.

  Main theorem `neutral_of_pair_satisfied` is stated for an ARBITRARY constraint
  `Phi` that is satisfied by every six-tuple of palettes of size <= 2. That is the
  exact class of constraints which the shrink argument discards; (C4) and (C5) are
  two members of it (`c4_of_pair`, `c5_of_pair`).
-/
import Mathlib

namespace PaletteShrink

open Finset

/-- Successor in the six-cycle of directions. -/
def next6 (i : Fin 6) : Fin 6 := ⟨(i.val + 1) % 6, Nat.mod_lt _ (by norm_num)⟩

/-- **Shrink lemma.** A finite set meeting both `O` and `I` has a subset of at most
two elements meeting both. -/
lemma exists_small_subset {α : Type*} [DecidableEq α] (P O I : Finset α)
    (hP : 1 ≤ P.card) (hO : (P ∩ O).Nonempty) (hI : (P ∩ I).Nonempty) :
    ∃ Q : Finset α, Q ⊆ P ∧ Q.card ≤ 2 ∧ (Q ∩ O).Nonempty ∧ (Q ∩ I).Nonempty := by
  by_cases h2 : P.card ≤ 2
  · exact ⟨P, subset_rfl, h2, hO, hI⟩
  · push_neg at h2
    obtain ⟨o, ho⟩ := hO
    obtain ⟨n, hn⟩ := hI
    rw [mem_inter] at ho hn
    have h3 : 3 ≤ P.card := h2
    -- a second element of `P` different from `o`
    have hero : 0 < (P.erase o).card := by
      rw [card_erase_of_mem ho.1]; omega
    obtain ⟨w, hw⟩ := card_pos.mp hero
    rw [mem_erase] at hw
    by_cases hon : o = n
    · refine ⟨{o, w}, ?_, ?_, ?_, ?_⟩
      · intro x hx
        rcases mem_insert.mp hx with rfl | hx
        · exact ho.1
        · rw [mem_singleton] at hx
          exact hx ▸ hw.2
      · rw [card_insert_of_notMem (by rw [mem_singleton]; exact fun h => hw.1 h.symm),
          card_singleton]
      · exact ⟨o, by simp [ho.2]⟩
      · exact ⟨o, by simp [hon ▸ hn.2]⟩
    · refine ⟨{o, n}, ?_, ?_, ?_, ?_⟩
      · intro x hx
        rcases mem_insert.mp hx with rfl | hx
        · exact ho.1
        · rw [mem_singleton] at hx
          exact hx ▸ hn.1
      · rw [card_insert_of_notMem (by simp [hon]), card_singleton]
      · exact ⟨o, by simp [ho.2]⟩
      · exact ⟨n, by simp [hn.2]⟩

/-- A union of two at-most-2-element palettes cannot be all of `Fin k` when `k ≥ 6`. -/
lemma union_ne_univ {k : ℕ} (hk : 6 ≤ k) (A B : Finset (Fin k))
    (hA : A.card ≤ 2) (hB : B.card ≤ 2) : A ∪ B ≠ univ := by
  intro h
  have hc : (A ∪ B).card = k := by rw [h, card_univ, Fintype.card_fin]
  have := card_union_le A B
  omega

/-- A palette of at most two elements is never of the maximal size `k-3` when `k ≥ 6`. -/
lemma card_ne_top {k : ℕ} (hk : 6 ≤ k) (A : Finset (Fin k)) (hA : A.card ≤ 2) :
    A.card ≠ k - 3 := by omega

/-- (C4) holds on every tuple of palettes of size at most 2, for `k ≥ 6`. -/
lemma c4_of_pair {k : ℕ} (hk : 6 ≤ k) (Q : Fin 6 → Finset (Fin k))
    (hQ : ∀ i, (Q i).card ≤ 2) : ∀ i j, Q i ∪ Q j ≠ univ := by
  intro i j
  exact union_ne_univ hk _ _ (hQ i) (hQ j)

/-- (C5) holds on every tuple of palettes of size at most 2, for `k ≥ 6`. -/
lemma c5_of_pair {k : ℕ} (hk : 6 ≤ k) (Q : Fin 6 → Finset (Fin k))
    (hQ : ∀ i, (Q i).card ≤ 2) :
    ∀ S : Finset (Fin 6), (∀ i ∈ S, (Q i).card = k - 3) → S.card ≤ 3 := by
  intro S hS
  have hempty : S = ∅ := by
    by_contra hne
    obtain ⟨i, hi⟩ := nonempty_iff_ne_empty.mpr hne
    exact card_ne_top hk _ (hQ i) (hS i hi)
  rw [hempty, card_empty]; omega

/-- **Neutrality theorem.** Let `k ≥ 6`, let `O`, `I` be any sliver data (the m5 encoding of
Lemma 8.1), and let `Phi` be any constraint on six palettes that is satisfied by every
six-tuple of palettes of size at most two. Then the m5 interface system (C1)-(C3) has a
model satisfying `Phi` as soon as it has any model at all.

Thus no member of this class -- which contains m6's (C4) and (C5) -- can turn a satisfiable
interface instance into an unsatisfiable one, at any k ≥ 6. -/
theorem neutral_of_pair_satisfied {k : ℕ} (hk : 6 ≤ k)
    (O I : Fin 6 → Finset (Fin k)) (Phi : (Fin 6 → Finset (Fin k)) → Prop)
    (hPhi : ∀ Q, (∀ i, (Q i).card ≤ 2) → Phi Q)
    (P : Fin 6 → Finset (Fin k))
    (h1 : ∀ i, 1 ≤ (P i).card) (hub : ∀ i, (P i).card ≤ k - 3)
    (hO : ∀ i, (P i ∩ O i).Nonempty) (hI : ∀ i, (P i ∩ I i).Nonempty)
    (h3 : ∀ i, Disjoint (P i) (P (next6 i))) :
    ∃ Q : Fin 6 → Finset (Fin k),
      (∀ i, 1 ≤ (Q i).card) ∧ (∀ i, (Q i).card ≤ k - 3) ∧
      (∀ i, (Q i ∩ O i).Nonempty) ∧ (∀ i, (Q i ∩ I i).Nonempty) ∧
      (∀ i, Disjoint (Q i) (Q (next6 i))) ∧ Phi Q := by
  classical
  have hchoice : ∀ i, ∃ Q : Finset (Fin k), Q ⊆ P i ∧ Q.card ≤ 2 ∧
      (Q ∩ O i).Nonempty ∧ (Q ∩ I i).Nonempty :=
    fun i => exists_small_subset (P i) (O i) (I i) (h1 i) (hO i) (hI i)
  choose Q hQsub hQ2 hQO hQI using hchoice
  refine ⟨Q, fun i => ?_, fun i => ?_, hQO, hQI, fun i => ?_, hPhi Q hQ2⟩
  · have hne : (Q i).Nonempty := (hQO i).mono (fun x hx => (mem_inter.mp hx).1)
    have := card_pos.mpr hne
    omega
  · have : (Q i).card ≤ 2 := hQ2 i
    omega
  · exact Disjoint.mono (hQsub i) (hQsub (next6 i)) (h3 i)

/-- Instance: the conjunction of m6's (C4) and (C5) is neutral. -/
theorem neutral_c4_c5 {k : ℕ} (hk : 6 ≤ k) (O I : Fin 6 → Finset (Fin k))
    (P : Fin 6 → Finset (Fin k))
    (h1 : ∀ i, 1 ≤ (P i).card) (hub : ∀ i, (P i).card ≤ k - 3)
    (hO : ∀ i, (P i ∩ O i).Nonempty) (hI : ∀ i, (P i ∩ I i).Nonempty)
    (h3 : ∀ i, Disjoint (P i) (P (next6 i))) :
    ∃ Q : Fin 6 → Finset (Fin k),
      (∀ i, 1 ≤ (Q i).card) ∧ (∀ i, (Q i).card ≤ k - 3) ∧
      (∀ i, (Q i ∩ O i).Nonempty) ∧ (∀ i, (Q i ∩ I i).Nonempty) ∧
      (∀ i, Disjoint (Q i) (Q (next6 i))) ∧
      (∀ i j, Q i ∪ Q j ≠ univ) ∧
      (∀ S : Finset (Fin 6), (∀ i ∈ S, (Q i).card = k - 3) → S.card ≤ 3) :=
  neutral_of_pair_satisfied hk O I
    (fun Q => (∀ i j, Q i ∪ Q j ≠ univ) ∧
      (∀ S : Finset (Fin 6), (∀ i ∈ S, (Q i).card = k - 3) → S.card ≤ 3))
    (fun Q hQ => ⟨c4_of_pair hk Q hQ, c5_of_pair hk Q hQ⟩)
    P h1 hub hO hI h3

end PaletteShrink
