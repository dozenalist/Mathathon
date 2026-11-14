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
end EuclideanFiveColor
end

noncomputable section
open MeasureTheory Filter Topology
open scoped RealInnerProductSpace
namespace EuclideanFiveColor
variable {X : Type*} [MeasurableSpace X] (μ : Measure X) [IsFiniteMeasure μ]
abbrev RealL2 := Lp ℝ 2 μ
end EuclideanFiveColor
end

noncomputable section
open MeasureTheory MeasureTheory.Measure Filter Topology
open scoped RealInnerProductSpace
namespace EuclideanFiveColor
variable {k : ℕ} (c : ℂ → Fin k)
def Typical (z : ℂ) : Prop := DensityOne {w | c w=c z} z
def TypicalSampling (y : ℂ) (r : ℝ) : Prop :=
  0 < r ∧ ∀ᵐ t ∂angularMeasure, Typical c (y+(r : ℂ)*direction t)
def sampleFn (y : ℂ) (r : ℝ) (i : Fin k) (t : Angles) : ℝ :=
  if c (y+(r : ℂ)*direction t)=i then 1 else 0
lemma sampleFn_measurable (hc : Measurable c) (y : ℂ) (r : ℝ) (i : Fin k) :
    Measurable (sampleFn c y r i) := by
  exact measurable_one.piecewise (measurableSet_eq_fun
    (hc.comp (measurable_const.add (measurable_const.mul direction_continuous.measurable))) measurable_const) measurable_zero
lemma sampleFn_nonneg (y : ℂ) (r : ℝ) (i : Fin k) (t : Angles) : 0 ≤ sampleFn c y r i t := by
  simp only [sampleFn]; split_ifs <;> norm_num
lemma sampleFn_le_one (y : ℂ) (r : ℝ) (i : Fin k) (t : Angles) : sampleFn c y r i t ≤ 1 := by
  simp only [sampleFn]; split_ifs <;> norm_num
lemma sampleFn_memLp (hc : Measurable c) (y : ℂ) (r : ℝ) (i : Fin k) :
    MemLp (sampleFn c y r i) 2 angularMeasure := by
  apply MemLp.of_bound (sampleFn_measurable c hc y r i).aestronglyMeasurable 1
  exact Eventually.of_forall fun t => by rw [Real.norm_eq_abs,abs_of_nonneg (sampleFn_nonneg c y r i t)]; exact sampleFn_le_one c y r i t
def sample (hc : Measurable c) (y : ℂ) (r : ℝ) (i : Fin k) : RealL2 angularMeasure :=
  (sampleFn_memLp c hc y r i).toLp _
lemma sample_ae (hc : Measurable c) (y : ℂ) (r : ℝ) (i : Fin k) :
    sample c hc y r i =ᵐ[angularMeasure] sampleFn c y r i := MemLp.coeFn_toLp _
lemma sample_norm_le (hc : Measurable c) (y : ℂ) (r : ℝ) (i : Fin k) :
    ‖sample c hc y r i‖ ≤ 1 := by
  have hh : ∀ᵐ t ∂angularMeasure, ‖sample c hc y r i t‖ ≤ 1 := by
    filter_upwards [sample_ae c hc y r i] with t ht
    rw [ht,Real.norm_eq_abs,abs_of_nonneg (sampleFn_nonneg c y r i t)]
    exact sampleFn_le_one c y r i t
  simpa [measureUnivNNReal] using Lp.norm_le_of_ae_bound (by norm_num : (0 : ℝ) ≤ 1) hh
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
lemma value_eval (a : Space E) (v : E) : ⟪value E a,v⟫ = a.1 v := by
  simp only [value,InnerProductSpace.toDual_symm_apply,WeakDual.toStrongDual_apply]
def ofNorm (v : E) (hv : ‖v‖ ≤ 1) : Space E := ⟨weakHilbert v,by
  simpa only [weakHilbert,StrongDual.toStrongDual_toWeakDual,Metric.mem_closedBall,dist_zero_right,
    LinearIsometryEquiv.norm_map] using hv⟩
omit [TopologicalSpace.SeparableSpace E] in
@[simp] lemma value_ofNorm (v : E) (hv : ‖v‖ ≤ 1) : value E (ofNorm E v hv) = v := by
  simp only [value,ofNorm,weakHilbert,StrongDual.toStrongDual_toWeakDual,LinearIsometryEquiv.symm_apply_apply]
