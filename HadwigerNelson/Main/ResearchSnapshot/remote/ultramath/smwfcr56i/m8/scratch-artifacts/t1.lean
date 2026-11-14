import Mathlib
example (z : ℂ) : (algebraMap ℝ ℂ) z.re = (z + (starRingEnd ℂ) z) * 2⁻¹ := by
  show ((z.re : ℝ) : ℂ) = _
  rw [Complex.re_eq_add_conj, div_eq_mul_inv]
example (z : ℂ) : (algebraMap ℝ ℂ) z.im = (z - (starRingEnd ℂ) z) * 2⁻¹ * Complex.I⁻¹ := by
  show ((z.im : ℝ) : ℂ) = _
  rw [Complex.im_eq_sub_conj, div_eq_mul_inv]
  simp [div_eq_mul_inv, mul_assoc, mul_comm]
