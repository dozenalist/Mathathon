import OAI.MeasureTheory.CompactFactors.Kernels

namespace OAI

noncomputable section

open scoped ComplexConjugate
open scoped BigOperators
open scoped BigOperators BoundedContinuousFunction
open Filter Topology
open MeasureTheory Filter
open scoped ENNReal ComplexConjugate
open MeasureTheory ProbabilityTheory
open scoped ComplexConjugate
open scoped BigOperators
open scoped BigOperators
open Polynomial
open MeasureTheory
open scoped BigOperators
open MeasureTheory
open scoped BigOperators
open MeasureTheory
open MeasureTheory ProbabilityTheory
open scoped BigOperators
open MeasureTheory
open scoped BigOperators ComplexConjugate
open MeasureTheory ProbabilityTheory
open scoped ENNReal BigOperators
open MeasureTheory Filter
open scoped Topology ENNReal NNReal
open MeasureTheory
open scoped ENNReal
open MeasureTheory ProbabilityTheory
open scoped ENNReal
open MeasureTheory ProbabilityTheory
open MeasureTheory ProbabilityTheory
open MeasureTheory ProbabilityTheory
open scoped ENNReal

namespace EuclideanFiveColor.CompactFunctions
open MeasureTheory
open scoped BigOperators
variable {K X Y : Type*} [SMul K X] [MeasurableSpace X] [MeasurableSpace Y]








lemma compact_conj {μ : Measure X} {q : X → Y} {H : X → ℂ}
    (hH : Compact (K := K) μ q H) : Compact (K := K) μ q (fun x => star (H x)) := by
  intro ε hε
  obtain ⟨r, B, C, F, hB, hC, hm, hb, ha⟩ := hH ε hε
  refine ⟨r, B, C, fun i x => star (F i x), hB, hC,
    fun i => Complex.continuous_conj.measurable.comp (hm i), ?_, ?_⟩
  · intro x; simpa using hb x
  · intro k
    obtain ⟨a, ham, hab, hai, hae⟩ := ha k
    refine ⟨fun y i => star (a y i), (Measurable.of_eval (fun i => Complex.continuous_conj.measurable.comp ((measurable_pi_iff.mp ham) i))), ?_, ?_, ?_⟩
    · intro y
      rw [pi_norm_le_iff_of_nonneg hB]
      intro i
      simpa using (norm_le_pi_norm (a y) i).trans (hab y)
    · have hs (x : X) : (∑ i, star (a (q x) i) * star (F i x)) = star (∑ i, a (q x) i * F i x) := by
        simp only [star_sum, star_mul, mul_comm]
      simpa only [hs, dist_star_star] using hai
    · have hs (x : X) : (∑ i, star (a (q x) i) * star (F i x)) = star (∑ i, a (q x) i * F i x) := by
        simp only [star_sum, star_mul, mul_comm]
      simpa only [hs, dist_star_star] using hae




end EuclideanFiveColor.CompactFunctions



end

end OAI
