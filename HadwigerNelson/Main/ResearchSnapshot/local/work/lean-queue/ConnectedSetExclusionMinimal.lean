-- Local audit copy: same theorem bodies, explicit imports replacing umbrella Mathlib.
-- Pinned Lean 4.34.1 and Mathlib revision; not full-project integration.
/-
Supervisor / simplify-verification block.
One general principle behind the paper's connected-set exclusion (Prop. 7.1 of the paper,
"connectedness of `K` implies that every point of the straddling region `Delta(K)` is at unit
distance from a point of `K`"), and the two theorems of
`lean/OAI/Geometry/PlaneColoring/ConnectedUnitFree.lean` re-derived from it in a few lines each.

Nothing here imports the development: only Mathlib.  Statements of the two corollaries are the
same as the development's (the first is in fact strengthened to a strict inequality, which the
intermediate value theorem gives directly).
-/
import Mathlib.Topology.Order.IntermediateValue
import Mathlib.Analysis.Normed.Group.Real
import Mathlib.Analysis.Normed.Group.Continuity
import Mathlib.Analysis.Normed.Group.Uniform
import Mathlib.Tactic.Push
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring

namespace SupervisorVerify

open Set

/-- **The single principle.**  If `f` is continuous on a preconnected set `C` and never takes the
value `c` there, then `f` is everywhere `< c` on `C` or everywhere `> c` on `C`.

This is the whole content of "a preconnected set avoiding a level set of a continuous function
cannot straddle it"; the intermediate value theorem supplies it. -/
theorem preconnected_forall_lt_or_forall_gt {E : Type*} [TopologicalSpace E]
    {C : Set E} {f : E → ℝ} {c : ℝ} (hC : IsPreconnected C) (hf : ContinuousOn f C)
    (hne : ∀ x ∈ C, f x ≠ c) : (∀ x ∈ C, f x < c) ∨ (∀ x ∈ C, f x > c) := by
  by_contra h
  push_neg at h
  obtain ⟨⟨a, ha, hac⟩, b, hb, hbc⟩ := h
  have hlt : c < f a := lt_of_le_of_ne hac (Ne.symm (hne a ha))
  have hgt : f b < c := lt_of_le_of_ne hbc (hne b hb)
  have hmem : c ∈ f '' C :=
    hC.intermediate_value hb ha hf ⟨hgt.le, hlt.le⟩
  obtain ⟨x, hx, hxc⟩ := hmem
  exact hne x hx hxc

/-- Paper §7, (7.1) and the sentence following it: a preconnected `C` cannot straddle the unit
circle about `z` unless it meets that circle.  Same statement as
`OAI.EuclideanFiveColor.not_straddle_of_isPreconnected`. -/
theorem unitFree_not_straddle {E : Type*} [NormedAddCommGroup E] {C : Set E}
    (hC : IsPreconnected C) {z : E} (h : ∀ q ∈ C, ‖z - q‖ ≠ 1) :
    ¬ ((∃ q ∈ C, ‖z - q‖ < 1) ∧ ∃ q ∈ C, 1 < ‖z - q‖) := by
  rintro ⟨⟨q₁, hq₁, h₁⟩, q₂, hq₂, h₂⟩
  have hcont : ContinuousOn (fun q : E => ‖z - q‖) C :=
    (continuous_const.sub continuous_id).norm.continuousOn
  rcases preconnected_forall_lt_or_forall_gt hC hcont h with hall | hall
  · exact absurd h₂ (not_lt.2 (hall q₂ hq₂).le)
  · exact absurd h₁ (not_lt.2 (hall q₁ hq₁).le)

/-- **Connected unit-free sets have pairwise distance `< 1`.**  This is the theorem
`OAI.EuclideanFiveColor.diam_le_one_of_preconnected_unitFree` with the conclusion the intermediate
value theorem actually yields; it implies that statement (and, with the unit-free hypothesis,
is equivalent to it).  Note the proof needs no product set `C x C`: apply the principle to the
single function `y ↦ ‖x - y‖`. -/
theorem unitFree_pairwise_lt {E : Type*} [NormedAddCommGroup E] {C : Set E}
    (hC : IsPreconnected C) (h : ∀ x ∈ C, ∀ y ∈ C, ‖x - y‖ ≠ 1) :
    ∀ x ∈ C, ∀ y ∈ C, ‖x - y‖ < 1 := by
  intro x hx y hy
  have hcont : ContinuousOn (fun q : E => ‖x - q‖) C :=
    (continuous_const.sub continuous_id).norm.continuousOn
  have hne : ∀ q ∈ C, ‖x - q‖ ≠ 1 := fun q hq => h x hx q hq
  rcases preconnected_forall_lt_or_forall_gt hC hcont hne with hall | hall
  · exact hall y hy
  · exact absurd (hall x hx) (by simp)

/-- The development's statement follows from the strict one. -/
theorem diam_le_one_of_preconnected_unitFree' {E : Type*} [NormedAddCommGroup E] {C : Set E}
    (hC : IsPreconnected C) (h : ∀ x ∈ C, ∀ y ∈ C, ‖x - y‖ ≠ 1) :
    ∀ x ∈ C, ∀ y ∈ C, ‖x - y‖ ≤ 1 :=
  fun x hx y hy => (unitFree_pairwise_lt hC h x hx y hy).le

/-- **The bound one cannot improve.**  No uniform strict bound holds: for every `ε > 0` there is a
preconnected unit-free set with two points at distance exactly `1 - ε`.  So `diam <= 1` is sharp
and no counting argument may replace it by `diam <= 1 - ε`. -/
theorem unitFree_sharp (ε : ℝ) (hε : 0 < ε) (hε1 : ε < 1) :
    ∃ C : Set ℝ, IsPreconnected C ∧ (∀ x ∈ C, ∀ y ∈ C, dist x y ≠ 1) ∧
      ∃ x ∈ C, ∃ y ∈ C, dist x y = 1 - ε := by
  have hpos : (0:ℝ) < (1 - ε) / 2 := by linarith
  have hlt : (1 - ε) / 2 < 1 / 2 := by linarith
  refine ⟨Ioo (-(1/2) : ℝ) (1/2), isPreconnected_Ioo, ?_,
    -((1 - ε) / 2), ⟨by linarith, by linarith⟩,
    (1 - ε) / 2, ⟨by linarith, by linarith⟩, ?_⟩
  · intro x hx y hy hxy
    have h : |x - y| < 1 := by
      rw [abs_lt]
      constructor <;> nlinarith [hx.1, hx.2, hy.1, hy.2]
    rw [Real.dist_eq] at hxy
    linarith
  · rw [Real.dist_eq, show -((1 - ε) / 2) - (1 - ε) / 2 = -(1 - ε) by ring, abs_neg,
      abs_of_pos (by linarith : (0:ℝ) < 1 - ε)]

end SupervisorVerify

#print axioms SupervisorVerify.preconnected_forall_lt_or_forall_gt
#print axioms SupervisorVerify.unitFree_not_straddle
#print axioms SupervisorVerify.unitFree_pairwise_lt
#print axioms SupervisorVerify.unitFree_sharp

#print axioms SupervisorVerify.diam_le_one_of_preconnected_unitFree'
