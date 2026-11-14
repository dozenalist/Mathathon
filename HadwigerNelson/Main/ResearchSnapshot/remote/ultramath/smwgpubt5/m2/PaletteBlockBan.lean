/-
  Palette-block contact ban.
  Member m2, swarm smwgpubt5, direction d1.

  STATUS [P] proposed / NOT ELABORATED.  Runs of Lean are outside this assignment
  ("do NOT build Lean"), so this file is hand-checked only.  Every tactic step is a
  transcription of a step that compiles elsewhere in OAI/Geometry/PlaneColoring; the
  citations are in collapse.md §5.  The remaining obligation is exactly: elaborate this
  file and the two replacement bodies in FiveReproof.lean.

  Destination: lean/OAI/Geometry/PlaneColoring/PaletteBlockBan.lean, after `AvoidingTrace`
  (which supplies `palette_neighbor_disjoint`) and before `FiveSupport`, which imports it.

  THE COLLAPSE.  Every support/contact exclusion of the five-state branch is
    finite-label core  (§1, 11 lines, no analysis)
  + geometric supplier (unit-distance pair  §3, or 60-degree pair  §4)
  + measure beat       (§2: a positive `J`-state meets every conull angular ban).
  The three suppliers are `avoiding_trace_palette` (BoundaryTrace.lean:53),
  `palette_neighbor_disjoint` (AvoidingTrace.lean:31) and `palette_sixty_disjoint`
  (PaletteTransport.lean:450); nothing else is used.
-/
import OAI.Geometry.PlaneColoring.AvoidingTrace

namespace OAI
noncomputable section
open Set Filter Topology MeasureTheory
open scoped RealInnerProductSpace
namespace EuclideanFiveColor

/-! ## 1. The finite-label core.  No metric, no measure, no colouring: `Finset (Fin k)` only.

`palette c hc x s` is the finite set of colours carried by the ray from `x` at angle `s`
(Palettes.lean:35).  The lemma: a label `X` that is the *unique* label outside `J ∪ K`
cannot hide from a palette `p` that avoids the set `J` and is not contained in `K`.  Read
twice it says: two such palettes can never be disjoint. -/

lemma palette_block_ban {k : ℕ} {c : ℂ → Fin k} (hc : Measurable c)
    {x y₁ y₂ : ℂ} {J₁ K₁ J₂ K₂ : Finset (Fin k)} {X : Fin k} {s₁ s₂ : Angles}
    (hl₁ : ∀ i, i ∉ J₁ ∪ K₁ ↔ i = X) (hl₂ : ∀ i, i ∉ J₂ ∪ K₂ ↔ i = X)
    (hJ₁ : J₁ ⊆ palette c hc x s₁) (hJ₂ : J₂ ⊆ palette c hc x s₂)
    (hn₁ : ¬ palette c hc y₁ s₁ ⊆ K₁) (hn₂ : ¬ palette c hc y₂ s₂ ⊆ K₂)
    (hd₁ : Disjoint (palette c hc y₁ s₁) (palette c hc x s₁))
    (hd₂ : Disjoint (palette c hc y₂ s₂) (palette c hc x s₂)) :
    ¬ Disjoint (palette c hc y₁ s₁) (palette c hc y₂ s₂) := by
  have key : ∀ (J K p q : Finset (Fin k)), (∀ i, i ∉ J ∪ K ↔ i = X) → J ⊆ q →
      ¬ p ⊆ K → Disjoint p q → X ∈ p := by
    intro J K p q hl hJq hnp hpq
    obtain ⟨e, hep, heK⟩ := Finset.not_subset.mp hnp
    have heJ : e ∉ J := fun h => Finset.disjoint_left.mp hpq hep (hJq h)
    have heX : e = X := (hl e).mp (by simp only [Finset.mem_union, not_or]; exact ⟨heJ, heK⟩)
    simpa only [heX] using hep
  intro hdisj
  exact (Finset.disjoint_left.mp hdisj)
    (key J₁ K₁ (palette c hc y₁ s₁) (palette c hc x s₁) hl₁ hJ₁ hn₁ hd₁)
    (key J₂ K₂ (palette c hc y₂ s₂) (palette c hc x s₂) hl₂ hJ₂ hn₂ hd₂)

