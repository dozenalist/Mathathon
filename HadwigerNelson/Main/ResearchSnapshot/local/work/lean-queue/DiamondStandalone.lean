-- Standalone audit copy: original import Mathlib narrowed to the built-in Omega tactic.
-- Tests the identical theorem bodies on local Lean 4.35.0; not pinned-project integration.
import Lean.Elab.Tactic.Omega

/-!
# The reusable invariant behind the Moser-spindle non-3-colourability

In a proper 3-colouring of the "diamond" K4 minus an edge (two unit equilateral
triangles sharing an edge), the two degree-2 vertices ("tips") receive the *same*
colour.  The paper's Lemma 8.9 uses this twice and then the unit edge between the
two tips.

The replacement for the development's `three_color_diamond` avoids the
3^4 = 81-case `fin_cases`/`simp_all` enumeration: the invariant is
`p.val + a.val + b.val = 3`, since three elements of `Fin 3` with pairwise
distinct values sum to 0 + 1 + 2 = 3.
-/

namespace SimplifyAngular

/-- Two vertices `p`, `q` of a proper 3-colouring that are both adjacent to the
same two differently coloured vertices `a ≠ b` have the same colour. -/
theorem three_color_diamond_omega {a b p q : Fin 3} (hab : a ≠ b)
    (hpa : p ≠ a) (hpb : p ≠ b) (hqa : q ≠ a) (hqb : q ≠ b) : p = q := by
  have key : ∀ r : Fin 3, r ≠ a → r ≠ b → r.val + a.val + b.val = 3 := by
    intro r hra hrb
    have h1 : r.val ≠ a.val := fun h => hra (Fin.ext h)
    have h2 : r.val ≠ b.val := fun h => hrb (Fin.ext h)
    have h3 : a.val ≠ b.val := fun h => hab (Fin.ext h)
    have hr := r.isLt
    have ha := a.isLt
    have hb := b.isLt
    omega
  exact Fin.ext (by have := key p hpa hpb; have := key q hqa hqb; omega)

/-- The spindles's two tips: a proper 3-colouring of the diamond forces equality. -/
theorem diamond_tips {c0 c1 c2 c3 : Fin 3}
    (h01 : c0 ≠ c1) (h02 : c0 ≠ c2) (h12 : c1 ≠ c2)
    (h31 : c3 ≠ c1) (h32 : c3 ≠ c2) : c0 = c3 :=
  three_color_diamond_omega h12 h01 h02 h31 h32

end SimplifyAngular

#print axioms SimplifyAngular.three_color_diamond_omega
#print axioms SimplifyAngular.diamond_tips

