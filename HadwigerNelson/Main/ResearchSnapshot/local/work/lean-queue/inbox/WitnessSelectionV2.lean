/-
  supervisor/simplify-verification — block 11 (repair of V1 after the local run).
  Monotone WITNESS selection: from witnesses of arbitrarily small positive scale, a sequence of whole
  witnesses whose scales strictly decrease and are bounded by `1/(n+1)` — hence tend to zero.

  V1 FAILED locally at four points; all four are repaired below and the changes are listed here.
    (1) `min (scale (sel n) / 2) (1/(n+1))` left the positivity proof `hε` uninferable.
        REPAIR: the successor budget is now `1/(n+2)` (i.e. `1/((n+1)+1)`), the positivity proof is
        supplied explicitly with `half_pos` and `positivity`, and the budget is written inline as the
        argument of `pickAt` (no `let` for the equation compiler to lose).
    (2) `sel` was defined by the equation compiler, so proofs had to unfold it.
        REPAIR: `sel` is now `Nat.rec` applied to a *named* step function `stepF`, and the recursion
        equations are `rfl` lemmas `sel_zero` / `sel_succ` — no unfolding heuristics needed.
    (3) `h2` had denominator `k+1` while the goal had `k+1+1`.
        REPAIR: the step bound is stated with `1/((k:ℝ)+2)` and the goal is reached by
        `heq : ((k+1:ℕ):ℝ) + 1 = (k:ℝ) + 2` proved by `push_cast; ring`, then `rw [heq]`.
    (4) the plain corollary returned an extra `∀ n, True` conjunct.
        REPAIR: the main theorem is destructured with `obtain ⟨w, -, hpos, hanti, hbound⟩`.
  New in this version: the `Tendsto` conclusion, via the checked-in Mathlib lemmas
  `squeeze_zero` (`Mathlib/Topology/MetricSpace/Pseudo/Lemmas.lean:38`) and
  `tendsto_one_div_add_atTop_nhds_zero_nat` (`Mathlib/Analysis/SpecificLimits/Basic.lean:71`).

  THE POINT OF THE SHAPE. One may not shrink `ε` while freezing the accompanying data (`H`, `g`):
  shrinking ε changes π^ε. One MAY select among *whole witnesses*, and strict decrease is obtained by
  making the next budget half of the previous witness's scale.

  INFORMAL PROOF. `w_0` from ε = 1. Given `w_n` with `scale w_n > 0`, put
  `b_n := min (scale w_n / 2) (1/(n+2)) > 0` and let `w_{n+1}` be a witness with `P w_{n+1}`,
  `0 < scale w_{n+1}` and `scale w_{n+1} < b_n`. Then `scale w_{n+1} < b_n ≤ scale w_n/2 < scale w_n`
  (strict decrease) and `scale w_{n+1} < 1/(n+2) = 1/((n+1)+1)` (public bound at index n+1); at n = 0,
  `scale w_0 < 1 = 1/(0+1)`. Hence `scale w_n < 1/(n+1)` for all n, and since `1/(n+1) → 0`, the
  scales tend to zero. QED

  No `sorry`, `admit`, `native_decide`, `opaque`, no custom axiom, no dependency on the development.
  `Classical.choice` enters only through `pickAt`'s `Classical.choose`.
-/
import Mathlib.Tactic
import Mathlib.Topology.MetricSpace.Pseudo.Lemmas
import Mathlib.Analysis.SpecificLimits.Basic

namespace WitnessSelection

variable {W : Type*}

/-- A witness is good for `P` when `P` holds and its scale is positive. -/
def Good (scale : W → ℝ) (P : W → Prop) (w : W) : Prop := P w ∧ 0 < scale w

