/-
  swarm smwfycy1c / member m4 / direction d4 ("three-colour-invariant-lean")

  Lemma 8.9's "diamond" step: in a proper 3-colouring of K4 minus an edge
  (two triangles sharing the edge a--b), the two tips p, q receive the *same*
  colour.  No `fin_cases` and no `simp_all`: the whole content is the
  arithmetic invariant `r.val + a.val + b.val = 3` (three pairwise distinct
  elements of `Fin 3` have values 0, 1, 2, whose sum is 0+1+2 = 3), so two
  tips have equal `.val` and hence are equal.
-/
import Mathlib

namespace M4

/-- **Invariant.**  If `a ≠ b` and `r` differs from both, then the three
values add up to `0 + 1 + 2 = 3`.  This is pure linear integer arithmetic:
`r.val, a.val, b.val < 3` and are pairwise distinct. -/
lemma val_sum_eq_three {a b r : Fin 3} (hab : a ≠ b) (hra : r ≠ a) (hrb : r ≠ b) :
    r.val + a.val + b.val = 3 := by
  have h1 : r.val ≠ a.val := fun h => hra (Fin.ext h)
  have h2 : r.val ≠ b.val := fun h => hrb (Fin.ext h)
  have h3 : a.val ≠ b.val := fun h => hab (Fin.ext h)
  omega

/-- **The diamond step.**  Two vertices `p`, `q` of a proper 3-colouring that
are both adjacent to the same two differently coloured vertices `a ≠ b` have
the same colour. -/
theorem three_color_diamond {a b p q : Fin 3} (hab : a ≠ b)
    (hpa : p ≠ a) (hpb : p ≠ b) (hqa : q ≠ a) (hqb : q ≠ b) : p = q := by
  have hp : p.val + a.val + b.val = 3 := val_sum_eq_three hab hpa hpb
  have hq : q.val + a.val + b.val = 3 := val_sum_eq_three hab hqa hqb
  exact Fin.ext (by omega)

/-- The invariant in the form actually used: the third colour is *determined*,
i.e. the complement of `{a, b}` in `Fin 3` is a singleton. -/
theorem eq_of_ne_of_ne {a b r s : Fin 3} (hab : a ≠ b)
    (hra : r ≠ a) (hrb : r ≠ b) (hsa : s ≠ a) (hsb : s ≠ b) : r = s :=
  three_color_diamond hab hra hrb hsa hsb

-- Axiom audit for the main theorem.
#print axioms M4.three_color_diamond
#print axioms M4.val_sum_eq_three

end M4
