/-
  Label merging at six colours: a machine-checked k = 6 theorem.

  Given a proper 6-colouring of the plane and two distinct labels, some unit pair carries
  exactly those two labels.  Proof: merging the two labels gives a 5-colouring; if no unit
  pair carried the two labels the merged colouring would be proper, contradicting
  `no_proper_five_coloring` (the paper's Theorem 1.1, machine-checked in the bundle).

  Special pair (0,1) proved directly; the general case by relabelling the colouring with an
  explicit permutation of Fin 6.
-/
import OAI.Geometry.PlaneColoring.Five

namespace OAI
namespace EuclideanFiveColor

/-- Merging labels `0` and `1`: the explicit 2-to-1 map `Fin 6 → Fin 5`. -/
def merge01 : Fin 6 → Fin 5 := ![0, 0, 1, 2, 3, 4]

lemma merge01_eq_iff (a b : Fin 6) :
    merge01 a = merge01 b ↔ a = b ∨ (a = 0 ∧ b = 1) ∨ (a = 1 ∧ b = 0) := by
  revert a b
  decide

/-- Special case: a proper 6-colouring has a unit pair of colours `0` and `1`. -/
theorem exists_unit_pair_zero_one (c : ℂ → Fin 6) (hc : ProperColoring 6 c) :
    ∃ x y : ℂ, ‖x - y‖ = 1 ∧ c x = 0 ∧ c y = 1 := by
  by_contra h
  simp only [not_exists, not_and] at h
  refine no_proper_five_coloring ⟨fun z => merge01 (c z), ?_⟩
  intro x y hxy hEq
  have hne : c x ≠ c y := hc x y hxy
  rcases (merge01_eq_iff (c x) (c y)).mp hEq with h' | ⟨h1, h2⟩ | ⟨h1, h2⟩
  · exact hne h'
  · exact h x y hxy h1 h2
  · exact h y x (by rwa [norm_sub_rev]) h2 h1

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

/-- **Theorem A2, machine-checked.** Every pair of distinct labels of a proper 6-colouring is
carried by a unit pair. -/
theorem exists_unit_pair_of_pair (c : ℂ → Fin 6) (hc : ProperColoring 6 c)
    (i j : Fin 6) (hij : i ≠ j) :
    ∃ x y : ℂ, ‖x - y‖ = 1 ∧ c x = i ∧ c y = j := by
  obtain ⟨x, y, hxy, hx, hy⟩ :=
    exists_unit_pair_zero_one (fun z => permToZeroOne i j (c z))
      (fun x y hxy hEq => hc x y hxy ((permToZeroOne i j).injective hEq))
  have key : ∀ (a b : Fin 6), permToZeroOne i j a = 0 → permToZeroOne i j b = 1 →
      a = i ∧ b = j := by
    intro a b ha hb
    constructor
    · exact (permToZeroOne i j).injective (by rw [ha, permToZeroOne_apply_i i j hij])
    · exact (permToZeroOne i j).injective (by rw [hb, permToZeroOne_apply_j i j])
  obtain ⟨hxi, hyj⟩ := key (c x) (c y) hx hy
  exact ⟨x, y, hxy, hxi, hyj⟩

end EuclideanFiveColor
end OAI

-- Axiom certificate and statement, for the record:
#print axioms OAI.EuclideanFiveColor.exists_unit_pair_of_pair
#check @OAI.EuclideanFiveColor.exists_unit_pair_of_pair
