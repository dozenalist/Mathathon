import OAI.MeasureTheory.CompactFactors.TowerAudit

/-!
# The compact tower with the missing hypothesis restored

`Tower` (transcribed from `sprint/simplify/m15/work/TowerMax.lean`) has a
`step` constructor with no compactness hypothesis, and `TowerAudit.hgood_false` shows the
consequence: its maximal member generates the whole `σ`-algebra, where `UniversalGood`
fails, so `exists_terminal_factor_of_tower_good` is vacuous.

Here the `step` constructor carries the compactness clause that
`CompactTower.strict_compact_successor` actually produces (the `_hc` field that m15
discards):

  `∀ F, Measurable F → bounded F → Compact (μ.map (extend p H)) Prod.fst F`.

With it (i) the maximality and ergodicity conclusions of m15 still hold with the same
proof, and (ii) the tower no longer collapses: a member can only be extended when its
successor is compact over it, so `TowerAudit.tower_max_all_factorizable` no longer
applies.  What the corrected class still owes is the invariant

  `L²(p) ⊆ A`, `A := {H : the K-orbit of H is totally bounded in L²(μ)}`,

i.e. that every member is a compact extension of the point factor; the step needs the
Furstenberg–Zimmer transition lemma (d6) for that, and properness needs (N) (d3).
-/

namespace OAI

noncomputable section

open MeasureTheory ProbabilityTheory
open scoped ENNReal

namespace PlaneFiveColor.Spectral
open EuclideanFiveColor

variable {X : Type*} [MeasurableSpace X] [StandardBorelSpace X] [Nonempty X]
  [MulAction K X] [MeasurableConstSMul K X]

/-- The compact tower: base, strict compact successor (with its compactness clause),
countable chain join. -/
inductive TowerC (μ : Measure X) : (X → OrbitSpace K) → Prop where
  | base : TowerC μ (fun _ => (⟨fun _ => 0⟩ : OrbitSpace K))
  | step : ∀ (p : X → OrbitSpace K) (H : X → ℂ), TowerC μ p → Measurable H →
      (∀ x, ‖H x‖ ≤ 2) →
      (¬ ∃ b : OrbitSpace K → ℂ, Measurable b ∧ H =ᵐ[μ] b ∘ p) →
      (∀ F : OrbitSpace K × OrbitSpace K → ℂ, Measurable F →
        (∃ C : ℝ, ∀ z, ‖F z‖ ≤ C) →
        CompactFunctions.Compact (K := K) (μ.map (OrbitFactor.extend (K := K) p H))
          Prod.fst F) →
      TowerC μ (FactorCode.encode (K := K) (OrbitFactor.extend (K := K) p H))
  | join : ∀ (q : ℕ → X → OrbitSpace K), (∀ n, TowerC μ (q n)) →
      (∀ i j, FactorLp.space μ (q i) ≤ FactorLp.space μ (q j) ∨
        FactorLp.space μ (q j) ≤ FactorLp.space μ (q i)) →
      TowerC μ (ChainJoin.code (K := K) q)

/-- Every member of the corrected tower is a member of m15's tower: the correction only
removes members, it adds none. -/
theorem TowerC.toTower {μ : Measure X} {p : X → OrbitSpace K} (h : TowerC μ p) :
    Tower μ p := by
  induction h with
  | base => exact Tower.base
  | step p H _ hH hB hnot _ ih => exact Tower.step p H ih hH hB hnot
  | join q _ hc ih => exact Tower.join q ih hc

/-- A maximal member of the corrected tower. -/
theorem exists_towerC_maximal (μ : Measure X) [IsProbabilityMeasure μ] :
    ∃ a : CodedMax.Model (K := K) μ (TowerC μ), IsMax a := by
  classical
  refine CodedMax.exists_maximal (K := K) μ (TowerC μ) ?_ ?_
  · refine ⟨⟨fun _ => (⟨fun _ => 0⟩ : OrbitSpace K), measurable_const, ?_, TowerC.base⟩⟩
    intro k
    exact Filter.Eventually.of_forall fun x => by ext l; rfl
  · intro q _hq _hqe hg hc
    exact TowerC.join q hg hc

