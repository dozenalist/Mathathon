/-
  MINIMAL SELF-CONTAINED LOCAL-CHECK PACKET: the k-generic null-set transfer lemma.
  Status: COMPLETE SOURCE, UNCOMPILED. No Lean run in this block.

  Goal: test the genuine generic fact WITHOUT pulling the weak-colouring machinery.
  `import OAI.Geometry.PlaneColoring.Converse` needs 17 OAI modules; we do not import it.
  `OAI.Geometry.PlaneColoring.Coloring` is a leaf: its only import is `Mathlib`, and it
  supplies the exact in-tree predicate. So this file needs Mathlib + 1 leaf module.

  Fallback if that leaf is not yet built: replace the import below by `import Mathlib` and
  paste, verbatim from Coloring.lean:7-8,

      def ProperColoring (k : ℕ) (c : ℂ → Fin k) : Prop :=
        ∀ x y : ℂ, ‖x - y‖ = 1 → c x ≠ c y

  inside this namespace and drop the `OAI.EuclideanFiveColor.` qualifiers. Nothing else
  changes: the two lemmas below never use any other in-tree constant.

  Contents:
    1. `exists_properColoring_of_finset` - the FINITE-COMPACTNESS step, extracted verbatim
       from Converse.lean:33-70 (de Bruijn-Erdos / Tychonoff). This is the only in-tree
       ingredient needed; extracting it removes the 17-module dependency.
    2. `null_transfer` - the null-set transfer lemma, proof transcribed from
       NullSetRobust.lean:20's `hfin` block with `Fin 5 -> Fin k` and the final `exact` line
       replaced. `Five` and `no_proper_five_coloring` are NOT imported and NOT reproved.

  Correspondence to the in-tree results, precisely:
    * `exists_properColoring_of_finset` here has the SAME statement as
      `OAI.EuclideanFiveColor.exists_properColoring_of_finset` (Converse.lean:33), and its
      proof is a verbatim extraction. It is a copy, so it is a re-check of that step, not a
      new theorem.
    * `null_transfer` here is the k-generic form of
      `OAI.EuclideanFiveColor.not_proper_five_coloring_compl_null` (NullSetRobust.lean:20).
      The latter is the k = 5 contrapositive plus `no_proper_five_coloring`; the generic
      statement is the k-arbitrary positive form. Both conclusions are stated in terms of the
      SAME in-tree predicate `OAI.EuclideanFiveColor.ProperColoring`, so no translation of
      meaning is involved.
-/
import OAI.Geometry.PlaneColoring.Coloring

namespace NullTransferCheck

open MeasureTheory Set

/-! ### 1. The finite-compactness step, extracted from `Converse.lean:33`

Statement identical to the in-tree `exists_properColoring_of_finset`; proof transcribed
verbatim, including binder names (`t`, `ht`, `hfip`, `hcomp`) and every tactic. -/
theorem exists_properColoring_of_finset {k : ℕ} [NeZero k]
    (h : ∀ F : Finset ℂ, ∃ c : ℂ → Fin k,
      ∀ x ∈ F, ∀ y ∈ F, ‖x - y‖ = 1 → c x ≠ c y) :
    ∃ c : ℂ → Fin k, OAI.EuclideanFiveColor.ProperColoring k c := by
  classical
  letI : CompactSpace (ℂ → Fin k) := Pi.compactSpace
  let t : ℂ × ℂ → Set (ℂ → Fin k) := fun p =>
    {c | c p.1 ≠ c p.2} ∪ {c | ¬ ‖p.1 - p.2‖ = 1}
  have ht : ∀ p, IsClosed (t p) := by
    intro p
    apply IsClosed.union
    · have hcont : Continuous (fun c : ℂ → Fin k => (c p.1, c p.2)) :=
        (continuous_apply p.1).prodMk (continuous_apply p.2)
      exact (isClosed_discrete {q : Fin k × Fin k | q.1 ≠ q.2}).preimage hcont
    · by_cases hd : ‖p.1 - p.2‖ = 1 <;> simp [hd]
  have hfip : ∀ u : Finset (ℂ × ℂ), (⋂ p ∈ u, t p).Nonempty := by
    intro u
    obtain ⟨c, hc⟩ := h (u.image Prod.fst ∪ u.image Prod.snd)
    refine ⟨c, ?_⟩
    simp only [mem_iInter, t]
    intro p hp
    have h1 : p.1 ∈ u.image Prod.fst ∪ u.image Prod.snd :=
      Finset.mem_union_left _ (Finset.mem_image_of_mem _ hp)
    have h2 : p.2 ∈ u.image Prod.fst ∪ u.image Prod.snd :=
      Finset.mem_union_right _ (Finset.mem_image_of_mem _ hp)
    by_cases hd : ‖p.1 - p.2‖ = 1
    · left
      exact hc p.1 h1 p.2 h2 hd
    · right; exact hd
  have hcomp : IsCompact (Set.univ : Set (ℂ → Fin k)) := isCompact_univ
  obtain ⟨c, -, hc⟩ := hcomp.inter_iInter_nonempty t ht (fun u => by simpa using hfip u)
  refine ⟨c, fun x y hxy => ?_⟩
  simp only [Set.mem_iInter] at hc
  have h1 : c ∈ t (x, y) := hc (x, y)
  simp only [t, mem_union] at h1
  rcases h1 with h1 | h1
  · exact h1
  · exact absurd hxy h1

