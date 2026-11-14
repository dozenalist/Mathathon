import OAI.Geometry.PlaneColoring.FiveSupport

noncomputable section
open Set Filter Topology MeasureTheory

namespace OAI.EuclideanFiveColor

-- A finite-state contact ban plus the existing support transport suffices.
-- This private validation module does not edit the supplied theorem.
lemma stateSupport_no_shift_of_contact_ban
    {ι : Type*} [Fintype ι] [MeasurableSpace ι] [MeasurableSingletonClass ι]
    {f : ℝ → ι} (hf : Measurable f) {d : ℝ}
    (hban : ∀ i j, ¬ Disjoint (stateSupport f i) (stateSupport f j) →
      ∀ᵐ t : ℝ ∂volume, ¬ (f t = i ∧ f (t+d) = j))
    {a : ℝ} {i : ι} (ha : a ∈ stateSupport f i) :
    a+d ∉ stateSupport f i := by
  classical
  have h : ∀ i j, ∀ᵐ t : ℝ ∂volume,
      (f t = i ∧ f (t+d) = j) → Disjoint (stateSupport f i) (stateSupport f j) := by
    intro i j
    by_cases hd : Disjoint (stateSupport f i) (stateSupport f j)
    · exact Filter.Eventually.of_forall (fun _ _ => hd)
    · exact (hban i j hd).mono (fun _ ht hij => False.elim (ht hij))
  have hR : ∀ᵐ t : ℝ ∂volume,
      Disjoint (stateSupport f (f t)) (stateSupport f (f (t+d))) := by
    filter_upwards [ae_all_iff.mpr (fun i => ae_all_iff.mpr (h i))] with t ht
    exact ht (f t) (f (t+d)) ⟨rfl, rfl⟩
  obtain ⟨j, hd, hj⟩ := stateSupport_shift_relation hf
    (R := fun i j => Disjoint (stateSupport f i) (stateSupport f j)) (d := d) hR ha
  intro hi
  exact Set.disjoint_left.mp hd hi hj

lemma five_support_no_sixty_joint_pair
    (c : ℂ → Fin 5) (hc : Measurable c) (hw : WeakColoring 5 c)
    {x : ℂ} (hx : FiveCenter c x) {a : ℝ} {i : Fin 5}
    (hi : a ∈ fiveSupport c hc x i) :
    a+sixty ∉ fiveSupport c hc x i := by
  apply stateSupport_no_shift_of_contact_ban
    ((fiveState_measurable c hc x).comp angleMk_quasiMeasurePreserving.measurable)
    (d := sixty) ?_ hi
  intro i j hcontact
  obtain ⟨b, hbi, hbj⟩ := Set.not_disjoint_iff.mp hcontact
  have hban : ∀ᵐ t ∂angularMeasure,
      ¬ (fiveState c hc x t = i ∧ fiveState c hc x (t+(sixty : Angles)) = j) := by
    by_cases hij : fiveAdj i j
    · exact (five_support_step_ban c hc hw hx hbi hbj hij).mono (fun _ ht => ht.1)
    · filter_upwards [fiveState_adj c hc hw hx] with t ht
      rintro ⟨hti, htj⟩
      exact hij (by simpa only [hti, htj] using ht)
  simpa only [Function.comp_def, AddCircle.coe_add] using
    angleMk_quasiMeasurePreserving.ae hban

#print axioms stateSupport_no_shift_of_contact_ban
#print axioms five_support_no_sixty_joint_pair

end OAI.EuclideanFiveColor
