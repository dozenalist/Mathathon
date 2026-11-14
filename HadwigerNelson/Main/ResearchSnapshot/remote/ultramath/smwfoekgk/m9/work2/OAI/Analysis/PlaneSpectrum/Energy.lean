import OAI.Analysis.PlaneSpectrum.Representations

namespace OAI

noncomputable section

section
open scoped BoundedContinuousFunction
open Filter Topology
namespace EuclideanFiveColor.MovingMean

section
open PlaneFiveColor.InvariantMean
variable {G : Type*} [AddCommGroup G] [TopologicalSpace G] [DiscreteTopology G]
/-- Both consumers (`RadialEnergy` and `Ergodicity`) use only the
`Amenable.Mean` fields, so the multiplicity-preserving cube average of this file is
not needed here: the invariant mean of `PlaneFiveColor.InvariantMean` supplies them. -/
def toMean (_ : Finset G × ℕ → G) : Amenable.Mean G where
  map := meanCLM
  map_const := mean_const
  positive := mean_nonneg
  invariant g f := mean_shift g f
end

open PlaneFiveColor.InvariantMean
variable {G : Type*} [AddCommGroup G] [TopologicalSpace G] [DiscreteTopology G]
local instance : DecidableEq G := Classical.decEq _
def cubeSupport : List G → ℕ → Finset G
  | [], _ => {0}
  | g::L, n => (Finset.range (n+1)).biUnion (fun k => (cubeSupport L n).image (fun h => k • g+h))
lemma cube_le_of_support (L : List G) (n : ℕ) (f : G →ᵇ ℝ) (v : G) (c : ℝ)
    (hf : ∀ h ∈ cubeSupport L n, f (v+h) ≤ c) : cube L n f v ≤ c := by
  induction L generalizing v with
  | nil => simpa [cubeSupport, cube] using hf 0 (by simp [cubeSupport])
  | cons g L ih =>
    rw [cube, single_apply]
    have hb : ∑ k ∈ Finset.range (n+1), cube L n f (v+k • g) ≤ (n+1 : ℕ) * c := by
      calc
        _ ≤ ∑ _k ∈ Finset.range (n+1), c := Finset.sum_le_sum fun k hk =>
          ih _ (by
            intro h hh
            have hm : k • g+h ∈ cubeSupport (g::L) n := by
              apply Finset.mem_biUnion.mpr
              exact ⟨k, hk, Finset.mem_image.mpr ⟨h,hh,rfl⟩⟩
            simpa only [add_assoc] using hf _ hm)
        _ = _ := by simp
    calc
      _ ≤ ((n+1 : ℕ) : ℝ)⁻¹ * ((n+1 : ℕ) * c) := mul_le_mul_of_nonneg_left hb (by positivity)
      _ = c := by rw [← mul_assoc, inv_mul_cancel₀ (by positivity), one_mul]

/-- If every invariant mean gives a bounded function a value above c, its
strict c-superlevel set has finitely many translates covering the group. -/
lemma syndetic_of_all_means (f : G →ᵇ ℝ) (c : ℝ)
    (hf : ∀ M : Amenable.Mean G, c < M.map f) :
    ∃ S : Finset G, ∀ v : G, ∃ s ∈ S, c < f (v+s) := by
  classical
  by_contra hn
  push Not at hn
  choose b hb using (fun i : Finset G × ℕ => hn (cubeSupport i.1.toList i.2))
  have hle : meanAt b f ≤ c := by
    apply le_of_tendsto (tendsto_approx b f)
    apply Filter.Eventually.of_forall
    intro i
    exact cube_le_of_support _ _ _ _ _ (hb i)
  exact (not_lt_of_ge hle) (hf (toMean b))
end EuclideanFiveColor.MovingMean
end

section
open MeasureTheory Filter
open scoped ENNReal NNReal BoundedContinuousFunction RealInnerProductSpace
namespace EuclideanFiveColor.BoundedMeasurable

section
variable {G X : Type*} [AddCommGroup G] [TopologicalSpace G] [DiscreteTopology G] [MeasurableSpace X]
variable (μ : Measure X) [IsProbabilityMeasure μ]
namespace Family
def energy (F : Family G X) : G →ᵇ ℝ := Amenable.Mean.squareNorm (toL2 μ F)
omit [AddCommGroup G] in
@[simp] lemma energy_apply (F : Family G X) (g : G) : energy μ F g = ‖l2 μ (F g)‖^2 :=
  Amenable.Mean.squareNorm_apply _ _
