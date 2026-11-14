import OAI.Geometry.PlaneColoring.BoundaryTrace

namespace OAI

noncomputable section
open Set Filter Topology MeasureTheory
open scoped RealInnerProductSpace
namespace EuclideanFiveColor

/-! ## 0. Neighbour-palette transport, moved verbatim out of `FiveSupport`.
These two lemmas are generic in `k` and had no five-state dependency; `FiveSupport` imports this
module and its one call site (`five_support_step_ban`) keeps the same argument list. -/

section Neighbor
variable {k : ℕ} (c : ℂ → Fin k) (hc : Measurable c)

lemma palette_neighbor_real (hw : WeakColoring k c) (x : ℂ) (a : ℝ) (i : Fin k) :
    ∀ᵐt : ℝ∂volume,t∈liftPalette c hc (x+direction (a : Angles)) i → t∉liftPalette c hc x i := by
  let U : Set ℝ := {t | Real.sin (a-t)≠0}
  have hU : IsOpen U := isOpen_ne_fun (Real.continuous_sin.comp (continuous_const.sub continuous_id)) continuous_const
  have hu : ∀ᵐt : ℝ∂volume,t∈U := by
    filter_upwards [ae_sin_sub_ne_zero a] with t ht
    change Real.sin (a-t)≠0
    rwa [← neg_sub t a,Real.sin_neg,neg_ne_zero]
  have hh := palette_smooth_transport c hc hw (x := x) (z := x+direction (a : Angles)) hU (s := id) (t := fun _ => a)
    (ds := fun _ => 1) (dt := fun _ => 0) (fun t _ => hasDerivAt_id t)
    (fun t _ => hasDerivAt_const t a) (fun _ _ => one_ne_zero) (fun _ ht => ht) (fun t _ => ?_) i
  · exact (ae_restrict_iff' hU.measurableSet).mp hh |>.mp (hu.mono fun t ht hi => hi ht)
  · simp only [circleTarget,samplingParameter,add_sub_cancel_left,direction_realPlane,circleSum,one_smul,one_mul,id_eq]
    exact Prod.ext (add_comm _ _) (add_comm _ _)
lemma palette_neighbor_disjoint (hw : WeakColoring k c) (x : ℂ) (a : ℝ) :
    ∀ᵐt∂angularMeasure,Disjoint (palette c hc (x+direction (a : Angles)) t) (palette c hc x t) := by
  have hp (i : Fin k) : ∀ᵐt∂angularMeasure,t∈paletteSet c hc (x+direction (a : Angles)) i → t∉paletteSet c hc x i := by
    apply ae_angular_of_ae_line
    · simpa only [imp_iff_not_or,Set.compl_def,Set.union_def,Set.mem_ofPred_eq] using
        (paletteSet_measurable c hc (x+direction (a : Angles)) i).compl.union (paletteSet_measurable c hc x i).compl
    · exact palette_neighbor_real c hc hw x a i
  filter_upwards [ae_all_iff.mpr hp] with t ht
  exact Finset.disjoint_left.mpr fun i hi hj => ht i ((mem_palette c hc _ t i).mp hi) ((mem_palette c hc _ t i).mp hj)

end Neighbor

/-! ## 1. The closed set `Z_K` of centres carrying a `K`-avoiding trace -/

section ThreeCentre
variable {k : ℕ} {c : ℂ → Fin k} (hc : Measurable c)

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
  obtain ⟨t, hta, ht⟩ := ((frequently_ae_mem_iff.mpr hp.ne').and_eventually hae).exists
  obtain ⟨hJt, hNKyt, hNKzt, hDxyt, hDxzt, hDyt⟩ := ht hta
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

end ThreeCentre
end EuclideanFiveColor
end
end OAI
