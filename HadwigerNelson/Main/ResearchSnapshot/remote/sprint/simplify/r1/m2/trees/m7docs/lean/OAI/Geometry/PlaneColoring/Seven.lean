import OAI.Geometry.PlaneColoring.Assembly
import OAI.Geometry.PlaneColoring.Lattice
import OAI.Geometry.PlaneColoring.Metric
import OAI.Geometry.PlaneColoring.Covering

namespace OAI

noncomputable section

namespace Problem160

theorem properColoring_seven_of_normalized_cover
    (hcover : ∀ x y : ℝ, ∃ a b : ℤ,
      (x - ((a : ℝ) + (b : ℝ) / 2)) ^ 2 +
        (y - Real.sqrt 3 * b / 2) ^ 2 ≤ (1 / 3 : ℝ)) :
    ProperColoring 7 := by
  apply exists_unit_distance_coloring_of_center_cover
    (fun p : ℤ × ℤ => triangularLattice p.1 p.2)
    (fun p : ℤ × ℤ => SevenLattice.colorFin p.1 p.2) (7 / 15 : ℝ)
  · intro x
    obtain ⟨a, b, hab⟩ := hcover ((5 / 4 : ℝ) * x 0) ((5 / 4 : ℝ) * x 1)
    exact ⟨(a, b), dist_triangularLattice_le_of_coordinates x a b hab⟩
  · norm_num
  · intro i j hij hc
    have hq := SevenLattice.same_color_separation
      (SevenLattice.colorFin_injective_value hc) hij
    have hsep := triangularLattice_dist_gt_two i.1 i.2 j.1 j.2 hq
    linarith

theorem properColoring_seven : ProperColoring 7 :=
  properColoring_seven_of_normalized_cover triangular_lattice_cover

end Problem160

end

end OAI
