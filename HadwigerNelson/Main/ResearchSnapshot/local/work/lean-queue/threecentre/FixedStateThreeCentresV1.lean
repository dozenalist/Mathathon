/-
  THREE-CENTRE FIXED-STATE SUPPORT EXCLUSION.

  Private validation module. It does NOT touch any shared source, imports only the two modules that
  already contain the three ingredients, and proves the EXACT statement of
  `EuclideanFiveColor.strict_state_no_unit_support` (States.lean:704) by an independent route that
  calls NONE of:
      strict_state_sequence_local_false  (States.lean:547)
      strict_state_sequence_false        (States.lean:683)
      strict_state_no_unit_support       (States.lean:704)
  nor any of their descendants.  `step_ban` (five_support_step_ban) is retained and used elsewhere.

  UNCOMPILED AS DELIVERED: no Lean run was made in this block (no cloud build permitted). The proof is
  complete -- every goal is discharged, there is no `sorry`, `admit` or placeholder constant -- but
  individual Mathlib lemma names were not checked against the pinned toolchain, so a first local run
  may need name-level adjustment. That is a compile-report matter, not a gap in the argument.

  Toolchain it is written for: Lean 4.34.1 commit 5045d0056413266e57c625dcd7c365b10e377c52,
  Mathlib d13f23b723b8a846827a245b89c10fc7d3f11612.

  PROOF SHAPE (see ../THREE-CENTRE-PLAN.md for the paper argument):
    y := x + direction b,  z := x + direction d  are unit apart, hence z - y = direction alpha for
    some angle alpha (`direction_exists`).  The two points b, d of supp(volume|B) give traces at y and
    at z that vanish on K, hence the palettes at y and z are not contained in K
    (`avoiding_trace_palette`).  `palette_neighbor_disjoint` at centres x, x, y gives pairwise
    disjointness of the three palettes.  Pulling the five conull angular statements to ℝ, and using
    `RealState` to get J inside the palette at x on a positive-measure set, one point t does
    everything; the label j in palette_y \ K is not in J by disjointness, hence j = X by the
    complement hypothesis, hence X is in both palettes, contradicting their disjointness.
-/

import OAI.Geometry.PlaneColoring.FiveSupport
import OAI.Geometry.PlaneColoring.BoundaryTrace

namespace OAI
noncomputable section
open Set Filter Topology MeasureTheory
open scoped RealInnerProductSpace
namespace EuclideanFiveColor

