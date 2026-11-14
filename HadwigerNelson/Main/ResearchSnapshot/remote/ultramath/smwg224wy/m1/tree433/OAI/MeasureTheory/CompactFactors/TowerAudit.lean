import OAI.MeasureTheory.CompactFactors.Stationary

/-!
# Audit of the m15 tower architecture (`sprint/simplify/m15/work/TowerMax.lean`)

`TowerMax.Tower` has three constructors: base, `step`, `join`.  Its `step` constructor
carries NO compactness hypothesis: it adjoins an arbitrary bounded measurable function
that is not already factorizable.  Consequently the class of tower factors is the class
of *all* countably generated factors, and every maximal member generates the whole
`σ`-algebra of `X`.

* `tower_max_all_factorizable` : at a maximal tower member every bounded measurable
  function is factorizable through the member;
* `tower_max_generating` : consequently the identity of `X` factors through the member.

The point for the sprint: `exists_terminal_factor_of_tower_good` requires
`UniversalGood μ p` at that maximal member.  We port m15's own `exists_ergodic_factor`
(`exists_ergodic_factor_audit`, proof transcribed) and then show in `hgood_false` that
its hypothesis `hgood` is refutable for every wild `μ` on `D`: a maximal member is
generating, so `condDistrib id p μ` is a Dirac kernel, the relative difference law of
the identity is `δ_1`, and `1 = j 0 ∈ C` makes its `C`-mass `1 ≠ 0`.

Singleton `X` (`X = PUnit`) would make the class trivial, so every statement below is
stated at the same generality as m15's file.
-/

namespace OAI

noncomputable section

open MeasureTheory ProbabilityTheory
open scoped ENNReal

namespace PlaneFiveColor.Spectral
open EuclideanFiveColor

variable {X : Type*} [MeasurableSpace X] [StandardBorelSpace X] [Nonempty X]
  [MulAction K X] [MeasurableConstSMul K X]

/-- The m15 tower class, transcribed verbatim from `TowerMax.lean`. -/
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

/-- The maximality clause returned by m15's `exists_ergodic_factor`, verbatim. -/
def TowerMaximal (μ : Measure X) (p : X → OrbitSpace K) : Prop :=
  ∀ (q : X → OrbitSpace K), Tower μ q → Measurable q →
    (∀ k : K, ∀ᵐ x ∂μ, q (k • x) = k • q x) →
    FactorLp.space μ p ≤ FactorLp.space μ q → FactorLp.space μ q ≤ FactorLp.space μ p

omit [StandardBorelSpace X] [Nonempty X] in
/-- A `Tower` member of `L²`-norm bound `2` is factorizable at a maximal tower member.
This is exactly m15's maximality argument in `exists_ergodic_factor`, with the
compactness output of `strict_compact_successor` (named `_hc` there) not used. -/
theorem tower_max_factorizable_bound
    (μ : Measure X) [IsProbabilityMeasure μ]
    (p : X → OrbitSpace K) (hp : Measurable p) (hpT : Tower μ p)
    (hmax : TowerMaximal μ p)
    (H : X → ℂ) (hH : Measurable H) (hHB : ∀ x, ‖H x‖ ≤ 2) :
    ∃ b : OrbitSpace K → ℂ, Measurable b ∧ H =ᵐ[μ] b ∘ p := by
  classical
  by_contra hnot
  have hvT : Tower μ (FactorCode.encode (K := K) (OrbitFactor.extend (K := K) p H)) :=
    Tower.step p H hpT hH hHB hnot
  set v : X → OrbitSpace K := FactorCode.encode (K := K) (OrbitFactor.extend (K := K) p H)
  have hvT' : Tower μ v := hvT
  have hvm : Measurable v :=
    FactorCode.encode_measurable (OrbitFactor.measurable_extend hp hH)
  have hve (k : K) : ∀ᵐ x ∂μ, v (k • x) = k • v x :=
    Filter.Eventually.of_forall (FactorCode.encode_equivariant (K := K) _ k)
  have hab : FactorLp.space μ p ≤ FactorLp.space μ v := by
    apply FactorLp.le_of_factor μ p v
      (Prod.fst ∘ FactorCode.decode (K := K) (Y := OrbitSpace K × OrbitSpace K))
      (measurable_fst.comp FactorCode.decode_measurable)
    exact Filter.Eventually.of_forall fun x => by
      dsimp only [Function.comp_apply, v]
      rw [FactorCode.decode_encode]
      rfl
  have hba : FactorLp.space μ v ≤ FactorLp.space μ p := hmax v hvT' hvm hve hab
  have hHlp : MemLp H 2 μ :=
    MemLp.of_bound hH.aestronglyMeasurable 2 (Filter.Eventually.of_forall hHB)
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
  obtain ⟨g, hg, hhe⟩ := FactorLp.exists_rep μ p _ (hba hHv)
  exact hnot ⟨g, hg, hHlp.coeFn_toLp.symm.trans hhe⟩