/-- **Maximality gives ergodicity of the relative product**, exactly as in m15 but for
the corrected class: the strict compact successor of a maximal member is itself a member
(its compactness clause is produced by `strict_compact_successor`), so maximality
forbids non-ergodicity. -/
theorem exists_ergodic_factor_C (μ : Measure X) [IsProbabilityMeasure μ]
    [ErgodicSMul K X μ] :
    ∃ p : X → OrbitSpace K, ∃ hp : Measurable p,
      (∀ k : K, ∀ᵐ x ∂μ, p (k • x) = k • p x) ∧ TowerC μ p ∧
      (∀ (q : X → OrbitSpace K), TowerC μ q → Measurable q →
        (∀ k : K, ∀ᵐ x ∂μ, q (k • x) = k • q x) →
        FactorLp.space μ p ≤ FactorLp.space μ q → FactorLp.space μ q ≤ FactorLp.space μ p) ∧
      ErgodicSMul K (X × X) (RelativeProduct.law μ p hp) := by
  classical
  obtain ⟨a, hamax⟩ := exists_towerC_maximal μ
  refine ⟨a.map, a.measurable, a.equivariant, a.good, ?_, ?_⟩
  · intro q hqT hqm hqe hle
    exact hamax (b := (⟨q, hqm, hqe, hqT⟩ : CodedMax.Model (K := K) μ (TowerC μ))) hle
  · by_contra hn
    obtain ⟨H, hH, hB, hnot, hc⟩ :=
      CompactTower.strict_compact_successor μ a.map a.measurable a.equivariant hn
    let v : X → OrbitSpace K :=
      FactorCode.encode (K := K) (OrbitFactor.extend (K := K) a.map H)
    have hvT : TowerC μ v := TowerC.step a.map H a.good hH hB hnot hc
    have hvm : Measurable v :=
      FactorCode.encode_measurable (OrbitFactor.measurable_extend a.measurable hH)
    have hve (k : K) : ∀ᵐ x ∂μ, v (k • x) = k • v x :=
      Filter.Eventually.of_forall
        (FactorCode.encode_equivariant (K := K) (OrbitFactor.extend (K := K) a.map H) k)
    have hab : FactorLp.space μ a.map ≤ FactorLp.space μ v := by
      apply FactorLp.le_of_factor μ a.map v
        (Prod.fst ∘ FactorCode.decode (K := K) (Y := OrbitSpace K × OrbitSpace K))
        (measurable_fst.comp FactorCode.decode_measurable)
      exact Filter.Eventually.of_forall fun x => by
        dsimp only [Function.comp_apply, v]
        rw [FactorCode.decode_encode]
        rfl
    have hba : FactorLp.space μ v ≤ FactorLp.space μ a.map :=
      hamax (b := (⟨v, hvm, hve, hvT⟩ : CodedMax.Model (K := K) μ (TowerC μ))) hab
    have hHlp : MemLp H 2 μ :=
      MemLp.of_bound hH.aestronglyMeasurable 2 (Filter.Eventually.of_forall hB)
    let J : OrbitSpace K → ℂ := fun z =>
      (FactorCode.decode (K := K) (Y := OrbitSpace K × OrbitSpace K) z).2.val 1
    have hJ : Measurable J := (measurable_pi_apply 1).comp
      (OrbitSpace.measurable_val.comp (measurable_snd.comp FactorCode.decode_measurable))
    have hHv : hHlp.toLp H ∈ FactorLp.space μ v := by
      apply FactorLp.mem_of_rep μ v _ J hJ
      filter_upwards [hHlp.coeFn_toLp] with x hx
      rw [hx]
      dsimp only [Function.comp_apply, J, v]
      rw [FactorCode.decode_encode]
      exact (OrbitFactor.orbit_one H x).symm
    obtain ⟨g, hg, hhe⟩ := FactorLp.exists_rep μ a.map _ (hba hHv)
    exact hnot ⟨g, hg, hHlp.coeFn_toLp.symm.trans hhe⟩

/-- The corrected interface for the terminal factor: everything except `UniversalGood`
at the maximal member is discharged here, and the hypothesis is now a statement about a
class that does not collapse. -/
theorem exists_terminal_factor_of_towerC_good
    (μ : Measure X) [IsProbabilityMeasure μ] [ErgodicSMul K X μ]
    (hgood : ∀ (p : X → OrbitSpace K) (hp : Measurable p),
      (∀ k : K, ∀ᵐ x ∂μ, p (k • x) = k • p x) → TowerC μ p →
      (∀ (q : X → OrbitSpace K), TowerC μ q → Measurable q →
        (∀ k : K, ∀ᵐ x ∂μ, q (k • x) = k • q x) →
        FactorLp.space μ p ≤ FactorLp.space μ q → FactorLp.space μ q ≤ FactorLp.space μ p) →
      ErgodicSMul K (X × X) (RelativeProduct.law μ p hp) → UniversalGood μ p) :
    ∃ p : X → OrbitSpace K, ∃ hp : Measurable p,
      (∀ k : K, ∀ᵐ x ∂μ, p (k • x) = k • p x) ∧ UniversalGood μ p ∧
      ErgodicSMul K (X × X) (RelativeProduct.law μ p hp) := by
  obtain ⟨p, hp, hpe, hpT, hmax, herg⟩ := exists_ergodic_factor_C μ
  exact ⟨p, hp, hpe, hgood p hp hpe hpT hmax herg, herg⟩

end PlaneFiveColor.Spectral

end

end OAI
