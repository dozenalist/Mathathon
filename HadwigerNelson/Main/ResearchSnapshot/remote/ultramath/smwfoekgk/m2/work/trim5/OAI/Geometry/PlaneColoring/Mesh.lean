import OAI.Geometry.PlaneColoring.FullApproximation

namespace OAI

noncomputable section
open scoped Classical
open Set Filter Topology MeasureTheory
namespace EuclideanFiveColor
/-- A point of a connected set with a distant partner can be moved to the
boundary of its (unique) small hole. Pairwise disjoint closed disks make the
new point lie outside every open hole. No path regularity is required. -/
lemma connected_escape_holes {S : Finset MarkedDisk} {t : ℝ}
    (hS : ∀d∈S,0≤d.radius)
    (hdis : (S : Set MarkedDisk).Pairwise (fun a b => Disjoint a.closedBall b.closedBall))
    (hsum : (∑d∈S,d.radius)<t) {K : Set ℂ} (hK : IsPreconnected K)
    {a b : ℂ} (ha : a∈K) (hb : b∈K) (hab : 2*t<dist a b) :
    ∃a'∈K,a'∉diskHoles S ∧ dist a a'≤2*t := by
  have ht : 0<t := (Finset.sum_nonneg hS).trans_lt hsum
  by_cases haS : a∈diskHoles S
  · obtain ⟨d,hd,had⟩ := mem_diskHoles.mp haS
    have hrad : d.radius<t := (MarkedDisk.radius_le_sum hS hd).trans_lt hsum
    have had' : dist a d.center<d.radius := had
    have hbd : d.radius<dist b d.center := by
      by_contra! hh
      have htri := dist_triangle a d.center b
      rw [dist_comm d.center b] at htri
      linarith
    obtain ⟨p,hp,hpd⟩ := hK.intermediate_value ha hb
      (continuous_id.dist continuous_const).continuousOn ⟨had'.le,hbd.le⟩
    refine ⟨p,hp,MarkedDisk.sphere_avoids_holes hdis hd hpd,?_⟩
    change dist p d.center=d.radius at hpd
    have htri := dist_triangle a d.center p
    rw [dist_comm d.center p,hpd] at htri
    linarith
  · exact ⟨a,ha,haS,by simpa using (mul_pos (by norm_num : (0:ℝ)<2) ht).le⟩

/-- Positive averages on shrinking disks force every limit center into the
actual measure support of that color. -/
lemma support_of_positive_diskAverage_limit {k : ℕ} {c : ℂ → Fin k} (hc : Measurable c)
    {ε : ℕ → ℝ} (hε : Tendsto ε atTop (𝓝 0)) {a : ℕ → ℂ} {x : ℂ}
    (ha : Tendsto a atTop (𝓝 x)) (i : Fin k)
    (hp : ∀n,0<diskAverage c (ε n) i (a n)) : x∈spatialSupport c i := by
  apply (Measure.mem_support_iff_forall x).mpr
  intro U hU
  obtain ⟨r,hr,hrU⟩ := Metric.mem_nhds_iff.mp hU
  have hnear : ∀ᶠ n in atTop,dist (a n) x<r/2 := ha.eventually (Metric.ball_mem_nhds x (by positivity))
  have hsmall : ∀ᶠ n in atTop,ε n<r/2 := hε.eventually (gt_mem_nhds (by positivity : (0:ℝ)<r/2))
  obtain ⟨n,han,hεn⟩ := (hnear.and hsmall).exists
  have hsub : Metric.ball (a n) (ε n)⊆U := by
    intro z hz
    apply hrU
    have hh : dist z (a n)<ε n := hz
    have htri := dist_triangle z (a n) x
    change dist z x<r
    linarith
  have hpos := hp n
  rw [diskAverage_area hc] at hpos
  apply pos_iff_ne_zero.mpr
  intro hzero
  have hzero' : volume (U∩{z | c z=i})=0 := by
    simpa only [spatialSupport,Measure.restrict_apply' (measurableSet_eq_fun hc measurable_const)] using hzero
  have hball : volume (Metric.ball (a n) (ε n)∩{z | c z=i})=0 :=
    measure_mono_null (inter_subset_inter_left _ hsub) hzero'
  simp only [Measure.real,hball,ENNReal.toReal_zero,zero_div,lt_self_iff_false] at hpos
end EuclideanFiveColor
end

noncomputable section
open scoped Classical
open Set Filter Topology MeasureTheory ContinuousMap
namespace EuclideanFiveColor
namespace FullApprox

/-- A continuous graph approximant cannot have positive-coordinate connected
sets of macroscopic diameter at every shrinking scale. This is the manuscript
mesh argument, with connectedness replacing the stronger path assumption. -/
end FullApprox
end EuclideanFiveColor
end

end OAI
