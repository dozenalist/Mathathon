import OAI.Geometry.PlaneColoring.CircleMaps
import OAI.Geometry.PlaneColoring.Palettes
namespace OAI

noncomputable section
open MeasureTheory Filter Topology
namespace EuclideanFiveColor
end EuclideanFiveColor
end

noncomputable section
open MeasureTheory Filter Topology
namespace EuclideanFiveColor
variable {k : ℕ} (c : ℂ → Fin k) (hc : Measurable c)
end EuclideanFiveColor

end

noncomputable section
open MeasureTheory Set
namespace EuclideanFiveColor
end EuclideanFiveColor
end

noncomputable section
open MeasureTheory Filter Topology Set
open scoped NNReal
namespace EuclideanFiveColor
def FlatDensityZero (A : Set (ℝ × ℝ)) (p : ℝ × ℝ) : Prop :=
  Tendsto (fun r : ℝ => volume.real (A ∩ Metric.closedBall p r)/r^2) (𝓝[>] 0) (𝓝 0)
lemma volume_image_bound {F : ℝ × ℝ → ℝ × ℝ} {s : Set (ℝ × ℝ)} {K : ℝ≥0}
    (hF : LipschitzWith K (s.domRestrict F)) (A : Set (ℝ × ℝ)) (hA : A ⊆ s) :
    volume (F '' A) ≤ (K : ENNReal)^2 * volume A := by
  let B : Set s := Subtype.val ⁻¹' A
  have he1 : (s.domRestrict F) '' B = F '' A := by
    ext y
    constructor
    · rintro ⟨z,hz,rfl⟩; exact ⟨z.1,hz,rfl⟩
    · rintro ⟨z,hz,rfl⟩; exact ⟨⟨z,hA hz⟩,hz,rfl⟩
  have he2 : Subtype.val '' B = A := by
    ext z
    exact ⟨fun ⟨q,hq,he⟩ => he ▸ hq,fun hz => ⟨⟨z,hA hz⟩,hz,rfl⟩⟩
  have hi := (isometry_subtype_coe : Isometry (Subtype.val : s → ℝ × ℝ)).hausdorffMeasure_image
    (Or.inl (by norm_num : (0 : ℝ)≤2)) B
  have ha := hF.hausdorffMeasure_image_le (by norm_num : (0 : ℝ)≤2) B
  rw [he1,hausdorffMeasure_prod_real,ENNReal.rpow_two] at ha
  rw [he2,hausdorffMeasure_prod_real] at hi
  rwa [← hi] at ha
lemma tendsto_pos_mul_nhdsWithin {a : ℝ} (ha : 0<a) :
    Tendsto (fun r : ℝ => a*r) (𝓝[>] 0) (𝓝[>] 0) := by
  apply tendsto_nhdsWithin_iff.mpr
  constructor
  · simpa using (tendsto_const_nhds.mul (tendsto_id.mono_left nhdsWithin_le_nhds : Tendsto (fun r : ℝ => r) (𝓝[>] 0) (𝓝 0)))
  · filter_upwards [self_mem_nhdsWithin] with r hr
    exact mul_pos ha hr
