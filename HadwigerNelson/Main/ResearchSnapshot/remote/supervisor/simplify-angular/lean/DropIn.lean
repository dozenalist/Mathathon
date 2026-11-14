import Mathlib

/-! Drop-in replacement for `OAI.EuclideanFiveColor.three_color_diamond`
(`lean/OAI/Geometry/PlaneColoring/Moser.lean:156`), same statement, same namespace.
Its only consumers are the two calls in `moser_not_three_colorable` (lines 161, 164).

The development's proof is a 3^4 = 81-case `fin_cases <;> fin_cases <;> fin_cases <;> fin_cases
<;> simp_all`.  The invariant here is `r.val + a.val + b.val = 3`, one `omega` call. -/
namespace OAI
noncomputable section
namespace EuclideanFiveColor

theorem three_color_diamond {a b p q : Fin 3} (hab : a≠b)
    (hpa : p≠a) (hpb : p≠b) (hqa : q≠a) (hqb : q≠b) : p = q := by
  have key : ∀ r : Fin 3, r ≠ a → r ≠ b → r.val + a.val + b.val = 3 := by
    intro r hra hrb
    have h1 : r.val ≠ a.val := fun h => hra (Fin.ext h)
    have h2 : r.val ≠ b.val := fun h => hrb (Fin.ext h)
    have h3 : a.val ≠ b.val := fun h => hab (Fin.ext h)
    have hr := r.isLt; have ha := a.isLt; have hb := b.isLt
    omega
  exact Fin.ext (by have := key p hpa hpb; have := key q hqa hqb; omega)

end EuclideanFiveColor
end
end OAI
