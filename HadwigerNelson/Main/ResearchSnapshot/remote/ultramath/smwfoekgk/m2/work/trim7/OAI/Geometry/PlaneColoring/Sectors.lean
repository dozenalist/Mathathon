import OAI.Geometry.PlaneColoring.AngularBoundary
import OAI.Geometry.PlaneColoring.Moser

namespace OAI

noncomputable section
open Set Filter Topology MeasureTheory
open scoped RealInnerProductSpace
namespace EuclideanFiveColor
def triangleEdge (i : Fin 3) : Finset (Fin 5) := if i=0 then {0,1} else if i=1 then {1,2} else {2,0}
lemma triangle_majority_cover : ∀s : Fin 3 → Bool,∃b : Bool,
    ∀j∈({0,1,2} : Finset (Fin 5)),∃i : Fin 3,s i=b ∧ j∈triangleEdge i := by decide
lemma triangle_outsider : ∀s : Fin 3 → Bool,∀b : Bool,
    (∀j∈({0,1,2} : Finset (Fin 5)),∃i : Fin 3,s i=b ∧ j∈triangleEdge i) →
    ∀j : Fin 5,(∀i : Fin 3,s i=b → j∉triangleEdge i) → j=3 ∨ j=4 := by decide
lemma ApproachingContinuum.side_strip {x : ℂ} {K : Set ℂ} {v e : ℂ}
    (h : ApproachingContinuum x K v) (he : ‖e‖=1) (hn : ⟪e,v⟫≠0) (b : Bool)
    (hs : decide (0<⟪e,v⟫)=b) : ∃δ>0,∀e' : ℂ,‖e'‖=1 → dist e' e<δ → ∀r : ℝ,
      0<r → |r-1|<δ → (if b then 1<r else r<1) → x+(r:ℂ)*e'∈Straddle K := by
  cases b
  · have hneg : ⟪e,v⟫<0 := lt_of_le_of_ne (le_of_not_gt (of_decide_eq_false hs)) hn
    obtain ⟨δ,hδ,hh⟩ := h.inner_strip he hneg
    refine ⟨δ,hδ,fun e' he' hd r hr hab hr1 => hh e' he' hd r hr ?_ hr1⟩
    have := (abs_lt.mp hab).1
    linarith
  · obtain ⟨δ,hδ,hh⟩ := h.outer_strip he (of_decide_eq_true hs)
    refine ⟨δ,hδ,fun e' he' hd r _ hab hr1 => hh e' he' hd r hr1 ?_⟩
    have := (abs_lt.mp hab).2
    linarith
/-- Three interface edges supply an actual outsider-only open strip in every
nonexceptional direction, with the radial side chosen by the majority sign. -/
lemma triangle_outsider_strip {c : ℂ → Fin 5} (hc : Measurable c)
    {x : ℂ} {K : Fin 3 → Set ℂ} {v : Fin 3 → ℂ}
    (hK : ∀i,ApproachingContinuum x (K i) (v i))
    (hH : ∀i,∀j∈triangleEdge i,Disjoint (spatialSupport c j) (Straddle (K i)))
    {e : ℂ} (he : ‖e‖=1) (hn : ∀i,⟪e,v i⟫≠0) :
    ∃b : Bool,∃δ>0,∃W : Set ℂ,IsOpen W ∧
      (∀ᵐz : ℂ∂volume,z∈W → c z=3 ∨ c z=4) ∧
      ∀e' : ℂ,‖e'‖=1 → dist e' e<δ → ∀r : ℝ,
        0<r → |r-1|<δ → (if b then 1<r else r<1) → x+(r:ℂ)*e'∈W := by
  classical
  let s : Fin 3 → Bool := fun i => decide (0<⟪e,v i⟫)
  obtain ⟨b,hb⟩ := triangle_majority_cover s
  let E : Finset (Fin 3) := Finset.univ.filter fun i => s i=b
  have hex (i : E) := (hK i).side_strip he (hn i) b ((Finset.mem_filter.mp i.2).2)
  choose d hd hs using hex
  obtain ⟨δ,hδ,_,hδd⟩ := finite_positive_lower_bound Finset.univ d (fun i _ => hd i)
  let W : Set ℂ := ⋂i : E,Straddle (K i)
  refine ⟨b,δ,hδ,W,isOpen_iInter_of_finite (fun i => straddle_isOpen (K i)),?_,?_⟩
  · filter_upwards [finite_support_exclusion_ae c hc K triangleEdge hH] with z hz hzW
    apply triangle_outsider s b hb (c z)
    intro i hi
    exact hz i (mem_iInter.mp hzW ⟨i,Finset.mem_filter.mpr ⟨Finset.mem_univ _,hi⟩⟩)
  · intro e' he' heδ r hr hrδ hside
    apply mem_iInter.mpr
    intro i
    exact hs i e' he' (heδ.trans_le (hδd i (Finset.mem_univ _))) r hr
      (hrδ.trans_le (hδd i (Finset.mem_univ _))) hside
/-- Actual local triangle palette rigidity, without terminal angular sectors
or boundary information as hypotheses. -/
lemma triangle_palette_local {c : ℂ → Fin 5} (hc : Measurable c) (hw : WeakColoring 5 c)
    {x : ℂ} {K : Fin 3 → Set ℂ} {v : Fin 3 → ℂ}
    (hK : ∀i,ApproachingContinuum x (K i) (v i))
    (hH : ∀i,∀j∈triangleEdge i,Disjoint (spatialSupport c j) (Straddle (K i)))
    {t : Angles} (hn : ∀i,⟪direction t,v i⟫≠0)
    (hnR : ∀i,⟪direction t*(Circle.exp (Real.pi/3) : ℂ),v i⟫≠0) :
    ∃i : Fin 5,(i=3 ∨ i=4) ∧ ∃A : Set Angles,IsOpen A ∧ t∈A ∧
      ∀ᵐu∂angularMeasure,u∈A → i∈palette c hc x u := by
  obtain ⟨bu,δu,hδu,U,hU,hUc,hsU⟩ := triangle_outsider_strip hc hK hH (direction_norm t) hn
  have hunit : ‖direction t*(Circle.exp (Real.pi/3) : ℂ)‖=1 := by
    rw [norm_mul,direction_norm,Circle.norm_coe,one_mul]
  obtain ⟨bv,δv,hδv,V,hV,hVc,hsV⟩ := triangle_outsider_strip hc hK hH hunit hnR
  apply binary_strip_palette_rigidity c hc hw hU hV hUc hVc (lt_min hδu hδv) bu bv
  · intro e' he' hd r hr hrd hb
    exact hsU e' he' (hd.trans_le (min_le_left _ _)) r hr (hrd.trans_le (min_le_left _ _)) hb
  · intro e' he' hd r hr hrd hb
    exact hsV e' he' (hd.trans_le (min_le_right _ _)) r hr (hrd.trans_le (min_le_right _ _)) hb
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology MeasureTheory
open scoped RealInnerProductSpace
namespace EuclideanFiveColor
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology MeasureTheory
namespace EuclideanFiveColor
end EuclideanFiveColor
end

noncomputable section
open Set MeasureTheory
namespace EuclideanFiveColor
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology MeasureTheory
namespace EuclideanFiveColor
variable {k : ℕ} {c : ℂ → Fin k} (hc : Measurable c)
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology MeasureTheory
namespace EuclideanFiveColor
end EuclideanFiveColor
end

end OAI
