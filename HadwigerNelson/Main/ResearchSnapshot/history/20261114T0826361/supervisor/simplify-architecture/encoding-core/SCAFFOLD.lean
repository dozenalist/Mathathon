/-
  UNCOMPILED SCAFFOLD — DO NOT ADD TO THE BUILD.
  ================================================
  Companion to PLAN.md. This file was never elaborated: no `lean`/`lake` invocation was made, and
  it contains exactly one `sorry`, which stands for the *verbatim transplant* of the 153-line proof
  body of `finite_uniform_precision_contradiction` (ConditionalSpectrum.lean:324-476) with the 7 edits
  listed in PLAN.md §6. Nothing here is proved, and the `sorry` must be replaced, not kept.

  Placement (measured, PLAN.md §2): the general definition and theorem belong in
  `lean/OAI/Analysis/PlaneSpectrum/ConditionalSpectrum.lean` (namespace `PlaneFiveColor.Spectral`),
  because `closure(ConditionalLimits) ∋ ConditionalSpectrum` and not conversely. The wrapper for the
  ambient theorem goes in `lean/OAI/MeasureTheory/CompactFactors/ConditionalLimits.lean`.
-/
import OAI.Analysis.PlaneSpectrum.FourierTests
import OAI.Analysis.PlaneSpectrum.SmallArcs
import OAI.MeasureTheory.CompactFactors.ConditionalSelection

namespace OAI
noncomputable section
open MeasureTheory ProbabilityTheory
open scoped ENNReal BigOperators ComplexConjugate

namespace PlaneFiveColor.Spectral

variable {K X Y W : Type*} [SMul K X] [MeasurableSpace X] [MeasurableSpace Y]
  [MeasurableSpace W]

/-! ### 1. The shared encoding hypothesis

`S : X → Z` is the read-out map: the approximating family lives on `Z` and is sampled at `S x`.
`P : X → W` is the factor map whose coefficients are used. The two existing definitions are the
instances `S := p` and `S := id`. -/
def EncodingApproximationAt (μ : Measure X) [IsProbabilityMeasure μ]
    (p : X → Y) (P : X → W) {Z : Type*} (S : X → Z)
    (b : X → D) (m : ℕ) (γ : ℝ) : Prop :=
  ∃ (r : ℕ) (B C : ℝ) (H : Fin r → Z → Fin m → ℂ),
    0 ≤ B ∧ 0 ≤ C ∧ (∀ z, ∑ i, ‖H i z‖ ≤ C) ∧
    ∀ k : K, ∃ coeff : W → Fin r → ℂ,
      (∀ w, ‖coeff w‖ ≤ B) ∧
      Integrable (fun x => dist
        (PhaseEncoding.kernelEncoding (condDistrib b p μ)
          (fun d => (eval (kCoeff k) d : ℂ)) m (p x))
        (∑ i, coeff (P x) i • H i (S x)) ^ 2) μ ∧
      (∫ x, dist
        (PhaseEncoding.kernelEncoding (condDistrib b p μ)
          (fun d => (eval (kCoeff k) d : ℂ)) m (p x))
        (∑ i, coeff (P x) i • H i (S x)) ^ 2 ∂μ) < γ^2

/-- Definitional alias for the *old* `FiniteEncodingApproximationAt` (PLAN.md §3). -/
abbrev FiniteEncodingApproximationAt' (μ : Measure X) [IsProbabilityMeasure μ]
    (p : X → Y) (q : Y → W) (b : X → D) (m : ℕ) (γ : ℝ) : Prop :=
  EncodingApproximationAt μ p (fun x => q (p x)) p b m γ

/-- Definitional alias for the *old* `AmbientEncodingAt`; lives in `ConditionalLimits`. -/
abbrev AmbientEncodingAt' (μ : Measure X) [IsProbabilityMeasure μ]
    (p : X → Y) (q : X → W) (b : X → D) (m : ℕ) (γ : ℝ) : Prop :=
  EncodingApproximationAt μ p q id b m γ

/-! ### 2. The common theorem

