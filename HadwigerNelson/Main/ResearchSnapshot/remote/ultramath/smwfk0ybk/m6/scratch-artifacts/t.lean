import Mathlib
example (s t : Finset (Fin 6)) : Decidable (s.Nonempty) := inferInstance
example (s t : Finset (Fin 6)) : Decidable (Disjoint s t) := inferInstance
example (s t : Finset (Fin 6)) : Decidable (s ∩ t = ∅) := inferInstance
example (s : Finset (Fin 6)) : Decidable (s.card ≠ 0) := inferInstance
