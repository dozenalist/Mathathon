/-
  m12 / swarm smwfoekgk, direction d3 (R1-structural).

  Machine-checked certificate of the (H2) content of `UniversalGood`.

  R1 replaces maximality over `UniversalGood` by maximality over compactness and then
  wants the C-nullness of the conditional difference law from Theorem A.  Theorem A needs
  (H2): "d is not Y-measurable".  This file proves that (H2) is not a consequence of the
  rest of the terminal-factor statement: any factor through which `id` factors has
  conditional difference law exactly `delta_1`, whose C-mass is 1.  Equivalently
  (contrapositive): today's `UniversalGood mu q` already implies that no wild equivariant
  map is `q`-measurable.
-/
import OAI.MeasureTheory.CompactFactors.ConditionalLimits

noncomputable section
open MeasureTheory ProbabilityTheory Filter
open scoped ENNReal

namespace OAI
namespace PlaneFiveColor.Spectral

open EuclideanFiveColor

/-- `1 in C`, because `C = range jHom` and `j 0 = 1`. -/
lemma one_mem_C : (1 : D) ∈ C := ⟨1, by simp⟩

/-- The conditional difference law of a deterministic kernel is the Dirac mass at `1`. -/
lemma differenceLaw_deterministic {Y : Type*} [MeasurableSpace Y]
    (ν : Measure Y) [IsProbabilityMeasure ν] (g : Y → D) (hg : Measurable g) :
    EuclideanFiveColor.DifferenceFourier.differenceLaw ν (Kernel.deterministic g hg) C = 1 := by
  have hprod : ((Kernel.deterministic g hg) ×ₖ (Kernel.deterministic g hg))
      = Kernel.deterministic (fun y => (g y, g y)) (hg.prodMk hg) :=
    Kernel.deterministic_prod_deterministic hg hg
  have hbind : (((Kernel.deterministic (fun y => (g y, g y)) (hg.prodMk hg)) :
      Kernel Y (D × D)) ∘ₘ ν) = ν.map (fun y => (g y, g y)) := by
    rw [← Measure.snd_compProd ν
      (Kernel.deterministic (fun y => (g y, g y)) (hg.prodMk hg)),
      Measure.compProd_deterministic (hg.prodMk hg)]
    have hs : Measure.map Prod.snd (Measure.map (fun a : Y => (a, (g a, g a))) ν)
        = ν.map (fun y => (g y, g y)) :=
      Measure.map_map (f := fun a : Y => (a, (g a, g a))) (g := Prod.snd)
        measurable_snd (measurable_id.prodMk (hg.prodMk hg))
    simpa only [Measure.snd] using hs
  rw [EuclideanFiveColor.DifferenceFourier.differenceLaw, hprod, hbind]
  have hpre : MeasurableSet ((fun p : D × D => p.1 / p.2) ⁻¹' (C : Set D)) :=
    measurableSet_C.preimage (measurable_fst.div measurable_snd)
  have h1 : Measure.map (fun p : D × D => p.1 / p.2) (ν.map (fun y => (g y, g y))) C
      = (ν.map (fun y => (g y, g y))) ((fun p : D × D => p.1 / p.2) ⁻¹' C) :=
    Measure.map_apply (measurable_fst.div measurable_snd) measurableSet_C
  have h2 : (ν.map (fun y => (g y, g y))) ((fun p : D × D => p.1 / p.2) ⁻¹' C)
      = ν ((fun y => (g y, g y)) ⁻¹' ((fun p : D × D => p.1 / p.2) ⁻¹' C)) :=
    Measure.map_apply (hg.prodMk hg) hpre
  rw [h1, h2]
  have huniv : (fun y => (g y, g y)) ⁻¹'
      ((fun p : D × D => p.1 / p.2) ⁻¹' (C : Set D)) = Set.univ := by
    ext y
    simp
  rw [huniv, measure_univ]

/-- `differenceLaw` only depends on the kernel up to a.e. equality. -/
lemma differenceLaw_congr {Y : Type*} [MeasurableSpace Y] (ν : Measure Y)
    {κ η : Kernel Y D} [IsMarkovKernel κ] [IsMarkovKernel η] (h : κ =ᵐ[ν] η) :
    EuclideanFiveColor.DifferenceFourier.differenceLaw ν κ C =
      EuclideanFiveColor.DifferenceFourier.differenceLaw ν η C := by
  have hp : (κ ×ₖ κ) =ᵐ[ν] (η ×ₖ η) := by
    filter_upwards [h] with y hy
    simp only [Kernel.prod_apply, hy]
  simp only [EuclideanFiveColor.DifferenceFourier.differenceLaw]
  rw [Measure.comp_congr hp]

/-- (H2) is not free: a factor that `id` factors through has C-mass `1`, so it can never
satisfy `UniversalGood`. -/
theorem not_universalGood_of_factorizable
    {Y : Type*} [MeasurableSpace Y] [MulAction K Y] [MeasurableConstSMul K Y]
    (μ : Measure D) [IsProbabilityMeasure μ] (q : D → Y) (hq : Measurable q)
    (hw : IsWild μ) (g : Y → D) (hg : Measurable g)
    (he : (fun d : D => g (q d)) =ᵐ[μ] id) :
    ¬ UniversalGood μ q := by
  intro hUG
  have h0 : EuclideanFiveColor.DifferenceFourier.differenceLaw (μ.map q)
      (condDistrib id q μ) C = 0 :=
    hUG id measurable_id (fun k => Eventually.of_forall fun _ => rfl) (by simpa using hw)
  have hdet : condDistrib id q μ =ᵐ[μ.map q] Kernel.deterministic g hg := by
    have h1 : condDistrib id q μ = condDistrib (fun d => g (q d)) q μ :=
      condDistrib_congr_left he.symm
    rw [h1]
    exact condDistrib_comp_self (X := q) hq.aemeasurable hg
  have h1 : EuclideanFiveColor.DifferenceFourier.differenceLaw (μ.map q)
      (condDistrib id q μ) C = 1 := by
    rw [differenceLaw_congr (μ.map q) hdet]
    exact differenceLaw_deterministic (μ.map q) g hg
  rw [h1] at h0
  exact one_ne_zero h0

end PlaneFiveColor.Spectral
end OAI

#print axioms OAI.PlaneFiveColor.Spectral.one_mem_C
#print axioms OAI.PlaneFiveColor.Spectral.differenceLaw_deterministic
#print axioms OAI.PlaneFiveColor.Spectral.differenceLaw_congr
#print axioms OAI.PlaneFiveColor.Spectral.not_universalGood_of_factorizable
