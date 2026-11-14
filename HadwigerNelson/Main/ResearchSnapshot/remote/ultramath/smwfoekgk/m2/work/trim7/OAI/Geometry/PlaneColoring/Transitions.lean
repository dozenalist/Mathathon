import OAI.Analysis.PlaneSpectrum.CircleOperator

namespace OAI

noncomputable section
open MeasureTheory MeasureTheory.Measure Filter Topology Set
namespace EuclideanFiveColor
variable {k : ℕ} (c : ℂ → Fin k)
def transitionSet (i j : Fin k) (x : ℂ) (R : ℝ) (h : ℂ) : Set ℂ :=
  {q | q ∈ Metric.ball x R ∧ ((c q=i ∧ c (q+h)=j) ∨ (c q=j ∧ c (q+h)=i))}
lemma transitionSet_measurable (hc : Measurable c) (i j : Fin k) (x : ℂ) (R : ℝ) (h : ℂ) :
    MeasurableSet (transitionSet c i j x R h) := by
  exact measurableSet_ball.inter (((measurableSet_eq_fun hc measurable_const).inter
    (measurableSet_eq_fun (hc.comp (measurable_id.add_const h)) measurable_const)).union
    ((measurableSet_eq_fun hc measurable_const).inter
    (measurableSet_eq_fun (hc.comp (measurable_id.add_const h)) measurable_const)))
lemma transitionSet_finite (i j : Fin k) (x : ℂ) (R : ℝ) (h : ℂ) :
    volume (transitionSet c i j x R h) < ⊤ :=
  (measure_mono (fun _ hq => Metric.ball_subset_closedBall hq.1)).trans_lt
    (isCompact_closedBall x R).measure_lt_top
def transitionRatio (i j : Fin k) (x : ℂ) (R : ℝ) (h : ℂ) : ENNReal :=
  volume (transitionSet c i j x R h) / ENNReal.ofReal ‖h‖
def TransitionEdge (i j : Fin k) (x : ℂ) : Prop :=
  i ≠ j ∧ ∀ R : ℝ, 0<R → 0 < limsup (transitionRatio c i j x R) (𝓝[≠] (0:ℂ))
lemma transition_abundance {i j : Fin k} {x : ℂ} (he : TransitionEdge c i j x)
    {R : ℝ} (hR : 0<R) : ∃ a : ℝ, 0<a ∧
      ∃ᶠ h in 𝓝[≠] (0:ℂ), a*‖h‖ < volume.real (transitionSet c i j x R h) := by
  obtain ⟨a,_,ha,hal⟩ := ENNReal.lt_iff_exists_real_btwn.mp (he.2 R hR)
  have ha0 : 0<a := ENNReal.ofReal_pos.mp ha
  refine ⟨a,ha0,?_⟩
  have hf := frequently_lt_of_lt_limsup (h := hal)
  refine (hf.and_eventually self_mem_nhdsWithin).mono ?_
  intro h hh
  have hne : h≠0 := hh.2
  have hn : ENNReal.ofReal ‖h‖≠0 := (ENNReal.ofReal_pos.mpr (norm_pos_iff.mpr hne)).ne'
  have hm : ENNReal.ofReal a*ENNReal.ofReal ‖h‖ < volume (transitionSet c i j x R h) :=
    (ENNReal.lt_div_iff_mul_lt (Or.inl hn) (Or.inl ENNReal.ofReal_ne_top)).mp hh.1
  rw [← ENNReal.ofReal_mul ha0.le] at hm
  exact (ENNReal.ofReal_lt_iff_lt_toReal (mul_nonneg ha0.le (norm_nonneg h)) (transitionSet_finite c i j x R h).ne).mp hm
lemma colorMass_own_zero (hc : Measurable c) (hw : WeakColoring k c) {q : ℂ}
    (hq : Typical c q) (hs : TypicalSampling c q 1) : colorMass c (c q) q=0 := by
  apply integral_eq_zero_of_ae
  filter_upwards [hs.2] with t ht
  simp only [Complex.ofReal_one,one_mul] at ht
  have hn : c (q+direction t)≠c q := by
    intro he
    have hd : ‖q-(q+direction t)‖=1 := by
      simp only [sub_add_cancel_left,norm_neg]
      exact Circle.norm_coe _
    exact weak_density_proper c hc hw (c q) hd hq (by simpa only [Typical,he] using ht)
  simp only [sampleFn,Complex.ofReal_one,one_mul,ite_eq_right hn,Pi.zero_apply]
lemma exists_energy_small {X : Type*} [MeasurableSpace X] (μ : Measure X)
    {T : Set X} (hT : MeasurableSet T) (hfin : μ T < ⊤) {E : X → ℝ}
    (hE : Integrable E μ) (hn : ∀ᵐ q ∂μ, 0≤E q) {P : X → Prop} (hP : ∀ᵐ q ∂μ, P q)
    {d : ℝ} (hi : (∫ q, E q ∂μ) < d*μ.real T) : ∃ q ∈ T, P q ∧ E q<d := by
  by_contra! h
  have : IsFiniteMeasure (μ.restrict T) := ⟨by simpa only [Measure.restrict_apply_univ] using hfin⟩
  have hge : ∀ᵐ q ∂μ.restrict T, d≤E q := by
    filter_upwards [ae_restrict_mem hT,ae_restrict_of_ae hP] with q hq hp
    exact h q hq hp
  have hl := integral_mono_ae (integrable_const d) hE.restrict hge
  have hr := integral_mono_measure (μ.restrict_le_self (s := T)) hn hE
  have he : (∫ _q in T, d ∂μ)=d*μ.real T := by simp [mul_comm]
  rw [he] at hl
  exact (not_lt_of_ge (hl.trans hr)) hi
end EuclideanFiveColor
end

noncomputable section
open MeasureTheory MeasureTheory.Measure Filter Topology Set
namespace EuclideanFiveColor
variable {k : ℕ} (c : ℂ → Fin k) (hc : Measurable c)
end EuclideanFiveColor
end

end OAI