lemma energy_mean_eq_of_meanNorm_zero (M : Amenable.Mean G) (F H : Family G X)
    (he : meanNorm μ M (F-H) = 0) : M.map (energy μ F) = M.map (energy μ H) := by
  have hb : |M.map (energy μ F - energy μ H)| ≤
      M.map (((bound F : ℝ)+(bound H : ℝ)) • Amenable.Mean.normFn (toL2 μ (F-H))) := by
    apply M.abs_le
    intro g
    simp only [BoundedContinuousFunction.sub_apply, energy_apply,
      BoundedContinuousFunction.smul_apply, Amenable.Mean.normFn_apply, toL2_apply,
      sub_apply, smul_eq_mul]
    rw [map_sub]
    have hn := abs_norm_sub_norm_le (l2 μ (F g)) (l2 μ (H g))
    have hF := l2_norm_le μ (F g) (F.norm_le_bound g)
    have hH := l2_norm_le μ (H g) (H.norm_le_bound g)
    calc
      _ = |‖l2 μ (F g)‖-‖l2 μ (H g)‖| * (‖l2 μ (F g)‖+‖l2 μ (H g)‖) := by
        have heq : ‖l2 μ (F g)‖^2 - ‖l2 μ (H g)‖^2 =
            (‖l2 μ (F g)‖-‖l2 μ (H g)‖) * (‖l2 μ (F g)‖+‖l2 μ (H g)‖) := by ring
        rw [heq, abs_mul, abs_of_nonneg (add_nonneg (norm_nonneg _) (norm_nonneg _))]
      _ ≤ ‖l2 μ (F g)-l2 μ (H g)‖ * ((bound F : ℝ)+bound H) :=
        mul_le_mul hn (add_le_add hF hH) (add_nonneg (norm_nonneg _) (norm_nonneg _)) (norm_nonneg _)
      _ = _ := mul_comm _ _
  rw [map_sub, map_smul] at hb
  change |M.map (energy μ F) - M.map (energy μ H)| ≤ _ * meanNorm μ M (F-H) at hb
  rw [he, mul_zero] at hb
  exact sub_eq_zero.mp (abs_eq_zero.mp (le_antisymm hb (abs_nonneg _)))
lemma avg_const (M : Amenable.Mean G) (f : Func X) :
    avg μ M (const (G := G) f) = l2 μ f := by
  apply ext_inner_right ℝ
  intro v
  rw [avg_pair]
  have he : Amenable.Mean.pairing (toL2 μ (const (G := G) f)) v =
      BoundedContinuousFunction.const G (inner ℝ (l2 μ f) v) := rfl
  rw [he, M.map_const]
end Family

def normSquare (f : Func X) : Func X := f * bmConj f
@[simp] lemma normSquare_apply (f : Func X) (x : X) : normSquare f x = (‖f x‖^2 : ℝ) := by
  change f x * star (f x) = _
  rw [← starRingEnd_apply, Complex.mul_conj, Complex.normSq_eq_norm_sq]
lemma integral_normSquare (f : Func X) : ∫ x, normSquare f x ∂μ = (‖l2 μ f‖^2 : ℝ) := by
  simp only [normSquare_apply, norm_l2_sq, integral_complex_ofReal]
lemma inner_normSquare (f h : Func X) :
    inner ℝ (l2 μ (normSquare f)) (l2 μ (normSquare h)) = ‖l2 μ (f*h)‖^2 := by
  rw [inner_l2, norm_l2_sq]
  apply integral_congr_ae
  exact .of_forall fun x => by
    simp only [normSquare_apply, Complex.inner, Complex.conj_ofReal, ← Complex.ofReal_mul, Complex.ofReal_re,
      mul_apply, norm_mul]
    ring

