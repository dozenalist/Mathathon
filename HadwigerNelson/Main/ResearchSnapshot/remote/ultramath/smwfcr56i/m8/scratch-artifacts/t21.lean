import Mathlib
open scoped IsMulCommutative
variable {A : Type*} [Ring A] [StarRing A] [Algebra ℂ A] [StarModule ℂ A]
example (s : StarSubalgebra ℂ A) [IsMulCommutative s] : CommRing s := inferInstance
example (s : StarSubalgebra ℂ A) [IsMulCommutative s] : CommMonoid s := inferInstance
example (s : StarSubalgebra ℂ A) [IsMulCommutative s] : CommCStarAlgebra s := inferInstance
