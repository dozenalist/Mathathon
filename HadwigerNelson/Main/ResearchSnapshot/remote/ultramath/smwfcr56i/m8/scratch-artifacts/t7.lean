import Mathlib
open MeasureTheory
example {α β : Type*} [MeasurableSpace α] [MeasurableSpace β] (μ : Measure α) (f : α → β) :
    (μ.map f) Set.univ = μ Set.univ := by simp
example {α β : Type*} [MeasurableSpace α] [MeasurableSpace β] (μ : Measure α) [IsProbabilityMeasure μ]
    (f : α → β) : IsProbabilityMeasure (μ.map f) := ⟨by simp⟩
example {α β : Type*} [MeasurableSpace α] [MeasurableSpace β] (μ : Measure α) [IsProbabilityMeasure μ]
    (f : α → β) : IsProbabilityMeasure (μ.map f) := inferInstance
