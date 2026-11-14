# Cell-family theorem, corrected and rigorously scoped (v2)

Supersedes `CELL-NOGO.md` (v1). Certificate: `verify_cell_nogo_v2.py` -> `verify_cell_nogo_v2.out`
(all asserts pass, exact arithmetic in `Q(sqrt3)`). Claim-by-claim audit of v1, of the retiring
rectangle worker (`supervisor/solve-six-colouring/FINDINGS.md`) and of the retiring graph worker
(`supervisor/solve-graphs/REPORT.md`): `LEDGER.md`.

## 1. Boundary ownership: the criterion is STRICT

A tiling by closed convex cells is not a partition: neighbours share their common edge, so a
function cannot be constant on two closed cells of different colours. Every cell tiling needs a
boundary-ownership rule. Whatever the rule, **interior points are unambiguous**: a point of
`int C` belongs to `C` under every rule. That gives a convention-free criterion.

**Lemma 1 (boundary ownership).** Let `{C_lambda}` be a family of compact convex sets with
nonempty interior whose interiors are pairwise disjoint and whose union is dense in the plane (the
closed convex cells of a tiling), and let `c` be constant on each interior `int C_lambda`. The
interiors are **not** a partition: they are disjoint open sets with dense union, and they omit the
tiling's 1-skeleton. Put `dmin(v) = inf{|q-p| : p in C_0, q in C_v}` and `dmax(v) = sup` (same sets).
Then

1. if `dmin(v) < 1 < dmax(v)`, there are `p in int C_0`, `q in int C_v` with `|p-q| = 1`, so
   `c` cannot be proper if `int C_0`, `int C_v` carry the same colour;
2. if `dmin(v) = 1` or `dmax(v) = 1`, every pair at distance exactly `1` in `C_0 x C_v` involves a
   boundary point of one of the two cells, so whether it is a violation depends on the boundary
   rule;
3. if `dmin(v) > 1` or `dmax(v) < 1`, there is no pair at distance `1` at all.

*Proof.* (1) interiors are dense in their closures, so `inf`/`sup` of `|q-p|` over
`int C_0 x int C_v` equal `dmin`,`dmax`; that domain is connected, so its distance set is an
interval with closure `[dmin,dmax]`, and it contains every value strictly between `dmin` and
`dmax`. ∎

Every point of the 1-skeleton is on the boundary of all cells meeting there, is in no interior, and
must be assigned by an ownership rule; that is exactly why case 2 depends on the rule and case 1
does not.

So the criterion for "the two cells must differ" is `dmin < 1 < dmax`, **strict**, and it is the
strongest convention-free one. The weak form `dmin <= 1 <= dmax` is correct only for *closed*
cells with both cells counted — which no function does. Concretely, at the honeycomb value
`a = 1/sqrt13` two tangent hexagons have `dmax = 1` exactly, and the unit pair is the two opposite
vertices of their union (certified exactly in `verify_cell_nogo_v2.py` §E): a vertex belongs to
exactly one of the three cells meeting there, so under a border rule it need not belong to either
tangent cell. Tangency therefore does **not** force.

> **REPAIR (later block, `NULL-TRANSFER.md`).** The following paragraph was **wrong** and is
> withdrawn. A positive result does **not** require colouring the 1-skeleton. By the null-set
> transfer lemma, a proper `k`-colouring of `C \ B` (equivalently: a colouring of all cell
> interiors, separated on the *strict* forced pairs, with `diam C <= 1`) already gives
> `chi(R^2) <= k` via translation plus de Bruijn–Erdos compactness. No ownership rule is ever
> needed, and tangency pairs (`dmin = 1` or `dmax = 1`) impose no constraint at all. The original
> text follows, struck through in effect:

Lemma 1 is one-sided on purpose: it is exactly what a no-go needs. A *positive* result (a
`k`-colouring of the plane from a `k`-colouring of the induced Cayley graph) additionally requires
colouring the 1-skeleton so that no boundary point is at distance `1` from a point of its own
colour — a separate step, unproven here and unproven in the rectangle worker's report (§3 there).

## 2. The corrected theorem

`Lambda` = triangular lattice with spacing `s = a sqrt3`; cell = its Voronoi cell, a regular
hexagon of circumradius `a`, inradius `s/2`, faces normal to the six neighbour directions.
`N(p,q) = p^2 + pq + q^2` is the Eisenstein norm, `|v|^2 = 3 a^2 N`.

**Theorem 2.** Let `a > 1/sqrt13` and let `c : R^2 -> {colours}` be constant on the interior of
every honeycomb cell (values on the 1-skeleton arbitrary). Then `c` uses at least **7** colours.
For `a > 1/2` this is vacuous (a cell interior then contains a unit pair); on `(1/sqrt13, 1/2]`
it is proved from the forced set below. Seven is attained at `a = 2/5`.

*Proof.* Distances scale linearly in `a`, so forcedness reduces to `a^2 mu^2(l) < 1 < a^2 nu^2(l)`
with `mu, nu` the values at `a = 1`, computed exactly. Per-ring results (exact endpoints, `a`):

