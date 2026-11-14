/-
  FRESH-CONTEXT SIGNATURE TEST.  NOT COMPILED HERE.  Resolves the limitation recorded in
  SignatureEquivalence.lean section 5.

  THE LIMITATION.  SignatureEquivalence section 3 reproved the old statements inside a module that
  declared `variable [StandardBorelSpace Y] [Nonempty Y]`. Inside such a block an implicit instance
  argument is filled silently from the section variable, so an ADDED binder on the public theorem
  would not have been detected -- it would have been discharged for free.

  THE FIX, AND WHY IT NEEDS NO BINDER-ORDER KNOWLEDGE.
  This file declares NO section variables. `Y`'s `StandardBorelSpace` and `Nonempty` are introduced
  as PLAIN hypotheses `(sbY : …) (neY : …)`, never as `[...]` instance binders. A plain hypothesis is
  not in Lean's instance cache, so the elaborator CANNOT synthesize `StandardBorelSpace Y` or
  `Nonempty Y` from them. The two theorems are then applied with only their explicit arguments.
  Therefore:
    * if the public theorem still omits those two instances (the pre-patch situation), it never asks
      for them and the application succeeds;
    * if a repair (e.g. the R3 `omit` move) re-attached them as binders, the elaborator must find
      `[StandardBorelSpace Y]` / `[Nonempty Y]` and will FAIL, because `sbY`/`neY` are not instances.
  The failure is therefore a positive detection, not a false alarm.

  POSITIVE CONTROL.  `control_finite` is the same application with `letI : StandardBorelSpace Y := sbY`
  and `letI : Nonempty Y := neY` supplied. It must succeed even in the failure case above, so a failure
  of BOTH tests points at my own hypothesis text rather than at the theorem. Read the pair together:
      fresh fails, control succeeds  -> the theorem BINDS the omitted instances (regression);
      both succeed                   -> the omission is intact (desired);
      both fail                      -> the test file is wrong, not the theorem.

  RUN (repo root, after the R4 pair is compiled into a private olean dir preceding lean/build/lib):
      source scripts/env4341.sh
      LEAN_PATH="$OUT:$LEAN_PATH" lean supervisor/simplify-lean/lean/SignatureCheckFresh.lean
-/

import OAI.Analysis.PlaneSpectrum.ConditionalSpectrum
import OAI.MeasureTheory.CompactFactors.ConditionalLimits

namespace OAI
noncomputable section
open Filter Topology
open MeasureTheory ProbabilityTheory
open EuclideanFiveColor
open scoped ENNReal BigOperators ComplexConjugate

set_option autoImplicit false

-- the patched modules declare these `local`; redeclare the same terms.
local instance : MeasurableSpace Circle := borel Circle
local instance : BorelSpace Circle := ⟨rfl⟩

namespace SignatureFresh

/-! ## 1. FROZEN CONTROL: the FINITE theorem, with `Y`'s two instances available.

  Expected: succeeds. If this fails, the hypothesis text below is wrong; nothing else in the file is
  meaningful until it passes. -/

theorem control_finite
    {X Y W : Type*} [MeasurableSpace X] [StandardBorelSpace X] [Nonempty X]
    [MeasurableSpace Y] [MeasurableSpace W] [StandardBorelSpace W] [Nonempty W]
    (sbY : StandardBorelSpace Y) (neY : Nonempty Y)
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
    (happrox : PlaneFiveColor.Spectral.FiniteEncodingApproximationAt μ p q b m
      (((ρ^m/(m : ℝ))/100)/100)) : False := by
  letI : StandardBorelSpace Y := sbY
  letI : Nonempty Y := neY
  exact PlaneFiveColor.Spectral.finite_uniform_precision_contradiction μ p q b hp hq hb
    m hm g hg hwild ρ c N hρ hc hN harc happrox

/-! ## 2. THE TEST: the same application with `sbY`/`neY` NOT registered as instances.

  Expected: succeeds if and only if the public theorem still omits `[StandardBorelSpace Y]` and
  `[Nonempty Y]`. The `_sbY`/`_neY` arguments exist only to keep the two hypotheses in scope as plain
  terms; they are deliberately never bound with `letI`. -/

theorem fresh_finite
    {X Y W : Type*} [MeasurableSpace X] [StandardBorelSpace X] [Nonempty X]
    [MeasurableSpace Y] [MeasurableSpace W] [StandardBorelSpace W] [Nonempty W]
    (_sbY : StandardBorelSpace Y) (_neY : Nonempty Y)
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
    (happrox : PlaneFiveColor.Spectral.FiniteEncodingApproximationAt μ p q b m
      (((ρ^m/(m : ℝ))/100)/100)) : False :=
  PlaneFiveColor.Spectral.finite_uniform_precision_contradiction μ p q b hp hq hb
    m hm g hg hwild ρ c N hρ hc hN harc happrox

/-! ## 3. Same pair for the AMBIENT theorem (`ConditionalLimits`).

  The ambient original omits the same two instances, so it gets the same treatment. Note `Y` still
  occurs in the statement through `p` and `g`, so `[MeasurableSpace Y]` stays a real binder. -/

theorem control_ambient
    {X Y W : Type*} [MeasurableSpace X] [StandardBorelSpace X] [Nonempty X]
    [MeasurableSpace Y] [MeasurableSpace W] [StandardBorelSpace W] [Nonempty W]
    (sbY : StandardBorelSpace Y) (neY : Nonempty Y)
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
    (happrox : PlaneFiveColor.Spectral.AmbientEncodingAt μ p q b m
      (((ρ^m/(m : ℝ))/100)/100)) : False := by
  letI : StandardBorelSpace Y := sbY
  letI : Nonempty Y := neY
  exact PlaneFiveColor.Spectral.ambient_uniform_precision_contradiction μ p q b hp hq hb
    m hm g hg hwild ρ c N hρ hc hN harc happrox

theorem fresh_ambient
    {X Y W : Type*} [MeasurableSpace X] [StandardBorelSpace X] [Nonempty X]
    [MeasurableSpace Y] [MeasurableSpace W] [StandardBorelSpace W] [Nonempty W]
    (_sbY : StandardBorelSpace Y) (_neY : Nonempty Y)
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
    (happrox : PlaneFiveColor.Spectral.AmbientEncodingAt μ p q b m
      (((ρ^m/(m : ℝ))/100)/100)) : False :=
  PlaneFiveColor.Spectral.ambient_uniform_precision_contradiction μ p q b hp hq hb
    m hm g hg hwild ρ c N hρ hc hN harc happrox

/-! ## 4. Axiom footprint of the four tests (wrappers; expect a small subset). -/

#print axioms SignatureFresh.control_finite
#print axioms SignatureFresh.fresh_finite
#print axioms SignatureFresh.control_ambient
#print axioms SignatureFresh.fresh_ambient

end SignatureFresh
end
end OAI
