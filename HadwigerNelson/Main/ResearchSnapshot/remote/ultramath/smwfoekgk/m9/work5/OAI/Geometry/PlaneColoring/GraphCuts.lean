import OAI.Geometry.PlaneColoring.DiskExtension

namespace OAI

noncomputable section
open scoped Classical
open Set Topology ContinuousMap
universe u
namespace EuclideanFiveColor
def graphCutRealization {V : Type u} (T : SimpleGraph V) : Set (V → ℝ) :=
  {p | p∈graphRealization (⊤ : SimpleGraph V) ∧ ∀ i j, i≠j → ¬T.Adj i j →
    p≠graphEdgePoint i j (1/2)}
abbrev GraphCutSpace {V : Type u} (T : SimpleGraph V) := ↥(graphCutRealization T)
def graphCutRetract {V : Type u} (T : SimpleGraph V) (p : GraphCutSpace T) : V → ℝ :=
  if h : p.val∈graphRealization T then p.val else graphVertex (graphCut_dominant p.property h).choose
lemma graphCutRetract_mem {V : Type u} (T : SimpleGraph V) (p : GraphCutSpace T) :
    graphCutRetract T p∈graphRealization T := by
  unfold graphCutRetract
  split
  · assumption
  · exact graphVertex_mem _ _
end EuclideanFiveColor
end

noncomputable section
open scoped Classical
open Set Topology ContinuousMap
universe u
namespace EuclideanFiveColor
def graphCutRetraction {V : Type u} [Finite V] (T : SimpleGraph V) :
    C(GraphCutSpace T,GraphSpace T) where
  toFun p := ⟨graphCutRetract T p,graphCutRetract_mem T p⟩
  continuous_toFun := (continuous_graphCutRetract T).subtype_mk _
def graphCutInclusion {V : Type u} (T : SimpleGraph V) : C(GraphSpace T,GraphCutSpace T) where
  toFun p := ⟨p.val,graphRealization_subset_cut T p.property⟩
  continuous_toFun := continuous_subtype_val.subtype_mk _
/-- Removing the non-tree edge midpoints leaves a contractible graph (tree with half-open stubs). -/
theorem graphCut_contractible {V : Type u} [Fintype V] {T : SimpleGraph V} (hT : T.IsTree) :
    ContractibleSpace (GraphCutSpace T) := by
  let := graphTree_contractible hT
  have hn := ((id_nullhomotopic (GraphSpace T)).comp_left
    (graphCutRetraction T)).comp_right (graphCutInclusion T)
  obtain ⟨a,ha⟩ := hn
  apply (contractible_iff_id_nullhomotopic _).mpr
  refine ⟨a,ContinuousMap.Homotopic.trans ⟨graphCutHomotopy T⟩ ?_⟩
  simpa only [ContinuousMap.id_comp] using ha
end EuclideanFiveColor
end

noncomputable section
open scoped Classical
open Set Topology ContinuousMap
universe u v
namespace EuclideanFiveColor
/-- A compact connected fiber joins both designated boundary sets. -/
def FiberCrosses {X : Type u} {Y : Type v} [TopologicalSpace X]
    (f : X → Y) (A B : Set X) (b : Y) : Prop :=
  ∃K : Set X, IsCompact K ∧ IsConnected K ∧ K⊆f ⁻¹' {b} ∧
    (K∩A).Nonempty ∧ (K∩B).Nonempty
lemma compact_fiber_partition {X : Type u} {Y : Type v} [TopologicalSpace X]
    [TopologicalSpace Y] [CompactSpace X] [T2Space X] [T1Space Y]
    (f : C(X,Y)) {A B : Set X} (hA : IsClosed A) (hB : IsClosed B) (b : Y)
    (hn : ¬FiberCrosses f A B b) :
    ∃K₀ K₁ : Set X, IsCompact K₀ ∧ IsCompact K₁ ∧ Disjoint K₀ K₁ ∧
      K₀∪K₁=f ⁻¹' {b} ∧ Disjoint K₀ B ∧ Disjoint K₁ A := by
  let F : Set X := f ⁻¹' {b}
  have hF : IsClosed F := isClosed_singleton.preimage f.continuous
  let : CompactSpace F := isCompact_iff_compactSpace.mp hF.isCompact
  let I : Set F := Subtype.val ⁻¹' A
  let O : Set F := Subtype.val ⁻¹' B
  have hI : IsCompact I := (hA.preimage continuous_subtype_val).isCompact
  have hO : IsCompact O := (hB.preimage continuous_subtype_val).isCompact
  have hno : ∀x∈I,Disjoint (connectedComponent x) O := by
    intro x hx
    apply disjoint_left.mpr
    intro y hy hOy
    apply hn
    refine ⟨Subtype.val '' connectedComponent x,
      isClosed_connectedComponent.isCompact.image continuous_subtype_val,
      isConnected_connectedComponent.image _ continuous_subtype_val.continuousOn,?_,?_,?_⟩
    · rintro z ⟨w,hw,rfl⟩; exact w.property
    · exact ⟨x.val,⟨⟨x,mem_connectedComponent,rfl⟩,hx⟩⟩
    · exact ⟨y.val,⟨⟨y,hy,rfl⟩,hOy⟩⟩
  obtain ⟨Z₀,Z₁,hZ₀,hZ₁,hd,hcov,hIZ,hOZ⟩ := compact_component_partition hI hO hno
  refine ⟨Subtype.val '' Z₀,Subtype.val '' Z₁,hZ₀.image continuous_subtype_val,
    hZ₁.image continuous_subtype_val,?_,?_,?_,?_⟩
  · apply disjoint_left.mpr
    rintro x ⟨y,hy,rfl⟩ ⟨z,hz,he⟩
    have hh : z=y := Subtype.ext he
    subst z
    exact disjoint_left.mp hd hy hz
  · rw [←image_union,hcov]
    ext x
    constructor
    · rintro ⟨y,_,rfl⟩; exact y.property
    · intro hx; exact ⟨⟨x,hx⟩,mem_univ _,rfl⟩
  · apply disjoint_left.mpr
    rintro z ⟨x,hx,rfl⟩ hz
    exact disjoint_left.mp hd hx (hOZ hz)
  · apply disjoint_left.mpr
    rintro z ⟨x,hx,rfl⟩ hz
    exact disjoint_left.mp hd (hIZ hz) hx

