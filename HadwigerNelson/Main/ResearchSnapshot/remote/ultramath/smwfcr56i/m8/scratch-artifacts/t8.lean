import Mathlib
open MeasureTheory
example {α β : Type*} [MeasurableSpace α] [MeasurableSpace β] (μ : Measure α) (f : α → β) :
    (μ.map f) Set.univ = μ Set.univ := rfl
example {α β : Type*} [MeasurableSpace α] [MeasurableSpace β] (μ : Measure α) (f : α → β) :
    IsProbabilityMeasure (μ.map f) := ⟨by rw [show (μ.map f) Set.univ = μ Set.univ from rfl, measure_univ]⟩
