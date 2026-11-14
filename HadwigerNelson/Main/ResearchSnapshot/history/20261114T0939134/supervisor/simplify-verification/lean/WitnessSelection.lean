/-
  supervisor/simplify-verification — block 10.
  A reusable selection principle: from "witnesses of arbitrarily small positive scale" build a
  SEQUENCE OF WHOLE WITNESSES whose scales strictly decrease and are explicitly bounded by 1/(n+1).

  Why this shape: the paper (Lemma 7.4) asks for `ε_n ↓ 0` *together with* the disk families `H_n` and
  the maps `g_n`. One may not shrink `ε` while freezing `H` and `g` — shrinking ε changes π^ε and hence
  the whole family. What one MAY do is select *among whole witnesses*: every witness is carried intact,
  and strict decrease is obtained by making the (n+1)-st budget half of the n-th witness's scale.
  This file formalises exactly that, with the witness type abstract and the extra predicates carried
  either as an explicit `P` or inside the witness type.

  NO dependency on the OAI development. No `sorry`, `admit`, `native_decide`, `opaque`, no custom
  axiom. Ordinary definitions and `Classical.choice` only.

  INFORMAL PROOF.
  Let `scale : W → ℝ` and let `hsmall : ∀ ε > 0, ∃ w, P w ∧ 0 < scale w ∧ scale w < ε`.
  Define `w_0` from `hsmall 1` and, given `w_n` with `0 < scale w_n`, set
  `b_n := min (scale w_n / 2) (1/(n+1)) > 0` and let `w_{n+1}` be a witness with
  `P w_{n+1}`, `0 < scale w_{n+1}` and `scale w_{n+1} < b_n`. Then
    * `scale w_{n+1} < b_n ≤ scale w_n / 2 < scale w_n`  — strict decrease;
    * `scale w_{n+1} < b_n ≤ 1/(n+1) = 1/((n+1))`        — the explicit bound at index n+1;
    * `scale w_0 < 1 = 1/(0+1)`                          — the bound at index 0.
  Hence `scale w_n < 1/(n+1)` for all n, and since `1/(n+1) → 0` the scales tend to zero. QED.
  (The last sentence is recorded as the explicit bound here; turning it into `Tendsto` needs a squeeze
  lemma, deliberately kept OUT of this file — see the note at the end.)

  IMPORTS: `Mathlib` (deliberately conservative: the proofs use `linarith` and `positivity`). A narrow
  cone is possible but NOT verified: `Mathlib.Data.Real.Basic` + `Mathlib.Algebra.Order.Field.Basic` +
  `Mathlib.Tactic.Linarith` + `Mathlib.Tactic.Positivity`.
-/
import Mathlib

namespace WitnessSelection

variable {W : Type*}

/-- A witness is *good* for the predicate `P` when `P` holds and its scale is positive. -/
def Good (scale : W → ℝ) (P : W → Prop) (w : W) : Prop := P w ∧ 0 < scale w

