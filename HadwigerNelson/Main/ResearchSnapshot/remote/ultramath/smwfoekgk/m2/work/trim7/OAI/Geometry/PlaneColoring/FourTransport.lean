import OAI.Geometry.PlaneColoring.FourContinuity

namespace OAI

noncomputable section
open Set Filter Topology MeasureTheory
open scoped NNReal
namespace EuclideanFiveColor
lemma circleSum_one_lipschitz_sumTransport : LipschitzWith 2 (circleSum 1) := by
  apply LipschitzWith.of_dist_le_mul
  intro p q
  have hh (g : ℝ → ℝ) (hg : LipschitzWith 1 g) :
      dist (g p.1+g p.2) (g q.1+g q.2)≤2*max (dist p.1 q.1) (dist p.2 q.2) := by
    have h1 := hg.dist_le_mul p.1 q.1
    have h2 := hg.dist_le_mul p.2 q.2
    norm_num only [NNReal.coe_one,one_mul] at h1 h2
    have h3 := dist_add_add_le (g p.1) (g p.2) (g q.1) (g q.2)
    have h4 := le_max_left (dist p.1 q.1) (dist p.2 q.2)
    have h5 := le_max_right (dist p.1 q.1) (dist p.2 q.2)
    linarith
  simpa only [circleSum,one_mul,Prod.dist_eq,NNReal.coe_ofNat] using
    max_le (hh _ Real.lipschitzWith_cos) (hh _ Real.lipschitzWith_sin)

def sumTransport {a b : ℝ} (h : Real.sin (b-a)≠0) (H : RealPlane) (q : RealPlane) :=
  circleInverse h (circleSum 1 q-H)
lemma sumTransport_measurable {a b : ℝ} (h : Real.sin (b-a)≠0) (H : RealPlane) :
    Measurable (sumTransport h H) :=
  (circleInverse_measurable h).comp ((circleSum_continuous 1).sub continuous_const).measurable
lemma sumTransport_neighborhood {a b : ℝ} (h : Real.sin (b-a)≠0) :
    ∃P V : Set RealPlane,IsOpen P ∧ 0∈P ∧ IsOpen V ∧ (a,b)∈V ∧
      ∃K : ℝ≥0,∀H∈P,
        (∀q∈V,ContinuousAt (sumTransport h H) q) ∧
        AntilipschitzWith K (V.domRestrict (sumTransport h H)) ∧
        (∀q∈V,Real.sin (q.2-q.1)≠0) ∧
        (∀q∈V,Real.sin ((sumTransport h H q).2-(sumTransport h H q).1)≠0) ∧
        ∀q∈V,circleSum 1 (sumTransport h H q)=circleSum 1 q-H := by
  have hc : Continuous (fun z : RealPlane×RealPlane => circleSum 1 z.2-z.1) :=
    ((circleSum_continuous 1).comp continuous_snd).sub continuous_fst
  have hbtarget : circleSum 1 (a,b)∈(circleInverseHomeo h).target :=
    (circleSum_strict 1 (a,b)).image_mem_toOpenPartialHomeomorph_target
  have ht : ∀ᶠ z : RealPlane×RealPlane in 𝓝 (0,(a,b)),
      circleSum 1 z.2-z.1∈(circleInverseHomeo h).target ∧
      Real.sin ((circleInverse h (circleSum 1 z.2-z.1)).2-(circleInverse h (circleSum 1 z.2-z.1)).1)≠0 := by
    have hlim : Tendsto (fun z : RealPlane×RealPlane => circleSum 1 z.2-z.1)
        (𝓝 (0,(a,b))) (𝓝 (circleSum 1 (a,b))) := by simpa only [sub_zero] using hc.tendsto (0,(a,b))
    have htt : ∀ᶠ q in 𝓝 (circleSum 1 (a,b)),q∈(circleInverseHomeo h).target :=
      (circleInverseHomeo h).open_target.mem_nhds hbtarget
    exact hlim.eventually (htt.and (circleInverse_regular h))
  obtain ⟨P,hP,W,hW,hPW⟩ := mem_nhds_prod_iff.mp ht
  obtain ⟨P₀,hP₀,hPsub,hPmem⟩ := mem_nhds_iff.mp hP
  obtain ⟨W₀,hW₀,hWsub,hWmem⟩ := mem_nhds_iff.mp hW
  obtain ⟨V₀,hV₀,hv₀,L,hL⟩ := circleSum_local_antilipschitz (r := 1) (p := (a,b)) (by simpa only [one_mul] using h)
  let V := W₀∩V₀∩{q : RealPlane | Real.sin (q.2-q.1)≠0}
  have hV : IsOpen V := (hWsub.inter hV₀).inter ((Real.continuous_sin.comp (continuous_snd.sub continuous_fst)).isOpen_preimage _ isOpen_ne)
  refine ⟨P₀,V,hPsub,hPmem,hV,⟨⟨hWmem,hv₀⟩,h⟩,L*2,?_⟩
  intro H hH
  have htarget (q : RealPlane) (hq : q∈V) := hPW (a := (H,q)) ⟨hP₀ hH,hW₀ hq.1.1⟩
  have heq (q : RealPlane) (hq : q∈V) : circleSum 1 (sumTransport h H q)=circleSum 1 q-H :=
    circleInverse_right h (htarget q hq).1
  refine ⟨?_,?_,fun _ hq => hq.2,fun q hq => (htarget q hq).2,heq⟩
  · intro q hq
    change ContinuousAt (fun z : RealPlane => circleInverse h (circleSum 1 z-H)) q
    exact (circleInverse_continuousAt h (htarget q hq).1).comp (x := q)
      (((circleSum_continuous 1).sub (continuous_const (y := H))).continuousAt)
  · apply AntilipschitzWith.of_le_mul_dist
    intro q r
    have hh := hL.le_mul_dist ⟨q,q.2.1.2⟩ ⟨r,r.2.1.2⟩
    have hd : dist (circleSum 1 q) (circleSum 1 r)=dist (circleSum 1 (sumTransport h H q)) (circleSum 1 (sumTransport h H r)) := by
      rw [heq q q.2,heq r r.2,dist_sub_right]
    change dist (q : RealPlane) (r : RealPlane) ≤ L*dist (circleSum 1 q) (circleSum 1 r) at hh
    rw [hd] at hh
    have hl := circleSum_one_lipschitz_sumTransport.dist_le_mul (sumTransport h H q) (sumTransport h H r)
    apply hh.trans
    have hm := mul_le_mul_of_nonneg_left hl L.2
    simp only [NNReal.coe_mul,NNReal.coe_ofNat,Set.domRestrict_apply] at *
    nlinarith
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology MeasureTheory
open scoped NNReal
namespace EuclideanFiveColor
variable (c : ℂ → Fin 5) (hc : Measurable c)
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology MeasureTheory
open scoped NNReal
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
variable (c : ℂ → Fin 5) (hc : Measurable c)
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology MeasureTheory
namespace EuclideanFiveColor
variable (c : ℂ → Fin 5) (hc : Measurable c)
end EuclideanFiveColor
end

noncomputable section
open Filter Topology Asymptotics
namespace EuclideanFiveColor
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

end OAI
