/-
  SIGNATURE-EQUIVALENCE PACKET for the R4 integration.  NOT COMPILED HERE.
  Local-queue check for the frozen R4 pair:
    OAI/Analysis/PlaneSpectrum/ConditionalSpectrum.lean   sha256 d26d5690...
    OAI/MeasureTheory/CompactFactors/ConditionalLimits.lean sha256 24f89dd3...

  WHAT THIS FILE PROVES, AND HOW IT AVOIDS REBUILDING THE ORIGINAL TREE.
  It does not import the pre-patch tree, so no original oleans are needed beyond the 14-module
  immediate closure that R4 already compiles. Instead the two ORIGINAL encoding predicates are
  copied verbatim from the unpatched sources under fresh `Baseline…` names, and:

    (1) `baseline_finite_iff` / `baseline_ambient_iff`  -- `Iff.rfl`. These are DEFINITIONAL
        EQUALITY certificates: they fail to elaborate if the new aliases are not literally the
        old predicates at `S := p` / `S := id`.
    (2) `baseline_finite_uniform_precision_contradiction` / `…_ambient_…` -- the two ORIGINAL
        PUBLIC STATEMENTS, written out with the original binders including the omitted
        `[StandardBorelSpace Y] [Nonempty Y]`, and PROVED by a direct call to the new theorem.
        Elaboration of this call is the statement-preservation certificate: if the `omit` move in
        R3 had re-attached to a different declaration or changed which instance binders appear,
        the call would not typecheck at these binders.
    (3) `#check` lines under `pp.explicit`/`pp.universes` for a textual diff against the
        pre-patch build output (section 4).

  WHY (2) IS THE RIGHT TEST. `finite_uniform_precision_contradiction` is a THEOREM, so it has no
  `def`-body to compare; the only meaning of "the statement is unchanged" that Lean can check is
  "the old hypothesis type is accepted where the new one is expected, at the old binders". That
  is exactly what (2) does, and it is stronger than a `#check` print because it also settles the
  `omit` question.

  RUN (from the repo root, after the R4 pair is compiled into a private olean dir that precedes
  lean/build/lib on LEAN_PATH):

      source scripts/env4341.sh
      LEAN_PATH="$OUT:$LEAN_PATH" lean supervisor/simplify-lean/lean/SignatureEquivalence.lean

  Expected: no errors. `#print axioms` of the two baselines must be a SUBSET of
  {propext, Classical.choice, Quot.sound} -- they are wrappers, so expect a small set.
-/

import OAI.Analysis.PlaneSpectrum.ConditionalSpectrum
import OAI.MeasureTheory.CompactFactors.ConditionalLimits

namespace OAI
noncomputable section
open Filter Topology
open MeasureTheory ProbabilityTheory
open EuclideanFiveColor
open PlaneFiveColor.Spectral
open scoped ENNReal BigOperators ComplexConjugate

-- Both patched modules declare these `local`, so they do not escape; redeclare the same terms
-- (this is the same pair the originals use, `borel Circle` / `⟨rfl⟩`).
local instance : MeasurableSpace Circle := borel Circle
local instance : BorelSpace Circle := ⟨rfl⟩

namespace SignatureCheck

variable {X Y W : Type*} [MeasurableSpace X] [StandardBorelSpace X] [Nonempty X]
  [MeasurableSpace Y] [StandardBorelSpace Y] [Nonempty Y]
  [MeasurableSpace W] [StandardBorelSpace W] [Nonempty W]

/-! ## 1. The ORIGINAL encoding predicates, copied verbatim under baseline names.
  Source: pre-patch `ConditionalSpectrum.lean:266-280` (finite) and
  `ConditionalLimits.lean:369-382` (ambient). Text unaltered apart from the name. -/

/-- Pre-patch `FiniteEncodingApproximationAt`, verbatim. -/
def BaselineFiniteEncodingApproximationAt (μ : Measure X) [IsProbabilityMeasure μ]
    (p : X → Y) (q : Y → W) (b : X → D) (m : ℕ) (γ : ℝ) : Prop :=
  ∃ (r : ℕ) (B C : ℝ) (H : Fin r → Y → Fin m → ℂ),
    0 ≤ B ∧ 0 ≤ C ∧ (∀ y, ∑ i, ‖H i y‖ ≤ C) ∧
    ∀ k : K, ∃ coeff : W → Fin r → ℂ,
      (∀ w, ‖coeff w‖ ≤ B) ∧
      Integrable (fun x => dist
        (PhaseEncoding.kernelEncoding (condDistrib b p μ)
          (fun d => (eval (kCoeff k) d : ℂ)) m (p x))
        (∑ i, coeff (q (p x)) i • H i (p x)) ^ 2) μ ∧
      (∫ x, dist
        (PhaseEncoding.kernelEncoding (condDistrib b p μ)
          (fun d => (eval (kCoeff k) d : ℂ)) m (p x))
        (∑ i, coeff (q (p x)) i • H i (p x)) ^ 2 ∂μ) < γ^2

