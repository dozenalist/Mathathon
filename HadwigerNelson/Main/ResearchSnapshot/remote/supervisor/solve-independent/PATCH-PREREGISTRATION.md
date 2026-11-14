# Patch pre-registration (written before any computation in this block)

**Parameter.** Honeycomb cell family at `a = 1/5` (fixed for the whole block). Cell `(p,q) in Z^2` is
the Voronoi hexagon of the triangular lattice of spacing `a sqrt3`; forced offsets are
`F = {v : dmin(v) < 1 < dmax(v)}`, which at this `a` is exactly `{v : N(v) in {4,7,9,12,13}}`,
`N(p,q) = p^2+pq+q^2`, `|F| = 42` (computed exactly in an earlier block and re-verified here).

**The one patch.** `P = { v in Z^2 : N(v) <= 19 }` — the closed Eisenstein-norm ball of radius 19.
Rationale, stated once: (i) it has `|P| = 73 <= 81`; (ii) it is induced, so its 6-UNSAT would refute
every 6-colouring of the whole family at this `a`, not just a periodic one; (iii) it contains `0` and
every forced offset (`F ⊆ {N <= 13}`), so no adjacency is lost at the centre; (iv) `N <= 19` is the
largest ball under the 81-vertex cap (`N <= 21` already has 85 vertices), so the cap is met as
tightly as it can be without changing shape.

**What is asked of it.** 6-colourability of the induced subgraph `G[P]` of `Cay(Z^2, F)`.

* SAT ⟹ print the colouring and verify all edges; this is a colouring of 73 cells of the family
  (it does not extend to the plane by itself).
* UNSAT ⟹ refute 6-colouring of `G[P]`, hence of the whole family at `a = 1/5`; certificate must be
  inspectable (a clique, or a DRUP/LRAT proof with a checker), not merely a solver verdict.
* Timeout ⟹ inconclusive, recorded as such.

**No sweep.** This file names exactly one patch and one number of colours. No other patch, radius or
`a` is examined in this block.
