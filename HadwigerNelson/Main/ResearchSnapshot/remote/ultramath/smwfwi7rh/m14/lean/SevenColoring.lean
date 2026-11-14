/-
  The classical seven-colouring of the plane on a triangular lattice, in ℂ, with the exact
  annulus certificate used by the k ≥ 7 counterexample.
-/
import Assembly
import OAI.Geometry.PlaneColoring.Covering

open MeasureTheory Filter Topology Set
open scoped ENNReal

attribute [local instance] Classical.propDecidable

namespace SectorGadget

/-! ## 9. The triangular lattice and the seven-colouring -/

/-- Lattice point `(a,b)` of the triangular lattice with nearest-neighbour spacing `4/5`. -/
noncomputable def lat (a b : ℤ) : ℂ :=
  ⟨(4:ℝ)/5 * ((a:ℝ) + (b:ℝ)/2), ((2:ℝ) * Real.sqrt 3 / 5) * (b:ℝ)⟩

@[simp] lemma lat_re (a b : ℤ) : (lat a b).re = (4:ℝ)/5 * ((a:ℝ) + (b:ℝ)/2) := rfl
@[simp] lemma lat_im (a b : ℤ) : (lat a b).im = ((2:ℝ) * Real.sqrt 3 / 5) * (b:ℝ) := rfl

/-- The norm form of the lattice. -/
def nrm (a b : ℤ) : ℤ := a ^ 2 + a * b + b ^ 2

lemma lat_sub (a b c d : ℤ) : lat a b - lat c d = lat (a - c) (b - d) := by
  apply Complex.ext
  · simp only [Complex.sub_re, lat_re]
    push_cast
    ring
  · simp only [Complex.sub_im, lat_im]
    push_cast
    ring

lemma lat_norm_sq (a b : ℤ) : ‖lat a b‖ ^ 2 = (16/25 : ℝ) * (nrm a b : ℝ) := by
  have h3 : (Real.sqrt 3) ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  rw [sq_norm_re_im, lat_re, lat_im]
  unfold nrm
  push_cast
  nlinarith [h3]

lemma nrm_pos {a b : ℤ} (h : a ≠ 0 ∨ b ≠ 0) : 0 < nrm a b := by
  unfold nrm
  rcases h with h | h
  · nlinarith [sq_nonneg (2 * a + b), sq_pos_of_ne_zero h]
  · nlinarith [sq_nonneg (a + 2 * b), sq_pos_of_ne_zero h]

lemma seven_dvd_nrm {a b : ℤ} (h : 7 ∣ a + 3 * b) : 7 ∣ nrm a b := by
  have hi : nrm a b = (a + 3 * b) * (a - 2 * b) + 7 * b ^ 2 := by unfold nrm; ring
  rw [hi]
  exact dvd_add (dvd_mul_of_dvd_left h _) ⟨b ^ 2, by ring⟩

lemma nrm_ge_seven {a b : ℤ} (h : 7 ∣ a + 3 * b) (hn : a ≠ 0 ∨ b ≠ 0) : 7 ≤ nrm a b :=
  Int.le_of_dvd (nrm_pos hn) (seven_dvd_nrm h)

/-- Same-coloured lattice points are more than `2` apart. -/
lemma lat_separation {a b c d : ℤ} (hne : (a, b) ≠ (c, d))
    (h : 7 ∣ (a - c) + 3 * (b - d)) : (2:ℝ) < ‖lat a b - lat c d‖ := by
  have hnz : a - c ≠ 0 ∨ b - d ≠ 0 := by
    by_contra hn
    push Not at hn
    exact hne (Prod.ext (by omega) (by omega))
  have h7 : 7 ≤ nrm (a - c) (b - d) := nrm_ge_seven h hnz
  have hsq : ‖lat a b - lat c d‖ ^ 2 = (16/25 : ℝ) * (nrm (a - c) (b - d) : ℝ) := by
    rw [lat_sub, lat_norm_sq]
  have h7r : (7:ℝ) ≤ (nrm (a - c) (b - d) : ℝ) := by exact_mod_cast h7
  have hnn : (0:ℝ) ≤ ‖lat a b - lat c d‖ := norm_nonneg _
  nlinarith

/-! ## 10. Covering the plane by the lattice -/

/-- Every point of `ℂ` is within `4√3/15` of a lattice point. -/
lemma cover_lat (q : ℂ) : ∃ a b : ℤ, ‖q - lat a b‖ ≤ 4 * Real.sqrt 3 / 15 := by
  obtain ⟨m, n, h⟩ := OAI.Problem160.triangular_lattice_cover ((5/4) * q.re) ((5/4) * q.im)
  have h3 : (Real.sqrt 3) ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  refine ⟨m, n, ?_⟩
  have hsq : ‖q - lat m n‖ ^ 2 = (16/25 : ℝ) *
      (((5/4) * q.re - ((m:ℝ) + (n:ℝ)/2)) ^ 2 +
       ((5/4) * q.im - Real.sqrt 3 * (n:ℝ) / 2) ^ 2) := by
    rw [sq_norm_re_im]
    simp only [Complex.sub_re, Complex.sub_im, lat_re, lat_im]
    push_cast
    nlinarith [h3]
  have hgoal : (4 * Real.sqrt 3 / 15) ^ 2 = (16/25 : ℝ) * (1/3) := by
    rw [div_pow, mul_pow]
    nlinarith [h3]
  refine le_of_sq_le_sq (by positivity) ?_
  rw [hsq, hgoal]
  nlinarith [h]

