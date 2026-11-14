import OAI.MeasureTheory.CompactFactors.Stationary

/-!
# The compact tower needs no approximation property

`PlaneFiveColor.Spectral.exists_terminal_factor` obtains a factor whose relative
product is ergodic by maximising over the class `UniversalGood`.  Every step of that
maximality except the last must re-establish `UniversalGood` at the new factor, which
is where the whole approximation / phase-collision theory is consumed.

This file records that the *ergodicity* half needs none of it.  `Tower` is the class of
factors generated from the trivial factor by countably many compact-extension steps,
generated inductively so that closure under joins and under strict compact successors is
free by construction.  `CompactTower.strict_compact_successor` is unconditional in the
non-ergodicity of the relative product, so maximality in `Tower` immediately gives a
factor with ergodic relative product, with no `UniversalGood` and no (2.6).
-/

namespace OAI

noncomputable section

open MeasureTheory ProbabilityTheory
open scoped ENNReal

namespace PlaneFiveColor.Spectral
open EuclideanFiveColor

variable {X : Type*} [MeasurableSpace X] [StandardBorelSpace X] [Nonempty X]
  [MulAction K X] [MeasurableConstSMul K X]

/-- Factors reached from the trivial factor by countably many compact-extension steps.

The three constructors are exactly the three things a maximality argument needs to be
closed under: the base case, the strict compact successor
(`CompactTower.strict_compact_successor`), and the countable chain join
(`ChainJoin.le_code`).  Unlike `UniversalGood`, membership is *not* antitone in the
factor, so the top factor is reachable exactly when the system is a compact extension of
the trivial factor. -/
inductive Tower (μ : Measure X) : (X → OrbitSpace K) → Prop where
  | base : Tower μ (fun _ => (⟨fun _ => 0⟩ : OrbitSpace K))
  | step : ∀ (p : X → OrbitSpace K) (H : X → ℂ), Tower μ p → Measurable H →
      (∀ x, ‖H x‖ ≤ 2) →
      (¬ ∃ b : OrbitSpace K → ℂ, Measurable b ∧ H =ᵐ[μ] b ∘ p) →
      Tower μ (FactorCode.encode (K := K) (OrbitFactor.extend (K := K) p H))
  | join : ∀ (q : ℕ → X → OrbitSpace K), (∀ n, Tower μ (q n)) →
      (∀ i j, FactorLp.space μ (q i) ≤ FactorLp.space μ (q j) ∨
        FactorLp.space μ (q j) ≤ FactorLp.space μ (q i)) →
      Tower μ (ChainJoin.code (K := K) q)

/-- A maximal member of the compact tower.  Nothing about `UniversalGood` is used. -/
theorem exists_tower_maximal (μ : Measure X) [IsProbabilityMeasure μ] :
    ∃ a : CodedMax.Model (K := K) μ (Tower μ), IsMax a := by
  classical
  refine CodedMax.exists_maximal (K := K) μ (Tower μ) ?_ ?_
  · refine ⟨⟨fun _ => (⟨fun _ => 0⟩ : OrbitSpace K), measurable_const, ?_, Tower.base⟩⟩
    intro k
    exact Filter.Eventually.of_forall fun x => by ext l; rfl
  · intro q _hq _hqe hg hc
    exact Tower.join q hg hc

/-- **The supremum of the compact tower has ergodic relative product.**

This is the whole of what `exists_terminal_factor` needs from maximality, and it is
obtained from `CompactTower.strict_compact_successor` alone: no approximation property,
no phase-collision induction, no `UniversalGood`. -/
theorem exists_ergodic_factor (μ : Measure X) [IsProbabilityMeasure μ] [ErgodicSMul K X μ] :
    ∃ p : X → OrbitSpace K, ∃ hp : Measurable p,
      (∀ k : K, ∀ᵐ x ∂μ, p (k • x) = k • p x) ∧
      (∀ q : X → OrbitSpace K, Tower μ q → Measurable q →
        (∀ k : K, ∀ᵐ x ∂μ, q (k • x) = k • q x) →
        FactorLp.space μ p ≤ FactorLp.space μ q → FactorLp.space μ q ≤ FactorLp.space μ p) ∧
      ErgodicSMul K (X × X) (RelativeProduct.law μ p hp) := by
  classical
  obtain ⟨a, hamax⟩ := exists_tower_maximal μ
  refine ⟨a.map, a.measurable, a.equivariant, ?_, ?_⟩
  · intro q hqT hqm hqe hle
    exact hamax (b := (⟨q, hqm, hqe, hqT⟩ : CodedMax.Model (K := K) μ (Tower μ))) hle
  · by_contra hn
    obtain ⟨H, hH, hB, hnot, _hc⟩ :=
      CompactTower.strict_compact_successor μ a.map a.measurable a.equivariant hn
    let v : X → OrbitSpace K :=
      FactorCode.encode (K := K) (OrbitFactor.extend (K := K) a.map H)
    have hvT : Tower μ v := Tower.step a.map H a.good hH hB hnot
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
      hamax (b := (⟨v, hvm, hve, hvT⟩ : CodedMax.Model (K := K) μ (Tower μ))) hab
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

/-- **Drop-in replacement for `exists_terminal_factor`, given the one remaining
obligation.**  Everything except `hgood` is discharged here, without the approximation
property.  `hgood` must supply `UniversalGood` at the tower supremum; by the report in
`sprint/simplify/m15/AUDIT.md` that is exactly Theorem A plus properness of the
supremum, and properness is the part that maximality cannot give. -/
theorem exists_terminal_factor_of_tower_good
    (μ : Measure X) [IsProbabilityMeasure μ] [ErgodicSMul K X μ]
    (hgood : ∀ (p : X → OrbitSpace K) (hp : Measurable p),
      (∀ k : K, ∀ᵐ x ∂μ, p (k • x) = k • p x) →
      (∀ q : X → OrbitSpace K, Tower μ q → Measurable q →
        (∀ k : K, ∀ᵐ x ∂μ, q (k • x) = k • q x) →
        FactorLp.space μ p ≤ FactorLp.space μ q → FactorLp.space μ q ≤ FactorLp.space μ p) →
      ErgodicSMul K (X × X) (RelativeProduct.law μ p hp) → UniversalGood μ p) :
    ∃ p : X → OrbitSpace K, ∃ hp : Measurable p,
      (∀ k : K, ∀ᵐ x ∂μ, p (k • x) = k • p x) ∧ UniversalGood μ p ∧
      ErgodicSMul K (X × X) (RelativeProduct.law μ p hp) := by
  obtain ⟨p, hp, hpe, hmax, herg⟩ := exists_ergodic_factor μ
  exact ⟨p, hp, hpe, hgood p hp hpe hmax herg, herg⟩

end PlaneFiveColor.Spectral

end

end OAI

#print axioms OAI.PlaneFiveColor.Spectral.exists_tower_maximal
#print axioms OAI.PlaneFiveColor.Spectral.exists_ergodic_factor
#print axioms OAI.PlaneFiveColor.Spectral.exists_terminal_factor_of_tower_good
