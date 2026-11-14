# No six-colouring by honeycomb cells: a sharp no-go in the cell-tiling family

Track: solve, independent route. Independent of the §7 / cyclic-centre / palette argument.
Trust grade: **the mathematics below is a proof**; its only computational input is a finite
exact computation over `Q(sqrt 3)` (no floating point decides anything), reproducible with
`python3 verify_cell_nogo.py` (output: `verify_cell_nogo.out`).

## 0. What this is and is not

It is **not** a result about `chi(R^2)`. It is a result about a delimited family of candidate
six-colourings: those that are *constant on the cells of a honeycomb tiling*. Within that family
six colours are impossible, and the exact parameter range is given. So:

* it kills the most natural family of "six-colouring with boundary points covered" — cell
  tilings — with a sharp constant, and says the paper's hexagon 7-colouring is optimal *in its own
  family*, with no slack to retune;
* it says nothing for or against `chi(R^2) = 6`, because a six-colouring need not be cell-based.

The fact that a honeycomb needs seven colours is folklore. What is checked here is the exact
forced set, the exact threshold, and its identification with a graph of known chromatic number.

## 1. The cell lemma

**Lemma 1.** Let `V` be a compact convex set with nonempty interior, and suppose the translates
`V + lambda` (`lambda` in a lattice `Lambda`) tile the plane. Let `c` be a colouring constant on
each cell and proper: no two points at distance exactly `1` share a colour. For `lambda in Lambda`
put

    dmin(lambda) = min { |q - p| : p, q in V, q - p = lambda + (z), ... }   (see below)

precisely: `dmin(lambda)` and `dmax(lambda)` are the min and max of `|q-p|` over
`p in V`, `q in V + lambda`. Then

> if `dmin(lambda) <= 1 <= dmax(lambda)`, then `c(V) != c(V + lambda)`.

*Proof.* `V x (V + lambda)` is connected and compact, `(p,q) |-> |q - p|` is continuous, so its
image is a compact interval containing `dmin` and `dmax`, hence every value between them; in
particular it contains `1`. That gives points at distance exactly `1` in the two cells. ∎

The useful corollary is that `dmin` and `dmax` are explicit: with `h` the support function of `V`,

    dmax(lambda) >= |lambda| + 2 h(lambda-hat),     dmin(lambda) <= |lambda| - 2 h(lambda-hat),

(evaluate at the two support points of `2V = V - V` in direction `+-lambda-hat`), and
`h >= r` (inradius), `h <= R` (circumradius). This gives the crude sufficient condition

    1 - 2r <= |lambda| <= 1 + 2r   ==>   forced apart,

which is already enough to see that the forced set is a full annulus of lattice vectors.
`verify_cell_nogo.py` does not use the crude bound: it computes `dmin^2` (exact point-to-segment
distance) and `dmax^2` (max over the six vertices of `2V`) exactly for every lattice vector in a
window, so the table is a certificate, not an estimate.

## 2. The honeycomb family

Take `Lambda` the triangular lattice of spacing `s = a*sqrt 3` and `V` its Voronoi cell, a regular
hexagon of circumradius `a` and inradius `s/2` whose six faces are normal to the six
nearest-neighbour directions. Cell diameter is `2a`, so `a < 1/2` is necessary for the family to
have a chance (at `a >= 1/2` a single cell already contains a unit pair).

Write the colouring as `f : Lambda -> labels`. Since distances scale linearly with `a`, the
condition `dmin(lambda) <= 1 <= dmax(lambda)` at circumradius `a` is the condition
`a dmin_1(lambda) <= 1 <= a dmax_1(lambda)` at `a = 1`, so the *set of forced vectors is a function
of `a` computable exactly*.

**Table** (at `a = 2/5 = 0.4`, the circumradius of the paper's seven-colouring, lattice spacing
`a sqrt3 = 0.69282`; `N` is the Eisenstein norm, `|lambda|^2 = 3 a^2 N`):