Statement identical to both existing theorems after substituting `P := q ∘ p, S := p` and
`P := q, S := id`. No hypothesis added, dropped or strengthened; `hwild` stays a hypothesis at `P`
(the difference law's wildness is **not** derived and **not** hidden as a new premise). -/
theorem uniform_precision_contradiction
    (μ : Measure X) [IsProbabilityMeasure μ]
    (p : X → Y) (P : X → W) {Z : Type*} (S : X → Z) (b : X → D)
    (hp : Measurable p) (hP : Measurable P) (hb : Measurable b)
    (m : ℕ) (hm : 0 < m) (g : Y → Fin m → D)
    (hg : ∀ᵐ y ∂μ.map p, condDistrib b p μ y =
      (m : ℝ≥0∞)⁻¹ • ∑ i, Measure.dirac (g y i))
    (hwild : IsWild (DifferenceFourier.differenceLaw (μ.map P)
      (condDistrib b P μ)))
    (ρ c : ℝ) (N : ℕ) (hρ : 0 < ρ) (hc : 0 < c) (hN : 0 < N)
    (harc : ∀ (ω : Measure Circle) [IsProbabilityMeasure ω],
      (∀ n, 0 < n → n ≤ N → ‖∫ w, (w : ℂ)^n ∂ω‖ < c) →
      ω.real {w | ‖(w : ℂ)-1‖ ≤ 4*ρ} < 1/(4*(m : ℝ)^2))
    (happrox : EncodingApproximationAt μ p P S b m (((ρ^m/(m : ℝ))/100)/100)) :
    False := by
  classical
  -- TRANSPLANT, verbatim, from `finite_uniform_precision_contradiction` (lines 324-476), with:
  --   (1) delete  `let P : X → W := q ∘ p`
  --   (2) delete  `have hP : Measurable P := hq.comp hp`
  --   (3)(4)(5)(6)(7) rewrite the 6 sites `H ?_ (p x)` → `H ?_ (S x)` and `hH (p x)` → `hH (S x)`
  --       (PLAN.md §6 lists them individually).
  sorry

/-! ### 3. Wrappers (each keeps its module's existing statement byte-for-byte)

In `ConditionalSpectrum.lean`, replacing the current proof body:

```lean
theorem finite_uniform_precision_contradiction
    (μ : Measure X) [IsProbabilityMeasure μ]
    (p : X → Y) (q : Y → W) (b : X → D)
    (hp : Measurable p) (hq : Measurable q) (hb : Measurable b)
    (m : ℕ) (hm : 0 < m) (g : Y → Fin m → D)
    (hg : …) (hwild : IsWild (DifferenceFourier.differenceLaw (μ.map (q ∘ p))
      (condDistrib b (q ∘ p) μ)))
    (ρ c : ℝ) (N : ℕ) (hρ : 0 < ρ) (hc : 0 < c) (hN : 0 < N)
    (harc : …) (happrox : FiniteEncodingApproximationAt μ p q b m (((ρ^m/(m : ℝ))/100)/100)) :
    False :=
  uniform_precision_contradiction μ p (fun x => q (p x)) (Z := Y) p b
    hp (hq.comp hp) hb m hm g hg hwild ρ c N hρ hc hN harc happrox
```

In `ConditionalLimits.lean`:

```lean
theorem ambient_uniform_precision_contradiction
    (μ : Measure X) [IsProbabilityMeasure μ]
    (p : X → Y) (q : X → W) (b : X → D)
    (hp : Measurable p) (hq : Measurable q) (hb : Measurable b)
    (m : ℕ) (hm : 0 < m) (g : Y → Fin m → D)
    (hg : …) (hwild : IsWild (DifferenceFourier.differenceLaw (μ.map q)
      (condDistrib b q μ)))
    (ρ c : ℝ) (N : ℕ) (hρ : 0 < ρ) (hc : 0 < c) (hN : 0 < N)
    (harc : …) (happrox : AmbientEncodingAt μ p q b m (((ρ^m/(m : ℝ))/100)/100)) :
    False :=
  uniform_precision_contradiction μ p q (Z := X) id b
    hp hq hb m hm g hg hwild ρ c N hρ hc hN harc happrox
```

Call sites that must keep working unchanged:
* `finite_uniform_successor_contradiction` (`ConditionalSpectrum.lean:479`) calls the finite theorem
  positionally — signature preserved, so no edit.
* the `CompactApproximation.At → AmbientEncodingAt` conversion (`ConditionalLimits.lean:592`) does
  `refine ⟨r, B, C, Hf, hB, hC, hHf, ?_⟩`: the general definition has the same four existential
  components (`S` and `P` are parameters), so the constructor arity is preserved.
-/

end PlaneFiveColor.Spectral
end
end OAI
