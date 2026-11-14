import C

/-!
# The terminal factor's obligation in its weakest form

`sprint/simplify/stage/lean/OAI/Analysis/PlaneSpectrum/Ergodicity.lean:54`
(`ergodic_wild_fourier`) is the only consumer of `exists_terminal_factor` in the
whole tree.  It uses it at exactly one place, `Ergodicity.lean:58`,

  `exact hgood id measurable_id (fun k => Eventually.of_forall (fun d => rfl)) (by simpa using hw)`

i.e. at the single instance `d = id` of `UniversalGood`.  What that line needs is

  `DifferenceFourier.differenceLaw (μ.map q) (condDistrib id q μ) C = 0`,

and by m5's Theorem A (`RelativeSingularity.relative_singularity_of_ergodic`,
`.ultramath/smwfoekgk/m5/work/C.lean`) that follows from two properties of `q`:

* `ErgodicSMul K (D × D) (RelativeProduct.law μ q hq)`  -- the ergodic relative square;
* `¬ ∀ᵐ z ∂(RelativeProduct.law μ q hq), z.1 = z.2`      -- the relative product is
  not carried by the diagonal ("`q` is proper").

So the *whole* obligation of the R1 restructure is the single predicate
`TerminalObligation μ` below: no `UniversalGood`, no quantification over wild
equivariant `d`, no propagation.  This file records that reduction, and nothing
about how the obligation is met.  Note that `exists_terminal_factor` supplies a
strictly stronger conclusion (`UniversalGood`, i.e. the statement for every wild
equivariant `d`), which is what makes the deletion zone of the R1 measurement
appear in the proof-term closure at all.
-/

namespace OAI

noncomputable section

open MeasureTheory ProbabilityTheory Filter
open scoped ENNReal

namespace PlaneFiveColor.Spectral
open EuclideanFiveColor

/-- The weakest form of what the terminal-factor construction has to deliver: a
measurable equivariant factor whose relative square is ergodic and whose relative
product is not carried by the diagonal. -/
def TerminalObligation (μ : Measure D) [IsProbabilityMeasure μ] : Prop :=
  ∃ (q : D → OrbitSpace K) (hq : Measurable q),
    (∀ k : K, ∀ᵐ d ∂μ, q (k • d) = k • q d) ∧
    ErgodicSMul K (D × D) (EuclideanFiveColor.RelativeProduct.law μ q hq) ∧
    ¬ ∀ᵐ z ∂(EuclideanFiveColor.RelativeProduct.law μ q hq), z.1 = z.2

/-- **`TerminalObligation` replaces `exists_terminal_factor` for the whole tree.**
This is the statement that `Ergodicity.lean:54` proves from `exists_terminal_factor`;
here it is proved from `TerminalObligation` alone, via m5's Theorem A at `d = id`. -/
theorem ergodic_wild_fourier_of_obligation (μ : Measure D) [IsProbabilityMeasure μ]
    [ErgodicSMul K D μ] (h : TerminalObligation μ) (z : E) (hz : z ≠ 0) :
    ∫ d, (eval z d : ℂ) ∂μ = 0 := by
  obtain ⟨q, hq, hqc, herg, hdiag⟩ := h
  have hC : EuclideanFiveColor.DifferenceFourier.differenceLaw (μ.map q)
      (condDistrib id q μ) C = 0 :=
    RelativeSingularity.relative_singularity_of_ergodic μ q hq id measurable_id
      (fun k x => rfl) hdiag
  have hd : IsWild (EuclideanFiveColor.DifferenceFourier.differenceLaw (μ.map q)
      (condDistrib id q μ)) :=
    ⟨relative_difference_invariant μ id q measurable_id hq
      (fun k => Filter.Eventually.of_forall (fun d => rfl)) hqc, hC⟩
  exact fourier_vanish_of_terminal μ q hq hqc hd z hz

end PlaneFiveColor.Spectral

end

end OAI
