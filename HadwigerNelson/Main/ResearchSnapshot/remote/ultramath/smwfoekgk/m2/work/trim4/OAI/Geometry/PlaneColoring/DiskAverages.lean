import OAI.Geometry.PlaneColoring.Accumulation

namespace OAI

noncomputable section
open scoped Classical
open Set Filter Topology MeasureTheory MeasureTheory.Measure
namespace EuclideanFiveColor
def diskLaw (ε : ℝ) : Measure ℂ :=
  (volume (Metric.ball (0:ℂ) ε))⁻¹ • volume.restrict (Metric.ball 0 ε)
lemma diskLaw_absolutelyContinuous (ε : ℝ) : diskLaw ε ≪ volume :=
  (Measure.restrict_le_self (s := Metric.ball (0:ℂ) ε)).absolutelyContinuous.smul_left _
lemma diskLaw_probability {ε : ℝ} (hε : 0<ε) : IsProbabilityMeasure (diskLaw ε) := by
  constructor
  simp only [diskLaw,Measure.smul_apply,Measure.restrict_apply_univ,smul_eq_mul]
  exact ENNReal.inv_mul_cancel (Metric.measure_ball_pos volume 0 hε).ne'
    ((measure_mono Metric.ball_subset_closedBall).trans_lt (isCompact_closedBall (0:ℂ) ε).measure_lt_top).ne
def colorFn {k : ℕ} (c : ℂ → Fin k) (i : Fin k) (z : ℂ) : ℝ := if c z=i then 1 else 0
lemma colorFn_measurable {k : ℕ} {c : ℂ → Fin k} (hc : Measurable c) (i : Fin k) :
    Measurable (colorFn c i) :=
  measurable_one.piecewise (measurableSet_eq_fun hc measurable_const) measurable_zero
lemma colorFn_nonneg {k : ℕ} (c : ℂ → Fin k) (i : Fin k) (z : ℂ) : 0≤colorFn c i z := by
  simp only [colorFn]; split_ifs <;> norm_num
lemma colorFn_le_one {k : ℕ} (c : ℂ → Fin k) (i : Fin k) (z : ℂ) : colorFn c i z≤1 := by
  simp only [colorFn]; split_ifs <;> norm_num
lemma colorFn_integrable {k : ℕ} {c : ℂ → Fin k} (hc : Measurable c) (i : Fin k)
    {μ : Measure ℂ} [IsFiniteMeasure μ] (q : ℂ) : Integrable (fun v => colorFn c i (q+v)) μ := by
  apply Integrable.of_bound ((colorFn_measurable hc i).comp (measurable_const.add measurable_id)).aestronglyMeasurable 1
  exact Eventually.of_forall fun v => by
    change ‖colorFn c i (q+v)‖ ≤ 1
    rw [Real.norm_eq_abs,abs_of_nonneg (colorFn_nonneg c i (q+v))]
    exact colorFn_le_one c i (q+v)
def diskAverage {k : ℕ} (c : ℂ → Fin k) (ε : ℝ) (i : Fin k) (q : ℂ) : ℝ :=
  ∫ v, colorFn c i (q+v) ∂diskLaw ε
lemma diskAverage_nonneg {k : ℕ} (c : ℂ → Fin k) (ε : ℝ) (i : Fin k) (q : ℂ) :
    0≤diskAverage c ε i q := integral_nonneg (fun v => colorFn_nonneg c i (q+v))
lemma diskAverage_le_one {k : ℕ} {c : ℂ → Fin k} (hc : Measurable c) {ε : ℝ} (hε : 0<ε)
    (i : Fin k) (q : ℂ) : diskAverage c ε i q≤1 := by
  have := diskLaw_probability hε
  simpa only [diskAverage,integral_const,probReal_univ,one_smul] using integral_mono (colorFn_integrable (μ := diskLaw ε) hc i q) (integrable_const (1:ℝ))
    (fun v => colorFn_le_one c i (q+v))
lemma diskAverage_sum {k : ℕ} {c : ℂ → Fin k} (hc : Measurable c) {ε : ℝ} (hε : 0<ε)
    (q : ℂ) : ∑ i,diskAverage c ε i q=1 := by
  have := diskLaw_probability hε
  simp only [diskAverage]
  rw [← integral_finsetSum _ (fun i _ => colorFn_integrable (μ := diskLaw ε) hc i q)]
  simp [colorFn]
lemma colorFn_unit_pair {k : ℕ} {c : ℂ → Fin k} (hc : Measurable c) (hw : WeakColoring k c)
    {q z : ℂ} (hunit : ‖q-z‖=1) (i : Fin k) :
    ∀ᵐ v ∂(volume : Measure ℂ), colorFn c i (q+v)+colorFn c i (z+v)≤1 := by
  obtain ⟨t,ht⟩ := direction_exists (u := z-q) (by simpa only [norm_sub_rev] using hunit)
  have ha := (measurePreserving_add_left (volume : Measure ℂ) q).quasiMeasurePreserving.ae
    (weak_all_directions c hc hw t)
  filter_upwards [ha] with v hv
  have hne : c (q+v)≠c (z+v) := by
    convert hv using 1
    rw [ht]
    congr 1
    ring
  simp only [colorFn]
  split_ifs with h1 h2 h2 <;> try norm_num
  exact False.elim (hne (h1.trans h2.symm))
lemma diskAverage_unit_pair {k : ℕ} {c : ℂ → Fin k} (hc : Measurable c) (hw : WeakColoring k c)
    {ε : ℝ} (hε : 0<ε) {q z : ℂ} (hunit : ‖q-z‖=1) (i : Fin k) :
    diskAverage c ε i q+diskAverage c ε i z≤1 := by
  have := diskLaw_probability hε
  rw [diskAverage,diskAverage,← integral_add (colorFn_integrable (μ := diskLaw ε) hc i q) (colorFn_integrable (μ := diskLaw ε) hc i z)]
  simpa using integral_mono_ae ((colorFn_integrable (μ := diskLaw ε) hc i q).add (colorFn_integrable (μ := diskLaw ε) hc i z))
    (integrable_const (1:ℝ)) ((diskLaw_absolutelyContinuous ε).ae_le (colorFn_unit_pair hc hw hunit i))
end EuclideanFiveColor
end

noncomputable section
open scoped Classical symmDiff
open Set Filter Topology MeasureTheory MeasureTheory.Measure
namespace EuclideanFiveColor
end EuclideanFiveColor
end

noncomputable section
open scoped Classical
open Set Filter Topology MeasureTheory MeasureTheory.Measure
namespace EuclideanFiveColor
variable {k : ℕ} {c : ℂ → Fin k}
end EuclideanFiveColor
end

noncomputable section
open scoped Classical
open Set Filter Topology MeasureTheory MeasureTheory.Measure
namespace EuclideanFiveColor
variable {k : ℕ} {c : ℂ → Fin k}
end EuclideanFiveColor
end

end OAI
