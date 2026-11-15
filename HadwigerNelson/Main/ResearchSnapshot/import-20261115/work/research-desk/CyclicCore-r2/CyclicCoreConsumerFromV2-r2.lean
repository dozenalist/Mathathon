/-
  OWNED COPY - the same-name swap for the CyclicCore consumer of manuscript Lemma 6.7,
  built for the parent's LOCAL Lean queue. Nothing here was compiled by me.

  What this file does (and nothing else):
    * reuses, VERBATIM, the three banked declarations from
      supervisor/simplify-architecture/step-ban/StepBanShort-r2.lean
      (sha256 19bffbcd71bed9b8e92daddf705df89963319604e1e20b4332d6b2f0cf717655);
    * reuses, VERBATIM, the audited body of five_opposite_contacts_false_from_v2 from
      .ultramath/smwgzbcnp/m1/ConsumerFromV2.lean (sha256 4e700e4a1954a9e9a9ed...);
    * restates the CyclicCore.lean:119 consumer - five_sequence_small_no_accumulation,
      declared at CyclicCore.lean:99 with `include hc in` at :98 - under the new name
      five_sequence_small_no_accumulation_from_v2, calling
      five_opposite_contacts_false_from_v2 with the identical positional arguments
      `c hc hw hx (by dsimp [sixty]; ring) hi hi' hj hj'`;
    * ends with a #check pair against the original CyclicCore theorem and #print axioms.

  NOT done here, on purpose:
    * FiveSupport.lean and CyclicCore.lean are untouched; this is an owned copy.
    * five_support_step_ban (v1, FiveSupport.lean:90) is retained.
    * the dead binders hn (FiveSupport.lean:203) and hp (:204) are NOT removed here -
      they stay inside the reused body so that the contract check is a pure
      rename-and-reroute. Their removal is a separate diff (swap/cleanup-hn-hp.diff).

  Statement identity: the restated consumer's `lemma` line through `:= by` is the
  original with exactly two substitutions - the lemma name and the callee name.
-/
import OAI.Geometry.PlaneColoring.CyclicCore

namespace OAI

noncomputable section
open Set Filter Topology MeasureTheory
namespace EuclideanFiveColor

variable (c : ℂ → Fin 5) (hc : Measurable c)

/-- reused verbatim from r2 / ConsumerFromV2: five_outsider_unique (sha256 ed263e7b31d4918d) -/
lemma five_outsider_unique : ∀ i j y z : Fin 5, (i + 1 = j ∨ j + 1 = i) →
    y ∉ fiveDiag i → y ∉ fiveDiag j → z ∉ fiveDiag i → z ∉ fiveDiag j → y = z := by
  decide

/-- reused verbatim from r2 / ConsumerFromV2: five_pair_meet (sha256 db64d67d2713f520) -/
lemma five_pair_meet {i j : Fin 5} (hij : fiveAdj i j) {p q : Finset (Fin 5)}
    (hp : Disjoint p (fiveDiag i)) (hq : Disjoint q (fiveDiag j))
    (hpj : ¬ p ⊆ fiveDiag j) (hqi : ¬ q ⊆ fiveDiag i) : ¬ Disjoint p q := by
  intro hpq
  obtain ⟨y, hyp, hyj⟩ := Finset.not_subset.mp hpj
  obtain ⟨z, hzq, hzi⟩ := Finset.not_subset.mp hqi
  have hyi : y ∉ fiveDiag i := Finset.disjoint_left.mp hp hyp
  have hzj : z ∉ fiveDiag j := Finset.disjoint_left.mp hq hzq
  -- `fiveAdj` is a plain `def`, so `hij` is definitionally the bare disjunction:
  have hyz : y = z := five_outsider_unique i j y z hij hyi hyj hzi hzj
  exact Finset.disjoint_left.mp hpq hyp (hyz.symm ▸ hzq)

/-- reused verbatim from r2 / ConsumerFromV2: five_support_step_ban_v2 (sha256 b8f73729aca777df) -/
lemma five_support_step_ban_v2 (hw : WeakColoring 5 c) {x : ℂ} (hx : FiveCenter c x) {a : ℝ} {i j : Fin 5}
    (hi : a∈fiveSupport c hc x i) (hj : a∈fiveSupport c hc x j) (hij : fiveAdj i j) :
    ∀ᵐt∂angularMeasure,¬(fiveState c hc x t=i ∧ fiveState c hc x (t+(sixty : Angles))=j) ∧
      ¬(fiveState c hc x t=j ∧ fiveState c hc x (t+(sixty : Angles))=i) := by
  obtain ⟨bi,hbi,hzi⟩ := five_support_trace c hc hw hx hi
  obtain ⟨bj,hbj,hzj⟩ := five_support_trace c hc hw hx hj
  have hq := (measurePreserving_add_right angularMeasure (sixty : Angles)).quasiMeasurePreserving
  have hni := avoiding_trace_palette c hc hbi hzi
  have hnj := avoiding_trace_palette c hc hbj hzj
  have hnd := palette_neighbor_disjoint c hc hw x a
  have hdg := fiveState_diag c hc hw hx
  filter_upwards [hni,hnj,hnd,hdg,hq.ae hni,hq.ae hnj,hq.ae hnd,hq.ae hdg,
    palette_sixty_disjoint c hc hw (x+direction (a : Angles))]
    with t hpi hpj hdt het hui huj hdu heu hdis
  refine ⟨?_,?_⟩
  · rintro ⟨hst,hsu⟩
    exact five_pair_meet hij (by simpa only [het,hst] using hdt) (by simpa only [heu,hsu] using hdu)
      hpj hui hdis
  · rintro ⟨hst,hsu⟩
    exact five_pair_meet hij.symm (by simpa only [het,hst] using hdt) (by simpa only [heu,hsu] using hdu)
      hpi huj hdis