/-- **The refutation.**  At a maximal member of the m15 tower, every bounded measurable
function is factorizable: the member generates the whole `σ`-algebra of `X`. -/
theorem tower_max_all_factorizable
    (μ : Measure X) [IsProbabilityMeasure μ]
    (p : X → OrbitSpace K) (hp : Measurable p) (hpT : Tower μ p)
    (hmax : TowerMaximal μ p)
    (H : X → ℂ) (hH : Measurable H) (hHB : ∃ C : ℝ, ∀ x, ‖H x‖ ≤ C) :
    ∃ b : OrbitSpace K → ℂ, Measurable b ∧ H =ᵐ[μ] b ∘ p := by
  classical
  obtain ⟨C, hC⟩ := hHB
  set c : ℝ := max C 0 + 1 with hcdef
  have hcpos : 0 < c := by rw [hcdef]; positivity
  have hle : ∀ x, ‖H x / (c : ℂ)‖ ≤ 2 := by
    intro x
    rw [norm_div, Complex.norm_real, Real.norm_eq_abs, abs_of_pos hcpos]
    have h1 : ‖H x‖ ≤ C := hC x
    have h2 : ‖H x‖ ≤ c := h1.trans ((le_max_left C 0).trans (le_add_of_nonneg_right zero_le_one))
    have h3 : ‖H x‖ / c ≤ 1 := by
      rw [div_le_one hcpos]; exact h2
    linarith
  have hfac : ∃ b : OrbitSpace K → ℂ, Measurable b ∧
      (fun x => H x / (c : ℂ)) =ᵐ[μ] b ∘ p :=
    tower_max_factorizable_bound μ p hp hpT hmax (fun x => H x / (c : ℂ))
      (hH.div_const (c : ℂ)) hle
  obtain ⟨b, hb, hbe⟩ := hfac
  refine ⟨fun z => (c : ℂ) * b z, measurable_const.mul hb, ?_⟩
  filter_upwards [hbe] with x hx
  simp only [Function.comp_apply] at hx ⊢
  have hcne : ((c : ℝ) : ℂ) ≠ 0 := by
    rw [ne_eq, Complex.ofReal_eq_zero]; exact ne_of_gt hcpos
  rw [← hx]
  field_simp

/-- At a maximal tower member the identity of `X` factors through the member:
the member is generating. -/
theorem tower_max_generating
    (μ : Measure X) [IsProbabilityMeasure μ]
    (p : X → OrbitSpace K) (hp : Measurable p) (hpT : Tower μ p)
    (hmax : TowerMaximal μ p) :
    ∃ b : OrbitSpace K → X, Measurable b ∧ (id : X → X) =ᵐ[μ] b ∘ p := by
  classical
  obtain ⟨b, hb, hbe⟩ := tower_max_all_factorizable μ p hp hpT hmax
    (fun x => FactorCode.scalar X x) FactorCode.scalar_measurable
    ⟨2, FactorCode.scalar_bound⟩
  refine ⟨FactorCode.scalar_embedding.invFun ∘ b,
    FactorCode.scalar_embedding.measurable_invFun.comp hb, ?_⟩
  filter_upwards [hbe] with x hx
  simp only [Function.comp_apply] at hx ⊢
  rw [← hx]
  exact (FactorCode.scalar_embedding.leftInverse_invFun x).symm

/-! ## The ported maximality and ergodicity theorem (m15 `exists_ergodic_factor`) -/

