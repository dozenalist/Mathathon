# The cyclic locus of the paper's seven-colouring, exactly

Member m3, direction d16 (swarm `smwfwi7rh`). Deliverable: a theorem, exact data, and a
sharpened constant, about the object `L` itself rather than about more palette systems.

**Check:** `python3 verify.py` in `.ultramath/smwfwi7rh/m3/` — 23 exact checks, exit status 0.
Supporting scripts: `step1_vertex.py`, `step2_transition.py`, `step3_annulus.py`,
`step4_circle.py`, `step5_gadget.py`, `step6_Lcheck.py`, `figure.py` (writes `figure.png`).
Every geometric quantity below lies in `Q(sqrt 3)`; `field.py` implements that field with
rational coefficients, so all comparisons are exact.

---

## 0. Results

1. **Lemma 1 (interface determination).** For a colouring that is constant on the cells of a
   partition into open connected sets with piecewise `C^1` boundaries, with every ball meeting
   finitely many cells and finitely many interface arcs, the transition graph `Gamma_x` of
   Definition 6.1 is *exactly* the graph of interface arcs through `x`. Hence
   `L` = the set of junctions at which three or more cells of pairwise distinct colours meet, and
   if the junctions are locally finite then `L` is locally finite.
   **Corollary.** `(W)` holds — `L cap B` finite for some `B` of radius `> 1` — for every such
   ("tame") colouring, at every `k`, with no palette bound, no measurability and no properness
   hypothesis. The class is not vacuous: it contains the paper's own seven-colouring and every
   polygonal-map colouring.

2. **Theorem 2 (`L` of the seven-colouring, exact).** For the paper's seven-colouring `c_0`
   (Voronoi hexagons of circumradius `2/5`, colour `(m+2n) mod 7`),
   `L(c_0) = V`, the vertex set of the hexagonal tiling, and nothing else.
   `V` is the honeycomb lattice with side `2/5`: minimum separation `2/5`, covering radius `2/5`,
   density `25/(3 sqrt3) = 4.811...` per unit area, `1`-dense. So `(W)` holds for `c_0` with every
   `R > 2/5`, with a large margin.

3. **Theorem 3 (`L` of the accumulating `k >= 7` colouring, exact).** For the colouring `c` of
   `.ultramath/smwfo9zkl/m3` (the seven-colouring altered inside a small square `W`),
   `L(c) = V  union  {q_n, z_n : n in N}  union  {p_0}`,
   where `q_n` are the Mercedes centres and `z_n = q_n - rho_n` the ray-endpoint of `D_n` at angle
   `180` degrees. Every listed point except `p_0` is isolated in `L(c)`, and `p_0` is the only
   accumulation point. So `L(c)` is **closed, countable, and not locally finite** — the failure of
   `(W)` at `k >= 7` is witnessed by a countable set with one accumulation point.

4. **Theorem 4 (sharpened constant, exact).** The shadow certificate holds with `eps = 1/70`:
   the annulus `1 +- 1/70` about `p_0 = (1/55, 18/55)` meets no hexagon of colour `0, 2, 3`, and
   meets all of `1, 4, 5, 6`. Since `ell sqrt2/2 < 1/70` for `ell = 1/50`, the gadget of Theorem 3
   works with `W` of side **`1/50` instead of `1/100`**. The exact threshold is
   `eps* = 0.01707898643...`, i.e. the largest square side is `sqrt2 eps* = 0.0241533342...`
   (exact bracket `eps*` in `(0.0170, 0.0171)`).

5. **Circle colour counts (exact).** For `c_0`, the unit circle about `p_0` meets exactly the four
   colours `{1,4,5,6}`; about a tiling vertex exactly four colours, e.g. `{2,4,5,6}`;
   about a hexagon centre all six colours `{1,...,6}`. The gadget of Theorem 3 spends exactly this
   resource: its palette values are the colours of the unit circle about the accumulation point.

