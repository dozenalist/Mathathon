import OAI.Analysis.PlaneSpectrum.Fourier
import OAI.Geometry.PlaneColoring.Coloring

namespace OAI

noncomputable section
open Set Filter Topology MeasureTheory
namespace EuclideanFiveColor
lemma oscillatory_integral_bound {a b : ℝ} (hab : a ≤ b)
    {g g' : ℝ → ℂ} {w w' : ℝ → ℝ}
    (hg : ∀ t ∈ Icc a b, HasDerivAt g (g' t) t)
    (hw : ∀ t ∈ Icc a b, HasDerivAt w (w' t) t)
    (hgi : IntervalIntegrable g' volume a b) (hwi : IntervalIntegrable w' volume a b)
    (hn : ∀ t ∈ Icc a b, ‖g t‖=1) (hwpos : ∀ t ∈ Icc a b, 0 ≤ w t)
    (hwneg : ∀ t ∈ Icc a b, w' t ≤ 0)
    (he : ∀ t ∈ Icc a b, ((w t : ℂ)*Complex.I)*g' t=g t) :
    ‖∫ t in a..b, g t‖ ≤ 2*w a := by
  have hwu : ∀ t ∈ uIcc a b, HasDerivAt (fun t => (w t : ℂ)*Complex.I) ((w' t : ℂ)*Complex.I) t := by
    intro t ht
    exact ((hw t (by simpa [uIcc_of_le hab] using ht)).ofReal_comp).mul_const _
  have hs := intervalIntegral.integral_mul_deriv_eq_deriv_mul hwu
    (fun t ht => hg t (by simpa [uIcc_of_le hab] using ht)) ((show IntervalIntegrable (fun t => (w' t : ℂ)) volume a b from
      ⟨Complex.ofRealCLM.integrable_comp hwi.1,Complex.ofRealCLM.integrable_comp hwi.2⟩).mul_const _) hgi
  have hleft : (∫ t in a..b, ((w t : ℂ)*Complex.I)*g' t) = ∫ t in a..b, g t :=
    intervalIntegral.integral_congr (fun t ht => he t (by simpa [uIcc_of_le hab] using ht))
  rw [hleft] at hs
  have hint : ‖∫ t in a..b, (w' t : ℂ)*Complex.I*g t‖ ≤ ∫ t in a..b, -w' t := by
    apply intervalIntegral.norm_integral_le_of_norm_le hab _ hwi.neg
    filter_upwards with t ht
    rw [norm_mul,norm_mul,Complex.norm_real,Real.norm_eq_abs,Complex.norm_I,hn t ⟨ht.1.le,ht.2⟩,mul_one,mul_one,
      abs_of_nonpos (hwneg t ⟨ht.1.le,ht.2⟩)]
    rfl
  have hiw : (∫ t in a..b, -w' t)=w a-w b := by
    rw [intervalIntegral.integral_neg,intervalIntegral.integral_eq_sub_of_hasDerivAt
      (fun t ht => hw t (by simpa [uIcc_of_le hab] using ht)) hwi]
    ring
  have hna : ‖(w a : ℂ)*Complex.I*g a‖=w a := by
    rw [norm_mul,norm_mul,Complex.norm_real,Real.norm_eq_abs,abs_of_nonneg (hwpos a ⟨le_rfl,hab⟩),
      Complex.norm_I,hn a ⟨le_rfl,hab⟩,mul_one,mul_one]
  have hnb : ‖(w b : ℂ)*Complex.I*g b‖=w b := by
    rw [norm_mul,norm_mul,Complex.norm_real,Real.norm_eq_abs,abs_of_nonneg (hwpos b ⟨hab,le_rfl⟩),
      Complex.norm_I,hn b ⟨hab,le_rfl⟩,mul_one,mul_one]
  rw [hs]
  have hh := norm_sub_le ((w b : ℂ)*Complex.I*g b-(w a : ℂ)*Complex.I*g a)
    (∫ t in a..b, (w' t : ℂ)*Complex.I*g t)
  have hh' := norm_sub_le ((w b : ℂ)*Complex.I*g b) ((w a : ℂ)*Complex.I*g a)
  rw [hna,hnb] at hh'
  rw [hiw] at hint
  linarith
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology MeasureTheory
namespace EuclideanFiveColor
end EuclideanFiveColor

end

noncomputable section
open MeasureTheory Filter Topology FourierTransform
namespace EuclideanFiveColor
end EuclideanFiveColor
end

end OAI
