import OAI.Geometry.PlaneColoring.BorelTransfer
import OAI.Geometry.PlaneColoring.Converse
namespace OAI

noncomputable section
open MeasureTheory Filter Topology Set
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

end EuclideanFiveColor
end

end OAI
