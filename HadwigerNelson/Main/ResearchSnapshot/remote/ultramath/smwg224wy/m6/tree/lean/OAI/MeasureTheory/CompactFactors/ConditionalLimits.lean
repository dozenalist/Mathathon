import OAI.MeasureTheory.CompactFactors.Approximation

namespace OAI

noncomputable section

open scoped ComplexConjugate
open scoped BigOperators
open scoped BigOperators BoundedContinuousFunction
open Filter Topology
open MeasureTheory Filter
open scoped ENNReal ComplexConjugate
open MeasureTheory ProbabilityTheory
open scoped ComplexConjugate
open scoped BigOperators
open scoped BigOperators
open Polynomial
open MeasureTheory
open scoped BigOperators
open MeasureTheory
open scoped BigOperators
open MeasureTheory
open MeasureTheory ProbabilityTheory
open scoped BigOperators
open MeasureTheory
open scoped BigOperators ComplexConjugate
open MeasureTheory ProbabilityTheory
open scoped ENNReal BigOperators
open MeasureTheory Filter
open scoped Topology ENNReal NNReal
open MeasureTheory
open scoped ENNReal
open MeasureTheory ProbabilityTheory
open scoped ENNReal
open MeasureTheory ProbabilityTheory

/-! Bounded finite-dimensional L² approximation at a generated limit factor.
The filtration is the pullback of an increasing sequence of earlier factors;
no martingale convergence theorem beyond Mathlib is assumed. -/
namespace EuclideanFiveColor.LimitDensity
open MeasureTheory Filter
open scoped Topology BigOperators
variable {Y : Type*} [mY : MeasurableSpace Y]

def clip (C t : ℝ) : ℝ := max (-C) (min C t)
lemma clip_bound {C : ℝ} (hC : 0 ≤ C) (t : ℝ) : |clip C t| ≤ C := by
  rw [abs_le]
  exact ⟨le_max_left _ _, max_le (by linarith) (min_le_left _ _)⟩
lemma clip_eq {C t : ℝ} (ht : |t| ≤ C) : clip C t = t := by
  obtain ⟨hl, hu⟩ := abs_le.mp ht
  simp only [clip, min_eq_right hu, max_eq_right hl]
lemma continuous_clip (C : ℝ) : Continuous (clip C) := by
  unfold clip
  fun_prop

