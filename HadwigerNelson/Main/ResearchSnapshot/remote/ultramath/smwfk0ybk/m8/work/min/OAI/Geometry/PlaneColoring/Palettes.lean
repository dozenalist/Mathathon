import OAI.Analysis.PlaneSpectrum.Fourier
import OAI.Geometry.PlaneColoring.Coloring
import OAI.Geometry.PlaneColoring.Compactness
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
def paletteSet (x : ℂ) (i : Fin k) : Set Angles :=
  ⋃ b ∈ paletteGenerators c hc x i, tracePositive c hc x i b
def palette (x : ℂ) (t : Angles) : Finset (Fin k) := by
  classical
  exact Finset.univ.filter (fun i => t ∈ paletteSet c hc x i)
@[simp] lemma mem_palette (x : ℂ) (t : Angles) (i : Fin k) :
    i ∈ palette c hc x t ↔ t ∈ paletteSet c hc x i := by simp [palette]
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
