import OAI.Geometry.PlaneColoring.DiskAverages

namespace OAI

noncomputable section
open Set
open scoped NNReal ENNReal
namespace EuclideanFiveColor
lemma finite_packed_cover {X : Type*} [MetricSpace X] {A : Set X} (hA : TotallyBounded A)
    {ρ : ℝ} (hρ : 0<ρ) : ∃ C : Finset X, (↑C : Set X)⊆A ∧
      (∀ x∈A, ∃ c∈C, dist x c≤ρ) ∧
      (↑C : Set X).Pairwise (fun x y => ρ<dist x y) := by
  classical
  let e : ℝ≥0 := ⟨ρ,hρ.le⟩
  obtain ⟨D,_,hD,hcover⟩ := Metric.exists_finite_isCover_of_totallyBounded
    (s := A) (ε := e/2) (by exact div_ne_zero (ne_of_gt (show (0 : ℝ≥0)<e from hρ)) (by norm_num) : e/2≠0) hA
  have hp : Metric.packingNumber e A≠⊤ := by
    have hh := (Metric.packingNumber_two_mul_le_externalCoveringNumber (e/2) A).trans
      hcover.externalCoveringNumber_le_encard
    have he : 2*(e/2)=e := by ring
    rw [he] at hh
    exact ne_top_of_le_ne_top hD.encard_lt_top.ne hh
  let C := Metric.maximalSeparatedSet e A
  have hCf : C.Finite := Set.encard_ne_top_iff.mp (by
    change (Metric.maximalSeparatedSet e A).encard≠⊤
    rwa [Metric.encard_maximalSeparatedSet hp])
  refine ⟨hCf.toFinset,?_,?_,?_⟩
  · simpa only [Set.Finite.coe_toFinset] using (Metric.maximalSeparatedSet_subset (ε := e) (A := A))
  · intro x hx
    obtain ⟨c,hc,hd⟩ := Metric.isCover_maximalSeparatedSet hp hx
    refine ⟨c,hCf.mem_toFinset.mpr hc,?_⟩
    change edist x c≤(e : ℝ≥0∞) at hd
    exact (ENNReal.ofReal_le_coe (b := e)).mp (by simpa only [edist_dist] using hd)
  · intro x hx y hy hne
    have hd := Metric.isSeparated_maximalSeparatedSet (ε := e) (A := A)
      (hCf.mem_toFinset.mp hx) (hCf.mem_toFinset.mp hy) hne
    exact (ENNReal.coe_lt_ofReal (a := e)).mp (by simpa only [edist_dist] using hd)
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology MeasureTheory Function
namespace EuclideanFiveColor
variable {k : ℕ} {c : ℂ → Fin k}
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology MeasureTheory
namespace EuclideanFiveColor
variable {k : ℕ} {c : ℂ → Fin k}
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology
namespace PlanarCover
end PlanarCover
end

noncomputable section
open Set MeasureTheory MeasureTheory.Measure
namespace PlanarCover
end PlanarCover
end

noncomputable section
open scoped Classical
open Set MeasureTheory
namespace PlanarCover
end PlanarCover
end

end OAI
