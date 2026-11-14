import OAI.Geometry.PlaneColoring.States

namespace OAI

noncomputable section
open Set Filter Topology MeasureTheory
namespace EuclideanFiveColor
variable (c : ℂ → Fin 5) (hc : Measurable c)
lemma four_avoiding_traces (hw : WeakColoring 5 c) {x : ℂ} (hx : FourCenter c x) :
    ∃ b : Fin 4 → TraceVector 5, (∀e,IsTrace c hc x (b e)) ∧
      ∀e,∀i∈fourEdge e,traceValue (b e) i=0 := by
  have hh (i j : Fin 5) (he : TransitionEdge c i j x) :
      ∃ b : TraceVector 5, IsTrace c hc x b ∧ ∀a∈({i,j} : Finset (Fin 5)),traceValue b a=0 := by
    obtain ⟨b,hb,hi,hj⟩ := transition_avoiding_trace c hc hw he
    refine ⟨b,hb,?_⟩
    intro a ha
    simp only [Finset.mem_insert,Finset.mem_singleton] at ha
    rcases ha with rfl|rfl <;> assumption
  have he (e : Fin 4) : ∃ b : TraceVector 5, IsTrace c hc x b ∧ ∀i∈fourEdge e,traceValue b i=0 := by
    fin_cases e
    · exact hh 0 1 hx.1
    · exact hh 1 2 hx.2.1
    · exact hh 2 3 hx.2.2.1
    · exact hh 3 0 hx.2.2.2
  choose b hb hz using he
  exact ⟨b,hb,hz⟩
lemma four_state_trace_domination (hw : WeakColoring 5 c) {x : ℂ} (hx : FourCenter c x)
    (b : Fin 4 → TraceVector 5) (hb : ∀e,IsTrace c hc x (b e))
    (hz : ∀e,∀i∈fourEdge e,traceValue (b e) i=0) (s : Fin 3) {i : Fin 5} (hi : i∈fourGroup s) :
    {t | fourState c hc x t=s}.indicator (fun _ => (1:ℝ)) ≤ᵐ[angularMeasure]
      (fun t => ∑e,traceValue (b e) i t) := by
  have hs (e : Fin 4) : (fun t => ∑a,traceValue (b e) a t)=ᵐ[angularMeasure] (fun _ => (1:ℝ)) := by
    have hh := Lp.coeFn_fun_finsetSum Finset.univ (traceValue (b e))
    rw [(trace_bounds c hc (hb e)).2.2] at hh
    exact hh.symm.trans (oneL2_ae angularMeasure)
  have hzero (e : Fin 4) (a : Fin 5) : ∀ᵐt∂angularMeasure,a∈fourEdge e → traceValue (b e) a t=0 := by
    by_cases ha : a∈fourEdge e
    · rw [hz e a ha]
      filter_upwards [Lp.coeFn_zero ℝ 2 angularMeasure] with t ht
      exact fun _ => ht
    · exact Eventually.of_forall fun _ => fun h => (ha h).elim
  filter_upwards [four_palette_admissible c hc hw hx,
    ae_all_iff.mpr (fun e => ae_all_iff.mpr fun a => (trace_bounds c hc (hb e)).1 a),
    ae_all_iff.mpr hs,ae_all_iff.mpr (fun e => ae_all_iff.mpr (hzero e)),
    ae_all_iff.mpr (fun e => ae_all_iff.mpr fun a => tracePositive_le_palette c hc x a ⟨b e,hb e⟩)]
    with t hadm hnon hsum hzero hpal
  by_cases hts : fourState c hc x t=s
  · rw [Set.indicator_of_mem (show t∈{t | fourState c hc x t=s} from hts)]
    obtain ⟨e,_,hep⟩ := four_trace_edge (palette c hc x t) hadm i (by simpa only [← hts, fourState] using hi)
    have hj (a : Fin 5) (ha : a≠i) : traceValue (b e) a t=0 := by
      by_cases he : a∈fourEdge e
      · exact hzero e a he
      · apply le_antisymm _ (hnon e a)
        by_contra! hpos
        have hp := (mem_palette c hc x t a).mpr (hpal e a hpos)
        exact he (hep (Finset.mem_sdiff.mpr ⟨hp,by simpa using ha⟩))
    have heq : traceValue (b e) i t=1 := by
      rw [← hsum e,Finset.sum_eq_single i _ (by simp)]
      intro a _ hai
      exact hj a hai
    rw [← heq]
    exact Finset.single_le_sum (fun j _ => hnon j i) (Finset.mem_univ e)
  · rw [Set.indicator_of_notMem (show t∉{t | fourState c hc x t=s} from hts)]
    exact Finset.sum_nonneg (fun e _ => hnon e i)
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology MeasureTheory
open scoped RealInnerProductSpace
namespace EuclideanFiveColor
variable {Y : Type*} [MeasurableSpace Y] {μ : Measure Y} [IsProbabilityMeasure μ]
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology MeasureTheory
open scoped RealInnerProductSpace
namespace EuclideanFiveColor
variable (c : ℂ → Fin 5) (hc : Measurable c)
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology MeasureTheory
open scoped RealInnerProductSpace
namespace EuclideanFiveColor
variable (c : ℂ → Fin 5) (hc : Measurable c)
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
namespace EuclideanFiveColor
variable (c : ℂ → Fin 5) (hc : Measurable c)
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology MeasureTheory
open scoped NNReal
namespace EuclideanFiveColor
end EuclideanFiveColor
end

end OAI
