import OAI.Geometry.PlaneColoring.CircleTransport
import OAI.Geometry.PlaneColoring.Palettes

namespace OAI

noncomputable section
open MeasureTheory Filter Topology
namespace EuclideanFiveColor
lemma weak_strong_disjoint {X Y : Type*} [MeasurableSpace X] [MeasurableSpace Y]
    {μ : Measure X} {ν : Measure Y} [IsProbabilityMeasure μ] [IsProbabilityMeasure ν]
    {F : ℕ → X → ℝ} {b : X → ℝ} {G : ℕ → X × Y → ℝ} {g : X × Y → ℝ}
    (hF : ∀ n, Measurable (F n)) (hb : Measurable b)
    (hG : ∀ n, Measurable (G n)) (hg : Measurable g)
    (hFb : ∀ n x, 0 ≤ F n x ∧ F n x ≤ 1)
    (hbb : ∀ᵐ x ∂μ, 0 ≤ b x ∧ b x ≤ 1)
    (hGb : ∀ n p, 0 ≤ G n p ∧ G n p ≤ 1)
    (hgb : ∀ p, 0 ≤ g p ∧ g p ≤ 1)
    (hw : ∀ v : X → ℝ, Integrable v μ →
      Tendsto (fun n => ∫ x, F n x*v x ∂μ) atTop (𝓝 (∫ x, b x*v x ∂μ)))
    (hs : Tendsto (fun n => ∫ p, ‖G n p-g p‖ ∂μ.prod ν) atTop (𝓝 0))
    (hz : ∀ n, ∀ᵐ p ∂μ.prod ν, F n p.1*G n p=0) :
    ∀ᵐ p ∂μ.prod ν, b p.1*g p=0 := by
  have hgi : Integrable g (μ.prod ν) := Integrable.of_bound hg.aestronglyMeasurable 1
    (Eventually.of_forall fun p => by rw [Real.norm_eq_abs,abs_of_nonneg (hgb p).1]; exact (hgb p).2)
  have hFi (n : ℕ) : Integrable (fun p : X × Y => F n p.1*g p) (μ.prod ν) := by
    apply Integrable.of_bound (((hF n).comp measurable_fst).mul hg).aestronglyMeasurable 1
    exact Eventually.of_forall fun p => by
      change ‖F n p.1*g p‖ ≤ 1
      rw [Real.norm_eq_abs,abs_of_nonneg (mul_nonneg (hFb n p.1).1 (hgb p).1)]
      exact (mul_le_of_le_one_left (hgb p).1 (hFb n p.1).2).trans (hgb p).2
  have hbi : Integrable (fun p : X × Y => b p.1*g p) (μ.prod ν) := by
    apply Integrable.of_bound ((hb.comp measurable_fst).mul hg).aestronglyMeasurable 1
    filter_upwards [Measure.quasiMeasurePreserving_fst.ae hbb] with p hp
    change ‖b p.1*g p‖ ≤ 1
    rw [Real.norm_eq_abs,abs_of_nonneg (mul_nonneg hp.1 (hgb p).1)]
    exact (mul_le_of_le_one_left (hgb p).1 hp.2).trans (hgb p).2
  have herr (n : ℕ) : Integrable (fun p => ‖G n p-g p‖) (μ.prod ν) := by
    apply Integrable.of_bound ((hG n).sub hg).norm.aestronglyMeasurable 1
    exact Eventually.of_forall fun p => by
      rw [norm_norm,Real.norm_eq_abs,abs_le]
      change -1 ≤ G n p-g p ∧ G n p-g p ≤ 1
      constructor <;> linarith [(hGb n p).1,(hGb n p).2,(hgb p).1,(hgb p).2]
  have hi0 : Tendsto (fun n => ∫ p, F n p.1*g p ∂μ.prod ν) atTop (𝓝 0) := by
    apply squeeze_zero (fun n => integral_nonneg fun p => mul_nonneg (hFb n p.1).1 (hgb p).1) _ hs
    intro n
    apply integral_mono_ae (hFi n) (herr n)
    filter_upwards [hz n] with p hp
    rw [Real.norm_eq_abs]
    calc
      F n p.1*g p = F n p.1*(g p-G n p) := by rw [mul_sub,hp,sub_zero]
      _ ≤ |g p-G n p| := by
        calc
          _ ≤ F n p.1*|g p-G n p| := mul_le_mul_of_nonneg_left (le_abs_self _) (hFb n p.1).1
          _ ≤ 1*|g p-G n p| := mul_le_mul_of_nonneg_right (hFb n p.1).2 (abs_nonneg _)
          _ = _ := one_mul _
      _ = |G n p-g p| := abs_sub_comm _ _
  let v : X → ℝ := fun x => ∫ y, g (x,y) ∂ν
  have hvi : Integrable v μ := hgi.integral_prod_left
  have hlim := hw v hvi
  have hconvert (f : X → ℝ) (hi : Integrable (fun p : X × Y => f p.1*g p) (μ.prod ν)) :
      (∫ p, f p.1*g p ∂μ.prod ν) = ∫ x, f x*v x ∂μ := by
    rw [integral_prod _ hi]
    apply integral_congr_ae
    exact Eventually.of_forall fun x => by
      exact integral_const_mul (f x) (fun y => g (x,y))
  have he0 : (∫ p, b p.1*g p ∂μ.prod ν)=0 := by
    have ht : Tendsto (fun n => ∫ p, F n p.1*g p ∂μ.prod ν) atTop
        (𝓝 (∫ p, b p.1*g p ∂μ.prod ν)) := by
      simpa only [hconvert b hbi,hconvert (F _) (hFi _)] using hlim
    exact tendsto_nhds_unique ht hi0
  exact (integral_eq_zero_iff_of_nonneg_ae
    ((Measure.quasiMeasurePreserving_fst.ae hbb).mono fun p hp => mul_nonneg hp.1 (hgb p).1) hbi).mp he0
