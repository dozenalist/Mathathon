import OAI.Geometry.PlaneColoring.Converse
import OAI.Geometry.PlaneColoring.BorelTransfer

namespace OAI

noncomputable section
open MeasureTheory Filter Topology Set
namespace EuclideanFiveColor

theorem proper_iff_weak {k : ℕ} [NeZero k] :
    (∃ c : ℂ → Fin k, ProperColoring k c) ↔
      (∃ c : ℂ → Fin k, Measurable c ∧ WeakColoring k c) := by
  constructor
  · rintro ⟨c, hc⟩
    obtain ⟨d, hd, hw⟩ := proper_to_borel_weak hc
    exact ⟨d, hd, hw⟩
  · rintro ⟨c, hc, hw⟩
    exact properColoring_of_weak hc hw

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
