/-
  Statement-fidelity check for paper Definition 1.2 (weak measurable k-coloring).

  Paper Definition 1.2. Let k be a positive integer, S^1 c R^2 the unit circle, sigma its
  normalized arc-length measure. A weak measurable k-coloring is a Lebesgue measurable
  function c : R^2 -> {1,...,k}, with color classes A_i = c^{-1}{i}, such that for every R > 0

      sum_{i=1}^{k}  int_{B(0,R)} int_{S^1} 1_{A_i}(x) 1_{A_i}(x+u) dsigma(u) dx = 0.

  The Lean bundle's definition (OAI.Geometry.PlaneColoring.Coloring) is

      WeakColoring k c  :=  AEMeasurable c volume  /\  forall^a (x,t),
                             c x /= c (x + direction t).

  This file proves, in the toolchain the bundle targets (Lean 4.34.1 + pinned Mathlib),
  that the two conditions are equivalent, and that the paper's colour-class sum is exactly
  the indicator of the bad-pair set.  Nothing below is asserted in prose only.

  Check:  cd repo && source scripts/env4341.sh && cd lean && \
          lean ../.ultramath/smwfcr56i/m1/Def12.lean
-/
import OAI.Geometry.PlaneColoring.Coloring

open MeasureTheory
open scoped ENNReal
namespace OAI
namespace EuclideanFiveColor

/-- The set of "bad pairs": a plane point and a direction at which the colour repeats at
unit distance.  Its complement is the bundle's almost-everywhere condition. -/
def BadPair (k : ℕ) (c : ℂ → Fin k) : Set (ℂ × Angles) :=
  {p | c p.1 = c (p.1 + direction p.2)}

lemma badPair_measurable {k : ℕ} {c : ℂ → Fin k} (hc : Measurable c) :
    MeasurableSet (BadPair k c) := by
  apply measurableSet_eq_fun
  · exact hc.comp measurable_fst
  · exact hc.comp (measurable_fst.add (direction_continuous.measurable.comp measurable_snd))

/-- The paper's colour-class sum is exactly the indicator of the bad-pair set: for all
`x`, `y` one has `sum_i 1_{A_i}(x) 1_{A_i}(y) = 1` iff `c x = c y`, and `0` otherwise. -/
lemma sum_class_indicators (k : ℕ) (c : ℂ → Fin k) (x y : ℂ) :
    (∑ i : Fin k, (if c x = i then (1:ℝ≥0∞) else 0) * (if c y = i then (1:ℝ≥0∞) else 0))
      = if c x = c y then 1 else 0 := by
  by_cases h : c x = c y
  · rw [if_pos h, ← h, Finset.sum_eq_single (c x)]
    · simp
    · intro b _ hb; simp [Ne.symm hb]
    · intro h; exact absurd (Finset.mem_univ _) h
  · rw [if_neg h]
    apply Finset.sum_eq_zero
    intro i _
    by_cases h1 : c x = i
    · have h2 : ¬ (c y = i) := fun h2 => h (h1.trans h2.symm)
      simp [h1, h2]
    · simp [h1]

/-- Definition 1.2 of the manuscript: for every `R > 0` the double integral over
`B(0,R) x S^1` of the colour-class sum vanishes.  Written as the measure of the bad-pair
set cut down to `B(0,R) x S^1`, which is what that nonnegative iterated integral equals
(`paperCondition_integral`). -/
def WeakColoringPaper (k : ℕ) (c : ℂ → Fin k) : Prop :=
  AEMeasurable c volume ∧
    ∀ R : ℝ, 0 < R →
      (volume.prod angularMeasure)
        (BadPair k c ∩ ((Metric.ball (0:ℂ) R) ×ˢ (Set.univ : Set Angles))) = 0