variable [AddAction G X] [MeasurableConstVAdd G X] [ErgodicVAdd G X μ]
lemma avg_orbit_const (M : Amenable.Mean G) (φ : G →+ G) (hs : Function.Surjective φ) (f : Func X) :
    Family.avg μ M (Family.orbit φ f) = l2 μ (algebraMap ℂ (Func X) (∫ x, f x ∂μ)) := by
  let c : Func X := algebraMap ℂ (Func X) (∫ x, f x ∂μ)
  have hc : ∫ x, l2 μ (f-c) x ∂μ = 0 := by
    rw [integral_l2]
    change ∫ x, f x-c x ∂μ = 0
    rw [integral_sub (integrable μ f) (integrable μ c)]
    change (∫ x, f x ∂μ) - (∫ _x : X, (∫ x, f x ∂μ) ∂μ) = 0
    simp
  have hv := Amenable.Koopman.vector_orbit_hom_zero μ M φ hs (l2 μ (f-c)) hc
  have he : Family.avg μ M (Family.orbit φ (f-c)) =
      M.vector (Amenable.Mean.orbit (fun g => Amenable.Koopman.action μ (φ g)) (l2 μ (f-c))) := by
    congr 1
  rw [← he] at hv
  have ho : Family.orbit φ (f-c) = Family.orbit φ f - Family.const c := by
    ext g x
    rfl
  rw [ho, (Family.avg μ M).map_sub, Family.avg_const] at hv
  exact sub_eq_zero.mp hv

lemma pair_energy_mean (M : Amenable.Mean G) (φ : G →+ G) (hs : Function.Surjective φ) (f h : Func X) :
    M.map (Family.energy μ (Family.const f * Family.orbit φ h)) = ‖l2 μ f‖^2 * ‖l2 μ h‖^2 := by
  have he : Family.energy μ (Family.const f * Family.orbit φ h) =
      Amenable.Mean.pairing (Family.toL2 μ (Family.orbit φ (normSquare h))) (l2 μ (normSquare f)) := by
    ext g
    rw [Family.energy_apply, Amenable.Mean.pairing_apply, Family.toL2_apply]
    change ‖l2 μ (f*act (φ g) h)‖^2 = inner ℝ (l2 μ (act (φ g) (normSquare h))) (l2 μ (normSquare f))
    rw [real_inner_comm]
    exact (inner_normSquare μ f (act (φ g) h)).symm
  rw [he, ← Family.avg_pair, avg_orbit_const μ M φ hs]
  rw [integral_normSquare]
  rw [inner_l2]
  calc
    _ = ∫ x, ‖l2 μ h‖^2 * ‖f x‖^2 ∂μ := by
      apply integral_congr_ae
      exact .of_forall fun x => by
        change inner ℝ ((‖l2 μ h‖^2 : ℝ) : ℂ) (normSquare f x) = _
        rw [normSquare_apply]
        simp only [Complex.inner, Complex.conj_ofReal, ← Complex.ofReal_mul, Complex.ofReal_re]
        ring
    _ = _ := by rw [integral_const_mul, ← norm_l2_sq]; ring
end

variable {G X : Type*} [AddCommGroup G] [TopologicalSpace G] [DiscreteTopology G]
  [MeasurableSpace X] [AddAction G X] [MeasurableConstVAdd G X]
  (μ : Measure X) [IsProbabilityMeasure μ] [VAddInvariantMeasure G X μ]
lemma energy_two_orbits (φ θ : G →+ G) (f h : Func X) :
    Family.energy μ (Family.orbit φ f * Family.orbit θ h) =
      Family.energy μ (Family.const f * Family.orbit (θ-φ) h) := by
  ext g
  rw [Family.energy_apply, Family.energy_apply]
  have he : act (φ g) f * act (θ g) h = act (φ g) (f * act ((θ-φ) g) h) := by
    ext x
    simp only [mul_apply, act_apply, AddMonoidHom.sub_apply, ← add_vadd]
    congr 2
    abel_nf
  change ‖l2 μ (act (φ g) f * act (θ g) h)‖^2 = _
  rw [he, l2_act]
  simp
omit [VAddInvariantMeasure G X μ]
variable [ErgodicVAdd G X μ]
lemma two_orbit_energy_mean (M : Amenable.Mean G) (φ θ : G →+ G)
    (hs : Function.Surjective (θ-φ)) (f h : Func X) :
    M.map (Family.energy μ (Family.orbit φ f * Family.orbit θ h)) = ‖l2 μ f‖^2 * ‖l2 μ h‖^2 := by
  rw [energy_two_orbits]
  exact pair_energy_mean μ M (θ-φ) hs f h
