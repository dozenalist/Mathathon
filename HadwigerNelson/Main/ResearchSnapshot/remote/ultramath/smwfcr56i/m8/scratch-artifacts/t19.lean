import Mathlib
open scoped IsMulCommutative
example {A : Type*} [Ring A] [StarRing A] (s : StarSubalgebra ℂ A) [IsMulCommutative s] : CommRing s := inferInstance
#check @IsMulCommutative
#check @CommCStarAlgebra
#check @StarSubalgebra.instCommRing
