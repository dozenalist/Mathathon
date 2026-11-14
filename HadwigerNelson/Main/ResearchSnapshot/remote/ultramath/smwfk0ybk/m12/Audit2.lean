import OAI.Geometry.PlaneColoring.Chromatic

/-! Trust audit (swarm smwfk0ybk, m12, d15).

`OAI.EuclideanFiveColor.WeakColoring` is the predicate that carries the entire
five-colour obstruction: every lemma in Accumulation / PaletteDensity /
PaletteTransport / ... consumes it as a hypothesis, and
`no_measurable_weak_five_coloring` refutes it at k = 5.  Nothing in the bundle
exhibits a single model of it, so the obstruction theorem could in principle be
vacuously true (predicate unsatisfiable for structural reasons, e.g. a wrong
`direction` or `angularMeasure`).  Below: it is inhabited at k = 7, inside the
same development, by composing the 7-colouring with the transfer.  Hence the
obstruction is not vacuous and the k = 5 / k = 7 threshold is real at the level
of this predicate. -/

namespace Audit

open OAI

theorem weakColoring_seven_inhabited :
    ∃ d : ℂ → Fin 7, Measurable d ∧ EuclideanFiveColor.WeakColoring 7 d := by
  obtain ⟨c, hc⟩ := Problem160.properColoring_seven
  exact EuclideanFiveColor.proper_to_borel_weak (Problem160.properColoring_of_plane hc)

/-- The same predicate is empty at k = 5 (with measurability): the threshold. -/
theorem weakColoring_five_empty :
    ¬ ∃ d : ℂ → Fin 5, Measurable d ∧ EuclideanFiveColor.WeakColoring 5 d := by
  rintro ⟨d, hd, hw⟩
  exact EuclideanFiveColor.no_measurable_weak_five_coloring hd hw

#print axioms Audit.weakColoring_seven_inhabited
#print axioms Audit.weakColoring_five_empty
#print axioms EuclideanFiveColor.proper_to_borel_weak
#print axioms EuclideanFiveColor.proper_to_borel_weak_algebraic
#print axioms EuclideanFiveColor.sample_field
#print axioms PlaneFiveColor.LabelModel.exists_label_field
#print axioms Problem160.properColoring_seven
#print axioms Problem160.exists_measurable_proper_seven
#print axioms Problem160.weakMeasurableColoring_seven

end Audit