6. `L(c_0)` was confirmed numerically by two independent predicates (interface crossing and
   three-colours-in-every-ball), and the previous swarm's annulus slacks are reproduced exactly
   (`0.028950` for colour 2, `0.017079` for colour 3) by a completely independent implementation.

---

## 1. Setting

`c : R^2 -> I` a colouring, `c_0` the paper's seven-colouring. For `h != 0` and a ball `B`,

    D_ij(B,h) = { q in B : (c(q), c(q+h)) in {(i,j),(j,i)} }.

**Definition 6.1 (the paper).** `ij` is an edge of `Gamma_x` iff for every ball `B` centred at `x`
of positive finite radius,

    limsup_{h -> 0, h != 0}  |D_ij(B,h)| / |h|  >  0.

`L = { x : Gamma_x contains a cycle }`.

Because the condition quantifies over *every* ball, `Gamma_x` depends only on the colouring at
*arbitrarily small* scales around `x`; that is used repeatedly below.

`c_0` in coordinates. `omega = e^{2 pi i/3}`, `r = 2/5`, `d = sqrt3 r = 2 sqrt3/5`,
`Lambda = d (Z + Z omega)`, so a lattice point is
`z(m,n) = ( sqrt3 (2m-n)/5 , 3n/5 )`, and its hexagon has colour `(m + 2n) mod 7`
(`Lambda/(2-omega)Lambda = Z/7` and `omega = 2` in that quotient). Hexagons have circumradius
`r = 2/5`, inradius `sqrt3/5`, and vertices at angles `30 + 60k` degrees, distance `r` from the
centre.

---

## 2. Lemma 1: for tame colourings `Gamma_x` is the interface graph

Call a colouring **tame** if it is constant on the cells of a partition of `R^2` into open
connected sets with piecewise `C^1` boundaries, such that

* (T1) every ball meets only finitely many cells, and
* (T2) every ball meets only finitely many interface arcs, where an **interface arc** is a maximal
  connected `C^1` curve contained in `dU cap dU'` for cells `U, U'` of different colours, along
  which both colours occur on their own sides; and any two interface arcs meet in finitely many
  points.

**Lemma 1.** Let `c` be tame. Then for every `x` and every pair `i != j`:

    ij in Gamma_x   <=>   x lies on an interface arc between a colour-i cell and a colour-j cell.

*Proof.* (<=) Let `gamma` be such an arc with `x in gamma`, and let `B` be a ball centred at `x`
of radius `s > 0`. Since `gamma` is a `C^1` curve through `x`, `gamma cap B` contains a
sub-arc of length `ell >= s/2` (for `s` small compared with the curvature radius; shrinking `B`
only helps because the condition is a limsup over all radii, and for the finitely many larger
balls the same estimate holds with `min(s, c)`). Let `n` be the unit normal to `gamma` at a point
of that sub-arc, and put `tau = |h|` with `h = tau n`. The set
`{q in B : c(q) = i, c(q+h) = j}` contains, for each sub-arc piece of length `delta`, a
parallelogram of area `>= delta tau / 2` (the strip on the `i`-side of `gamma` of width `tau/2`
that stays inside the `H`-side after translation by `h`; the boundary curvature is `C^1` so the
strip is contained in the two cells for small `tau`). Hence
`|D_ij(B,h)| >= (ell/2) |h|`, so the limsup is `>= ell/2 > 0`. As `B` and `h` were arbitrary,
`ij in Gamma_x`.

