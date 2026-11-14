import OAI.Geometry.PlaneColoring.DiskExtension

namespace OAI

noncomputable section
open scoped Classical
open Set Topology
namespace EuclideanFiveColor
namespace MarkedDisk
lemma radius_le_sum {S : Finset MarkedDisk} (hS : ∀d∈S,0≤d.radius) {d : MarkedDisk} (hd : d∈S) :
    d.radius≤∑e∈S,e.radius := Finset.single_le_sum hS hd
lemma noncoreCost_nonneg {d : MarkedDisk} (hd : 0≤d.radius) : 0≤d.noncoreCost := by
  unfold noncoreCost
  split <;> positivity
lemma noncore_radius_le_sum {S : Finset MarkedDisk} (hS : ∀d∈S,0≤d.radius)
    {d : MarkedDisk} (hd : d∈S) (hc : d.core=false) : d.radius≤∑e∈S,e.noncoreCost := by
  have hh := Finset.single_le_sum (fun e he => noncoreCost_nonneg (hS e he)) hd
  simpa [noncoreCost,hc] using hh
lemma sphere_avoids_holes {S : Finset MarkedDisk}
    (hdis : (S : Set MarkedDisk).Pairwise (fun a b => Disjoint a.closedBall b.closedBall))
    {d : MarkedDisk} (hd : d∈S) {z : ℂ} (hz : z∈Metric.sphere d.center d.radius) : z∉diskHoles S := by
  rintro hh
  obtain ⟨e,he,hze⟩ := mem_diskHoles.mp hh
  by_cases hde : d=e
  · subst e
    have hh' : dist z d.center<d.radius := hze
    have hz' : dist z d.center=d.radius := hz
    linarith
  · exact Set.disjoint_left.mp (hdis hd he hde) (Metric.sphere_subset_closedBall hz)
      (Metric.ball_subset_closedBall hze)
lemma closedBall_near_core {L : Set ℂ} {d : MarkedDisk} (hd : d.Valid L) (hc : d.core=true) :
    ∃x∈L,d.closedBall⊆Metric.ball x (2*d.radius) := by
  obtain ⟨x,hx,hxd⟩ := hd.2 hc
  refine ⟨x,hx,fun z hz => ?_⟩
  have hx' : dist d.center x<d.radius := by simpa only [ball,Metric.mem_ball,dist_comm] using hxd
  exact lt_of_le_of_lt (dist_triangle z d.center x) (by dsimp [closedBall] at hz; change dist z d.center≤d.radius at hz; linarith)
lemma sphere_norm_bound {d : MarkedDisk} {R : ℝ}
    (hmeet : (d.closedBall∩Metric.closedBall (0:ℂ) R).Nonempty) {z : ℂ}
    (hz : z∈Metric.sphere d.center d.radius) : dist z 0≤2*d.radius+R := by
  obtain ⟨a,ha,haR⟩ := hmeet
  have hza : dist z a≤2*d.radius := calc
    dist z a≤dist z d.center+dist d.center a := dist_triangle _ _ _
    _ ≤ 2*d.radius := by
      have hh : dist z d.center=d.radius := hz
      have ha' : dist d.center a≤d.radius := by simpa only [closedBall,Metric.mem_closedBall,dist_comm] using ha
      linarith
  exact (dist_triangle z a 0).trans (by change dist a 0≤R at haR; linarith)
end MarkedDisk
end EuclideanFiveColor
end

noncomputable section
open scoped Classical
open Set Topology
namespace EuclideanFiveColor
namespace MarkedDisk
end MarkedDisk
end EuclideanFiveColor
end

noncomputable section
open scoped Classical
open Set Filter Topology MeasureTheory ContinuousMap
namespace EuclideanFiveColor
open MarkedDisk
end EuclideanFiveColor
end

noncomputable section
open scoped Classical ENNReal
open Set Filter Topology MeasureTheory
namespace EuclideanFiveColor
end EuclideanFiveColor
end

noncomputable section
open scoped Classical
open Set Filter Topology MeasureTheory ContinuousMap
namespace EuclideanFiveColor
/-- Data actually constructed by the small-hole lemma. -/
structure HoleApprox (c : ℂ → Fin 5) (α : ℝ) (L : Finset ℂ) (t : ℝ) where
  ε : ℝ
  ε_pos : 0<ε
  ε_lt : ε<t
  disks : Finset MarkedDisk
  valid : ∀d∈disks,d.Valid (L : Set ℂ)
  disjoint : (disks : Set MarkedDisk).Pairwise (fun a b => Disjoint a.closedBall b.closedBall)
  sum_lt : (∑d∈disks,d.radius)<t
  map : C(↥(Metric.closedBall (0:ℂ) 7 \ coreHoles disks),GraphSpace (⊤ : SimpleGraph (Fin 5)))
  agrees : ∀z : ↥(Metric.closedBall (0:ℂ) 7 \ coreHoles disks),z.val∉diskHoles disks →
    (map z).val=thresholdMap c ε α z.val
namespace HoleApprox
end HoleApprox
end EuclideanFiveColor
end

end OAI
