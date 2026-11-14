import OAI.Geometry.PlaneColoring.PaletteTransport

namespace OAI

noncomputable section
open MeasureTheory Filter Topology Set
namespace EuclideanFiveColor
variable {k : ℕ} (c : ℂ → Fin k) (hc : Measurable c)
def BinaryCenter (x : ℂ) (i j : Fin k) : Prop :=
  ∀ᵐ t ∂angularMeasure, t ∈ paletteSet c hc x i ∨ t ∈ paletteSet c hc x j
lemma binary_alternation (hw : WeakColoring k c) {x : ℂ} {i j : Fin k}
    (hb : BinaryCenter c hc x i j) :
    ∀ᵐ t ∂angularMeasure, (t+(sixty : Angles) ∈ paletteSet c hc x i ↔ t ∉ paletteSet c hc x i) ∧
      (t ∈ paletteSet c hc x j ↔ t ∉ paletteSet c hc x i) := by
  have hb' := (measurePreserving_add_right angularMeasure (sixty : Angles)).quasiMeasurePreserving.ae hb
  filter_upwards [hb,hb',palette_sixty c hc hw x i,palette_sixty c hc hw x j] with t h h' hi hj
  constructor
  · constructor
    · exact fun ht ht' => hi ht' ht
    · intro hnot
      exact h'.resolve_right (hj (h.resolve_left hnot))
  · constructor
    · intro ht ht'
      rcases h' with hpi | hpj
      · exact hi ht' hpi
      · exact hj ht hpj
    · exact h.resolve_left
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
namespace EuclideanFiveColor
end EuclideanFiveColor
end

noncomputable section
open MeasureTheory Filter Topology
namespace EuclideanFiveColor
instance anglesNontrivial : Nontrivial Angles := by
  have : Nontrivial Circle := ⟨⟨1,-1,by
    intro h
    have hh := congrArg (fun z : Circle => (z : ℂ)) h
    norm_num at hh⟩⟩
  exact AddCircle.homeomorphCircle'.toEquiv.nontrivial
instance angularMeasure_nullSingleton : NullSingletonClass angularMeasure := by
  exact Measure.IsAddHaarMeasure.nullSingletonClass angularMeasure
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
namespace EuclideanFiveColor
end EuclideanFiveColor
end

end OAI