end EuclideanFiveColor.BoundedMeasurable
end

section
open MeasureTheory Filter
namespace EuclideanFiveColor.BoundedMeasurable
variable {G X Y : Type*} [AddCommGroup G] [MeasurableSpace X] [MeasurableSpace Y]
  [AddAction G X] [AddAction G Y] [MeasurableConstVAdd G X] [MeasurableConstVAdd G Y]
variable (μ : Measure X) [IsProbabilityMeasure μ] [ErgodicVAdd G X μ]
  (q : X → Y) (hq : Measurable q)
  (hqcov : ∀ g : G, (fun x => q (g +ᵥ x)) =ᵐ[μ] (fun x => g +ᵥ q x))
omit [IsProbabilityMeasure μ] in
include hq hqcov in
lemma factor_ergodic : ErgodicVAdd G Y (μ.map q) := by
  have hp (g : G) : MeasurePreserving (fun y : Y => g +ᵥ y) (μ.map q) (μ.map q) := by
    refine ⟨measurable_const_vadd _, ?_⟩
    rw [Measure.map_map (measurable_const_vadd _) hq]
    calc
      _ = μ.map (q ∘ (fun x => g +ᵥ x)) := Measure.map_congr (hqcov g).symm
      _ = _ := by rw [← Measure.map_map hq (measurable_const_vadd _), (measurePreserving_vadd g μ).map_eq]
  have : VAddInvariantMeasure G Y (μ.map q) := ⟨fun g s hs => (hp g).measure_preimage hs.nullMeasurableSet⟩
  constructor
  intro s hs hinv
  have hc : EventuallyEmptyOrUniv (q ⁻¹' s) (ae μ) := by
    apply ErgodicVAdd.aeconst_of_forall_preimage_vadd_ae_eq (G := G) (hs.preimage hq)
    intro g
    filter_upwards [ae_of_ae_map hq.aemeasurable (hinv g), hqcov g] with x hx he
    change (q (g +ᵥ x) ∈ s) = (q x ∈ s)
    rw [he]
    exact hx
  rw [eventuallyEmptyOrUniv_iff] at hc ⊢
  rcases hc with hc | hc
  · exact Or.inl ((ae_map_iff hq.aemeasurable hs).mpr hc)
  · exact Or.inr ((ae_map_iff hq.aemeasurable hs.compl).mpr hc)
end EuclideanFiveColor.BoundedMeasurable

open MeasureTheory Filter
open scoped ENNReal NNReal BoundedContinuousFunction RealInnerProductSpace
namespace EuclideanFiveColor.BoundedMeasurable
variable {G X Y : Type*} [AddCommGroup G] [TopologicalSpace G] [DiscreteTopology G]
  [MeasurableSpace X] [MeasurableSpace Y] [StandardBorelSpace X] [Nonempty X]
  [StandardBorelSpace Y] [Nonempty Y]
  [AddAction G X] [AddAction G Y] [MeasurableConstVAdd G X] [MeasurableConstVAdd G Y]
  (μ : Measure X) [IsProbabilityMeasure μ] [ErgodicVAdd G X μ]
  (q : X → Y) (hq : Measurable q)
  (hqcov : ∀ g : G, (fun x => q (g +ᵥ x)) =ᵐ[μ] (fun x => g +ᵥ q x))
variable [IsProbabilityMeasure (μ.map q)]
variable [ErgodicVAdd G (X×X) (RelativeProduct.law μ q hq)]
include hq hqcov in
lemma conditional_pair_energy (M : Amenable.Mean G) (φ : G →+ G)
    (hs : Function.Surjective φ) (f h : Func X) :
    M.map (Family.energy (μ.map q) (Family.conditional μ q (Family.const f * Family.orbit φ h))) =
      ‖l2 (μ.map q) (conditional μ q f)‖^2 * ‖l2 (μ.map q) (conditional μ q h)‖^2 := by
  have : ErgodicVAdd G Y (μ.map q) := factor_ergodic μ q hq hqcov
  have hp := pairVanishing_of_ergodic μ q hq M
  have he := covariance_mean_zero μ q hq hqcov M hp φ hs f h
  have hv := Family.energy_mean_eq_of_meanNorm_zero (μ.map q) M _ _ he
  rw [hv]
  exact pair_energy_mean (μ.map q) M φ hs (conditional μ q f) (conditional μ q h)
include hq hqcov in
lemma conditional_integer_pair_energy
    (hdiv : ∀ n : ℤ, n ≠ 0 → Function.Surjective (scaleHom (G := G) n))
    (M : Amenable.Mean G) {n m : ℤ} (hnm : n ≠ m) (f h : Func X) :
    M.map (Family.energy (μ.map q) (Family.conditional μ q
      (Family.orbit (scaleHom n) f * Family.orbit (scaleHom m) h))) =
      ‖l2 (μ.map q) (conditional μ q f)‖^2 * ‖l2 (μ.map q) (conditional μ q h)‖^2 := by
  have : ErgodicVAdd G Y (μ.map q) := factor_ergodic μ q hq hqcov
  have hp := pairVanishing_of_ergodic μ q hq M
  have hn : Set.InjOn (![n,m]) (Finset.univ : Finset (Fin 2)) := by
    intro i _ j _ he
    fin_cases i <;> fin_cases j <;> simp_all
  have he := conditional_integer_multiple_mean_zero μ q hq hqcov hdiv M hp
    Finset.univ ![n,m] ![f,h] hn
  simp only [Fin.prod_univ_two, Matrix.cons_val_zero, Matrix.cons_val_one] at he
  rw [Family.energy_mean_eq_of_meanNorm_zero (μ.map q) M _ _ he]
  apply two_orbit_energy_mean
  rw [← scaleHom_sub]
  exact hdiv _ (sub_ne_zero.mpr hnm.symm)
include hq hqcov in
lemma conditional_integer_triple_energy
    (hdiv : ∀ n : ℤ, n ≠ 0 → Function.Surjective (scaleHom (G := G) n))
    (M : Amenable.Mean G) (f h k : Func X) :
    M.map (Family.energy (μ.map q) (Family.conditional μ q
      (Family.orbit (scaleHom 0) f * Family.orbit (scaleHom 1) h * Family.orbit (scaleHom 2) k))) =
    M.map (Family.energy (μ.map q)
      (Family.orbit (scaleHom 0) (conditional μ q f) * Family.orbit (scaleHom 1) (conditional μ q h) *
        Family.orbit (scaleHom 2) (conditional μ q k))) := by
  have hp := pairVanishing_of_ergodic μ q hq M
  have hn : Set.InjOn (![(0:ℤ),1,2]) (Finset.univ : Finset (Fin 3)) := by
    intro i _ j _ he
    fin_cases i <;> fin_cases j <;> simp_all
  have he := conditional_integer_multiple_mean_zero μ q hq hqcov hdiv M hp
    Finset.univ ![(0:ℤ),1,2] ![f,h,k] hn
  simp only [Fin.prod_univ_three, Matrix.cons_val_zero, Matrix.cons_val_one,
    Matrix.cons_val_two] at he
  exact Family.energy_mean_eq_of_meanNorm_zero (μ.map q) M _ _ he
end EuclideanFiveColor.BoundedMeasurable
end

open MeasureTheory ProbabilityTheory Filter EuclideanFiveColor
open scoped ENNReal NNReal ComplexConjugate
namespace PlaneFiveColor.Spectral
open EuclideanFiveColor.BoundedMeasurable

/-- The exact evaluation character, as a bounded measurable function. -/
def char (z : E) : Func D := ⟨fun d => (eval z d : ℂ), measurable_eval_coe z,
  1, fun d => by simp only [Circle.norm_coe, NNReal.coe_one, le_refl]⟩
@[simp] lemma char_apply (z : E) (d : D) : char z d = (eval z d : ℂ) := rfl
@[simp] lemma norm_char (z : E) (d : D) : ‖char z d‖ = 1 := Circle.norm_coe _
@[simp] lemma char_zero : char 0 = 1 := by ext d; simp
lemma char_add (z w : E) : char (z+w) = char z * char w := by
  ext d
  exact congrArg (fun a : Circle => (a : ℂ)) (eval_add z w d)
lemma char_act (g : Rot) (z : E) : act g (char z) = char (kCoeff (rotMul g)*z) := rfl

variable {Y : Type*} [MeasurableSpace Y]
variable (μ : Measure D) [IsProbabilityMeasure μ] (q : D → Y)
def projectedMass (z : E) : ℝ := ‖l2 (μ.map q) (conditional μ q (char z))‖^2
lemma projectedMass_nonneg (z : E) : 0 ≤ projectedMass μ q z := sq_nonneg _
lemma projected_char_bound (z : E) (y : Y) : ‖conditional μ q (char z) y‖ ≤ 1 :=
  expect_bound _ _ (fun d => le_of_eq (norm_char _ d)) y
variable (hq : Measurable q)
include hq in
lemma projectedMass_le_one (z : E) : projectedMass μ q z ≤ 1 := by
  let : IsProbabilityMeasure (μ.map q) :=
    (Measure.isProbabilityMeasure_map_iff hq.aemeasurable).mpr inferInstance
  have hn := l2_norm_le (μ.map q) (conditional μ q (char z)) (projected_char_bound μ q z)
  unfold projectedMass
  nlinarith [norm_nonneg (l2 (μ.map q) (conditional μ q (char z)))]
include hq in
lemma projectedMass_zero : projectedMass μ q 0 = 1 := by
  let : IsProbabilityMeasure (μ.map q) :=
    (Measure.isProbabilityMeasure_map_iff hq.aemeasurable).mpr inferInstance
  have he : conditional μ q (char 0) = 1 := by
    ext y
    change (∫ d, char 0 d ∂condDistrib id q μ y) = 1
    simp
  unfold projectedMass
  rw [he, norm_l2_sq]
  simp
include hq in
lemma differenceFourier_projectedMass (z : E) :
    ∫ d, (eval z d : ℂ) ∂DifferenceFourier.differenceLaw (μ.map q) (condDistrib id q μ) =
      (projectedMass μ q z : ℂ) := by
  let : IsProbabilityMeasure (μ.map q) :=
    (Measure.isProbabilityMeasure_map_iff hq.aemeasurable).mpr inferInstance
  rw [DifferenceFourier.difference_coefficient (eval z) (measurable_eval_coe z)]
  congr 1
  exact (norm_l2_sq (μ.map q) (conditional μ q (char z))).symm

variable [MulAction K Y] [MeasurableConstSMul K Y] [SMulInvariantMeasure K D μ]
variable (hqcov : ∀ k : K, ∀ᵐ d ∂μ, q (k • d) = k • q d)
include hq hqcov in
lemma projectedMass_rotation (u : K) (z : E) :
    projectedMass μ q (kCoeff u*z) = projectedMass μ q z := by
  let : IsProbabilityMeasure (μ.map q) :=
    (Measure.isProbabilityMeasure_map_iff hq.aemeasurable).mpr inferInstance
  unfold projectedMass
  rw [← norm_project_l2 μ q hq, ← norm_project_l2 μ q hq]
  have hchar : char (kCoeff u*z) = act (mulRot u) (char z) := rfl
  rw [hchar]
  have he := (l2_eq_iff μ _ _).mpr (project_act μ q hq (fun g : Rot => hqcov (rotMul g)) (mulRot u) (char z))
  rw [he, l2_act]
  simp
include hq hqcov in
lemma projectedMass_radial {z w : E} (hn : ‖(z : ℂ)‖ = ‖(w : ℂ)‖) :
    projectedMass μ q z = projectedMass μ q w := by
  by_cases hw : w = 0
  · have hz : z = 0 := by
      apply Subtype.ext
      apply norm_eq_zero.mp
      simpa [hw] using hn
    rw [hz, hw]
  have hwc : (w : ℂ) ≠ 0 := fun h => hw (Subtype.ext h)
  let c : Circle := ⟨(z : ℂ)/(w : ℂ), mem_sphere_zero_iff_norm.mpr (by
    rw [norm_div, hn, div_self (norm_ne_zero_iff.mpr hwc)])⟩
  let u : K := ⟨c, mem_algebraicClosure_iff.mp (div_mem z.property w.property)⟩
  have he : kCoeff u * w = z := by
    apply Subtype.ext
    exact div_mul_cancel₀ _ hwc
  rw [← he]
  exact projectedMass_rotation μ q hq hqcov u w
end PlaneFiveColor.Spectral

end

end OAI
