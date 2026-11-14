import Mathlib

/-!
# Core lemmas for relative singularity at a factor with ergodic relative product

These are the finite inputs of the four-step argument that replaces the phase-collision
induction of the paper's Lemma 2.7 in the only place that lemma is used (Section 3.3,
terminal factor).  See `relative-singularity.md`.
-/

open MeasureTheory

namespace SwarmM11

variable {V : Type*} [NormedAddCommGroup V] [InnerProductSpace ℝ V]

/-- **Gram-matrix obstruction.**  Three vectors whose Gram matrix is
`(r^2/2) • (1 + J)` with `r > 0` are linearly independent, so they need
`finrank ≥ 3`. -/
theorem gram_obstruction [Module.Finite ℝ V] (hV : Module.finrank ℝ V ≤ 2) {r : ℝ}
    (hr : 0 < r) (u1 u2 u3 : V)
    (h11 : inner ℝ u1 u1 = r ^ 2) (h22 : inner ℝ u2 u2 = r ^ 2) (h33 : inner ℝ u3 u3 = r ^ 2)
    (h12 : inner ℝ u1 u2 = r ^ 2 / 2) (h13 : inner ℝ u1 u3 = r ^ 2 / 2)
    (h23 : inner ℝ u2 u3 = r ^ 2 / 2) : False := by
  classical
  have hc : (0:ℝ) < r ^ 2 / 2 := by positivity
  have hli : LinearIndependent ℝ ![u1, u2, u3] := by
    rw [Fintype.linearIndependent_iffₛ]
    intro f g hfg k
    set w : Fin 3 → ℝ := fun k => f k - g k with hw
    have h0 : (∑ i, w i • ![u1, u2, u3] i) = 0 := by
      have hsplit : (∑ i, w i • ![u1, u2, u3] i)
          = (∑ i, f i • ![u1, u2, u3] i) - (∑ i, g i • ![u1, u2, u3] i) := by
        rw [← Finset.sum_sub_distrib]
        exact Finset.sum_congr rfl (fun i _ => by rw [hw]; simp [sub_smul])
      rw [hsplit, hfg, sub_self]
    have hexp : (∑ i, w i • ![u1, u2, u3] i) = w 0 • u1 + w 1 • u2 + w 2 • u3 := by
      rw [Fin.sum_univ_three]
      simp
    have e1 : (2 * w 0 + w 1 + w 2) * (r ^ 2 / 2) = 0 := by
      have h := congrArg (fun z => inner ℝ z u1) h0
      rw [inner_zero_left, hexp, inner_add_left, inner_add_left, real_inner_smul_left,
        real_inner_smul_left, real_inner_smul_left, real_inner_comm u1 u2, real_inner_comm u1 u3,
        h11, h12, h13] at h
      linear_combination h
    have e2 : (2 * w 1 + w 0 + w 2) * (r ^ 2 / 2) = 0 := by
      have h := congrArg (fun z => inner ℝ z u2) h0
      rw [inner_zero_left, hexp, inner_add_left, inner_add_left, real_inner_smul_left,
        real_inner_smul_left, real_inner_smul_left, real_inner_comm u2 u3, h12, h22, h23] at h
      linear_combination h
    have e3 : (2 * w 2 + w 0 + w 1) * (r ^ 2 / 2) = 0 := by
      have h := congrArg (fun z => inner ℝ z u3) h0
      rw [inner_zero_left, hexp, inner_add_left, inner_add_left, real_inner_smul_left,
        real_inner_smul_left, real_inner_smul_left, h13, h23, h33] at h
      linear_combination h
    have n1 : 2 * w 0 + w 1 + w 2 = 0 := by
      rcases mul_eq_zero.mp e1 with h | h
      · exact h
      · exact absurd h hc.ne'
    have n2 : 2 * w 1 + w 0 + w 2 = 0 := by
      rcases mul_eq_zero.mp e2 with h | h
      · exact h
      · exact absurd h hc.ne'
    have n3 : 2 * w 2 + w 0 + w 1 = 0 := by
      rcases mul_eq_zero.mp e3 with h | h
      · exact h
      · exact absurd h hc.ne'
    have h0' : w 0 = 0 := by linarith
    have h1' : w 1 = 0 := by linarith
    have h2' : w 2 = 0 := by linarith
    have : w k = 0 := by
      fin_cases k
      · exact h0'
      · exact h1'
      · exact h2'
    simp only [hw] at this
    linarith
  have hcard := hli.fintype_card_le_finrank (R := ℝ) (M := V)
  simp only [Fintype.card_fin] at hcard
  omega

