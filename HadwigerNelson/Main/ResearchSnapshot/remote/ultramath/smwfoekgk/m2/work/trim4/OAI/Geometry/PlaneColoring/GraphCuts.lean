import OAI.Geometry.PlaneColoring.DiskExtension

namespace OAI

noncomputable section
open scoped Classical
open Set Topology ContinuousMap
universe u
namespace EuclideanFiveColor
lemma graphEdgePoint_index {V : Type u} {i j k : V} {t : ℝ}
    (h : graphEdgePoint i j t k ≠ 0) : k=i ∨ k=j := by
  by_contra hh
  simp only [not_or] at hh
  exact h (by simp [graphEdgePoint_apply,hh.1,hh.2])
lemma graphRealization_positive_adj {V : Type u} {G : SimpleGraph V} {p : V → ℝ}
    (hp : p∈graphRealization G) {i j : V} (hne : i≠j) (hi : 0<p i) (hj : 0<p j) : G.Adj i j := by
  obtain ⟨a,b,hab,t,ht,rfl⟩ := hp
  have ha := graphEdgePoint_index (ne_of_gt hi)
  have hb := graphEdgePoint_index (ne_of_gt hj)
  rcases ha with rfl|rfl <;> rcases hb with rfl|rfl
  · exact (hne rfl).elim
  · exact hab.resolve_left hne
  · exact (hab.resolve_left hne.symm).symm
  · exact (hne rfl).elim
lemma graphRealization_pair_le {V : Type u} {G : SimpleGraph V} {p : V → ℝ}
    (hp : p∈graphRealization G) {i j : V} (hne : i≠j) : p i+p j≤1 := by
  obtain ⟨a,b,hab,t,ht,rfl⟩ := hp
  simp only [graphEdgePoint_apply]
  split_ifs <;> subst_vars <;> first | contradiction | nlinarith [ht.1,ht.2]

def graphCutRealization {V : Type u} (T : SimpleGraph V) : Set (V → ℝ) :=
  {p | p∈graphRealization (⊤ : SimpleGraph V) ∧ ∀ i j, i≠j → ¬T.Adj i j →
    p≠graphEdgePoint i j (1/2)}
abbrev GraphCutSpace {V : Type u} (T : SimpleGraph V) := ↥(graphCutRealization T)
lemma graphRealization_subset_cut {V : Type u} (T : SimpleGraph V) :
    graphRealization T⊆graphCutRealization T := by
  intro p hp
  refine ⟨graphRealization_mono le_top hp,?_⟩
  intro i j hne hn he
  apply hn
  apply graphRealization_positive_adj hp hne
  · rw [he]; norm_num [graphEdgePoint_apply,hne,hne.symm]
  · rw [he]; norm_num [graphEdgePoint_apply,hne,hne.symm]
lemma graphCut_dominant {V : Type u} {T : SimpleGraph V} {p : V → ℝ}
    (hp : p∈graphCutRealization T) (hn : p∉graphRealization T) : ∃i,1/2<p i := by
  obtain ⟨i,j,hij,t,ht,he⟩ := hp.1
  have hne : i≠j := by
    intro h; apply hn; exact ⟨i,j,Or.inl h,t,ht,he⟩
  have hadj : ¬T.Adj i j := by
    intro h; apply hn; exact ⟨i,j,Or.inr h,t,ht,he⟩
  have htm : t≠1/2 := by intro h; exact hp.2 i j hne hadj (he.trans (by rw [h]))
  rcases lt_or_gt_of_ne htm with hl|hr
  · refine ⟨i,?_⟩; rw [he]; simp [graphEdgePoint_apply,hne]; linarith
  · refine ⟨j,?_⟩; rw [he]; simpa [graphEdgePoint_apply,hne.symm] using hr
lemma graphCut_dominant_unique {V : Type u} {T : SimpleGraph V} {p : V → ℝ}
    (hp : p∈graphCutRealization T) {i j : V} (hi : 1/2<p i) (hj : 1/2<p j) : i=j := by
  by_contra hne
  have hh := graphRealization_pair_le hp.1 hne
  linarith

def graphCutRetract {V : Type u} (T : SimpleGraph V) (p : GraphCutSpace T) : V → ℝ :=
  if h : p.val∈graphRealization T then p.val else graphVertex (graphCut_dominant p.property h).choose
