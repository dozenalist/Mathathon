/-  Smoke root for the dedup candidate. UNCOMPILED here (no build ran in this block).

    Run after applying 0001-kernels-norm-integral-sq.patch to a private copy of the tree:
      LEAN_PATH="<private lib>" lean SmokeNames.lean
    Expected: no errors, and every `#print axioms` prints [propext, Classical.choice, Quot.sound].

    What this file checks, in order:
      1. BOTH public names still exist (no API break);
      2. they have the SAME TYPE (the statement is unchanged to the character);
      3. the three known consumers' enclosing lemmas still carry clean axioms.

    WITHDRAWN CLAIM: an earlier version also asserted `KernelCompact.norm_integral_sq … =
    ProbabilityL2.norm_integral_sq …` by `rfl` and described that as certifying "the same proof
    object". That claim is void: Lean proof irrelevance makes ANY two proofs of the same proposition
    definitionally equal, so such an `rfl` holds for every pair of proofs of that statement and
    witnesses nothing about the implementations. What IS true is a source-level fact, checkable only
    by reading: the wrapper's body is the term `…ProbabilityL2.norm_integral_sq μ f hf hf₂`, so the
    implementation is that application. Type identity plus the source reading is the whole content;
    there is no `rfl`-level implementation-identity certificate.
-/
import OAI.MeasureTheory.CompactFactors.Functions

namespace OAI
open MeasureTheory

-- (1) both names exist, both from the leaf copy and from the wrapper
#check @EuclideanFiveColor.ProbabilityL2.norm_integral_sq
#check @EuclideanFiveColor.KernelCompact.norm_integral_sq

-- (2) same statement ...
example : (∀ (X : Type*) [MeasurableSpace X] (μ : Measure X) [IsProbabilityMeasure μ]
    (f : X → ℂ) (hf : Integrable f μ) (hf₂ : Integrable (fun x => ‖f x‖^2) μ),
    ‖∫ x, f x ∂μ‖^2 ≤ ∫ x, ‖f x‖^2 ∂μ) :=
  @EuclideanFiveColor.ProbabilityL2.norm_integral_sq

-- (2b) same type: the wrapper's type is the leaf lemma's type, by `#check` comparison above.
-- NOTE: do NOT add an `… = … := rfl` line here. Proof irrelevance makes it trivially true for any
-- two proofs of the statement, so it certifies nothing (see the header). Implementation identity is a
-- source fact: the wrapper body is exactly `…ProbabilityL2.norm_integral_sq μ f hf hf₂`.

-- (3) axioms of the two names themselves
#print axioms EuclideanFiveColor.ProbabilityL2.norm_integral_sq
#print axioms EuclideanFiveColor.KernelCompact.norm_integral_sq

-- (3) axioms of the three consumers (their bodies are unchanged by the patch)
#print axioms EuclideanFiveColor.KernelCompact.fiberMean_l2_bound      -- Kernels.lean:78,  uses the name at :101
#print axioms EuclideanFiveColor.BoundedMeasurable.conditional_norm_l2_le -- BoundedFunctions.lean:202, uses it at :211
#print axioms EuclideanFiveColor.CompactFunctions.compact_descend      -- Functions.lean:803, uses it at :875
end OAI