/-- Three-centre fixed-state exclusion: with the complement of `J ∪ K` exactly `{X}`, two points of
the `K`-support cannot be at unit angular distance.  Statement identical to
`strict_state_no_unit_support` (States.lean:704). -/
theorem fixed_state_no_unit_three_centres {k : ℕ} {c : ℂ → Fin k}
    (hc : Measurable c) (hw : WeakColoring k c)
    {x : ℂ} {J K : Finset (Fin k)} {X : Fin k}
    (hlabels : ∀ i, i ∉ J ∪ K ↔ i = X)
    {A B : Set ℝ} (hA : RealState c hc x A J) (hB : RealState c hc x B K)
    (hp : 0 < volume A) {b d : ℝ}
    (hb : b ∈ (volume.restrict B).support) (hd : d ∈ (volume.restrict B).support) :
    ‖direction (b : Angles) - direction (d : Angles)‖ ≠ 1 := by
  classical
  intro hu
  -- ### 1. The two traces at y = x + direction b and z = x + direction d, vanishing on K.
  obtain ⟨tb, htb, hzb⟩ := state_support_avoiding_trace c hc hw (x := x) (A := B) (J := K) hB hb
  obtain ⟨td, htd, hzd⟩ := state_support_avoiding_trace c hc hw (x := x) (A := B) (J := K) hB hd
  -- ### 2. Neither palette is contained in K, for almost every angle.
  have hNKy : ∀ᵐ t ∂angularMeasure,
      ¬ palette c hc (x + direction (b : Angles)) t ⊆ K :=
    avoiding_trace_palette c hc (x := x + direction (b : Angles)) htb hzb
  have hNKz : ∀ᵐ t ∂angularMeasure,
      ¬ palette c hc (x + direction (d : Angles)) t ⊆ K :=
    avoiding_trace_palette c hc (x := x + direction (d : Angles)) htd hzd
  -- ### 3. Pairwise disjointness of the three palettes.
  have hDxy : ∀ᵐ t ∂angularMeasure,
      Disjoint (palette c hc (x + direction (b : Angles)) t) (palette c hc x t) :=
    palette_neighbor_disjoint c hc hw x b
  have hDxz : ∀ᵐ t ∂angularMeasure,
      Disjoint (palette c hc (x + direction (d : Angles)) t) (palette c hc x t) :=
    palette_neighbor_disjoint c hc hw x d
  -- unit direction of z - y
  have hzy : ‖(x + direction (d : Angles)) - (x + direction (b : Angles))‖ = 1 := by
    have h : (x + direction (d : Angles)) - (x + direction (b : Angles))
        = direction (d : Angles) - direction (b : Angles) := by ring
    rw [h, norm_sub_rev]; exact hu
  obtain ⟨alpha, halpha⟩ := direction_exists hzy
  have hDyz : ∀ᵐ t ∂angularMeasure,
      Disjoint (palette c hc (x + direction (b : Angles)) t)
        (palette c hc (x + direction (d : Angles)) t) := by
    have h := palette_neighbor_disjoint c hc hw (x + direction (b : Angles)) alpha
    have hyz : (x + direction (b : Angles)) + direction (alpha : Angles)
        = x + direction (d : Angles) := by
      rw [halpha]; ring
    filter_upwards [h] with t ht
    rw [hyz] at ht
    exact ht.symm
  -- ### 4. On a positive-measure set, J sits inside the palette at x.
  have hJae : ∀ᵐ t ∂volume, ∀ i : Fin k, i ∈ J → t ∈ A → t ∈ liftPalette c hc x i := by
    apply ae_all_iff.mpr
    intro i
    by_cases hi : i ∈ J
    · filter_upwards [hA.2 i hi] with t ht
      intro _ hta
      exact ht hta
    · exact Eventually.of_forall fun t h => absurd h hi
  -- ### 5. Pull the five conull angular statements to ℝ.
  have hNKy' := angleMk_quasiMeasurePreserving.ae hNKy
  have hNKz' := angleMk_quasiMeasurePreserving.ae hNKz
  have hDxy' := angleMk_quasiMeasurePreserving.ae hDxy
  have hDxz' := angleMk_quasiMeasurePreserving.ae hDxz
  have hDyz' := angleMk_quasiMeasurePreserving.ae hDyz
  -- ### 6. One real point in A satisfies everything.
  have hae : ∀ᵐ t ∂volume, t ∈ A →
      (∀ i : Fin k, i ∈ J → i ∈ palette c hc x (t : Angles)) ∧
      ¬ palette c hc (x + direction (b : Angles)) (t : Angles) ⊆ K ∧
      ¬ palette c hc (x + direction (d : Angles)) (t : Angles) ⊆ K ∧
      Disjoint (palette c hc (x + direction (b : Angles)) (t : Angles))
        (palette c hc x (t : Angles)) ∧
      Disjoint (palette c hc (x + direction (d : Angles)) (t : Angles))
        (palette c hc x (t : Angles)) ∧
      Disjoint (palette c hc (x + direction (b : Angles)) (t : Angles))
        (palette c hc (x + direction (d : Angles)) (t : Angles)) := by
    filter_upwards [hJae, hNKy', hNKz', hDxy', hDxz', hDyz'] with t hJt h1 h2 h3 h4 h5
    intro hta
    refine ⟨?_, h1, h2, h3, h4, h5⟩
    intro i hi
    rw [mem_palette]
    simpa only [liftPalette, mem_preimage] using hJt i hi hta
  have hz0 : volume {t : ℝ | ¬ (t ∈ A →
      (∀ i : Fin k, i ∈ J → i ∈ palette c hc x (t : Angles)) ∧
      ¬ palette c hc (x + direction (b : Angles)) (t : Angles) ⊆ K ∧
      ¬ palette c hc (x + direction (d : Angles)) (t : Angles) ⊆ K ∧
      Disjoint (palette c hc (x + direction (b : Angles)) (t : Angles))
        (palette c hc x (t : Angles)) ∧
      Disjoint (palette c hc (x + direction (d : Angles)) (t : Angles))
        (palette c hc x (t : Angles)) ∧
      Disjoint (palette c hc (x + direction (b : Angles)) (t : Angles))
        (palette c hc (x + direction (d : Angles)) (t : Angles)))} = 0 :=
    ae_iff.mp hae
  obtain ⟨t, hta, hJt, hNKyt, hNKzt, hDxyt, hDxzt, hDyt⟩ : ∃ t ∈ A,
      (∀ i : Fin k, i ∈ J → i ∈ palette c hc x (t : Angles)) ∧
      ¬ palette c hc (x + direction (b : Angles)) (t : Angles) ⊆ K ∧
      ¬ palette c hc (x + direction (d : Angles)) (t : Angles) ⊆ K ∧
      Disjoint (palette c hc (x + direction (b : Angles)) (t : Angles))
        (palette c hc x (t : Angles)) ∧
      Disjoint (palette c hc (x + direction (d : Angles)) (t : Angles))
        (palette c hc x (t : Angles)) ∧
      Disjoint (palette c hc (x + direction (b : Angles)) (t : Angles))
        (palette c hc (x + direction (d : Angles)) (t : Angles)) := by
    by_contra hcon
    push_neg at hcon
    have hsub : A ⊆ {t : ℝ | ¬ (t ∈ A →
        (∀ i : Fin k, i ∈ J → i ∈ palette c hc x (t : Angles)) ∧
        ¬ palette c hc (x + direction (b : Angles)) (t : Angles) ⊆ K ∧
        ¬ palette c hc (x + direction (d : Angles)) (t : Angles) ⊆ K ∧
        Disjoint (palette c hc (x + direction (b : Angles)) (t : Angles))
          (palette c hc x (t : Angles)) ∧
        Disjoint (palette c hc (x + direction (d : Angles)) (t : Angles))
          (palette c hc x (t : Angles)) ∧
        Disjoint (palette c hc (x + direction (b : Angles)) (t : Angles))
          (palette c hc (x + direction (d : Angles)) (t : Angles)))} := by
      intro u hu'
      simp only [mem_setOf_eq, not_imp]
      exact ⟨hu', hcon u hu'⟩
    have hle : volume A ≤ volume {t : ℝ | ¬ (t ∈ A →
        (∀ i : Fin k, i ∈ J → i ∈ palette c hc x (t : Angles)) ∧
        ¬ palette c hc (x + direction (b : Angles)) (t : Angles) ⊆ K ∧
        ¬ palette c hc (x + direction (d : Angles)) (t : Angles) ⊆ K ∧
        Disjoint (palette c hc (x + direction (b : Angles)) (t : Angles))
          (palette c hc x (t : Angles)) ∧
        Disjoint (palette c hc (x + direction (d : Angles)) (t : Angles))
          (palette c hc x (t : Angles)) ∧
        Disjoint (palette c hc (x + direction (b : Angles)) (t : Angles))
          (palette c hc (x + direction (d : Angles)) (t : Angles)))} :=
      measure_mono hsub
    rw [hz0] at hle
    exact absurd (le_antisymm hle (zero_le _)) hp.ne'
  -- ### 7. The finite label fact: X lands in both palettes.
  obtain ⟨j, hjQ, hjK⟩ := Finset.not_subset.mp hNKyt
  have hjNotJ : j ∉ J := by
    intro hjJ
    exact (Finset.disjoint_left.mp hDxyt) hjQ (hJt j hjJ)
  have hjX : j = X := (hlabels j).mp (by
    simp only [Finset.mem_union, not_or]
    exact ⟨hjNotJ, hjK⟩)
  obtain ⟨j', hj'Q, hj'K⟩ := Finset.not_subset.mp hNKzt
  have hj'NotJ : j' ∉ J := by
    intro hjJ
    exact (Finset.disjoint_left.mp hDxzt) hj'Q (hJt j' hjJ)
  have hj'X : j' = X := (hlabels j').mp (by
    simp only [Finset.mem_union, not_or]
    exact ⟨hj'NotJ, hj'K⟩)
  have hXy : X ∈ palette c hc (x + direction (b : Angles)) (t : Angles) := hjX ▸ hjQ
  have hXz : X ∈ palette c hc (x + direction (d : Angles)) (t : Angles) := hj'X ▸ hj'Q
  exact (Finset.disjoint_left.mp hDyt) hXy hXz

#print axioms fixed_state_no_unit_three_centres

end EuclideanFiveColor
end
end OAI
