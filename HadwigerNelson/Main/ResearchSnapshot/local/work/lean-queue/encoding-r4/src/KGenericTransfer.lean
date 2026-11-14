/-
  k-GENERIC NULL-SET TRANSFER LEMMA (upper-bound direction).
  Status: COMPLETE SOURCE, UNCOMPILED. No Lean was run in this block; the tree is frozen
  and its dependency build was still in progress.

  Transcribed mechanically from the `hfin` block of
  `theorem not_proper_five_coloring_compl_null` in
  lean/OAI/Geometry/PlaneColoring/NullSetRobust.lean:20
  with exactly two edits:
    (i)  `Fin 5` -> `Fin k` in the type of `hfin` and in the statement;
    (ii) the final `exact no_proper_five_coloring (...)` is replaced by
         `exact exists_properColoring_of_finset hfin`.
  Nothing else is changed: the proof body of `hfin` is copied verbatim, including binder
  names and the `by ring` / `by positivity` closers. The body never mentions `Fin` at all,
  so it is type-generic as written and the `Fin 5 -> Fin k` edit touches only the statement.

  `Five` is NOT imported, and the theorem being generalised is not re-derived.
-/
import OAI.Geometry.PlaneColoring.Converse
-- `Converse` imports `States` -> `BinaryPalettes` -> ... -> `Coloring` -> `Mathlib`.
-- `Five` (lean/OAI/Geometry/PlaneColoring/Five.lean) is imported only by CyclicCore,
-- Chromatic and NullSetRobust, so this module does not reach it.

namespace OAI
noncomputable section
open MeasureTheory
namespace EuclideanFiveColor

/-- **Null-set transfer, upper-bound direction.** If `Z` is Lebesgue-null and `c` is a proper
`k`-colouring of `ℂ \ Z` (i.e. it separates every unit pair that avoids `Z`, and nothing is
asserted about pairs meeting `Z`), then the whole plane has a proper `k`-colouring.

Note what the conclusion is and is not: it produces *some* global colouring, and there is no
reason for that colouring to agree with `c` on `ℂ \ Z`. The argument is the finite
characterisation: every finite configuration can be translated off `Z`, since the bad
translations form a finite union of null sets; so every finite unit-distance graph is
`k`-colourable, and `exists_properColoring_of_finset` (de Bruijn–Erdős / Tychonoff) concludes.

The lower-bound counterpart is `not_proper_five_coloring_compl_null` (`k = 5`, contrapositive). -/
theorem exists_properColoring_of_compl_null {k : ℕ} [NeZero k] {Z : Set ℂ}
    (hZ : volume Z = 0) (c : ℂ → Fin k)
    (hc : ∀ x ∉ Z, ∀ y ∉ Z, ‖x - y‖ = 1 → c x ≠ c y) :
    ∃ d : ℂ → Fin k, ProperColoring k d := by
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
        · intro h; exact ⟨w + x, h, by ring⟩
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
      by_contra h
      exact hne (Set.eq_univ_of_forall fun v => by by_contra hv; exact h ⟨v, hv⟩)
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

end EuclideanFiveColor
end
end OAI

#print axioms OAI.EuclideanFiveColor.exists_properColoring_of_compl_null
