import OAI.Analysis.PlaneSpectrum.TerminalGlue

/-!
# The terminal obligation is satisfied when the point factor already has ergodic
relative product

`TerminalObligation μ` (m7's `TerminalGlue`) asks for a factor `p` that is
`K`-equivariant, satisfies `GoodId μ p` (`C`-nullness of the relative difference law of
the identity) and has ergodic relative product.  Nothing in it asks for a *nontrivial*
factor.

At the point factor:

* `GoodId` is free — `goodId_const`, from `relative_singularity_base`;
* the relative product is `μ.prod μ` — `law_const` below;
* so the obligation is discharged as soon as `μ.prod μ` is ergodic in the relevant
  sense.

This is the "no new mathematics" endpoint of the census: for a wild `μ` whose square is
ergodic, the whole `UniversalGood` propagation zone (harness: 4112 declaration lines) is
dead code, with no `(N)`, no compact tower and no approximation property.
-/

namespace OAI

noncomputable section

open MeasureTheory ProbabilityTheory
open scoped ENNReal

namespace PlaneFiveColor.Spectral
open EuclideanFiveColor

variable {X Y : Type*} [MeasurableSpace X] [StandardBorelSpace X] [Nonempty X]
  [MeasurableSpace Y] [StandardBorelSpace Y] [Nonempty Y]

/-- **The relative product at a constant factor is the square measure.** -/
theorem law_const (μ : Measure X) [IsProbabilityMeasure μ]
    (y₀ : Y) (hy : Measurable (fun _ : X => y₀)) :
    RelativeProduct.law μ (fun _ => y₀) hy = μ.prod μ := by
  classical
  set κ := condDistrib id (fun _ : X => y₀) μ with hκdef
  have hmap : μ.map (fun _ : X => y₀) = Measure.dirac y₀ := by
    rw [Measure.map_const, measure_univ, one_smul]
  have hfib : κ ∘ₘ μ.map (fun _ : X => y₀) = μ :=
    ConditionalFiber.comp_identity_fiber μ (fun _ : X => y₀) hy
  -- the constant conditional kernel, evaluated at `y₀`, is `μ`
  have hκ : κ y₀ = μ := by
    have h1 : κ ∘ₘ Measure.dirac y₀ = μ := by rw [← hmap]; exact hfib
    have h2 : κ ∘ₘ Measure.dirac y₀ = κ y₀ := by
      change Measure.bind (Measure.dirac y₀) ⇑κ = κ y₀
      rw [Measure.dirac_bind (Kernel.measurable _) y₀]
    rw [← h2]; exact h1
  have hstep : ((κ ×ₖ κ) ∘ₘ Measure.dirac y₀) = (κ y₀).prod (κ y₀) := by
    have h1 : ((κ ×ₖ κ) ∘ₘ Measure.dirac y₀) = (κ ×ₖ κ) y₀ := by
      change Measure.bind (Measure.dirac y₀) ⇑(κ ×ₖ κ) = (κ ×ₖ κ) y₀
      rw [Measure.dirac_bind (Kernel.measurable _) y₀]
    rw [h1, Kernel.prod_apply]
  rw [RelativeProduct.law_eq_mixture, hmap, hstep, hκ]

/-- **The terminal obligation holds at the point factor whenever the relative product
there is ergodic.**  No `(N)`, no compact tower, no approximation property: `GoodId` at
the point factor is `relative_singularity_base`. -/
theorem terminalObligation_of_pointFactor_ergodic
    (μ : Measure D) [IsProbabilityMeasure μ] (hw : IsWild μ)
    (h : ErgodicVAdd Rot (D × D)
      (RelativeProduct.law μ (fun _ => (⟨fun _ => 0⟩ : OrbitSpace K)) measurable_const)) :
    TerminalObligation μ := by
  refine ⟨fun _ => (⟨fun _ => 0⟩ : OrbitSpace K), measurable_const, ?_, ?_, ?_⟩
  · intro k
    exact Filter.Eventually.of_forall fun x => by ext l; rfl
  · exact goodId_const μ hw _
  · exact h

/-- **Weak mixing discharges the terminal obligation.**  Here weak mixing is expressed as
ergodicity of the square `μ.prod μ`; `law_const` identifies it with the relative product
at the point factor. -/
theorem terminalObligation_of_square_ergodic
    (μ : Measure D) [IsProbabilityMeasure μ] (hw : IsWild μ)
    (h : ErgodicVAdd Rot (D × D) (μ.prod μ)) :
    TerminalObligation μ := by
  have hlaw : RelativeProduct.law μ (fun _ => (⟨fun _ => 0⟩ : OrbitSpace K)) measurable_const
      = μ.prod μ := law_const μ _ measurable_const
  refine ⟨fun _ => (⟨fun _ => 0⟩ : OrbitSpace K), measurable_const, ?_, ?_, ?_⟩
  · intro k
    exact Filter.Eventually.of_forall fun x => by ext l; rfl
  · exact goodId_const μ hw _
  · rw [hlaw]
    exact h

end PlaneFiveColor.Spectral

end

end OAI