/-- m15 `exists_tower_maximal`, transcribed. -/
theorem exists_tower_maximal (μ : Measure X) [IsProbabilityMeasure μ] :
    ∃ a : CodedMax.Model (K := K) μ (Tower μ), IsMax a := by
  classical
  refine CodedMax.exists_maximal (K := K) μ (Tower μ) ?_ ?_
  · refine ⟨⟨fun _ => (⟨fun _ => 0⟩ : OrbitSpace K), measurable_const, ?_, Tower.base⟩⟩
    intro k
    exact Filter.Eventually.of_forall fun x => by ext l; rfl
  · intro q _hq _hqe hg hc
    exact Tower.join q hg hc

/-- m15 `exists_ergodic_factor`, transcribed.  Note that the compactness clause
`_hc` produced by `strict_compact_successor` is discarded: the ergodicity conclusion
is obtained from maximality over the over-permissive class alone. -/
theorem exists_ergodic_factor_audit (μ : Measure X) [IsProbabilityMeasure μ]
    [ErgodicSMul K X μ] :
    ∃ p : X → OrbitSpace K, ∃ hp : Measurable p,
      (∀ k : K, ∀ᵐ x ∂μ, p (k • x) = k • p x) ∧ Tower μ p ∧
      TowerMaximal μ p ∧
      ErgodicSMul K (X × X) (RelativeProduct.law μ p hp) := by
  classical
  obtain ⟨a, hamax⟩ := exists_tower_maximal μ
  refine ⟨a.map, a.measurable, a.equivariant, a.good, ?_, ?_⟩
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

/-! ## A maximal tower member has Dirac fibres, so `UniversalGood` fails there -/

section Wild

variable (μ : Measure D) [IsProbabilityMeasure μ]

/-- At a generating factor of a measure on `D`, the relative difference law of the
identity is the Dirac mass at `1`. -/
theorem diffLaw_id_eq_dirac_of_generating
    (p : D → OrbitSpace K) (hp : Measurable p)
    {b : OrbitSpace K → D} (hb : Measurable b) (hid : (id : D → D) =ᵐ[μ] b ∘ p) :
    (DifferenceFourier.differenceLaw (μ.map p) (condDistrib id p μ) : Measure D) =
      Measure.dirac (1 : D) := by
  classical
  haveI : IsProbabilityMeasure (μ.map p) := MeasureTheory.Measure.isProbabilityMeasure_map hp.aemeasurable
  -- the pair law is the graph of `b`
  have hpair : μ.map (fun x => (p x, (id : D → D) x)) =
      (μ.map p) ⊗ₘ Kernel.deterministic b hb := by
    rw [Measure.compProd_deterministic hb,
      Measure.map_map (by fun_prop : Measurable (fun y : OrbitSpace K => (y, b y))) hp]
    refine Measure.map_congr ?_
    filter_upwards [hid] with x hx
    rw [hx]
    simp only [Function.comp_apply]
  -- hence the conditional kernel is deterministic
  have hκ : condDistrib id p μ =ᵐ[μ.map p] Kernel.deterministic b hb :=
    condDistrib_ae_eq_of_measure_eq_compProd_of_measurable hp measurable_id hpair
  -- the product of two deterministic kernels is the deterministic kernel of the pair
  have hprod : (Kernel.deterministic b hb ×ₖ Kernel.deterministic b hb) =
      Kernel.deterministic (fun y => (b y, b y)) (by fun_prop) := by
    ext y s hs
    simp only [Kernel.prod_apply, Kernel.deterministic_apply, Measure.dirac_prod_dirac]
  have hcomp : (condDistrib id p μ ×ₖ condDistrib id p μ) ∘ₘ (μ.map p) =
      (Kernel.deterministic b hb ×ₖ Kernel.deterministic b hb) ∘ₘ (μ.map p) := by
    refine Measure.comp_congr ?_
    filter_upwards [hκ] with y hy
    rw [Kernel.prod_apply, Kernel.prod_apply, hy]
  calc (DifferenceFourier.differenceLaw (μ.map p) (condDistrib id p μ) : Measure D)
      = ((condDistrib id p μ ×ₖ condDistrib id p μ) ∘ₘ (μ.map p)).map
          (fun z : D × D => z.1 / z.2) := rfl
    _ = ((Kernel.deterministic b hb ×ₖ Kernel.deterministic b hb) ∘ₘ (μ.map p)).map
          (fun z : D × D => z.1 / z.2) := by rw [hcomp]
    _ = ((μ.map p).map (fun y => (b y, b y))).map (fun z : D × D => z.1 / z.2) := by
        rw [hprod, Measure.deterministic_comp_eq_map]
    _ = (μ.map p).map (fun _ => (1 : D)) := by
        rw [Measure.map_map (by fun_prop : Measurable (fun z : D × D => z.1 / z.2))
          (by fun_prop : Measurable (fun y : OrbitSpace K => (b y, b y)))]
        exact Measure.map_congr (Filter.Eventually.of_forall fun y => by simp)
    _ = Measure.dirac (1 : D) := by
        rw [Measure.map_const, measure_univ, one_smul]

