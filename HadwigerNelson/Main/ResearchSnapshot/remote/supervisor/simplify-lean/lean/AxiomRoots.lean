/-
  AXIOM-ROOT FILE -- R3 revision.  Analysis only: this file has NOT been compiled here.

  FROZEN INPUTS (do not chase later revisions):
    lean/OAI/Analysis/PlaneSpectrum/ConditionalSpectrum.lean   R3 sha256 d26d5690...
      (R2 frozen copy in ../snapshots/integ-48aa378f6f6db82b/ sha256 48aa378f...)
    lean/OAI/MeasureTheory/CompactFactors/ConditionalLimits.lean R3 sha256 fed6e99a...
      (R2 copy sha256 58707f04...)

  ACCEPTANCE. Each printed axiom set must be a SUBSET of
    {propext, Classical.choice, Quot.sound}.
  Subsets are normal and accepted -- do not demand all three. `sorryAx`, or any other name,
  is a FAILURE. Gate: ../../axiom_gate.py.

  STRUCTURE. Part A is the AFFECTED claim: everything whose proof or statement the edit can
  reach (the 19 reverse-dependent modules of BUILD-PLAN.json). Part B is OPTIONAL and kept
  separate on purpose: the chi <= 7 roots are NOT reverse-dependent on the edit, so printing
  them inside Part A would let an unaffected result inflate the dependency claim.
-/

import OAI.Analysis.PlaneSpectrum.ConditionalSpectrum
import OAI.MeasureTheory.CompactFactors.ConditionalLimits
import OAI.MeasureTheory.CompactFactors.Approximation
import OAI.Geometry.PlaneColoring.Five

/-! # PART A -- affected surface -/

/-! ## A1. The changed surface: the common core and the two rewritten wrappers -/

#print axioms OAI.PlaneFiveColor.Spectral.uniform_precision_contradiction
#print axioms OAI.PlaneFiveColor.Spectral.finite_uniform_precision_contradiction
#print axioms OAI.PlaneFiveColor.Spectral.ambient_uniform_precision_contradiction

/-! ## A2. Nearest consumers, fully qualified

  `finite_uniform_successor_contradiction` is the only in-module consumer of the finite root.
  `relative_singularity_successor` (Approximation.lean:384, call at 413-414) is the nearest
  cross-module consumer and applies the finite statement positionally -- it is the strongest
  available statement-preservation test.  `relative_singularity_approximation`
  (ConditionalLimits.lean:463, call at 501) is the nearest consumer of the ambient root. -/

#print axioms OAI.PlaneFiveColor.Spectral.finite_uniform_successor_contradiction
#print axioms OAI.PlaneFiveColor.Spectral.relative_singularity_successor
#print axioms OAI.PlaneFiveColor.Spectral.relative_singularity_approximation

/-! ## A3. The affected public root: chi(R^2) >= 6.
  `Five` (build order 72) IS reverse-dependent on the edits. -/

#print axioms OAI.EuclideanFiveColor.no_proper_five_coloring

/-! ## A4. EXACT STATEMENT PRESERVATION (not an axiom check).
  Print the three statements with full binders, universes and instance arguments, and diff
  against the same three lines taken from the pre-patch 83-module build. The three R3 syntax
  fixes (omit moved above the doc comment; two `exact`s) were reported as syntax-only, and a
  passing build does NOT prove the printed signature is unchanged -- `omit` placement in
  particular controls which instance binders appear. This diff is the check that decides it. -/

set_option pp.explicit true in
set_option pp.universes true in
#check @OAI.PlaneFiveColor.Spectral.finite_uniform_precision_contradiction
set_option pp.explicit true in
set_option pp.universes true in
#check @OAI.PlaneFiveColor.Spectral.ambient_uniform_precision_contradiction
set_option pp.explicit true in
set_option pp.universes true in
#check @OAI.PlaneFiveColor.Spectral.uniform_precision_contradiction

/-! ## A5. The two definitions changed kind (`def` -> `abbrev`); arity/explicitness check. -/

#check @OAI.PlaneFiveColor.Spectral.EncodingApproximationAt
#check @OAI.PlaneFiveColor.Spectral.FiniteEncodingApproximationAt

/-! # PART B -- OPTIONAL, UNAFFECTED
  chi(R^2) <= 7. `Seven` (build order 78) is NOT among the 19 reverse-dependent modules, so
  this root cannot be affected by the edit. Kept separate so it does not pollute Part A.
  Expected and acceptable: this may well print a proper subset, or the same set, as Part A. -/

#print axioms OAI.Problem160.properColoring_seven
#print axioms OAI.Problem160.weakMeasurableColoring_seven