/-- All finitely many non-crossing bad fibers can simultaneously be separated,
 with the prescribed inner/outer closed sets on opposite sides. -/
theorem finite_fiber_separation {X : Type u} {Y : Type v} [TopologicalSpace X]
    [TopologicalSpace Y] [CompactSpace X] [T2Space X] [T1Space Y]
    (f : C(X,Y)) {A B : Set X} (hA : IsClosed A) (hB : IsClosed B) (hd : Disjoint A B)
    (S : Finset Y) (hn : ∀b∈S,¬FiberCrosses f A B b) :
    ∃C₀ C₁ : Set X, IsCompact C₀ ∧ IsCompact C₁ ∧ Disjoint C₀ C₁ ∧
      A⊆C₀ ∧ B⊆C₁ ∧ f ⁻¹' (↑S : Set Y)⊆C₀∪C₁ := by
  choose K₀ K₁ hK using (fun b : S => compact_fiber_partition f hA hB b.val (hn b.val b.property))
  let Z₀ : Set X := ⋃b : S,K₀ b
  let Z₁ : Set X := ⋃b : S,K₁ b
  have hz₀ : IsCompact Z₀ := isCompact_iUnion fun b => (hK b).1
  have hz₁ : IsCompact Z₁ := isCompact_iUnion fun b => (hK b).2.1
  have hsub₀ (b : S) : K₀ b⊆f ⁻¹' {b.val} := by
    rw [←(hK b).2.2.2.1]; exact subset_union_left
  have hsub₁ (b : S) : K₁ b⊆f ⁻¹' {b.val} := by
    rw [←(hK b).2.2.2.1]; exact subset_union_right
  have h01 : Disjoint Z₀ Z₁ := by
    apply disjoint_left.mpr
    intro x hx hy
    obtain ⟨b,hb⟩ := mem_iUnion.mp hx
    obtain ⟨c,hc⟩ := mem_iUnion.mp hy
    have he : b=c := Subtype.ext ((hsub₀ b hb).symm.trans (hsub₁ c hc))
    subst c
    exact disjoint_left.mp (hK b).2.2.1 hb hc
  have h0B : Disjoint Z₀ B := by
    apply disjoint_left.mpr
    intro x hx hB
    obtain ⟨b,hb⟩ := mem_iUnion.mp hx
    exact disjoint_left.mp (hK b).2.2.2.2.1 hb hB
  have h1A : Disjoint Z₁ A := by
    apply disjoint_left.mpr
    intro x hx hA
    obtain ⟨b,hb⟩ := mem_iUnion.mp hx
    exact disjoint_left.mp (hK b).2.2.2.2.2 hb hA
  refine ⟨A∪Z₀,B∪Z₁,hA.isCompact.union hz₀,hB.isCompact.union hz₁,?_,subset_union_left,subset_union_left,?_⟩
  · exact disjoint_union_left.mpr ⟨disjoint_union_right.mpr ⟨hd,h1A.symm⟩,
      disjoint_union_right.mpr ⟨h0B,h01⟩⟩
  · intro x hx
    let b : S := ⟨f x,hx⟩
    have hh : x∈K₀ b∪K₁ b := by rw [(hK b).2.2.2.1]; rfl
    rcases hh with hh|hh
    · exact Or.inl (Or.inr (mem_iUnion.mpr ⟨b,hh⟩))
    · exact Or.inr (Or.inr (mem_iUnion.mpr ⟨b,hh⟩))
end EuclideanFiveColor
end

end OAI