(=>) Suppose `x` lies on no interface arc between a colour-`i` and a colour-`j` cell. By (T2),
choose a ball `B` centred at `x` meeting only the interface arcs that pass through `x`, and none
of them is an `(i,j)`-arc. Then `B` contains no `(i,j)`-interface point: any point of `B` that is
a limit of `i`-points and of `j`-points lies on an `(i,j)`-interface arc in `B` (the cells are
open, so a point of `dU cap dU'` with `U` of colour `i` and `U'` of colour `j` is on such an arc,
and an accumulation point of `i`-points and `j`-points is such a point). Take `q in B` with
`c(q) = i`, `c(q+h) = j` and `|h|` so small that `[q, q+h] subset B`. Walking along the segment,
the colour changes from `i` to `j`, so some point of `[q,q+h]` lies in `dA_i cap dA_j cap B`, which
does not exist. Hence `D_ij(B,h)` is empty for all small `h`, the limsup is `0`, and
`ij notin Gamma_x`. QED

**Corollary 1.** If `c` is tame, then `Gamma_x` is the graph on the colours of the cells whose
closures contain `x`, with `i -- j` iff `i != j` and an interface arc through `x` separates an
`i`-cell from a `j`-cell. Consequently `L` is contained in the set of junctions (points where at
least three cells meet), and if there are finitely many junctions in every ball then `L` is closed
and locally finite; in particular `(W)` holds.

