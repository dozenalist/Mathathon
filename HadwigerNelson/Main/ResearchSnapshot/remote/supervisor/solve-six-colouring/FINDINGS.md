# Rectangular cell-tiling family at k = 6: exact criterion, certified no-go, and the residual region

Block: 2026-11-14 05:10-05:45 UTC. Owned paths: `supervisor/solve-six-colouring/`.
Status: **exact computation, single implementation, self-checked against an independent
`Fraction` reference; not yet independently re-implemented** (see "trust grade").

## 1. The family and the exact criterion  (proved; no analysis/measurability input)

Fix `0 < s, t` with `s^2 + t^2 < 1`. Let `L = sZ x tZ` and let the **cells**
`R(i,j) = [is-s/2,is+s/2] x [jt-t/2,jt+t/2]` be the (closed) Voronoi rectangles of `L`; they
tile the plane. A **cell colouring** is any `f : Z^2 -> {1,...,k}`; the induced plane colouring is
`c(x) = f(i,j)` for `x` in the interior of `R(i,j)` (values on the shared edges are irrelevant:
they are unions of segments and can be assigned arbitrarily, see SS3).

For `v = (ps, qt)` put

    dmin^2 = max(0,|p|-1)^2 s^2 + max(0,|q|-1)^2 t^2      (closest approach of R(0,0), R(v))
    dmax^2 = (|p|+1)^2 s^2     + (|q|+1)^2 t^2            (farthest pair)

**Lemma 1 (interval).** The set of distances `{|x-y| : x in R(0,0), y in R(v)}` is the closed
interval `[dmin, dmax]`.
*Proof.* `R(0,0) x R(v)` is connected and compact, `(x,y) |-> |x-y|` is continuous, so the image is
a compact interval of `R`; its endpoints are the min and the max, attained. The formulas are the
two-coordinate min/max of `|(z,y)-(x,w)|^2` over rectangles. `square`

**Lemma 2 (criterion).** `v` is forced `:<=> dmin <= 1 <= dmax` is exactly the statement that some
`x in R(0,0)`, `y in R(v)` have `|x-y| = 1`. Hence a cell colouring is **proper** iff no colour
class contains two cells whose difference is forced. Let `F = {v forced}`; then

    a proper k-colouring of the plane constant on cells exists  <=>  Cay(Z^2, F) is k-colourable.

*Both directions are exact and use no regularity assumption.* (=>) the colouring avoids forced
differences. (<=) given `f` with no monochromatic forced difference: two points at distance 1 lie
either in the same cell (diameter `sqrt(s^2+t^2) < 1`, impossible) or in cells differing by a
vector that is not forced, hence by Lemma 1 not at distance 1. `square`

**Lemma 3 (finite search space).** `forced` requires `dmin <= 1` and `dmin >= |v| - sqrt(s^2+t^2)`,
so `|v| <= 1 + sqrt(s^2+t^2)`; with `s,t >= i0/60` this gives explicit integer bounds
`|p| <= 1 + 60/i0` etc. Every computation below is therefore finite, and is done in **exact
integer arithmetic** with common denominator 60 (`M = 3600`):

    forced(i,j,p,q)  <=>  sq(p) i^2 + sq(q) j^2 <= 3600 <= (|p|+1)^2 i^2 + (|q|+1)^2 j^2,
    sq(n) = max(0,|n|-1)^2,   s = i/60, t = j/60.

**Lemma 4 (7-clique certificate).** If `F` contains 6 non-zero vectors pairwise differing by
elements of `F`, then `{0} u {v_1,...,v_6}` is 7 cells pairwise forced, needing 7 distinct
colours. So **no proper 6-colouring** of that tiling (of the plane at all) exists.

**Lemma 5 (monotone box test, certified cover).** For fixed `p,q`, `dmin^2` and `dmax^2` are
increasing in `s` and in `t`. Hence on the box `s in (i/60,(i+1)/60]`, `t in (j/60,(j+1)/60]`
every `v` with `dmin^2((i+1)/60,(j+1)/60) <= 1` and `dmax^2(i/60,j/60) >= 1` is forced
throughout the box. A 7-clique in *that* superset kills the whole box, not just a grid point.

## 2. Certified result  (exact; ONE implementation + independent-arithmetic self-test)

Search space declared: all boxes of the grid `(i/60,(i+1)/60] x (j/60,(j+1)/60]` with
`1 <= i <= j <= 59` (WLOG `s <= t` by the swap symmetry of `(s,t,p,q)`), `i^2 + j^2 < 3600`
(lower corner inside `s^2+t^2 < 1`). That is **1401 boxes**; they cover the entire open region
`{0 < s <= t, s^2 + t^2 < 1}`.

* **681 boxes certified**: the guaranteed-forced set contains a 7-clique (Lemma 4 + 5).
* **720 boxes not decided** by this test; a bounded clique search on them found no 7-clique
  (largest clique found: 6), so the certificate method provably cannot decide them.

