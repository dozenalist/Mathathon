/-
A6 palette producer, lane A: the finite forcing lemma.

Pure `Fin 6` combinatorics.  `import Mathlib` only: nothing here depends on the
OAI library, and nothing constrains the cardinality of any palette.

Main results
* `A6Forcing.a6_canonical_pairs` -- from the two source hit hypotheses at every
  index `j` plus cyclic adjacent disjointness, every palette `P j` contains the
  forced label `A6f j` and its canonical partner `A6g j = A6f j + 3`.
* `A6Forcing.a6_canonical_pairs_add_three` -- the same conclusion in the literal
  form `A6f j ∈ P j ∧ A6f j + 3 ∈ P j`.
* `A6Forcing.a6_canonical_pairs_of_mem` -- variant with the inner hit given as a
  membership rather than an intersection hit.
* `A6Forcing.a6_hypotheses_satisfiable` -- the three hypotheses are consistent
  (the forcing lemma is not vacuous), witnessed by `A6canonical`.
* `A6Forcing.disjointness_necessary`, `A6Forcing.outer_hit_necessary` -- each
  hypothesis other than the inner one is essential.
* `A6Forcing.a6_containment_unsatisfiable` -- the *containment* reading of the
  source restriction (`A6H j ⊆ P j`) is inconsistent with cyclic adjacent
  disjointness; the source lemmas deliver intersection hits, and the hit form is
  what is used above.

Every closed goal is discharged by `fin_cases j <;> decide` (or `decide` on a
closed statement): the kernel evaluates the table, no native code generation and
no extra axioms are involved.
-/
import Mathlib

set_option autoImplicit false

namespace A6Forcing

/-! ### 1. The A6 source table -/

/-- `f`: the singleton label forced at index `j`, i.e. the residual `J = {f j}`
of the inner restriction (`continuum_inner_restriction` composed with
`finite_support_exclusion_ae`).  Source table: `(1, 5, 3, 1, 5, 3)`. -/
def A6f : Fin 6 → Fin 6 := ![1, 5, 3, 1, 5, 3]

/-- `H`: the labels hit by the other restriction at index `j`, i.e. the residual
`J` of `continuum_outer_restriction` at that index.  Source table:
`({3,4,5}, {1,2,3}, {0,1,5}, {3,4,5}, {1,2,3}, {0,1,5})`. -/
def A6H : Fin 6 → Finset (Fin 6) :=
  ![({3, 4, 5} : Finset (Fin 6)), ({1, 2, 3} : Finset (Fin 6)), ({0, 1, 5} : Finset (Fin 6)),
    ({3, 4, 5} : Finset (Fin 6)), ({1, 2, 3} : Finset (Fin 6)), ({0, 1, 5} : Finset (Fin 6))]

/-- `g`: the canonical partner forced as the second label.  Source table:
`(4, 2, 0, 4, 2, 0)`, which is `f j + 3` mod 6. -/
def A6g : Fin 6 → Fin 6 := ![4, 2, 0, 4, 2, 0]

/-! ### 2. Closed arithmetic of the table -/

/-- The canonical partner is the source's `f j + 3` (mod 6). -/
theorem A6f_add_three (j : Fin 6) : A6f j + 3 = A6g j := by
  fin_cases j <;> decide

/-- The label forced by the forcing step lies among the other hits. -/
theorem A6g_mem_A6H (j : Fin 6) : A6g j ∈ A6H j := by
  fin_cases j <;> decide

/-- The forcing arithmetic: after the two neighbouring forced labels are removed
from the other hits, exactly the canonical partner remains.  This is the whole
content of the forcing step, and it needs no cardinality information. -/
theorem A6H_sdiff (j : Fin 6) :
    A6H j \ ({A6f (j - 1), A6f (j + 1)} : Finset (Fin 6)) = {A6g j} := by
  fin_cases j <;> decide

/-- Cyclic bookkeeping: stepping one index back and then one forward returns the
index (`j - 1` is taken in `Fin 6`, so at `j = 0` it is `5`). -/
theorem A6_pred_succ (j : Fin 6) : (j - 1) + 1 = j := by
  fin_cases j <;> decide

