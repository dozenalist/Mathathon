import OAI.Geometry.PlaneColoring.Transitions

namespace OAI

noncomputable section
open MeasureTheory Filter Topology
namespace EuclideanFiveColor
variable {k : ℕ} (c : ℂ → Fin k) (hc : Measurable c)
abbrev Traces (x : ℂ) := {b : TraceVector k // IsTrace c hc x b}
def tracePositive (x : ℂ) (i : Fin k) (b : Traces c hc x) : Set Angles :=
  {t | 0 < traceValue b.1 i t}
lemma tracePositive_measurable (x : ℂ) (i : Fin k) (b : Traces c hc x) :
    MeasurableSet (tracePositive c hc x i b) :=
  measurableSet_lt measurable_const (Lp.stronglyMeasurable _).measurable
def paletteGenerators (x : ℂ) (i : Fin k) : Set (Traces c hc x) :=
  (exists_countable_essential_union angularMeasure (tracePositive c hc x i) (tracePositive_measurable c hc x i)).choose
lemma paletteGenerators_countable (x : ℂ) (i : Fin k) : (paletteGenerators c hc x i).Countable :=
  (exists_countable_essential_union angularMeasure (tracePositive c hc x i) (tracePositive_measurable c hc x i)).choose_spec.1
def paletteSet (x : ℂ) (i : Fin k) : Set Angles :=
  ⋃ b ∈ paletteGenerators c hc x i, tracePositive c hc x i b
lemma paletteSet_measurable (x : ℂ) (i : Fin k) : MeasurableSet (paletteSet c hc x i) :=
  MeasurableSet.biUnion (paletteGenerators_countable c hc x i) (fun b _ => tracePositive_measurable c hc x i b)
lemma tracePositive_le_palette (x : ℂ) (i : Fin k) (b : Traces c hc x) :
    tracePositive c hc x i b ≤ᵐ[angularMeasure] paletteSet c hc x i :=
  (exists_countable_essential_union angularMeasure (tracePositive c hc x i) (tracePositive_measurable c hc x i)).choose_spec.2 b
def palette (x : ℂ) (t : Angles) : Finset (Fin k) := by
  classical
  exact Finset.univ.filter (fun i => t ∈ paletteSet c hc x i)
@[simp] lemma mem_palette (x : ℂ) (t : Angles) (i : Fin k) :
    i ∈ palette c hc x t ↔ t ∈ paletteSet c hc x i := by simp [palette]
lemma palette_nonempty (x : ℂ) : ∀ᵐ t ∂angularMeasure, (palette c hc x t).Nonempty := by
  obtain ⟨b,hb⟩ := exists_trace c hc x
  let B : Traces c hc x := ⟨b,hb⟩
  have hsum := (trace_bounds c hc hb).2.2
  have hs : (fun t => ∑ i, traceValue b i t) =ᵐ[angularMeasure] (fun _ => (1 : ℝ)) := by
    have hh := Lp.coeFn_fun_finsetSum Finset.univ (traceValue b)
    rw [hsum] at hh
    exact hh.symm.trans (oneL2_ae angularMeasure)
  filter_upwards [hs,ae_all_iff.mpr (fun i => tracePositive_le_palette c hc x i B)] with t ht hP
  have he : ∃ i : Fin k, 0 < traceValue b i t := by
    by_contra! hh
    have hz : (∑ i, traceValue b i t) ≤ 0 := Finset.sum_nonpos (fun i _ => hh i)
    linarith
  obtain ⟨i,hi⟩ := he
  exact ⟨i,(mem_palette c hc x t i).mpr ((hP i) hi)⟩
end EuclideanFiveColor
end

noncomputable section
open MeasureTheory Filter Topology
open scoped RealInnerProductSpace
namespace EuclideanFiveColor
variable {k : ℕ} (c : ℂ → Fin k) (hc : Measurable c)
end EuclideanFiveColor
end

end OAI
