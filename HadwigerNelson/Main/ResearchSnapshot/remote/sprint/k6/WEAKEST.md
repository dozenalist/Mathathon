# The weakest hypothesis on the cyclic locus that §7 consumes

**Result.** The printed proof of Proposition 7.1 uses local finiteness of
`L = {x : Gamma_x contains a cycle}` twice: to choose a square `Q` with `partial Q cap L = empty`,
and to have `L cap Q'` finite so that the core disks can be taken with total radius `-> 0` and
one disk per point. The second use is only through the existence of **one** point of `L` that is
isolated from the rest *inside a small ball*. Precisely:

**Theorem (conditional §7, weakest form).** Let `c` be a weak measurable 6-colouring of the plane
and suppose

  **(ISO)** there exist `x_0 in L` and `r > sqrt 2` such that `L cap B(x_0,r) = {x_0}`.

Then the conclusion of Proposition 7.1 at `k = 6` holds: there are `ell in {3,4,5,6}`, distinct
labels, a centre `x`, a radius `rho`, and a cycle of compact connected exclusion continua with
all the properties listed in `TRANSFER.md`.

*Proof.* Choose a closed square `Q` centred at `x_0` with side `s`, where `2 < s <= r sqrt 2`, so
`Q subset B(x_0,r)` — a square of side `s` has circumradius `s/sqrt 2`, so the inclusion is
`s <= r sqrt 2`, and the demand `s > 2` is then satisfiable exactly when `r > sqrt 2`. (Corrected:
an earlier version of this line displayed `4 < s < r/sqrt 2`, which is arithmetically
inconsistent with its own conclusion — the direction of the `sqrt 2` is wrong, and the display
has no solution for any `r <= 4 sqrt 2`. See `smwg1r9lg/m3` errata E5.)
Then `partial Q cap L = empty` and `L cap Q = {x_0}`. Take `Q' = Q` (or any
slightly larger square still inside `B(x_0,r)`). Lemma 7.4 applies with `L_0 = {x_0}`; Lemma 7.6
produces the non-null core loop; the proof of Prop 7.1 then chooses `rho > 0` with
`B(x_0,rho) cap L_0 = {x_0}` — which holds for every `rho < r`. The rest is verbatim. (The cover
obstruction used here must be the sharpened one, inradius `>` mesh — `smwg1r9lg/m3` Lemma C,
independently `m5` — not the printed side-ten/mesh-two Lemma 7.5; see the note on trust grades in
`REPORT.md` §2.)

**Why the cover lemma still applies on a smaller square.** Lemma 7.5's proof uses the open
central region `{y in Q : dist(y, partial Q) > 2}` and Brouwer's theorem on a disk of radius two.
The region is nonempty exactly when the side of `Q` exceeds `2m`; with the component-cover
bound `m = 1 + o(1)` this is `s > 2`. (With the paper's rounded constants `s = 10, m = 2` it is
`s > 4`.) The value `10` in the paper is a convenient large constant, not a threshold. So an
isolated cyclic centre whose isolation radius exceeds `sqrt 2` is legitimate; an isolation
radius below `1` is not enough for the printed argument. The clean weakest form is the ball
version of m12: `L cap B(y,R)` finite for some `R > 1`.

**Sharpness: perfect `L` breaks the printed proof.** Suppose `L` is perfect (closed, no isolated
points) and nonempty. Then for every `x in L` and every `rho > 0`, `B(x,rho) cap L` contains a
point `x' != x`. In the proof of Prop 7.1, after choosing `x` and `rho`, the ball `B(x,rho)`
contains another point of `L_0`, hence another core disk `B_{n,x'}`. That disk is a hole of the
domain of `g_n` and lies inside the annulus `A_n = B(x,rho) \ B_{n,x}`, so `g_n` is not defined on
all of `A_n` and Lemma 7.8 (which needs a continuous map on the whole annulus) does not apply.
No choice of the subsequence repairs this: every point of `L` is an accumulation point of `L`,
so the annulus always contains further core disks. The printed extraction genuinely needs an
isolated point.

**Consequences for the sprint.**

* `(LF)` (local finiteness) implies `(ISO)`, but `(ISO)` is strictly weaker: the disjoint union of
  one isolated point and a Cantor set in `L` satisfies `(ISO)` and not `(LF)`.
* `(ISO)` is not a consequence of nonemptiness: `L` is nonempty and `5 sqrt 2`-dense at every `k`
  (`TRANSFER.md`, corollary), and a dense set can be perfect.
* Neither is it a consequence of any cardinality or closedness property of `L`: an abstract lattice
  is closed, countable and `1`-dense, and violates `(W)`. But **no colouring's `L` is known to
  violate `(W)` at any `k`**: for the proper measurable `k >= 7` colouring of `m3` (`smwfwi7rh`,
  accepted) `L` is closed and countable with exactly one accumulation point, and it **satisfies**
  `(W)` — a ball of radius `3/2` centred more than `2` from the accumulation point meets only the
  base lattice (`smwfycxze` m1, Prop. 7). So the `k >= 7` example does not show that `(W)` fails at
  `k >= 7`; a proof of `(ISO)` must exhibit an isolated point directly.
* It *is* automatic in the tame class: for a colouring constant on a locally finite partition with
  piecewise `C^1` boundaries, `Gamma_x` is exactly the interface graph (`m3` Lemma 1, accepted), so
  `(W)` holds at every `k`. Hence the colourings in question are exactly the non-tame ones, i.e.
  some ball must meet infinitely many cells or infinitely many interface arcs.
* Thus the exact missing input is **not** "`L` is locally finite" but the weaker
  **"`L` has an isolated point"**. Every member's proof of local finiteness at `k = 6` is
  therefore more than enough; a proof of `(ISO)` would already make §7 available.

**The covering/content weakening is refuted (`m5`, `smwfwi7rh`).** One might hope that
finiteness of `L` can be replaced by a size bound — zero upper 1-dimensional Minkowski content,
zero Hausdorff measure, porosity, `1`-density — since the disk-removal stage of Lemma 7.4 does
run under a covering bound (`m5`, Theorem 1). It cannot. `m5` proves (i) at a non-isolated
cyclic centre every annulus contains another core disk (Theorem 3), and (ii) the crossing lemma
(Lemma 7.8) is **false on a punctured annulus**: an explicit continuous graph-valued map on
`{1 <= |z| <= 3} \ B(2,1/4)` has non-null inner boundary word but its midpoint preimage joins
the inner boundary to the hole and never reaches the outer boundary (Theorem 3', exact
certificate). Hence a hole inside the annulus genuinely kills the annihilation step: the loop's
winding has a hole contribution that cancels it. There is also a closed **perfect**, `1`-dense,
porous set with zero upper 1-dimensional Minkowski content on every compact (Theorem 4), so no
size condition at all can imply an isolated point. The exact input is therefore
**isolation at radius `> 1`**, not any covering-content bound.

**What a counterexample has to do.** To kill the interface route it is enough to exhibit a weak
measurable 6-colouring whose cyclic locus is perfect (or merely has no isolated points). That is
still a 6-colouring, hence out of reach unconditionally; but it sharpens the target: a
palette-level model with a perfect cyclic locus kills the route for its constraint class, even if
it cannot be realised by a colouring.