theorem A6_zero_add_one : (0 : Fin 6) + 1 = 1 := by decide

/-- An other-hit label that avoids the forced labels of both neighbours must be
the canonical partner. -/
theorem A6_hit_unique (j : Fin 6) {y : Fin 6} (hy : y ∈ A6H j)
    (hprev : y ≠ A6f (j - 1)) (hnext : y ≠ A6f (j + 1)) : y = A6g j := by
  have hmem : y ∈ A6H j \ ({A6f (j - 1), A6f (j + 1)} : Finset (Fin 6)) := by
    refine Finset.mem_sdiff.mpr ⟨hy, ?_⟩
    intro hcon
    rcases Finset.mem_insert.mp hcon with h | h
    · exact hprev h
    · exact hnext (Finset.mem_singleton.mp h)
  rw [A6H_sdiff j] at hmem
  exact Finset.mem_singleton.mp hmem

/-! ### 3. The finite forcing lemma -/

/-- **A6 finite forcing lemma (hit form, faithful to the source).**

`P j` is the palette carried at the `j`-th of the six directions `θ + j * π/3`.

* `hInner` is the task's INNER hit: at index `j` the restriction whose residual set
  is the singleton `{f j}` hits `P j` (`continuum_inner_restriction` at
  `AngularBoundary.lean:279` composed with `finite_support_exclusion_ae` at
  `AngularBoundary.lean:317`).  Which geometric gate supplies this residual varies
  with `j`: recomputing the sign table, the inner (negative-sign) restriction gives
  `{f j}` at even `j` and the non-singleton residual at odd `j`.  The lemma only
  needs both hits at each `j`, so it does not distinguish the gates.
* `hOuter` is the task's OUTER hit: at index `j` the restriction whose residual set
  is `H j` hits `P j` (`continuum_outer_restriction` at
  `AngularBoundary.lean:259`, same composition).  These are intersection hits, not
  containments; see `a6_containment_unsatisfiable` for why the containment reading
  cannot be used.
* `hDisj` formalises `palette_sixty_disjoint` (`PaletteTransport.lean:450`) read
  along the six-step cycle: palettes one sixth-turn apart are disjoint, with
  `j + 1` taken in `Fin 6`, so `j = 5` is disjointness of `P 5` and `P 0`.

Conclusion: at every index both the forced label `f j` and its canonical partner
`f j + 3` lie in `P j`.  No cardinality hypothesis on any palette appears. -/
theorem a6_canonical_pairs (P : Fin 6 → Finset (Fin 6))
    (hInner : ∀ j, (P j ∩ {A6f j}).Nonempty)
    (hOuter : ∀ j, (P j ∩ A6H j).Nonempty)
    (hDisj : ∀ j, Disjoint (P j) (P (j + 1))) :
    ∀ j, A6f j ∈ P j ∧ A6g j ∈ P j := by
  -- the inner hit is a membership at each index, uniformly in the index
  have hfmem : ∀ k : Fin 6, A6f k ∈ P k := by
    intro k
    obtain ⟨z, hz⟩ := hInner k
    obtain ⟨hzP, hzS⟩ := Finset.mem_inter.mp hz
    rw [Finset.mem_singleton] at hzS
    rw [hzS] at hzP
    exact hzP
  intro j
  refine ⟨hfmem j, ?_⟩
  -- the outer hit supplies a label of `H j` inside `P j`
  obtain ⟨y, hy⟩ := hOuter j
  obtain ⟨hyP, hyH⟩ := Finset.mem_inter.mp hy
  -- disjointness with the previous palette removes the previous forced label
  have hleft : y ∉ P (j - 1) := by
    have hd : Disjoint (P (j - 1)) (P j) := by
      have h := hDisj (j - 1)
      rwa [A6_pred_succ j] at h
    exact (Finset.disjoint_right.mp hd) hyP
  -- disjointness with the next palette removes the next forced label
  have hright : y ∉ P (j + 1) := (Finset.disjoint_left.mp (hDisj j)) hyP
  have hnotprev : y ≠ A6f (j - 1) := by
    intro heq
    apply hleft
    rw [heq]
    exact hfmem (j - 1)
  have hnotnext : y ≠ A6f (j + 1) := by
    intro heq
    apply hright
    rw [heq]
    exact hfmem (j + 1)
  -- so `y` is the canonical partner
  have hyg : y = A6g j := A6_hit_unique j hyH hnotprev hnotnext
  rw [hyg] at hyP
  exact hyP