/-- **Four equidistant points need dimension at least three**, in usable form. -/
theorem no_four_points [Module.Finite ℝ V] (hV : Module.finrank ℝ V ≤ 2) {r : ℝ}
    (hr : 0 < r) (a b c d : V)
    (hab : dist a b = r) (hac : dist a c = r) (had : dist a d = r)
    (hbc : dist b c = r) (hbd : dist b d = r) (hcd : dist c d = r) : False := by
  have hnorm : ∀ x y : V, dist x y = r → ‖x - y‖ = r := fun x y h => by
    rwa [dist_eq_norm] at h
  have inner_half : ∀ x y : V, ‖x‖ = r → ‖y‖ = r → ‖x - y‖ = r →
      inner ℝ x y = r ^ 2 / 2 := by
    intro x y hx hy hxy
    have h := norm_sub_sq_real x y
    rw [hxy, hx, hy] at h
    nlinarith
  set u1 : V := b - a with hu1
  set u2 : V := c - a with hu2
  set u3 : V := d - a with hu3
  have hn1 : ‖u1‖ = r := hnorm b a (by rw [dist_comm]; exact hab)
  have hn2 : ‖u2‖ = r := hnorm c a (by rw [dist_comm]; exact hac)
  have hn3 : ‖u3‖ = r := hnorm d a (by rw [dist_comm]; exact had)
  refine gram_obstruction hV hr u1 u2 u3 ?_ ?_ ?_ ?_ ?_ ?_
  · rw [real_inner_self_eq_norm_sq, hn1, pow_two]
  · rw [real_inner_self_eq_norm_sq, hn2, pow_two]
  · rw [real_inner_self_eq_norm_sq, hn3, pow_two]
  · refine inner_half u1 u2 hn1 hn2 ?_
    have h : u1 - u2 = b - c := by rw [hu1, hu2]; abel
    rw [h]; exact hnorm b c hbc
  · refine inner_half u1 u3 hn1 hn3 ?_
    have h : u1 - u3 = b - d := by rw [hu1, hu3]; abel
    rw [h]; exact hnorm b d hbd
  · refine inner_half u2 u3 hn2 hn3 ?_
    have h : u2 - u3 = c - d := by rw [hu2, hu3]; abel
    rw [h]; exact hnorm c d hcd

