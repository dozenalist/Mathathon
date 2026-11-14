import Mathlib
open scoped IsMulCommutative
example {A : Type*} [Ring A] [StarRing A] [Algebra ℂ A] (s : StarSubalgebra ℂ A) [IsMulCommutative s] : CommRing s := inferInstance
example {A : Type*} [Ring A] [StarRing A] [Algebra ℂ A] (s : StarSubalgebra ℂ A) [IsMulCommutative s] : CommMonoid s := inferInstance
