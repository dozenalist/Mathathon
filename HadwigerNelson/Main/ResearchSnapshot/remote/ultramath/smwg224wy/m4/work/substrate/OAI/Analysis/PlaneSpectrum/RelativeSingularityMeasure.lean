import OAI.Analysis.PlaneSpectrum.RelativeSingularityInput
import Mathlib.Dynamics.Ergodic.Action.Basic
import Mathlib.MeasureTheory.Measure.Prod
import Mathlib.MeasureTheory.Measure.Typeclasses.Probability

/-! Two measure-algebra inputs for Theorem A. -/

open MeasureTheory Filter
open scoped ENNReal

namespace RelativeSingularity

/-- If `lam ⊗ lam` is carried by `T`, there are four points with all six pairs in `T`
(four conditionally independent samples). -/
theorem exists_four_pairwise {α : Type*} [MeasurableSpace α]
    (lam : Measure α) [IsProbabilityMeasure lam]
    (T : Set (α × α)) (hT : MeasurableSet T) (h : (lam.prod lam) T = 1) :
    ∃ a b c d : α, (a, b) ∈ T ∧ (a, c) ∈ T ∧ (a, d) ∈ T ∧
      (b, c) ∈ T ∧ (b, d) ∈ T ∧ (c, d) ∈ T := by
  classical
  set M : Measure ((α × α) × (α × α)) := (lam.prod lam).prod (lam.prod lam) with hM
  haveI hMp : IsProbabilityMeasure M := by rw [hM]; infer_instance
  have hM1 : M (Set.univ : Set ((α × α) × (α × α))) = 1 := by
    rw [hM]; simp
  have hmarg : ∀ (f g : α × α → α), Measurable f → Measurable g →
      (lam.prod lam).map f = lam → (lam.prod lam).map g = lam →
      M {t : (α × α) × (α × α) | (f t.1, g t.2) ∈ T} = 1 := by
    intro f g hfm hgm hfl hgl
    have hm : Measurable (fun t : (α × α) × (α × α) => (f t.1, g t.2)) :=
      (hfm.comp measurable_fst).prodMk (hgm.comp measurable_snd)
    have hmap : M.map (fun t : (α × α) × (α × α) => (f t.1, g t.2)) = lam.prod lam := by
      have he : (fun t : (α × α) × (α × α) => (f t.1, g t.2)) = Prod.map f g := rfl
      rw [he, hM, ← Measure.map_prod_map (lam.prod lam) (lam.prod lam) hfm hgm, hfl, hgl]
    have hpre : {t : (α × α) × (α × α) | (f t.1, g t.2) ∈ T}
        = (fun t => (f t.1, g t.2)) ⁻¹' T := rfl
    rw [hpre, ← Measure.map_apply hm hT, hmap, h]
  have hfst : (lam.prod lam).map Prod.fst = lam := by
    simpa using Measure.map_fst_prod (μ := lam) (ν := lam)
  have hsnd : (lam.prod lam).map Prod.snd = lam := by
    simpa using Measure.map_snd_prod (μ := lam) (ν := lam)
  have hfstM : M.map (fun t : (α × α) × (α × α) => t.1) = lam.prod lam := by
    rw [hM]; simpa using Measure.map_fst_prod (μ := lam.prod lam) (ν := lam.prod lam)
  have hsndM : M.map (fun t : (α × α) × (α × α) => t.2) = lam.prod lam := by
    rw [hM]; simpa using Measure.map_snd_prod (μ := lam.prod lam) (ν := lam.prod lam)
  set S1 : Set ((α × α) × (α × α)) := {t | t.1 ∈ T} with hS1
  set S2 : Set ((α × α) × (α × α)) := {t | t.2 ∈ T} with hS2
  set S3 : Set ((α × α) × (α × α)) := {t | (t.1.1, t.2.1) ∈ T} with hS3
  set S4 : Set ((α × α) × (α × α)) := {t | (t.1.1, t.2.2) ∈ T} with hS4
  set S5 : Set ((α × α) × (α × α)) := {t | (t.1.2, t.2.1) ∈ T} with hS5
  set S6 : Set ((α × α) × (α × α)) := {t | (t.1.2, t.2.2) ∈ T} with hS6
  have hS1m : MeasurableSet S1 := hT.preimage measurable_fst
  have hS2m : MeasurableSet S2 := hT.preimage measurable_snd
  have hS3m : MeasurableSet S3 :=
    hT.preimage (measurable_fst.fst.prodMk measurable_snd.fst)
  have hS4m : MeasurableSet S4 :=
    hT.preimage (measurable_fst.fst.prodMk measurable_snd.snd)
  have hS5m : MeasurableSet S5 :=
    hT.preimage (measurable_fst.snd.prodMk measurable_snd.fst)
  have hS6m : MeasurableSet S6 :=
    hT.preimage (measurable_fst.snd.prodMk measurable_snd.snd)
  have hm1 : M S1 = 1 := by
    have hpre : S1 = (fun t : (α × α) × (α × α) => t.1) ⁻¹' T := rfl
    rw [hpre, ← Measure.map_apply measurable_fst hT, hfstM, h]
  have hm2 : M S2 = 1 := by
    have hpre : S2 = (fun t : (α × α) × (α × α) => t.2) ⁻¹' T := rfl
    rw [hpre, ← Measure.map_apply measurable_snd hT, hsndM, h]
  have hm3 : M S3 = 1 := hmarg Prod.fst Prod.fst measurable_fst measurable_fst hfst hfst
  have hm4 : M S4 = 1 := hmarg Prod.fst Prod.snd measurable_fst measurable_snd hfst hsnd
  have hm5 : M S5 = 1 := hmarg Prod.snd Prod.fst measurable_snd measurable_fst hsnd hfst
  have hm6 : M S6 = 1 := hmarg Prod.snd Prod.snd measurable_snd measurable_snd hsnd hsnd
  set G : Set ((α × α) × (α × α)) := S1 ∩ (S2 ∩ (S3 ∩ (S4 ∩ (S5 ∩ S6)))) with hG
  have hGm : MeasurableSet G := by
    rw [hG]
    exact hS1m.inter (hS2m.inter (hS3m.inter (hS4m.inter (hS5m.inter hS6m))))
  have hcz : ∀ s : Set ((α × α) × (α × α)), MeasurableSet s → M s = 1 → M sᶜ = 0 := by
    intro s hs hms
    have h2 : M sᶜ = M (Set.univ : Set ((α × α) × (α × α))) - M s :=
      measure_compl hs (measure_ne_top M s)
    rw [hms, hM1] at h2
    simpa using h2
  have hGc_eq : Gᶜ = S1ᶜ ∪ (S2ᶜ ∪ (S3ᶜ ∪ (S4ᶜ ∪ (S5ᶜ ∪ S6ᶜ)))) := by
    rw [hG, Set.compl_inter, Set.compl_inter, Set.compl_inter, Set.compl_inter,
      Set.compl_inter]
  have hG1 : M G = 1 := by
    have h0 : M Gᶜ = 0 := by
      rw [hGc_eq]
      exact measure_union_null (hcz S1 hS1m hm1) (measure_union_null (hcz S2 hS2m hm2)
        (measure_union_null (hcz S3 hS3m hm3) (measure_union_null (hcz S4 hS4m hm4)
        (measure_union_null (hcz S5 hS5m hm5) (hcz S6 hS6m hm6)))))
    have h2 : M G + M Gᶜ = M (Set.univ : Set ((α × α) × (α × α))) :=
      measure_add_measure_compl hGm
    rw [h0, hM1, add_zero] at h2
    exact h2
  have hne : G.Nonempty := by
    rw [Set.nonempty_iff_ne_empty]
    intro hemp
    have h0 : M G = 0 := by rw [hemp]; exact MeasureTheory.measure_empty
    rw [hG1] at h0
    exact one_ne_zero h0
  obtain ⟨t, ht⟩ := hne
  simp only [hG, Set.mem_inter_iff, Set.mem_setOf_eq] at ht
  obtain ⟨h1, h2, h3, h4, h5, h6⟩ := ht
  exact ⟨t.1.1, t.1.2, t.2.1, t.2.2, h1, h3, h4, h5, h6, h2⟩