*Proof.* `L` consists of points where `Gamma_x` has a cycle; a cycle needs at least three
vertices and three edges, i.e. three cells pairwise joined by interface arcs through `x`; such an
`x` is a common limit point of three cells, i.e. a junction. Since every ball meets finitely many
cells and interface arcs, and pairs of arcs meet finitely often, the junctions in a ball are
finitely many. QED (Closedness of `L` is the paper's argument, valid for any colouring.)

**What the corollary does and does not say.** It is a proof of `(W)` in a class that contains
every polygonal-map or tiling colouring, in particular the paper's seven-colouring — and it uses
no palette bound, no measurability, no properness and no bound on `k`. It says nothing about
non-tame colourings; Theorem 3 below shows the tameness hypothesis cannot be dropped, and shows
what dropping it costs: a colouring whose cyclic locus is closed, countable, and accumulating at
one point.

---

## 3. Theorem 2: the cyclic locus of the seven-colouring is the honeycomb lattice

**Theorem 2.** `L(c_0) = V`, the set of vertices of the hexagonal tiling.

*Proof.* Every point of the plane is (i) in the interior of a hexagon, (ii) in the relative
interior of an edge, or (iii) a vertex. `c_0` is tame (six-hexagon stars: every ball meets
finitely many cells and edges), so Lemma 1 applies.

(i) At a cell-interior point `x`: no interface arc passes through `x`, so `Gamma_x` has no edge;
not cyclic.

(ii) At an edge-interior point `x`: the only interface arc through `x` is the edge itself,
separating the two hexagons; `Gamma_x` is a single edge; not cyclic.

(iii) At a vertex `x`: exactly three hexagons `H_0, H_1, H_2` meet at `x`, pairwise along the three
edges ending at `x`. So `Gamma_x` is the complete graph on `{c_0(H_0), c_0(H_1), c_0(H_2)}` by
Lemma 1, and it is cyclic **iff those three colours are distinct**. They always are:

*Fact.* The six unit vectors of `Z + Z omega` are `(1,0), (0,1), (-1,0), (0,-1), (1,1), (-1,-1)`
and their colours are `1, 2, 6, 5, 3, 4` — exactly the six nonzero residues mod 7.
A vertex is the circumcentre of an elementary triangle `{z, z + d u, z + d (u+v)}` with
`u, v, u+v` unit vectors, so its three colours are `c, c + colour(u), c + colour(u) + colour(v)`
with `colour(v) != 0 mod 7`; hence `colour(u) != colour(u) + colour(v)`, and the three are
distinct. QED

**Exact data.** `V` is the honeycomb lattice with side `r = 2/5`:
minimum distance `r = 2/5` (exact check `V6b`), covering radius `r` attained at the hexagon centres
(exact, `V6c`), density `2/(covolume Lambda) = 2/(6 sqrt3/25) = 25/(3 sqrt3) = 4.811...` per unit
area, `1`-dense with a large margin (the paper's Theorem B needs covering radius `<= 1`).

**Consequence.** `(W)` holds for `c_0` for every `R > 2/5`, so the seven-colouring is far from the
extremal behaviour of `(W)`; the altered colouring of Theorem 3 destroys it in one point.

---

## 4. Theorem 3: what the accumulating colouring does to `L`

Recall the construction (`.ultramath/smwfo9zkl/m3/proof.md`): `w = e^{2 pi i/3}`, `r = 2/5`,
`d = sqrt3 r`, `Lambda = d(Z + Zw)`, `c_0` as above;
`p_0 = (1/55, 18/55)`, `ell = 1/100`, `W = p_0 + [-ell/2, ell/2]^2`;
`q_n = p_0 + (ell 2^{-n-3}, 0)`, `rho_n = ell 2^{-n-14}`, `D_n = B(q_n, rho_n)`; on `D_n` the
Mercedes partition with label `0` on directions `(-60,60)`, label `2` on `(60,180)`, label `3` on
`(180,300)` degrees; label `0` on `W` minus the disks; `c = c_0` outside `W`.

**Theorem 3.** `L(c) = V  union  {q_n : n in N}  union  {z_n : n in N}  union  {p_0}`, where
`z_n = q_n - rho_n` is the point of `dD_n` at angle `180` degrees. All points except `p_0` are
isolated in `L(c)`; `p_0` is the unique accumulation point; `L(c)` is closed and countable.

*Proof.* `W` lies in the interior of the hexagon of the origin (`V3b`), so outside `W` the
colouring is `c_0` and, across `dW`, the colour is `0` on both sides: no interface lies on `dW`.
For `x != p_0` there is a ball about `x` not meeting any `D_n` except possibly finitely many, so
`c` is tame near `x` and Lemma 1 (local form) computes `Gamma_x` from the interfaces through `x`:

* `x` outside `W`: unchanged, `Gamma_x` = the interface graph of `c_0` near `x`; cyclic iff
  `x in V` (Theorem 2).
* `x` in `W`, on no interface, in the interior of a sector or on an arc of some `dD_n`: at most
  one colour pair occurs near `x`, so `Gamma_x` has at most one edge; not cyclic.
* `x = q_n`: the three sector rays meet at `q_n` with pairs `{0,2}, {2,3}, {3,0}`, so
  `Gamma_{q_n} supseteq K_3`; cyclic. (Numerically confirmed, `step5_gadget.py`.)
* `x = z_n` (angle `180` of `dD_n`): the ray at `180` degrees carries `{2,3}`, the arc below it
  `{2,0}`, the arc above it `{3,0}`, so again `Gamma_{z_n} supseteq K_3`; cyclic. (Same script.)
* `x` = the points of `dD_n` at angles `60` and `300` degrees: only the pair `{0,2}` resp.
  `{0,3}` occurs (the sector on one side of the ray has label `0`, equal to the background), so
  `Gamma_x` is a single edge; not cyclic.
* `x = p_0`: for every ball `B` about `p_0` some disk `D_n subset B`, and by the sector lemma
  `|D_ij(B,h)| >= (min(rho_n,s)/8)|h|` for each of the three pairs; so `{0,2},{2,3},{3,0}` are all
  in `Gamma_{p_0}`; cyclic.

`V` is discrete and meets `W` in no point (vertices lie on cell boundaries, `V3c`); the sequences
`q_n, z_n` are distinct and tend to `p_0`; hence `L(c)` is as claimed. QED

**Corollary 3.** `(W)` fails for `c`: every ball about `p_0` contains infinitely many points of
`L(c)`. Moreover the failure is *countable*: `L(c)` is closed, countable, and has exactly one
accumulation point. So no argument proving `(W)` can rely on `L` being uncountable, of positive
measure, or of positive content: a countable closed `L` already violates `(W)`. The only available
route is local finiteness itself.

---

## 5. Theorem 4: the shadow certificate, and a sharpened constant

The gadget needs: `p in W`, `q notin W`, `|p-q| = 1` implies `c_0(q)` is not one of `0, 2, 3`.
Since `|p - p_0| <= ell sqrt2/2` for `p in W`,

    shadow(W) = { q : exists p in W, |p-q| = 1 }  subset  { q : 1 - ell sqrt2/2 <= |q-p_0| <= 1 + ell sqrt2/2 },

so it suffices that the annulus `1 +- eps` about `p_0` meets no hexagon of colour `0, 2, 3`, with
`eps = ell sqrt2 / 2`.

**Theorem 4.** For the seven-colouring, the annulus `A(eps) = {q : 1-eps <= |q-p_0| <= 1+eps}` with
`eps = 1/70` meets no hexagon of colour `0`, `2` or `3`, and it meets hexagons of colours `1, 4, 5`
and `6`. Consequently the construction of Theorem 3 is proper with `W` of side `ell = 1/50`
(`ell sqrt2/2 = 0.014142 < 1/70 = 0.014285`).

*Proof (certificate).* A convex set meets the closed annulus iff
`d_min <= 1+eps` and `d_max >= 1-eps`, where `d_min`, `d_max` are the least and greatest distance
from `p_0` to the set. For each hexagon `H` of colour `0, 2, 3` whose centre is within distance
`3/2` of `p_0` (a superset of everything that can meet `A(eps)`), `verify.py` decides exactly

    d_min(H)^2 > (1+eps)^2     (H beyond the outer circle)  or
    d_max(H)^2 < (1-eps)^2     (H inside the inner circle),

with `(1 +- eps)^2` rational and `d_min(H)^2, d_max(H)^2` in `Q(sqrt3)`: no square roots are
taken and no rounding occurs. A second, logically independent method reaches the same conclusion
from vertex data and the six supporting faces of each hexagon (a vertex test for the inner disk,
and a separating supporting line at distance `> 1+eps` for the outer one). Both methods agree for
`eps = 1/70` and for the previous `eps = 71/10000`; the annulus is non-vacuous, since colours
`1, 4, 5, 6` do meet it (`V2b`, `V2c`, `V2d`). QED

**Exact threshold.** Bisection with the same exact predicate gives

    eps* = 0.017078986431...,      maximal square side  sqrt2 eps* = 0.024153334242...,

with the exact bracket `0.0170 <= eps* <= 0.0171` (`V5a`-`V5d`). The previous constant
`ell = 1/100` is therefore not tight; `ell = 1/50` is certified, and so is any `ell <= 0.024`.

**Independent reproduction of the previous certificate.** `step3_annulus.py` recomputes the slacks
independently and gets `0.028950` for colour `2`, `0.017079` for colour `3`, and "no colour-`0`
hexagon near the annulus at all" — the numbers of `.ultramath/smwfo9zkl/m3/proof.md` §3.3 exactly.
The colours meeting the annulus are `{1,4,5,6}` in both implementations.

---

## 6. The resource the gadget spends, counted exactly

For `c_0`, the set of colours met by the circle of radius `1` about a point is a colour count we can
compute exactly (a hexagon meets the circle iff `d_min <= 1 <= d_max`, exact in `Q(sqrt3)`):

| centre | colours on the unit circle |
|---|---|
| `p_0 = (1/55, 18/55)` | `{1,4,5,6}` (four) |
| a tiling vertex | four colours, e.g. `{2,4,5,6}` |
| a hexagon centre `z(0,0)` | `{1,2,3,4,5,6}` (six) |

Two independent exact methods agree on all three (`V4`). The first row is the gadget's mechanism in
one line: the unit circle about `p_0` misses exactly three colours — the three used on the Mercedes
disks — and this is why three labels can be spent on the disks while the annulus still colours
properly with the other four. The count `4 = k - 3` at `k = 7` is exactly the budget of the
construction.

---

## 7. What this says about `k = 6` (the boundary, stated exactly)

1. **`(W)` cannot be proved by a tameness argument at `k = 6`.** Corollary 1 proves `(W)` for every
   tame colouring at every `k`; a `k = 6` countermodel therefore *must* be non-tame: some ball must
   meet infinitely many cells or infinitely many interface arcs. Theorem 3 exhibits exactly such a
   colouring at `k >= 7`, with the accumulation at one point `p_0`.
2. **Countability, null measure and zero content of `L` do not imply `(W)`.** At `k >= 7` the
   failing locus is closed, *countable*, and has a single accumulation point (Theorem 3). So `(W)`
   cannot be deduced from any property of `L` that a countable closed set already has; a proof of
   `(W)` must establish finiteness of `L` in a ball directly.
3. **The gadget's geometric requirement at `k = 6` is a unit circle with at most three colours.**
   The shadow of `W` contains the unit circle about `p_0`. At `k = 7` the paper's own colouring gives
   a point whose circle meets exactly `4 = k-3` colours (Section 6), and the three labels outside
   that count go on the Mercedes disks. To run the same mechanism at `k = 6` one needs a proper
   `6`-colouring and a point whose unit circle (indeed a whole thin annulus around it) meets at most
   `3` colours; the count at `p_0` is `4`, so the seven-colouring is exactly at the boundary and
   cannot be reused.
4. **The exact locus data is available for calibration of any such attempt**: `L(c_0) = V` is a
   Delone set (separation and covering radius `2/5`, density `25/(3 sqrt3)`), while `L(c)` adds two
   isolated points per disk and one accumulation point. Any candidate `k = 6` construction will have
   to produce an `L` that is not a Delone set; comparing with `V` says precisely what is being asked.

---

## 8. Verification

`python3 verify.py` (exact `Q(sqrt3)` arithmetic; 23 checks, all pass):

* `V1` the six unit vectors carry the six nonzero colours; every elementary triangle has three
  distinct colours (exhaustive over 169 centres x 12 orientations, plus the algebraic argument);
* `V2` the shadow certificate by two independent exact methods, for `eps = 1/70` and
  `eps = 71/10000`; non-vacuity (colours `1,4,5,6` do meet the annulus);
* `V3` `W` of side `1/50` lies in the open colour-`0` hexagon (corners against the six faces);
* `V4` exact circle colour counts, two methods, at `p_0`, a vertex, and a hexagon centre;
* `V5` the exact bracket for `eps*`;
* `V6` Delone constants of `V`: separation and covering radius `2/5`.

Independent numerical checks (not certificates, reported as such):
`step2_transition.py` (transition ratios `|D|/|h| ~ delta` at a vertex for the three pairs, at an
edge midpoint for exactly one pair, zero in a cell interior); `step5_gadget.py` (the three pairs at
`q_0` and at `z_0`, none at a generic point of `W`, the hexagon-vertex triangle); `step6_Lcheck.py`
("ball of radius `delta` meets `>=3` colours" coincides with "`dist(x,V) < delta`" at four scales,
away from the boundary band).

## 9. Not claimed

* Nothing here decides `(W)` at `k = 6`; Section 7 states only what a countermodel must look like.
* Lemma 1 is a sufficient condition, not a characterisation: non-tame colourings can still have
  locally finite `L` (the paper's `k = 5` theorem says every five-colouring does), so tameness is
  *necessary* for the known counterexample but certainly not sufficient for failure.
* Theorem 3 is an exact description of `L(c)` for the specific colouring `c` of
  `.ultramath/smwfo9zkl/m3`; a different alteration of the seven-colouring would give a different
  `L` (though the same mechanism).
* The circle colour counts in Section 6 are computed at three specific points; the minimum over the
  plane for `c_0` is `4` in all samplings (`step4_circle.py`, 700 centres), but no exact lower bound
  over the whole plane is proved here.
* The figure `figure.png` is illustrative; radii of the disks are not to scale.
