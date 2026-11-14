/-
  The two `k = 5` consumers re-proved from the master.
  Member m2, swarm smwgpubt5, direction d1.

  STATUS [P] proposed / NOT ELABORATED (no Lean runs in this assignment).

  The declarations below have, binder for binder, the same type as
    `five_support_no_sixty`   (FiveSupport.lean:138)
    `five_support_step_ban`   (FiveSupport.lean:90, = manuscript Lemma 6.7)
  Replacing the originals by these bodies is a proof substitution: no statement change,
  no rename, no call-site change (collapse.md §4).  The primes exist only so that both
  versions can sit side by side while the integration is reviewed.

  After the substitution, `five_support_step_ban`'s proof still has 21 lines
  (FiveSupport.lean:94-114 -> 45-65 below) but contains no analytic reasoning at all: the trace,
  transport and 60-degree content is inside `no_joint_block_of_sixty_pair`.  The declaration grows
  by one line (statement wraps differently).
-/
import OAI.Geometry.PlaneColoring.FiveSupport
import OAI.Geometry.PlaneColoring.PaletteBlockBan

namespace OAI
noncomputable section
open Set Filter Topology MeasureTheory
open scoped RealInnerProductSpace
namespace EuclideanFiveColor

variable (c : ℂ → Fin 5) (hc : Measurable c)

/-- `FiveSupport.lean:138`, same type, proof = master §3 + the five-state dictionary. -/
lemma five_support_no_sixty' (hw : WeakColoring 5 c) {x : ℂ} (hx : FiveCenter c x) {a : ℝ} {i : Fin 5}
    (hi : a ∈ fiveSupport c hc x i) : a + sixty ∉ fiveSupport c hc x i := by
  obtain ⟨j, hj, hsj⟩ := five_support_next c hc hw hx hi
  obtain ⟨X, hX⟩ := five_adj_four j i hj.symm
  have hp : 0 < volume (fiveRealState c hc x j) := stateSupport_nonempty_measure hsj
  intro hs
  exact strict_state_no_unit_joint_block hc hw hX (fiveState_represents c hc hw hx j)
    (fiveState_represents c hc hw hx i) hp hi hs (direction_sixty_unit_real a)

/-- `FiveSupport.lean:90` (manuscript Lemma 6.7), same type, proof = master §4. -/
lemma five_support_step_ban' (hw : WeakColoring 5 c) {x : ℂ} (hx : FiveCenter c x) {a : ℝ}
    {i j : Fin 5}
    (hi : a ∈ fiveSupport c hc x i) (hj : a ∈ fiveSupport c hc x j) (hij : fiveAdj i j) :
    ∀ᵐ t ∂angularMeasure, ¬(fiveState c hc x t = i ∧ fiveState c hc x (t + (sixty : Angles)) = j) ∧
      ¬(fiveState c hc x t = j ∧ fiveState c hc x (t + (sixty : Angles)) = i) := by
  obtain ⟨bi, hbi, hzi⟩ := five_support_trace c hc hw hx hi
  obtain ⟨bj, hbj, hzj⟩ := five_support_trace c hc hw hx hj
  obtain ⟨X, hX⟩ := five_adj_four i j hij
  have hX' : ∀ l, l ∉ fiveDiag j ∪ fiveDiag i ↔ l = X := by
    intro l; rw [Finset.union_comm]; exact hX l
  have hy : ‖(x + direction (a : Angles)) - x‖ = 1 := by
    rw [add_sub_cancel_left]; exact direction_norm (a : Angles)
  have hban := no_joint_block_of_sixty_pair hc hw hy hbj hbi hzj hzi
  have hdiag := fiveState_diag c hc hw hx
  have hdiag' :=
    (measurePreserving_add_right angularMeasure (sixty : Angles)).quasiMeasurePreserving.ae hdiag
  filter_upwards [hban, hdiag, hdiag'] with t Hban Hdiag Hdiag'
  constructor
  · rintro ⟨h₁, h₂⟩
    have hJ₁ : fiveDiag i ⊆ palette c hc x t := by rw [Hdiag, h₁]
    have hJ₂ : fiveDiag j ⊆ palette c hc x (t + (sixty : Angles)) := by rw [Hdiag', h₂]
    exact Hban (fiveDiag i) (fiveDiag j) X hX hX' ⟨hJ₁, hJ₂⟩
  · rintro ⟨h₁, h₂⟩
    have hJ₁ : fiveDiag j ⊆ palette c hc x t := by rw [Hdiag, h₁]
    have hJ₂ : fiveDiag i ⊆ palette c hc x (t + (sixty : Angles)) := by rw [Hdiag', h₂]
    exact Hban (fiveDiag j) (fiveDiag i) X hX' hX ⟨hJ₁, hJ₂⟩

end EuclideanFiveColor
end
end OAI