/-- Single-slot form: `five_forced_label` (Exclusion.lean:26), with the `by decide`
replaced by logic and `k = 5` replaced by an arbitrary `k`. -/
lemma forced_label_of_complement {k : ℕ} {c : ℂ → Fin k} (hc : Measurable c)
    {J K p : Finset (Fin k)} {X : Fin k}
    (hl : ∀ i, i ∉ J ∪ K ↔ i = X) (hd : Disjoint p J) (hn : ¬ p ⊆ K) : X ∈ p := by
  obtain ⟨e, hep, heK⟩ := Finset.not_subset.mp hn
  have heJ : e ∉ J := fun h => Finset.disjoint_left.mp hd hep h
  have heX : e = X := (hl e).mp (by simp only [Finset.mem_union, not_or]; exact ⟨heJ, heK⟩)
  simpa only [heX] using hep

/-! ## 2. The measure beat.  This is the only step that uses `RealState`, and it is the same
step in the fixed and in the moving case. -/

lemma block_of_positive_state {k : ℕ} {c : ℂ → Fin k} (hc : Measurable c)
    {x : ℂ} {J K : Finset (Fin k)} {X : Fin k} (hlabels : ∀ i, i ∉ J ∪ K ↔ i = X)
    {A : Set ℝ} (hA : RealState hc x A J) (hp : 0 < volume A)
    (hban : ∀ᵐ s ∂angularMeasure, ∀ (J' : Finset (Fin k)) (X' : Fin k),
      (∀ i, i ∉ J' ∪ K ↔ i = X') → ¬ J' ⊆ palette c hc x s) : False := by
  have hban' : ∀ᵐ t : ℝ ∂volume, ∀ (J' : Finset (Fin k)) (X' : Fin k),
      (∀ i, i ∉ J' ∪ K ↔ i = X') → ¬ J' ⊆ palette c hc x (t : Angles) :=
    angleMk_quasiMeasurePreserving.ae hban
  have hJae : ∀ᵐ t : ℝ ∂volume, t ∈ A → J ⊆ palette c hc x (t : Angles) := by
    filter_upwards [ae_all_iff.mpr (fun i : Fin k => ae_all_iff.mpr (fun hi : i ∈ J => hA.2 i hi))]
      with t ht hta i hiJ
    rw [mem_palette]
    simpa only [liftPalette, mem_preimage] using ht i hiJ hta
  obtain ⟨t, _hta, hb'⟩ :=
    ((frequently_ae_mem_iff.mpr hp.ne').and_eventually (hban'.and hJae)).exists
  exact hb'.1 J X hlabels hb'.2

/-! ## 3. Supplier A: two trace centres at unit distance from the base centre. -/

theorem no_joint_block_of_unit_pair {k : ℕ} {c : ℂ → Fin k} (hc : Measurable c)
    (hw : WeakColoring k c) {x y₁ y₂ : ℂ}
    (hy₁ : ‖y₁ - x‖ = 1) (hy₂ : ‖y₂ - x‖ = 1) (hy₁₂ : ‖y₁ - y₂‖ = 1)
    {K : Finset (Fin k)} {β₁ β₂ : TraceVector k}
    (ht₁ : IsTrace c hc y₁ β₁) (ht₂ : IsTrace c hc y₂ β₂)
    (hK₁ : ∀ i ∈ K, traceValue β₁ i = 0) (hK₂ : ∀ i ∈ K, traceValue β₂ i = 0) :
    ∀ᵐ s ∂angularMeasure, ∀ (J : Finset (Fin k)) (X : Fin k),
      (∀ i, i ∉ J ∪ K ↔ i = X) → ¬ J ⊆ palette c hc x s := by
  obtain ⟨a₁, ha₁⟩ := direction_exists hy₁
  obtain ⟨a₂, ha₂⟩ := direction_exists hy₂
  obtain ⟨a₁₂, ha₁₂⟩ := direction_exists (show ‖y₂ - y₁‖ = 1 by rwa [norm_sub_rev] at hy₁₂)
  have e₁ : x + direction (a₁ : Angles) = y₁ := by rw [ha₁]; ring
  have e₂ : x + direction (a₂ : Angles) = y₂ := by rw [ha₂]; ring
  have e₁₂ : y₁ + direction (a₁₂ : Angles) = y₂ := by rw [ha₁₂]; ring
  have hn₁ := avoiding_trace_palette c hc ht₁ hK₁
  have hn₂ := avoiding_trace_palette c hc ht₂ hK₂
  have hd₁ := palette_neighbor_disjoint c hc hw x a₁
  have hd₂ := palette_neighbor_disjoint c hc hw x a₂
  have hd₁₂ := palette_neighbor_disjoint c hc hw y₁ a₁₂
  filter_upwards [hn₁, hn₂, hd₁, hd₂, hd₁₂]
    with s Hn₁ Hn₂ Hd₁ Hd₂ Hd₁₂ J X hl hJ
  have Hd₁' : Disjoint (palette c hc y₁ s) (palette c hc x s) := by simpa only [e₁] using Hd₁
  have Hd₂' : Disjoint (palette c hc y₂ s) (palette c hc x s) := by simpa only [e₂] using Hd₂
  have Hd₁₂' : Disjoint (palette c hc y₂ s) (palette c hc y₁ s) := by simpa only [e₁₂] using Hd₁₂
  exact (palette_block_ban hc hl hl hJ hJ Hn₁ Hn₂ Hd₁' Hd₂') Hd₁₂'.symm

/-- Instance: `triangle_no_unit_of_avoiding_traces` (integration/AvoidingTrace.lean:58),
statement unchanged, proof = supplier A + measure beat. -/
theorem triangle_no_unit_of_avoiding_traces' {k : ℕ} {c : ℂ → Fin k} (hc : Measurable c)
    (hw : WeakColoring k c)
    {x : ℂ} {J K : Finset (Fin k)} {X : Fin k}
    (hlabels : ∀ i, i ∉ J ∪ K ↔ i = X)
    {A : Set ℝ} (hA : RealState hc x A J) (hp : 0 < volume A)
    {ay az : ℝ} {βy βz : TraceVector k}
    (hty : IsTrace c hc (x + direction (ay : Angles)) βy)
    (htz : IsTrace c hc (x + direction (az : Angles)) βz)
    (hKy : ∀ i ∈ K, traceValue βy i = 0)
    (hKz : ∀ i ∈ K, traceValue βz i = 0)
    (hunit : ‖direction (ay : Angles) - direction (az : Angles)‖ = 1) : False := by
  have hy₁ : ‖(x + direction (ay : Angles)) - x‖ = 1 := by
    rw [add_sub_cancel_left]; exact direction_norm (ay : Angles)
  have hy₂ : ‖(x + direction (az : Angles)) - x‖ = 1 := by
    rw [add_sub_cancel_left]; exact direction_norm (az : Angles)
  have hy₁₂ : ‖(x + direction (ay : Angles)) - (x + direction (az : Angles))‖ = 1 := by
    have h : (x + direction (ay : Angles)) - (x + direction (az : Angles))
        = direction (ay : Angles) - direction (az : Angles) := by ring
    rw [h]; exact hunit
  exact block_of_positive_state hc hlabels hA hp
    (no_joint_block_of_unit_pair hc hw hy₁ hy₂ hy₁₂ hty htz hKy hKz)

/-- Instance: exact contract of `States.lean:704` `strict_state_no_unit_support`
(= integration/AvoidingTrace.lean:148 `fixed_state_no_unit_three_centres`),
statement copied binder for binder, proof = supplier A + measure beat. -/
theorem strict_state_no_unit_joint_block {k : ℕ} {c : ℂ → Fin k}
    (hc : Measurable c) (hw : WeakColoring k c)
    {x : ℂ} {J K : Finset (Fin k)} {X : Fin k}
    (hlabels : ∀ i, i ∉ J ∪ K ↔ i = X)
    {A B : Set ℝ} (hA : RealState hc x A J) (hB : RealState hc x B K)
    (hp : 0 < volume A) {b d : ℝ}
    (hb : b ∈ (volume.restrict B).support) (hd : d ∈ (volume.restrict B).support) :
    ‖direction (b : Angles) - direction (d : Angles)‖ ≠ 1 := by
  intro hu
  obtain ⟨βy, hty, hKy⟩ := state_support_avoiding_trace c hc hw (x := x) (A := B) (J := K) hB hb
  obtain ⟨βz, htz, hKz⟩ := state_support_avoiding_trace c hc hw (x := x) (A := B) (J := K) hB hd
  have hy₁ : ‖(x + direction (b : Angles)) - x‖ = 1 := by
    rw [add_sub_cancel_left]; exact direction_norm (b : Angles)
  have hy₂ : ‖(x + direction (d : Angles)) - x‖ = 1 := by
    rw [add_sub_cancel_left]; exact direction_norm (d : Angles)
  have hy₁₂ : ‖(x + direction (b : Angles)) - (x + direction (d : Angles))‖ = 1 := by
    have h : (x + direction (b : Angles)) - (x + direction (d : Angles))
        = direction (b : Angles) - direction (d : Angles) := by ring
    rw [h]; exact hu
  exact block_of_positive_state hc hlabels hA hp
    (no_joint_block_of_unit_pair hc hw hy₁ hy₂ hy₁₂ hty htz hKy hKz)

/-! ## 4. Supplier B: one trace centre, two angles 60 degrees apart.

Only `palette_sixty_disjoint` replaces the closing `palette_neighbor_disjoint` of §3. -/

theorem no_joint_block_of_sixty_pair {k : ℕ} {c : ℂ → Fin k} (hc : Measurable c)
    (hw : WeakColoring k c) {x y : ℂ} (hy : ‖y - x‖ = 1)
    {K₁ K₂ : Finset (Fin k)} {β₁ β₂ : TraceVector k}
    (ht₁ : IsTrace c hc y β₁) (ht₂ : IsTrace c hc y β₂)
    (hK₁ : ∀ i ∈ K₁, traceValue β₁ i = 0) (hK₂ : ∀ i ∈ K₂, traceValue β₂ i = 0) :
    ∀ᵐ s ∂angularMeasure, ∀ (J₁ J₂ : Finset (Fin k)) (X : Fin k),
      (∀ i, i ∉ J₁ ∪ K₁ ↔ i = X) → (∀ i, i ∉ J₂ ∪ K₂ ↔ i = X) →
      ¬ (J₁ ⊆ palette c hc x s ∧ J₂ ⊆ palette c hc x (s + (sixty : Angles))) := by
  obtain ⟨a, ha⟩ := direction_exists hy
  have e : x + direction (a : Angles) = y := by rw [ha]; ring
  have hn₁ := avoiding_trace_palette c hc ht₁ hK₁
  have hn₂ := avoiding_trace_palette c hc ht₂ hK₂
  have hd₁ := palette_neighbor_disjoint c hc hw x a
  have hn₂' := (measurePreserving_add_right angularMeasure (sixty : Angles)).quasiMeasurePreserving.ae hn₂
  have hd₂ := (measurePreserving_add_right angularMeasure (sixty : Angles)).quasiMeasurePreserving.ae hd₁
  have hs := palette_sixty_disjoint c hc hw (x + direction (a : Angles))
  filter_upwards [hn₁, hn₂', hd₁, hd₂, hs]
    with s Hn₁ Hn₂ Hd₁ Hd₂ Hs J₁ J₂ X hl₁ hl₂ h
  obtain ⟨hJ₁, hJ₂⟩ := h
  have Hd₁' : Disjoint (palette c hc y s) (palette c hc x s) := by simpa only [e] using Hd₁
  have Hd₂' : Disjoint (palette c hc y (s + (sixty : Angles)))
      (palette c hc x (s + (sixty : Angles))) := by simpa only [e] using Hd₂
  have Hs' : Disjoint (palette c hc y s) (palette c hc y (s + (sixty : Angles))) := by
    simpa only [e] using Hs
  exact Hs' (palette_block_ban hc hl₁ hl₂ hJ₁ hJ₂ Hn₁ Hn₂ Hd₁' Hd₂')

end EuclideanFiveColor
end
end OAI
