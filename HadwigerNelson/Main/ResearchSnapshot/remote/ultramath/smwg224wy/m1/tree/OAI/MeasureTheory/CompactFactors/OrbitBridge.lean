import OAI.MeasureTheory.CompactFactors.Stationary

/-!
# Where the tree's `Compact` predicate does and does not imply precompact orbits

`CompactFunctions.At μ q H ε` says: there are finitely many fixed functions `Hf`, bounds
`B C`, such that for **each** `k : K` the shift `H (k • ·)` is `ε`-close in `L²(μ)` to a
combination `∑ i, a (q ·) i * Hf i` whose coefficients `a` are `q`-measurable and bounded
by `B` — the coefficients may depend on `k`.

At the **point factor** (`q` constant, so `a (q x)` is one bounded vector in `ℂ^Fin r`)
the family of such combinations is a bounded subset of the finite-dimensional space
`span {Hf i}`, which is totally bounded.  Hence `Compact` at the point factor DOES give
total boundedness of the `K`-orbit of `H`
(`orbit_totallyBounded_of_compact_point`).

At a **non-point** factor it does not: `a` ranges over all `q`-measurable coefficient
functions with `‖a‖ ≤ B`, and `{a * f}` is not totally bounded in `L²` for nonzero `f`.
So `At` is strictly weaker there.  That asymmetry is what makes `(N)` (d3) usable for
`(H2)` at the point factor, and it is why the tower step cannot be composed at the `At`
level (d6).
-/

namespace OAI

noncomputable section

open MeasureTheory ProbabilityTheory
open scoped ENNReal BigOperators

namespace PlaneFiveColor.Spectral
open EuclideanFiveColor

variable {X : Type*} [MeasurableSpace X] [StandardBorelSpace X] [Nonempty X]
  [MulAction K X] [MeasurableConstSMul K X]

/-- Total boundedness of the `K`-orbit of `H` in the `L²(μ)` seminorm. -/
def OrbitTB (μ : Measure X) (H : X → ℂ) : Prop :=
  ∀ ε : ℝ, 0 < ε → ∃ (n : ℕ) (g : Fin n → X → ℂ), (∀ i, Measurable (g i)) ∧
    ∀ k : K, ∃ i, ∫ x, ‖H (k • x) - g i x‖ ^ 2 ∂μ < ε ^ 2

/-- The point factor. -/
def pointFactor (X : Type*) : X → OrbitSpace K := fun _ => ⟨fun _ => 0⟩

lemma pointFactor_apply (x : X) : pointFactor X x = (⟨fun _ => 0⟩ : OrbitSpace K) := rfl