/-- reused verbatim from r2 / ConsumerFromV2: five_opposite_contacts_false_from_v2 (sha256 d38fc85d53a81c30) -/
lemma five_opposite_contacts_false_from_v2 (hw : WeakColoring 5 c) {x : ℂ} (hx : FiveCenter c x)
    {a b : ℝ} (hab : b=a+3*sixty) {i j : Fin 5}
    (hi : a∈fiveSupport c hc x i) (hi' : a∈fiveSupport c hc x (i+1))
    (hj : b∈fiveSupport c hc x j) (hj' : b∈fiveSupport c hc x (j+1)) : False := by
  have hn := five_contact_next c hc hw hx hi hi'
  have hp := five_contact_prev c hc hw hx hj hj'
  have hdis : Disjoint ({i-1,i+2} : Finset (Fin 5)) {j-1,j+2} := by
    apply Finset.disjoint_left.mpr
    intro k hk hl
    have hiK : a+sixty∈fiveSupport c hc x k := by
      apply (mem_fiveSupportList _ _ _ _ _).mp
      simp only [Finset.mem_insert,Finset.mem_singleton] at hk
      rcases hk with rfl|rfl <;> tauto
    have hjK : b-sixty∈fiveSupport c hc x k := by
      apply (mem_fiveSupportList _ _ _ _ _).mp
      simp only [Finset.mem_insert,Finset.mem_singleton] at hl
      rcases hl with rfl|rfl <;> tauto
    exact five_support_no_sixty c hc hw hx hiK (by convert hjK using 1; rw [hab]; ring)
  have hji := FiveComb.opposite_contacts i j hdis
  obtain ⟨s,hs,_hst,hban⟩ := FiveComb.two_bans i j hji
  have hss : a∈fiveSupport c hc x s := by rcases hs with rfl|rfl <;> assumption
  have hbanI := five_support_step_ban_v2 c hc hw hx hi hi' (Or.inl rfl)
  have hbanJ := five_support_step_ban_v2 c hc hw hx hj hj' (Or.inl rfl)
  have hnot : ∀ᵐt∂angularMeasure,fiveState c hc x t≠s := by
    filter_upwards [hbanI,hbanJ,fiveState_adj c hc hw hx] with t hbI hbJ ha he
    rw [he] at ha
    rcases hban _ ha with h|h
    · rcases h with ⟨rfl,ht⟩|⟨rfl,ht⟩
      · exact hbI.1 ⟨he,ht⟩
      · exact hbI.2 ⟨he,ht⟩
    · rcases h with ⟨rfl,ht⟩|⟨rfl,ht⟩
      · exact hbJ.1 ⟨he,ht⟩
      · exact hbJ.2 ⟨he,ht⟩
  have hz : volume (fiveRealState c hc x s)=0 := measure_eq_zero_iff_ae_notMem.mpr (angleMk_quasiMeasurePreserving.ae hnot)
  exact (stateSupport_nonempty_measure hss).ne' hz

include hc in
lemma five_sequence_small_no_accumulation_from_v2 (hw : WeakColoring 5 c)
    {yn : ℕ → ℂ} {x : ℂ} (hyn : ∀n,FiveCenter c (yn n)) (hx : FiveCenter c x)
    (hy : Tendsto yn atTop (𝓝 x)) (hne : ∀n,yn n≠x) (hsmall : ∀n,‖yn n-x‖<2) : False := by
  obtain ⟨φ,hφ,t,a,b,ha,hb,hs,hab⟩ := chord_sequence_lifts
    (by simpa only [sub_self] using hy.sub_const x) (fun n => sub_ne_zero.mpr (hne n)) hsmall
  have hcSum (n : ℕ) : x+direction (a n : Angles)+direction (b n : Angles)=yn (φ n) := by
    rw [direction_real,direction_real,Circle.coe_exp,Circle.coe_exp,add_assoc,hs]
    abel
  have haC : ∀n,∀k : Fin 5,∃i,a n∈fiveSupport c hc x i ∧ k∉fiveDiag i := by
    intro n
    apply five_endpoint_no_common c hc hw hx (hab n)
    rw [hcSum]; exact hyn _
  have hbC : ∀n,∀k : Fin 5,∃i,b n∈fiveSupport c hc x i ∧ k∉fiveDiag i := by
    intro n
    apply five_endpoint_no_common c hc hw hx
    · rw [show a n-b n=-(b n-a n) by ring,Real.sin_neg]
      exact neg_ne_zero.mpr (hab n)
    · rw [add_right_comm,hcSum]; exact hyn _
  obtain ⟨i,hi,hi'⟩ := five_limit_contact c hc ha haC
  obtain ⟨j,hj,hj'⟩ := five_limit_contact c hc hb hbC
  exact five_opposite_contacts_false_from_v2 c hc hw hx (by dsimp [sixty]; ring) hi hi' hj hj'

-- Contract checks: the two signatures must print identically except for the name,
-- and the restated consumer must rest on the standard axioms only.
#check @five_sequence_small_no_accumulation
#check @five_sequence_small_no_accumulation_from_v2
#print axioms five_sequence_small_no_accumulation_from_v2

end EuclideanFiveColor
end
end OAI
