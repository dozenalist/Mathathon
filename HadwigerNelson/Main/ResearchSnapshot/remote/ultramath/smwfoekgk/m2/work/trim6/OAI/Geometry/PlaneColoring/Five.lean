import OAI.Geometry.PlaneColoring.BorelTransfer
import OAI.Geometry.PlaneColoring.Mesh

namespace OAI

noncomputable section
open scoped Classical
open Set Topology ContinuousMap
namespace EuclideanFiveColor
lemma graphRealization_positive_three {V : Type*} {G : SimpleGraph V} {p : V → ℝ}
    (hp : p∈graphRealization G) {i j k : V} (hi : 0<p i) (hj : 0<p j) (hk : 0<p k) :
    i=j ∨ i=k ∨ j=k := by
  obtain ⟨a,b,_,t,_,rfl⟩ := hp
  have hpos (v : V) (hv : 0<graphEdgePoint a b t v) : v=a ∨ v=b := by
    by_contra! hh
    simp [graphEdgePoint_apply,hh.1,hh.2] at hv
  rcases hpos i hi with rfl|rfl <;> rcases hpos j hj with rfl|rfl <;>
    rcases hpos k hk with rfl|rfl <;> simp

/-- The actual positive-coordinate component cover contradicts the planar cover
obstruction whenever every connected positive region has diameter at most two. -/
theorem graph_map_small_mesh_impossible
    (F : C(Metric.closedBall (0:ℂ) 5,GraphSpace (⊤ : SimpleGraph (Fin 5))))
    (hmesh : ∀(i : Fin 5) (K : Set ℂ),IsPreconnected K → K⊆Metric.closedBall (0:ℂ) 5 →
      (∀z : Metric.closedBall (0:ℂ) 5,z.val∈K → 0<(F z).val i) →
      ∀x∈K,∀y∈K,dist x y≤2) : False := by
  let Q := Metric.closedBall (0:ℂ) 5
  have : LocallyPathConnectedSpace Q := (convex_closedBall (0:ℂ) (5:ℝ)).locallyPathConnectedSpace
  let U : Fin 5 → Set Q := fun i => {z | 0<(F z).val i}
  have hU (i : Fin 5) : IsOpen (U i) :=
    isOpen_lt continuous_const ((continuous_apply i).comp (continuous_subtype_val.comp F.continuous))
  let I := {p : Fin 5 × Set Q // ∃x : Q,p.2=connectedComponentIn (U p.1) x}
  let W : I → Set Q := fun p => p.val.2
  have hW (p : I) : IsOpen (W p) := by
    obtain ⟨x,hx⟩ := p.property
    change IsOpen p.val.2
    rw [hx]
    exact (hU _).connectedComponentIn
  have hpos {p : I} {z : Q} (hz : z∈W p) : 0<(F z).val p.val.1 := by
    obtain ⟨x,hx⟩ := p.property
    change z∈p.val.2 at hz
    rw [hx] at hz
    exact connectedComponentIn_subset (U p.val.1) x hz
  have heq {p q : I} {z : Q} (hpq : p.val.1=q.val.1) (hp : z∈W p) (hq : z∈W q) : p=q := by
    apply Subtype.ext
    apply Prod.ext hpq
    obtain ⟨x,hx⟩ := p.property
    obtain ⟨y,hy⟩ := q.property
    change z∈p.val.2 at hp
    change z∈q.val.2 at hq
    rw [hx,hpq] at hp
    rw [hy] at hq
    rw [hx,hy,hpq,connectedComponentIn_eq hp,connectedComponentIn_eq hq]
  apply PlanarCover.compact_open_cover_impossible Metric.ball_subset_closedBall
    (isCompact_closedBall (0:ℂ) 5) W hW ?_ ?_ ?_
  · intro z
    have he : ∃i,0<(F z).val i := by
      by_contra! hh
      have hsum := Finset.sum_nonpos (s := (Finset.univ : Finset (Fin 5))) (fun i _ => hh i)
      rw [graphRealization_sum (F z).property] at hsum
      norm_num at hsum
    obtain ⟨i,hi⟩ := he
    exact ⟨⟨(i,connectedComponentIn (U i) z),⟨z,rfl⟩⟩,mem_connectedComponentIn hi⟩
  · intro z p q r hp hq hr
    rcases graphRealization_positive_three (F z).property (hpos hp) (hpos hq) (hpos hr) with h|h|h
    · exact Or.inl (heq h hp hq)
    · exact Or.inr (Or.inl (heq h hp hr))
    · exact Or.inr (Or.inr (heq h hq hr))
  · intro p x hx y hy
    obtain ⟨z,hz⟩ := p.property
    let K : Set ℂ := Subtype.val '' W p
    have hK : IsPreconnected K := by
      apply IsPreconnected.image _ _ continuous_subtype_val.continuousOn
      change IsPreconnected p.val.2
      rw [hz]
      exact isPreconnected_connectedComponentIn
    have hsub : K⊆Q := by rintro a ⟨b,_,rfl⟩; exact b.property
    have hprob : ∀z : Q,z.val∈K → 0<(F z).val p.val.1 := by
      rintro z ⟨b,hb,he⟩
      have hh : b=z := Subtype.ext he
      subst b
      exact hpos hb
    have hh := hmesh p.val.1 K hK hsub hprob x.val ⟨x,hx,rfl⟩ y.val ⟨y,hy,rfl⟩
    simpa only [dist_eq_norm] using hh
end EuclideanFiveColor
end

noncomputable section
open scoped Classical
open Set Filter Topology MeasureTheory
namespace EuclideanFiveColor

/-- No unrestricted five-coloring separates all unit-distance pairs in the Euclidean plane. -/
theorem no_proper_five_coloring : ¬ ∃ c : ℂ → Fin 5, ProperColoring 5 c := by
  rintro ⟨c,hc⟩
  exact no_proper_five_coloring_algebraic ⟨fun x => c x, fun x y h => hc x y h⟩
end EuclideanFiveColor
end

end OAI