/-- Definition 1.2 with the indicator integral written out, for measurable `c`
(which is exactly the measurability the paper asks for). -/
lemma paperCondition_integral {k : ℕ} {c : ℂ → Fin k} (hc : Measurable c) (R : ℝ) :
    (∫⁻ p in ((Metric.ball (0:ℂ) R) ×ˢ (Set.univ : Set Angles)),
        (if c p.1 = c (p.1 + direction p.2) then (1:ℝ≥0∞) else 0)
          ∂(volume.prod angularMeasure))
      = (volume.prod angularMeasure)
          (BadPair k c ∩ ((Metric.ball (0:ℂ) R) ×ˢ (Set.univ : Set Angles))) := by
  have hs : MeasurableSet
      ((Metric.ball (0:ℂ) R) ×ˢ (Set.univ : Set Angles) : Set (ℂ × Angles)) :=
    measurableSet_ball.prod MeasurableSet.univ
  have hB : MeasurableSet (BadPair k c) := badPair_measurable hc
  have he : (fun p : ℂ × Angles =>
        if c p.1 = c (p.1 + direction p.2) then (1:ℝ≥0∞) else 0)
      = (BadPair k c).indicator (fun _ => (1:ℝ≥0∞)) := by
    funext p
    by_cases h : c p.1 = c (p.1 + direction p.2) <;> simp [BadPair, h]
  rw [he, ← lintegral_indicator hs]
  have hstep : ∀ p : ℂ × Angles,
      ((Metric.ball (0:ℂ) R) ×ˢ (Set.univ : Set Angles) : Set (ℂ × Angles)).indicator
        ((BadPair k c).indicator (fun _ => (1:ℝ≥0∞))) p
      = (((Metric.ball (0:ℂ) R) ×ˢ (Set.univ : Set Angles) : Set (ℂ × Angles))
          ∩ BadPair k c).indicator (fun _ => (1:ℝ≥0∞)) p := by
    intro p
    by_cases h1 : p ∈ ((Metric.ball (0:ℂ) R) ×ˢ (Set.univ : Set Angles) : Set (ℂ × Angles))
    · by_cases h2 : p ∈ BadPair k c <;> simp [h1, h2]
    · simp [h1]
  simp only [hstep]
  exact (lintegral_indicator_one (μ := volume.prod angularMeasure) (hs.inter hB)).trans
    (by rw [Set.inter_comm])

/-- **Definition 1.2 = the bundle's `WeakColoring`.** No hypothesis is needed: the two
conditions are equivalent for every `c : ℂ → Fin k`, so the bundle's definition imposes
nothing that the paper's definition does not, and vice versa. -/
theorem weakColoring_iff_paper (k : ℕ) (c : ℂ → Fin k) :
    WeakColoring k c ↔ WeakColoringPaper k c := by
  constructor
  · intro h
    refine ⟨h.1, fun R _ => ?_⟩
    have hz : (volume.prod angularMeasure) (BadPair k c) = 0 := by
      have h1 := ae_iff.mp h.2
      rwa [show {a : ℂ × Angles | ¬ c a.1 ≠ c (a.1 + direction a.2)} = BadPair k c from by
        ext p; simp only [BadPair, Set.mem_setOf_eq, ne_eq, not_not]] at h1
    exact measure_mono_null Set.inter_subset_left hz
  · rintro ⟨hae, hR⟩
    refine ⟨hae, ?_⟩
    have hset : {a : ℂ × Angles | ¬ c a.1 ≠ c (a.1 + direction a.2)} = BadPair k c := by
      ext p; simp only [BadPair, Set.mem_setOf_eq, ne_eq, not_not]
    rw [ae_iff, hset]
    have hcover : BadPair k c ⊆ ⋃ n : ℕ,
        BadPair k c ∩ ((Metric.ball (0:ℂ) (n:ℝ)) ×ˢ (Set.univ : Set Angles)) := by
      intro p hp
      obtain ⟨n, hn⟩ : ∃ n : ℕ, ‖p.1‖ < (n:ℝ) := exists_nat_gt ‖p.1‖
      exact Set.mem_iUnion.mpr ⟨n, hp, by
        refine ⟨?_, Set.mem_univ _⟩
        simpa only [Metric.mem_ball, dist_zero_right] using hn⟩
    have hnull : ∀ n : ℕ, (volume.prod angularMeasure)
        (BadPair k c ∩ ((Metric.ball (0:ℂ) (n:ℝ)) ×ˢ (Set.univ : Set Angles))) = 0 := by
      intro n
      rcases Nat.eq_zero_or_pos n with rfl | hn
      · simp
      · exact hR (n:ℝ) (by exact_mod_cast hn)
    exact measure_mono_null hcover (measure_iUnion_null hnull)

end EuclideanFiveColor
end OAI
