import OAI.Geometry.PlaneColoring.WeakColoring

namespace OAI

noncomputable section
open Filter Topology
open scoped RealInnerProductSpace
namespace EuclideanFiveColor
variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E]
  [TopologicalSpace.SeparableSpace E]
def weakHilbert (v : E) : WeakDual ℝ E := StrongDual.toWeakDual (InnerProductSpace.toDual ℝ E v)
omit [TopologicalSpace.SeparableSpace E] in
@[simp] lemma weakHilbert_apply (v w : E) : weakHilbert v w = ⟪v,w⟫ := rfl
lemma exists_finite_weak_subseq {ι : Type*} [Finite ι] (f : ℕ → ι → E) (C : ℝ)
    (hf : ∀ n i, ‖f n i‖ ≤ C) :
    ∃ b : ι → E, ∃ φ : ℕ → ℕ, StrictMono φ ∧
      (∀ i, ‖b i‖ ≤ C) ∧ ∀ i v, Tendsto (fun n => ⟪f (φ n) i,v⟫) atTop (𝓝 ⟪b i,v⟫) := by
  let K : Set (WeakDual ℝ E) := WeakDual.toStrongDual ⁻¹' Metric.closedBall 0 C
  have hK : IsCompact K := WeakDual.isCompact_closedBall 0 C
  let : CompactSpace K := isCompact_iff_compactSpace.mp hK
  let : TopologicalSpace.MetrizableSpace K := WeakDual.metrizable_of_isCompact ℝ E K hK
  let u : ℕ → ι → K := fun n i => ⟨weakHilbert (f n i), by
    simpa only [K,Set.mem_preimage,Metric.mem_closedBall,dist_zero_right,weakHilbert,
      StrongDual.toStrongDual_toWeakDual,LinearIsometryEquiv.norm_map] using hf n i⟩
  obtain ⟨b,_,φ,hφ,hb⟩ := (isCompact_univ : IsCompact (Set.univ : Set (ι → K))).isSeqCompact.subseq_of_frequently_in
    (Filter.Eventually.frequently (Filter.Eventually.of_forall (fun n => Set.mem_univ (u n))))
  refine ⟨fun i => (InnerProductSpace.toDual ℝ E).symm (WeakDual.toStrongDual (b i).1),φ,hφ,?_,?_⟩
  · intro i
    simpa only [LinearIsometryEquiv.norm_map,K,Set.mem_preimage,Metric.mem_closedBall,dist_zero_right] using (b i).2
  · intro i v
    have ht := ((WeakDual.eval_continuous v).comp continuous_subtype_val).tendsto (b i)
      |>.comp ((continuous_apply i).tendsto b |>.comp hb)
    change Tendsto (fun n => ⟪f (φ n) i,v⟫) atTop (𝓝 ((b i).1 v)) at ht
    simpa only [InnerProductSpace.toDual_symm_apply,WeakDual.toStrongDual_apply] using ht
end EuclideanFiveColor
end

noncomputable section
open MeasureTheory Filter Topology
open scoped RealInnerProductSpace
namespace EuclideanFiveColor
variable {X : Type*} [MeasurableSpace X] (μ : Measure X) [IsFiniteMeasure μ]
end EuclideanFiveColor
end

noncomputable section
open MeasureTheory MeasureTheory.Measure Filter Topology
open scoped RealInnerProductSpace
namespace EuclideanFiveColor
variable {k : ℕ} (c : ℂ → Fin k)
def sample (hc : Measurable c) (y : ℂ) (r : ℝ) (i : Fin k) : RealL2 angularMeasure :=
  (sampleFn_memLp c hc y r i).toLp _
end EuclideanFiveColor
end

noncomputable section
open Filter Topology
open scoped RealInnerProductSpace
namespace EuclideanFiveColor.WeakBall
variable (E : Type*) [NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E]
  [TopologicalSpace.SeparableSpace E]
abbrev Space := {v : WeakDual ℝ E // WeakDual.toStrongDual v ∈ Metric.closedBall 0 1}
instance : CompactSpace (Space E) := isCompact_iff_compactSpace.mp (WeakDual.isCompact_closedBall 0 1)
instance : TopologicalSpace.MetrizableSpace (Space E) :=
  WeakDual.metrizable_of_isCompact ℝ E _ (WeakDual.isCompact_closedBall 0 1)
def value (a : Space E) : E := (InnerProductSpace.toDual ℝ E).symm (WeakDual.toStrongDual a.1)
omit [TopologicalSpace.SeparableSpace E] in
omit [TopologicalSpace.SeparableSpace E] in
omit [TopologicalSpace.SeparableSpace E] in
@[simp] lemma value_ofNorm (v : E) (hv : ‖v‖ ≤ 1) : value E (ofNorm E v hv) = v := by
  simp only [value,ofNorm,weakHilbert,StrongDual.toStrongDual_toWeakDual,LinearIsometryEquiv.symm_apply_apply]
omit [TopologicalSpace.SeparableSpace E] in
omit [TopologicalSpace.SeparableSpace E] in
end EuclideanFiveColor.WeakBall
end

noncomputable section
open MeasureTheory Filter Topology
open scoped RealInnerProductSpace
namespace EuclideanFiveColor
variable {X : Type*} [MeasurableSpace X] {μ : Measure X} [IsFiniteMeasure μ]
end EuclideanFiveColor
end

noncomputable section
open MeasureTheory Filter Topology
open scoped RealInnerProductSpace
namespace EuclideanFiveColor
private instance : Fact ((2 : ENNReal) ≠ ⊤) := ⟨by norm_num⟩
variable {k : ℕ} (c : ℂ → Fin k) (hc : Measurable c)
@[simp] lemma traceValue_sampleCode (y : ℂ) (r : ℝ) (i : Fin k) :
    traceValue (sampleCode c hc y r) i = sample c hc y r i := WeakBall.value_ofNorm _ _ _
end EuclideanFiveColor
end

noncomputable section
open MeasureTheory Topology Filter Set
namespace EuclideanFiveColor
variable {X I : Type*} [MeasurableSpace X] (μ : Measure X) [IsFiniteMeasure μ]
end EuclideanFiveColor
end

end OAI
