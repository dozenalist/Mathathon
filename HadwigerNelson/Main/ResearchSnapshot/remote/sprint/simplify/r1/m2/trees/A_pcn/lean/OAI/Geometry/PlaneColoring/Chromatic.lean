/-
  The paper's displayed consequence of Theorem 1.1,

        Theorem 1.1 (second sentence).  Consequently   6 <= chi(R^2) <= 7.

  is not stated anywhere in the bundle, and `OAI.Problem160.planeChromaticNumber` (the
  bundle's own definition of chi(R^2)) occurs only in its definition.  This file closes
  that statement-fidelity gap in Lean: it transports the five-colouring obstruction from
  the bundle's ℂ-vocabulary to the `Plane = EuclideanSpace ℝ (Fin 2)` vocabulary through an
  explicit isometry, and deduces the paper's displayed inequality.

  Contributed by swarm member `m1` (direction d5) and integrated here.
  Check (from repo/lean):
    source ../scripts/env4341.sh
    lean OAI/Geometry/PlaneColoring/Chromatic.lean
-/
import OAI.Geometry.PlaneColoring.Five
import OAI.Geometry.PlaneColoring.Seven
import OAI.Geometry.PlaneColoring.Basic

namespace OAI
namespace Problem160

noncomputable section

/-! ## the explicit isometry `ℂ ≃ Plane` -/

/-- `z ↦ (re z, im z)` as a point of the bundle's plane. -/
def toPlane (z : ℂ) : Plane := WithLp.toLp 2 ![z.re, z.im]

/-- Its inverse. -/
def ofPlane (p : Plane) : ℂ := ⟨p 0, p 1⟩

@[simp] lemma toPlane_zero (z : ℂ) : toPlane z 0 = z.re := rfl
@[simp] lemma toPlane_one (z : ℂ) : toPlane z 1 = z.im := rfl
@[simp] lemma ofPlane_re (p : Plane) : (ofPlane p).re = p 0 := rfl
@[simp] lemma ofPlane_im (p : Plane) : (ofPlane p).im = p 1 := rfl

lemma toPlane_sub (z w : ℂ) : toPlane (z - w) = toPlane z - toPlane w := by
  ext i <;> fin_cases i <;> simp [toPlane]

lemma sq_norm_toPlane (z : ℂ) : ‖toPlane z‖ ^ 2 = z.re ^ 2 + z.im ^ 2 := by
  rw [EuclideanSpace.real_norm_sq_eq]
  simp only [Fin.sum_univ_two, toPlane_zero, toPlane_one]

lemma sq_norm_complex (z : ℂ) : ‖z‖ ^ 2 = z.re ^ 2 + z.im ^ 2 := by
  rw [Complex.sq_norm, Complex.normSq_apply]; ring

lemma norm_toPlane (z : ℂ) : ‖toPlane z‖ = ‖z‖ := by
  have h : ‖toPlane z‖ ^ 2 = ‖z‖ ^ 2 := by rw [sq_norm_toPlane, sq_norm_complex]
  calc ‖toPlane z‖ = Real.sqrt (‖toPlane z‖ ^ 2) := (Real.sqrt_sq (norm_nonneg _)).symm
    _ = Real.sqrt (‖z‖ ^ 2) := by rw [h]
    _ = ‖z‖ := Real.sqrt_sq (norm_nonneg _)

lemma dist_toPlane (z w : ℂ) : dist (toPlane z) (toPlane w) = dist z w := by
  rw [dist_eq_norm, dist_eq_norm, ← toPlane_sub, norm_toPlane]

lemma dist_ofPlane (x y : Plane) : dist (ofPlane x) (ofPlane y) = dist x y := by
  have h1 : dist (ofPlane x) (ofPlane y) ^ 2 = (x 0 - y 0) ^ 2 + (x 1 - y 1) ^ 2 := by
    rw [dist_eq_norm, sq_norm_complex]
    simp [ofPlane]
  have h2 : dist x y ^ 2 = (x 0 - y 0) ^ 2 + (x 1 - y 1) ^ 2 := by
    rw [dist_eq_norm, EuclideanSpace.real_norm_sq_eq]
    simp only [Fin.sum_univ_two, PiLp.sub_apply]
  have h : dist (ofPlane x) (ofPlane y) ^ 2 = dist x y ^ 2 := by rw [h1, h2]
  calc dist (ofPlane x) (ofPlane y)
      = Real.sqrt (dist (ofPlane x) (ofPlane y) ^ 2) :=
        (Real.sqrt_sq (dist_nonneg)).symm
    _ = Real.sqrt (dist x y ^ 2) := by rw [h]
    _ = dist x y := Real.sqrt_sq (dist_nonneg)

/-! ## transporting colourings between the two vocabularies -/

/-- A proper colouring of the bundle's plane pulls back to one of `ℂ`. -/
lemma properColoring_of_plane {k : ℕ} {c : Plane → Fin k}
    (hc : ∀ x y : Plane, dist x y = 1 → c x ≠ c y) :
    EuclideanFiveColor.ProperColoring k (fun z => c (toPlane z)) := by
  intro x y hxy
  refine hc _ _ ?_
  rw [dist_toPlane, dist_eq_norm]
  exact hxy

/-- A proper colouring of `ℂ` pushes forward to one of the bundle's plane. -/
lemma plane_of_properColoring {k : ℕ} {d : ℂ → Fin k}
    (hd : EuclideanFiveColor.ProperColoring k d) :
    ∀ x y : Plane, dist x y = 1 → (fun p => d (ofPlane p)) x ≠ (fun p => d (ofPlane p)) y := by
  intro x y hxy
  refine hd _ _ ?_
  rw [← dist_eq_norm, dist_ofPlane]
  exact hxy

/-- The two vocabularies define the same property. -/
lemma planeProperColoring_iff {k : ℕ} :
    ProperColoring k ↔ ∃ d : ℂ → Fin k, EuclideanFiveColor.ProperColoring k d := by
  constructor
  · rintro ⟨c, hc⟩
    exact ⟨fun z => c (toPlane z), properColoring_of_plane hc⟩
  · rintro ⟨d, hd⟩
    exact ⟨fun p => d (ofPlane p), plane_of_properColoring hd⟩

/-! ## monotonicity in the number of colours -/

lemma properColoring_mono {k m : ℕ} (hkm : k ≤ m) (h : ProperColoring k) :
    ProperColoring m := by
  obtain ⟨c, hc⟩ := h
  refine ⟨fun p => Fin.castLE hkm (c p), ?_⟩
  intro x y hxy hcontra
  exact hc x y hxy (Fin.eq_of_val_eq (by simpa using congrArg Fin.val hcontra))

/-! ## no colouring with at most five colours -/

/-- The five-colouring obstruction, stated for the bundle's own `ProperColoring`. -/
theorem not_properColoring_five : ¬ ProperColoring 5 := by
  intro h
  obtain ⟨d, hd⟩ := planeProperColoring_iff.mp h
  exact EuclideanFiveColor.no_proper_five_coloring ⟨d, hd⟩

theorem not_properColoring_of_le {k : ℕ} (hk : k ≤ 5) : ¬ ProperColoring k := fun h =>
  not_properColoring_five (properColoring_mono hk h)

/-! ## the paper's displayed inequality  6 <= chi(R^2) <= 7 -/

theorem six_le_planeChromaticNumber : 6 ≤ planeChromaticNumber := by
  simp [planeChromaticNumber]

theorem planeChromaticNumber_le_seven : planeChromaticNumber ≤ 7 := by
  simp [planeChromaticNumber]

/-- The paper's Theorem 1.1, second sentence, as a statement about chi(R^2). -/
theorem chromaticNumber_bounds : 6 ≤ planeChromaticNumber ∧ planeChromaticNumber ≤ 7 :=
  ⟨six_le_planeChromaticNumber, planeChromaticNumber_le_seven⟩

end
end Problem160
end OAI

#print axioms OAI.Problem160.chromaticNumber_bounds
#print axioms OAI.Problem160.six_le_planeChromaticNumber
#print axioms OAI.Problem160.not_properColoring_five