lemma FlatDensityZero.image {D s : Set (ℝ × ℝ)} {p : ℝ × ℝ} {F : ℝ × ℝ → ℝ × ℝ}
    {K L : ℝ≥0} (hD : FlatDensityZero D p) (hps : p ∈ s)
    (hF : LipschitzWith K (s.domRestrict F)) (hA : AntilipschitzWith L (s.domRestrict F))
    (hL : 0 < L) : FlatDensityZero (F '' (D ∩ s)) (F p) := by
  have h := (hD.comp (tendsto_pos_mul_nhdsWithin (show 0 < (L : ℝ) from hL))).const_mul
    ((K : ℝ)^2*(L : ℝ)^2)
  simp only [mul_zero] at h
  apply squeeze_zero' (Eventually.of_forall fun r => div_nonneg measureReal_nonneg (sq_nonneg r)) _ h
  filter_upwards [self_mem_nhdsWithin] with r hr
  have hp : 0 < r := hr
  let E : Set (ℝ × ℝ) := D ∩ s ∩ Metric.closedBall p ((L : ℝ)*r)
  have he : F '' (D ∩ s) ∩ Metric.closedBall (F p) r ⊆ F '' E := by
    rintro z ⟨⟨q,hq,rfl⟩,hz⟩
    refine ⟨q,⟨hq,?_⟩,rfl⟩
    exact (hA.le_mul_dist ⟨q,hq.2⟩ ⟨p,hps⟩).trans
      (mul_le_mul_of_nonneg_left hz L.2)
  have hm := (measure_mono he).trans (volume_image_bound hF E (fun q hq => hq.1.2))
  have hsub : E ⊆ D ∩ Metric.closedBall p ((L : ℝ)*r) := fun q hq => ⟨hq.1.1,hq.2⟩
  have hfin : volume (D ∩ Metric.closedBall p ((L : ℝ)*r)) ≠ ⊤ :=
    ne_top_of_le_ne_top (isCompact_closedBall _ _).measure_ne_top (measure_mono inter_subset_right)
  have hm' := hm.trans (mul_le_mul (le_refl _) (measure_mono hsub) bot_le bot_le)
  have hreal := ENNReal.toReal_mono (ENNReal.mul_ne_top (by finiteness) hfin) hm'
  simp only [ENNReal.toReal_mul,ENNReal.toReal_pow,ENNReal.coe_toReal] at hreal
  calc
    _ ≤ (K : ℝ)^2*volume.real (D ∩ Metric.closedBall p ((L : ℝ)*r))/r^2 :=
      div_le_div_of_nonneg_right hreal (sq_nonneg r)
    _ = _ := by
      change _ = ((K : ℝ)^2*(L : ℝ)^2)*
        (volume.real (D ∩ Metric.closedBall p ((L : ℝ)*r))/((L : ℝ)*r)^2)
      have hLr : (L : ℝ) ≠ 0 := ne_of_gt hL
      field_simp [hp.ne',hLr]
end EuclideanFiveColor
end

noncomputable section
open MeasureTheory Filter Topology Set
open scoped NNReal
namespace EuclideanFiveColor
lemma FlatDensityZero.of_locally_le {A B s : Set (ℝ × ℝ)} {p : ℝ × ℝ}
    (hb : FlatDensityZero B p) (hs : s ∈ 𝓝 p) (hAB : (A ∩ s : Set (ℝ × ℝ)) ≤ᵐ[volume] B) :
    FlatDensityZero A p := by
  obtain ⟨δ,hδ,hsδ⟩ := Metric.mem_nhds_iff.mp hs
  apply squeeze_zero' (Eventually.of_forall fun r => div_nonneg measureReal_nonneg (sq_nonneg r)) _ hb
  filter_upwards [(eventually_lt_nhds hδ).filter_mono nhdsWithin_le_nhds] with r hr
  apply div_le_div_of_nonneg_right _ (sq_nonneg r)
  apply ENNReal.toReal_mono
  · exact ne_top_of_le_ne_top (isCompact_closedBall p r).measure_ne_top (measure_mono inter_subset_right)
  · apply measure_mono_ae
    filter_upwards [hAB] with q hq
    intro hqa
    exact ⟨hq ⟨hqa.1,hsδ (Metric.closedBall_subset_ball hr hqa.2)⟩,hqa.2⟩
lemma FlatDensityZero.transport {A D s : Set (ℝ × ℝ)} {p : ℝ × ℝ}
    {F : ℝ × ℝ → ℝ × ℝ} {K L : ℝ≥0} (hD : FlatDensityZero D p)
    (hps : p ∈ s) (hs : F '' s ∈ 𝓝 (F p))
    (hF : LipschitzWith K (s.domRestrict F)) (hA : AntilipschitzWith L (s.domRestrict F))
    (hL : 0 < L) (hAD : (F ⁻¹' A ∩ s : Set (ℝ × ℝ)) ≤ᵐ[volume] D) : FlatDensityZero A (F p) := by
  let N := (F ⁻¹' A ∩ s) \ D
  have hN : volume N=0 := measure_eq_zero_iff_ae_notMem.mpr (hAD.mono fun q hq h => h.2 (hq h.1))
  have himg : volume (F '' N)=0 := by
    apply le_antisymm _ (zero_le : (0 : ENNReal) ≤ volume (F '' N))
    simpa only [hN,mul_zero] using volume_image_bound hF N (fun q hq => hq.1.2)
  apply (hD.image hps hF hA hL).of_locally_le hs
  filter_upwards [measure_eq_zero_iff_ae_notMem.mp himg] with q hq
  rintro ⟨hqa,⟨t,ht,rfl⟩⟩
  by_cases hd : t ∈ D
  · exact ⟨t,⟨hd,ht⟩,rfl⟩
  · exact (hq ⟨t,⟨⟨hqa,ht⟩,hd⟩,rfl⟩).elim
end EuclideanFiveColor
end

noncomputable section
open MeasureTheory Filter Topology Set
open scoped NNReal
namespace EuclideanFiveColor
end EuclideanFiveColor
end

noncomputable section
open MeasureTheory Filter Topology Set
namespace EuclideanFiveColor
end EuclideanFiveColor
end

noncomputable section
open MeasureTheory Filter Topology Set
namespace EuclideanFiveColor
end EuclideanFiveColor
end

noncomputable section
open MeasureTheory Filter Topology Set
namespace EuclideanFiveColor
variable {k : ℕ} (c : ℂ → Fin k) (hc : Measurable c)
end EuclideanFiveColor
end

noncomputable section
open MeasureTheory Filter Topology Set
namespace EuclideanFiveColor
variable {k : ℕ} (c : ℂ → Fin k) (hc : Measurable c)
end EuclideanFiveColor
end

end OAI