lemma graphCutRetract_tree {V : Type u} {T : SimpleGraph V} (p : GraphCutSpace T)
    (hp : p.val∈graphRealization T) : graphCutRetract T p=p.val := by
  simp [graphCutRetract,hp]
lemma graphCutRetract_dominant {V : Type u} {T : SimpleGraph V} (p : GraphCutSpace T)
    (hp : p.val∉graphRealization T) {i : V} (hi : 1/2<p.val i) : graphCutRetract T p=graphVertex i := by
  rw [graphCutRetract,dite_eq_right hp]
  congr 1
  exact graphCut_dominant_unique p.property (graphCut_dominant p.property hp).choose_spec hi
lemma graphCutRetract_mem {V : Type u} (T : SimpleGraph V) (p : GraphCutSpace T) :
    graphCutRetract T p∈graphRealization T := by
  unfold graphCutRetract
  split
  · assumption
  · exact graphVertex_mem _ _
/-- The closed half of a deleted edge, viewed inside the cut graph. -/
def graphCutStub {V : Type u} (T : SimpleGraph V) (i j : V) : Set (GraphCutSpace T) :=
  {p | i≠j ∧ ¬T.Adj i j ∧ p.val∈graphEdgePoint i j '' Icc (0:ℝ) (1/2)}
lemma graphCutStub_retract {V : Type u} {T : SimpleGraph V} {i j : V}
    {p : GraphCutSpace T} (hp : p∈graphCutStub T i j) : graphCutRetract T p=graphVertex i := by
  obtain ⟨hne,hadj,t,ht,he⟩ := hp
  have he' := he.symm
  have htm : t<1/2 := lt_of_le_of_ne ht.2 (by
    intro h; exact p.property.2 i j hne hadj (he'.trans (by rw [h])))
  by_cases hT : p.val∈graphRealization T
  · rw [graphCutRetract_tree p hT]
    have ht0 : t=0 := by
      by_contra hh
      have hp1 : 0<p.val i := by rw [he']; simp [graphEdgePoint_apply,hne]; linarith
      have hp2 : 0<p.val j := by rw [he']; simp [graphEdgePoint_apply,hne.symm]; exact lt_of_le_of_ne ht.1 (Ne.symm hh)
      exact hadj (graphRealization_positive_adj hT hne hp1 hp2)
    rw [he',ht0,graphEdgePoint_zero]
  · apply graphCutRetract_dominant p hT
    rw [he']; simp [graphEdgePoint_apply,hne]; linarith
lemma graphCut_cover {V : Type u} {T : SimpleGraph V} (p : GraphCutSpace T) :
    p.val∈graphRealization T ∨ ∃i j,p∈graphCutStub T i j := by
  by_cases h : p.val∈graphRealization T
  · exact Or.inl h
  right
  obtain ⟨i,j,hij,t,ht,he⟩ := p.property.1
  have hne : i≠j := by intro hh; exact h ⟨i,j,Or.inl hh,t,ht,he⟩
  have hadj : ¬T.Adj i j := by intro hh; exact h ⟨i,j,Or.inr hh,t,ht,he⟩
  by_cases ht' : t≤1/2
  · exact ⟨i,j,hne,hadj,t,⟨ht.1,ht'⟩,he.symm⟩
  · refine ⟨j,i,hne.symm,fun hh => hadj hh.symm,1-t,⟨by linarith [ht.2],by linarith⟩,?_⟩
    exact (graphEdgePoint_swap i j t).symm.trans he.symm
end EuclideanFiveColor
end

noncomputable section
open scoped Classical
open Set Topology ContinuousMap
universe u
namespace EuclideanFiveColor


/-- Removing the non-tree edge midpoints leaves a contractible graph (tree with half-open stubs). -/
end EuclideanFiveColor
end

noncomputable section
open scoped Classical
open Set Topology ContinuousMap
universe u v
namespace EuclideanFiveColor
/-- A compact connected fiber joins both designated boundary sets. -/

/-- All finitely many non-crossing bad fibers can simultaneously be separated,
 with the prescribed inner/outer closed sets on opposite sides. -/
end EuclideanFiveColor
end

end OAI