/-- A bounded vector measurable for a generated join is an L² limit of
uniformly bounded functions measurable at finite stages. -/
theorem bounded_vector_approximation
    (ν : Measure Y) [IsProbabilityMeasure ν] (ℱ : Filtration ℕ mY)
    (m : ℕ) (H : Y → Fin m → ℂ) (hH : Measurable[⨆ n, ℱ n] H)
    (C : ℝ) (hC : 0 ≤ C) (hbound : ∀ y, ‖H y‖ ≤ C) :
    ∃ Hn : ℕ → Y → Fin m → ℂ,
      (∀ n, Measurable[ℱ n] (Hn n)) ∧
      (∀ n y, ‖Hn n y‖ ≤ 2*C) ∧
      (∀ n, Integrable (fun y => dist (H y) (Hn n y)^2) ν) ∧
      Tendsto (fun n => ∫ y, dist (H y) (Hn n y)^2 ∂ν) atTop (𝓝 0) := by
  classical
  have hle : (⨆ n, ℱ n) ≤ mY := iSup_le fun n => ℱ.le n
  have hHm : Measurable H := hH.mono hle le_rfl
  let R : Fin m → Y → ℝ := fun j y => (H y j).re
  let I : Fin m → Y → ℝ := fun j y => (H y j).im
  have hR (j : Fin m) : Measurable[⨆ n, ℱ n] (R j) := by
    let : MeasurableSpace Y := ⨆ n, ℱ n
    exact Complex.measurable_re.comp ((measurable_pi_iff.mp hH) j)
  have hI (j : Fin m) : Measurable[⨆ n, ℱ n] (I j) := by
    let : MeasurableSpace Y := ⨆ n, ℱ n
    exact Complex.measurable_im.comp ((measurable_pi_iff.mp hH) j)
  have hRB (j : Fin m) (y : Y) : |R j y| ≤ C :=
    (Complex.abs_re_le_norm _).trans ((norm_le_pi_norm (H y) j).trans (hbound y))
  have hIB (j : Fin m) (y : Y) : |I j y| ≤ C :=
    (Complex.abs_im_le_norm _).trans ((norm_le_pi_norm (H y) j).trans (hbound y))
  have hRi (j : Fin m) : Integrable (R j) ν :=
    Integrable.of_bound ((hR j).mono hle le_rfl).aestronglyMeasurable C
      (Filter.Eventually.of_forall fun y => by simpa only [Real.norm_eq_abs] using hRB j y)
  have hIi (j : Fin m) : Integrable (I j) ν :=
    Integrable.of_bound ((hI j).mono hle le_rfl).aestronglyMeasurable C
      (Filter.Eventually.of_forall fun y => by simpa only [Real.norm_eq_abs] using hIB j y)
  let Hn : ℕ → Y → Fin m → ℂ := fun n y j =>
    (clip C ((ν[R j | ℱ n]) y) : ℂ) + Complex.I * (clip C ((ν[I j | ℱ n]) y) : ℂ)
  have hHn (n : ℕ) : Measurable[ℱ n] (Hn n) := by
    let : MeasurableSpace Y := ℱ n
    apply Measurable.of_eval
    intro j
    exact ((Complex.measurable_ofReal.comp ((continuous_clip C).measurable.comp
      stronglyMeasurable_condExp.measurable))).add
      (measurable_const.mul (Complex.measurable_ofReal.comp ((continuous_clip C).measurable.comp
        stronglyMeasurable_condExp.measurable)))
  have hBn (n : ℕ) (y : Y) : ‖Hn n y‖ ≤ 2*C := by
    rw [pi_norm_le_iff_of_nonneg (by positivity)]
    intro j
    calc
      ‖Hn n y j‖ ≤ ‖(clip C ((ν[R j | ℱ n]) y) : ℂ)‖ +
          ‖Complex.I * (clip C ((ν[I j | ℱ n]) y) : ℂ)‖ := norm_add_le _ _
      _ = |clip C ((ν[R j | ℱ n]) y)| + |clip C ((ν[I j | ℱ n]) y)| := by
        simp only [norm_mul, Complex.norm_I, one_mul, Complex.norm_real, Real.norm_eq_abs]
      _ ≤ 2*C := by linarith [clip_bound hC ((ν[R j | ℱ n]) y), clip_bound hC ((ν[I j | ℱ n]) y)]
  have hconv : ∀ᵐ y ∂ν, Tendsto (fun n => Hn n y) atTop (𝓝 (H y)) := by
    have hr (j : Fin m) := (hRi j).tendsto_ae_condExp (hR j).stronglyMeasurable
    have hi (j : Fin m) := (hIi j).tendsto_ae_condExp (hI j).stronglyMeasurable
    filter_upwards [ae_all_iff.mpr hr, ae_all_iff.mpr hi] with y hyr hyi
    apply tendsto_pi_nhds.mpr
    intro j
    have hr' := (continuous_clip C).continuousAt.tendsto.comp (hyr j)
    have hi' := (continuous_clip C).continuousAt.tendsto.comp (hyi j)
    rw [clip_eq (hRB j y)] at hr'
    rw [clip_eq (hIB j y)] at hi'
    have ht := (Complex.continuous_ofReal.continuousAt.tendsto.comp hr').add
      ((Complex.continuous_ofReal.continuousAt.tendsto.comp hi').const_mul Complex.I)
    convert ht using 1
    · rfl
    · simp only [R, I, Complex.re_add_im, mul_comm Complex.I]
  have hdist (n : ℕ) (y : Y) : dist (H y) (Hn n y)^2 ≤ (3*C)^2 := by
    have hd : dist (H y) (Hn n y) ≤ 3*C :=
      (dist_le_norm_add_norm _ _).trans (by linarith [hbound y, hBn n y])
    exact pow_le_pow_left₀ dist_nonneg hd 2
  have hint (n : ℕ) : Integrable (fun y => dist (H y) (Hn n y)^2) ν :=
    Integrable.of_bound ((hHm.dist ((hHn n).mono (ℱ.le n) le_rfl)).pow_const 2).aestronglyMeasurable
      ((3*C)^2) (Filter.Eventually.of_forall fun y => by
        simpa only [Real.norm_eq_abs, abs_sq] using hdist n y)
  refine ⟨Hn, hHn, hBn, hint, ?_⟩
  simpa only [integral_zero] using tendsto_integral_of_dominated_convergence
    (f := fun _ : Y => (0 : ℝ)) (fun _ : Y => (3*C)^2)
    (fun n => (hint n).aestronglyMeasurable) (integrable_const _) (fun n =>
      Filter.Eventually.of_forall fun y => by simpa only [Real.norm_eq_abs, abs_sq] using hdist n y)
    (hconv.mono fun y hy => by
      have ht := ((tendsto_const_nhds : Tendsto (fun _ : ℕ => H y) atTop (𝓝 (H y))).dist hy).pow 2
      simpa only [dist_self, zero_pow (by norm_num : (2 : ℕ) ≠ 0)] using ht)

/-- At a generated limit factor, one earlier factor carries a bounded
finite-vector approximant, with a pointwise bounded measurable representative. -/
theorem generated_factor_approximation
    {Z : ℕ → Type*} [∀ n, MeasurableSpace (Z n)]
    (ν : Measure Y) [IsProbabilityMeasure ν] (p : ∀ n, Y → Z n)
    (hp : ∀ n, Measurable (p n))
    (hmono : Monotone (fun n => (inferInstance : MeasurableSpace (Z n)).comap (p n)))
    (hgen : (⨆ n, (inferInstance : MeasurableSpace (Z n)).comap (p n)) = mY)
    (m : ℕ) (H : Y → Fin m → ℂ) (hH : Measurable H)
    (C : ℝ) (hC : 0 ≤ C) (hbound : ∀ y, ‖H y‖ ≤ C)
    (ε : ℝ) (hε : 0 < ε) :
    ∃ n, ∃ H₀ : Z n → Fin m → ℂ, Measurable H₀ ∧ (∀ z, ‖H₀ z‖ ≤ 2*C) ∧
      Integrable (fun y => dist (H y) (H₀ (p n y))^2) ν ∧
      (∫ y, dist (H y) (H₀ (p n y))^2 ∂ν) < ε^2 := by
  classical
  let ℱ : Filtration ℕ mY := ⟨fun n => (inferInstance : MeasurableSpace (Z n)).comap (p n),
    hmono, fun n => (hp n).comap_le⟩
  have hHg : Measurable[⨆ n, ℱ n] H := by
    change Measurable[⨆ n, (inferInstance : MeasurableSpace (Z n)).comap (p n)] H
    rwa [hgen]
  obtain ⟨Hn, hHn, hBn, hint, hlim⟩ := bounded_vector_approximation ν ℱ m H hHg C hC hbound
  obtain ⟨n, hn⟩ := (hlim.eventually (gt_mem_nhds (sq_pos_of_pos hε))).exists
  obtain ⟨H', hH', heq⟩ := (hHn n).exists_eq_measurable_comp
  let H₀ : Z n → Fin m → ℂ := fun z => if ‖H' z‖ ≤ 2*C then H' z else 0
  have hH₀ : Measurable H₀ := hH'.piecewise (measurableSet_le hH'.norm measurable_const) measurable_const
  have hB₀ (z : Z n) : ‖H₀ z‖ ≤ 2*C := by
    by_cases hz : ‖H' z‖ ≤ 2*C
    · simpa only [H₀, ite_eq_left hz] using hz
    · simp only [H₀, ite_eq_right hz, norm_zero]; positivity
  have heq₀ (y : Y) : H₀ (p n y) = Hn n y := by
    have hy := congrFun heq y
    simp only [Function.comp_apply] at hy
    have hb : ‖H' (p n y)‖ ≤ 2*C := hy ▸ hBn n y
    simpa only [H₀, ite_eq_left hb] using hy.symm
  refine ⟨n, H₀, hH₀, hB₀, ?_, ?_⟩
  · simpa only [heq₀] using hint n
  · simpa only [heq₀] using hn

end EuclideanFiveColor.LimitDensity

namespace PlaneFiveColor.Spectral

section
open MeasureTheory ProbabilityTheory EuclideanFiveColor
open scoped BigOperators ENNReal
variable {X Y W : Type*} [MeasurableSpace X] [MeasurableSpace Y] [MeasurableSpace W]
  [MulAction K X] [MulAction K Y]
  [MeasurableConstSMul K X] [MeasurableConstSMul K Y]


lemma finite_encoding_at_of_approximation
    (μ : Measure X) [IsProbabilityMeasure μ] [SMulInvariantMeasure K X μ]
    (p : X → Y) (q : Y → W) (b : X → D)
    (hp : Measurable p) (hb : Measurable b)
    (hpe : ∀ k : K, ∀ᵐ x ∂μ, p (k • x) = k • p x)
    (hbe : ∀ k : K, ∀ᵐ x ∂μ, b (k • x) = k • b x)
    (m : ℕ) (H : Y → Fin m → ℂ)
    (hHeq : H =ᵐ[μ.map p] PhaseEncoding.kernelEncoding (condDistrib b p μ) (fun d => (eval 1 d : ℂ)) m)
    (γ : ℝ) (ha : CompactApproximation.At (K := K) (μ.map p) q m H γ) :
    FiniteEncodingApproximationAt μ p q b m γ := by
  classical
  let : IsProbabilityMeasure (μ.map p) := inferInstance
  obtain ⟨r, B, C, Hf, hB, hC, _hHm, hHf, ha⟩ := ha
  refine ⟨r, B, C, Hf, hB, hC, hHf, ?_⟩
  intro k
  obtain ⟨a, _ham, hab, hai, hae⟩ := ha k
  have hker := KernelSupport.condDistrib_equivariant μ b p hb hp
    (MeasurableEquiv.smul k) (MeasurableEquiv.smul k) (fun d : D => k • d)
    (measurable_const_smul k) (measurePreserving_smul k μ) (hpe k) (hbe k)
  have hcov := PhaseEncoding.kernelEncoding_covariance (μ.map p) (condDistrib b p μ)
    (fun y : Y => k • y) (fun d : D => k • d) (measurable_const_smul k)
    (fun d => (eval 1 d : ℂ)) (measurable_eval_coe 1) m hker
  have heq : ∀ᵐ y ∂μ.map p, H (k • y) =
      PhaseEncoding.kernelEncoding (condDistrib b p μ) (fun d => (eval (kCoeff k) d : ℂ)) m y := by
    filter_upwards [(KernelSupport.factor_smul_preserving μ p hp hpe k).quasiMeasurePreserving.ae hHeq,
      hcov] with y hy hc'
    exact hy.trans (by simpa only [Function.comp_def, eval_smul_one] using hc')
  have he : (fun y => dist (H (k • y)) (∑ i, a (q y) i • Hf i y)^2) =ᵐ[μ.map p]
      (fun y => dist (PhaseEncoding.kernelEncoding (condDistrib b p μ)
        (fun d => (eval (kCoeff k) d : ℂ)) m y) (∑ i, a (q y) i • Hf i y)^2) := by
    filter_upwards [heq] with y hy
    rw [hy]
  have hai' := hai.congr he
  refine ⟨a, hab, hai'.comp_measurable hp, ?_⟩
  rw [← integral_map hp.aemeasurable hai'.aestronglyMeasurable,
    ← integral_congr_ae he]
  exact hae

end

open MeasureTheory ProbabilityTheory EuclideanFiveColor
open scoped BigOperators ENNReal
variable {X Y : Type*} [MeasurableSpace X] [MeasurableSpace Y]
  [StandardBorelSpace X] [Nonempty X] [StandardBorelSpace Y] [Nonempty Y]
  [MulAction K X] [MulAction K Y]
  [MeasurableConstSMul K X] [MeasurableConstSMul K Y]

/-- The source limit implication: a generated increasing sequence of earlier
compact successor factors supplies the requisite single approximation precision.
The induction hypothesis is universal in the recentered wild map. -/
theorem relative_singularity_limit
    {Z W : ℕ → Type*} [∀ n, MeasurableSpace (Z n)] [∀ n, MeasurableSpace (W n)]
    [∀ n, StandardBorelSpace (W n)] [∀ n, Nonempty (W n)]
    [∀ n, MulAction K (Z n)] [∀ n, MulAction K (W n)]
    [∀ n, MeasurableConstSMul K (Z n)] [∀ n, MeasurableConstSMul K (W n)]
    (μ : Measure X) [IsProbabilityMeasure μ] [ErgodicSMul K X μ]
    (d : X → D) (p : X → Y) (v : ∀ n, Y → Z n) (q : ∀ n, Z n → W n)
    (hd : Measurable d) (hp : Measurable p)
    (hv : ∀ n, Measurable (v n)) (hq : ∀ n, Measurable (q n))
    (hde : ∀ k : K, ∀ᵐ x ∂μ, d (k • x) = k • d x)
    (hpe : ∀ k : K, ∀ᵐ x ∂μ, p (k • x) = k • p x)
    (hve : ∀ n, ∀ k : K, ∀ᵐ y ∂μ.map p, v n (k • y) = k • v n y)
    (hqe : ∀ n, ∀ k : K, ∀ᵐ z ∂(μ.map p).map (v n), q n (k • z) = k • q n z)
    (hmono : Monotone (fun n => (inferInstance : MeasurableSpace (Z n)).comap (v n)))
    (hgen : (⨆ n, (inferInstance : MeasurableSpace (Z n)).comap (v n)) = (inferInstance : MeasurableSpace Y))
    (hwild : IsWild (μ.map d))
    (hc : ∀ n, CompactApproximation.Scalar (K := K) ((μ.map p).map (v n)) (q n))
    (hprev : ∀ n, ∀ b : X → D, Measurable b →
      (∀ k : K, ∀ᵐ x ∂μ, b (k • x) = k • b x) → IsWild (μ.map b) →
      DifferenceFourier.differenceLaw (μ.map ((q n ∘ v n) ∘ p))
        (condDistrib b ((q n ∘ v n) ∘ p) μ) C = 0) :
    DifferenceFourier.differenceLaw (μ.map p) (condDistrib d p μ) C = 0 := by
  classical
  let : IsProbabilityMeasure (μ.map p) := inferInstance
  by_contra hn
  have hpos : 0 < RelativeCenters.differenceLaw (μ.map p) (condDistrib d p μ) C :=
    pos_iff_ne_zero.mpr hn
  obtain ⟨b, hb, hbe, hbw, a, ha, hf⟩ := exact_finite_center_reduction μ d p hd hp hde hpe hwild hpos
  obtain ⟨m, hm, g, hg⟩ := UniformEnumeration.constant_uniform_lists (μ.map p)
    (condDistrib b p μ) a ha (hf.mono fun y ⟨S, hS, hSa, hSupp, hcS, _⟩ =>
      ⟨S, hS, hSa, hSupp, hcS⟩)
  obtain ⟨ρ, c, N, hρ, hc', hN, harc⟩ := SmallArc.exists_small_arc_constants m hm
  let γ : ℝ := ((ρ^m/(m : ℝ))/100)/100
  have hγ : 0 < γ := by dsimp [γ]; positivity
  obtain ⟨H, hH, ⟨A, hA, hHB⟩, hHeq⟩ := bounded_phase_encoding μ p b m hm g hg
  obtain ⟨n, H₀, hH₀, hH₀B, hi, he⟩ := LimitDensity.generated_factor_approximation
    (μ.map p) v hv hmono hgen m H hH A hA hHB (γ/2) (by positivity)
  let : IsProbabilityMeasure ((μ.map p).map (v n)) := inferInstance
  have hvector := CompactApproximation.vector_of_scalar ((μ.map p).map (v n)) (q n) (hq n) (hc n)
  have happ := CompactApproximation.lift_at (μ.map p) (v n) (q n) (hv n) (hq n)
    (KernelSupport.factor_smul_preserving μ p hp hpe) (hve n) m H H₀ hH hH₀
    ⟨2*A, hH₀B⟩ γ hγ hi he hvector
  have henc := finite_encoding_at_of_approximation μ p (q n ∘ v n) b hp hb hpe hbe m H hHeq γ happ
  have heqv (k : K) : ∀ᵐ x ∂μ, ((q n ∘ v n) ∘ p) (k • x) = k • ((q n ∘ v n) ∘ p) x := by
    have hqp : ∀ᵐ y ∂μ.map p, q n (v n (k • y)) = k • q n (v n y) := by
      filter_upwards [hve n k, ae_of_ae_map (hv n).aemeasurable (hqe n k)] with y hy hz
      rw [hy, hz]
    filter_upwards [hpe k, ae_of_ae_map hp.aemeasurable hqp] with x hx hy
    simp only [Function.comp_def, hx, hy]
  have hpwild : IsWild (DifferenceFourier.differenceLaw (μ.map ((q n ∘ v n) ∘ p))
      (condDistrib b ((q n ∘ v n) ∘ p) μ)) :=
    ⟨relative_difference_invariant μ b ((q n ∘ v n) ∘ p) hb ((hq n).comp ((hv n).comp hp)) hbe heqv,
      hprev n b hb hbe hbw⟩
  exact finite_uniform_precision_contradiction μ p (q n ∘ v n) b hp ((hq n).comp (hv n)) hb m hm g hg
    hpwild ρ c N hρ hc' hN harc henc

end PlaneFiveColor.Spectral

namespace EuclideanFiveColor.ConditionalBase
open MeasureTheory ProbabilityTheory
variable {X Y G : Type*} [MeasurableSpace X] [MeasurableSpace Y]
  [MeasurableSpace G] [StandardBorelSpace G] [Nonempty G]

end EuclideanFiveColor.ConditionalBase



end

end OAI
