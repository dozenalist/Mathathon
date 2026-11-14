/- Semantic statement freeze for the headline results.

Each `example` states a headline result exactly as published in this repository and
closes it by the named declaration from the tree under test.  If a restructure changes
the statement (adds a hypothesis, strengthens the colouring notion, weakens `¬ ∃`, …)
one of these fails to elaborate.  Run under both toolchains. -/
import OAI.Geometry.PlaneColoring.Five
import OAI.Geometry.PlaneColoring.Seven
import OAI.Geometry.PlaneColoring.Transfer
import OAI.Geometry.PlaneColoring.Chromatic
import OAI.Geometry.PlaneColoring.NullSetRobust

namespace Certify

-- 1. the sprint's headline, fully unfolded: no 5-colouring separates every unit pair
example : ¬ ∃ c : ℂ → Fin 5, ∀ x y : ℂ, ‖x - y‖ = 1 → c x ≠ c y :=
  OAI.EuclideanFiveColor.no_proper_five_coloring

-- 1'. same through the bundled predicate
example : ¬ ∃ c : ℂ → Fin 5, OAI.EuclideanFiveColor.ProperColoring 5 c :=
  OAI.EuclideanFiveColor.no_proper_five_coloring

-- 2. same on the algebraic plane
example : ¬ ∃ c : OAI.PlaneFiveColor.Spectral.E → Fin 5,
    OAI.PlaneFiveColor.LabelModel.Proper 5 c :=
  OAI.EuclideanFiveColor.no_proper_five_coloring_algebraic

-- 3. a proper 7-colouring exists
example : OAI.Problem160.ProperColoring 7 :=
  OAI.Problem160.properColoring_seven

-- 4. proper <-> measurable weak, both directions, all k
example {k : ℕ} [NeZero k] :
    (∃ c : ℂ → Fin k, OAI.EuclideanFiveColor.ProperColoring k c) ↔
      (∃ c : ℂ → Fin k, Measurable c ∧ OAI.EuclideanFiveColor.WeakColoring k c) :=
  OAI.EuclideanFiveColor.proper_iff_weak

-- 5. 6 <= chi(R^2) <= 7
example : 6 ≤ OAI.Problem160.planeChromaticNumber ∧ OAI.Problem160.planeChromaticNumber ≤ 7 :=
  OAI.Problem160.chromaticNumber_bounds

-- 6. lower bound survives deleting any null set
example {Z : Set ℂ} (hZ : MeasureTheory.volume Z = 0) :
    ¬ ∃ c : ℂ → Fin 5, ∀ x ∉ Z, ∀ y ∉ Z, ‖x - y‖ = 1 → c x ≠ c y :=
  OAI.EuclideanFiveColor.not_proper_five_coloring_compl_null hZ

-- 7. the algebraic-plane transfer, both directions
example {k : ℕ} [NeZero k] :
    (∃ c : OAI.PlaneFiveColor.Spectral.E → Fin k, OAI.PlaneFiveColor.LabelModel.Proper k c) ↔
      (∃ c : ℂ → Fin k, OAI.EuclideanFiveColor.ProperColoring k c) :=
  OAI.EuclideanFiveColor.algebraic_colorable_iff

end Certify