**Theorem (computed, exact).** For every `s > 13/30` with `s <= t` and `s^2 + t^2 < 1`
(i.e. every box with `i >= 26`), and for 16 further anisotropic boxes with `i <= 5`
(`(i,j)` = (1,59),(2,58),(2,59),(3,58),(3,59),(4,55),(4,57),(4,58),(4,59),(5,52),(5,53),
(5,55),(5,56),(5,57),(5,58),(5,59)), the rectangle tiling above admits **no proper 6-colouring**;
equivalently no proper 6-colouring of the plane is constant on those cells.
*Every* certified box is killed by one explicit 7-clique of pairwise-forced offsets, recorded in
`out/cover.json` (e.g. box (30,42): offsets (0,0),(±1,0),(0,±1),(-1,-1),(-1,1)).

Boundary points handled explicitly:
* `s^2+t^2 = 1`: excluded from the family, and correctly so - the cell has two opposite corners at
  distance exactly 1 (the cell contains a unit segment), so *no* cell colouring is proper there;
  the family is the open region, so the closed box cover of SS2 loses nothing.
* `dmin = 1` or `dmax = 1` exactly: `1` lies in the closed interval, so `v` is forced. The
  integer tests use `<=`/`>=`, matching this. (This is the "tangency counts" convention; the
  triangle-lattice worker's honeycomb check uses the same convention.)
* `s = 0` or `t = 0` (rank-one lattice, no tiling) excluded; boxes with `i = 0` are handled by
  taking the lower corner `0` as the *infimum* of `dmax^2` on the open box, which is legitimate.

## 3. What a finite certificate would imply, and what it would NOT

* A 6-colouring of `Cay(Z^2,F)` for **some** `(s,t)` is, by Lemma 2, a genuine proper 6-colouring
  of the whole plane: `chi(R^2) <= 6`. It is *not* "a colouring of a discretisation"; the finite
  CSP is exactly equivalent to a full-plane colouring inside this family, boundary points included
  (edge sets are 1-dimensional, measure zero, and any assignment on them keeps properness: a
  distance-1 pair is either in one cell or in two cells with interiors involved, and a point on an
  edge has interior points of its own cell at every distance <= its distance to the other edge,
  so the Lemma 2 argument covers them).
* Conversely the certified boxes above are a *negative* result about this family only. They do
  **not** say `chi(R^2) >= 7`, and they do not touch non-cell-constant colourings.
* The residual region (`s` small, or `s` small relative to `t`) is genuinely open: there the
  forbidden band `[dmax^{-1}(1), dmin^{-1}(1)]` is thin compared with the lattice spacing's
  freedom, cliques are small (<= 6), and the question becomes a chromatic-number question for a
  "thickened unit-distance" Cayley graph of `Z^2`, which no 20-minute computation settles.

## 4. Trust grade and what is missing

* Grade: **machine-checked arithmetic**, one implementation (`scripts/cells.py`, `scripts/cover.py`),
  with a built-in self-test comparing the integer test to an independent `Fraction`-arithmetic
  reference on 7 shapes (`python3 scripts/cells.py` -> `selftest passed: True`, 0 mismatches) and
  checking every guaranteed-box member is forced at all four corners of its box.
* Every one of the 681 recorded 7-clique witnesses was re-checked through the `Fraction` path on
  the original formulas (`python3 scripts/verify_witness.py` -> `certified boxes re-verified:
  681/681; point-checks 4086; failures 0`). That is a second arithmetic path but the *same*
  mathematical derivation, so it does not remove the need for an independent re-implementation.
* Two bugs were found and fixed during the block (a
  signed-coordinate bug in `sq` that *fabricated* 7-cliques, and an off-by-`sqrt` window bound);
  both would have produced a false positive/negative, so a second implementation is required
  before this is quoted as established. The 7-clique witnesses in `out/cover.json` are the cheap
  place to start: each is a finite, directly checkable claim.

## 5. A limit on the K_7 certificate (found after the block, in a subagent's refused proposal; re-derived here)

**Lemma.** If 7 planar points have all pairwise distances in `[a,b]` then `b >= (sqrt7 - 1) a`.
*Proof.* The 7 closed disks of radius `a/2` about the points are interior-disjoint, so they have total
area `7 pi a^2/4`; they lie in the `(a/2)`-neighbourhood of the convex hull, whose area is at most
`area(hull) + perim(hull) a/2 + pi a^2/4 <= pi b^2/4 + pi b a/2 + pi a^2/4` (isodiametric inequality;
Barbier for `perim <= pi b`). Hence `6a^2 <= b^2 + 2ab`. `square`

**Consequence for this family.** A forced difference satisfies `|v| <= dmax <= |v| + D` and
`dmin >= |v| - D`, so `1 in [dmin,dmax]` gives `|v| in [1-D, 1+D]` with `D = sqrt(s^2+t^2)` the cell
diameter. A 7-clique of cells therefore needs all pairwise offsets in `[1-D,1+D]`, so
`(1+D)/(1-D) >= sqrt7 - 1`, i.e.

    D >= 1 - 2/sqrt7 = 0.24407...

So the K_7 certificate provably **cannot** decide any tiling with cell diameter below `0.2441`, and
this is a limit of the method used above, not a statement about `chi(R^2)`. It also explains why the
`i >= 26` band (diameters `>= 0.61`) is easy and the small-cell boxes are not; note the undecided
boxes extend well above `0.2441`, so anisotropy costs more than the diameter bound alone.
