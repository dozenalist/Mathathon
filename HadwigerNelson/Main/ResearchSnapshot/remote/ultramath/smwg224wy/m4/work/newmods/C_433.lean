import B
import OAI.Analysis.PlaneSpectrum.Ergodicity

/-!
# Theorem A: relative singularity at a factor with ergodic relative product.

Against the `OAI` development: `D`, `C`, `j` from
`OAI/Analysis/PlaneSpectrum/Basic.lean`; `differenceLaw` from
`OAI/Analysis/PlaneSpectrum/FourierTests.lean`; `RelativeProduct.law` from
`OAI/MeasureTheory/CompactFactors/Kernels.lean`.
-/

namespace OAI
noncomputable section
open MeasureTheory ProbabilityTheory Filter
open scoped ENNReal NNReal Topology

namespace PlaneFiveColor.Spectral
namespace RelativeSingularity

/-! ## Auxiliary facts about `j`, `C` and the `K`-action on `D`. -/

theorem C_eq_range : (C : Set D) = Set.range j := by
  ext w
  constructor
  · intro hw
    obtain ⟨x, hx⟩ := hw
    exact ⟨Multiplicative.toAdd x, hx⟩
  · rintro ⟨ξ, rfl⟩
    exact ⟨Multiplicative.ofAdd ξ, rfl⟩

theorem image_closedBall_measurable (t : ℝ) :
    MeasurableSet (j '' Metric.closedBall (0:ℂ) t) :=
  (isCompact_closedBall (0:ℂ) t).image continuous_j |>.measurableSet

theorem image_closedBall_zero : j '' Metric.closedBall (0:ℂ) 0 = ({1} : Set D) := by
  rw [Metric.closedBall_zero, Set.image_singleton, j_zero]

theorem C_eq_iUnion : (C : Set D) = ⋃ n : ℕ, j '' Metric.closedBall (0:ℂ) (n : ℝ) := by
  rw [C_eq_range]
  ext w
  constructor
  · rintro ⟨ξ, rfl⟩
    obtain ⟨n, hn⟩ := exists_nat_ge ‖ξ‖
    refine Set.mem_iUnion.mpr ⟨n, ξ, ?_, rfl⟩
    rw [Metric.mem_closedBall, dist_zero_right]
    exact hn
  · intro hw
    obtain ⟨n, ξ, -, rfl⟩ := Set.mem_iUnion.mp hw
    exact ⟨ξ, rfl⟩

theorem kCoeff_norm (k : K) : ‖(((kCoeff k : E)) : ℂ)‖ = 1 := by
  have h : ((kCoeff k : E) : ℂ) = ((k : Circle) : ℂ) := rfl
  rw [h]
  exact Circle.norm_coe (k : Circle)

theorem scalar_div (a : E) (p q : D) : scalar a (p / q) = scalar a p / scalar a q :=
  map_div (scalarHom a) p q

/-! ## The kernel bridge -/

variable {X Y : Type*} [MeasurableSpace X] [MeasurableSpace Y]
  [StandardBorelSpace X] [Nonempty X] [StandardBorelSpace Y] [Nonempty Y]

