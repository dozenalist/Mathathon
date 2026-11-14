import OAI.Geometry.PlaneColoring.Converse
import OAI.Geometry.PlaneColoring.BorelTransfer
open Filter MeasureTheory Set Topology

namespace OAI

noncomputable section
namespace EuclideanFiveColor

/-- The transfer theorem, both directions: a proper colouring of the plane exists iff a weak
measurable one does. -/
theorem proper_iff_weak {k : ℕ} [NeZero k] :
    (∃ c : ℂ → Fin k, ProperColoring k c) ↔
      (∃ c : ℂ → Fin k, Measurable c ∧ WeakColoring k c) := by
  constructor
  · rintro ⟨c, hc⟩
    obtain ⟨d, hd, hw⟩ := proper_to_borel_weak hc
    exact ⟨d, hd, hw⟩
  · rintro ⟨c, hc, hw⟩
    exact properColoring_of_weak hc hw

/-- The chromatic number of the plane is the chromatic number of the countable algebraic plane:
`E` is `k`-colourable iff the plane is. -/
theorem algebraic_colorable_iff {k : ℕ} [NeZero k] :
    (∃ c : PlaneFiveColor.Spectral.E → Fin k, PlaneFiveColor.LabelModel.Proper k c) ↔
      (∃ c : ℂ → Fin k, ProperColoring k c) := by
  constructor
  · rintro ⟨c, hc⟩
    obtain ⟨d, hd, hw⟩ := proper_to_borel_weak_algebraic hc
    exact properColoring_of_weak hd hw
  · rintro ⟨c, hc⟩
    exact ⟨fun x => c x, fun x y h => hc x y h⟩

end EuclideanFiveColor
end

end OAI