end EuclideanFiveColor
end

noncomputable section
open MeasureTheory Filter Topology
namespace EuclideanFiveColor
variable {k : ℕ} (c : ℂ → Fin k) (hc : Measurable c)
def colorIndicator (i : Fin k) (z : ℂ) : ℝ := if c z=i then 1 else 0
include hc in
lemma colorIndicator_measurable (i : Fin k) : Measurable (colorIndicator c i) :=
  measurable_one.piecewise (measurableSet_eq_fun hc measurable_const) measurable_zero
lemma colorIndicator_bounds (i : Fin k) (z : ℂ) : 0 ≤ colorIndicator c i z ∧ colorIndicator c i z ≤ 1 := by
  simp only [colorIndicator]; split_ifs <;> norm_num
include hc in
lemma sample_pair_disjoint (hw : WeakColoring k c) {y : ℂ} {r : ℝ}
    (hy : TypicalSampling c y r) (i : Fin k) :
    ∀ᵐ p ∂angularMeasure.prod angularMeasure,
      sampleFn c y r i p.1*colorIndicator c i (angularSum y r p)=0 := by
  have h1 : ∀ᵐ p ∂angularMeasure.prod angularMeasure, Typical c (y+(r : ℂ)*direction p.1) :=
    Measure.quasiMeasurePreserving_fst.ae hy.2
  have h2 := (angularSum_quasiMeasurePreserving y hy.1.ne').ae (ae_density_actual c hc)
  filter_upwards [h1,h2] with p hp1 hp2
  by_cases ha : c (y+(r : ℂ)*direction p.1)=i
  · have hb : c (angularSum y r p) ≠ i := by
      intro hb
      have hdist : ‖(y+(r : ℂ)*direction p.1)-angularSum y r p‖=1 := by
        simp [angularSum]
      apply weak_density_proper c hc hw i hdist
      · simpa only [Typical,ha] using hp1
      · simpa only [hb] using hp2
    simp [sampleFn,colorIndicator,ha,hb]
  · simp [sampleFn,ha]
lemma trace_pair_disjoint (hw : WeakColoring k c) {x : ℂ} {b : TraceVector k}
    (hb : IsTrace c hc x b) (i : Fin k) :
    ∀ᵐ p ∂angularMeasure.prod angularMeasure,
      traceValue b i p.1*colorIndicator c i (angularSum x 1 p)=0 := by
  obtain ⟨y,r,ht,hy,hr,hweak⟩ := trace_realization_weakStar c hc hb
  have hbnd := trace_bounds c hc hb
  apply weak_strong_disjoint (F := fun n => sampleFn c (y n) (r n) i)
    (G := fun n p => colorIndicator c i (angularSum (y n) (r n) p))
    (fun n => sampleFn_measurable c hc (y n) (r n) i) (Lp.stronglyMeasurable _).measurable
    (fun n => (colorIndicator_measurable c hc i).comp (angularSum_measurable _ _))
    ((colorIndicator_measurable c hc i).comp (angularSum_measurable _ _))
    (fun n t => ⟨sampleFn_nonneg c _ _ _ t,sampleFn_le_one c _ _ _ t⟩)
    (Eventually.and (hbnd.1 i) (hbnd.2.1 i))
    (fun n p => colorIndicator_bounds c i _) (fun p => colorIndicator_bounds c i _)
    (hweak i) (angularSum_tendsto_L1 hr hy (colorIndicator_measurable c hc i) (colorIndicator_bounds c i))
    (fun n => sample_pair_disjoint c hc hw (ht n) i)
lemma palette_first_exclusion (hw : WeakColoring k c) (x : ℂ) (i : Fin k) :
    ∀ᵐ p ∂angularMeasure.prod angularMeasure,
      p.1 ∈ paletteSet c hc x i → c (angularSum x 1 p) ≠ i := by
  have hall : ∀ᵐ p ∂angularMeasure.prod angularMeasure, ∀ b ∈ paletteGenerators c hc x i,
      traceValue b.1 i p.1*colorIndicator c i (angularSum x 1 p)=0 :=
    (ae_ball_iff (paletteGenerators_countable c hc x i)).mpr
      (fun b _ => trace_pair_disjoint c hc hw b.2 i)
  filter_upwards [hall] with p hp
  intro hm he
  obtain ⟨b,hb,hpos⟩ := Set.mem_iUnion₂.mp hm
  have hzero := hp b hb
  have hval : colorIndicator c i (angularSum x 1 p)=1 := by simp [colorIndicator,he]
  rw [hval,mul_one] at hzero
  exact (show 0 < traceValue b.1 i p.1 from hpos).ne' hzero
def FlatDensityZero (A : Set (ℝ × ℝ)) (p : ℝ × ℝ) : Prop :=
  Tendsto (fun r : ℝ => volume.real (A ∩ Metric.closedBall p r)/r^2) (𝓝[>] 0) (𝓝 0)
def LineDensityZero (D : Set ℝ) (t : ℝ) : Prop :=
  Tendsto (fun r : ℝ => volume.real (D ∩ Metric.closedBall t r)/r) (𝓝[>] 0) (𝓝 0)
lemma flatDensityZero_prod {D : Set ℝ} {t u : ℝ} (hD : LineDensityZero D t) :
    FlatDensityZero (D ×ˢ univ) (t,u) := by
  have h := hD.const_mul 2
  simp only [mul_zero] at h
  apply h.congr'
  filter_upwards [self_mem_nhdsWithin] with r hr
  have hp : 0 < r := hr
  rw [← closedBall_prod_same,prod_inter_prod,univ_inter,Measure.volume_eq_prod]
  simp only [Measure.real,Measure.prod_prod,ENNReal.toReal_mul,Real.volume_closedBall,
    ENNReal.toReal_ofReal (by positivity : 0 ≤ 2*r)]
  change 2*(volume.real (D ∩ Metric.closedBall t r)/r) =
    volume.real (D ∩ Metric.closedBall t r)*(2*r)/r^2
  field_simp [hp.ne']
lemma circleSum_densityZero {D : Set ℝ} {A : Set RealPlane} {t u : ℝ} (x : RealPlane)
    (hD : LineDensityZero D t) (hu : Real.sin (u-t) ≠ 0)
    (hAD : ∀ᵐ q : RealPlane ∂volume, x+circleSum 1 q ∈ A → q.1 ∈ D) :
    FlatDensityZero A (x+circleSum 1 (t,u)) := by
  let F : RealPlane → RealPlane := fun q => x+circleSum 1 q
  have hreg : (1 : ℝ)*Real.sin (u-t) ≠ 0 := by simpa only [one_mul] using hu
  obtain ⟨s,hso,hps,K,hK⟩ := circleSum_local_antilipschitz (r := 1) (p := (t,u)) hreg
  have ha : AntilipschitzWith (K+1) (s.domRestrict F) := by
    apply AntilipschitzWith.of_le_mul_dist
    intro a b
    have h := hK.le_mul_dist a b
    simp only [domRestrict] at h
    simp only [domRestrict,F,dist_add_left,NNReal.coe_add,NNReal.coe_one]
    nlinarith [dist_nonneg (x := circleSum 1 a.1) (y := circleSum 1 b.1)]
  let L := circleSumDerivEquiv (r := 1) (p := (t,u)) hreg
  have hd : HasStrictFDerivAt F (L : RealPlane →L[ℝ] RealPlane) (t,u) :=
    (circleSum_strict 1 (t,u)).const_add x
  have him : F '' s ∈ 𝓝 (F (t,u)) := by
    rw [← hd.map_nhds_eq_of_equiv]
    exact image_mem_map (hso.mem_nhds hps)
  have hl : LipschitzWith 2 F := LipschitzWith.of_dist_le_mul fun a b => by
    simpa only [F,dist_add_left] using circleSum_one_lipschitz.dist_le_mul a b
  apply (flatDensityZero_prod hD).transport hps him
    (show LipschitzWith 2 (s.domRestrict F) from fun a b => hl a.1 b.1) ha (by positivity)
  filter_upwards [hAD] with q hq
  rintro ⟨hm,_⟩
  exact ⟨hq hm,mem_univ _⟩
end EuclideanFiveColor
end

noncomputable section
open MeasureTheory Filter Topology Set
namespace EuclideanFiveColor
lemma complex_ball_flat_ball {z w : ℂ} {r : ℝ} (h : w ∈ Metric.closedBall z r) :
    Complex.equivRealProdCLM w ∈ Metric.closedBall (Complex.equivRealProdCLM z) r := by
  rw [Metric.mem_closedBall,dist_eq_norm] at h ⊢
  change max ‖w.re-z.re‖ ‖w.im-z.im‖ ≤ r
  simpa only [Real.norm_eq_abs,Complex.sub_re,Complex.sub_im] using
    max_le ((Complex.abs_re_le_norm (w-z)).trans h) ((Complex.abs_im_le_norm (w-z)).trans h)
lemma flat_to_complex_densityZero {A : Set ℂ} {z : ℂ}
    (h : FlatDensityZero (Complex.equivRealProdCLM.symm ⁻¹' A) (Complex.equivRealProdCLM z)) :
    Tendsto (fun r : ℝ => volume (A ∩ Metric.closedBall z r)/volume (Metric.closedBall z r))
      (𝓝[>] 0) (𝓝 (0 : ENNReal)) := by
  have ht := h.const_mul (Real.pi)⁻¹
  simp only [mul_zero] at ht
  have he := ENNReal.continuous_ofReal.continuousAt.tendsto.comp ht
  simp only [ENNReal.ofReal_zero] at he
  apply tendsto_of_tendsto_of_tendsto_of_le_of_le' tendsto_const_nhds he
    (Eventually.of_forall fun _ => zero_le) ?_
  filter_upwards [self_mem_nhdsWithin] with r hr
  have hp : 0 < r := hr
  let B := Complex.equivRealProdCLM.symm ⁻¹' A ∩ Metric.closedBall (Complex.equivRealProdCLM z) r
  have hm : volume (A ∩ Metric.closedBall z r) ≤ (volume : Measure (ℝ × ℝ)) B := by
    apply (measure_mono (t := Complex.equivRealProdCLM ⁻¹' B) ?_).trans
      (Complex.volume_preserving_equiv_real_prod.measure_preimage_le B)
    intro w hw
    exact ⟨by simpa only [Set.mem_preimage,ContinuousLinearEquiv.symm_apply_apply] using hw.1,complex_ball_flat_ball hw.2⟩
  have hfin : (volume : Measure (ℝ × ℝ)) B ≠ ⊤ :=
    ne_top_of_le_ne_top (isCompact_closedBall _ _).measure_ne_top (measure_mono inter_subset_right)
  have hfinA : volume (A ∩ Metric.closedBall z r) ≠ ⊤ := ne_top_of_le_ne_top (isCompact_closedBall z r).measure_ne_top
    (measure_mono (s := A ∩ Metric.closedBall z r) inter_subset_right)
  apply (ENNReal.toReal_le_toReal (ENNReal.div_ne_top hfinA
    (Metric.measure_closedBall_pos volume z hp).ne') ENNReal.ofReal_ne_top).mp
  rw [ENNReal.toReal_div,Complex.volume_closedBall,ENNReal.toReal_mul,ENNReal.toReal_pow,
    ENNReal.toReal_ofReal hp.le,ENNReal.coe_toReal,NNReal.coe_real_pi,
    ENNReal.toReal_ofReal (by positivity)]
  calc
    _ ≤ volume.real B/(r^2*Real.pi) := div_le_div_of_nonneg_right (ENNReal.toReal_mono hfin hm) (by positivity)
    _ = _ := by dsimp [B]; ring
lemma ae_lineDensityZero_compl {D : Set ℝ} (hD : MeasurableSet D) :
    ∀ᵐ t : ℝ ∂volume, t ∈ D → LineDensityZero Dᶜ t := by
  have hh := Besicovitch.ae_tendsto_measure_inter_div_of_measurableSet volume hD.compl
  filter_upwards [hh] with t ht htd
  rw [Set.indicator_of_notMem (show t ∉ Dᶜ from by simpa only [mem_compl_iff,not_not] using htd)] at ht
  have hreal := (ENNReal.tendsto_toReal (by simp : (0 : ENNReal) ≠ ⊤)).comp ht
  simp only [ENNReal.toReal_zero,Function.comp_def,ENNReal.toReal_div] at hreal
  have h := hreal.const_mul 2
  simp only [mul_zero] at h
  apply h.congr'
  filter_upwards [self_mem_nhdsWithin] with r hr
  have hp : 0 < r := hr
  rw [Real.volume_closedBall,ENNReal.toReal_ofReal (by positivity : 0 ≤ 2*r)]
  change 2*(volume.real (Dᶜ ∩ Metric.closedBall t r)/(2*r)) = _
  field_simp
end EuclideanFiveColor
end

noncomputable section
open MeasureTheory Filter Topology Set
namespace EuclideanFiveColor
variable {k : ℕ} (c : ℂ → Fin k) (hc : Measurable c)
def liftPalette (x : ℂ) (i : Fin k) : Set ℝ :=
  ((↑) : ℝ → Angles) ⁻¹' paletteSet c hc x i
lemma liftPalette_measurable (x : ℂ) (i : Fin k) : MeasurableSet (liftPalette c hc x i) :=
  (paletteSet_measurable c hc x i).preimage angleMk_quasiMeasurePreserving.measurable
lemma palette_spatial_densityZero (hw : WeakColoring k c) {x : ℂ} {i : Fin k} {t u : ℝ}
    (ht : LineDensityZero (liftPalette c hc x i)ᶜ t) (hu : Real.sin (u-t) ≠ 0) :
    Tendsto (fun r : ℝ => volume ({z | c z=i} ∩ Metric.closedBall (angularSum x 1 (angleChart (t,u))) r)/
      volume (Metric.closedBall (angularSum x 1 (angleChart (t,u))) r))
        (𝓝[>] 0) (𝓝 (0 : ENNReal)) := by
  apply flat_to_complex_densityZero
  have he := anglePair_quasiMeasurePreserving.ae (palette_first_exclusion c hc hw x i)
  have hAD : ∀ᵐ q : RealPlane ∂volume, Complex.equivRealProdCLM x+circleSum 1 q ∈
      Complex.equivRealProdCLM.symm ⁻¹' {z | c z=i} → q.1 ∈ (liftPalette c hc x i)ᶜ := by
    filter_upwards [he] with q hq hm hd
    apply hq hd
    change c (Complex.equivRealProdCLM.symm (Complex.equivRealProdCLM x+circleSum 1 q))=i at hm
    change c (angularSum x 1 (angleChart q))=i
    rwa [angularSum_chart]
  have hb := circleSum_densityZero (Complex.equivRealProdCLM x) ht hu hAD
  rwa [← circleSum_chart x 1 (t,u)] at hb
lemma palette_spatial_not_densityOne (hw : WeakColoring k c) {x : ℂ} {i : Fin k} {t u : ℝ}
    (ht : LineDensityZero (liftPalette c hc x i)ᶜ t) (hu : Real.sin (u-t) ≠ 0) :
    ¬ DensityOne {z | c z=i} (angularSum x 1 (angleChart (t,u))) := by
  intro hd
  exact zero_ne_one (tendsto_nhds_unique (palette_spatial_densityZero c hc hw ht hu) hd)
end EuclideanFiveColor
end

noncomputable section
open MeasureTheory Filter Topology Set
namespace EuclideanFiveColor
variable {k : ℕ} (c : ℂ → Fin k) (hc : Measurable c)
lemma palette_sample_branch_exclusion (hw : WeakColoring k c) {x y : ℂ} {r : ℝ}
    (hy : TypicalSampling c y r) (i : Fin k) {I : Set ℝ} (hI : MeasurableSet I) {s t : ℝ → ℝ}
    (hq : Measure.QuasiMeasurePreserving s (volume.restrict I) volume)
    (hn : ∀ f ∈ I, Real.sin (t f-s f) ≠ 0)
    (he : ∀ f ∈ I, y+(r : ℂ)*direction (f : Angles)=angularSum x 1 (angleChart (s f,t f))) :
    ∀ᵐ f : ℝ ∂volume.restrict I,
      sampleFn c y r i (f : Angles)*(liftPalette c hc x i).indicator (fun _ => (1 : ℝ)) (s f)=0 := by
  have hd := hq.ae (ae_lineDensityZero_compl (liftPalette_measurable c hc x i))
  have ht := ae_restrict_of_ae (s := I) (angleMk_quasiMeasurePreserving.ae hy.2)
  filter_upwards [hd,ht,ae_restrict_mem hI] with f hfd hft hf
  by_cases hs : s f ∈ liftPalette c hc x i
  · have hzero := palette_spatial_not_densityOne c hc hw (hfd hs) (hn f hf)
    have hi : c (y+(r : ℂ)*direction (f : Angles)) ≠ i := by
      intro hi
      apply hzero
      rw [← he f hf]
      simpa only [Typical,hi] using hft
    simp only [sampleFn,ite_eq_right hi,zero_mul]
  · rw [indicator_of_notMem hs,mul_zero]
end EuclideanFiveColor
end

end OAI