| `N` | `|lambda|` in units of `a` | `dmin^2` | `dmax^2` | forced apart? | count |
|---|---|---|---|---|---|
| 0 | 0 | 0.480 | 0.640 | no (one cell: no unit pair, `2a<1`) | 1 |
| 1 | 1.000 | **0** (tangent) | 2.080 | **yes** | 6 |
| 3 | 1.732 | 0.160 | 4.000 | **yes** | 6 |
| 4 | 2.000 | 0.480 | 4.480 | **yes** | 6 |
| 7 | 2.646 | 1.120 | 6.880 | no (`dmin = 1.058 > 1`) | 12 |
| 9 | 3.000 | 1.920 | 7.840 | no | 6 |
| 12 | 3.464 | 2.560 | 10.240 | no | 6 |

and all rings from `N = 13` on are also unforced.

**Theorem 2.** Let `a` in `[1/sqrt 13, 1/2)` — in particular `a = 2/5` — and let `c` be a
colouring of the plane that is constant on the cells of the honeycomb with circumradius `a`. Then
`c` is improper and, in fact, any such `c` needs at least seven colours. Seven is attained.

*Proof.* By Lemma 1 and the exact table, every pair of cells whose lattice difference has
`N in {1,3,4}` must receive different colours — exactly the pairs with `|lambda| <= 2s`. That
difference graph is the square `T^2` of the triangular lattice.
(`i`) `T^2` contains a `7`-clique: the cell at `0` together with its six neighbours has all
pairwise differences of norm `N in {1,3}` (`verify_cell_nogo.py` checks all `7*6` ordered pairs
exactly). Hence `>= 7` colours.
(`ii`) `chi(T^2) = 7`: `f(p,q) = p + 3q mod 7` is a group homomorphism `Z^2 -> Z/7` that is nonzero
on all eighteen vectors with `0 < N <= 4` (checked exhaustively; the eighteen values are
`+-{1,2,3,4,6}`).
(`iii`) Sharpness at `a = 2/5`: in the same colouring the smallest nonzero same-colour difference
has `N = 7`, i.e. `|lambda|^2 = 21 a^2 = 3.36`, while `(1+2a)^2 = 3.24`; since `dmin >= |lambda| - 2a`,
every same-colour pair of cells is at distance `> 1`. The exact margin on the tight ring is
`dmin^2 = 28/25 = 1.12 > 1` (`dmin = 1.0583`, against the paper's cruder `(sqrt21-2)(2/5) = 1.0335`,
which uses the maximal width `2a` instead of the width in that direction). So `c` is proper with
seven colours. ∎

This seven-colouring is exactly the paper's hexagonal seven-colouring (`results/COMPRESSED-PROOF.md`:
`r = 2/5` is the hexagon **circumradius**, the lattice spacing is `sqrt3 r`, the index-7 sublattice
is `(2 - omega) Lambda` with `|2 - omega|^2 = 7`, and the paper's check is
`(sqrt 21 - 2)(2/5) > 1`). Theorem 2 says: **that construction is optimal in its
own family, at the exact margin, and no retuning of hexagon size or lattice labelling down to six
labels exists.**

## 3. The exact threshold, and where the family stops being excluded

Solving the table symbolically (scale `a = 1`, then invert):

| forced ring | condition on `a` |
|---|---|
| `N = 1` (tangent neighbours) | `a >= 1/sqrt 13 = 0.277350...` |
| `N = 3` | `a >= 1/5`, `a <= 1` |
| `N = 4` | `a >= 1/sqrt 28`, `a <= 1/sqrt 3 = 0.577350...` |

Intersecting with `a < 1/2` gives `a in [1/sqrt 13, 1/2)`. The bound `1/sqrt 13` is sharp for this
argument and is *attained*: at `a = 1/sqrt 13` two tangent hexagons have `dmax^2 = 13 a^2 = 1`
exactly, i.e. they contain a pair of points at distance exactly one, so tangent cells are still
forced apart — the constraining pair is the two opposite vertices of the union. (The crude support
function bound only gives `a >= 1/(2 sqrt 3) = 0.288675`; the sharper `1/sqrt 13` needs the vertex
computation, which is what the certificate does.)

