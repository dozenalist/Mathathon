import OAI.Analysis.PlaneSpectrum.Energy

/-!
# Elementary bricks for (N), at the real OAI types

(N) is the properness statement the R1 restructure needs: for a wild `μ` on `D` the
maximal compact extension of the point factor is a proper factor.  Its documented proof
(`.ultramath/smwfoekgk/m7/N-proof.md` §2) is invalid -- see `N-sharpened.md`.  The bricks
below are the elementary facts that proof uses, stated at the tree's own objects
(`E`, `K`, `kCoeff`, `scalar`, `eval`, `char`, `D`, `C`).  They are correct independently
of the gap and are what any repaired argument will consume.
-/

namespace OAI

noncomputable section

open MeasureTheory ProbabilityTheory Filter
namespace PlaneFiveColor.Spectral
open EuclideanFiveColor.BoundedMeasurable

/-- **(F2)**, three-term form: the character increments are subadditive in the argument.
This is the triangle inequality behind `φ(a+b) ≤ φ(a) + φ(b)`; it needs only
`‖char b d‖ = 1`. -/
theorem norm_char_add_sub_one_le (a b : E) (d : D) :
    ‖char (a + b) d - 1‖ ≤ ‖char a d - 1‖ + ‖char b d - 1‖ := by
  rw [char_add, mul_apply]
  have hb : ‖char b d‖ = 1 := norm_char b d
  have hb0 : char b d ≠ 0 := by
    intro h
    rw [h] at hb
    simp at hb
  have key : char a d * char b d - 1 = char b d * (char a d - (char b d)⁻¹) := by
    field_simp
  rw [key, norm_mul, hb, one_mul]
  calc ‖char a d - (char b d)⁻¹‖
      = ‖(char a d - 1) + (1 - (char b d)⁻¹)‖ := by ring_nf
    _ ≤ ‖char a d - 1‖ + ‖1 - (char b d)⁻¹‖ := norm_add_le _ _
    _ = ‖char a d - 1‖ + ‖char b d - 1‖ := by
        have hone : 1 - (char b d)⁻¹ = (char b d)⁻¹ * (char b d - 1) := by
          field_simp
        rw [hone, norm_mul, norm_inv, hb, inv_one, one_mul]

/-- **(F2)**, finite-sum form. -/
theorem norm_char_sum_sub_one_le {ι : Type*} (s : Finset ι) (f : ι → E) (d : D) :
    ‖char (∑ i ∈ s, f i) d - 1‖ ≤ ∑ i ∈ s, ‖char (f i) d - 1‖ := by
  classical
  induction s using Finset.induction_on with
  | empty => simp
  | insert a s ha ih =>
    rw [Finset.sum_insert ha, Finset.sum_insert ha]
    exact (norm_char_add_sub_one_le (f a) (∑ i ∈ s, f i) d).trans (add_le_add le_rfl ih)

/-- **(F1)**: `char (k·a)` is `char a` composed with the `K`-action on `D`. -/
theorem char_kCoeff_mul_eq_char_smul (a : E) (u : K) (d : D) :
    char (kCoeff u * a) d = char a (u • d) := by
  show ((eval (kCoeff u * a) d : Circle) : ℂ) = ((eval a (u • d) : Circle) : ℂ)
  have h1 : eval (kCoeff u * a) d = eval a (u • d) := by
    show d (Multiplicative.ofAdd (kCoeff u * a))
      = scalar (kCoeff u) d (Multiplicative.ofAdd a)
    change d (Multiplicative.ofAdd (kCoeff u * a))
      = d (Multiplicative.ofAdd (kCoeff u * Multiplicative.toAdd (Multiplicative.ofAdd a)))
    rfl
  rw [h1]

/-- **(F1)**, coefficient form: `K`-invariance of `μ` makes the Fourier coefficients
`K`-invariant.  This is the only place `IsWild`'s first component is used. -/
theorem integral_char_kCoeff_mul (μ : Measure D) [IsProbabilityMeasure μ]
    (hμ : ∀ u : K, MeasurePreserving (fun d : D => u • d) μ μ) (a : E) (u : K) :
    ∫ d, char (kCoeff u * a) d ∂μ = ∫ d, char a d ∂μ := by
  have hfun : (fun d => char (kCoeff u * a) d) = (fun d => char a (u • d)) :=
    funext fun d => char_kCoeff_mul_eq_char_smul a u d
  have hmap : Measure.map (fun d : D => u • d) μ = μ := (hμ u).map_eq
  have him := (integral_map (f := fun y : D => char a y) (hμ u).aemeasurable
    (measurable (char a)).aestronglyMeasurable).symm
  rw [hmap] at him
  rw [hfun]
  exact him

/-- **(O)**: the trivial character `1 = j 0` lies in `C`. -/
theorem one_mem_C : (1 : D) ∈ C := ⟨1, jHom.map_one⟩

/-- Hence `IsWild` forces the measure off every point of `C`. -/
theorem wild_ne_dirac_of_mem_C {ν : Measure D} (hν : IsWild ν) {d : D} (hd : d ∈ C) :
    ν ≠ Measure.dirac d := by
  intro h
  have h1 : ν (C : Set D) = 1 := by
    rw [h, Measure.dirac_apply' d measurableSet_C, Set.indicator_of_mem hd]
    norm_num
  exact zero_ne_one (hν.2.symm.trans h1)

end PlaneFiveColor.Spectral

end

end OAI
