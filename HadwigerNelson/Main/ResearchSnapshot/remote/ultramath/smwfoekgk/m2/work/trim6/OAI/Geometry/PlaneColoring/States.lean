import OAI.Geometry.PlaneColoring.BinaryPalettes

namespace OAI

noncomputable section
open Set
namespace EuclideanFiveColor
def fourGroup (s : Fin 3) : Finset (Fin 5) := if s=0 then {4} else if s=1 then {0,2} else {1,3}
def fourEdge (e : Fin 4) : Finset (Fin 5) :=
  if e=0 then {0,1} else if e=1 then {1,2} else if e=2 then {2,3} else {3,0}
def fourCanonical (p : Finset (Fin 5)) : Fin 3 := if 4∈p then 0 else if 0∈p then 1 else 2
def FourAdmissible (p : Finset (Fin 5)) : Prop :=
  p.Nonempty ∧ p.card≤2 ∧ ∀ e : Fin 4, ¬p⊆fourEdge e
lemma fourGroup_nonempty (s : Fin 3) : (fourGroup s).Nonempty := by
  fin_cases s <;> simp [fourGroup]
lemma four_admissible_group : ∀ p : Finset (Fin 5), FourAdmissible p → fourGroup (fourCanonical p)⊆p := by
  unfold FourAdmissible
  decide
lemma four_group_unique : ∀ p : Finset (Fin 5), p.card≤2 → ∀ s t : Fin 3,
    fourGroup s⊆p → fourGroup t⊆p → s=t := by decide
lemma four_admissible_character : ∀ p : Finset (Fin 5), FourAdmissible p → ∀ s : Fin 3,
    fourGroup s⊆p ↔ fourCanonical p=s := by
  intro p hp s
  constructor
  · intro hs
    exact (four_group_unique p hp.2.1 s (fourCanonical p) hs (four_admissible_group p hp)).symm
  · rintro rfl
    exact four_admissible_group p hp
lemma four_trace_edge : ∀ p : Finset (Fin 5), FourAdmissible p → ∀ i∈fourGroup (fourCanonical p),
    ∃ e : Fin 4, i∉fourEdge e ∧ p\{i}⊆fourEdge e := by
  unfold FourAdmissible
  decide
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology MeasureTheory
namespace EuclideanFiveColor
lemma DensityZero.mono {A B : Set ℂ} {x : ℂ} (hB : DensityZero B x) (hAB : A⊆B) :
    DensityZero A x := by
  apply tendsto_of_tendsto_of_tendsto_of_le_of_le tendsto_const_nhds hB (fun _ => zero_le)
  intro r
  exact ENNReal.div_le_div_right (measure_mono (inter_subset_inter_left _ hAB)) _
lemma DensityZero.union {A B : Set ℂ} {x : ℂ} (hA : DensityZero A x) (hB : DensityZero B x) :
    DensityZero (A∪B) x := by
  have hh := hA.add hB
  rw [add_zero] at hh
  apply tendsto_of_tendsto_of_tendsto_of_le_of_le tendsto_const_nhds hh (fun _ => zero_le)
  intro r
  dsimp only
  rw [← ENNReal.add_div,union_inter_distrib_right]
  exact ENNReal.div_le_div_right (measure_union_le _ _) _
variable {k : ℕ} {c : ℂ → Fin k} (hc : Measurable c)
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology MeasureTheory
namespace EuclideanFiveColor
variable {k : ℕ} {c : ℂ → Fin k}
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology MeasureTheory
namespace EuclideanFiveColor
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology MeasureTheory
namespace EuclideanFiveColor
variable (c : ℂ → Fin 5) (hc : Measurable c)
end EuclideanFiveColor
end

noncomputable section
open MeasureTheory Filter Topology Set
open scoped NNReal
namespace EuclideanFiveColor
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology MeasureTheory
open scoped NNReal
namespace EuclideanFiveColor
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology
namespace EuclideanFiveColor
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology MeasureTheory
open scoped NNReal
namespace EuclideanFiveColor
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology MeasureTheory
namespace EuclideanFiveColor
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology MeasureTheory
namespace EuclideanFiveColor
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology MeasureTheory
open scoped RealInnerProductSpace
namespace EuclideanFiveColor
end EuclideanFiveColor
end

end OAI
