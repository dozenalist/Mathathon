import Mathlib

namespace OAI

noncomputable section

open MeasureTheory

namespace Problem160

abbrev Plane := EuclideanSpace ℝ (Fin 2)

def ProperColoring (k : ℕ) : Prop :=
  ∃ c : Plane → Fin k,
    ∀ x y : Plane, dist x y = 1 → c x ≠ c y

def planeChromaticNumber : ℕ :=
  sInf {k : ℕ | ProperColoring k}

end Problem160

end

end OAI
