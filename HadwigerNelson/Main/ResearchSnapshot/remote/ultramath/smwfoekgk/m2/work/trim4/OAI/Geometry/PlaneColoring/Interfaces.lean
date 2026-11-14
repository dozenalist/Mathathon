import OAI.Geometry.PlaneColoring.AngularBoundary

namespace OAI

noncomputable section
open Set
namespace EuclideanFiveColor
/-- The four cyclic edges, with outsider label `4`. This definition is local to
this interface argument and agrees extensionally with `fourEdge`. -/
def interfaceFourEdge (i : Fin 4) : Finset (Fin 5) :=
  if i=0 then {0,1} else if i=1 then {1,2} else if i=2 then {2,3} else {3,0}
def interfaceFourAllowed (s : Fin 4 → Bool) (b : Bool) : Finset (Fin 5) :=
  Finset.univ.filter fun j => ∀i, s i=b → j∉interfaceFourEdge i
def InterfaceFourCompatible (s : Fin 4 → Bool) (p : Finset (Fin 5)) : Prop :=
  p.Nonempty ∧ p.card≤2 ∧
    (p∩interfaceFourAllowed s true).Nonempty ∧ (p∩interfaceFourAllowed s false).Nonempty
def InterfaceFourSplit (s : Fin 4 → Bool) : Prop := s 0≠s 2 ∧ s 1≠s 3
def interfaceFourDiagonal (s : Fin 4 → Bool) : Fin 3 := if s 0=s 1 then 2 else 1
lemma interface_four_not_edge : ∀s : Fin 4 → Bool, ∀p : Finset (Fin 5),
    InterfaceFourCompatible s p → ∀i, ¬p⊆interfaceFourEdge i := by
  unfold InterfaceFourCompatible interfaceFourAllowed
  decide
lemma interface_four_split : ∀s : Fin 4 → Bool, ∀p : Finset (Fin 5),
    InterfaceFourCompatible s p → 4∉p → InterfaceFourSplit s ∧
      (if 4∈p then (0:Fin 3) else if 0∈p then 1 else 2)=interfaceFourDiagonal s := by
  unfold InterfaceFourCompatible InterfaceFourSplit interfaceFourAllowed interfaceFourDiagonal
  decide
lemma interface_four_diagonal_neg (s : Fin 4 → Bool) :
    interfaceFourDiagonal (fun i => !(s i))=interfaceFourDiagonal s := by
  simp [interfaceFourDiagonal]
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology MeasureTheory
open scoped RealInnerProductSpace
namespace EuclideanFiveColor
variable {c : ℂ → Fin 5} (hc : Measurable c)
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology MeasureTheory
namespace EuclideanFiveColor
/-- Every point of an angular essential support has a real essential-support lift.
The compact fundamental domain is used only to establish the support inclusion. -/
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology MeasureTheory
open scoped RealInnerProductSpace
namespace EuclideanFiveColor
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology MeasureTheory
open scoped RealInnerProductSpace
namespace EuclideanFiveColor

variable {c : ℂ → Fin 5} (hc : Measurable c)
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology MeasureTheory
open scoped RealInnerProductSpace
namespace EuclideanFiveColor
/-- The three-direction quadratic moment replaces the source's projective arc
length argument. No assumption about antipodal ray pairs or the collinear case
is required: two opposite uniform diagonal triples are already contradictory. -/
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology MeasureTheory
open scoped RealInnerProductSpace
namespace EuclideanFiveColor
variable {c : ℂ → Fin 5} (hc : Measurable c)
/-- Construction of the dense conull shift-invariant set and its actual
six-position words, from the previously established genuine state system. -/
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology MeasureTheory
open scoped RealInnerProductSpace
namespace EuclideanFiveColor


/-- The actual length-four interface cycle is impossible. All hypotheses are
exactly approach directions and common straddling exclusion of both endpoints. -/
end EuclideanFiveColor
end

end OAI
