import OAI.Geometry.PlaneColoring.ConeObstruction

namespace OAI.EuclideanFiveColor

noncomputable section
open Set Filter Topology MeasureTheory

def coneSurvivorAngles : Fin 3 → ℝ := ![0,0,Real.pi/3]

def coneSurvivorExclusions : Fin 3 → Finset (Fin 6) := ![{0,1},{1,2},{2,3}]

/-- A direct actual-interface consumer of CC60. These are the first three
edges of the specified direction tuple `(0,0,1,3,3,4)`, measured in sixth turns.
No finite palette witness is used as a geometric premise. -/
theorem cone_survivor_001334_impossible {c : ℂ → Fin 6}
    (hc : Measurable c) (hw : WeakColoring 6 c) {x : ℂ} {K : Fin 3 → Set ℂ}
    (hK : ∀ i, ApproachingContinuum x (K i)
      (Circle.exp (coneSurvivorAngles i) : ℂ))
    (hexcl : ∀ i, ∀ j ∈ coneSurvivorExclusions i,
      Disjoint (spatialSupport c j) (Straddle (K i))) : False := by
  have hangle : ∀ i : Fin 3, coneSurvivorAngles i ∈
      Icc (Real.pi/6-Real.pi/6) (Real.pi/6+Real.pi/6) := by
    intro i
    fin_cases i <;> dsimp [coneSurvivorAngles] <;> constructor <;> linarith [Real.pi_pos]
  have hres : ∀ j : Fin 6, (∀ i, j ∉ coneSurvivorExclusions i) → j = 4 ∨ j = 5 := by
    intro j hj
    have h0 := hj 0
    have h1 := hj 1
    have h2 := hj 2
    fin_cases j <;> norm_num [coneSurvivorExclusions] at *
  exact closed60_exclusions_not_binary hc hw coneSurvivorExclusions hK
    (φ := Real.pi/6) hangle hexcl hres

end
end OAI.EuclideanFiveColor