theorem differenceLaw_eq_law (μ : Measure X) [IsProbabilityMeasure μ]
    (q : X → Y) (hq : Measurable q) (d : X → D) (hd : Measurable d) :
    EuclideanFiveColor.DifferenceFourier.differenceLaw (μ.map q) (condDistrib d q μ)
      = (EuclideanFiveColor.RelativeProduct.law μ q hq).map
          (fun z : X × X => d z.1 / d z.2) := by
  classical
  have hdm : Measurable (fun z : X × X => (d z.1, d z.2)) :=
    (hd.comp measurable_fst).prodMk (hd.comp measurable_snd)
  have hdivm : Measurable (fun p : D × D => p.1 / p.2) :=
    measurable_fst.div measurable_snd
  have hratm : Measurable (fun z : X × X => d z.1 / d z.2) :=
    (hd.comp measurable_fst).div (hd.comp measurable_snd)
  set ν : Measure Y := μ.map q with hν
  set κ : Kernel Y X := condDistrib id q μ with hκ
  haveI hνp : IsProbabilityMeasure ν := by
    rw [hν]; exact Measure.isProbabilityMeasure_map hq.aemeasurable
  haveI hκmk : IsMarkovKernel κ := by rw [hκ]; infer_instance
  have hκd : ∀ᵐ y ∂ν, condDistrib d q μ y = (κ y).map d := by
    have h : condDistrib (d ∘ (id : X → X)) q μ =ᵐ[μ.map q]
        (condDistrib (id : X → X) q μ).map d :=
      condDistrib_comp (X := q) (Y := (id : X → X)) (f := d) aemeasurable_id hd
    filter_upwards [h] with y hy
    rw [Kernel.map_apply (condDistrib id q μ) hd y] at hy
    simpa [hκ, Function.comp_def] using hy
  have hmix : (κ.prod κ) ∘ₘ ν = EuclideanFiveColor.RelativeProduct.law μ q hq := by
    rw [hκ, hν, EuclideanFiveColor.RelativeProduct.law_eq_mixture]
  have hkey : ∀ s : Set (D × D), MeasurableSet s →
      (((condDistrib d q μ).prod (condDistrib d q μ)) ∘ₘ ν) s
        = ((κ.prod κ) ∘ₘ ν) ((fun z : X × X => (d z.1, d z.2)) ⁻¹' s) := by
    intro s hs
    have hpre : MeasurableSet ((fun z : X × X => (d z.1, d z.2)) ⁻¹' s) := hdm hs
    rw [Measure.bind_apply hs (Kernel.measurable _).aemeasurable,
      Measure.bind_apply hpre (Kernel.measurable _).aemeasurable]
    apply lintegral_congr_ae
    filter_upwards [hκd] with y hy
    have h1 : ((condDistrib d q μ).prod (condDistrib d q μ)) y
        = ((κ y).map d).prod ((κ y).map d) := by
      simp only [Kernel.prod_apply]; rw [hy]
    have h3 : (κ.prod κ) y = (κ y).prod (κ y) := by simp only [Kernel.prod_apply]
    rw [h1, h3, Measure.map_prod_map (κ y) (κ y) hd hd,
      Measure.map_apply (hd.prodMap hd) hs]
    rfl
  have hmix' : EuclideanFiveColor.RelativeProduct.law μ q hq = (κ.prod κ) ∘ₘ ν := hmix.symm
  have hA : ∀ s : Set D, (fun z : X × X => (d z.1, d z.2)) ⁻¹'
      ((fun p : D × D => p.1 / p.2) ⁻¹' s) = (fun z : X × X => d z.1 / d z.2) ⁻¹' s := by
    intro s
    ext z
    rfl
  ext s hs
  have hs' : MeasurableSet ((fun p : D × D => p.1 / p.2) ⁻¹' s) := hdivm hs
  rw [EuclideanFiveColor.DifferenceFourier.differenceLaw, Measure.map_apply hdivm hs,
    hkey ((fun p : D × D => p.1 / p.2) ⁻¹' s) hs', hA,
    Measure.map_apply hratm hs, hmix']

/-! ## Theorem A -/

variable [MulAction K X]

/-- **Theorem A** (relative singularity at a factor with ergodic relative product).

`hdiag` is hypothesis (H2) in the sharp form consumed by the `r = 0` branch of the
proof: `d` is not almost surely constant on the relative product. -/
theorem relative_singularity_of_ergodic
    (μ : Measure X) [IsProbabilityMeasure μ]
    (q : X → Y) (hq : Measurable q)
    (d : X → D) (hd : Measurable d)
    (hde : ∀ (k : K) (x : X), d (k • x) = k • d x)
    [ErgodicVAdd Rot (X × X) (EuclideanFiveColor.RelativeProduct.law μ q hq)]
    (hdiag : ¬ ∀ᵐ z ∂(EuclideanFiveColor.RelativeProduct.law μ q hq), d z.1 = d z.2) :
    EuclideanFiveColor.DifferenceFourier.differenceLaw (μ.map q) (condDistrib d q μ) C = 0 := by
  classical
  set ν : Measure Y := μ.map q with hν
  set κ : Kernel Y X := condDistrib id q μ with hκ
  haveI hνp : IsProbabilityMeasure ν := by
    rw [hν]; exact Measure.isProbabilityMeasure_map hq.aemeasurable
  haveI hκmk : IsMarkovKernel κ := by rw [hκ]; infer_instance
  set μR : Measure (X × X) := EuclideanFiveColor.RelativeProduct.law μ q hq with hμR
  have hmix : μR = (κ.prod κ) ∘ₘ ν := by
    rw [hμR, hκ, hν]; exact EuclideanFiveColor.RelativeProduct.law_eq_mixture μ q hq
  haveI hμRp : IsProbabilityMeasure μR := by rw [hmix]; infer_instance
  set ratio : X × X → D := fun z => d z.1 / d z.2 with hratio
  have hratiom : Measurable ratio := (hd.comp measurable_fst).div (hd.comp measurable_snd)
  set A : ℝ → Set (X × X) := fun t => ratio ⁻¹' (j '' Metric.closedBall (0:ℂ) t) with hA
  have hAm : ∀ t, MeasurableSet (A t) := fun t =>
    (image_closedBall_measurable t).preimage hratiom
  have hAmono : ∀ s t : ℝ, s ≤ t → A s ⊆ A t := by
    intro s t hst z hz
    simp only [hA, Set.mem_preimage] at hz ⊢
    obtain ⟨ξ, hξ, hξt⟩ := hz
    exact ⟨ξ, (by rw [Metric.mem_closedBall, dist_zero_right] at hξ ⊢; linarith), hξt⟩
  have hAinv : ∀ (g : Rot) (t : ℝ), A t ⊆ (fun z : X × X => g +ᵥ z) ⁻¹' A t := by
    intro g t z hz
    simp only [hA, Set.mem_preimage] at hz ⊢
    obtain ⟨ξ, hξ, hξt⟩ := hz
    refine ⟨(starRingEnd ℂ) (((kCoeff (rotMul g) : E)) : ℂ) * ξ, ?_, ?_⟩
    · rw [Metric.mem_closedBall, dist_zero_right] at hξ ⊢
      rw [norm_mul, Complex.norm_conj, kCoeff_norm, one_mul]
      exact hξ
    · have hstep : ratio (g +ᵥ z) = scalar (kCoeff (rotMul g)) (ratio z) := by
        have hgz : (g +ᵥ z) = (rotMul g • z.1, rotMul g • z.2) := by rw [rot_vadd, Prod.smul_mk]
        rw [hgz]
        simp only [hratio]
        rw [hde (rotMul g) z.1, hde (rotMul g) z.2]
        exact (scalar_div (kCoeff (rotMul g)) (d z.1) (d z.2)).symm
      rw [hstep, ← hξt, scalar_j]
  have hae_inv : ∀ (g : Rot) (t : ℝ), (fun z : X × X => g +ᵥ z) ⁻¹' A t =ᵐ[μR] A t := by
    intro g t
    have hinv := VAddInvariantMeasure.measure_preimage_vadd (μ := μR) g (hAm t)
    have hsd : μR ((fun z : X × X => g +ᵥ z) ⁻¹' A t \ A t) = 0 := by
      rw [measure_sdiff (hAinv g t) (hAm t).nullMeasurableSet (measure_ne_top μR _), hinv,
        tsub_self]
    have hsub : {z : X × X | ¬ (z ∈ (fun z : X × X => g +ᵥ z) ⁻¹' A t ↔ z ∈ A t)}
        ⊆ ((fun z : X × X => g +ᵥ z) ⁻¹' A t \ A t) := by
      intro z hz
      simp only [Set.mem_setOf_eq, Set.mem_preimage, Set.mem_sdiff] at hz ⊢
      refine ⟨?_, ?_⟩
      · by_contra hcon
        exact hz ⟨fun h1 => absurd h1 hcon, fun h2 => absurd (hAinv g t h2) hcon⟩
      · intro hcon
        exact hz ⟨fun _ => hcon, fun h2 => hAinv g t h2⟩
    have h0 : μR {z : X × X | ¬ (z ∈ (fun z : X × X => g +ᵥ z) ⁻¹' A t ↔ z ∈ A t)} = 0 :=
      measure_mono_null hsub hsd
    have h1 : ∀ᵐ z ∂μR, (z ∈ (fun z : X × X => g +ᵥ z) ⁻¹' A t ↔ z ∈ A t) := ae_iff.mpr h0
    show ∀ᵐ z ∂μR, (z ∈ (fun z : X × X => g +ᵥ z) ⁻¹' A t) = (z ∈ A t)
    filter_upwards [h1] with z hz
    exact propext hz
  have hle1 : ∀ t : ℝ, μR (A t) ≤ 1 := fun t => by
    calc μR (A t) ≤ μR (Set.univ : Set (X × X)) := measure_mono (Set.subset_univ _)
      _ = 1 := measure_univ
  have h01 : ∀ t : ℝ, μR (A t) = 0 ∨ μR (A t) = 1 := by
    intro t
    rcases _root_.RelativeSingularity.measure_eq_zero_or_univ_of_ae_invariant (G := Rot) (μ := μR) (s := A t) (hAm t)
      (fun g => hae_inv g t) with h | h
    · exact Or.inl h
    · exact Or.inr (by rw [h]; exact measure_univ)
  -- the conclusion, by contradiction
  by_contra hnot
  have hpos : 0 < μR (ratio ⁻¹' (C : Set D)) := by
    rw [hμR]
    change 0 < EuclideanFiveColor.RelativeProduct.law μ q hq
      ((fun z : X × X => d z.1 / d z.2) ⁻¹' (C : Set D))
    rw [← Measure.map_apply hratiom measurableSet_C, ← differenceLaw_eq_law μ q hq d hd]
    exact pos_iff_ne_zero.mpr hnot
  have hF_eq : ratio ⁻¹' (C : Set D) = ⋃ n : ℕ, A (n : ℝ) := by
    rw [C_eq_iUnion, Set.preimage_iUnion]
  -- the threshold radius
  set Tset : Set ℝ := {t : ℝ | 0 ≤ t ∧ μR (A t) = 1} with hTset
  have hTne : Tset.Nonempty := by
    by_contra hcon
    rw [Set.not_nonempty_iff_eq_empty] at hcon
    have hall : ∀ n : ℕ, μR (A (n : ℝ)) = 0 := by
      intro n
      rcases h01 (n : ℝ) with h | h
      · exact h
      · exfalso
        have hmem : (n : ℝ) ∈ Tset := ⟨Nat.cast_nonneg n, h⟩
        rw [hcon] at hmem
        exact hmem
    have h0 : μR (⋃ n : ℕ, A (n : ℝ)) = 0 := measure_iUnion_null hall
    rw [← hF_eq] at h0
    exact hpos.ne' h0
  set r : ℝ := sInf Tset with hr
  have hr0 : 0 ≤ r := le_csInf hTne (fun b hb => hb.1)
  have hrd : ∀ t ∈ Tset, r ≤ t := fun t ht =>
    csInf_le (⟨0, fun b hb => hb.1⟩ : BddBelow Tset) ht
  have hbig : ∀ t : ℝ, r < t → μR (A t) = 1 := by
    intro t ht
    have hex : ∃ s ∈ Tset, s < t := by
      by_contra hcon
      push_neg at hcon
      have : t ≤ r := le_csInf hTne (fun b hb => hcon b hb)
      linarith
    obtain ⟨s, hs, hst⟩ := hex
    exact le_antisymm (hle1 t) (by rw [← hs.2]; exact measure_mono (hAmono s t hst.le))
  have hsmall : ∀ t : ℝ, 0 ≤ t → t < r → μR (A t) = 0 := by
    intro t ht0 htr
    rcases h01 t with h | h
    · exact h
    · exact absurd (hrd t ⟨ht0, h⟩) (not_le.mpr htr)
  -- `A r` is conull
  have hAr : μR (A r) = 1 := by
    have hterm : ∀ m : ℕ, μR (A (r + 1/((m:ℝ)+1))) = 1 := fun m => hbig _ (by
      have h : (0:ℝ) < 1/((m:ℝ)+1) := by positivity
      linarith)
    have hnull : ∀ m : ℕ, μR ((A (r + 1/((m:ℝ)+1)))ᶜ) = 0 := by
      intro m
      rw [measure_compl (hAm _) (measure_ne_top μR _), hterm m]
      simp
    have h0 : μR (⋃ m : ℕ, (A (r + 1/((m:ℝ)+1)))ᶜ) = 0 := measure_iUnion_null hnull
    have hsub : (A r)ᶜ ⊆ ⋃ m : ℕ, (A (r + 1/((m:ℝ)+1)))ᶜ := by
      intro z hz
      rw [Set.mem_iUnion]
      simp only [Set.mem_compl_iff]
      by_cases hrng : ∃ ξ : ℂ, j ξ = ratio z
      · obtain ⟨ξ, hξ⟩ := hrng
        have hξgt : r < ‖ξ‖ := by
          by_contra hle
          push_neg at hle
          exact hz (by
            simp only [hA, Set.mem_preimage]
            exact ⟨ξ, by rw [Metric.mem_closedBall, dist_zero_right]; exact hle, hξ⟩)
        have hposd : 0 < ‖ξ‖ - r := by linarith
        obtain ⟨m, hm⟩ := exists_nat_gt (1 / (‖ξ‖ - r))
        refine ⟨m, ?_⟩
        simp only [hA, Set.mem_preimage]
        rintro ⟨ξ', hξ', hξ''⟩
        have hcon : ξ' = ξ := j_injective (hξ''.trans hξ.symm)
        rw [hcon] at hξ'
        rw [Metric.mem_closedBall, dist_zero_right] at hξ'
        rw [div_lt_iff₀ hposd] at hm
        have : 1 / ((m:ℝ) + 1) < ‖ξ‖ - r := by
          rw [div_lt_iff₀ (by positivity : (0:ℝ) < (m:ℝ) + 1)]
          nlinarith
        linarith
      · push_neg at hrng
        exact ⟨0, by
          simp only [hA, Set.mem_preimage]
          rintro ⟨ξ, -, hξ⟩
          exact hrng ξ hξ⟩
    have hc : μR ((A r)ᶜ) = 0 := measure_mono_null hsub h0
    have h2 : μR (A r) + μR ((A r)ᶜ) = μR (Set.univ : Set (X × X)) :=
      measure_add_measure_compl (hAm r)
    rw [hc, add_zero, measure_univ] at h2
    exact h2
  rcases eq_or_lt_of_le hr0 with hzero | hposr
  · -- `r = 0`: the relative product is carried by the diagonal
    apply hdiag
    have hA0 : A 0 = {z : X × X | d z.1 = d z.2} := by
      rw [hA]
      ext z
      simp only [Set.mem_preimage, image_closedBall_zero, Set.mem_singleton_iff,
        Set.mem_setOf_eq, hratio, div_eq_one]
    have hAr0 : μR (A 0) = 1 := by rw [show r = 0 from hzero.symm] at hAr; exact hAr
    rw [ae_iff]
    have hcomp : {z : X × X | ¬ d z.1 = d z.2} = (A 0)ᶜ := by rw [hA0, Set.compl_setOf]
    rw [hcomp, measure_compl (hAm 0) (measure_ne_top μR _), hAr0, measure_univ, tsub_self]
  · -- `r > 0`
    set U : ℕ → Set (X × X) := fun m => A (r - r/((m:ℝ)+1)) with hU
    have hUm : ∀ m, MeasurableSet (U m) := fun m => hAm _
    have hUnull : μR (⋃ m, U m) = 0 := by
      refine measure_iUnion_null (fun m => ?_)
      have hm2 : 0 < r/((m:ℝ)+1) := by positivity
      have hle : r/((m:ℝ)+1) ≤ r := by
        rw [div_le_iff₀ (by positivity : (0:ℝ) < (m:ℝ) + 1)]
        nlinarith
      exact hsmall _ (by linarith) (by linarith)
    have hT : μR (A r \ ⋃ m, U m) = 1 := by rw [measure_sdiff_null hUnull, hAr]
    have hTm : MeasurableSet (A r \ ⋃ m, U m) := (hAm r).diff (MeasurableSet.iUnion hUm)
    have hfib : ∀ᵐ y ∂ν, (κ.prod κ) y ((A r \ ⋃ m, U m)ᶜ) = 0 := by
      have hcomp : μR ((A r \ ⋃ m, U m)ᶜ) = 0 := by
        rw [measure_compl hTm (measure_ne_top μR _), hT, measure_univ, tsub_self]
      rw [hmix, Measure.bind_apply hTm.compl (Kernel.measurable _).aemeasurable] at hcomp
      exact (lintegral_eq_zero_iff (Kernel.measurable_coe _ hTm.compl)).mp hcomp
    obtain ⟨y, hy⟩ : ∃ y, (κ.prod κ) y ((A r \ ⋃ m, U m)ᶜ) = 0 := by
      by_contra hcon
      rw [not_exists] at hcon
      have hsub : (Set.univ : Set Y) ⊆ {y | ¬ ((κ.prod κ) y ((A r \ ⋃ m, U m)ᶜ) = 0)} :=
        fun y _ => by simpa using hcon y
      have h0 : ν (Set.univ : Set Y) = 0 :=
        measure_mono_null hsub (by rwa [ae_iff] at hfib)
      rw [measure_univ] at h0
      exact one_ne_zero h0
    have hy1 : (κ.prod κ) y (A r \ ⋃ m, U m) = 1 := by
      have h2 : (κ.prod κ) y (A r \ ⋃ m, U m) + (κ.prod κ) y ((A r \ ⋃ m, U m)ᶜ)
          = (κ.prod κ) y (Set.univ : Set (X × X)) := measure_add_measure_compl hTm
      rw [hy, add_zero, measure_univ] at h2
      exact h2
    -- push forward to `D`
    set SphD : Set D := j '' Metric.closedBall (0:ℂ) r
      \ ⋃ m : ℕ, j '' Metric.closedBall (0:ℂ) (r - r/((m:ℝ)+1)) with hSphD
    have hSphDm : MeasurableSet SphD := (image_closedBall_measurable r).diff
      (MeasurableSet.iUnion (fun m => image_closedBall_measurable _))
    have hSphDmem : ∀ w : D, w ∈ SphD ↔ ∃ ξ : ℂ, j ξ = w ∧ ‖ξ‖ = r := by
      intro w
      constructor
      · rintro ⟨hm, hn⟩
        simp only [hSphD, Set.mem_sdiff, Set.mem_iUnion] at hm hn
        obtain ⟨ξ, hmem, hjeq⟩ := hm
        refine ⟨ξ, hjeq, ?_⟩
        rw [Metric.mem_closedBall, dist_zero_right] at hmem
        by_contra hne
        have hlt : ‖ξ‖ < r := lt_of_le_of_ne hmem hne
        obtain ⟨m, hm⟩ := exists_nat_gt (r / (r - ‖ξ‖))
        refine absurd ⟨m, ξ, ?_, hjeq⟩ hn
        rw [Metric.mem_closedBall, dist_zero_right]
        rw [div_lt_iff₀ (by linarith : (0:ℝ) < r - ‖ξ‖)] at hm
        have hle : r / ((m:ℝ) + 1) ≤ r - ‖ξ‖ := by
          rw [div_le_iff₀ (by positivity : (0:ℝ) < (m:ℝ) + 1)]
          nlinarith
        linarith
      · rintro ⟨ξ, rfl, hξr⟩
        refine ⟨⟨ξ, ?_, rfl⟩, ?_⟩
        · rw [Metric.mem_closedBall, dist_zero_right]; linarith
        · simp only [Set.mem_iUnion, Set.mem_image, not_exists, not_and]
          intro m ξ' hξ' hcon
          have hcon' : ξ' = ξ := j_injective hcon
          rw [hcon', Metric.mem_closedBall, dist_zero_right] at hξ'
          have hmm : 0 < r/((m:ℝ)+1) := by positivity
          linarith
    have hpre : (A r \ ⋃ m, U m) = ratio ⁻¹' SphD := by
      simp only [hSphD, hU, hA, Set.preimage_sdiff, Set.preimage_iUnion]
    set lam : Measure D := (κ y).map d with hlam
    haveI hlamP : IsProbabilityMeasure lam := by
      rw [hlam]; exact Measure.isProbabilityMeasure_map hd.aemeasurable
    have hmain : lam.prod lam {p : D × D | p.1 / p.2 ∈ SphD} = 1 := by
      have hset : MeasurableSet {p : D × D | p.1 / p.2 ∈ SphD} :=
        hSphDm.preimage (measurable_fst.div measurable_snd)
      have hpre2 : (Prod.map d d) ⁻¹' {p : D × D | p.1 / p.2 ∈ SphD} = (A r \ ⋃ m, U m) := by
        rw [hpre]; rfl
      rw [hlam, Measure.map_prod_map (κ y) (κ y) hd hd, Measure.map_apply (hd.prodMap hd) hset,
        hpre2, ← Kernel.prod_apply]
      exact hy1
    obtain ⟨a, b, c', e, hab, hac, had, hbc, hbd, hcd⟩ :=
      _root_.RelativeSingularity.exists_four_pairwise lam {p : D × D | p.1 / p.2 ∈ SphD}
        (hSphDm.preimage (measurable_fst.div measurable_snd)) hmain
    obtain ⟨ξab, hξab, hξabr⟩ := (hSphDmem (a / b)).mp hab
    obtain ⟨ξac, hξac, hξacr⟩ := (hSphDmem (a / c')).mp hac
    obtain ⟨ξad, hξad, hξadr⟩ := (hSphDmem (a / e)).mp had
    obtain ⟨ξbc, hξbc, hξbcr⟩ := (hSphDmem (b / c')).mp hbc
    obtain ⟨ξbd, hξbd, hξbdr⟩ := (hSphDmem (b / e)).mp hbd
    obtain ⟨ξcd, hξcd, hξcdr⟩ := (hSphDmem (c' / e)).mp hcd
    have hd1 : ξab + ξbc = ξac := by
      apply j_injective
      rw [j_add, hξab, hξbc, hξac, div_mul_div_cancel]
    have hd2 : ξab + ξbd = ξad := by
      apply j_injective
      rw [j_add, hξab, hξbd, hξad, div_mul_div_cancel]
    have hd3 : ξac + ξcd = ξad := by
      apply j_injective
      rw [j_add, hξac, hξcd, hξad, div_mul_div_cancel]
    have hf : Module.finrank ℝ ℂ ≤ 2 := by rw [Complex.finrank_real_complex]
    exact _root_.RelativeSingularity.no_four_points (V := ℂ) hf hposr 0 ξab ξac ξad
      (by rw [dist_eq_norm, zero_sub, norm_neg]; exact hξabr)
      (by rw [dist_eq_norm, zero_sub, norm_neg]; exact hξacr)
      (by rw [dist_eq_norm, zero_sub, norm_neg]; exact hξadr)
      (by rw [dist_eq_norm, show ξab - ξac = -ξbc by rw [← hd1]; ring, norm_neg]; exact hξbcr)
      (by rw [dist_eq_norm, show ξab - ξad = -ξbd by rw [← hd2]; ring, norm_neg]; exact hξbdr)
      (by rw [dist_eq_norm, show ξac - ξad = -ξcd by rw [← hd3]; ring, norm_neg]; exact hξcdr)

end RelativeSingularity
end PlaneFiveColor.Spectral
end
end OAI
