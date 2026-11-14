/-
  AXIOM-ROOT FILE for the isolated full build of the encoding-core integration.

  Frozen inputs this file is written against (do not chase later revisions):
    lean/OAI/Analysis/PlaneSpectrum/ConditionalSpectrum.lean
      sha256 48aa378f6f6db82bfeb0e65920ec2606507364541e72bf77ab969c6c87895dd1
    lean/OAI/MeasureTheory/CompactFactors/ConditionalLimits.lean
      sha256 58707f0495837a89b58d5ac7d131ee855220c74cba28851474489b7a8cdd9e0d

  PURPOSE. Print the axiom dependency of every public root whose statement or proof
  can be affected by the edit, plus the two headline roots of the tree.
  Acceptance rule (see ../AXIOM-GATE.md): each printed set must be a SUBSET of
  {propext, Classical.choice, Quot.sound}. Subsets are expected and accepted --
  a root that uses only propext, or only Quot.sound, PASSES. Do not require all three.

  A set containing `sorryAx`, or any name outside the three above, FAILS: the former
  means the transplanted body was not substituted, the latter means a custom axiom.

  RUN (from the repo root, after the patched pair is compiled into a private olean dir
  that precedes lean/build/lib on LEAN_PATH -- recipe in ../BUILD-NOTES-full.md section 3):

      source scripts/env4341.sh
      LEAN_PATH="$OUT:$LEAN_PATH" lean supervisor/simplify-lean/lean/AxiomRoots.lean

  Exit status 0 means the file elaborated; the gate on the printed sets is separate.
-/

import OAI.Analysis.PlaneSpectrum.ConditionalSpectrum
import OAI.MeasureTheory.CompactFactors.ConditionalLimits
import OAI.MeasureTheory.CompactFactors.Approximation
import OAI.Geometry.PlaneColoring.Five
import OAI.Geometry.PlaneColoring.Seven

/-! ## 1. The changed surface: the new common core and the two rewritten wrappers -/

#print axioms OAI.PlaneFiveColor.Spectral.uniform_precision_contradiction
#print axioms OAI.PlaneFiveColor.Spectral.finite_uniform_precision_contradiction
#print axioms OAI.PlaneFiveColor.Spectral.ambient_uniform_precision_contradiction

/-! ## 2. Nearest consumers, by fully qualified name

  `finite_uniform_successor_contradiction` is the only in-module consumer of the finite
  root. `relative_singularity_successor` (Approximation.lean:384, call at 413-414) is the
  nearest cross-module consumer and applies the finite statement positionally, so it is the
  strongest available statement-preservation test. `relative_singularity_approximation`
  (ConditionalLimits.lean:463, call at 501) is the nearest consumer of the ambient root. -/

#print axioms OAI.PlaneFiveColor.Spectral.finite_uniform_successor_contradiction
#print axioms OAI.PlaneFiveColor.Spectral.relative_singularity_successor
#print axioms OAI.PlaneFiveColor.Spectral.relative_singularity_approximation

/-! ## 3. The tree's headline roots (chi(R^2) >= 6 and chi(R^2) <= 7) -/

#print axioms OAI.EuclideanFiveColor.no_proper_five_coloring
#print axioms OAI.Problem160.properColoring_seven
#print axioms OAI.Problem160.weakMeasurableColoring_seven

/-! ## 4. Display checks: the two definitions changed kind (`def` -> `abbrev`).
  These are not axiom checks; they confirm the binders and the `S := p` / `S := id`
  instantiation still elaborate with the same arity and explicitness. -/

#check @OAI.PlaneFiveColor.Spectral.EncodingApproximationAt
#check @OAI.PlaneFiveColor.Spectral.FiniteEncodingApproximationAt
#check @OAI.PlaneFiveColor.Spectral.ambient_uniform_precision_contradiction
