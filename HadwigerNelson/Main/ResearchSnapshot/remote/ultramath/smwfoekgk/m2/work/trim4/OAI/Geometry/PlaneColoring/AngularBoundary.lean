import OAI.Geometry.PlaneColoring.BoundaryTrace

namespace OAI

noncomputable section
namespace EuclideanFiveColor
/-- `0` is the outsider and `1,2` the two diagonal states. -/
def FourWordValid (w : Fin 6 → Fin 3) : Prop :=
  (∀j,w j≠w (j+1)) ∧ (∀j,w j≠0 → w (j+3)≠0 → w (j+3)=w j)
instance (w : Fin 6 → Fin 3) : Decidable (FourWordValid w) := inferInstanceAs (Decidable (_∧_))
def FourWordMixed (w : Fin 6 → Fin 3) : Prop :=
  ∃i j,w i=0 ∧ w j=0 ∧ i.val%2≠j.val%2
instance (w : Fin 6 → Fin 3) : Decidable (FourWordMixed w) := inferInstanceAs (Decidable (∃_i _j,_∧_∧_))
def FourWordCross (w u : Fin 6 → Fin 3) : Prop :=
  ∀j,w j≠0 → u (j+1)≠w j ∧ u (j-1)≠w j
instance (w u : Fin 6 → Fin 3) : Decidable (FourWordCross w u) := inferInstanceAs (Decidable (∀_j,_→_∧_))
lemma forall_six_word (P : (Fin 6 → Fin 3) → Prop) :
    (∀w,P w) ↔ ∀a b c d e f : Fin 3,P ![a,b,c,d,e,f] := by
  constructor
  · intro h a b c d e f
    exact h _
  · intro h w
    have he : w=![w 0,w 1,w 2,w 3,w 4,w 5] := by
      ext j
      fin_cases j <;> rfl
    rw [he]
    exact h _ _ _ _ _ _
lemma four_word_has_outsider : ∀w : Fin 6 → Fin 3,FourWordValid w → ∃j,w j=0 := by
  simp only [forall_six_word]
  decide
lemma four_word_mixed_isolated : ∀w : Fin 6 → Fin 3,FourWordValid w → FourWordMixed w →
    ∀u : Fin 6 → Fin 3,FourWordValid u → FourWordCross w u → u=w := by
  simp only [forall_six_word]
  decide
lemma four_word_parity : ∀w : Fin 6 → Fin 3,FourWordValid w → ¬FourWordMixed w →
    ∃p : Fin 2,∀j,w j=0 → j.val%2=p.val := by
  simp only [forall_six_word]
  decide
lemma four_word_shift_parity : ∀w : Fin 6 → Fin 3,∀p : Fin 2,
    (∀j,w j=0 → j.val%2=p.val) → ∀j,w (j+1)=0 → j.val%2=(p+1).val := by
  simp only [forall_six_word]
  decide
lemma four_word_opposite_parity : ∀w : Fin 6 → Fin 3,FourWordValid w →
    (∀j,w j=0 → j.val%2=0) → ∀u : Fin 6 → Fin 3,FourWordValid u →
    (∀j,u j=0 → j.val%2=1) → FourWordCross w u →
    ∃a b : Fin 3,a≠0 ∧ b≠0 ∧ a≠b ∧
      (∀j,j.val%2=1 → w j=a) ∧ (∀j,j.val%2=0 → u j=b) := by
  simp only [forall_six_word]
  decide
end EuclideanFiveColor
end

noncomputable section
open Set Topology
namespace EuclideanFiveColor
/-- Uniform local isolation of a value on a dense subset of a connected metric
space propagates globally. This is the manuscript dense-set chain argument. -/
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology MeasureTheory
namespace EuclideanFiveColor
end EuclideanFiveColor
end

noncomputable section
open Set Topology
namespace EuclideanFiveColor
/-- The mixed-parity exceptional words are excluded by actual local isolation
and sixty-degree covariance on a dense set. -/
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology MeasureTheory
open scoped RealInnerProductSpace
namespace EuclideanFiveColor
/-- The source's strict min/max straddling region, in equivalent witness form. -/
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology MeasureTheory
open scoped RealInnerProductSpace
namespace EuclideanFiveColor
/-- The approach data furnished by the manuscript interface proposition, with no
assumption of angular strip conclusions. -/
structure ApproachingContinuum (x : ℂ) (K : Set ℂ) (v : ℂ) where
  center_mem : x∈K
  r : ℕ → ℝ
  w : ℕ → ℂ
  r_pos : ∀n,0<r n
  r_tendsto : Tendsto r atTop (𝓝 0)
  w_unit : ∀n,‖w n‖=1
  w_tendsto : Tendsto w atTop (𝓝 v)
  point_mem : ∀n,x+(r n : ℂ)*w n∈K
variable {k : ℕ} (c : ℂ → Fin k) (hc : Measurable c)
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology MeasureTheory
namespace EuclideanFiveColor
variable {k : ℕ} (c : ℂ → Fin k)
/-- The manuscript's essential spatial color support. -/
end EuclideanFiveColor
end

noncomputable section
open Set Filter Topology MeasureTheory
namespace EuclideanFiveColor
/-- Core finite obstruction behind the one-orbit boundary theorem. -/
end EuclideanFiveColor
end

end OAI
