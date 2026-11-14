/-
  Label merging at six colours: two machine-checked k = 6 theorems.

  (A2) proper form: every pair of distinct labels of a proper 6-colouring is carried by a
       unit pair  (paper's Theorem 1.1 applied to the merge).
  (A)  measure form: for a measurable weak 6-colouring, the set of unit pairs carrying a fixed
       pair of labels has positive measure  (paper's Theorem 1.4 applied to the merge).

  Both proofs are the same collapse: merge two labels to get a five-label colouring, whose
  monochromatic unit pairs are exactly the pairs carrying those two labels.

  Check with:   source scripts/env4341.sh && lean .ultramath/smwfo9zkl/m4/lean/MergeSixK6.lean
-/
import OAI.Geometry.PlaneColoring.Five

namespace OAI
namespace EuclideanFiveColor

open MeasureTheory

/-! ### The merge map and its kernel -/

/-- Merging labels `0` and `1`: the explicit 2-to-1 map `Fin 6 → Fin 5`. -/
def merge01 : Fin 6 → Fin 5 := ![0, 0, 1, 2, 3, 4]

lemma merge01_eq_iff (a b : Fin 6) :
    merge01 a = merge01 b ↔ a = b ∨ (a = 0 ∧ b = 1) ∨ (a = 1 ∧ b = 0) := by
  revert a b
  decide

/-- The permutation of `Fin 6` sending `i` to `0` and `j` to `1`, for `i ≠ j`:
first swap `i` with `0`, then swap the image of `j` with `1` (which leaves `0` fixed). -/
noncomputable def permToZeroOne (i j : Fin 6) : Equiv.Perm (Fin 6) :=
  (Equiv.swap i 0).trans (Equiv.swap ((Equiv.swap i 0) j) 1)

lemma permToZeroOne_apply_i (i j : Fin 6) (hij : i ≠ j) : permToZeroOne i j i = 0 := by
  have h1 : (Equiv.swap i 0) i = 0 := Equiv.swap_apply_left i 0
  have h2 : (Equiv.swap i 0) j ≠ 0 := by
    intro h
    have hh : (Equiv.swap i 0) j = (Equiv.swap i 0) i := by rw [h, h1]
    exact hij ((Equiv.swap i 0).injective hh).symm
  show Equiv.swap ((Equiv.swap i 0) j) 1 ((Equiv.swap i 0) i) = 0
  rw [h1]
  exact Equiv.swap_apply_of_ne_of_ne (Ne.symm h2) (by decide)

lemma permToZeroOne_apply_j (i j : Fin 6) : permToZeroOne i j j = 1 := by
  show Equiv.swap ((Equiv.swap i 0) j) 1 ((Equiv.swap i 0) j) = 1
  exact Equiv.swap_apply_left ((Equiv.swap i 0) j) 1

/-- The merge map for an arbitrary pair of distinct labels: collapse `i` and `j`. -/
noncomputable def mergePair (i j : Fin 6) : Fin 6 → Fin 5 :=
  fun x => merge01 (permToZeroOne i j x)

/-- **Kernel of the merge map**: two labels have the same image iff they are equal or they are
exactly the merged pair. -/
lemma mergePair_eq_iff (i j : Fin 6) (hij : i ≠ j) (a b : Fin 6) :
    mergePair i j a = mergePair i j b ↔ a = b ∨ (a = i ∧ b = j) ∨ (a = j ∧ b = i) := by
  have hτ : Function.Injective (permToZeroOne i j) := (permToZeroOne i j).injective
  have hi : permToZeroOne i j i = 0 := permToZeroOne_apply_i i j hij
  have hj : permToZeroOne i j j = 1 := permToZeroOne_apply_j i j
  constructor
  · intro h
    rcases (merge01_eq_iff _ _).mp h with h' | ⟨h1, h2⟩ | ⟨h1, h2⟩
    · exact Or.inl (hτ h')
    · exact Or.inr (Or.inl ⟨hτ (by rw [h1, hi]), hτ (by rw [h2, hj])⟩)
    · exact Or.inr (Or.inr ⟨hτ (by rw [h1, hj]), hτ (by rw [h2, hi])⟩)
  · intro hmem
    rcases hmem with h | ⟨h1, h2⟩ | ⟨h1, h2⟩
    · rw [h]
    · rw [h1, h2]
      show merge01 (permToZeroOne i j i) = merge01 (permToZeroOne i j j)
      rw [hi, hj]
      decide
    · rw [h1, h2]
      show merge01 (permToZeroOne i j j) = merge01 (permToZeroOne i j i)
      rw [hi, hj]
      decide

/-! ### (A2) the proper form -/

/-- **Theorem A2, machine-checked.** Every pair of distinct labels of a proper 6-colouring is
carried by a unit pair. -/
theorem exists_unit_pair_of_pair (c : ℂ → Fin 6) (hc : ProperColoring 6 c)
    (i j : Fin 6) (hij : i ≠ j) :
    ∃ x y : ℂ, ‖x - y‖ = 1 ∧ c x = i ∧ c y = j := by
  by_contra h
  simp only [not_exists, not_and] at h
  refine no_proper_five_coloring ⟨fun z => mergePair i j (c z), ?_⟩
  intro x y hxy hEq
  have hne : c x ≠ c y := hc x y hxy
  rcases (mergePair_eq_iff i j hij (c x) (c y)).mp hEq with h' | ⟨h1, h2⟩ | ⟨h1, h2⟩
  · exact hne h'
  · exact h x y hxy h1 h2
  · exact h y x (by rwa [norm_sub_rev]) h2 h1

/-! ### (A) the measure form -/

/-- **Theorem A, machine-checked (weak measurable form).** For a measurable weak 6-colouring and
two distinct labels `i j`, it is *not* the case that almost every unit pair fails to carry the
pair `{i,j}`: the set of unit pairs carrying `{i,j}` has positive product measure. -/
theorem pair_transition_not_null (c : ℂ → Fin 6) (hc : Measurable c) (hw : WeakColoring 6 c)
    (i j : Fin 6) (hij : i ≠ j) :
    ¬ (∀ᵐ p ∂((volume : Measure ℂ).prod angularMeasure),
        ¬ ((c p.1 = i ∧ c (p.1 + direction p.2) = j) ∨
           (c p.1 = j ∧ c (p.1 + direction p.2) = i))) := by
  intro hnull
  have hc' : Measurable (fun z => mergePair i j (c z)) :=
    (measurable_of_finite (mergePair i j)).comp hc
  have hw' : WeakColoring 5 (fun z => mergePair i j (c z)) := by
    refine ⟨hc'.aemeasurable, ?_⟩
    filter_upwards [hw.2, hnull] with p hne hpair
    intro hEq
    rcases (mergePair_eq_iff i j hij (c p.1) (c (p.1 + direction p.2))).mp hEq with
      h' | ⟨h1, h2⟩ | ⟨h1, h2⟩
    · exact hne h'
    · exact hpair (Or.inl ⟨h1, h2⟩)
    · exact hpair (Or.inr ⟨h1, h2⟩)
  exact no_measurable_weak_five_coloring hc' hw'

end EuclideanFiveColor
end OAI

-- certificates
#print axioms OAI.EuclideanFiveColor.exists_unit_pair_of_pair
#print axioms OAI.EuclideanFiveColor.pair_transition_not_null
#check @OAI.EuclideanFiveColor.pair_transition_not_null