| ring `N` | strictly forced for `a` in |
|---|---|
| 1 | `(1/sqrt13, inf)` |
| 3 | `(1/5, 1)` |
| 4 | `(1/sqrt28, 1/sqrt3)` |
| 7 | `(1/sqrt43, 1/sqrt7)` |
| 9 | `(1/7, 1/sqrt12)` |
| 12 | `(1/8, 1/4)` |
| 13 | `(1/sqrt67, 1/sqrt19)` |
| ... | every `N >= 12` has upper endpoint `<= 1/4 < 1/sqrt13` |

Window sufficiency (no search truncation): a ring forced at `a >= 1/sqrt13` satisfies
`dmin^2(a=1) <= 1/a^2 <= 13`, and `dmin(a=1) >= |v|(a=1) - 2`, so `3N <= (sqrt13+2)^2 = 31.4`,
i.e. only `N in {1,3,4,7,9}` can ever be forced in this range. Hence the **exact** forced set on
`a in (1/sqrt13, 1/2]` is

    {1,3,4,7,9}  on (1/sqrt13, 1/sqrt12)      (0.277350, 0.288675)
    {1,3,4,7}    on (1/sqrt12, 1/sqrt7)       (0.288675, 0.377964)
    {1,3,4}      on (1/sqrt7, 1/2]            (0.377964, 0.500000]

— all three verified exactly, not sampled. On the whole range it contains the difference set of
`T^2` = the square of the triangular lattice (`N in {1,3,4}`, i.e. `|v| <= 2s`). `T^2` has a
7-clique (`{0} u N(0)`, all 42 ordered pairs strictly forced) and is 7-coloured by
`(p,q) |-> p + 3q mod 7`, zero-free on all 18 vectors with `0 < N <= 4`. So the constraint graph
has chromatic number `>= 7`. ∎

**Sharpness and the exact margins at `a = 2/5`** (the paper's hexagonal seven-colouring,
`results/COMPRESSED-PROOF.md`: circumradius `r = 2/5`, index-7 sublattice `(2-omega)Lambda`,
`|2-omega|^2 = 7`): the smallest nonzero same-colour vector has `N = 7`, witness `(p,q) = (-3,1)`,
with `dmin^2 = 28/25 = 1.12 > 1` strictly (the paper's cruder `(sqrt21-2)(2/5) = 1.0335` uses the
maximal width `2a` instead of the width in that direction). So the family is non-vacuous and this
instance is proper with exactly 7.

**Both endpoints are now correct and both moved against v1:**
* bottom `1/sqrt13` is **excluded** (open): at `a = 1/sqrt13` ring 1 is a tangency and Lemma 1(2)
  applies — certified, the maximiser is a vertex pair.
* top `1/2` is **included**: at `a = 1/2` a single cell has `dmax = 1` attained only at two
  opposite vertices, so its interior distance set is `(0,1)`; rings 1,3,4 are still strictly
  forced and the seven-colouring is still proper (`dmin^2 = 7a^2 = 1.75`). v1's `< 1/2` was too
  small; for `a > 1/2` the family is empty.

## 3. What the theorem does and does not say

It is a statement about **one family**: colourings constant on cell interiors of honeycombs with
`a > 1/sqrt13` (cell diameter `> 0.5547`). It says nothing about
* honeycombs or any tiling with cells of diameter `<= 0.5547` (the whole small-cell regime),
* colourings that are not cell-constant at all.

**v1's sentence "a six-colouring must be cell-free" is withdrawn.** It cannot follow from a
restricted parameter family: the small-cell regime is exactly where a cell-constant colouring
would most resemble an arbitrary one, and there the argument is silent. The correct content is:
*no six-colouring is constant on the interiors of the cells of a honeycomb with `a > 1/sqrt13`*,
plus the same for square cells at `c = 3/5` (`square_family.py`, re-checked under the strict
criterion). Whether any cell family at all admits six colours is **open**.

## 4. Limit of the 7-clique method (imported, re-derived)

From the retiring rectangle worker, re-derived independently: if 7 planar points have all pairwise
distances in `[A,B]` then `B >= (sqrt7 - 1)A` (seven interior-disjoint disks of radius `A/2`
inside the `A/2`-neighbourhood of the hull; isodiametric `area <= pi B^2/4`, Barbier
`perim <= pi B`), giving `6A^2 <= B^2 + 2AB`. Forced pairs have offsets in `(1-D, 1+D)` with `D`
the cell diameter, so a 7-**clique** needs `D >= 1 - 2/sqrt7 = 0.24407`. For the honeycomb `D = 2a`, this rules out
7-clique certificates only for `a < 0.12204`. It does **not** close the clique route on
`[0.12204, 0.27735)`: there a 7-clique is not excluded, and none has been found. It says nothing
at all about non-clique finite 7-chromatic subgraphs, at any `a`. (An earlier phrasing here and in
`STATUS.json` said the K7 route was "closed" there; that was wrong and is corrected.)

## 5. Precise open problem left behind

*Honeycomb, `a in [0.12204, 0.27735)`: is the Cayley graph `Cay(Lambda, F_a)` with
`F_a = {v : dmin(v) < 1 < dmax(v)}` 6-colourable?* A positive answer needs a periodic colouring;
a negative answer needs a finite subgraph with chromatic number 7 that is not a clique (the clique
route is closed by §4). Both are finite, checkable objects. Nothing in this block bounds
`chi(R^2)` in either direction.
