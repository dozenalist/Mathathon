import OAI.Geometry.PlaneColoring.ContinuumLimits
import OAI.Geometry.PlaneColoring.GraphPatches

namespace OAI

noncomputable section
open scoped Classical
open Set Filter Topology TopologicalSpace MeasureTheory
namespace EuclideanFiveColor
/-- Compactness and the angular theorems force all sufficiently fine crossing graphs
to be forests. This is about actual compact bridges, not assumed interface data. -/
theorem eventually_forest_of_bridges {c : ℂ → Fin 5} (hc : Measurable c)
    (hw : WeakColoring 5 c) {x : ℂ} {ρ : ℝ} (hρ : 0<ρ)
    (D : ℕ → SimpleGraph (Fin 5)) {r ε : ℕ → ℝ}
    (hr : Tendsto r atTop (𝓝 0)) (hε : Tendsto ε atTop (𝓝 0)) (hpos : ∀n,0<ε n)
    {H E : ℕ → Set ℂ} (hE : Tendsto (fun n => volume (E n)) atTop (𝓝 0))
    (hnear : ∀n z q,q∈H n → dist z q=1 → z∈E n)
    {α : ℝ} (hα : 0<α)
    (hbridge : ∀n i j,(D n).Adj i j → ∃K : NonemptyCompacts ℂ,
      (K : Set ℂ)⊆Metric.closedBall x ρ ∧ IsPreconnected (K : Set ℂ) ∧
      (∃a∈K,dist a x≤r n) ∧ ((K : Set ℂ)∩Metric.sphere x ρ).Nonempty ∧
      (∀q∈K,q∉H n → α<diskAverage c (ε n) i q) ∧
      (∀q∈K,q∉H n → α<diskAverage c (ε n) j q)) :
    ∀ᶠ n in atTop,(D n).IsAcyclic := by
  have he : ∀i j : Fin 5,∀ᶠ n in atTop,(D n).Adj i j → CommonInterface c x i j := by
    intro i j
    by_cases hcommon : CommonInterface c x i j
    · exact Eventually.of_forall fun _ _ => hcommon
    · have hn : ∀ᶠ n in atTop,¬(D n).Adj i j := by
        by_contra hnot
        have hfreq : ∃ᶠ n in atTop,(D n).Adj i j := hnot
        obtain ⟨φ,hφ,hφD⟩ := subseq_forall_of_frequently (x:=fun n : ℕ => n) (p:=fun n => (D n).Adj i j) tendsto_id hfreq
        choose K hK hconn ha hout hi hj using fun n => hbridge (φ n) i j (hφD n)
        choose a haK har using ha
        have halim : Tendsto a atTop (𝓝 x) := by
          rw [tendsto_iff_dist_tendsto_zero]
          exact squeeze_zero (fun _ => dist_nonneg) har (hr.comp hφ)
        exact hcommon (commonInterface_of_compact_sequence hc hw hρ K hK hconn a haK halim hout
          (hε.comp hφ) (fun n => hpos (φ n)) (hE.comp hφ) (fun n => hnear (φ n)) hα i j hi hj)
      exact hn.mono fun _ hn hd => False.elim (hn hd)
  have hall : ∀ᶠ n in atTop,∀i j : Fin 5,(D n).Adj i j → CommonInterface c x i j :=
    eventually_all.mpr fun i => eventually_all.mpr (he i)
  filter_upwards [hall] with n hn
  exact commonInterface_graph_acyclic hc hw x (D n) hn
end EuclideanFiveColor
end

noncomputable section
open scoped Classical
open Set Filter Topology TopologicalSpace MeasureTheory ContinuousMap
namespace EuclideanFiveColor
end EuclideanFiveColor
end

noncomputable section
open scoped Classical
open Set Topology ContinuousMap
universe u
namespace EuclideanFiveColor
end EuclideanFiveColor
end

noncomputable section
open scoped Classical
open Set Filter Topology MeasureTheory ContinuousMap
namespace EuclideanFiveColor
namespace HoleApprox
end HoleApprox
end EuclideanFiveColor
end

noncomputable section
open scoped Classical
open Set Topology
namespace EuclideanFiveColor
end EuclideanFiveColor
end

noncomputable section
open scoped Classical
open Set Filter Topology MeasureTheory ContinuousMap
namespace EuclideanFiveColor
/-- A global graph approximation, with actual small exceptional disks.
All fields will be constructed, not postulated as coloring hypotheses. -/
structure FullApprox (c : ℂ → Fin 5) (α t : ℝ) where
  ε : ℝ
  ε_pos : 0<ε
  ε_lt : ε<t
  disks : Finset MarkedDisk
  positive : ∀d∈disks,0<d.radius
  disjoint : (disks : Set MarkedDisk).Pairwise (fun a b => Disjoint a.closedBall b.closedBall)
  sum_lt : (∑d∈disks,d.radius)<t
  map : C(Metric.closedBall (0:ℂ) 5,GraphSpace (⊤ : SimpleGraph (Fin 5)))
  agrees : ∀z : Metric.closedBall (0:ℂ) 5,z.val∉diskHoles disks →
    (map z).val=thresholdMap c ε α z.val
end EuclideanFiveColor
end

end OAI