/-! ### 2. The k-generic null-set transfer lemma

Assumptions preserved in full: `Z` is Lebesgue-null (`volume Z = 0`), `k` is nonzero, `c` is an
arbitrary (not assumed measurable, not assumed regular) `ℂ → Fin k`, constrained only on pairs
that avoid `Z`. The conclusion is existence of *some* proper `k`-colouring of the plane; it is
NOT claimed to extend `c` on `ℂ \ Z`. -/
theorem null_transfer {k : ℕ} [NeZero k] {Z : Set ℂ} (hZ : volume Z = 0) (c : ℂ → Fin k)
    (hc : ∀ x ∉ Z, ∀ y ∉ Z, ‖x - y‖ = 1 → c x ≠ c y) :
    ∃ d : ℂ → Fin k, OAI.EuclideanFiveColor.ProperColoring k d := by
  classical
  have hfin : ∀ F : Finset ℂ, ∃ d : ℂ → Fin k,
      ∀ x ∈ F, ∀ y ∈ F, ‖x - y‖ = 1 → d x ≠ d y := by
    intro F
    have hsingle : ∀ x : ℂ, volume ((fun z : ℂ => z - x) '' Z) = 0 := by
      intro x
      have heq : (fun z : ℂ => z - x) '' Z = (fun w : ℂ => w + x) ⁻¹' Z := by
        ext w
        simp only [Set.mem_image, Set.mem_preimage]
        constructor
        · rintro ⟨z, hz, rfl⟩; simpa using hz
        · intro hh; exact ⟨w + x, hh, by ring⟩
      rw [heq, measure_preimage_add_right]
      exact hZ
    have hbad : volume (⋃ x ∈ (F : Set ℂ), (fun z : ℂ => z - x) '' Z) = 0 := by
      induction F using Finset.induction_on with
      | empty => simp
      | insert a s ha ih =>
        rw [Finset.coe_insert, Set.biUnion_insert]
        exact measure_union_null (hsingle a) ih
    have hne : (⋃ x ∈ (F : Set ℂ), (fun z : ℂ => z - x) '' Z) ≠ Set.univ := by
      intro hall
      have hzero : volume (Set.univ : Set ℂ) = 0 := by rw [← hall]; exact hbad
      have hpos : 0 < volume (Metric.ball (0 : ℂ) 1) := Metric.measure_ball_pos volume 0 zero_lt_one
      have hle : volume (Metric.ball (0 : ℂ) 1) ≤ volume (Set.univ : Set ℂ) :=
        measure_mono (Set.subset_univ _)
      rw [hzero] at hle
      exact hpos.ne' (le_antisymm hle (by positivity))
    obtain ⟨v, hv⟩ : ∃ v, v ∉ ⋃ x ∈ (F : Set ℂ), (fun z : ℂ => z - x) '' Z := by
      by_contra hcontra
      exact hne (Set.eq_univ_of_forall fun v => by by_contra hv; exact hcontra ⟨v, hv⟩)
    refine ⟨fun x => c (x + v), ?_⟩
    intro x hx y hy hxy
    have hxZ : x + v ∉ Z := by
      intro hmem
      exact hv (Set.mem_biUnion hx ⟨x + v, hmem, by ring⟩)
    have hyZ : y + v ∉ Z := by
      intro hmem
      exact hv (Set.mem_biUnion hy ⟨y + v, hmem, by ring⟩)
    exact hc (x + v) hxZ (y + v) hyZ (by simpa only [add_sub_add_right_eq_sub] using hxy)
  exact exists_properColoring_of_finset hfin

end NullTransferCheck

#print axioms NullTransferCheck.exists_properColoring_of_finset
#print axioms NullTransferCheck.null_transfer