/-- The forcing lemma with the conclusion written as `f j + 3`. -/
theorem a6_canonical_pairs_add_three (P : Fin 6 → Finset (Fin 6))
    (hInner : ∀ j, (P j ∩ {A6f j}).Nonempty)
    (hOuter : ∀ j, (P j ∩ A6H j).Nonempty)
    (hDisj : ∀ j, Disjoint (P j) (P (j + 1))) :
    ∀ j, A6f j ∈ P j ∧ A6f j + 3 ∈ P j := by
  intro j
  obtain ⟨h1, h2⟩ := a6_canonical_pairs P hInner hOuter hDisj j
  refine ⟨h1, ?_⟩
  rw [A6f_add_three j]
  exact h2

/-- The canonical pair at each index is contained in the palette: the canonical
subpalette is included, which is the form a downstream consumer wants. -/
theorem a6_canonical_pair_subset (P : Fin 6 → Finset (Fin 6))
    (hInner : ∀ j, (P j ∩ {A6f j}).Nonempty)
    (hOuter : ∀ j, (P j ∩ A6H j).Nonempty)
    (hDisj : ∀ j, Disjoint (P j) (P (j + 1))) :
    ∀ j, ({A6f j, A6g j} : Finset (Fin 6)) ⊆ P j := by
  intro j
  obtain ⟨h1, h2⟩ := a6_canonical_pairs P hInner hOuter hDisj j
  rw [Finset.insert_subset_iff, Finset.singleton_subset_iff]
  exact ⟨h1, h2⟩

/-- The forcing lemma with the inner hit given in membership form. -/
theorem a6_canonical_pairs_of_mem (P : Fin 6 → Finset (Fin 6))
    (hInner : ∀ j, A6f j ∈ P j)
    (hOuter : ∀ j, (P j ∩ A6H j).Nonempty)
    (hDisj : ∀ j, Disjoint (P j) (P (j + 1))) :
    ∀ j, A6f j ∈ P j ∧ A6g j ∈ P j :=
  a6_canonical_pairs P
    (fun j => ⟨A6f j, Finset.mem_inter.mpr
      ⟨hInner j, Finset.mem_singleton_self (A6f j)⟩⟩)
    hOuter hDisj

/-! ### 4. Non-vacuity -/

/-- The canonical field: palette `{f j, g j}` at every index.  This is the field
`A_{j mod 3}` of the source. -/
def A6canonical : Fin 6 → Finset (Fin 6) := fun j => {A6f j, A6g j}

/-- The canonical field satisfies all three hypotheses of the forcing lemma. -/
theorem A6canonical_hypotheses :
    (∀ j, (A6canonical j ∩ {A6f j}).Nonempty) ∧
      (∀ j, (A6canonical j ∩ A6H j).Nonempty) ∧
        (∀ j, Disjoint (A6canonical j) (A6canonical (j + 1))) := by
  refine ⟨?_, ?_, ?_⟩
  · intro j
    exact ⟨A6f j, Finset.mem_inter.mpr
      ⟨Finset.mem_insert_self (A6f j) ({A6g j} : Finset (Fin 6)),
        Finset.mem_singleton_self (A6f j)⟩⟩
  · intro j
    exact ⟨A6g j, Finset.mem_inter.mpr
      ⟨Finset.mem_insert.mpr (Or.inr (Finset.mem_singleton_self (A6g j))),
        A6g_mem_A6H j⟩⟩
  · intro j
    fin_cases j <;> decide