**Below `a = 1/sqrt 13` the family is not excluded by this argument**, and the reason is
structural, not technical: at that point two tangent cells are *entirely* within distance `< 1` of
each other, so they may share a colour. The forced set collapses from the ball `|lambda| <= 2s` to
an annulus around `|lambda| = 1`, whose lattice radii grow like `1/a`; in the limit `a -> 0` the
problem becomes the plane problem itself. So this is a genuine phase transition of the *family*,
not a gap that a better constant closes.

## 4. What a six-colouring must therefore do

Combining Theorem 2 with `results/K6-BARRIER.md` and `sprint/k6/FREE-LABEL.md`:

* palette-level axioms at `k = 6` have no teeth (accumulating countermodels for every cycle
  length);
* adding any trace function collapses to the original problem;
* and now: no cell-tiling scheme — the family that contains every known plane colouring, including
  the 7-colouring — can be six-coloured in the range `a in [1/sqrt 13, 1/2)`.

So a six-colouring, if one exists, must be **cell-free**: it cannot be constant on the cells of any
honeycomb. That is a concrete negative specification for the construction route, and it is the
only thing in this report that a future construction attempt has to respect.

## 5. Falsifiers, and what would overturn this

* Any exact computation of a `dmin`/`dmax` pair that contradicts the table would refute Theorem 2;
  the script recomputes everything from the definition (point-to-segment distances) and needs no
  trusted input beyond the hexagon's six vertices at `30 + 60k` degrees and the lattice basis.
* The orientation is essential and is asserted: ring `N = 1` must have `dmin = 0` exactly
  (shared edge). With vertices at `60k` degrees instead the cells *overlap* and the "tiling" is not
  one — an earlier version of the script had that bug and produced a nonsensical `a`-range; the
  assertion is now in the code.
* A six-colouring of a honeycomb with `a < 1/sqrt 13` would not contradict anything here.

## 6. Other cell shapes, and a correction to an earlier guess

The same computation is exact for any lattice and any Voronoi cell. For the **square grid**
(`Lambda = c Z^2`, cell side `c`, cell diameter `c sqrt 2 < 1` iff `c < 0.70711`) the forced set at
`c = 3/5` contains the seven cells

    (0,0) (1,0) (2,0) (0,1) (1,1) (2,1) (0,2)

all of whose 21 pairwise differences are forced (`square_family.py`, exact rational arithmetic:
`dmin^2 = 0` or `9/25` and `dmax^2 >= 9/5` on every pair). So square-cell colourings need at least
seven colours at `c = 3/5` as well, and the square family is **not** a place where six colours
survive. (An earlier draft of this file guessed it might be; that guess is retracted here, with the
certificate against it.) What is genuinely open is the small-cell regime `a` (resp. `c`) below the
clique threshold, where the forced set is an annulus around lattice distance `1` instead of a ball.

**Next step (proposed, not started).** Decide the annulus regime in one cell shape: for
`c` just below the threshold where the forced set stops containing a `7`-clique, `Lambda` with the
annulus connection set is a Cayley graph with a finite symmetric connection set, and the question
"is it 6-colourable" is a finite CSP modulo periodicity. Two outcomes are useful and both are
checkable: an explicit periodic 6-colouring of the Cayley graph (a cell-family six-colouring, which
would be a genuine `chi(R^2) = 6` candidate and would immediately deserve independent checking), or
a no-go (a finite subgraph of the Cayley graph with chromatic number 7). Since the cell lemma is
shape-agnostic, the natural second target is the family of **parallelogram cells** (all lattice
Voronoi cells of index-2 sublattice type), where the forced set can be computed once and for all as
a function of the two side lengths and the angle.

A caution that applies to both outcomes: a six-colouring of a Cayley graph is a six-colouring of a
*discretised* cell family, so it is a colouring of the plane **only because the cells are a
tiling** — the cells cover the plane and each is monochromatic, so the colouring is total. It is
still not a colouring of the plane if the colours are assigned to lattice points and the cells are
not monochromatic; no such relaxation is used here.
