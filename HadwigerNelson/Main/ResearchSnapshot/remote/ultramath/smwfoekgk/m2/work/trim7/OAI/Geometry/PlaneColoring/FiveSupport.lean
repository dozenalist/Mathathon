import OAI.Geometry.PlaneColoring.Accumulation

namespace OAI

noncomputable section
open Set Filter Topology MeasureTheory
namespace EuclideanFiveColor
variable {k : ℕ} (c : ℂ → Fin k) (hc : Measurable c)
lemma palette_neighbor_real (hw : WeakColoring k c) (x : ℂ) (a : ℝ) (i : Fin k) :
    ∀ᵐt : ℝ∂volume,t∈liftPalette c hc (x+direction (a : Angles)) i → t∉liftPalette c hc x i := by
  let U : Set ℝ := {t | Real.sin (a-t)≠0}
  have hU : IsOpen U := isOpen_ne_fun (Real.continuous_sin.comp (continuous_const.sub continuous_id)) continuous_const
  have hu : ∀ᵐt : ℝ∂volume,t∈U := by
    filter_upwards [ae_sin_sub_ne_zero a] with t ht
    change Real.sin (a-t)≠0
    rwa [← neg_sub t a,Real.sin_neg,neg_ne_zero]
  have hh := palette_smooth_transport c hc hw (x := x) (z := x+direction (a : Angles)) hU (s := id) (t := fun _ => a)
    (ds := fun _ => 1) (dt := fun _ => 0) (fun t _ => hasDerivAt_id t)
    (fun t _ => hasDerivAt_const t a) (fun _ _ => one_ne_zero) (fun _ ht => ht) (fun t _ => ?_) i
  · exact (ae_restrict_iff' hU.measurableSet).mp hh |>.mp (hu.mono fun t ht hi => hi ht)
  · simp only [circleTarget,samplingParameter,add_sub_cancel_left,direction_realPlane,circleSum,one_smul,one_mul,id_eq]
    exact Prod.ext (add_comm _ _) (add_comm _ _)
lemma palette_neighbor_disjoint (hw : WeakColoring k c) (x : ℂ) (a : ℝ) :
    ∀ᵐt∂angularMeasure,Disjoint (palette c hc (x+direction (a : Angles)) t) (palette c hc x t) := by
  have hp (i : Fin k) : ∀ᵐt∂angularMeasure,t∈paletteSet c hc (x+direction (a : Angles)) i → t∉paletteSet c hc x i := by
    apply ae_angular_of_ae_line
    · simpa only [imp_iff_not_or,Set.compl_def,Set.union_def,Set.mem_ofPred_eq] using
        (paletteSet_measurable c hc (x+direction (a : Angles)) i).compl.union (paletteSet_measurable c hc x i).compl
    · exact palette_neighbor_real c hc hw x a i
  filter_upwards [ae_all_iff.mpr hp] with t ht
  exact Finset.disjoint_left.mpr fun i hi hj => ht i ((mem_palette c hc _ t i).mp hi) ((mem_palette c hc _ t i).mp hj)
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology MeasureTheory
namespace EuclideanFiveColor
variable {ι : Type*} [Fintype ι] [MeasurableSpace ι] [MeasurableSingletonClass ι]
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology MeasureTheory
namespace EuclideanFiveColor
variable (c : ℂ → Fin 5) (hc : Measurable c)
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology MeasureTheory
namespace EuclideanFiveColor
variable (c : ℂ → Fin 5) (hc : Measurable c)
end EuclideanFiveColor
end

noncomputable section
namespace EuclideanFiveColor.FiveComb
-- Independent finite arithmetic facts; the source labels are Z/5Z, represented by Fin 5.
def Adj (i j : Fin 5) : Prop := i+1=j ∨ j+1=i
instance (i j : Fin 5) : Decidable (Adj i j) := inferInstanceAs (Decidable (_∨_))
lemma neighbors : ∀i j : Fin 5, Adj i j → j=i-1 ∨ j=i+1 := by decide
end EuclideanFiveColor.FiveComb
end

noncomputable section
open Set Filter Topology MeasureTheory
namespace EuclideanFiveColor
variable (c : ℂ → Fin 5) (hc : Measurable c)
@[simp] lemma mem_fiveSupportList (x : ℂ) (a : ℝ) (i : Fin 5) :
    i∈fiveSupportList c hc x a ↔ a∈fiveSupport c hc x i := by simp only [fiveSupportList,Finset.mem_filter,Finset.mem_univ,true_and]
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology MeasureTheory
namespace EuclideanFiveColor
open scoped NNReal ENNReal
variable {k : ℕ} (c : ℂ → Fin k) (hc : Measurable c)
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology MeasureTheory
namespace EuclideanFiveColor
variable {k : ℕ} (c : ℂ → Fin k)
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology
namespace EuclideanFiveColor
variable {ι X : Type*} [Finite ι] [TopologicalSpace X]
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology MeasureTheory
namespace EuclideanFiveColor
end EuclideanFiveColor
end

end OAI
