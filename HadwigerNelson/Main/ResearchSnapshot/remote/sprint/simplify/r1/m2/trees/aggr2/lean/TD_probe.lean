import OAI.MeasureTheory.CompactFactors.Stationary

/-!
# `TowerMax.lean`'s `Tower` is the class of *all* factors, so its maximal member
  sees the whole of `L²` and `UniversalGood` is false there.

`sprint/simplify/m15/work/TowerMax.lean` isolates the ergodicity half of
`exists_terminal_factor` by maximising over

  `Tower μ` = base / `Tower.step` / `Tower.join`

and claims (docstring of `Tower`): "Unlike `UniversalGood`, membership is *not*
antitone in the factor, so the top factor is reachable exactly when the system is a
compact extension of the trivial factor."

That claim is false for the `step` constructor as written.  `Tower.step` has only

  `Measurable H`, `∀ x, ‖H x‖ ≤ 2`, `¬ ∃ b, Measurable b ∧ H =ᵐ b ∘ p`

-- no compactness, no approximation, no hypothesis that the relative product over `p`
fails to be ergodic.  So `Tower.step` can be applied to the maximal member `a` with
*any* non-degenerate bounded measurable `H`, and the resulting factor is strictly
larger (the argument already present in `exists_ergodic_factor`).  Maximality
therefore forces every bounded measurable function to be `μ`-a.e. a function of
`a.map`:

  `tower_max_all_measurable` below.

Consequently the maximal tower member determines the whole sigma-algebra, so its
relative product `RelativeProduct.law μ a.map` is carried by the diagonal, and
`UniversalGood μ a.map` is *false* for every wild `μ` (witness `d = id`: over the
top factor the relative difference law is the Dirac mass at `1`, and `1 ∈ C`).
Since `exists_terminal_factor_of_tower_good` demands `UniversalGood` at exactly
such an `a`, its hypothesis is refutable: the theorem is vacuous, and no
R1 deletion can be routed through it until `Tower.step` is restricted.
-/

namespace OAI

noncomputable section

open MeasureTheory ProbabilityTheory
open scoped ENNReal

namespace PlaneFiveColor.Spectral
open EuclideanFiveColor

variable {X : Type*} [MeasurableSpace X] [StandardBorelSpace X] [Nonempty X]
  [MulAction K X] [MeasurableConstSMul K X]

/-- Verbatim copy of `sprint/simplify/m15/work/TowerMax.lean`. -/
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

theorem exists_tower_maximal (μ : Measure X) [IsProbabilityMeasure μ] :
    ∃ a : CodedMax.Model (K := K) μ (Tower μ), IsMax a := by
  classical
  refine CodedMax.exists_maximal (K := K) μ (Tower μ) ?_ ?_
  · refine ⟨⟨fun _ => (⟨fun _ => 0⟩ : OrbitSpace K), measurable_const, ?_, Tower.base⟩⟩
    intro k
    exact Filter.Eventually.of_forall fun x => by ext l; rfl
  · intro q _hq _hqe hg hc
    exact Tower.join q hg hc

/-- **Maximality in `Tower` forces everything to be measurable.**  For a maximal
member `a` of `Tower`, every bounded measurable `H : X → ℂ` is `μ`-a.e. a function
of `a.map`; otherwise `Tower.step` would produce a strictly larger member. -/
theorem tower_max_all_measurable (μ : Measure X) [IsProbabilityMeasure μ] [ErgodicSMul K X μ]
    (a : CodedMax.Model (K := K) μ (Tower μ)) (hamax : IsMax a)
    (H : X → ℂ) (hH : Measurable H) (hB : ∀ x, ‖H x‖ ≤ 2) :
    ∃ b : OrbitSpace K → ℂ, Measurable b ∧ H =ᵐ[μ] b ∘ a.map := by
  classical
  by_contra hnot
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

end PlaneFiveColor.Spectral

end

end OAI
