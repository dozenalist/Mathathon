import Mathlib
import TightCore
open TightCSP
example : Decidable (IsModel 6 5 (by norm_num) (cellSig 5 cells5) P5) := inferInstance
