/-
  Axiom report for the two top-level theorems of the Hadwiger--Nelson Lean bundle,
  run in the exact toolchain the bundle was written for (Lean 4.34.1 + Mathlib
  @ d13f23b723b8a846827a245b89c10fc7d3f11612).

  Check (from repo/lean):
    source ../scripts/env4341.sh
    lean ../.ultramath/smwfcr56i/m1/Axioms.lean
-/
import OAI.Geometry.PlaneColoring.Five
import OAI.Geometry.PlaneColoring.Seven

-- the lower bound, paper Theorem 1.1
#print axioms OAI.EuclideanFiveColor.no_proper_five_coloring
-- the upper bound, paper section 1 (Hadwiger hexagonal colouring)
#print axioms OAI.Problem160.properColoring_seven
-- the measurable step it rests on, paper Theorem 1.4
#print axioms OAI.EuclideanFiveColor.no_measurable_weak_five_coloring
-- the transfer, paper Theorem 1.3 (forward direction only in the bundle)
#print axioms OAI.EuclideanFiveColor.proper_to_borel_weak
-- the global graph approximation, paper sections 7-8
#print axioms OAI.EuclideanFiveColor.fullApprox_exists
#print axioms OAI.EuclideanFiveColor.FullApprox.no_large_positive_sequence
-- the topological core, paper section 7
#print axioms OAI.EuclideanFiveColor.graph_map_large_positive
#print axioms OAI.PlanarCover.compact_open_cover_impossible
-- the finite simplex lemma, paper section 7 (a point of the K5 realization has <= 2
-- positive barycentric coordinates)
#print axioms OAI.EuclideanFiveColor.graphRealization_positive_three
