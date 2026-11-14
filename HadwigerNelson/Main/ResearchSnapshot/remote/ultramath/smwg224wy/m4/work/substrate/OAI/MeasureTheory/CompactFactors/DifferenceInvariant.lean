import OAI.Analysis.PlaneSpectrum.DifferenceLaw
import OAI.MeasureTheory.CompactFactors.RelativeCenters

namespace OAI

noncomputable section

open MeasureTheory ProbabilityTheory
open scoped BigOperators ENNReal

namespace EuclideanFiveColor.DifferenceInvariant
variable {G Y : Type*} [CommGroup G] [MeasurableSpace G]
  [MeasurableMul₂ G] [MeasurableInv G] [MeasurableSpace Y]

noncomputable def differenceLaw (ν : Measure Y) (κ : Kernel Y G) [IsMarkovKernel κ] : Measure G :=
  ((κ ×ₖ κ) ∘ₘ ν).map (fun p : G × G => p.1 / p.2)

lemma invariant (ν : Measure Y) [IsProbabilityMeasure ν]
    (κ : Kernel Y G) [IsMarkovKernel κ]
    (R : Y → Y) (hR : MeasurePreserving R ν ν)
    (T : G →* G) (hT : Measurable T)
    (he : ∀ᵐ y ∂ν, κ (R y) = (κ y).map T) :
    MeasurePreserving T (differenceLaw ν κ) (differenceLaw ν κ) := by
  have hprod : (((κ ×ₖ κ) ∘ₘ ν).map (Prod.map T T)) = ((κ ×ₖ κ) ∘ₘ ν) := by
    ext s hs
    rw [Measure.map_apply (hT.prodMap hT) hs,
      Measure.bind_apply ((hT.prodMap hT) hs) (κ ×ₖ κ).aemeasurable,
      Measure.bind_apply hs (κ ×ₖ κ).aemeasurable]
    calc
      (∫⁻ y, (κ ×ₖ κ) y ((Prod.map T T) ⁻¹' s) ∂ν) =
          ∫⁻ y, (κ ×ₖ κ) (R y) s ∂ν := by
        apply lintegral_congr_ae
        filter_upwards [he] with y hy
        rw [Kernel.prod_apply, Kernel.prod_apply, hy,
          Measure.map_prod_map _ _ hT hT, Measure.map_apply (hT.prodMap hT) hs]
      _ = ∫⁻ y, (κ ×ₖ κ) y s ∂ν := hR.lintegral_comp (Kernel.measurable_coe _ hs)
  have hdiv : Measurable (fun p : G × G => p.1 / p.2) := measurable_fst.div measurable_snd
  refine ⟨hT, ?_⟩
  rw [differenceLaw, Measure.map_map hT hdiv]
  calc
    (((κ ×ₖ κ) ∘ₘ ν).map (T ∘ (fun p : G × G => p.1 / p.2))) =
        ((κ ×ₖ κ) ∘ₘ ν).map ((fun p : G × G => p.1 / p.2) ∘ Prod.map T T) := by
      congr 1
      funext p
      exact map_div T p.1 p.2
    _ = (((κ ×ₖ κ) ∘ₘ ν).map (Prod.map T T)).map (fun p : G × G => p.1 / p.2) :=
      (Measure.map_map hdiv (hT.prodMap hT)).symm
    _ = _ := by rw [hprod]


end EuclideanFiveColor.DifferenceInvariant

namespace EuclideanFiveColor.KernelSupport
open MeasureTheory
variable {K X Y : Type*} [Group K] [MeasurableSpace X] [MeasurableSpace Y]
  [MulAction K X] [MulAction K Y] [MeasurableConstSMul K X] [MeasurableConstSMul K Y]
lemma factor_smul_preserving (μ : Measure X) [SMulInvariantMeasure K X μ]
    (p : X → Y) (hp : Measurable p)
    (hpe : ∀ k : K, ∀ᵐ x ∂μ, p (k • x) = k • p x) (k : K) :
    MeasurePreserving (fun y : Y => k • y) (μ.map p) (μ.map p) := by
  refine ⟨measurable_const_smul k, ?_⟩
  rw [Measure.map_map (measurable_const_smul k) hp]
  calc
    μ.map ((fun y : Y => k • y) ∘ p) = μ.map (p ∘ (fun x : X => k • x)) :=
      Measure.map_congr ((hpe k).mono fun _ hx => hx.symm)
    _ = (μ.map (fun x : X => k • x)).map p :=
      (Measure.map_map hp (measurable_const_smul k)).symm
    _ = μ.map p := by rw [measurePreserving_smul k μ |>.map_eq]
end EuclideanFiveColor.KernelSupport

namespace PlaneFiveColor.Spectral
open MeasureTheory ProbabilityTheory EuclideanFiveColor
open scoped BigOperators ENNReal
variable {X Y W : Type*} [MeasurableSpace X] [MeasurableSpace Y] [MeasurableSpace W]
  [MulAction K X] [MulAction K Y]
  [MeasurableConstSMul K X] [MeasurableConstSMul K Y]

lemma relative_difference_invariant (μ : Measure X) [IsProbabilityMeasure μ]
    [SMulInvariantMeasure K X μ] (b : X → D) (p : X → Y)
    (hb : Measurable b) (hp : Measurable p)
    (hbe : ∀ k : K, ∀ᵐ x ∂μ, b (k • x) = k • b x)
    (hpe : ∀ k : K, ∀ᵐ x ∂μ, p (k • x) = k • p x) (k : K) :
    MeasurePreserving (fun d : D => k • d)
      (DifferenceFourier.differenceLaw (μ.map p) (condDistrib b p μ))
      (DifferenceFourier.differenceLaw (μ.map p) (condDistrib b p μ)) := by
  have he := KernelSupport.condDistrib_equivariant μ b p hb hp
    (MeasurableEquiv.smul k) (MeasurableEquiv.smul k) (fun d : D => k • d)
    (measurable_const_smul k) (measurePreserving_smul k μ) (hpe k) (hbe k)
  haveI : IsProbabilityMeasure (Measure.map p μ) :=
    Measure.isProbabilityMeasure_map hp.aemeasurable
  exact DifferenceInvariant.invariant (μ.map p) (condDistrib b p μ)
    (fun y : Y => k • y) (KernelSupport.factor_smul_preserving μ p hp hpe k)
    (scalarHom (kCoeff k)) (measurable_const_smul k) he


end PlaneFiveColor.Spectral

end

end OAI
