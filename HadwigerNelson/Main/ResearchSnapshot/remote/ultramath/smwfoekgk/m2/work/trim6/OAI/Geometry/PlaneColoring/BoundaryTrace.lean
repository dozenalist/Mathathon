import OAI.Geometry.PlaneColoring.Rigidity
import OAI.Geometry.PlaneColoring.States

namespace OAI

noncomputable section
open Set Filter Topology MeasureTheory
open scoped RealInnerProductSpace
namespace EuclideanFiveColor
variable {k : ℕ} (c : ℂ → Fin k) (hc : Measurable c)
lemma support_good_sequence {A : Set ℝ} {P : ℝ → Prop} {a : ℝ}
    (ha : a∈(volume.restrict A).support) (hP : ∀ᵐt∂volume,t∈A → P t) :
    ∃t : ℕ → ℝ, Tendsto t atTop (𝓝 a) ∧ ∀n,P (t n) := by
  have hex (n : ℕ) : ∃t,dist t a<1/((n:ℝ)+1) ∧ P t := by
    have hp : 0<volume (Metric.ball a (1/((n:ℝ)+1))∩A) := by
      simpa only [Measure.restrict_apply measurableSet_ball] using
        (Measure.mem_support_iff_forall a).mp ha _ (Metric.ball_mem_nhds a (by positivity))
    obtain ⟨t,ht,hpt⟩ := ((frequently_ae_mem_iff.mpr hp.ne').and_eventually hP).exists
    exact ⟨t,ht.1,hpt ht.2⟩
  choose t hd hpt using hex
  refine ⟨t,?_,hpt⟩
  rw [tendsto_iff_dist_tendsto_zero]
  exact squeeze_zero (fun _ => dist_nonneg) (fun n => (hd n).le) tendsto_one_div_add_atTop_nhds_zero_nat
lemma state_support_avoiding_trace (hw : WeakColoring k c) {x : ℂ} {A : Set ℝ} {J : Finset (Fin k)}
    (hA : RealState hc x A J) {a : ℝ} (ha : a∈(volume.restrict A).support) :
    ∃b : TraceVector k,IsTrace c hc (x+direction (a : Angles)) b ∧ ∀i∈J,traceValue b i=0 := by
  have he := angleMk_quasiMeasurePreserving.ae (ae_circle_palette_exclusion c hc hw x)
  have ht := angleMk_quasiMeasurePreserving.ae (ae_circle_typicalSampling c hc x)
  have hp : ∀ᵐt : ℝ∂volume,t∈A → TypicalSampling c (x+direction (t : Angles)) 1 ∧
      ∀i∈J,sample c hc (x+direction (t : Angles)) 1 i=0 := by
    filter_upwards [he,ht,ae_all_iff.mpr (fun i => ae_all_iff.mpr (fun hi : i∈J => hA.2 i hi))] with t he ht hJ hta
    refine ⟨ht,?_⟩
    intro i hi
    apply Lp.ext
    filter_upwards [sample_ae c hc (x+direction (t : Angles)) 1 i,he,Lp.coeFn_zero ℝ 2 angularMeasure] with v hv he hz
    rw [hz,hv]
    have hne : c (x+direction (t : Angles)+direction v)≠i := by
      intro hh
      apply he
      rw [hh]
      exact (mem_palette c hc x (t : Angles) i).mpr (hJ i hi hta)
    simp only [sampleFn,Complex.ofReal_one,one_mul,ite_eq_right hne,Pi.zero_apply]
  obtain ⟨t,ht,hp⟩ := support_good_sequence ha hp
  obtain ⟨b,_,φ,hφ,hb⟩ := (isCompact_univ : IsCompact (Set.univ : Set (TraceVector k))).isSeqCompact.subseq_of_frequently_in
    (Eventually.frequently (Eventually.of_forall fun n => Set.mem_univ (sampleCode c hc (x+direction (t n : Angles)) 1)))
  have hlim : Tendsto (fun n => x+direction (t n : Angles)) atTop (𝓝 (x+direction (a : Angles))) :=
    tendsto_const_nhds.add (direction_continuous.continuousAt.tendsto.comp ((AddCircle.continuous_mk' (2*Real.pi)).continuousAt.tendsto.comp ht))
  refine ⟨b,trace_of_realization c hc (fun n => (hp (φ n)).1) (hlim.comp hφ.tendsto_atTop) tendsto_const_nhds hb,?_⟩
  intro i hi
  have hh := traceCode_tendsto_iff.mp hb i (traceValue b i)
  simp only [Function.comp_apply,traceValue_sampleCode,(hp _).2 i hi,inner_zero_left] at hh
  exact inner_self_eq_zero.mp (tendsto_nhds_unique tendsto_const_nhds hh).symm
lemma avoiding_trace_palette {x : ℂ} {b : TraceVector k} (hb : IsTrace c hc x b)
    {J : Finset (Fin k)} (hJ : ∀i∈J,traceValue b i=0) :
    ∀ᵐt∂angularMeasure,¬palette c hc x t⊆J := by
  have hs : (fun t => ∑i,traceValue b i t)=ᵐ[angularMeasure](fun _ => (1:ℝ)) := by
    have hh := Lp.coeFn_fun_finsetSum Finset.univ (traceValue b)
    rw [(trace_bounds c hc hb).2.2] at hh
    exact hh.symm.trans (oneL2_ae angularMeasure)
  have hz (i : Fin k) : ∀ᵐt∂angularMeasure,i∈J → traceValue b i t=0 := by
    by_cases hi : i∈J
    · rw [hJ i hi]
      exact (Lp.coeFn_zero ℝ 2 angularMeasure).mono fun _ hh _ => hh
    · exact Eventually.of_forall fun _ hh => (hi hh).elim
  filter_upwards [hs,ae_all_iff.mpr hz,ae_all_iff.mpr (fun i => tracePositive_le_palette c hc x i ⟨b,hb⟩)] with t hs hz hp hsub
  have hn : ∀i : Fin k,traceValue b i t≤0 := by
    intro i
    by_contra! hpos
    have hm := hsub ((mem_palette c hc x t i).mpr (hp i hpos))
    linarith [hz i hm]
  have hh := Finset.sum_nonpos (s := Finset.univ) (fun i _ => hn i)
  linarith
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology MeasureTheory MeasureTheory.Measure
open scoped RealInnerProductSpace
namespace EuclideanFiveColor
variable {k : ℕ} (c : ℂ → Fin k) (hc : Measurable c)
include hc in
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology MeasureTheory
namespace EuclideanFiveColor
variable {k : ℕ} (c : ℂ → Fin k) (hc : Measurable c)
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