omit [TopologicalSpace.SeparableSpace E] in
lemma continuous_eval (v : E) : Continuous (fun a : Space E => ⟪value E a,v⟫) := by
  simp_rw [value_eval]
  exact (WeakDual.eval_continuous v).comp continuous_subtype_val
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
abbrev TraceVector (k : ℕ) := Fin k → WeakBall.Space (RealL2 angularMeasure)
def traceValue {k : ℕ} (b : TraceVector k) (i : Fin k) : RealL2 angularMeasure :=
  WeakBall.value _ (b i)
variable {k : ℕ} (c : ℂ → Fin k) (hc : Measurable c)
def sampleCode (y : ℂ) (r : ℝ) : TraceVector k :=
  fun i => WeakBall.ofNorm _ (sample c hc y r i) (sample_norm_le c hc y r i)
@[simp] lemma traceValue_sampleCode (y : ℂ) (r : ℝ) (i : Fin k) :
    traceValue (sampleCode c hc y r) i = sample c hc y r i := WeakBall.value_ofNorm _ _ _
def sampleSet : Set (ℂ × ℝ × TraceVector k) :=
  {p | TypicalSampling c p.1 p.2.1 ∧ p.2.2=sampleCode c hc p.1 p.2.1}
def IsTrace (x : ℂ) (b : TraceVector k) : Prop := (x,1,b) ∈ closure (sampleSet c hc)
end EuclideanFiveColor
end

noncomputable section
open MeasureTheory Topology Filter Set
namespace EuclideanFiveColor
variable {X I : Type*} [MeasurableSpace X] (μ : Measure X) [IsFiniteMeasure μ]
/-- A finite-measure essential union is generated by countably many members of the original family. -/
lemma exists_countable_essential_union (A : I → Set X) (hm : ∀ i, MeasurableSet (A i)) :
    ∃ J : Set I, J.Countable ∧ ∀ i, A i ≤ᵐ[μ] (⋃ j ∈ J, A j) := by
  let S : Set ENNReal := {m | ∃ J : Set I, J.Countable ∧ μ (⋃ j ∈ J, A j)=m}
  have hs : S.Nonempty := ⟨0,∅,Set.countable_empty,by simp⟩
  obtain ⟨f,_,ht,hf⟩ := exists_seq_tendsto_sSup hs (OrderTop.bddAbove S)
  choose J hJ he using hf
  let K : Set I := ⋃ n, J n
  have hK : K.Countable := Set.countable_iUnion hJ
  let D : Set X := ⋃ j ∈ K, A j
  have hD : MeasurableSet D := MeasurableSet.biUnion hK (fun j _ => hm j)
  have hS : μ D ∈ S := ⟨K,hK,rfl⟩
  have hmax : μ D = sSup S := le_antisymm (le_sSup hS) (le_of_tendsto ht (Eventually.of_forall (fun n => by
    rw [← he n]
    apply measure_mono
    intro x hx
    rcases Set.mem_iUnion₂.mp hx with ⟨j,hj,hx⟩
    exact Set.mem_iUnion₂.mpr ⟨j,Set.mem_iUnion.mpr ⟨n,hj⟩,hx⟩)))
  refine ⟨K,hK,fun i => ?_⟩
  have hun : μ (D ∪ A i) ≤ μ D := by
    rw [hmax]
    apply le_sSup
    refine ⟨insert i K,hK.insert i,?_⟩
    congr 1
    ext x
    simp only [Set.mem_iUnion,Set.mem_insert_iff,Set.mem_union,D]
    aesop
  have heq : μ (D ∪ A i) = μ D := le_antisymm hun (measure_mono Set.subset_union_left)
  have hzero : μ ((D ∪ A i) \ D)=0 := by
    rw [measure_sdiff Set.subset_union_left hD.nullMeasurableSet (measure_ne_top μ D),heq,tsub_self]
  have hz : μ (A i \ D)=0 := measure_mono_null (by intro x hx; exact ⟨Or.inr hx.1,hx.2⟩) hzero
  simpa only [ae_le_set] using hz
end EuclideanFiveColor
end

end OAI
