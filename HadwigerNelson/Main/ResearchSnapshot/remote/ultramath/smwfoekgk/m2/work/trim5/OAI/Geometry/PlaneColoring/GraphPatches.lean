import OAI.Geometry.PlaneColoring.GraphCuts
import OAI.Geometry.PlaneColoring.HoleApproximation

namespace OAI

noncomputable section
open scoped Classical
open Set Topology ContinuousMap
universe u v
namespace EuclideanFiveColor
/-- Patch a map across separated bad fibers. Only the intervening values need lie in
 a contractible subspace; the map is kept on one closed set and made constant on the other. -/
theorem contractible_patch {X : Type u} {Y : Type v} [TopologicalSpace X]
    [TopologicalSpace Y] [NormalSpace X] (D : Set Y) [ContractibleSpace D]
    (f : C(X,Y)) {A B : Set X} (hA : IsClosed A) (hB : IsClosed B) (hd : Disjoint A B)
    (hg : ∀x,x∉A → x∉B → f x∈D) :
    ∃a : D, ∃g : C(X,Y), EqOn g (fun _ => a.val) A ∧ EqOn g f B ∧
      ∀x,g x=f x ∨ g x∈D := by
  obtain ⟨t,htB,htA,ht⟩ := exists_continuous_zero_one_of_isClosed hB hA hd.symm
  obtain ⟨a,⟨H⟩⟩ := id_nullhomotopic D
  let S : Fin 3 → Set X := ![{x | t x≤1/3},{x | 1/3≤t x ∧ t x≤2/3},{x | 2/3≤t x}]
  have hS : ∀i,IsClosed (S i) := by
    intro i
    fin_cases i
    · exact isClosed_le t.continuous continuous_const
    · exact (isClosed_le continuous_const t.continuous).inter
        (isClosed_le t.continuous continuous_const)
    · exact isClosed_le continuous_const t.continuous
  have hc : ⋃i,S i=univ := by
    apply iUnion_eq_univ_iff.mpr
    intro x
    by_cases h0 : t x≤1/3
    · exact ⟨0,h0⟩
    by_cases h1 : t x≤2/3
    · exact ⟨1,⟨(not_le.mp h0).le,h1⟩⟩
    · exact ⟨2,(not_le.mp h1).le⟩
  have hgood (x : S 1) : f x.val∈D := by
    apply hg
    · intro hx
      have he : t x.val=1 := htA hx
      have hh : t x.val≤2/3 := x.property.2
      linarith
    · intro hx
      have he : t x.val=0 := htB hx
      have hh : 1/3≤t x.val := x.property.1
      linarith
  have hτmem (x : S 1) : 3*t x.val-1∈unitInterval := by
    constructor
    · linarith [x.property.1]
    · linarith [x.property.2]
  let τ : C(S 1,unitInterval) := ⟨fun x => ⟨3*t x.val-1,hτmem x⟩,
    ((continuous_const.mul (t.continuous.comp continuous_subtype_val)).sub continuous_const).subtype_mk hτmem⟩
  let φ₁ : C(S 1,Y) := ⟨fun x => (H (τ x,⟨f x.val,hgood x⟩)).val,
    continuous_subtype_val.comp (H.continuous.comp (τ.continuous.prodMk
      ((f.continuous.comp continuous_subtype_val).subtype_mk hgood)))⟩
  let φ : ∀i,C(S i,Y) := fun i => Fin.cases (f.restrict (S 0))
    (fun j => Fin.cases φ₁ (fun j => ContinuousMap.const (S j.succ.succ) a.val) j) i
  have h01 (x : X) (h0 : x∈S 0) (h1 : x∈S 1) : φ 0 ⟨x,h0⟩=φ 1 ⟨x,h1⟩ := by
    have he : t x=1/3 := le_antisymm h0 h1.1
    have hτ : τ ⟨x,h1⟩=0 := by apply Subtype.ext; change 3*t x-1=0; rw [he]; norm_num
    change f x=(H (τ ⟨x,h1⟩,⟨f x,hgood ⟨x,h1⟩⟩)).val
    rw [hτ]
    exact congrArg Subtype.val (H.map_zero_left ⟨f x,hgood ⟨x,h1⟩⟩) |>.symm
  have h12 (x : X) (h1 : x∈S 1) (h2 : x∈S 2) : φ 1 ⟨x,h1⟩=φ 2 ⟨x,h2⟩ := by
    have he : t x=2/3 := le_antisymm h1.2 h2
    have hτ : τ ⟨x,h1⟩=1 := by apply Subtype.ext; change 3*t x-1=1; rw [he]; norm_num
    change (H (τ ⟨x,h1⟩,⟨f x,hgood ⟨x,h1⟩⟩)).val=a.val
    rw [hτ]
    exact congrArg Subtype.val (H.map_one_left ⟨f x,hgood ⟨x,h1⟩⟩)
  have hφ : ∀i j x (hi : x∈S i) (hj : x∈S j),φ i ⟨x,hi⟩=φ j ⟨x,hj⟩ := by
    intro i j x hi hj
    fin_cases i <;> fin_cases j
    · rfl
    · exact h01 x hi hj
    · have h0 : t x≤1/3 := hi; have h2 : 2/3≤t x := hj; linarith
    · exact (h01 x hj hi).symm
    · rfl
    · exact h12 x hi hj
    · have h0 : t x≤1/3 := hj; have h2 : 2/3≤t x := hi; linarith
    · exact (h12 x hj hi).symm
    · rfl
  refine ⟨a,closedCoverMap S hS hc φ hφ,?_,?_,?_⟩
  · intro x hx
    have hx2 : x∈S 2 := by change 2/3≤t x; rw [htA hx]; norm_num
    exact closedCoverMap_apply S hS hc φ hφ ⟨x,hx2⟩
  · intro x hx
    have hx0 : x∈S 0 := by change t x≤1/3; rw [htB hx]; norm_num
    exact closedCoverMap_apply S hS hc φ hφ ⟨x,hx0⟩
  · intro x
    obtain ⟨i,hi⟩ := iUnion_eq_univ_iff.mp hc x
    rw [closedCoverMap_apply S hS hc φ hφ ⟨x,hi⟩]
    fin_cases i
    · exact Or.inl rfl
    · exact Or.inr (H (τ ⟨x,hi⟩,⟨f x,hgood ⟨x,hi⟩⟩)).property
    · exact Or.inr a.property
end EuclideanFiveColor
end

noncomputable section
open scoped Classical
open Set Topology ContinuousMap
universe u v
namespace EuclideanFiveColor
end EuclideanFiveColor
end

noncomputable section
open scoped Classical
open Set Topology ContinuousMap
universe u
namespace EuclideanFiveColor
/-- A forest crossing graph yields an actual extension of the outer boundary over
its disk. This uses compact fiber separation and tree contraction, not graph words. -/
end EuclideanFiveColor
end

noncomputable section
open scoped Classical
open Set Topology
namespace EuclideanFiveColor
namespace HoleApprox
end HoleApprox
end EuclideanFiveColor
end

end OAI
