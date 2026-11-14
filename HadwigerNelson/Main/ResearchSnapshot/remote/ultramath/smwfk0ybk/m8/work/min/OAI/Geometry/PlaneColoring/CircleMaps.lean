import OAI.Geometry.PlaneColoring.Coloring
namespace OAI

noncomputable section
open Filter Topology Set
open scoped NNReal
namespace EuclideanFiveColor
abbrev RealPlane := ℝ × ℝ
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
