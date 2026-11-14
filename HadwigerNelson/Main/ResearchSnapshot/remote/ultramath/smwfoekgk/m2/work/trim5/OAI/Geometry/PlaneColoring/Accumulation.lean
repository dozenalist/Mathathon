import OAI.Geometry.PlaneColoring.Exclusion
import OAI.Geometry.PlaneColoring.FourTransport

namespace OAI

noncomputable section
open Set Filter Topology MeasureTheory
namespace EuclideanFiveColor
lemma normalized_increment_endpoint_gap {l r a : ℝ} (hlr : l<r)
    {u δ : ℕ → ℝ} {v : ℝ} (hδ : ∀n,0<δ n)
    (hv : (a=l ∧ 0<v) ∨ (a=r ∧ v<0))
    (hu : Tendsto u atTop (𝓝 a))
    (hs : Tendsto (fun n => (u n-a)/δ n) atTop (𝓝 v)) :
    ∀ᶠn in atTop,u n∈Ioo l r := by
  rcases hv with ⟨rfl,hv⟩ | ⟨rfl,hv⟩
  · exact positive_normalized_increment_enters_gap hlr hδ hv hu hs
  · filter_upwards [hu.eventually (lt_mem_nhds hlr),hs.eventually (gt_mem_nhds hv)] with n hn hp
    exact ⟨hn,sub_neg.mp ((div_neg_iff.mp hp).resolve_left (fun h => (not_lt_of_ge (hδ n).le) h.2)).1⟩