/-! ## 11. The colouring -/

/-- The lattice colour `a + 3b mod 7`, as an element of `ZMod 7`. -/
def colr (a b : ℤ) : ZMod 7 := (a : ZMod 7) + 3 * (b : ZMod 7)

lemma colr_eq_iff {a b c d : ℤ} : colr a b = colr c d ↔ 7 ∣ (c + 3 * d) - (a + 3 * b) := by
  unfold colr
  have h1 : ((a : ZMod 7) + 3 * (b : ZMod 7)) = (((a + 3 * b : ℤ)) : ZMod 7) := by
    push_cast; ring
  have h2 : ((c : ZMod 7) + 3 * (d : ZMod 7)) = (((c + 3 * d : ℤ)) : ZMod 7) := by
    push_cast; ring
  rw [h1, h2, ZMod.intCast_eq_intCast_iff, Int.modEq_iff_dvd]
  norm_num

/-- The colouring as a `Fin 7`-valued function on lattice indices. -/
noncomputable def colFin (a b : ℤ) : Fin 7 := ⟨(colr a b).val, ZMod.val_lt _⟩

lemma colFin_eq_iff {a b c d : ℤ} : colFin a b = colFin c d ↔ colr a b = colr c d := by
  constructor
  · intro h
    exact ZMod.val_injective 7 (by simpa [colFin] using congrArg Fin.val h)
  · intro h
    simp only [colFin, h]

lemma colFin_zero : colFin 0 0 = 0 := by decide

lemma colFin_three : colFin 0 1 = 3 := by decide

lemma colFin_two : colFin (-1) 1 = 2 := by decide

/-- A covering centre of `x`. -/
noncomputable def coverPt (x : ℂ) : ℤ × ℤ :=
  (Classical.choose (cover_lat x), Classical.choose (Classical.choose_spec (cover_lat x)))

lemma coverPt_spec (x : ℂ) :
    ‖x - lat (coverPt x).1 (coverPt x).2‖ ≤ 4 * Real.sqrt 3 / 15 :=
  Classical.choose_spec (Classical.choose_spec (cover_lat x))

/-- The seven-colouring of the plane. -/
noncomputable def sevenColor (x : ℂ) : Fin 7 := colFin (coverPt x).1 (coverPt x).2

/-! ## 12. The annulus certificate -/

/-- The centre of the annulus: the circumcentre of the equilateral triangle whose vertices are
the lattice points `(0,0)`, `(0,1)`, `(-1,1)`, of colours `0`, `3`, `2`. -/
noncomputable def p0 : ℂ := ⟨0, (4:ℝ) * Real.sqrt 3 / 15⟩

@[simp] lemma p0_re : p0.re = 0 := rfl
@[simp] lemma p0_im : p0.im = (4:ℝ) * Real.sqrt 3 / 15 := rfl

lemma sqrt3_lt : Real.sqrt 3 < 77/40 := by
  have h3 : (Real.sqrt 3) ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  have hnn := Real.sqrt_nonneg 3
  nlinarith

lemma dist_p0 (a b : ℤ) :
    ‖p0 - lat a b‖ ^ 2 = ((4:ℝ)/5 * ((a:ℝ) + (b:ℝ)/2)) ^ 2 +
      (4 * Real.sqrt 3 / 15 - (2:ℝ) * Real.sqrt 3 / 5 * (b:ℝ)) ^ 2 := by
  rw [sq_norm_re_im]
  simp only [Complex.sub_re, Complex.sub_im, p0_re, p0_im, lat_re, lat_im]
  ring

lemma dist_p0_zero : ‖p0 - lat 0 0‖ = 4 * Real.sqrt 3 / 15 := by
  have h3 : (Real.sqrt 3) ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  have hsq : ‖p0 - lat 0 0‖ ^ 2 = (4 * Real.sqrt 3 / 15) ^ 2 := by
    rw [dist_p0]; push_cast; ring
  exact le_antisymm (le_of_sq_le_sq (by positivity) (le_of_eq hsq))
    (le_of_sq_le_sq (norm_nonneg _) (le_of_eq hsq.symm))

lemma dist_p0_one : ‖p0 - lat 0 1‖ = 4 * Real.sqrt 3 / 15 := by
  have h3 : (Real.sqrt 3) ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  have hsq : ‖p0 - lat 0 1‖ ^ 2 = (4 * Real.sqrt 3 / 15) ^ 2 := by
    rw [dist_p0]; push_cast; nlinarith [h3]
  exact le_antisymm (le_of_sq_le_sq (by positivity) (le_of_eq hsq))
    (le_of_sq_le_sq (norm_nonneg _) (le_of_eq hsq.symm))

lemma dist_p0_neg : ‖p0 - lat (-1) 1‖ = 4 * Real.sqrt 3 / 15 := by
  have h3 : (Real.sqrt 3) ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  have hsq : ‖p0 - lat (-1) 1‖ ^ 2 = (4 * Real.sqrt 3 / 15) ^ 2 := by
    rw [dist_p0]; push_cast; nlinarith [h3]
  exact le_antisymm (le_of_sq_le_sq (by positivity) (le_of_eq hsq))
    (le_of_sq_le_sq (norm_nonneg _) (le_of_eq hsq.symm))

end SectorGadget
