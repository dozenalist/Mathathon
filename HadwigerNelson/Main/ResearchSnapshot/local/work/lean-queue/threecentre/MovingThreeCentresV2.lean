/-
  MOVING-CENTRE EXTENSION (V2).  Private validation module.  UNCOMPILED AS DELIVERED.

  V1 (threecentre/FixedStateThreeCentres.V1.lean, sha256 af45ff16...) is preserved unchanged; it passed
  locally after three API repairs. V2 uses the repaired API idioms throughout:
    * `RealState hc x A J`  -- `c` is implicit in `RealState`, not an argument;
    * `direction_exists` returns an `Angles`, so a REAL angle is obtained from it with
      `QuotientAddGroup.mk_surjective` (the idiom already used in States:700);
    * the positive-AE witness is `((frequently_ae_mem_iff.mpr hp.ne').and_eventually hae).exists`,
      not a by-contradiction measure computation.

  CONTENTS
    1. avoidingTraceCentre Z_K  (a set in the PLANE depending only on c and K)
    2. triangle_no_unit_of_avoiding_traces  -- the core, from two ACTUAL K-avoiding traces
    3. fixed_state_no_unit_three_centres    -- V1's statement, now a one-line wrapper
    4. Z_K is sequentially closed (compactTraceVector subsequence + trace_limit +
       traceCode_tendsto_iff tested at the limit coordinate; no projection API, and no continuity
       of traceValue is asserted)
    5. strict_state_sequence_no_unit_three_centres -- converging centres, identical conclusion
    6. four_support_sequence_no_unit_three_centres (k = 5)      -- unchanged statement, new proof

  NO `sorry`, no `admit`, no placeholder.  No cloud build was run and no shared file was edited.

  Toolchain: Lean 4.34.1 commit 5045d0056413266e57c625dcd7c365b10e377c52,
  Mathlib d13f23b723b8a846827a245b89c10fc7d3f11612.
-/

import OAI.Geometry.PlaneColoring.FiveSupport
import OAI.Geometry.PlaneColoring.BoundaryTrace
import OAI.Geometry.PlaneColoring.FourContinuity

namespace OAI
noncomputable section
open Set Filter Topology MeasureTheory
open scoped RealInnerProductSpace
namespace EuclideanFiveColor

section Generic
variable {k : ℕ} {c : ℂ → Fin k} (hc : Measurable c)

/-! ## 1. The closed set of centres admitting a `K`-avoiding trace -/

/-- `Z_K`: centres in the plane at which some trace vanishes on every label of `K`.  It depends only
on `c` and `K` — not on a base centre, an angular state set, or a sequence. -/
def avoidingTraceCentre (K : Finset (Fin k)) : Set ℂ :=
  {y | ∃ β : TraceVector k, IsTrace c hc y β ∧ ∀ i ∈ K, traceValue β i = 0}

/-! ## 2. The core: two actual avoiding traces at unit distance from a common centre -/

