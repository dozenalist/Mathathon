/-
  SUPERSEDED 2026-11-14 (block 20). Kept for the record, not to be queued.

  This file's three BLOCKERs (restrict of a finite disjoint union, support of a finite measure sum,
  translate of a support point) are UNNECESSARY: the development already contains that machinery in
  `stateSupport_shift_relation` (FiveSupport.lean:55), which proves the same conclusion directly with
  `R i j := Disjoint (stateSupport f i) (stateSupport f j)`. See ../DOWNSTREAM-INTEGRATION-PLAN.md §2.
  Do not build this file; do not duplicate it.

  JOINT-PAIR SUPPORT THEOREM -- proposed, NOT COMPILED.  Astra candidate, independently audited.

  STATUS: the MATHEMATICS is verified by hand (see ../JOINT-PAIR-AUDIT.md §2). The LEAN proof below is
  a structured plan with exactly three named gaps, each marked `BLOCKER`. No admission tactic appears in this
  file: unfinished steps are named `BLOCKER_n` constants that do not exist, so the file cannot
  compile and therefore cannot be mistaken for a compiled theorem. That is deliberate.

  CAVEAT: not only the three BLOCKER_n steps are unverified. The closing theorem's rewrites
  (`Measure.restrict_apply'`, `Measure.support_mono`, `Measure.restrict_eq_zero`,
  `Measure.support_zero`) are candidate Mathlib names and were not checked against the pinned
  toolchain. Treat the whole file as a PLAN, not a near-compiling artifact.

  WHAT IT SAYS.  For a finite-valued measurable f : ℝ → ι and a shift d, if every pair of state
  supports that meet anywhere has a volume-null joint-pair set, then each support is disjoint from
  its own translate by d.

  WHY IT IS USEFUL.  Applied with ι = Fin 5, f = fiveState at a five-centre x, d = sixty, it yields
  five_support_no_sixty (FiveSupport.lean:138) from fiveState_adj (non-adjacent pairs) and
  five_support_step_ban (adjacent pairs), WITHOUT strict_state_no_unit_support (States.lean:704).
  It does NOT remove that theorem from the development: see the audit, §3.

  SOURCE HASHES (lean/OAI as of 2026-11-14):
    Geometry/PlaneColoring/FiveSupport.lean   (stateSupport, stateSupport_shift_relation)
    Geometry/PlaneColoring/Accumulation.lean  (fiveState_adj:390)
    Geometry/PlaneColoring/States.lean        (strict_state_no_unit_support:704)
-/

import OAI.Geometry.PlaneColoring.FiveSupport

namespace OAI
noncomputable section
open Set Filter Topology MeasureTheory
namespace EuclideanFiveColor

variable {ι : Type*} [Fintype ι] [MeasurableSpace ι] [MeasurableSingletonClass ι]

/-- The joint-pair set: points of state `i` whose translate by `d` has state `j`. -/
def jointPair (f : ℝ → ι) (d : ℝ) (i j : ι) : Set ℝ := {t | f t = i ∧ f (t + d) = j}

lemma jointPair_measurable {f : ℝ → ι} (hf : Measurable f) (d : ℝ) (i j : ι) :
    MeasurableSet (jointPair f d i j) :=
  (measurableSet_eq_fun hf measurable_const).inter
    (measurableSet_eq_fun (hf.comp (continuous_id.add continuous_const).measurable) measurable_const)

/-- Every state class is the disjoint union of its joint-pair pieces over the second state. -/
lemma stateSet_eq_iUnion_jointPair (f : ℝ → ι) (d : ℝ) (i : ι) :
    {t | f t = i} = ⋃ j, jointPair f d i j := by
  ext t
  simp only [mem_iUnion, jointPair, mem_setOf_eq]
  constructor
  · intro ht; exact ⟨f (t + d), ht, rfl⟩
  · rintro ⟨j, ht, -⟩; exact ht

/-- **BLOCKER 1** — restrict of a finite disjoint union.
  Needed: `volume.restrict (⋃ j ∈ s, A j) = ∑ j ∈ s, volume.restrict (A j)` for pairwise disjoint
  measurable `A j`. Candidate Mathlib names to try, in order:
    `Measure.restrict_iUnion_finset`, `Measure.restrict_iUnion` (needs Countable + PairwiseDisjoint),
    or a `Finset.induction` over `Measure.restrict_union` with `MeasurableSet` + `Disjoint`.
  The disjointness here is `j ≠ j' → Disjoint (jointPair f d i j) (jointPair f d i j')`, immediate
  from `f (t+d) = j` and `= j'`. -/
