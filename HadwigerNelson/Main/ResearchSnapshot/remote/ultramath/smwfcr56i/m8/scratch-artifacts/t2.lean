import Mathlib
open MeasureTheory
example : ENNReal.HolderTriple 2 ⊤ 2 := inferInstance
example {X : Type*} [MeasurableSpace X] (μ : Measure X) (f φ : X → ℂ)
    (hf : MemLp f ⊤ μ) (hφ : MemLp φ 2 μ) : MemLp (fun x => φ x * f x) 2 μ :=
  MemLp.mul' hf hφ
example {X : Type*} [MeasurableSpace X] (μ : Measure X) (f φ : X → ℂ)
    (hf : MemLp f ⊤ μ) (hφ : MemLp φ 2 μ) : MemLp (fun x => φ x * f x) 2 μ :=
  MemLp.mul' (hpqr := ENNReal.HolderTriple.instInfty 2) hf hφ