/-- The `C`-mass of that difference law is `1`, since `1 = j 0 ∈ C`. -/
theorem diffLaw_id_apply_C_of_generating
    (p : D → OrbitSpace K) (hp : Measurable p)
    {b : OrbitSpace K → D} (hb : Measurable b) (hid : (id : D → D) =ᵐ[μ] b ∘ p) :
    DifferenceFourier.differenceLaw (μ.map p) (condDistrib id p μ) C = 1 := by
  rw [diffLaw_id_eq_dirac_of_generating μ p hp hb hid]
  exact Measure.dirac_apply_of_mem C.one_mem

/-- `UniversalGood` fails at every generating factor of a wild measure on `D`. -/
theorem not_universalGood_of_generating (hμ : IsWild μ)
    (p : D → OrbitSpace K) (hp : Measurable p)
    (hid : ∃ b : OrbitSpace K → D, Measurable b ∧ (id : D → D) =ᵐ[μ] b ∘ p) :
    ¬ UniversalGood μ p := by
  intro hg
  obtain ⟨b, hb, hbe⟩ := hid
  have hΔ : DifferenceFourier.differenceLaw (μ.map p) (condDistrib id p μ) C = 0 :=
    hg id measurable_id (fun k => Filter.Eventually.of_forall fun x => rfl) (by simpa using hμ)
  rw [diffLaw_id_apply_C_of_generating μ p hp hb hbe] at hΔ
  exact one_ne_zero hΔ

/-- **Necessary condition on any witness of the terminal obligation.**  At a generating
factor the identity's relative difference law has `C`-mass `1`, so the conclusion of
`GoodId` (equivalently of `UniversalGood` at `d = id`) is false there.  Hence no factor
witnessing `TerminalObligation` can be generating: any candidate must be a *proper*
factor. -/
theorem relDiffLaw_id_ne_zero_of_generating (hμ : IsWild μ)
    (p : D → OrbitSpace K) (hp : Measurable p)
    (hid : ∃ b : OrbitSpace K → D, Measurable b ∧ (id : D → D) =ᵐ[μ] b ∘ p) :
    DifferenceFourier.differenceLaw (μ.map p) (condDistrib id p μ) C ≠ 0 := by
  obtain ⟨b, hb, hbe⟩ := hid
  rw [diffLaw_id_apply_C_of_generating μ p hp hb hbe]
  exact one_ne_zero

/-- **The audit's verdict on m15.**  The hypothesis `hgood` of
`exists_terminal_factor_of_tower_good` is false for every wild `μ` on `D`: the tower
member it is applied to is generating, and `UniversalGood` fails there. -/
theorem hgood_false (hμ : IsWild μ) [ErgodicSMul K D μ] :
    ¬ ∀ (p : D → OrbitSpace K) (hp : Measurable p),
        (∀ k : K, ∀ᵐ x ∂μ, p (k • x) = k • p x) → Tower μ p → TowerMaximal μ p →
        ErgodicSMul K (D × D) (RelativeProduct.law μ p hp) → UniversalGood μ p := by
  intro hgood
  obtain ⟨p, hp, hpe, hpT, hmax, herg⟩ := exists_ergodic_factor_audit μ
  have hg : UniversalGood μ p := hgood p hp hpe hpT hmax herg
  obtain ⟨b, hb, hbe⟩ := tower_max_generating μ p hp hpT hmax
  exact not_universalGood_of_generating μ hμ p hp ⟨b, hb, hbe⟩ hg

end Wild

end PlaneFiveColor.Spectral

end

end OAI
