/-
  Machine-checked certificate for the k = 6 single-centre R-orbit count.

  Setting (see AUDIT.md, Theorem R): c a weak measurable 6-colouring, x a typical
  centre with c x = 0 whose transition graph Gamma_x contains a 6-cycle.
  A palette is admissible iff it is a nonempty subset of {1,...,5} of size <= 3
  that is not contained in a cycle edge {v, v+1}.  (Singletons never occur: every
  label of C_6 lies in a cycle edge.)  Two consecutive palettes on an R-orbit must
  be disjoint.  Hence the number of admissible six-palette orbit words is the
  number of closed 6-walks in the disjointness graph, i.e. (A^6).trace.

  This file proves, in the kernel (no `native_decide`, axioms
  [propext, Classical.choice, Quot.sound]):
    * palA is exactly the admissible alphabet (16 elements);
    * Aexp is its disjointness matrix;
    * (Aexp^6).trace = 510.

  Check with:  lean k6_orbit_count.lean
-/
import Mathlib

open Finset

/-- The 16 admissible palettes: the 2- and 3-subsets of {1,2,3,4,5} other than the
cycle edges {1,2},{2,3},{3,4},{4,5}. -/
def pal : Fin 16 → Finset (Fin 6)
  | 0 => {1, 3}
  | 1 => {1, 4}
  | 2 => {1, 5}
  | 3 => {2, 4}
  | 4 => {2, 5}
  | 5 => {3, 5}
  | 6 => {1, 2, 3}
  | 7 => {1, 2, 4}
  | 8 => {1, 2, 5}
  | 9 => {1, 3, 4}
  | 10 => {1, 3, 5}
  | 11 => {1, 4, 5}
  | 12 => {2, 3, 4}
  | 13 => {2, 3, 5}
  | 14 => {2, 4, 5}
  | 15 => {3, 4, 5}

/-- Disjointness matrix of the admissible alphabet. -/
def Aformula : Matrix (Fin 16) (Fin 16) ℕ := fun i j => if Disjoint (pal i) (pal j) then 1 else 0

/-- The same matrix written out. -/
def Aexp : Matrix (Fin 16) (Fin 16) ℕ :=
     ![
       ![0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
       ![0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
       ![0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
       ![1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
       ![1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
       ![0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
       ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       ![0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       ![0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       ![0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       ![0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       ![0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       ![1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
       ]

theorem Aexp_eq_Aformula : Aexp = Aformula := by
  ext i j
  fin_cases i <;> fin_cases j <;> decide

/-- The single-centre count at a k = 6 six-cycle centre. -/
theorem k6_orbit_count : (Aformula ^ 6).trace = 510 := by
  rw [← Aexp_eq_Aformula]
  decide

#print axioms k6_orbit_count
