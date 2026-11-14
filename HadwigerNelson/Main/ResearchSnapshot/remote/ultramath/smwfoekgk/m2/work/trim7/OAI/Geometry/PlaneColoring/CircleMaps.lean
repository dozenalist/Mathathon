import OAI.Geometry.PlaneColoring.Coloring

namespace OAI

noncomputable section
open Filter Topology Set
open scoped NNReal
namespace EuclideanFiveColor
abbrev RealPlane := ℝ × ℝ
def circleSum (r : ℝ) (p : RealPlane) : RealPlane :=
  (r*Real.cos p.1+Real.cos p.2,r*Real.sin p.1+Real.sin p.2)
def circleSumDeriv (r : ℝ) (p : RealPlane) : RealPlane →L[ℝ] RealPlane :=
  (r • ((-Real.sin p.1) • ContinuousLinearMap.fst ℝ ℝ ℝ) +
    (-Real.sin p.2) • ContinuousLinearMap.snd ℝ ℝ ℝ).prod
  (r • (Real.cos p.1 • ContinuousLinearMap.fst ℝ ℝ ℝ) +
    Real.cos p.2 • ContinuousLinearMap.snd ℝ ℝ ℝ)
lemma circleSum_strict (r : ℝ) (p : RealPlane) : HasStrictFDerivAt (circleSum r) (circleSumDeriv r p) p := by
  have hc1 := (Real.hasStrictDerivAt_cos p.1).comp_hasStrictFDerivAt p
    (ContinuousLinearMap.fst ℝ ℝ ℝ).hasStrictFDerivAt
  have hc2 := (Real.hasStrictDerivAt_cos p.2).comp_hasStrictFDerivAt p
    (ContinuousLinearMap.snd ℝ ℝ ℝ).hasStrictFDerivAt
  have hs1 := (Real.hasStrictDerivAt_sin p.1).comp_hasStrictFDerivAt p
    (ContinuousLinearMap.fst ℝ ℝ ℝ).hasStrictFDerivAt
  have hs2 := (Real.hasStrictDerivAt_sin p.2).comp_hasStrictFDerivAt p
    (ContinuousLinearMap.snd ℝ ℝ ℝ).hasStrictFDerivAt
  exact ((hc1.const_smul r).add hc2).prodMk ((hs1.const_smul r).add hs2)
lemma circleSum_continuous (r : ℝ) : Continuous (circleSum r) :=
  continuous_iff_continuousAt.mpr fun p => (circleSum_strict r p).continuousAt
lemma circleSumDeriv_injective {r : ℝ} {p : RealPlane} (h : r*Real.sin (p.2-p.1) ≠ 0) :
    Function.Injective (circleSumDeriv r p) := by
  apply (circleSumDeriv r p).toLinearMap.ker_eq_bot.mp
  apply LinearMap.ker_eq_bot'.mpr
  intro q hq
  have h1 := congrArg Prod.fst hq
  have h2 := congrArg Prod.snd hq
  change r * (-Real.sin p.1 * q.1) + -Real.sin p.2 * q.2 = 0 at h1
  change r * (Real.cos p.1 * q.1) + Real.cos p.2 * q.2 = 0 at h2
  have ha : r*Real.sin (p.2-p.1)*q.1=0 := by
    rw [Real.sin_sub]
    linear_combination Real.cos p.2*h1+Real.sin p.2*h2
  have hb : r*Real.sin (p.2-p.1)*q.2=0 := by
    rw [Real.sin_sub]
    linear_combination -(r*Real.cos p.1)*h1-(r*Real.sin p.1)*h2
  exact Prod.ext ((mul_eq_zero.mp ha).resolve_left h) ((mul_eq_zero.mp hb).resolve_left h)
def circleSumDerivEquiv {r : ℝ} {p : RealPlane} (h : r*Real.sin (p.2-p.1) ≠ 0) :
    RealPlane ≃L[ℝ] RealPlane :=
  ContinuousLinearEquiv.ofBijective (circleSumDeriv r p)
    (LinearMap.ker_eq_bot.mpr (circleSumDeriv_injective h))
    (LinearMap.range_eq_top.mpr ((LinearMap.injective_iff_surjective_of_finrank_eq_finrank rfl).mp
      (circleSumDeriv_injective h)))
lemma circleSum_local_antilipschitz {r : ℝ} {p : RealPlane} (h : r*Real.sin (p.2-p.1) ≠ 0) :
    ∃ s : Set RealPlane, IsOpen s ∧ p ∈ s ∧ ∃ K : ℝ≥0, AntilipschitzWith K (s.domRestrict (circleSum r)) := by
  let L := circleSumDerivEquiv h
  have hd : HasStrictFDerivAt (circleSum r) (L : RealPlane →L[ℝ] RealPlane) p := circleSum_strict r p
  obtain ⟨s,hp,hs,ha⟩ := hd.approximates_deriv_on_open_nhds
  refine ⟨s,hs,hp,_,ha.antilipschitz ?_⟩
  right
  have hpos := L.subsingleton_or_nnnorm_symm_pos.resolve_left (not_subsingleton RealPlane)
  exact half_lt_self (inv_pos.mpr hpos)
lemma realDirection_lipschitz : LipschitzWith 1 (fun t : ℝ => (Real.cos t,Real.sin t)) := by
  simpa using Real.lipschitzWith_cos.prodMk Real.lipschitzWith_sin
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology MeasureTheory
namespace EuclideanFiveColor
variable {t u : ℝ} (h : Real.sin (u-t) ≠ 0)
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology
open scoped NNReal
namespace EuclideanFiveColor
variable {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E] [CompleteSpace E]
end EuclideanFiveColor
end

noncomputable section
open Filter Topology Set MeasureTheory
open scoped NNReal
namespace EuclideanFiveColor
variable {t u : ℝ} (h : Real.sin (u-t) ≠ 0)
end EuclideanFiveColor
end

noncomputable section
open Filter Topology Set MeasureTheory
open scoped NNReal
namespace EuclideanFiveColor
variable {t u : ℝ} (h : Real.sin (u-t) ≠ 0)
end EuclideanFiveColor
end

noncomputable section
open MeasureTheory Filter Topology Set
namespace EuclideanFiveColor
def angleChartMeasure : Measure RealPlane :=
  volume.restrict (Ioc (0 : ℝ) (2*Real.pi) ×ˢ Ioc (0 : ℝ) (2*Real.pi))
instance : IsFiniteMeasure angleChartMeasure := by
  change IsFiniteMeasure (volume.restrict _)
  apply isFiniteMeasure_restrict.mpr
  apply ne_of_lt
  apply (measure_mono (Set.prod_mono Ioc_subset_Icc_self Ioc_subset_Icc_self)).trans_lt
  exact (isCompact_Icc.prod isCompact_Icc).measure_lt_top
end EuclideanFiveColor
end

noncomputable section
open MeasureTheory Filter Topology Set
open scoped NNReal ENNReal
namespace EuclideanFiveColor
end EuclideanFiveColor
end

noncomputable section
open MeasureTheory Filter Topology Set
open scoped NNReal
namespace EuclideanFiveColor
end EuclideanFiveColor
end

noncomputable section
open MeasureTheory Filter Topology Set
namespace EuclideanFiveColor
end EuclideanFiveColor
end

end OAI