/-- **The bridge.**  At the point factor, the tree's `Compact` predicate implies that the
`K`-orbit of `H` is totally bounded in `L²(μ)`. -/
theorem orbit_totallyBounded_of_compact_point
    (μ : Measure X) [IsProbabilityMeasure μ]
    (H : X → ℂ) (hH : Measurable H)
    (hc : CompactFunctions.Compact (K := K) μ (pointFactor X) H) :
    OrbitTB μ H := by
  classical
  intro ε hε
  have hε2 : 0 < ε / 2 := by linarith
  obtain ⟨r, B, C, Hf, hB, hC, hHfm, hHfb, ha⟩ := hc (ε / 2) hε2
  have hHfC (i : Fin r) (x : X) : ‖Hf i x‖ ≤ C :=
    (Finset.single_le_sum (f := fun i => ‖Hf i x‖) (fun j _ => norm_nonneg _)
      (Finset.mem_univ i)).trans (hHfb x)
  -- the coefficient ball is totally bounded
  have hball : TotallyBounded (Metric.closedBall (0 : Fin r → ℂ) B) :=
    (isCompact_closedBall (0 : Fin r → ℂ) B).totallyBounded
  obtain ⟨t, htfin, htcover⟩ :=
    Metric.totallyBounded_iff.mp hball (ε / (2 * (C + 1))) (by positivity)
  haveI htf : Fintype t := htfin.fintype
  -- net functions indexed by the finite set of coefficient vectors
  let net : t → X → ℂ := fun c x => ∑ i, (c : Fin r → ℂ) i * Hf i x
  refine ⟨Fintype.card t, fun i => net ((Fintype.equivFin t).symm i), ?_, ?_⟩
  · intro i
    exact Finset.measurable_sum _ (fun j _ => measurable_const.mul (hHfm j))
  · intro k
    obtain ⟨a, ham, hab, hai, hae⟩ := ha k
    set c : Fin r → ℂ := a (pointFactor X (Classical.arbitrary X)) with hcdef
    have hconst (x : X) : a (pointFactor X x) = c := by
      rw [hcdef, pointFactor_apply, pointFactor_apply]
    have hcb : c ∈ Metric.closedBall (0 : Fin r → ℂ) B := by
      rw [Metric.mem_closedBall, dist_zero_right]
      exact hab _
    have hmem := htcover hcb
    simp only [Set.mem_iUnion] at hmem
    obtain ⟨d, hd, hcd⟩ := hmem
    rw [Metric.mem_ball, dist_eq_norm] at hcd
    refine ⟨Fintype.equivFin t ⟨d, hd⟩, ?_⟩
    set S : X → ℂ := fun x => ∑ i, c i * Hf i x with hS
    set T : X → ℂ := fun x => ∑ i, d i * Hf i x with hT
    have hTnet : net ⟨d, hd⟩ = T := by
      funext x; rfl
    have hSm : Measurable S := Finset.measurable_sum _ (fun i _ => measurable_const.mul (hHfm i))
    have hTm : Measurable T := Finset.measurable_sum _ (fun i _ => measurable_const.mul (hHfm i))
    -- first error, from `At`
    have h1 : (∫ x, dist (H (k • x)) (S x) ^ 2 ∂μ) < (ε / 2) ^ 2 := by
      have he := hae
      simp only [hconst, hS] at he
      simpa only [dist_eq_norm] using he
    -- second error, from the net
    have h2pt (x : X) : dist (S x) (T x) ^ 2 ≤ (ε / 2) ^ 2 := by
      have hdiff : S x - T x = ∑ i, (c i - d i) * Hf i x := by
        rw [hS, hT, ← Finset.sum_sub_distrib]
        exact Finset.sum_congr rfl fun i _ => by ring
      have hnorm : ‖S x - T x‖ ≤ ‖c - d‖ * C := by
        rw [hdiff]
        exact CompactFunctions.module_bound (c - d) (fun i => Hf i x) (norm_nonneg _)
          le_rfl (hHfb x)
      have hcdC : ‖c - d‖ * C ≤ ε / 2 := by
        have h1 : ‖c - d‖ * C ≤ (ε / (2 * (C + 1))) * C :=
          mul_le_mul_of_nonneg_right hcd.le hC
        have h2 : (ε / (2 * (C + 1))) * C ≤ ε / 2 := by
          have hpos : (0:ℝ) < 2 * (C + 1) := by linarith
          rw [div_mul_eq_mul_div, div_le_iff₀ hpos]
          nlinarith
        linarith
      rw [dist_eq_norm]
      have hnn : 0 ≤ ‖S x - T x‖ := norm_nonneg _
      calc ‖S x - T x‖ ^ 2 ≤ (‖c - d‖ * C) ^ 2 := pow_le_pow_left₀ hnn hnorm 2
        _ ≤ (ε / 2) ^ 2 := by
            apply pow_le_pow_left₀ (by positivity) hcdC
    have h2int : Integrable (fun x => dist (S x) (T x) ^ 2) μ :=
      Integrable.of_bound ((hSm.dist hTm).pow_const 2).aestronglyMeasurable ((ε / 2) ^ 2)
        (Filter.Eventually.of_forall fun x => by
          simpa only [Real.norm_eq_abs, abs_sq] using h2pt x)
    have h2 : (∫ x, dist (S x) (T x) ^ 2 ∂μ) ≤ (ε / 2) ^ 2 := by
      calc (∫ x, dist (S x) (T x) ^ 2 ∂μ) ≤ ∫ _x, (ε / 2) ^ 2 ∂μ :=
            integral_mono h2int (integrable_const _) h2pt
        _ = (ε / 2) ^ 2 := by rw [integral_const, probReal_univ, one_smul]
    -- combine with the triangle inequality for the `L²` seminorm
    have hSm' : Integrable (fun x => dist (H (k • x)) (S x) ^ 2) μ := by
      have hi := hai
      simp only [hconst, hS] at hi
      simpa only [dist_eq_norm] using hi
    have hpt (x : X) : dist (H (k • x)) (T x) ^ 2 ≤
        2 * (dist (H (k • x)) (S x) ^ 2 + dist (S x) (T x) ^ 2) :=
      CompactFunctions.dist_sq_chain _ _ _
    have hmaj : Integrable (fun x => 2 * (dist (H (k • x)) (S x) ^ 2 +
        dist (S x) (T x) ^ 2)) μ := (hSm'.add h2int).const_mul 2
    have hint : Integrable (fun x => dist (H (k • x)) (T x) ^ 2) μ :=
      hmaj.mono' ((((hH.comp (measurable_const_smul k)).dist hTm)).pow_const 2).aestronglyMeasurable
        (Filter.Eventually.of_forall fun x => by
          simpa only [Real.norm_eq_abs, abs_sq] using hpt x)
    have hfin : (∫ x, dist (H (k • x)) (T x) ^ 2 ∂μ) < ε ^ 2 := by
      calc (∫ x, dist (H (k • x)) (T x) ^ 2 ∂μ)
          ≤ ∫ x, 2 * (dist (H (k • x)) (S x) ^ 2 + dist (S x) (T x) ^ 2) ∂μ :=
            integral_mono hint hmaj hpt
        _ = 2 * ((∫ x, dist (H (k • x)) (S x) ^ 2 ∂μ) +
              ∫ x, dist (S x) (T x) ^ 2 ∂μ) := by
            rw [integral_const_mul, integral_add hSm' h2int]
        _ < ε ^ 2 := by nlinarith
    have hidx : (Fintype.equivFin t).symm (Fintype.equivFin t ⟨d, hd⟩) = ⟨d, hd⟩ :=
      Equiv.symm_apply_apply _ _
    simp only [hidx, hTnet]
    simpa only [dist_eq_norm] using hfin

end PlaneFiveColor.Spectral

end

end OAI