/-- The hypothesis set of the forcing lemma is consistent, so the lemma is not
vacuous. -/
theorem a6_hypotheses_satisfiable :
    ∃ P : Fin 6 → Finset (Fin 6), (∀ j, (P j ∩ {A6f j}).Nonempty) ∧
      (∀ j, (P j ∩ A6H j).Nonempty) ∧ (∀ j, Disjoint (P j) (P (j + 1))) :=
  ⟨A6canonical, A6canonical_hypotheses.1, A6canonical_hypotheses.2.1,
    A6canonical_hypotheses.2.2⟩

/-! ### 5. Each hypothesis is essential -/

/-- Palettes that satisfy both hit hypotheses but fail adjacent disjointness and
fail the conclusion: `{1,3}` at index `0` keeps `f 0 = 1` and meets
`H 0 = {3,4,5}` in `3`, but misses `g 0 = 4`.  So disjointness cannot be dropped. -/
def A6sharp : Fin 6 → Finset (Fin 6) :=
  ![({1, 3} : Finset (Fin 6)), ({2, 5} : Finset (Fin 6)), ({0, 3} : Finset (Fin 6)),
    ({1, 4} : Finset (Fin 6)), ({2, 5} : Finset (Fin 6)), ({0, 3} : Finset (Fin 6))]

/-- Adjacent disjointness is not redundant. -/
theorem disjointness_necessary :
    (∀ j, (A6sharp j ∩ {A6f j}).Nonempty) ∧
      (∀ j, (A6sharp j ∩ A6H j).Nonempty) ∧ ¬ (∀ j, A6g j ∈ A6sharp j) := by
  refine ⟨?_, ?_, ?_⟩
  · intro j
    fin_cases j <;> decide
  · intro j
    fin_cases j <;> decide
  · decide

/-- The single-label field `{f j}`: inner hit and cyclic adjacent disjointness
hold, the outer hit fails, and so does the conclusion (`g 0 = 4 ∉ {1}`).  So the
outer hit cannot be dropped. -/
def A6singleton : Fin 6 → Finset (Fin 6) := fun j => {A6f j}

/-- The outer hit is not redundant. -/
theorem outer_hit_necessary :
    (∀ j, (A6singleton j ∩ {A6f j}).Nonempty) ∧
      (∀ j, Disjoint (A6singleton j) (A6singleton (j + 1))) ∧
        ¬ (∀ j, A6g j ∈ A6singleton j) := by
  refine ⟨?_, ?_, ?_⟩
  · intro j
    exact ⟨A6f j, Finset.mem_inter.mpr
      ⟨Finset.mem_singleton_self (A6f j), Finset.mem_singleton_self (A6f j)⟩⟩
  · intro j
    fin_cases j <;> decide
  · decide

/-! ### 6. The containment reading is inconsistent -/

/-- The *containment* reading of the source restriction (`H j ⊆ P j`, rather than
`P j` meeting `H j`) is inconsistent with cyclic adjacent disjointness: `f 0 = 1`
is in `P 0` while `1 ∈ H 1` forces `1 ∈ P 1`, and `P 0`, `P 1` are declared
disjoint.  Hence a lemma stated for the containment reading would be vacuous,
which is why the hit form is used above. -/
theorem a6_containment_unsatisfiable (P : Fin 6 → Finset (Fin 6))
    (hInner : ∀ j, A6f j ∈ P j)
    (hOuter : ∀ j, ∀ x ∈ A6H j, x ∈ P j)
    (hDisj : ∀ j, Disjoint (P j) (P (j + 1))) : False := by
  have h0 : (1 : Fin 6) ∈ P 0 := hInner 0
  have h1 : (1 : Fin 6) ∈ P 1 := hOuter 1 1 (by decide)
  have hd : Disjoint (P 0) (P 1) := by
    have h := hDisj 0
    rwa [A6_zero_add_one] at h
  exact (Finset.disjoint_left.mp hd) h0 h1

end A6Forcing
