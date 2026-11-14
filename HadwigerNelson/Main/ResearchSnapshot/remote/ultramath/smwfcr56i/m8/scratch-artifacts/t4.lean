import Mathlib
open MeasureTheory
example {G : Type*} [MeasurableSpace G] [CommGroup G] [MeasurableMul₂ G] [MeasurableInv G] :
    Measurable (fun p : G × G => p.1 / p.2) := by fun_prop
example {G : Type*} [MeasurableSpace G] [CommGroup G] [MeasurableMul₂ G] [MeasurableInv G] :
    Measurable (fun p : G × G => p.1 / p.2) := measurable_fst.div measurable_snd
