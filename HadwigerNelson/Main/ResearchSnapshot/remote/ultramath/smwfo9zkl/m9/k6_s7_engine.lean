import OAI.Geometry.PlaneColoring.PlanarCovers
import OAI.Geometry.PlaneColoring.GraphRealization

/-!
# §7 of the five-colour proof at six labels: the label-blind engine

This file isolates, and machine-checks, the two ingredients of §7 ("Extraction of common
exclusion continua") that the printed proof states only for five labels:

* `card_le_two_of_isClique_of_acyclic` -- the *conversion step*.  In §7 the thresholded
  vector `q^ε(z)` is shown to be a point of the 1-skeleton because the set of labels with
  `p_i^ε(z) > α` is a clique in the transition graph `Γ` of a nearby centre, and `Γ` is a
  forest there.  A clique in a forest has at most two vertices.  No palette-cardinality
  bound is used: a palette of three labels produces three positive coordinates, but the
  *thresholded* set is a clique in a forest and therefore still has at most two.

* `graph_map_small_mesh_impossible_generic` / `graph_map_large_positive_generic` -- the cover obstruction
  engine (`PlanarCover.compact_open_cover_impossible`, already generic in the label type)
  combined with the fact that a point of the graph realization of a complete graph on *any*
  label type has at most two positive barycentric coordinates.

The statements are given for an arbitrary finite label type `V`, hence for `Fin 6`.
-/

namespace OAI

noncomputable section
open scoped Classical
open Set Topology ContinuousMap
namespace EuclideanFiveColor

/-- At a point of the graph realization of any simple graph, at most two coordinates are
positive.  (The `Fin 5` instance is `graphRealization_positive_three`.) -/
lemma graphRealization_positive_two {V : Type*} {G : SimpleGraph V} {p : V → ℝ}
    (hp : p ∈ graphRealization G) {i j l : V} (hi : 0 < p i) (hj : 0 < p j) (hl : 0 < p l) :
    i = j ∨ i = l ∨ j = l := by
  obtain ⟨a, b, _, t, _, rfl⟩ := hp
  have hpos (v : V) (hv : 0 < graphEdgePoint a b t v) : v = a ∨ v = b := by
    by_contra! hh
    simp [graphEdgePoint_apply, hh.1, hh.2] at hv
  rcases hpos i hi with rfl | rfl <;> rcases hpos j hj with rfl | rfl <;>
    rcases hpos l hl with rfl | rfl <;> simp

/-- **The conversion step of §7.**  A finite set of labels that is a clique in an acyclic
transition graph has at most two elements. -/
theorem card_le_two_of_isClique_of_acyclic {V : Type*} {G : SimpleGraph V} (hG : G.IsAcyclic)
    {s : Finset V} (hcl : ∀ i ∈ s, ∀ j ∈ s, i ≠ j → G.Adj i j) : s.card ≤ 2 := by
  by_contra h
  have h2 : 2 < s.card := by omega
  obtain ⟨i, hi, j, hj, l, hl, hij, hil, hjl⟩ := Finset.two_lt_card.mp h2
  have e1 : G.Adj i j := hcl i hi j hj hij
  have e2 : G.Adj j l := hcl j hj l hl hjl
  have e3 : G.Adj l i := (hcl i hi l hl hil).symm
  have hcf := hG.cliqueFree (n := 3) (by norm_num)
  refine hcf {i, j, l} ⟨?_, by simp [hij, hil, hjl]⟩
  intro a ha b hb hab
  simp only [Finset.coe_insert, Finset.coe_singleton, Set.mem_insert_iff,
    Set.mem_singleton_iff] at ha hb
  rcases ha with rfl | rfl | rfl <;> rcases hb with rfl | rfl | rfl <;>
    simp_all [SimpleGraph.adj_comm]

/-- §7's geometric engine, for an arbitrary finite label type: a continuous map of the disk
into the graph realization of a complete graph that is "graph valued" (its positive-coordinate
regions have diameter at most two) is impossible.  This is the multiplicity-two cover
obstruction of Lemma 7.5 applied to the component cover of Lemma 7.6. -/
theorem graph_map_small_mesh_impossible_generic {V : Type*} [Fintype V]
    (F : C(Metric.closedBall (0:ℂ) 5, GraphSpace (⊤ : SimpleGraph V)))
    (hmesh : ∀ (i : V) (K : Set ℂ), IsPreconnected K → K ⊆ Metric.closedBall (0:ℂ) 5 →
      (∀ z : Metric.closedBall (0:ℂ) 5, z.val ∈ K → 0 < (F z).val i) →
      ∀ x ∈ K, ∀ y ∈ K, dist x y ≤ 2) : False := by
  let Q := Metric.closedBall (0:ℂ) 5
  have : LocallyPathConnectedSpace Q := (convex_closedBall (0:ℂ) (5:ℝ)).locallyPathConnectedSpace
  let U : V → Set Q := fun i => {z | 0 < (F z).val i}
  have hU (i : V) : IsOpen (U i) :=
    isOpen_lt continuous_const ((continuous_apply i).comp (continuous_subtype_val.comp F.continuous))
  let I := {p : V × Set Q // ∃ x : Q, p.2 = connectedComponentIn (U p.1) x}
  let W : I → Set Q := fun p => p.val.2
  have hW (p : I) : IsOpen (W p) := by
    obtain ⟨x, hx⟩ := p.property
    change IsOpen p.val.2
    rw [hx]
    exact (hU _).connectedComponentIn
  have hpos {p : I} {z : Q} (hz : z ∈ W p) : 0 < (F z).val p.val.1 := by
    obtain ⟨x, hx⟩ := p.property
    change z ∈ p.val.2 at hz
    rw [hx] at hz
    exact connectedComponentIn_subset (U p.val.1) x hz
  have heq {p q : I} {z : Q} (hpq : p.val.1 = q.val.1) (hp : z ∈ W p) (hq : z ∈ W q) : p = q := by
    apply Subtype.ext
    apply Prod.ext hpq
    obtain ⟨x, hx⟩ := p.property
    obtain ⟨y, hy⟩ := q.property
    change z ∈ p.val.2 at hp
    change z ∈ q.val.2 at hq
    rw [hx, hpq] at hp
    rw [hy] at hq
    rw [hx, hy, hpq, connectedComponentIn_eq hp, connectedComponentIn_eq hq]
  apply PlanarCover.compact_open_cover_impossible Metric.ball_subset_closedBall
    (isCompact_closedBall (0:ℂ) 5) W hW ?_ ?_ ?_
  · intro z
    have he : ∃ i, 0 < (F z).val i := by
      by_contra! hh
      have hsum := Finset.sum_nonpos (s := (Finset.univ : Finset V)) (fun i _ => hh i)
      rw [graphRealization_sum (F z).property] at hsum
      norm_num at hsum
    obtain ⟨i, hi⟩ := he
    exact ⟨⟨(i, connectedComponentIn (U i) z), ⟨z, rfl⟩⟩, mem_connectedComponentIn hi⟩
  · intro z p q r hp hq hr
    rcases graphRealization_positive_two (F z).property (hpos hp) (hpos hq) (hpos hr) with h | h | h
    · exact Or.inl (heq h hp hq)
    · exact Or.inr (Or.inl (heq h hp hr))
    · exact Or.inr (Or.inr (heq h hq hr))
  · intro p x hx y hy
    obtain ⟨z, hz⟩ := p.property
    let K : Set ℂ := Subtype.val '' W p
    have hK : IsPreconnected K := by
      apply IsPreconnected.image _ _ continuous_subtype_val.continuousOn
      change IsPreconnected p.val.2
      rw [hz]
      exact isPreconnected_connectedComponentIn
    have hsub : K ⊆ Q := by rintro a ⟨b, _, rfl⟩; exact b.property
    have hprob : ∀ z : Q, z.val ∈ K → 0 < (F z).val p.val.1 := by
      rintro z ⟨b, hb, he⟩
      have hh : b = z := Subtype.ext he
      subst hh
      exact hpos hb
    have hh := hmesh p.val.1 K hK hsub hprob x.val ⟨x, hx, rfl⟩ y.val ⟨y, hy, rfl⟩
    simpa only [dist_eq_norm] using hh

/-- Conversely: §7 must produce a positive-coordinate region of diameter greater than two.
At five labels this is `graph_map_large_positive`; the label count never enters. -/
lemma graph_map_large_positive_generic {V : Type*} [Fintype V]
    (F : C(Metric.closedBall (0:ℂ) 5, GraphSpace (⊤ : SimpleGraph V))) :
    ∃ i : V, ∃ K : Set ℂ, IsPreconnected K ∧ K ⊆ Metric.closedBall (0:ℂ) 5 ∧
      (∀ z : Metric.closedBall (0:ℂ) 5, z.val ∈ K → 0 < (F z).val i) ∧
      ∃ x ∈ K, ∃ y ∈ K, 2 < dist x y := by
  by_contra! h
  exact graph_map_small_mesh_impossible_generic F h

/-- The six-label instance, named for the record. -/
theorem k6_graph_map_large_positive
    (F : C(Metric.closedBall (0:ℂ) 5, GraphSpace (⊤ : SimpleGraph (Fin 6)))) :
    ∃ i : Fin 6, ∃ K : Set ℂ, IsPreconnected K ∧ K ⊆ Metric.closedBall (0:ℂ) 5 ∧
      (∀ z : Metric.closedBall (0:ℂ) 5, z.val ∈ K → 0 < (F z).val i) ∧
      ∃ x ∈ K, ∃ y ∈ K, 2 < dist x y :=
  graph_map_large_positive_generic F

/-- The six-label instance of the conversion step. -/
theorem k6_card_le_two_of_isClique_of_acyclic {G : SimpleGraph (Fin 6)} (hG : G.IsAcyclic)
    {s : Finset (Fin 6)} (hcl : ∀ i ∈ s, ∀ j ∈ s, i ≠ j → G.Adj i j) : s.card ≤ 2 :=
  card_le_two_of_isClique_of_acyclic hG hcl

end EuclideanFiveColor
end
end OAI

namespace OAI
noncomputable section
open scoped Classical
namespace EuclideanFiveColor

/-! ### The thresholding step (paper (7.4)) at six labels

The paper's `α < 1/5` is the special case `k = 5` of `α < 1/k`: the denominator of the
renormalised threshold vector is at least `1 − kα`.  Below is the `k = 6` instance, i.e. the
only *numeric* `k`-dependence of §7. -/

namespace K6

/-- Paper (7.4) at six labels. -/
def thresholdWeight (c : ℂ → Fin 6) (ε α : ℝ) (q : ℂ) (i : Fin 6) : ℝ :=
  max (diskAverage c ε i q - α) 0

def thresholdTotal (c : ℂ → Fin 6) (ε α : ℝ) (q : ℂ) : ℝ :=
  ∑ i, thresholdWeight c ε α q i

def thresholdMap (c : ℂ → Fin 6) (ε α : ℝ) (q : ℂ) (i : Fin 6) : ℝ :=
  thresholdWeight c ε α q i / thresholdTotal c ε α q

/-- `α < 1/6` is exactly what positivity of the denominator needs at six labels. -/
lemma thresholdTotal_pos {c : ℂ → Fin 6} (hc : Measurable c) {ε α : ℝ}
    (hε : 0 < ε) (hα : α < 1/6) (q : ℂ) : 0 < thresholdTotal c ε α q := by
  have hs := diskAverage_sum hc hε q
  have hh : 1 - 6*α ≤ thresholdTotal c ε α q := by
    have h' := Finset.sum_le_sum (s := (Finset.univ : Finset (Fin 6)))
      (fun i _ => le_max_left (diskAverage c ε i q - α) 0)
    simpa [thresholdTotal, thresholdWeight, Finset.sum_sub_distrib, hs] using h'
  linarith

lemma thresholdMap_pos {c : ℂ → Fin 6} (hc : Measurable c) {ε α : ℝ}
    (hε : 0 < ε) (hα : α < 1/6) (q : ℂ) (i : Fin 6) :
    0 < thresholdMap c ε α q i ↔ α < diskAverage c ε i q := by
  rw [thresholdMap, div_pos_iff_of_pos_right (thresholdTotal_pos hc hε hα q)]
  simp [thresholdWeight]

lemma thresholdMap_sum {c : ℂ → Fin 6} (hc : Measurable c) {ε α : ℝ}
    (hε : 0 < ε) (hα : α < 1/6) (q : ℂ) : ∑ i, thresholdMap c ε α q i = 1 := by
  unfold thresholdMap
  rw [← Finset.sum_div]
  exact div_self (thresholdTotal_pos hc hε hα q).ne'

/-- The six-label conversion step: if the above-threshold label set is a clique in an acyclic
transition graph, the thresholded vector lies in the 1-skeleton. -/
theorem threshold_support_card_le_two {c : ℂ → Fin 6} {ε α : ℝ}
    {G : SimpleGraph (Fin 6)} (hG : G.IsAcyclic) (q : ℂ)
    (hcl : ∀ i, α < diskAverage c ε i q → ∀ j, α < diskAverage c ε j q → i ≠ j → G.Adj i j) :
    (Finset.univ.filter (fun i => α < diskAverage c ε i q)).card ≤ 2 := by
  refine card_le_two_of_isClique_of_acyclic hG (fun i hi j hj hij => ?_)
  simp only [Finset.mem_filter, Finset.mem_univ, true_and] at hi hj
  exact hcl i hi j hj hij

end K6

end EuclideanFiveColor
end
end OAI
