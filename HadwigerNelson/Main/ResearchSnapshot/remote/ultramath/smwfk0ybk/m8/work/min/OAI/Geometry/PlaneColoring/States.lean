import OAI.Geometry.PlaneColoring.PaletteDensity
namespace OAI

noncomputable section
open Set
namespace EuclideanFiveColor
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology MeasureTheory
namespace EuclideanFiveColor
def DensityZero (A : Set ℂ) (x : ℂ) : Prop :=
  Tendsto (fun r : ℝ => volume (A∩Metric.closedBall x r)/volume (Metric.closedBall x r))
    (𝓝[>] 0) (𝓝 (0:ENNReal))
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
lemma DensityZero.compl {A : Set ℂ} {x : ℂ} (hA : MeasurableSet A) (hz : DensityZero A x) :
    DensityOne Aᶜ x := by
  have ht := ENNReal.Tendsto.sub (tendsto_const_nhds (x := (1:ENNReal))) hz (Or.inl (by finiteness))
  rw [tsub_zero] at ht
  apply ht.congr'
  filter_upwards [self_mem_nhdsWithin] with r hr
  have hfin : volume (A∩Metric.closedBall x r)≠⊤ :=
    ne_top_of_le_ne_top (isCompact_closedBall x r).measure_ne_top (measure_mono inter_subset_right)
  have hp := (Metric.measure_closedBall_pos volume x hr).ne'
  have he : Aᶜ∩Metric.closedBall x r=Metric.closedBall x r\(A∩Metric.closedBall x r) := by
    ext z; simp; tauto
  rw [he,measure_sdiff inter_subset_right (hA.inter measurableSet_closedBall).nullMeasurableSet hfin,
    ENNReal.sub_div (fun _ _ => hp),ENNReal.div_self hp (isCompact_closedBall x r).measure_ne_top]
variable {k : ℕ} {c : ℂ → Fin k} (hc : Measurable c)
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology MeasureTheory
namespace EuclideanFiveColor
lemma DensityOne.compl {A : Set ℂ} {x : ℂ} (hA : MeasurableSet A) (h : DensityOne A x) :
    DensityZero Aᶜ x := by
  have ht := ENNReal.Tendsto.sub (tendsto_const_nhds (x := (1:ENNReal))) h (Or.inl (by finiteness))
  rw [tsub_self] at ht
  apply ht.congr'
  filter_upwards [self_mem_nhdsWithin] with r hr
  have hfin : volume (A∩Metric.closedBall x r)≠⊤ :=
    ne_top_of_le_ne_top (isCompact_closedBall x r).measure_ne_top (measure_mono inter_subset_right)
  have hp := (Metric.measure_closedBall_pos volume x hr).ne'
  have he : Aᶜ∩Metric.closedBall x r=Metric.closedBall x r\(A∩Metric.closedBall x r) := by
    ext z; simp; tauto
  rw [he,measure_sdiff inter_subset_right (hA.inter measurableSet_closedBall).nullMeasurableSet hfin,
    ENNReal.sub_div (fun _ _ => hp),ENNReal.div_self hp (isCompact_closedBall x r).measure_ne_top]
lemma DensityOne.inter {A B : Set ℂ} {x : ℂ} (hA : MeasurableSet A) (hB : MeasurableSet B)
    (ha : DensityOne A x) (hb : DensityOne B x) : DensityOne (A∩B) x := by
  have hh := ((ha.compl hA).union (hb.compl hB)).compl (hA.compl.union hB.compl)
  simpa using hh
lemma DensityOne.measure_ne_zero {A : Set ℂ} {x : ℂ} (h : DensityOne A x) : volume A≠0 := by
  intro hz
  have hzero : (fun r => volume (A∩Metric.closedBall x r)/volume (Metric.closedBall x r))=fun _ : ℝ => (0:ENNReal) := by
    funext r
    rw [measure_mono_null inter_subset_left hz,ENNReal.zero_div]
  change Tendsto _ _ _ at h
  rw [hzero] at h
  exact zero_ne_one (tendsto_nhds_unique tendsto_const_nhds h)
lemma densityOne_univ (x : ℂ) : DensityOne univ x := by
  apply tendsto_const_nhds.congr'
  filter_upwards [self_mem_nhdsWithin] with r hr
  simp only [univ_inter]
  exact (ENNReal.div_self (Metric.measure_closedBall_pos volume x hr).ne'
    (isCompact_closedBall x r).measure_ne_top).symm
lemma DensityOne.iInter {ι : Type*} [Finite ι] {A : ι → Set ℂ} {x : ℂ}
    (hm : ∀i,MeasurableSet (A i)) (h : ∀i,DensityOne (A i) x) : DensityOne (⋂i,A i) x := by
  classical
  let := Fintype.ofFinite ι
  have hh (J : Finset ι) : DensityOne (⋂i∈J,A i) x := by
    induction J using Finset.induction_on with
    | empty => simpa using densityOne_univ x
    | @insert i J hi ih =>
      simp only [Finset.set_biInter_insert]
      exact (h i).inter (hm i) (J.measurableSet_biInter fun j _ => hm j) ih
  simpa using hh Finset.univ
variable {k : ℕ} {c : ℂ → Fin k}
lemma finite_density_realization (hc : Measurable c) (hw : WeakColoring k c)
    {ι : Type*} [Finite ι] (z : ι → ℂ) (J : ι → Finset (Fin k))
    (hz : ∀v,DensityOne {q | c q∈J v} (z v)) :
    ∃q : ℂ, (∀v,c (q+z v)∈J v) ∧
      ∀v w, ‖z v-z w‖=1 → c (q+z v)≠c (q+z w) := by
  have hmem : DensityOne (⋂v,{q | c (q+z v)∈J v}) 0 := by
    apply DensityOne.iInter
    · intro v
      exact (J v).finite_toSet.measurableSet.preimage (hc.comp (measurable_id.add_const _))
    · intro v
      simpa only [zero_add,preimage_ofPred_eq] using (densityOne_translate (A := {q | c q∈J v}) (x := 0) (u := z v)).mpr (by simpa using hz v)
  have hproper : ∀ᵐ q : ℂ ∂volume, ∀v w, ‖z v-z w‖=1 → c (q+z v)≠c (q+z w) := by
    apply ae_all_iff.mpr
    intro v
    apply ae_all_iff.mpr
    intro w
    by_cases hh : ‖z v-z w‖=1
    · obtain ⟨t,ht⟩ := direction_exists (u := z w-z v) (by simpa only [norm_sub_rev] using hh)
      have hd := (measurePreserving_add_right volume (z v)).quasiMeasurePreserving.ae
        (weak_all_directions c hc hw t)
      filter_upwards [hd] with q hq _
      simpa only [ht,show q+z v+(z w-z v)=q+z w by ring] using hq
    · exact Eventually.of_forall fun _ => fun h => (hh h).elim
  obtain ⟨q,hq,hqp⟩ := Measure.exists_mem_of_measure_ne_zero_of_ae hmem.measure_ne_zero (ae_restrict_of_ae hproper)
  exact ⟨q,fun v => mem_iInter.mp hq v,hqp⟩
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
