/-
  m4, direction d10 (R2 transfinite / stabilization).

  Result: the class of compact extensions of the trivial factor is a *complete
  lattice of sigma-algebras with an explicit top*, which the tree already defines
  (`compactSigma` in MeasureTheory/CompactFactors/Functions.lean).  Therefore
  maximality, chain-join closure, Zorn (`CodedMax`) and any ordinal tower are NOT
  where the difficulty of `exists_terminal_factor` lies.  What remains is the
  successor step ("compact over compact is compact"), see VERDICT-d10.md.

  Everything below is checked against the tree's own definitions, no new axioms.
-/
import OAI.MeasureTheory.CompactFactors.Functions

open MeasureTheory
open OAI.EuclideanFiveColor.CompactFunctions
open OAI.EuclideanFiveColor

namespace M4Probe

variable {K X : Type*} [SMul K X] [MeasurableSpace X] [MeasurableConstSMul K X]
  (μ : Measure X) [IsProbabilityMeasure μ]
  (hpres : ∀ k : K, MeasurePreserving (fun x : X => k • x) μ μ)

/-- The trivial factor. -/
def triv (X : Type*) : X → Unit := fun _ => ()

/-- **The top of the class of compact extensions of the trivial factor.** -/
@[instance_reducible] def topSigma : MeasurableSpace X :=
  compactSigma (K := K) μ (triv X) measurable_const hpres

lemma topSigma_le : topSigma (K := K) μ hpres ≤ ‹MeasurableSpace X› :=
  compactSigma_le μ (triv X) measurable_const hpres

/-- Membership unfolded: the sets whose indicator is compact over the trivial factor. -/
lemma mem_topSigma {s : Set X} :
    @MeasurableSet X (topSigma (K := K) μ hpres) s ↔
      MeasurableSet s ∧ Compact (K := K) μ (triv X) (s.indicator (fun _ => (1 : ℂ))) :=
  Iff.rfl

/-- (i) bounded + compact over the trivial factor => measurable for the top. -/
lemma measurable_topSigma_of_compact {H : X → ℂ} (hm : Measurable H)
    (hc : Compact (K := K) μ (triv X) H) :
    @Measurable X ℂ (topSigma (K := K) μ hpres) inferInstance H :=
  measurable_compactSigma (K := K) (q := triv X) measurable_const hpres hm hc

/-- (ii) bounded + measurable for the top => compact over the trivial factor.
Together with (i): the top is exactly "the sigma-algebra of compact functions". -/
lemma compact_of_measurable_topSigma {H : X → ℂ}
    (hm : @Measurable X ℂ (topSigma (K := K) μ hpres) inferInstance H) (C : ℝ) (hC : 0 ≤ C)
    (hb : ∀ x, ‖H x‖ ≤ C) : Compact (K := K) μ (triv X) H :=
  compact_of_measurable_compactSigma (K := K) (q := triv X) measurable_const hpres hm C hC hb

/-- A member of the class, as an inclusion of sigma-algebras. -/
def InClass {Y : Type*} (mY : MeasurableSpace Y) (q : X → Y) : Prop :=
  MeasurableSpace.comap q mY ≤ topSigma (K := K) μ hpres

/-- **The class is closed under finite joins**: every bounded function of a member is
compact over the trivial factor.  This is the hypothesis `hjoin` of
`CodedMax.exists_maximal` in the only form that machinery needs. -/
lemma compact_of_inClass {Y : Type*} {mY : MeasurableSpace Y} {q : X → Y}
    (hq : InClass (K := K) μ hpres mY q) {F : Y → ℂ} (hF : @Measurable Y ℂ mY inferInstance F)
    (C : ℝ) (hC : 0 ≤ C) (hb : ∀ y, ‖F y‖ ≤ C) :
    Compact (K := K) μ (triv X) (F ∘ q) := by
  have hq' : @Measurable X Y (MeasurableSpace.comap q mY) mY q :=
    measurable_iff_comap_le.mpr le_rfl
  have h1 : @Measurable X ℂ (MeasurableSpace.comap q mY) inferInstance (F ∘ q) := hF.comp hq'
  have h2 : @Measurable X ℂ (topSigma (K := K) μ hpres) inferInstance (F ∘ q) :=
    h1.mono hq le_rfl
  exact compact_of_measurable_topSigma (K := K) μ hpres h2 C hC (fun x => hb (q x))

/-- **Join closure in full generality**: the join of ANY family of sub-sigma-algebras
inside the class is again inside it.  One application of `iSup_le`; no approximation
property, no chain enumeration, no phase-collision induction. -/
lemma join_inClass {ι : Type*} (m : ι → MeasurableSpace X)
    (hm : ∀ i, m i ≤ topSigma (K := K) μ hpres) :
    (⨆ i, m i) ≤ topSigma (K := K) μ hpres :=
  iSup_le hm

/-- The class has a greatest element: the top itself, coded by the identity. -/
lemma topSigma_inClass :
    InClass (K := K) μ hpres (topSigma (K := K) μ hpres) (id : X → X) := by
  show MeasurableSpace.comap id (topSigma (K := K) μ hpres) ≤ topSigma (K := K) μ hpres
  rw [MeasurableSpace.comap_id]

#print axioms M4Probe.measurable_topSigma_of_compact
#print axioms M4Probe.compact_of_measurable_topSigma
#print axioms M4Probe.compact_of_inClass
#print axioms M4Probe.join_inClass
#print axioms M4Probe.topSigma_inClass

end M4Probe
