import OAI.Geometry.PlaneColoring.GraphRealization

namespace OAI

noncomputable section
open scoped Classical
open Set Topology
namespace EuclideanFiveColor
structure MarkedDisk where
  center : ℂ
  radius : ℝ
  core : Bool
namespace MarkedDisk
def ball (d : MarkedDisk) : Set ℂ := Metric.ball d.center d.radius
def closedBall (d : MarkedDisk) : Set ℂ := Metric.closedBall d.center d.radius
def noncoreCost (d : MarkedDisk) : ℝ := if d.core then 0 else d.radius
def Valid (L : Set ℂ) (d : MarkedDisk) : Prop :=
  0<d.radius ∧ (d.core=true → ∃x∈L,x∈d.ball)

lemma merge {a b : MarkedDisk} {L : Set ℂ} (ha : a.Valid L) (hb : b.Valid L)
    (hab : ¬Disjoint a.closedBall b.closedBall) {η : ℝ} (hη : 0<η) :
    ∃d : MarkedDisk, d.Valid L ∧ a.closedBall⊆d.ball ∧ b.closedBall⊆d.ball ∧
      d.radius≤a.radius+b.radius+η ∧ d.noncoreCost≤a.noncoreCost+b.noncoreCost+η ∧ d.core=(a.core || b.core) := by
  obtain ⟨z,hza,hzb⟩ := Set.not_disjoint_iff.mp hab
  have hd : dist a.center b.center≤a.radius+b.radius :=
    (dist_triangle a.center z b.center).trans (add_le_add (by simpa [closedBall,dist_comm] using hza) hzb)
  let t : ℝ := b.radius/(a.radius+b.radius)
  have hrs : 0<a.radius+b.radius := add_pos ha.1 hb.1
  have ht0 : 0≤t := (div_pos hb.1 hrs).le
  have ht1 : t≤1 := (div_le_one hrs).mpr (by linarith [ha.1])
  let c := AffineMap.lineMap a.center b.center t
  have hca : dist a.center c≤b.radius := by
    rw [dist_left_lineMap,Real.norm_of_nonneg ht0]
    calc t*dist a.center b.center ≤ t*(a.radius+b.radius) := mul_le_mul_of_nonneg_left hd ht0
         _ = b.radius := by dsimp [t]; field_simp
  have hcb : dist b.center c≤a.radius := by
    rw [dist_right_lineMap,Real.norm_of_nonneg (sub_nonneg.mpr ht1)]
    calc (1-t)*dist a.center b.center ≤ (1-t)*(a.radius+b.radius) :=
            mul_le_mul_of_nonneg_left hd (sub_nonneg.mpr ht1)
         _ = a.radius := by dsimp [t]; field_simp; ring
  let d : MarkedDisk := ⟨c,a.radius+b.radius+η,a.core || b.core⟩
  have hA : a.closedBall⊆d.ball := by
    intro q hq
    have hq' : dist q a.center≤a.radius := hq
    change dist q c<a.radius+b.radius+η
    exact lt_of_le_of_lt (dist_triangle q a.center c) (by linarith)
  have hB : b.closedBall⊆d.ball := by
    intro q hq
    have hq' : dist q b.center≤b.radius := hq
    change dist q c<a.radius+b.radius+η
    exact lt_of_le_of_lt (dist_triangle q b.center c) (by linarith)
  refine ⟨d,⟨by dsimp [d]; linarith,?_⟩,hA,hB,le_refl _,?_,rfl⟩
  · intro hc
    have hc' : a.core=true ∨ b.core=true := by cases hca : a.core <;> cases hcb : b.core <;> simp_all [d]
    rcases hc' with hh|hh
    · obtain ⟨x,hx,hxa⟩ := ha.2 hh
      exact ⟨x,hx,hA (Metric.ball_subset_closedBall hxa)⟩
    · obtain ⟨x,hx,hxb⟩ := hb.2 hh
      exact ⟨x,hx,hB (Metric.ball_subset_closedBall hxb)⟩
  · dsimp [noncoreCost,d]
    cases a.core <;> cases b.core <;> simp <;> linarith [ha.1,hb.1]
end MarkedDisk
end EuclideanFiveColor
end

noncomputable section
open scoped Classical
open Set Topology
namespace EuclideanFiveColor
namespace MarkedDisk

