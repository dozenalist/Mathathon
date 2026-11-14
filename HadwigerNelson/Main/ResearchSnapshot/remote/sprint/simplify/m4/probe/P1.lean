/-
  m4, direction d10. Question: does the class of compact extensions of the trivial
  factor have an explicit TOP?  If so, chain-join closure, Zorn and the ordinal
  tower are all unnecessary, and R1's only real obligation is the successor step.
-/
import OAI.MeasureTheory.CompactFactors.Stationary

open MeasureTheory
open OAI.EuclideanFiveColor.CompactFunctions
open OAI.EuclideanFiveColor

namespace M4Probe

variable {K X : Type*} [SMul K X] [MeasurableSpace X] [MeasurableConstSMul K X]
  (μ : Measure X) [IsProbabilityMeasure μ]
  (hpres : ∀ k : K, MeasurePreserving (fun x : X => k • x) μ μ)

/-- The trivial factor. -/
def triv (X : Type*) : X → Unit := fun _ => ()

/-- The top of the class: the tree's own `compactSigma` at the trivial factor. -/
def top : MeasurableSpace X := compactSigma (K := K) μ (triv X) measurable_const hpres

lemma top_le : top (K := K) μ hpres ≤ ‹MeasurableSpace X› :=
  compactSigma_le μ (triv X) measurable_const hpres

/-- Membership, unfolded: sets whose indicator is compact over the trivial factor. -/
lemma mem_top {s : Set X} :
    @MeasurableSet X (top (K := K) μ hpres) s ↔
      MeasurableSet s ∧ Compact (K := K) μ (triv X) (s.indicator (fun _ => (1 : ℂ))) :=
  Iff.rfl

lemma measurable_top_of_compact {H : X → ℂ} (hm : Measurable H)
    (hc : Compact (K := K) μ (triv X) H) :
    @Measurable X ℂ (top (K := K) μ hpres) inferInstance H :=
  measurable_compactSigma (K := K) (q := triv X) measurable_const hpres hm hc

lemma compact_of_measurable_top {H : X → ℂ}
    (hm : @Measurable X ℂ (top (K := K) μ hpres) inferInstance H) (C : ℝ) (hC : 0 ≤ C)
    (hb : ∀ x, ‖H x‖ ≤ C) : Compact (K := K) μ (triv X) H :=
  compact_of_measurable_compactSigma (K := K) (q := triv X) measurable_const hpres hm C hC hb

/-- A member of the class, as an inclusion of sigma-algebras. -/
def InClass {Y : Type*} (mY : MeasurableSpace Y) (q : X → Y) : Prop :=
  MeasurableSpace.comap q mY ≤ top (K := K) μ hpres

/-- Bounded functions of a member of the class are compact over the trivial factor. -/
lemma compact_of_inClass {Y : Type*} {mY : MeasurableSpace Y} {q : X → Y}
    (hq : InClass (K := K) μ hpres mY q) {F : Y → ℂ} (hF : @Measurable Y ℂ mY inferInstance F)
    (C : ℝ) (hC : 0 ≤ C) (hb : ∀ y, ‖F y‖ ≤ C) :
    Compact (K := K) μ (triv X) (F ∘ q) := by
  have hq' : @Measurable X Y (MeasurableSpace.comap q mY) mY q :=
    measurable_iff_comap_le.mpr le_rfl
  have h1 : @Measurable X ℂ (MeasurableSpace.comap q mY) inferInstance (F ∘ q) := hF.comp hq'
  have h2 : @Measurable X ℂ (top (K := K) μ hpres) inferInstance (F ∘ q) :=
    h1.mono hq (le_refl inferInstance)
  exact compact_of_measurable_top (K := K) μ hpres h2 C hC (fun x => hb (q x))

/-- JOIN CLOSURE, full generality, one `iSup_le`.  This is what Stationary.lean
currently buys through `relative_singularity_approximation` + `ChainJoin.approximation`. -/
lemma join_inClass {ι : Type*} {Y : ι → Type*} {mY : ∀ i, MeasurableSpace (Y i)}
    (q : ∀ i, X → Y i) (h : ∀ i, InClass (K := K) μ hpres (mY i) (q i)) :
    (⨆ i, MeasurableSpace.comap (q i) (mY i)) ≤ top (K := K) μ hpres :=
  iSup_le h

/-- The top itself is a member. -/
lemma top_inClass : InClass (K := K) μ hpres ‹MeasurableSpace X› (id : X → X) := le_rfl

/-- Strictness: a bounded measurable function that is not compact over the trivial
factor is not measurable for the top. -/
lemma not_measurable_top {H : X → ℂ} (hm : Measurable H) (C : ℝ)
    (hb : ∀ x, ‖H x‖ ≤ C) (hc : ¬ Compact (K := K) μ (triv X) H) :
    ¬ @Measurable X ℂ (top (K := K) μ hpres) inferInstance H :=
  fun h => hc (compact_of_measurable_top (K := K) μ hpres h C (by linarith [norm_nonneg (H (Classical.arbitrary X))]) hb)

#check @OAI.EuclideanFiveColor.CompactTower.strict_compact_successor
#check @OAI.EuclideanFiveColor.ChainJoin.code
#check @OAI.EuclideanFiveColor.ChainJoin.approximation
#check @OAI.PlaneFiveColor.Spectral.CodedMax.exists_maximal
#check @OAI.PlaneFiveColor.Spectral.relative_singularity_base
#check @OAI.EuclideanFiveColor.RelativeProduct.law
#check @OAI.EuclideanFiveColor.OrbitFactor.extend
#check @OAI.EuclideanFiveColor.FactorLp.space

end M4Probe