variable (c : ℂ → Fin 5) (hc : Measurable c)
lemma four_support_positive (hw : WeakColoring 5 c) {x : ℂ} (hx : FourCenter c x)
    {s : Fin 3} (hs : s≠0) : 0<volume (fourSupport c hc x s) := by
  apply (four_realState_positive c hc hw hx hs).trans_le
  apply measure_mono_ae
  exact (ae_restrict_iff' (four_realState_measurable c hc x s)).mp
    (volume.restrict (fourRealState c hc x s)).support_mem_ae
lemma four_other_union (x : ℂ) {s : Fin 3} (hs : s≠0) :
    fourNonSingleton c hc x=fourSupport c hc x s∪fourSupport c hc x (if s=1 then 2 else 1) := by
  fin_cases s
  · exact (hs rfl).elim
  · rfl
  · exact Set.union_comm _ _
lemma four_endpoint_sequence_false (hw : WeakColoring 5 c)
    {yn : ℕ → ℂ} {x : ℂ} (hyn : ∀n,FourCenter c (yn n)) (hx : FourCenter c x)
    (hy : Tendsto yn atTop (𝓝 x)) {δ : ℕ → ℝ} {H : RealPlane} (hδ : ∀n,0<δ n)
    (hdir : Tendsto (fun n => (δ n)⁻¹•Complex.equivRealProdCLM (yn n-x)) atTop (𝓝 H))
    {l r a : ℝ} (hlr : l<r) (haEnd : a=l ∨ a=r)
    (hgap : Ioo l r⊆(fourSupport c hc x 1∪fourSupport c hc x 2)ᶜ)
    {s : Fin 3} (hs : s≠0) (ha : a∈fourSupport c hc x s)
    (hHa : H.1*Real.cos a+H.2*Real.sin a≠0) : False := by
  classical
  let t : Fin 3 := if s=1 then 2 else 1
  have ht : t≠0 := by dsimp [t]; split <;> decide
  have hRaN := four_gap_shift_subset c hc hw hx hlr hgap
    (show a+sixty∈Icc (l+sixty) (r+sixty) from by rcases haEnd with rfl|rfl <;> constructor <;> linarith)
  have hRa : a+sixty∈fourSupport c hc x t := by
    change a+sixty∈fourNonSingleton c hc x at hRaN
    rw [four_other_union c hc x hs] at hRaN
    exact hRaN.resolve_left (four_support_no_sixty c hc hw hx hs ha)
  obtain ⟨b0,hb0,b1,hb1,hb0a,hb1a,hv01⟩ := exists_transportVelocity_lt
    (four_support_positive c hc hw hx ht) hHa
  have hp : ∃b b',b∈fourSupport c hc x t ∧ b'∈fourSupport c hc x t ∧
      Real.sin (b-a)≠0 ∧ Real.sin (b'-a)≠0 ∧
      ((a=l ∧ 0<transportVelocity H a b-transportVelocity H a b') ∨
       (a=r ∧ transportVelocity H a b-transportVelocity H a b'<0)) := by
    rcases haEnd with hal|har
    · exact ⟨b1,b0,hb1,hb0,hb1a,hb0a,Or.inl ⟨hal,sub_pos.mpr hv01⟩⟩
    · exact ⟨b0,b1,hb0,hb1,hb0a,hb1a,Or.inr ⟨har,sub_neg.mpr hv01⟩⟩
  obtain ⟨b,b',hb,hb',hab,hab',hvel⟩ := hp
  obtain ⟨bn,hbn,hbt⟩ := four_support_continuity c hc hw hyn hx hy ht hb'
  obtain ⟨dn,hdn,hdt⟩ := four_support_continuity c hc hw hyn hx hy ht hRa
  let Hn := fun n => Complex.equivRealProdCLM (yn n-x)
  have hH : Tendsto Hn atTop (𝓝 0) := by
    simpa only [sub_self,map_zero,Function.comp_def] using
      Complex.equivRealProdCLM.continuous.continuousAt.tendsto.comp (hy.sub_const x)
  let cn := fun n => (sumTransport hab (Hn n) (a,b)).1
  have hcn : Tendsto cn atTop (𝓝 a) := (sumTransport_tendsto hab hH tendsto_const_nhds).fst_nhds
  have hneg : Tendsto (fun n => -Hn n) atTop (𝓝 0) := by simpa only [neg_zero] using hH.neg
  let un := fun n => (sumTransport hab' (-Hn n) (cn n,bn n)).1
  have hun : Tendsto un atTop (𝓝 a) :=
    (sumTransport_tendsto hab' hneg (hcn.prodMk_nhds hbt)).fst_nhds
  have huGap : ∀ᶠn in atTop,un n∈Ioo l r := normalized_increment_endpoint_gap hlr hδ hvel hun
    (sumTransport_double_increment hab hab' hH hbt hδ hdir)
  obtain ⟨P,V,hP,hP0,hV,haV,K,hbranch⟩ := sumTransport_neighborhood hab
  have hcN : ∀ᶠn in atTop,cn n∈fourNonSingleton c hc (yn n) := by
    filter_upwards [hH.eventually (hP.mem_nhds hP0)] with n hn
    exact (four_support_transport c hc hw hx (hyn n) hs ha hb hab hV haV hbranch hn).1
  obtain ⟨P',V',hP',hP0',hV',haV',K',hbranch'⟩ := sumTransport_neighborhood hab'
  have hcNot : ∀ᶠn in atTop,cn n∉fourSupport c hc (yn n) s := by
    filter_upwards [hneg.eventually (hP'.mem_nhds hP0'),
      (hcn.prodMk_nhds hbt).eventually (hV'.mem_nhds haV'),huGap] with n hn hqn hgn hcu
    have hcenter : Complex.equivRealProdCLM (x-yn n)= -Hn n := by
      dsimp [Hn]
      rw [← map_neg,neg_sub]
    have htr := four_support_transport_general c hc hw (hyn n) hx hs hab' hcu (hbn n)
      hV' hqn hbranch' (hcenter.symm ▸ hn)
    rw [hcenter] at htr
    exact hgap hgn htr.1
  have hcT : ∀ᶠn in atTop,cn n∈fourSupport c hc (yn n) t := by
    filter_upwards [hcN,hcNot] with n hn hnot
    rw [four_other_union c hc (yn n) hs] at hn
    exact hn.resolve_left hnot
  let vn := fun n => if h : cn n∈fourSupport c hc (yn n) t then cn n
    else (four_support_nonempty c hc hw (hyn n) ht).choose
  have hvn : ∀n,vn n∈fourSupport c hc (yn n) t := by
    intro n
    dsimp [vn]
    split
    · assumption
    · exact (four_support_nonempty c hc hw (hyn n) ht).choose_spec
  have hvlim : Tendsto vn atTop (𝓝 a) := hcn.congr' (by
    filter_upwards [hcT] with n hn
    simp only [vn,dite_eq_left hn])
  exact four_support_sequence_no_unit c hc hw hyn hx hy ht hvlim hdt hvn hdn (direction_sixty_unit_real a)
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
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology MeasureTheory
namespace EuclideanFiveColor
variable {k : ℕ} (c : ℂ → Fin k)
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology MeasureTheory
namespace EuclideanFiveColor
variable (c : ℂ → Fin 5) (hc : Measurable c)
include hc
omit hc in

end EuclideanFiveColor

end

noncomputable section
open Set Filter Topology MeasureTheory
namespace EuclideanFiveColor
variable {k : ℕ} (c : ℂ → Fin k) (e : Equiv.Perm (Fin k))
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology MeasureTheory
namespace EuclideanFiveColor
variable (c : ℂ → Fin 5) (hc : Measurable c)
include hc in
include hc in
include hc in
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology MeasureTheory
namespace EuclideanFiveColor
variable (c : ℂ → Fin 5) (hc : Measurable c)
end EuclideanFiveColor
end

end OAI
