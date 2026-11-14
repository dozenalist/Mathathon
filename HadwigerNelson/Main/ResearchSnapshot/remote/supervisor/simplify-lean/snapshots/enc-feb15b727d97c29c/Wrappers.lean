/-
  PROPOSED WRAPPERS.  For review; not integrated.

  Both statements below are copied BYTE-FOR-BYTE from the shared originals
  (`ConditionalSpectrum.lean` and `ConditionalLimits.lean`, extracted mechanically by `gen.py`);
  only the proof body is replaced, and only by the corresponding call to
  `uniform_precision_contradiction`.

  The two `Iff.rfl` lemmas are the *definitional-equality certificates* for the aliases:
  if the old definition and the new one are not definitionally the same proposition, these fail to
  elaborate. They are the check that `S := p` and `S := id` reproduce the originals exactly.

  Names carry a `_core` suffix only because the originals are imported in this review file; at
  integration the originals' bodies are replaced and the suffix disappears (the statements, hence
  all call sites such as `finite_uniform_successor_contradiction`, are unchanged).
-/
import EncodingCore
import OAI.Analysis.PlaneSpectrum.ConditionalSpectrum
import OAI.MeasureTheory.CompactFactors.ConditionalLimits

namespace OAI
noncomputable section
open Filter Topology
open MeasureTheory ProbabilityTheory
open scoped ENNReal BigOperators ComplexConjugate
open scoped BigOperators ENNReal

-- The two originals each declare these LOCAL instances (Spectrum:43-44,178-179,260-261;
-- Limits:363-364) and they never leak across files, so the merged file must declare them again.
-- They are the same terms in both sources (`borel Circle`), which is what makes the two statements
-- the same proposition; `Circle` is Mathlib's unit circle with `ω.real : ℝ`.
local instance : MeasurableSpace Circle := borel Circle
local instance : BorelSpace Circle := ⟨rfl⟩

namespace PlaneFiveColor.Spectral
open EuclideanFiveColor
variable {X Y W : Type*} [MeasurableSpace X] [StandardBorelSpace X] [Nonempty X]
  [MeasurableSpace Y] [StandardBorelSpace Y] [Nonempty Y]
  [MeasurableSpace W] [StandardBorelSpace W] [Nonempty W]

/-- Definitional-equality certificate for the finite alias (`S := p`, `Z := Y`). -/
theorem finite_core_iff (μ : Measure X) [IsProbabilityMeasure μ]
    (p : X → Y) (q : Y → W) (b : X → D) (m : ℕ) (γ : ℝ) :
    FiniteEncodingApproximationAt μ p q b m γ
      ↔ FiniteEncodingApproximationAt' μ p q b m γ :=
  Iff.rfl

omit [StandardBorelSpace Y] [Nonempty Y] in

theorem finite_uniform_precision_contradiction
    (μ : Measure X) [IsProbabilityMeasure μ]
    (p : X → Y) (q : Y → W) (b : X → D)
    (hp : Measurable p) (hq : Measurable q) (hb : Measurable b)
    (m : ℕ) (hm : 0 < m) (g : Y → Fin m → D)
    (hg : ∀ᵐ y ∂μ.map p, condDistrib b p μ y =
      (m : ℝ≥0∞)⁻¹ • ∑ i, Measure.dirac (g y i))
    (hwild : IsWild (DifferenceFourier.differenceLaw (μ.map (q ∘ p))
      (condDistrib b (q ∘ p) μ)))
    (ρ c : ℝ) (N : ℕ) (hρ : 0 < ρ) (hc : 0 < c) (hN : 0 < N)
    (harc : ∀ (ω : Measure Circle) [IsProbabilityMeasure ω],
      (∀ n, 0 < n → n ≤ N → ‖∫ w, (w : ℂ)^n ∂ω‖ < c) →
      ω.real {w | ‖(w : ℂ)-1‖ ≤ 4*ρ} < 1/(4*(m : ℝ)^2))
    (happrox : FiniteEncodingApproximationAt μ p q b m (((ρ^m/(m : ℝ))/100)/100)) : False := uniform_precision_contradiction μ p (fun x => q (p x)) (Z := Y) p b
    hp (hq.comp hp) hb m hm g hg hwild ρ c N hρ hc hN harc (finite_core_iff.mp happrox)

/-- Definitional-equality certificate for the ambient alias (`S := id`, `Z := X`). -/
theorem ambient_core_iff (μ : Measure X) [IsProbabilityMeasure μ]
    (p : X → Y) (q : X → W) (b : X → D) (m : ℕ) (γ : ℝ) :
    AmbientEncodingAt μ p q b m γ ↔ AmbientEncodingAt' μ p q b m γ :=
  Iff.rfl

omit [StandardBorelSpace Y] [Nonempty Y] in
theorem ambient_uniform_precision_contradiction
    (μ : Measure X) [IsProbabilityMeasure μ]
    (p : X → Y) (q : X → W) (b : X → D)
    (hp : Measurable p) (hq : Measurable q) (hb : Measurable b)
    (m : ℕ) (hm : 0 < m) (g : Y → Fin m → D)
    (hg : ∀ᵐ y ∂μ.map p, condDistrib b p μ y =
      (m : ℝ≥0∞)⁻¹ • ∑ i, Measure.dirac (g y i))
    (hwild : IsWild (DifferenceFourier.differenceLaw (μ.map (q))
      (condDistrib b (q) μ)))
    (ρ c : ℝ) (N : ℕ) (hρ : 0 < ρ) (hc : 0 < c) (hN : 0 < N)
    (harc : ∀ (ω : Measure Circle) [IsProbabilityMeasure ω],
      (∀ n, 0 < n → n ≤ N → ‖∫ w, (w : ℂ)^n ∂ω‖ < c) →
      ω.real {w | ‖(w : ℂ)-1‖ ≤ 4*ρ} < 1/(4*(m : ℝ)^2))
    (happrox : AmbientEncodingAt μ p q b m (((ρ^m/(m : ℝ))/100)/100)) : False := uniform_precision_contradiction μ p q (Z := X) id b
    hp hq hb m hm g hg hwild ρ c N hρ hc hN harc (ambient_core_iff.mp happrox)

end PlaneFiveColor.Spectral
end
end OAI