/-- Pick a good witness with scale below a given positive budget. -/
noncomputable def pickAt (scale : W → ℝ) (P : W → Prop)
    (hsmall : ∀ ε : ℝ, 0 < ε → ∃ w : W, Good scale P w ∧ scale w < ε)
    (ε : ℝ) (hε : 0 < ε) : {w : W // Good scale P w} :=
  ⟨Classical.choose (hsmall ε hε), (Classical.choose_spec (hsmall ε hε)).1⟩

/-- The picked witness respects the budget. -/
theorem pickAt_lt (scale : W → ℝ) (P : W → Prop)
    (hsmall : ∀ ε : ℝ, 0 < ε → ∃ w : W, Good scale P w ∧ scale w < ε)
    (ε : ℝ) (hε : 0 < ε) : scale (pickAt scale P hsmall ε hε).1 < ε :=
  (Classical.choose_spec (hsmall ε hε)).2

/-- The recursive selection. Each step's budget is *half of the previous witness's scale*, capped by
`1/(n+1)`; the previous witness itself supplies the positivity needed to make the budget positive. -/
noncomputable def sel (scale : W → ℝ) (P : W → Prop)
    (hsmall : ∀ ε : ℝ, 0 < ε → ∃ w : W, Good scale P w ∧ scale w < ε) :
    ℕ → {w : W // Good scale P w}
  | 0 => pickAt scale P hsmall 1 one_pos
  | (n + 1) =>
      let prev := sel scale P hsmall n
      let ε := min (scale prev.1 / 2) (1 / ((n : ℝ) + 1))
      pickAt scale P hsmall ε
        (lt_min (by linarith [prev.2.2]) (by positivity))

/-- The scale of the selected witness is bounded by `1/(n+1)`, and strictly decreases. -/
theorem sel_bound (scale : W → ℝ) (P : W → Prop)
    (hsmall : ∀ ε : ℝ, 0 < ε → ∃ w : W, Good scale P w ∧ scale w < ε) :
    (∀ n, scale ((sel scale P hsmall n).1) < 1 / ((n : ℝ) + 1)) ∧
      (∀ n, scale ((sel scale P hsmall (n + 1)).1) < scale ((sel scale P hsmall n).1)) := by
  have hstep : ∀ n, scale ((sel scale P hsmall (n + 1)).1) <
      min (scale ((sel scale P hsmall n).1) / 2) (1 / ((n : ℝ) + 1)) := by
    intro n
    exact pickAt_lt scale P hsmall _ _
  constructor
  · intro n
    cases n with
    | zero => simpa using pickAt_lt scale P hsmall 1 one_pos
    | succ k =>
        have h := hstep k
        have h2 : scale ((sel scale P hsmall (k + 1)).1) < 1 / ((k : ℝ) + 1) :=
          lt_of_lt_of_le h (min_le_right _ _)
        simpa [Nat.cast_add, Nat.cast_one] using h2
  · intro n
    have h := hstep n
    have h2 : scale ((sel scale P hsmall (n + 1)).1) < scale ((sel scale P hsmall n).1) / 2 :=
      lt_of_lt_of_le h (min_le_left _ _)
    have h3 : 0 < scale ((sel scale P hsmall n).1) := (sel scale P hsmall n).2.2
    linarith

/-- **The selection principle.** From witnesses of arbitrarily small positive scale, a sequence of
whole witnesses whose scales strictly decrease and satisfy `scale (w n) < 1/(n+1)` — hence tend to
zero. Every witness is carried intact: the predicate `P` holds at every index, and no witness data is
frozen while the scale changes. -/
theorem exists_strictAnti_scale (scale : W → ℝ) (P : W → Prop)
    (hsmall : ∀ ε : ℝ, 0 < ε → ∃ w : W, Good scale P w ∧ scale w < ε) :
    ∃ w : ℕ → W, (∀ n, P (w n)) ∧ (∀ n, 0 < scale (w n)) ∧
      (∀ n, scale (w (n + 1)) < scale (w n)) ∧ (∀ n, scale (w n) < 1 / ((n : ℝ) + 1)) := by
  refine ⟨fun n => (sel scale P hsmall n).1, fun n => (sel scale P hsmall n).2.1,
    fun n => (sel scale P hsmall n).2.2, (sel_bound scale P hsmall).2,
    (sel_bound scale P hsmall).1⟩

/-- The plain (no extra predicate) instance, showing the `P` parameter is optional in practice. -/
theorem exists_strictAnti_scale' {scale : W → ℝ}
    (hsmall : ∀ ε : ℝ, 0 < ε → ∃ w : W, 0 < scale w ∧ scale w < ε) :
    ∃ w : ℕ → W, (∀ n, 0 < scale (w n)) ∧ (∀ n, scale (w (n + 1)) < scale (w n)) ∧
      (∀ n, scale (w n) < 1 / ((n : ℝ) + 1)) :=
  exists_strictAnti_scale scale (fun _ => True) fun ε hε => by
    obtain ⟨w, hp, hlt⟩ := hsmall ε hε
    exact ⟨w, ⟨trivial, hp⟩, hlt⟩

/-! ## What this file does not do

* It does not state `Tendsto (fun n => scale (w n)) atTop (𝓝 0)`. That is one squeeze step from
  `scale (w n) < 1/(n+1)` and `1/(n+1) → 0`; it is kept in a separate file so that a name mismatch in
  the squeeze lemma cannot break the selection theorem above.
* It says nothing about disk families, `FullApprox`, or §6.3.4; it does not touch Lemma 6.7.
-/

end WitnessSelection

#print axioms WitnessSelection.pickAt_lt
#print axioms WitnessSelection.sel_bound
#print axioms WitnessSelection.exists_strictAnti_scale
#print axioms WitnessSelection.exists_strictAnti_scale'