lemma restrict_stateSet_eq_sum (f : ℝ → ι) (d : ℝ) (i : ι) :
    volume.restrict {t | f t = i} = ∑ j, volume.restrict (jointPair f d i j) := by
  BLOCKER_1

/-- **BLOCKER 2** — support of a finite sum is the union of the supports.
  Needed: `support (∑ j ∈ s, μ j) = ⋃ j ∈ s, support (μ j)`. Candidate: `Measure.support_sum`;
  otherwise `Finset.induction` from `Measure.support_add` and `Measure.support_zero`.
  (Note `Measure.support_add` is the only genuinely load-bearing instance; positivity of a sum of
  measures is `add_pos_iff`-like, which is why the finite case reduces cleanly.) -/
lemma support_iUnion_jointPair {f : ℝ → ι} (hf : Measurable f) (d : ℝ) (i : ι) :
    stateSupport f i
      = ⋃ j, (volume.restrict (jointPair f d i j)).support := by
  rw [stateSupport, stateSet_eq_iUnion_jointPair, restrict_stateSet_eq_sum]
  exact BLOCKER_2

/-- **BLOCKER 3** — the translate of a support point lands in the support of the translated set.
  If `a ∈ support (volume.restrict A)` then `a + d ∈ support (volume.restrict ((· + d) '' A))`.
  Ingredients, all available for `volume` on `ℝ`:
    * `Measure.map_add_right_eq_self (volume : Measure ℝ) d` or `isAddHaarMeasure`-based
      measure preservation of `t ↦ t + d`;
    * `Homeomorph.addRight d` maps neighbourhoods to neighbourhoods (so no `IsOpen` juggling is
      needed if the statement is phrased with `nhds`);
    * `Measure.IsOpenPosMeasure`/`support` monotonicity for the final inclusion.
  Phrased here for the image, which is what the application uses. -/
lemma mem_support_add_image {A : Set ℝ} {a d : ℝ}
    (ha : a ∈ (volume.restrict A).support) :
    a + d ∈ (volume.restrict ((fun t => t + d) '' A)).support := by
  BLOCKER_3

/-- **The joint-pair support theorem.**  Independently audited; correct. Proof plan:
  `a ∈ S i` → by `support_iUnion_jointPair` pick `j` with `a ∈ support (volume.restrict (Q i j))`;
  by `mem_support_add_image`, `a + d` lies in `support (volume.restrict (image Q i j))`, and the image
  is contained in `{t | f t = j}`, so `a + d ∈ S j`; if also `a + d ∈ S i` then `S i ∩ S j` is
  nonempty, so the hypothesis gives `volume (Q i j) = 0`, whence `volume.restrict (Q i j) = 0` and its
  support is empty — contradicting `a`'s membership. -/
theorem disjoint_translate_of_null_jointPair {f : ℝ → ι} (hf : Measurable f) {d : ℝ}
    (hQ : ∀ i j, (stateSupport f i ∩ stateSupport f j).Nonempty →
      volume (jointPair f d i j) = 0) (i : ι) :
    Disjoint (stateSupport f i) ((fun t => t + d) ⁻¹' stateSupport f i) := by
  rw [Set.disjoint_left]
  intro a ha ha'
  simp only [mem_preimage] at ha'
  rw [support_iUnion_jointPair hf d i, mem_iUnion] at ha
  obtain ⟨j, hj⟩ := ha
  have hsub : (fun t => t + d) '' jointPair f d i j ⊆ {t | f t = j} := by
    rintro _ ⟨t, ⟨-, ht⟩, rfl⟩
    exact ht
  have haj : a + d ∈ stateSupport f j := by
    rw [stateSupport, ← Measure.restrict_apply' (measurableSet_eq_fun hf measurable_const)]
    exact Measure.support_mono (by rw [Measure.restrict_apply' (jointPair_measurable hf d i j)])
      (mem_support_add_image hj)
  have hne : (stateSupport f i ∩ stateSupport f j).Nonempty := ⟨a + d, ha', haj⟩
  have h0 : volume (jointPair f d i j) = 0 := hQ i j hne
  have hzero : volume.restrict (jointPair f d i j) = 0 := by
    rw [Measure.restrict_eq_zero]; exact h0
  rw [hzero, Measure.support_zero, mem_empty_iff_false] at hj
  exact hj

end EuclideanFiveColor
end
end OAI