/-- A probability measure on the plane whose independent difference law is concentrated on a
circle of positive radius cannot exist. -/
theorem no_measure_fixed_difference_norm {r : ℝ} (hr : 0 < r)
    (lam : Measure (EuclideanSpace ℝ (Fin 2))) [IsProbabilityMeasure lam]
    (h : (lam.prod lam) {p : EuclideanSpace ℝ (Fin 2) × EuclideanSpace ℝ (Fin 2) |
      ‖p.1 - p.2‖ = r} = 1) : False := by
  classical
  set ν : Measure (EuclideanSpace ℝ (Fin 2) × EuclideanSpace ℝ (Fin 2)) := lam.prod lam with hνdef
  have : IsProbabilityMeasure ν := by rw [hνdef]; infer_instance
  set μ : Measure ((EuclideanSpace ℝ (Fin 2) × EuclideanSpace ℝ (Fin 2)) ×
      (EuclideanSpace ℝ (Fin 2) × EuclideanSpace ℝ (Fin 2))) := ν.prod ν with hμdef
  have : IsProbabilityMeasure μ := by rw [hμdef]; infer_instance
  set A : Set (EuclideanSpace ℝ (Fin 2) × EuclideanSpace ℝ (Fin 2)) :=
    {p | ‖p.1 - p.2‖ = r} with hAdef
  have hAmeas : MeasurableSet A := by
    rw [hAdef]
    exact (measurableSet_singleton r).preimage
      ((continuous_fst.sub continuous_snd).norm.measurable)
  have hfst : ν.map Prod.fst = lam := by rw [hνdef]; simp
  have hsnd : ν.map Prod.snd = lam := by rw [hνdef]; simp
  have key : ∀ m : ((EuclideanSpace ℝ (Fin 2) × EuclideanSpace ℝ (Fin 2)) ×
      (EuclideanSpace ℝ (Fin 2) × EuclideanSpace ℝ (Fin 2))) →
      (EuclideanSpace ℝ (Fin 2) × EuclideanSpace ℝ (Fin 2)),
      Measurable m → μ.map m = ν → ∀ᵐ q ∂μ, ‖(m q).1 - (m q).2‖ = r := by
    intro m hm hmap
    have hmeas : MeasurableSet {q | ‖(m q).1 - (m q).2‖ = r} :=
      (measurableSet_singleton r).preimage ((hm.fst.sub hm.snd).norm)
    have h1 : μ {q | ‖(m q).1 - (m q).2‖ = r} = 1 := by
      have hset : {q | ‖(m q).1 - (m q).2‖ = r} = m ⁻¹' A := rfl
      rw [hset, ← Measure.map_apply hm hAmeas, hmap]
      exact h
    rw [MeasureTheory.ae_iff,
      show {q | ¬ ‖(m q).1 - (m q).2‖ = r} = {q | ‖(m q).1 - (m q).2‖ = r}ᶜ from rfl,
      measure_compl hmeas (by simp), h1]
    simp
  have e1 : ∀ᵐ q ∂μ, ‖q.1.1 - q.1.2‖ = r :=
    key Prod.fst measurable_fst (by rw [hμdef]; simp)
  have e2 : ∀ᵐ q ∂μ, ‖q.2.1 - q.2.2‖ = r :=
    key Prod.snd measurable_snd (by rw [hμdef]; simp)
  have e3 : ∀ᵐ q ∂μ, ‖q.1.1 - q.2.1‖ = r :=
    key (Prod.map Prod.fst Prod.fst) (measurable_fst.prodMap measurable_fst) (by
      rw [hμdef, ← Measure.map_prod_map ν ν measurable_fst measurable_fst, hfst, ← hνdef])
  have e4 : ∀ᵐ q ∂μ, ‖q.1.1 - q.2.2‖ = r :=
    key (Prod.map Prod.fst Prod.snd) (measurable_fst.prodMap measurable_snd) (by
      rw [hμdef, ← Measure.map_prod_map ν ν measurable_fst measurable_snd, hfst, hsnd, ← hνdef])
  have e5 : ∀ᵐ q ∂μ, ‖q.1.2 - q.2.1‖ = r :=
    key (Prod.map Prod.snd Prod.fst) (measurable_snd.prodMap measurable_fst) (by
      rw [hμdef, ← Measure.map_prod_map ν ν measurable_snd measurable_fst, hsnd, hfst, ← hνdef])
  have e6 : ∀ᵐ q ∂μ, ‖q.1.2 - q.2.2‖ = r :=
    key (Prod.map Prod.snd Prod.snd) (measurable_snd.prodMap measurable_snd) (by
      rw [hμdef, ← Measure.map_prod_map ν ν measurable_snd measurable_snd, hsnd, ← hνdef])
  have hall : ∀ᵐ q ∂μ, (‖q.1.1 - q.1.2‖ = r ∧ ‖q.2.1 - q.2.2‖ = r ∧
      ‖q.1.1 - q.2.1‖ = r ∧ ‖q.1.1 - q.2.2‖ = r ∧
      ‖q.1.2 - q.2.1‖ = r ∧ ‖q.1.2 - q.2.2‖ = r) := by
    filter_upwards [e1, e2, e3, e4, e5, e6] with q h1 h2 h3 h4 h5 h6
    exact ⟨h1, h2, h3, h4, h5, h6⟩
  obtain ⟨q, h1, h2, h3, h4, h5, h6⟩ := hall.exists
  have hfin : Module.finrank ℝ (EuclideanSpace ℝ (Fin 2)) ≤ 2 := by
    rw [finrank_euclideanSpace_fin]
  exact no_four_points (V := EuclideanSpace ℝ (Fin 2)) hfin hr q.1.1 q.1.2 q.2.1 q.2.2
    (by rw [dist_eq_norm]; exact h1) (by rw [dist_eq_norm]; exact h3)
    (by rw [dist_eq_norm]; exact h4) (by rw [dist_eq_norm]; exact h5)
    (by rw [dist_eq_norm]; exact h6) (by rw [dist_eq_norm]; exact h2)

end SwarmM11

/-! Axiom check: only the standard three. -/
#print axioms SwarmM11.gram_obstruction
#print axioms SwarmM11.no_four_points
#print axioms SwarmM11.no_measure_fixed_difference_norm