/-- Pre-patch `AmbientEncodingAt`, verbatim. -/
def BaselineAmbientEncodingAt (μ : Measure X) [IsProbabilityMeasure μ]
    (p : X → Y) (q : X → W) (b : X → D) (m : ℕ) (γ : ℝ) : Prop :=
  ∃ (r : ℕ) (B C : ℝ) (H : Fin r → X → Fin m → ℂ),
    0 ≤ B ∧ 0 ≤ C ∧ (∀ y, ∑ i, ‖H i y‖ ≤ C) ∧
    ∀ k : K, ∃ coeff : W → Fin r → ℂ,
      (∀ w, ‖coeff w‖ ≤ B) ∧
      Integrable (fun x => dist
        (PhaseEncoding.kernelEncoding (condDistrib b p μ)
          (fun d => (eval (kCoeff k) d : ℂ)) m (p x))
        (∑ i, coeff (q x) i • H i x) ^ 2) μ ∧
      (∫ x, dist
        (PhaseEncoding.kernelEncoding (condDistrib b p μ)
          (fun d => (eval (kCoeff k) d : ℂ)) m (p x))
        (∑ i, coeff (q x) i • H i x) ^ 2 ∂μ) < γ^2

/-! ## 2. Definitional equality with the new aliases.
  `Iff.rfl` is the check: it demands the two sides be definitionally equal. -/

theorem baseline_finite_iff (μ : Measure X) [IsProbabilityMeasure μ]
    (p : X → Y) (q : Y → W) (b : X → D) (m : ℕ) (γ : ℝ) :
    BaselineFiniteEncodingApproximationAt μ p q b m γ
      ↔ PlaneFiveColor.Spectral.FiniteEncodingApproximationAt μ p q b m γ :=
  Iff.rfl

theorem baseline_ambient_iff (μ : Measure X) [IsProbabilityMeasure μ]
    (p : X → Y) (q : X → W) (b : X → D) (m : ℕ) (γ : ℝ) :
    BaselineAmbientEncodingAt μ p q b m γ
      ↔ PlaneFiveColor.Spectral.AmbientEncodingAt μ p q b m γ :=
  Iff.rfl

/-! ## 3. The ORIGINAL public statements, proved from the new theorems.
  Binders and hypotheses are those of the pre-patch files, including the `omit` of
  `[StandardBorelSpace Y] [Nonempty Y]`; the new module-level variables above are deliberately
  NOT omitted here, which makes this the stricter direction: the theorem must be callable with
  the full instance set and with the old hypothesis. -/

omit [StandardBorelSpace Y] [Nonempty Y] in
theorem baseline_finite_uniform_precision_contradiction
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
    (happrox : BaselineFiniteEncodingApproximationAt μ p q b m
      (((ρ^m/(m : ℝ))/100)/100)) : False :=
  PlaneFiveColor.Spectral.finite_uniform_precision_contradiction μ p q b hp hq hb m hm g hg
    hwild ρ c N hρ hc hN harc happrox

omit [StandardBorelSpace Y] [Nonempty Y] in
theorem baseline_ambient_uniform_precision_contradiction
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
    (happrox : BaselineAmbientEncodingAt μ p q b m
      (((ρ^m/(m : ℝ))/100)/100)) : False :=
  PlaneFiveColor.Spectral.ambient_uniform_precision_contradiction μ p q b hp hq hb m hm g hg
    hwild ρ c N hρ hc hN harc happrox

end SignatureCheck

/-! ## 4. Implicit-binder display checks (`omit` inspection).
  Diff these against the same lines taken from the PRE-PATCH 83-module build. The question they
  answer: does `[StandardBorelSpace Y]` / `[Nonempty Y]` still appear as an implicit instance
  binder of the public theorems, or did the `omit` move pull it in? -/

set_option pp.explicit true in
set_option pp.universes true in
#check @PlaneFiveColor.Spectral.finite_uniform_precision_contradiction

set_option pp.explicit true in
set_option pp.universes true in
#check @PlaneFiveColor.Spectral.ambient_uniform_precision_contradiction

/-! Axiom footprint of the two baseline wrappers: expected to be a SUBSET of
{propext, Classical.choice, Quot.sound}. Any `sorryAx` means a baseline was admitted. -/

#print axioms SignatureCheck.baseline_finite_uniform_precision_contradiction
#print axioms SignatureCheck.baseline_ambient_uniform_precision_contradiction

/-! ## 5. What sections 1-3 do and do NOT establish (read before trusting a green run).

  Proves:
    * the new aliases are DEFINITIONALLY the old predicates (1-2), including `S := id` for the
      ambient case -- if `H i (id x)` were not reducible to `H i x`, `baseline_ambient_iff` fails;
    * the two ORIGINAL public statements are derivable from the R4 theorems at the original
      binders (3), so no hypothesis was dropped or strengthened and the old `happrox` is accepted.

  Does NOT prove, on its own:
    * that the public theorems gained NO extra implicit binder. Section 3 lives inside the
      module's `variable` block, so an added `[StandardBorelSpace Y]` argument would be filled
      automatically and the call would still succeed. An added binder is detected ONLY by the
      textual `#check` diff in section 4 against the pre-patch build output.
    * anything about the 82-module downstream elaboration; that is the full build's job.
  Both checks are needed; neither alone is sufficient. State both when reporting. -/

end
end OAI

#print axioms OAI.SignatureCheck.baseline_finite_iff
#print axioms OAI.SignatureCheck.baseline_ambient_iff
