/-
  Sharpness of the *radius* constant in the §7 engine (swarm smwg1r9lg, member m7, d8).

  `graph_map_small_mesh_impossible_generic` says: there is no continuous graph-valued map of
  the closed disk of radius 5 whose every positive-coordinate preconnected set has diameter
  at most 2.  The radius is not gratuitous.  On a closed disk of radius at most 1 *every*
  subset already has diameter at most 2, so the mesh hypothesis is automatic there: the
  analogous statement fails on every disk of radius <= 1, and in fact every continuous
  graph-valued map on such a disk satisfies the hypothesis.  So the cover obstruction needs a
  disk of radius greater than 1 in the normalisation in which the diameter bound is 2 — the
  same constant that appears as `R > 1` in hypothesis (W).
-/
import OAI.Geometry.PlaneColoring.PlanarCovers
import OAI.Geometry.PlaneColoring.GraphRealization

open OAI Set Topology

namespace M7Radius

/-- On a disk of radius `r <= 1` the mesh hypothesis of the §7 engine is automatic: the whole
disk has diameter `2r <= 2`, so every continuous graph-valued map satisfies it.  Hence the
obstruction cannot be lowered to radius `<= 1`. -/
theorem cover_radius_le_one_vacuous (r : ℝ) (hr1 : r ≤ 1) :
    ∃ F : C(Metric.closedBall (0:ℂ) r,
        EuclideanFiveColor.GraphSpace (⊤ : SimpleGraph (Fin 2))),
      ∀ (i : Fin 2) (K : Set ℂ), IsPreconnected K → K ⊆ Metric.closedBall (0:ℂ) r →
        (∀ z (hz : z ∈ Metric.closedBall (0:ℂ) r), z ∈ K → 0 < (F ⟨z, hz⟩).val i) →
        ∀ x ∈ K, ∀ y ∈ K, dist x y ≤ 2 := by
  classical
  refine ⟨ContinuousMap.const _ ⟨EuclideanFiveColor.graphVertex 0,
    EuclideanFiveColor.graphVertex_mem (⊤ : SimpleGraph (Fin 2)) 0⟩, ?_⟩
  intro i K _ hsub _ x hx y hy
  have hx1 : ‖x‖ ≤ r := by
    simpa [Metric.mem_closedBall, dist_zero_right] using hsub hx
  have hy1 : ‖y‖ ≤ r := by
    simpa [Metric.mem_closedBall, dist_zero_right] using hsub hy
  calc dist x y = ‖x - y‖ := dist_eq_norm x y
    _ ≤ ‖x‖ + ‖y‖ := norm_sub_le x y
    _ ≤ 2 := by linarith

/-- The radius-1 instance, named for the record. -/
theorem cover_radius_one_vacuous :
    ∃ F : C(Metric.closedBall (0:ℂ) 1,
        EuclideanFiveColor.GraphSpace (⊤ : SimpleGraph (Fin 2))),
      ∀ (i : Fin 2) (K : Set ℂ), IsPreconnected K → K ⊆ Metric.closedBall (0:ℂ) 1 →
        (∀ z (hz : z ∈ Metric.closedBall (0:ℂ) 1), z ∈ K → 0 < (F ⟨z, hz⟩).val i) →
        ∀ x ∈ K, ∀ y ∈ K, dist x y ≤ 2 :=
  cover_radius_le_one_vacuous 1 le_rfl

#print axioms cover_radius_le_one_vacuous
#print axioms cover_radius_one_vacuous

end M7Radius
