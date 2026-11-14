import Mathlib
open MeasureTheory
example {X : Type*} [MeasurableSpace X] {ι : Type*} (m : ι → MeasurableSpace X)
    (T : MeasurableSpace X) (hm : ∀ i, m i ≤ T) : (⨆ i, m i) ≤ T := iSup_le hm
example {X : Type*} [MeasurableSpace X] {ι : Type*} (m : ι → MeasurableSpace X)
    (T : MeasurableSpace X) (hm : ∀ i, m i ≤ T) : sSup (Set.range m) ≤ T := sSup_le (Set.forall_range_iff.mpr hm)
