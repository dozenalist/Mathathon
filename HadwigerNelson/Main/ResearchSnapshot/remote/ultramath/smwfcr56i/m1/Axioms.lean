/-
  Axiom report for the Hadwiger--Nelson Lean bundle, run in the toolchain the bundle was
  written for (Lean 4.34.1 + Mathlib @ d13f23b723b8a846827a245b89c10fc7d3f11612).

  Check (from repo/lean):
    source ../scripts/env4341.sh
    lean ../.ultramath/smwfcr56i/m1/Axioms.lean
-/
import OAI.Geometry.PlaneColoring.Five
import OAI.Geometry.PlaneColoring.Seven
import OAI.Geometry.PlaneColoring.Exclusion
import OAI.Geometry.PlaneColoring.AngularBoundary
import OAI.Geometry.PlaneColoring.BinaryPalettes
import OAI.Geometry.PlaneColoring.ContinuumLimits
import OAI.Geometry.PlaneColoring.CyclicCore
import OAI.Geometry.PlaneColoring.Interfaces
import OAI.Analysis.PlaneSpectrum.Multipliers

/-! ## the two roots -/
-- paper Theorem 1.1: no proper 5-colouring of the plane
#print axioms OAI.EuclideanFiveColor.no_proper_five_coloring
-- paper section 1: a proper 7-colouring of the plane
#print axioms OAI.Problem160.properColoring_seven
#print axioms OAI.Problem160.exists_unit_distance_coloring_of_center_cover
#print axioms OAI.Problem160.triangular_lattice_cover
#print axioms OAI.Problem160.triangularLattice_dist_gt_two
#print axioms OAI.Problem160.SevenLattice.same_color_separation

/-! ## paper section 4, Theorems 1.3 and 1.4 -/
#print axioms OAI.EuclideanFiveColor.no_measurable_weak_five_coloring
#print axioms OAI.EuclideanFiveColor.proper_to_borel_weak

/-! ## paper sections 7-8 -/
#print axioms OAI.EuclideanFiveColor.fullApprox_exists
#print axioms OAI.EuclideanFiveColor.FullApprox.no_large_positive_sequence
#print axioms OAI.EuclideanFiveColor.graph_map_large_positive
#print axioms OAI.PlanarCover.compact_open_cover_impossible
#print axioms OAI.EuclideanFiveColor.graphRealization_positive_three
#print axioms OAI.EuclideanFiveColor.thresholdMap_mem_forest
#print axioms OAI.EuclideanFiveColor.compact_forest_charts

/-! ## paper section 2, rigidity -/
#print axioms OAI.PlaneFiveColor.Spectral.wild_coset_null
#print axioms OAI.PlaneFiveColor.Spectral.wild_independent_difference
#print axioms OAI.PlaneFiveColor.Spectral.wild_line_average_zero

/-! ## paper sections 5-6 -/
#print axioms OAI.EuclideanFiveColor.palette_cardinality
#print axioms OAI.EuclideanFiveColor.binary_centers_separated
#print axioms OAI.EuclideanFiveColor.cyclicCore_compact_finite

/-! ## paper section 7/8 cycle exclusions -/
#print axioms OAI.EuclideanFiveColor.no_five_exclusion_continua
#print axioms OAI.EuclideanFiveColor.no_five_commonInterface
#print axioms OAI.EuclideanFiveColor.no_triangle_commonInterface
#print axioms OAI.EuclideanFiveColor.five_opposite_contacts_false
#print axioms OAI.EuclideanFiveColor.straddle_connected_unit
#print axioms OAI.EuclideanFiveColor.four_words_no_mixed
