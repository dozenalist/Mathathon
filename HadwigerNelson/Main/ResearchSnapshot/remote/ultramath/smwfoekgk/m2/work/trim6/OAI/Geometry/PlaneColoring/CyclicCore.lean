import OAI.Geometry.PlaneColoring.FiveSupport

namespace OAI

noncomputable section
open Set Filter Topology MeasureTheory
namespace EuclideanFiveColor
variable (c : ℂ → Fin 5) (hc : Measurable c)
lemma five_real_diag (hw : WeakColoring 5 c) {x : ℂ} (hx : FiveCenter c x) :
    ∀ᵐt : ℝ∂volume,palette c hc x (t : Angles)=fiveDiag (fiveState c hc x (t : Angles)) :=
  angleMk_quasiMeasurePreserving.ae (fiveState_diag c hc hw hx)
lemma five_local_palette (hw : WeakColoring 5 c) {x : ℂ} (hx : FiveCenter c x) {a : ℝ} {k : Fin 5}
    (hk : ∀i,a∈fiveSupport c hc x i → k∈fiveDiag i) :
    ∃V, IsOpen V ∧ a∈V ∧ ∀ᵐt : ℝ∂volume,t∈V → (t : Angles)∈paletteSet c hc x k := by
  obtain ⟨V,hV,ha,hkV⟩ := stateSupport_local_pred
    ((fiveState_measurable c hc x).comp angleMk_quasiMeasurePreserving.measurable) hk
  refine ⟨V,hV,ha,?_⟩
  filter_upwards [hkV,five_real_diag c hc hw hx] with t ht hd htv
  apply (mem_palette c hc x (t : Angles) k).mp
  rw [hd]
  exact ht htv
lemma five_endpoint_no_common (hw : WeakColoring 5 c) {x : ℂ} (hx : FiveCenter c x) {a b : ℝ}
    (hab : Real.sin (b-a)≠0) (hy : FiveCenter c (x+direction (a : Angles)+direction (b : Angles))) :
    ∀k : Fin 5,∃i,a∈fiveSupport c hc x i ∧ k∉fiveDiag i := by
  intro k
  by_contra! h
  obtain ⟨V,hV,ha,hpal⟩ := five_local_palette c hc hw hx h
  obtain ⟨U,hU,hyU,hnull⟩ := palette_open_exclusion c hc hw hab hV ha hpal
  exact transitionEdge_no_open_exclusion c (hy k) hU hyU hnull
lemma five_limit_contact {x : ℂ} {an : ℕ → ℝ} {a : ℝ} (ha : Tendsto an atTop (𝓝 a))
    (hn : ∀n,∀k : Fin 5,∃i,an n∈fiveSupport c hc x i ∧ k∉fiveDiag i) :
    ∃i,a∈fiveSupport c hc x i ∧ a∈fiveSupport c hc x (i+1) := by
  have hall : ∀k : Fin 5,∃i,a∈fiveSupport c hc x i ∧ k∉fiveDiag i := fun k =>
    finite_closed_family_no_common_limit (fun _ => Measure.isClosed_support) ha (fun n => hn n k)
  have hnList : (fiveSupportList c hc x a).Nonempty := by
    obtain ⟨i,hi⟩ := five_support_cover c hc x a
    exact ⟨i,(mem_fiveSupportList _ _ _ _ _).mpr hi⟩
  have hp : ∀k,∃i∈fiveSupportList c hc x a,k∉fiveDiag i := by
    intro k; obtain ⟨i,hi,hk⟩ := hall k
    exact ⟨i,(mem_fiveSupportList _ _ _ _ _).mpr hi,hk⟩
  obtain ⟨i,hi,hi'⟩ := FiveComb.adjacent_oriented _ (five_no_common_adj _ hnList hp)
  exact ⟨i,(mem_fiveSupportList _ _ _ _ _).mp hi,(mem_fiveSupportList _ _ _ _ _).mp hi'⟩
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology
namespace EuclideanFiveColor
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology MeasureTheory
namespace EuclideanFiveColor
variable (c : ℂ → Fin 5) (hc : Measurable c)
include hc in
include hc in
include hc in
include hc in
end EuclideanFiveColor
end

noncomputable section
open Set
namespace EuclideanFiveColor
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology MeasureTheory
namespace EuclideanFiveColor
variable (c : ℂ → Fin 5) (hc : Measurable c)

def CyclicCore : Set ℂ := {x | ¬(transitionGraph c x).IsAcyclic}
include hc in
include hc in
end EuclideanFiveColor
end

end OAI
