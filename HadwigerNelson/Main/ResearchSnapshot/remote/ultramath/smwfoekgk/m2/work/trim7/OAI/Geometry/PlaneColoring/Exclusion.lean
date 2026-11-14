import OAI.Geometry.PlaneColoring.AngularBoundary

namespace OAI

noncomputable section
open Set
namespace EuclideanFiveColor
def fiveDiag (i : Fin 5) : Finset (Fin 5) := {i,i+2}
def fiveAdj (i j : Fin 5) : Prop := i+1=j ∨ j+1=i
instance (i j : Fin 5) : Decidable (fiveAdj i j) := inferInstanceAs (Decidable (_ ∨ _))
def fiveEdge (i : Fin 5) : Finset (Fin 5) := {i,i+1}
def FiveAdmissible (p : Finset (Fin 5)) : Prop :=
  p.Nonempty ∧ p.card≤2 ∧ ∀ i : Fin 5, ¬p⊆fiveEdge i
def fiveCanonical (p : Finset (Fin 5)) : Fin 5 :=
  if p=fiveDiag 0 then 0 else if p=fiveDiag 1 then 1 else if p=fiveDiag 2 then 2 else
    if p=fiveDiag 3 then 3 else 4
lemma five_admissible_diag : ∀p : Finset (Fin 5), FiveAdmissible p → p=fiveDiag (fiveCanonical p) := by
  unfold FiveAdmissible
  decide
lemma five_diag_disjoint : ∀i j : Fin 5, Disjoint (fiveDiag i) (fiveDiag j) ↔ fiveAdj i j := by decide
lemma five_adj_four : ∀i j : Fin 5, fiveAdj i j → ∃ X : Fin 5, ∀k, k∉fiveDiag i∪fiveDiag j ↔ k=X := by decide
lemma five_no_common_adj : ∀I : Finset (Fin 5), I.Nonempty → (∀k,∃i∈I,k∉fiveDiag i) →
    ∃i∈I,∃j∈I,fiveAdj i j := by decide
lemma five_forced_label : ∀i j X : Fin 5, fiveAdj i j →
    (∀k,k∉fiveDiag i∪fiveDiag j ↔ k=X) → ∀p : Finset (Fin 5),
    Disjoint p (fiveDiag i) → ¬p⊆fiveDiag j → X∈p := by decide
end EuclideanFiveColor
end

noncomputable section
namespace EuclideanFiveColor
/-- Both actual one-sided strip restrictions on a palette. -/
def SideCompatible (s : Fin 5 → Bool) (p : Finset (Fin 5)) : Prop :=
  p.card≤2 ∧ (p∩sideAllowed s true).Nonempty ∧ (p∩sideAllowed s false).Nonempty
instance (s : Fin 5 → Bool) (p : Finset (Fin 5)) : Decidable (SideCompatible s p) :=
  inferInstanceAs (Decidable (_∧_∧_))
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology MeasureTheory
open scoped RealInnerProductSpace
namespace EuclideanFiveColor
variable (c : ℂ → Fin 5) (hc : Measurable c)
end EuclideanFiveColor
end

end OAI