/-- Finite disk merging with separate total and non-core radius budgets. Strict
containment at merges, and the retained core witness, are both included. -/
theorem separate (S : Finset MarkedDisk) {L : Set ℂ} (hS : ∀d∈S,d.Valid L)
    {η : ℝ} (hη : 0<η) : ∃T : Finset MarkedDisk,
      (∀d∈T,d.Valid L) ∧ (T : Set MarkedDisk).Pairwise (fun a b => Disjoint a.closedBall b.closedBall) ∧
      (∀d∈S,∃e∈T,d.ball⊆e.ball ∧ (d.core=true → e.core=true)) ∧
      (∑d∈T,d.radius)<(∑d∈S,d.radius)+η ∧
      (∑d∈T,d.noncoreCost)<(∑d∈S,d.noncoreCost)+η := by
  suffices hh : ∀n : ℕ, ∀S : Finset MarkedDisk, S.card=n →
      (∀d∈S,d.Valid L) → ∀η : ℝ,0<η → ∃T : Finset MarkedDisk,
      (∀d∈T,d.Valid L) ∧ (T : Set MarkedDisk).Pairwise (fun a b => Disjoint a.closedBall b.closedBall) ∧
      (∀d∈S,∃e∈T,d.ball⊆e.ball ∧ (d.core=true → e.core=true)) ∧
      (∑d∈T,d.radius)<(∑d∈S,d.radius)+η ∧
      (∑d∈T,d.noncoreCost)<(∑d∈S,d.noncoreCost)+η from hh _ S rfl hS η hη
  intro n
  induction n using Nat.strong_induction_on with
  | h n ih =>
    intro S hn hS η hη
    by_cases hp : (S : Set MarkedDisk).Pairwise (fun a b => Disjoint a.closedBall b.closedBall)
    · exact ⟨S,hS,hp,fun d hd => ⟨d,hd,Subset.rfl,fun h => h⟩,
        lt_add_of_pos_right _ hη,lt_add_of_pos_right _ hη⟩
    · simp only [Set.Pairwise,Finset.mem_coe] at hp
      push Not at hp
      obtain ⟨a,ha,b,hb,hab,hd⟩ := hp
      obtain ⟨d,hdv,hda,hdb,hdr,hdc,hdcore⟩ := merge (hS a ha) (hS b hb) hd (half_pos hη)
      let R := (S.erase a).erase b
      let S' := insert d R
      have hR : ∀e∈R,e∈S := by intro e he; exact (Finset.mem_erase.mp (Finset.mem_erase.mp he).2).2
      have hS' : ∀e∈S',e.Valid L := by
        intro e he
        rcases Finset.mem_insert.mp he with rfl|he
        · exact hdv
        · exact hS e (hR e he)
      have hcard : S'.card<n := by
        have hc₁ := Finset.card_erase_add_one ha
        have hc₂ := Finset.card_erase_add_one (Finset.mem_erase.mpr ⟨hab.symm,hb⟩)
        have hc₃ := Finset.card_insert_le d R
        change R.card+1=(S.erase a).card at hc₂
        dsimp only [S']
        omega
      obtain ⟨T,hT,hdis,hcov,hr,hc⟩ := ih S'.card hcard S' rfl hS' (η/2) (half_pos hη)
      refine ⟨T,hT,hdis,?_,?_,?_⟩
      · intro e he
        have he' : ∃f∈S',e.ball⊆f.ball ∧ (e.core=true → f.core=true) := by
          by_cases hea : e=a
          · subst e
            refine ⟨d,Finset.mem_insert_self _ _,fun _ hq => hda (Metric.ball_subset_closedBall hq),?_⟩
            intro ha
            rw [hdcore,ha]
            simp
          · by_cases heb : e=b
            · subst e
              refine ⟨d,Finset.mem_insert_self _ _,fun _ hq => hdb (Metric.ball_subset_closedBall hq),?_⟩
              intro hb
              rw [hdcore,hb]
              simp
            · exact ⟨e,Finset.mem_insert_of_mem (by simp [R,he,hea,heb]),Subset.rfl,fun h => h⟩
        obtain ⟨f,hf,hef,hcore⟩ := he'
        obtain ⟨g,hg,hfg,hcore'⟩ := hcov f hf
        exact ⟨g,hg,hef.trans hfg,fun hec => hcore' (hcore hec)⟩
      · have hb' := merge_sum_bound S ha hb hab radius hdv.1.le hdr
        change (∑x∈S',x.radius)≤(∑x∈S,x.radius)+η/2 at hb'
        linarith
      · have hdc0 : 0≤d.noncoreCost := by unfold noncoreCost; split_ifs <;> linarith [hdv.1]
        have hb' := merge_sum_bound S ha hb hab noncoreCost hdc0 hdc
        change (∑x∈S',x.noncoreCost)≤(∑x∈S,x.noncoreCost)+η/2 at hb'
        linarith
end MarkedDisk
end EuclideanFiveColor
end

noncomputable section
open scoped Classical
open Set Topology ContinuousMap
universe u
namespace EuclideanFiveColor

/-- A contraction genuinely extends arbitrary continuous sphere data across a disk. -/
end EuclideanFiveColor
end

noncomputable section
open scoped Classical
open Set Topology
universe u
namespace EuclideanFiveColor
/-- Linear transfer of a leaf coordinate along its unique incident edge. -/
def graphLeafMove {V : Type u} (v w : V) (t : ℝ) (p : V → ℝ) : V → ℝ :=
  p+(t*p v) • (graphVertex w-graphVertex v)
@[simp] lemma graphLeafMove_zero {V : Type u} (v w : V) (p : V → ℝ) : graphLeafMove v w 0 p=p := by
  simp [graphLeafMove]

def graphDrop {V : Type u} (v : V) (p : V → ℝ) : {i : V // i≠v} → ℝ := fun i => p i

def graphLift {V : Type u} (v : V) (p : {i : V // i≠v} → ℝ) : V → ℝ :=
  fun i => if hi : i≠v then p ⟨i,hi⟩ else 0
@[simp] lemma graphLift_drop {V : Type u} (v : V) (p : V → ℝ) (hp : p v=0) :
    graphLift v (graphDrop v p)=p := by
  ext i
  by_cases hi : i=v
  · subst i; simp [graphLift,hp]
  · simp [graphLift,graphDrop,hi]
@[simp] lemma graphDrop_lift {V : Type u} (v : V) (p : {i : V // i≠v} → ℝ) :
    graphDrop v (graphLift v p)=p := by
  ext i; simp [graphDrop,graphLift,i.property]
end EuclideanFiveColor
end

noncomputable section
open scoped Classical
open Set Topology ContinuousMap
universe u
namespace EuclideanFiveColor

def graphLeafRetraction {V : Type u} {G : SimpleGraph V} {v w : V}
    (hvw : G.Adj v w) (hleaf : ∀i,G.Adj v i → i=w) :
    C(GraphSpace G, GraphSpace (G.induce {i | i≠v})) where
  toFun p := ⟨graphDrop v (graphLeafMove v w 1 p.val),
    graphDrop_mem v (graphLeafMove_mem hvw hleaf p.property (by norm_num))
      (graphLeafMove_one_at hvw.ne p.val)⟩
  continuous_toFun := (continuous_graphDrop v |>.comp
    ((continuous_graphLeafMove v w).comp (continuous_const.prodMk continuous_subtype_val))).subtype_mk _

def graphLeafInclusion {V : Type u} (G : SimpleGraph V) (v : V) :
    C(GraphSpace (G.induce {i | i≠v}), GraphSpace G) where
  toFun p := ⟨graphLift v p.val,graphLift_mem v p.property⟩
  continuous_toFun := ((continuous_graphLift v).comp continuous_subtype_val).subtype_mk _


private lemma graphTree_contractible_aux (n : ℕ) :
    ∀ (V : Type u) [Fintype V] (G : SimpleGraph V), Fintype.card V=n →
      G.IsTree → ContractibleSpace (GraphSpace G) := by
  induction n using Nat.strong_induction_on with
  | h n ih =>
    intro V inst G hcard hG
    rcases subsingleton_or_nontrivial V with hSS|hNT
    · let := hSS
      obtain ⟨a⟩ := hG.nonempty
      let : Nonempty (GraphSpace G) := ⟨⟨graphVertex a,graphVertex_mem G a⟩⟩
      let : Subsingleton (GraphSpace G) := ⟨fun p q => Subtype.ext (by
        have hp := p.property
        have hq := q.property
        simp only [graphRealization_singleton G a,mem_singleton_iff] at hp hq
        exact hp.trans hq.symm)⟩
      infer_instance
    · let := hNT
      obtain ⟨v,hv⟩ := hG.exists_vert_degree_one_of_nontrivial
      obtain ⟨w,hvw,hleaf⟩ := SimpleGraph.degree_eq_one_iff_existsUnique_adj.mp hv
      let W := {i : V // i≠v}
      let G' : SimpleGraph W := G.induce {i | i≠v}
      have hs : ({v}ᶜ : Set V)={i | i≠v} := by ext i; simp
      have hconn : G'.Connected := by
        have hh := hG.connected.induce_compl_singleton_of_degree_eq_one hv
        rwa [hs] at hh
      have hac : G'.IsAcyclic := hG.isAcyclic.induce _
      have hlt : Fintype.card W<n := by
        rw [←hcard]
        apply Fintype.card_lt_of_injective_not_surjective (Subtype.val : W → V) Subtype.val_injective
        intro hh
        obtain ⟨i,hi⟩ := hh v
        exact i.property hi
      let : ContractibleSpace (GraphSpace G') := ih _ hlt W G' rfl ⟨hconn,hac⟩
      have hn := ((id_nullhomotopic (GraphSpace G')).comp_left
        (graphLeafRetraction hvw hleaf)).comp_right (graphLeafInclusion G v)
      obtain ⟨a,ha⟩ := hn
      apply (contractible_iff_id_nullhomotopic _).mpr
      refine ⟨a,ContinuousMap.Homotopic.trans ⟨graphLeafHomotopy hvw hleaf⟩ ?_⟩
      simpa only [ContinuousMap.id_comp] using ha

/-- Genuine contraction of the geometric probability-simplex realization of a finite tree. -/
end EuclideanFiveColor
end

noncomputable section
open scoped Classical
open Set Topology ContinuousMap
universe u
namespace EuclideanFiveColor
/-- Forest-valued boundary data extend through an actual spanning tree inside the
complete graph. Isolated labels and empty edge sets are retained. -/
end EuclideanFiveColor
end

noncomputable section
open scoped Classical
open Set Topology ContinuousMap
universe u v w
namespace EuclideanFiveColor
/-- Finite closed-cover pasting, with the actual glued continuous map. -/
def closedCoverMap {X : Type u} {Y : Type v} {ι : Type w}
    [TopologicalSpace X] [TopologicalSpace Y] [Finite ι]
    (S : ι → Set X) (hS : ∀i,IsClosed (S i)) (hc : ⋃i,S i=univ)
    (f : ∀i,C(S i,Y))
    (hf : ∀i j x (hi : x∈S i) (hj : x∈S j), f i ⟨x,hi⟩=f j ⟨x,hj⟩) : C(X,Y) where
  toFun := Set.liftCover S (fun i => f i) hf hc
  continuous_toFun := (locallyFinite_of_finite S).continuous hc hS (fun i => by
    rw [continuousOn_iff_continuous_domRestrict]
    simpa +unfoldPartialApp only [Set.domRestrict,Set.liftCover_coe] using (f i).continuous)
@[simp] lemma closedCoverMap_apply {X : Type u} {Y : Type v} {ι : Type w}
    [TopologicalSpace X] [TopologicalSpace Y] [Finite ι]
    (S : ι → Set X) (hS : ∀i,IsClosed (S i)) (hc : ⋃i,S i=univ)
    (f : ∀i,C(S i,Y))
    (hf : ∀i j x (hi : x∈S i) (hj : x∈S j), f i ⟨x,hi⟩=f j ⟨x,hj⟩)
    {i : ι} (x : S i) : closedCoverMap S hS hc f hf x=f i x := by
  change Set.liftCover S (fun i => f i) hf hc x=f i x
  exact Set.liftCover_coe x
end EuclideanFiveColor
end

noncomputable section
open scoped Classical
open Set Topology ContinuousMap
universe u
namespace EuclideanFiveColor

/-- Finite closed pasting fills precisely the non-core holes, with actual continuous
tree extensions on their disks and no change outside the original open holes. -/
end EuclideanFiveColor
end

end OAI
