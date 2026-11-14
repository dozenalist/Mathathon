/-
  TerminalGlue: the exact interface a rerouted terminal-factor argument must supply.

  Machine-checked point: the only property of the terminal factor that the proof of
  `ergodic_wild_fourier` consumes is `GoodId` — relative singularity for the IDENTITY
  map — not `UniversalGood`, which quantifies over every equivariant wild `d`.
  `GoodId` already holds at the point factor (`goodId_const`, one line, by
  `relative_singularity_base`). So the whole content of the terminal-factor argument is:
  transport `GoodId` from the point factor to a factor whose relative square is ergodic.
  Theorem A performs that transport in one step, which is why the UniversalGood induction
  (and the approximation chain that feeds it) can be dropped.
-/
import OAI.Analysis.PlaneSpectrum.Ergodicity

namespace OAI
noncomputable section
open MeasureTheory ProbabilityTheory Filter
namespace PlaneFiveColor.Spectral
open EuclideanFiveColor

variable {Y : Type*} [MeasurableSpace Y]

/-- Relative singularity for the identity map only: the single conjunct of
`exists_terminal_factor` that `ergodic_wild_fourier` uses. -/
def GoodId (mu : Measure D) [IsProbabilityMeasure mu] (p : D → Y) : Prop :=
  DifferenceFourier.differenceLaw (mu.map p) (condDistrib id p mu) C = 0

/-- `UniversalGood` is stronger than `GoodId`. -/
theorem goodId_of_universalGood (mu : Measure D) [IsProbabilityMeasure mu]
    {p : D → Y} (hw : IsWild mu) (h : UniversalGood mu p) : GoodId mu p :=
  h id measurable_id (fun _ => Eventually.of_forall (fun _ => rfl)) (by simpa using hw)

/-- `GoodId` holds at the trivial (point) factor: the base case of the tower. -/
theorem goodId_const (mu : Measure D) [IsProbabilityMeasure mu] (hw : IsWild mu) (y0 : Y) :
    GoodId mu (fun _ => y0) :=
  relative_singularity_base mu id measurable_id y0 (by simpa using hw)

/-- The whole conclusion of `ergodic_wild_fourier`, from `GoodId` plus ergodicity of the
relative square over `p`. No tower, no approximation property. -/
theorem ergodic_wild_fourier_of_goodId
    [StandardBorelSpace Y] [Nonempty Y] [MulAction K Y] [MeasurableConstSMul K Y]
    (mu : Measure D) [IsProbabilityMeasure mu] [ErgodicSMul K D mu]
    (p : D → Y) (hp : Measurable p)
    [ErgodicVAdd Rot (D × D) (RelativeProduct.law mu p hp)]
    (hpe : ∀ k : K, ∀ᵐ d ∂mu, p (k • d) = k • p d)
    (hgood : GoodId mu p) (_hw : IsWild mu) (z : E) (hz : z ≠ 0) :
    ∫ d, (eval z d : ℂ) ∂mu = 0 := by
  have hd : IsWild (DifferenceFourier.differenceLaw (mu.map p) (condDistrib id p mu)) :=
    ⟨relative_difference_invariant mu id p measurable_id hp
      (fun _ => Eventually.of_forall (fun _ => rfl)) hpe, hgood⟩
  exact fourier_vanish_of_terminal mu p hp hpe hd z hz

/-- The exact obligation of an R1/R2/R6-style route, at the codomain the development
already uses for coded factors. Nothing here mentions `UniversalGood`. -/
def TerminalObligation (mu : Measure D) [IsProbabilityMeasure mu] : Prop :=
  ∃ (p : D → OrbitSpace K) (hp : Measurable p),
    (∀ k : K, ∀ᵐ d ∂mu, p (k • d) = k • p d) ∧ GoodId mu p ∧
      ErgodicVAdd Rot (D × D) (RelativeProduct.law mu p hp)

/-- Cost certificate: a factor satisfying `TerminalObligation` gives `ergodic_wild_fourier`
outright. -/
theorem ergodic_wild_fourier_of_terminalObligation
    (mu : Measure D) [IsProbabilityMeasure mu] [ErgodicSMul K D mu]
    (H : TerminalObligation mu) (hw : IsWild mu) (z : E) (hz : z ≠ 0) :
    ∫ d, (eval z d : ℂ) ∂mu = 0 := by
  obtain ⟨p, hp, hpe, hg, herg⟩ := H
  haveI := herg
  exact ergodic_wild_fourier_of_goodId mu p hp hpe hg hw z hz

/-- Non-vacuity: the terminal factor of the existing development discharges
`TerminalObligation`. -/
theorem terminalObligation_of_exists_terminal_factor (mu : Measure D) [IsProbabilityMeasure mu]
    [ErgodicSMul K D mu] (hw : IsWild mu) : TerminalObligation mu := by
  obtain ⟨p, hp, hpe, hgood, hmix⟩ := exists_terminal_factor (X := D) mu
  haveI : ErgodicSMul K (D × D) (RelativeProduct.law mu p hp) := hmix
  exact ⟨p, hp, hpe, goodId_of_universalGood mu hw hgood, inferInstance⟩

end PlaneFiveColor.Spectral
end
end OAI

#print axioms OAI.PlaneFiveColor.Spectral.ergodic_wild_fourier_of_goodId
#print axioms OAI.PlaneFiveColor.Spectral.ergodic_wild_fourier_of_terminalObligation
#print axioms OAI.PlaneFiveColor.Spectral.terminalObligation_of_exists_terminal_factor