/-- An a.e. invariant measurable set of an ergodic additive action has measure `0` or `univ`. -/
theorem measure_eq_zero_or_univ_of_ae_invariant {G α : Type*} [VAdd G α] [MeasurableSpace α]
    {μ : Measure α} [ErgodicVAdd G α μ] {s : Set α} (hs : MeasurableSet s)
    (h : ∀ g : G, (g +ᵥ ·) ⁻¹' s =ᵐ[μ] s) : μ s = 0 ∨ μ s = μ Set.univ := by
  classical
  have hec : EventuallyConst s (ae μ) :=
    ErgodicVAdd.aeconst_of_forall_preimage_vadd_ae_eq hs h
  obtain ⟨b, hb⟩ := EventuallyConst.eventuallyEq_const hec
  by_cases hbb : b
  · right
    have hmem : ∀ᵐ x ∂μ, (x ∈ s) := by
      filter_upwards [hb] with x hx
      exact hx.mpr hbb
    have hcompl : μ sᶜ = 0 := by
      have hres := (ae_iff (μ := μ) (p := fun x => (x ∈ s))).mp hmem
      exact hres
    have h2 : μ s + μ sᶜ = μ (Set.univ : Set α) := measure_add_measure_compl hs
    rw [hcompl, add_zero] at h2
    exact h2
  · left
    have hmem : ∀ᵐ x ∂μ, ¬ (x ∈ s) := by
      filter_upwards [hb] with x hx
      exact fun h => hbb (hx.mp h)
    have hres := (ae_iff (μ := μ) (p := fun x => ¬ (x ∈ s))).mp hmem
    simpa using hres

end RelativeSingularity