/-- **Triangle exclusion.**  If `A` is a positive-measure `J`-state at `x`, the complement of `J ∪ K`
is exactly `{X}`, and two centres at unit distance from `x` carry actual traces vanishing on `K`,
then those two centres are not at unit distance from each other. -/
theorem triangle_no_unit_of_avoiding_traces (hw : WeakColoring k c)
    {x : ℂ} {J K : Finset (Fin k)} {X : Fin k}
    (hlabels : ∀ i, i ∉ J ∪ K ↔ i = X)
    {A : Set ℝ} (hA : RealState hc x A J) (hp : 0 < volume A)
    {ay az : ℝ} {βy βz : TraceVector k}
    (hty : IsTrace c hc (x + direction (ay : Angles)) βy)
    (htz : IsTrace c hc (x + direction (az : Angles)) βz)
    (hKy : ∀ i ∈ K, traceValue βy i = 0)
    (hKz : ∀ i ∈ K, traceValue βz i = 0)
    (hunit : ‖direction (ay : Angles) - direction (az : Angles)‖ = 1) : False := by
  classical
  -- ### palettes
  have hNKy : ∀ᵐ t ∂angularMeasure,
      ¬ palette c hc (x + direction (ay : Angles)) t ⊆ K :=
    avoiding_trace_palette c hc (x := x + direction (ay : Angles)) hty hKy
  have hNKz : ∀ᵐ t ∂angularMeasure,
      ¬ palette c hc (x + direction (az : Angles)) t ⊆ K :=
    avoiding_trace_palette c hc (x := x + direction (az : Angles)) htz hKz
  have hDxy : ∀ᵐ t ∂angularMeasure,
      Disjoint (palette c hc (x + direction (ay : Angles)) t) (palette c hc x t) :=
    palette_neighbor_disjoint c hc hw x ay
  have hDxz : ∀ᵐ t ∂angularMeasure,
      Disjoint (palette c hc (x + direction (az : Angles)) t) (palette c hc x t) :=
    palette_neighbor_disjoint c hc hw x az
  -- ### the unit direction between the two outer centres, fixed BEFORE any exceptional set
  have hzy : ‖(x + direction (az : Angles)) - (x + direction (ay : Angles))‖ = 1 := by
    have h : (x + direction (az : Angles)) - (x + direction (ay : Angles))
        = direction (az : Angles) - direction (ay : Angles) := by ring
    rw [h, norm_sub_rev]; exact hunit
  obtain ⟨t₀, ht₀⟩ := direction_exists hzy
  obtain ⟨a, rfl⟩ := QuotientAddGroup.mk_surjective t₀
  have hDyz : ∀ᵐ t ∂angularMeasure,
      Disjoint (palette c hc (x + direction (ay : Angles)) t)
        (palette c hc (x + direction (az : Angles)) t) := by
    have h := palette_neighbor_disjoint c hc hw (x + direction (ay : Angles)) a
    have hyz : (x + direction (ay : Angles)) + direction (a : Angles)
        = x + direction (az : Angles) := by rw [ht₀]; ring
    filter_upwards [h] with t ht'
    rw [hyz] at ht'
    exact ht'.symm
  -- ### `J` inside the palette at `x` on a positive-measure set
  have hJae : ∀ᵐ t ∂volume, ∀ i : Fin k, i ∈ J → t ∈ A → t ∈ liftPalette c hc x i := by
    apply ae_all_iff.mpr
    intro i
    by_cases hi : i ∈ J
    · filter_upwards [hA.2 i hi] with t ht'
      intro _ hta
      exact ht' hta
    · exact Eventually.of_forall fun t h => absurd h hi
  -- ### pull the five conull angular statements to ℝ
  have hNKy' := angleMk_quasiMeasurePreserving.ae hNKy
  have hNKz' := angleMk_quasiMeasurePreserving.ae hNKz
  have hDxy' := angleMk_quasiMeasurePreserving.ae hDxy
  have hDxz' := angleMk_quasiMeasurePreserving.ae hDxz
  have hDyz' := angleMk_quasiMeasurePreserving.ae hDyz
  have hae : ∀ᵐ t ∂volume, t ∈ A →
      (∀ i : Fin k, i ∈ J → i ∈ palette c hc x (t : Angles)) ∧
      ¬ palette c hc (x + direction (ay : Angles)) (t : Angles) ⊆ K ∧
      ¬ palette c hc (x + direction (az : Angles)) (t : Angles) ⊆ K ∧
      Disjoint (palette c hc (x + direction (ay : Angles)) (t : Angles))
        (palette c hc x (t : Angles)) ∧
      Disjoint (palette c hc (x + direction (az : Angles)) (t : Angles))
        (palette c hc x (t : Angles)) ∧
      Disjoint (palette c hc (x + direction (ay : Angles)) (t : Angles))
        (palette c hc (x + direction (az : Angles)) (t : Angles)) := by
    filter_upwards [hJae, hNKy', hNKz', hDxy', hDxz', hDyz'] with t hJt h1 h2 h3 h4 h5
    intro hta
    refine ⟨?_, h1, h2, h3, h4, h5⟩
    intro i hi
    rw [mem_palette]
    simpa only [liftPalette, mem_preimage] using hJt i hi hta
  -- ### one real point of `A` carries all of it
  obtain ⟨t, hta, hJt, hNKyt, hNKzt, hDxyt, hDxzt, hDyt⟩ :=
    ((frequently_ae_mem_iff.mpr hp.ne').and_eventually hae).exists
  -- ### the finite label fact
  obtain ⟨j, hjQ, hjK⟩ := Finset.not_subset.mp hNKyt
  have hjNotJ : j ∉ J := fun hjJ => (Finset.disjoint_left.mp hDxyt) hjQ (hJt j hjJ)
  have hjX : j = X := (hlabels j).mp (by
    simp only [Finset.mem_union, not_or]
    exact ⟨hjNotJ, hjK⟩)
  obtain ⟨j', hj'Q, hj'K⟩ := Finset.not_subset.mp hNKzt
  have hj'NotJ : j' ∉ J := fun hjJ => (Finset.disjoint_left.mp hDxzt) hj'Q (hJt j' hjJ)
  have hj'X : j' = X := (hlabels j').mp (by
    simp only [Finset.mem_union, not_or]
    exact ⟨hj'NotJ, hj'K⟩)
  exact (Finset.disjoint_left.mp hDyt) (hjX ▸ hjQ) (hj'X ▸ hj'Q)

/-! ## 3. The fixed-state theorem, now a wrapper -/

/-- Same statement as `States.lean:704` `strict_state_no_unit_support`. -/
theorem fixed_state_no_unit_three_centres (hw : WeakColoring k c)
    {x : ℂ} {J K : Finset (Fin k)} {X : Fin k}
    (hlabels : ∀ i, i ∉ J ∪ K ↔ i = X)
    {A B : Set ℝ} (hA : RealState hc x A J) (hB : RealState hc x B K)
    (hp : 0 < volume A) {b d : ℝ}
    (hb : b ∈ (volume.restrict B).support) (hd : d ∈ (volume.restrict B).support) :
    ‖direction (b : Angles) - direction (d : Angles)‖ ≠ 1 := by
  intro hu
  obtain ⟨βy, hty, hKy⟩ := state_support_avoiding_trace c hc hw (x := x) (A := B) (J := K) hB hb
  obtain ⟨βz, htz, hKz⟩ := state_support_avoiding_trace c hc hw (x := x) (A := B) (J := K) hB hd
  exact triangle_no_unit_of_avoiding_traces hc hw hlabels hA hp hty htz hKy hKz hu

/-! ## 4. `Z_K` is sequentially closed -/

lemma avoidingTraceCentre_seqClosed (K : Finset (Fin k)) :
    IsSeqClosed (avoidingTraceCentre hc K) := by
  intro yseq y hy hylim
  choose β hβ hβK using hy
  obtain ⟨β₀, -, φ, hφ, hcon⟩ :=
    (isCompact_univ : IsCompact (Set.univ : Set (TraceVector k))).isSeqCompact.subseq_of_frequently_in
      (Eventually.frequently (Eventually.of_forall fun n => Set.mem_univ (β n)))
  refine ⟨β₀, ?_, ?_⟩
  · exact trace_limit c hc (fun n => hβ (φ n)) (hylim.comp hφ.tendsto_atTop) hcon
  · intro i hi
    -- test the weak convergence at the limit coordinate; NO continuity of `traceValue` is asserted
    have hh := (traceCode_tendsto_iff.mp hcon) i (traceValue β₀ i)
    have hz : ∀ n, ⟪traceValue (β (φ n)) i, traceValue β₀ i⟫ = 0 := by
      intro n
      rw [hβK (φ n) i hi]
      simp
    have h0 : ⟪traceValue β₀ i, traceValue β₀ i⟫ = 0 :=
      tendsto_nhds_unique hh
        (tendsto_const_nhds.congr' (Eventually.of_forall fun n => (hz n).symm))
    exact inner_self_eq_zero.mp h0

lemma isClosed_avoidingTraceCentre (K : Finset (Fin k)) :
    IsClosed (avoidingTraceCentre hc K) :=
  (avoidingTraceCentre_seqClosed hc K).isClosed

/-! ## 5. Converging centres -/

/-- The moving-centre theorem: centres converge, each carries a `K`-state, the limit carries a
positive `J`-state, and the two support points converge.  Conclusion identical to the fixed case. -/
theorem strict_state_sequence_no_unit_three_centres (hw : WeakColoring k c)
    {x : ℕ → ℂ} {y : ℂ} (hxt : Tendsto x atTop (𝓝 y))
    {J K : Finset (Fin k)} {X : Fin k} (hlabels : ∀ i, i ∉ J ∪ K ↔ i = X)
    {B : ℕ → Set ℝ} (hB : ∀ n, RealState hc (x n) (B n) K)
    {A : Set ℝ} (hA : RealState hc y A J) (hp : 0 < volume A)
    {b d : ℕ → ℝ} {b₀ d₀ : ℝ} (hb : Tendsto b atTop (𝓝 b₀)) (hd : Tendsto d atTop (𝓝 d₀))
    (hbs : ∀ n, b n ∈ (volume.restrict (B n)).support)
    (hds : ∀ n, d n ∈ (volume.restrict (B n)).support) :
    ‖direction (b₀ : Angles) - direction (d₀ : Angles)‖ ≠ 1 := by
  classical
  -- each centre `x n + direction (b n)` lies in `Z_K`
  have hmem : ∀ n, (x n + direction (b n : Angles)) ∈ avoidingTraceCentre hc K ∧
      (x n + direction (d n : Angles)) ∈ avoidingTraceCentre hc K := by
    intro n
    exact ⟨state_support_avoiding_trace c hc hw (x := x n) (A := B n) (J := K) (hB n) (hbs n),
           state_support_avoiding_trace c hc hw (x := x n) (A := B n) (J := K) (hB n) (hds n)⟩
  -- limits
  have hbA : Tendsto (fun n => (b n : Angles)) atTop (𝓝 (b₀ : Angles)) :=
    (AddCircle.continuous_mk' (2 * Real.pi)).continuousAt.tendsto.comp hb
  have hdA : Tendsto (fun n => (d n : Angles)) atTop (𝓝 (d₀ : Angles)) :=
    (AddCircle.continuous_mk' (2 * Real.pi)).continuousAt.tendsto.comp hd
  have hlimb : Tendsto (fun n => x n + direction (b n : Angles)) atTop
      (𝓝 (y + direction (b₀ : Angles))) :=
    hxt.add (direction_continuous.continuousAt.tendsto.comp hbA)
  have hlimd : Tendsto (fun n => x n + direction (d n : Angles)) atTop
      (𝓝 (y + direction (d₀ : Angles))) :=
    hxt.add (direction_continuous.continuousAt.tendsto.comp hdA)
  have hZy : (y + direction (b₀ : Angles)) ∈ avoidingTraceCentre hc K :=
    (isClosed_avoidingTraceCentre hc K).mem_of_tendsto hlimb
      (Eventually.of_forall fun n => (hmem n).1)
  have hZz : (y + direction (d₀ : Angles)) ∈ avoidingTraceCentre hc K :=
    (isClosed_avoidingTraceCentre hc K).mem_of_tendsto hlimd
      (Eventually.of_forall fun n => (hmem n).2)
  -- the two traces at the limit centres may come from different subsequences; that is enough
  obtain ⟨βy, hty, hKy⟩ := hZy
  obtain ⟨βz, htz, hKz⟩ := hZz
  intro hu
  exact triangle_no_unit_of_avoiding_traces hc hw hlabels hA hp hty htz hKy hKz hu

end Generic

/-! ## 6. The unchanged four-support consumer (its own section, so `c : ℂ → Fin 5` is not shadowed) -/

section FourState
variable {c : ℂ → Fin 5} (hc : Measurable c)

/-- Statement identical to `FourContinuity.lean:441` `four_support_sequence_no_unit_three_centres`; the proof
consumes neither `four_realState_continuity` nor `strict_state_sequence_false`. -/
theorem four_support_sequence_no_unit_three_centres (hw : WeakColoring 5 c)
    {x : ℕ → ℂ} {y : ℂ} (hx : ∀ n, FourCenter c (x n)) (hy : FourCenter c y)
    (hxt : Tendsto x atTop (𝓝 y)) {s : Fin 3} (hs : s ≠ 0)
    {b d : ℕ → ℝ} {b₀ d₀ : ℝ} (hb : Tendsto b atTop (𝓝 b₀)) (hd : Tendsto d atTop (𝓝 d₀))
    (hbs : ∀ n, b n ∈ fourSupport c hc (x n) s) (hds : ∀ n, d n ∈ fourSupport c hc (x n) s) :
    ‖direction (b₀ : Angles) - direction (d₀ : Angles)‖ ≠ 1 := by
  let r : Fin 3 := if s = 1 then 2 else 1
  have hr : r ≠ 0 := by dsimp [r]; split <;> decide
  have hl : ∀ i : Fin 5, i ∉ fourGroup r ∪ fourGroup s ↔ i = 4 := by
    exact (show ∀ s : Fin 3, s ≠ 0 → ∀ i : Fin 5,
      i ∉ fourGroup (if s = 1 then 2 else 1) ∪ fourGroup s ↔ i = 4 from by decide) s hs
  exact strict_state_sequence_no_unit_three_centres hc hw hxt hl
    (fun n => fourState_represents c hc hw (hx n) s)
    (fourState_represents c hc hw hy r) (four_realState_positive c hc hw hy hr)
    hb hd hbs hds

end FourState

#print axioms triangle_no_unit_of_avoiding_traces
#print axioms fixed_state_no_unit_three_centres
#print axioms strict_state_sequence_no_unit_three_centres
#print axioms four_support_sequence_no_unit_three_centres

end EuclideanFiveColor
end
end OAI