/-- Pick a good witness with scale below a given positive budget. -/
noncomputable def pickAt (scale : W → ℝ) (P : W → Prop)
    (hsmall : ∀ ε : ℝ, 0 < ε → ∃ w : W, Good scale P w ∧ scale w < ε)
    (ε : ℝ) (hε : 0 < ε) : {w : W // Good scale P w} :=
  ⟨Classical.choose (hsmall ε hε), (Classical.choose_spec (hsmall ε hε)).1⟩

/-- The picked witness respects its budget. -/
theorem pickAt_lt (scale : W → ℝ) (P : W → Prop)
    (hsmall : ∀ ε : ℝ, 0 < ε → ∃ w : W, Good scale P w ∧ scale w < ε)
    (ε : ℝ) (hε : 0 < ε) : scale (pickAt scale P hsmall ε hε).1 < ε :=
  (Classical.choose_spec (hsmall ε hε)).2

/-- One step of the selection: budget `min (scale prev / 2) (1/(n+2))`, derived from the previous
witness itself. -/
noncomputable def stepF (scale : W → ℝ) (P : W → Prop)
    (hsmall : ∀ ε : ℝ, 0 < ε → ∃ w : W, Good scale P w ∧ scale w < ε)
    (n : ℕ) (prev : {w : W // Good scale P w}) : {w : W // Good scale P w} :=
  pickAt scale P hsmall (min (scale prev.1 / 2) (1 / ((n : ℝ) + 2)))
    (lt_min (half_pos prev.2.2) (by positivity))

/-- The selection, as `Nat.rec` — so the recursion equations below are `rfl`. -/
noncomputable def sel (scale : W → ℝ) (P : W → Prop)
    (hsmall : ∀ ε : ℝ, 0 < ε → ∃ w : W, Good scale P w ∧ scale w < ε) :
    ℕ → {w : W // Good scale P w} :=
  Nat.rec (pickAt scale P hsmall 1 one_pos) (stepF scale P hsmall)

theorem sel_zero (scale : W → ℝ) (P : W → Prop)
    (hsmall : ∀ ε : ℝ, 0 < ε → ∃ w : W, Good scale P w ∧ scale w < ε) :
    sel scale P hsmall 0 = pickAt scale P hsmall 1 one_pos := rfl

theorem sel_succ (scale : W → ℝ) (P : W → Prop)
    (hsmall : ∀ ε : ℝ, 0 < ε → ∃ w : W, Good scale P w ∧ scale w < ε) (n : ℕ) :
    sel scale P hsmall (n + 1) = stepF scale P hsmall n (sel scale P hsmall n) := rfl

/-- The step bound: the new scale is below the step's budget. -/
theorem sel_step_lt (scale : W → ℝ) (P : W → Prop)
    (hsmall : ∀ ε : ℝ, 0 < ε → ∃ w : W, Good scale P w ∧ scale w < ε) (n : ℕ) :
    scale ((sel scale P hsmall (n + 1)).1) <
      min (scale ((sel scale P hsmall n).1) / 2) (1 / ((n : ℝ) + 2)) := by
  rw [sel_succ]
  exact pickAt_lt scale P hsmall _ _

/-- The public bound `scale (w n) < 1/(n+1)`. -/
theorem sel_bound (scale : W → ℝ) (P : W → Prop)
    (hsmall : ∀ ε : ℝ, 0 < ε → ∃ w : W, Good scale P w ∧ scale w < ε) :
    ∀ n, scale ((sel scale P hsmall n).1) < 1 / ((n : ℝ) + 1) := by
  intro n
  cases n with
  | zero =>
      rw [sel_zero]
      simpa using pickAt_lt scale P hsmall 1 one_pos
  | succ k =>
      have h2 : scale ((sel scale P hsmall (k + 1)).1) < 1 / ((k : ℝ) + 2) :=
        lt_of_lt_of_le (sel_step_lt scale P hsmall k) (min_le_right _ _)
      have heq : ((k + 1 : ℕ) : ℝ) + 1 = (k : ℝ) + 2 := by push_cast; ring
      rw [heq]
      exact h2

/-- Strict decrease of the scales. -/
theorem sel_anti (scale : W → ℝ) (P : W → Prop)
    (hsmall : ∀ ε : ℝ, 0 < ε → ∃ w : W, Good scale P w ∧ scale w < ε) :
    ∀ n, scale ((sel scale P hsmall (n + 1)).1) < scale ((sel scale P hsmall n).1) := by
  intro n
  have h := lt_of_lt_of_le (sel_step_lt scale P hsmall n) (min_le_left _ _)
  have hpos : 0 < scale ((sel scale P hsmall n).1) := (sel scale P hsmall n).2.2
  linarith

/-- Scales tend to zero. -/
theorem sel_tendsto (scale : W → ℝ) (P : W → Prop)
    (hsmall : ∀ ε : ℝ, 0 < ε → ∃ w : W, Good scale P w ∧ scale w < ε) :
    Tendsto (fun n => scale ((sel scale P hsmall n).1)) atTop (𝓝 0) :=
  squeeze_zero (fun n => ((sel scale P hsmall n).2.2).le)
    (fun n => (sel_bound scale P hsmall n).le)
    tendsto_one_div_add_atTop_nhds_zero_nat

/-- **The selection principle.** Whole witnesses, strictly decreasing scales, tending to zero, with the
extra predicate carried at every index. -/
theorem exists_strictAnti_scale (scale : W → ℝ) (P : W → Prop)
    (hsmall : ∀ ε : ℝ, 0 < ε → ∃ w : W, Good scale P w ∧ scale w < ε) :
    ∃ w : ℕ → W, (∀ n, P (w n)) ∧ (∀ n, 0 < scale (w n)) ∧
      (∀ n, scale (w (n + 1)) < scale (w n)) ∧ (∀ n, scale (w n) < 1 / ((n : ℝ) + 1)) ∧
      Tendsto (fun n => scale (w n)) atTop (𝓝 0) :=
  ⟨fun n => (sel scale P hsmall n).1, fun n => (sel scale P hsmall n).2.1,
    fun n => (sel scale P hsmall n).2.2, sel_anti scale P hsmall, sel_bound scale P hsmall,
    sel_tendsto scale P hsmall⟩

/-- The plain instance: `P := True`, destructured to drop the vacuous conjunct. -/
theorem exists_strictAnti_scale' {scale : W → ℝ}
    (hsmall : ∀ ε : ℝ, 0 < ε → ∃ w : W, 0 < scale w ∧ scale w < ε) :
    ∃ w : ℕ → W, (∀ n, 0 < scale (w n)) ∧ (∀ n, scale (w (n + 1)) < scale (w n)) ∧
      (∀ n, scale (w n) < 1 / ((n : ℝ) + 1)) ∧ Tendsto (fun n => scale (w n)) atTop (𝓝 0) := by
  obtain ⟨w, -, hpos, hanti, hbound, hlim⟩ :=
    exists_strictAnti_scale scale (fun _ => True) (fun ε hε => by
      obtain ⟨v, hp, hlt⟩ := hsmall ε hε
      exact ⟨v, ⟨trivial, hp⟩, hlt⟩)
  exact ⟨w, hpos, hanti, hbound, hlim⟩

end WitnessSelection

#print axioms WitnessSelection.pickAt_lt
#print axioms WitnessSelection.sel_bound
#print axioms WitnessSelection.sel_tendsto
#print axioms WitnessSelection.exists_strictAnti_scale
#print axioms WitnessSelection.exists_strictAnti_scale'
