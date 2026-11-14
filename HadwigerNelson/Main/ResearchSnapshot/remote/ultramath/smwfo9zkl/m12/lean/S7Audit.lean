/-
Section 7 at six colours: two machine-checked steps of the audit
Swarm smwfo9zkl, member m12, direction d9.  Companion to `S7-INPUT.md`.

Both lemmas below are quoted in `S7-INPUT.md` and are the only places where the
printed proof of Section 7 uses finite combinatorics:

* Lemma 6.1 (Step 5): a clique in a forest has at most two vertices.  This is the
  step which carries the thresholded disk averages (7.4) into the one-skeleton `G`
  of the simplex, and it involves NO palette bound: the passage is produced by the
  acyclicity of `Gamma_z` off the cyclic locus `L`.

* Step 2: the threshold `alpha < 1/k`.  The printed constant is `alpha < 1/5` (five
  probabilities summing to one); at `k = 6` it becomes `alpha < 1/6`, and that is the
  only numerical `k`-dependence of Section 7 besides the cycle-length range.

Check with:   lean lean/S7Audit.lean
-/
import Mathlib

set_option linter.unusedSectionVars false
set_option linter.unusedSimpArgs false

namespace S7Audit

open Finset

variable {V : Type*} [Fintype V] {G : SimpleGraph V}

/-- **Lemma 6.1 of `S7-INPUT.md`.** Every clique of an acyclic graph has at most two
vertices; equivalently, a forest has no triangle.  This is the label-blind step of
paper Lemma 7.4 -- outside the cyclic locus the positive coordinates of (7.4) form a
clique in the forest `Gamma_z`, hence number at most two, and a two-element clique is
a forest edge, so the value lies in the one-skeleton. -/
theorem card_le_two_of_isAcyclic_of_isClique (hG : G.IsAcyclic) {C : Finset V}
    (hC : G.IsClique C) : C.card ≤ 2 := by
  by_contra h
  have h2 : 3 ≤ C.card := by omega
  have h3 : G.CliqueFree 3 := hG.cliqueFree (by norm_num)
  exact (SimpleGraph.CliqueFree.mono h2 h3) C ⟨hC, rfl⟩

/-- **Step 2 of `S7-INPUT.md`.** Let `p : Fin k -> R` be probability coordinates
(`p >= 0`, `sum p = 1`) and let `alpha < 1/k`.  Then some coordinate exceeds `alpha`,
so the denominator in (7.4) is positive.  The printed hypothesis `alpha < 1/5` is the
case `k = 5`; at `k = 6` the constant is `alpha < 1/6`. -/
theorem exists_gt_of_sum_eq_one {k : Nat} (hk : 0 < k) {p : Fin k → ℝ}
    (_h0 : ∀ i, 0 ≤ p i) (hsum : ∑ i, p i = 1) {α : ℝ}
    (hα : α < ((k : ℝ))⁻¹) : ∃ i, α < p i := by
  by_contra h
  have hle : ∀ i, p i ≤ α := fun i => le_of_not_gt (fun hlt => h ⟨i, hlt⟩)
  have hkR : (0 : ℝ) < k := by exact_mod_cast hk
  have h4 : (∑ _i : Fin k, α) = (k : ℝ) * α := by
    rw [sum_const, nsmul_eq_mul]
    simp
  have h5 : (1 : ℝ) ≤ (k : ℝ) * α := by
    rw [← hsum, ← h4]
    exact sum_le_sum (fun i _ => hle i)
  have h6 : (k : ℝ) * α < 1 := by
    have hlt := mul_lt_mul_of_pos_left hα hkR
    rwa [mul_inv_cancel₀ (ne_of_gt hkR)] at hlt
  linarith

/-- The six-label instance of the threshold: at `k = 6` the printed `alpha < 1/5`
must be replaced by `alpha < 1/6`. -/
theorem exists_gt_six {p : Fin 6 → ℝ} (h0 : ∀ i, 0 ≤ p i)
    (hsum : ∑ i, p i = 1) {α : ℝ} (hα : α < 1 / 6) : ∃ i, α < p i := by
  refine exists_gt_of_sum_eq_one (by norm_num) h0 hsum ?_
  simpa using hα

/- Sanity checks that the statements are the intended ones and are not vacuous. -/

/-- The hypotheses of `exists_gt_of_sum_eq_one` are satisfiable at `k = 6`
(uniform probability coordinates), so the lemma is not vacuous. -/
example : ∃ p : Fin 6 → ℝ, (∀ i, 0 ≤ p i) ∧ (∑ i, p i = 1) := by
  refine ⟨fun _ => 1 / 6, fun _ => by norm_num, ?_⟩
  simp [Finset.sum_const, Finset.card_fin]

/-- Consequently, at `k = 6` some coordinate exceeds `1/7`, as Step 2 requires. -/
example : ∃ p : Fin 6 → ℝ, (∀ i, 0 ≤ p i) ∧ (∑ i, p i = 1) ∧ ∃ i, (1 / 7 : ℝ) < p i := by
  refine ⟨fun _ => 1 / 6, fun _ => by norm_num, ?_, ?_⟩
  · simp [Finset.sum_const, Finset.card_fin]
  · exact exists_gt_six (fun _ => by norm_num)
      (by simp [Finset.sum_const, Finset.card_fin]) (by norm_num)

/-- The clique hypothesis of `card_le_two_of_isAcyclic_of_isClique` is satisfiable
for an acyclic graph (the bottom graph), so the lemma is not vacuous. -/
example : (⊥ : SimpleGraph (Fin 6)).IsAcyclic ∧
    ((⊥ : SimpleGraph (Fin 6)).IsClique (∅ : Finset (Fin 6))) :=
  ⟨SimpleGraph.isAcyclic_bot, by intro a ha; simp at ha⟩

end S7Audit
