import Mathlib.LinearAlgebra.Dimension.Finite
import Mathlib.LinearAlgebra.FiniteDimensional.Defs
import Mathlib.Analysis.InnerProductSpace.Basic
import Mathlib.MeasureTheory.Measure.Prod
import Mathlib.MeasureTheory.Measure.Typeclasses.Probability

/-! Finite inputs for relative singularity at a factor with ergodic relative product. -/

open MeasureTheory

namespace RelativeSingularity

variable {V : Type*} [NormedAddCommGroup V] [InnerProductSpace ℝ V]

/-- Three vectors with Gram matrix `(r^2/2) • (1 + J)`, `r > 0`, are independent. -/
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

/-- Four equidistant points need `finrank ≥ 3`. -/
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

end RelativeSingularity
