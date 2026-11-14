import OAI.Geometry.PlaneColoring.Converse
import OAI.Geometry.PlaneColoring.Five

namespace OAI

noncomputable section
open MeasureTheory
namespace EuclideanFiveColor

/-- **The lower bound survives deleting any Lebesgue-null set.**

If `Z` has measure zero, the induced unit-distance graph on `ℂ \ Z` still has no proper
5-colouring. Equivalently, every 6-colouring of the plane would have to use the points of `Z`:
no null set can be discarded to simplify the problem.

The proof is the finite characterisation: every finite configuration can be translated off `Z`
(the bad translations form a finite union of null sets), so a 5-colouring of `ℂ \ Z` would give
one of every finite configuration, hence — by compactness — one of the plane, contradicting
`no_proper_five_coloring`. -/
theorem not_proper_five_coloring_compl_null {Z : Set ℂ} (hZ : volume Z = 0) :
    ¬ ∃ c : ℂ → Fin 5, ∀ x ∉ Z, ∀ y ∉ Z, ‖x - y‖ = 1 → c x ≠ c y := by
  rintro ⟨c, hc⟩
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
  have hfin : ∀ F : Finset ℂ, ∃ d : ℂ → Fin 5,
      ∀ x ∈ F, ∀ y ∈ F, ‖x - y‖ = 1 → d x ≠ d y := by
    intro F
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
  exact no_proper_five_coloring (exists_properColoring_of_finset hfin)

end EuclideanFiveColor
end

end OAI
