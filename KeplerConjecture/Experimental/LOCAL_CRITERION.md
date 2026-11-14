# A cluster-averaged correction criterion

Role E (Experimental). Claim `K15-E001`. Status **PROVED** (criterion), with the
local lemma it exposes left **OPEN**. Independent reviewer: X.

## 0. Reconstruction of the source mechanism

Source H05U, Section 3.1, Definition 3.2 and Lemma 3.3, printed p. 34, PDF p. 46;
proof continues on printed p. 35. Verified verbatim against
`Literature/Papers/Hales2005-unabridged.pdf` page 46 in this repository.

Definitions. `Lambda` is the centre set of a *saturated* packing of unit balls, so
pairwise distances are `>= 2`. `Omega(v)` is the Voronoi cell. `A : Lambda -> R` is

- **negligible**: `sum_{v in Lambda(x,r)} A(v) <= C1 r^2` for all `x`, `r >= 1`, where
  `Lambda(x,r) = Lambda cap B(x,r)`; and
- **fcc-compatible**: `vol Omega(v) + A(v) >= sqrt(32)` for every `v in Lambda`.

Lemma 3.3 then gives `delta(x,r,Lambda) <= pi/sqrt(18) + C/r`, with `C` depending on
`Lambda` only through `C1`.

**What the mechanism actually uses.** The proof is pure accounting and contains no
geometry beyond two facts:

1. `vol B(x,r,Lambda) <= |Lambda(x,r+1)| * 4pi/3` (each ball has volume `4pi/3`);
2. Voronoi cells are disjoint and `Omega(v) subset B(v,2)` (saturation), so the cells
   of centres in `B(x,r+1)` are contained in `B(x,r+3)`.

Fcc-compatibility is used in exactly one place: to replace a *count* of centres by a
*volume*, `sqrt(32)|Lambda(x,r+1)| <= sum_{v in Lambda(x,r+1)} (vol Omega(v) + A(v))`.
Negligibility is used in the other direction, to bound that volume sum from above.
The whole geometric burden of the proof therefore sits in *producing* `A`, and the
accounting lemma is indifferent to how `A` is built.

That observation is the opening for the relaxation below.

## 1. Lemma (cluster-averaged criterion) — `K15-E001`

Let `Lambda` be saturated. Let `A : Lambda -> R` and let `Pi` be a partition of
`Lambda` into finite clusters. Suppose there are constants `D, Vmax, C1` with:

- **(C1)** `diam K <= D` for every `K in Pi`;
- **(C2)** `|K| <= Vmax` for every `K in Pi` (implied by (C1) and separation `>= 2`);
- **(C3)** `vol Omega(v) + A(v) >= 0` for every `v in Lambda`;
- **(C4)** `sum_{v in K} (vol Omega(v) + A(v)) >= sqrt(32) |K|` for every `K in Pi`;
- **(C5)** `sum_{v in Lambda(x,r)} A(v) <= C1 r^2` for all `x`, `r >= 1`.

Then there is `C = C(C1, D, Vmax)` with

```
delta(x,r,Lambda) <= pi/sqrt(18) + C/r        for all r >= 1, x in R^3.
```

**Lemma 3.3 is the special case** `Pi` = singletons (`D = 0`, `Vmax = 1`), where
(C4) becomes fcc-compatibility and (C3) is implied. So `K15-E001` is a strict
relaxation of the source criterion.

### Proof

*Step 1 — cluster accounting.* Fix `x` and `r >= 1`. Put `S = Lambda(x,r+1)` and let
`Pi_S = {K in Pi : K subset S}`, `S' = union Pi_S`. By (C4),

```
sum_{v in S'} (vol Omega(v) + A(v))
   = sum_{K in Pi_S} sum_{v in K} (vol Omega(v) + A(v))
  >= sqrt(32) sum_{K in Pi_S} |K| = sqrt(32) |S'|.
```

By (C3) the summands are nonnegative, so `sum_{v in S'} <= sum_{v in S}` and

```
sqrt(32) |S'| <= sum_{v in S} (vol Omega(v) + A(v)).                     (1)
```

*Step 2 — boundary clusters.* If `v in S \ S'`, its cluster `K(v)` is not contained in
`S`, so `K(v)` meets `Lambda \ S`. Since `v in S` and `diam K(v) <= D`, that point lies
in `B(x,r+1+D)`. Hence `K(v)` meets the shell
`T = Lambda cap (B(x,r+1+D) \ B(x,r+1))`. Because `Pi` is a partition, the fibre of any
assignment `v |-> t(v) in K(v) cap T` over a point `t in T` is contained in `K(t)`, so is
of size at most `Vmax`. Thus `|S \ S'| <= Vmax |T|`.

*Step 3 — shell bound.* Balls of radius 1 about the points of `Lambda` are disjoint and
lie in `B(y, rho+1)`, so `|Lambda cap B(y,rho)| <= (rho+1)^3`. For `rho >= 1` both
radii `r+1` and `r+1+D` exceed 1, so

```
|T| <= (r+2+D)^3 - (r+1)^3 <= 3D (r+2+D)^2 <= C' r^2     (r >= 1)
```

for a constant `C' = C'(D)`. Hence `|S| <= |S'| + Vmax C' r^2`, and with (1),

```
sqrt(32) |S| <= sum_{v in S} (vol Omega(v) + A(v)) + sqrt(32) Vmax C' r^2.   (2)
```

*Step 4 — volume bound.* The cells `Omega(v)`, `v in S`, are pairwise disjoint and each
lies in `B(v,2) subset B(x,r+3)`, so by (C5)

```
sum_{v in S} (vol Omega(v) + A(v)) <= vol B(x,r+3) + C1 (r+1)^2.            (3)
```

*Step 5 — conclude.* Combine (2), (3) and the count bound
`vol B(x,r,Lambda) <= |S| * 4pi/3`:

```
delta(x,r,Lambda) <= (4pi/3)/sqrt(32) * [vol B(x,r+3) + C1(r+1)^2 + sqrt(32)Vmax C' r^2] / vol B(x,r).
```

Since `(4pi/3)/sqrt(32) = (4pi/3)/(4 sqrt 2) = pi/(3 sqrt 2) = pi/sqrt(18)` and
`vol B(x,r+3)/vol B(x,r) = (1+3/r)^3`, while the remaining numerator is `O(r^2)`
against `vol B(x,r) = (4pi/3) r^3`,

```
delta(x,r,Lambda) <= pi/sqrt(18) (1+3/r)^3 + C''/r,
```

and absorbing `pi/sqrt(18)((1+3/r)^3 - 1) = O(1/r)` into `C''` gives the claim. `QED`

### What the relaxation buys, and what it costs

*Buys.* The corrected volume no longer has to be correct **cell by cell**; only
**cluster by cluster**. Hales pays for the pointwise version with an explicit transfer
formula: the V-cell construction (Chapter 5), its compatibility with the Q-system
(Lemma 5.28), and the four-way cancellation `sum_{i=1..4} A1(S,c,v_i) = 0` (Lemma 7.10)
that makes negligibility provable. Under (C4) no transfer formula is needed at all;
`A` may be taken simple, and the compensation that small cells receive from large
neighbours is absorbed into an average instead of being written down analytically.
This is the natural formal home for Fejes Toth averaging over cells.

*Costs.* (i) The hypothesis is now a *universal statement over cluster shapes*, which
is harder to attack than a formula. (ii) It is **not certifiable by sampling**; see the
obstruction in Section 3.

## 2. Why the pointwise condition cannot be weakened to `A = 0` — exact fixture

`K15-E002`, status **PROVED** (elementary). Take the icosahedral 13-cluster: a central
ball with 12 tangent neighbours at the vertices of a regular icosahedron of
circumradius 2. The neighbours are mutually at distance `2*(4/sqrt(10+2 sqrt5))` ~ `2.1029 > 2`,
so this is a legal local configuration. The Voronoi cell of the centre is the regular
dodecahedron of inradius 1, of volume

```
V_dodeca = (15 + 7 sqrt5)/4 * a^3,   a = 4/sqrt(10 + 22/sqrt5),
```

which evaluates to `5.5502910285155105` against `sqrt(32) = 4 sqrt 2 = 5.656854249492381`.
The deficit is `0.1065632209768701`.

Consequence: **no pointwise fcc-compatible correction can vanish identically.** Any
`A` satisfying `sqrt(32) <= vol Omega(v) + A(v)` must be nonzero, and must be nonzero
in a way that pays exactly this deficit at the icosahedral centre. This is the precise
sense in which the dodecahedral configuration is the obstruction the correction exists
to handle; it is also why the dodecahedral theorem's own bound `4pi/(3 V_dodeca)` ~
`0.7546973993` is the barrier for any single-cell argument.

Verified numerically and exactly in `Experimental/scripts/icosa_cluster_test.py`; the
computed centre-cell volume reproduces `V_dodeca` to `1e-15`.

## 3. Obstruction: cluster averages are not certifiable by truncation

`K15-E003`, status **PROVED** (elementary monotonicity). For a finite set `K` let
`vol_K Omega(v)` be the Voronoi volume of `v` computed inside `K`. If `K subset K'` then
`vol_{K'} Omega(v) <= vol_K Omega(v)` for every `v in K`, because more bisector
constraints can only shrink a cell.

Hence every finite computation of cell volumes is an **upper** bound for the volumes in
any packing containing that cluster. A numerical test can therefore only **refute** a
cluster-average lower bound, never establish it. Our runs confirm the practical form of
this: with a sparse completion of the icosahedral core the 13-cluster mean was `8.69`
and with a denser randomized completion `12.90`, both dominated by the free space
outside the cluster rather than by any property of the core. Both numbers are
uninformative upper bounds and are recorded only as evidence for the obstruction.

Consequence for the programme: `K15-E001` shifts the burden from a pointwise analytic
inequality to a cluster-level one, and the cluster-level inequality cannot be discharged
by sampling. It requires either an analytic lower bound on cell volume over a cluster
(Rogers-simplex or Fejes Toth style) or a *certified* saturation of the outer region.
This must be priced in before the criterion is promoted.

## 4. The exposed question

`K15-E004`, status **OPEN**. With `A = 0` and `Pi` the partition into clusters of
diameter at most `D`:

> Is `sum_{v in K} vol Omega(v) >= sqrt(32) |K|` for every cluster `K` of diameter at
> most `D`, in every saturated packing?

`D = infinity` is Kepler. The point of the question is the smallest `D` for which it
holds, and the icosahedral 13-cluster (Section 2) is the first test case: it violates
the pointwise version and is the natural candidate to violate the averaged version.
Note that (C1)–(C5) with `A = 0` and unbounded `D` is equivalent to the theorem, so no
claim of a shortcut is made here; the content is the reframing plus the proved
criterion plus the certification obstruction.

## 5. What the criterion actually removes, and what it does not

`K15-E001` is a **conditional accounting lemma**. It is not a bound on packing density
and it does not shorten Hales's proof by itself. The honest accounting:

**Removed.** (i) The obligation to write an explicit pointwise transfer formula. In Hales
the corrected volume must be correct cell by cell, and the machinery that achieves this —
the V-cell construction (Chapter 5), its compatibility with the Q-system (Lemma 5.28),
and the four-way cancellation `sum_i A1(S,c,v_i) = 0` (Lemma 7.10) — exists to make the
transfer explicit and to make negligibility provable. Under (C4) none of that is needed:
the compensation is absorbed into an average. (ii) The pointwise failure at the
dodecahedral configuration (`K15-E002`) stops being fatal, because the configuration is
precisely a case where a small cell has large neighbours.

**Not removed.** (i) `K15-E004` is unproved, and it is the entire geometric content.
(ii) The hypothesis (C4) is a universal statement over cluster *shapes*, which is a larger
quantifier range than a single formula. (iii) `K15-E003` shows (C4) cannot be certified by
truncated computation. So the criterion relocates the difficulty; it does not reduce it.
Any statement that it "simplifies Hales" must be qualified as *simplifies the interface
between the local analysis and the accounting*, not the local analysis itself.

### Audit points for X (boundary clusters, saturation, signs)

1. **(C1) versus the boundary count.** Step 2 needs each cluster meeting `Lambda \ S` to
   lie in `B(x, r+1+D)`, using `diam K <= D` and `v in S`. Confirm no use of cluster
   *convexity* is smuggled in — diameter suffices, but check the step as written.
2. **Saturation.** Used only for `Omega(v) subset B(v,2)`. Is saturation required, or does
   `Omega(v) subset B(v, c)` with a constant `c` suffice, giving a different final
   constant? The criterion should state the weakest form it needs.
3. **(C3) nonnegativity.** Used only to discard terms with `v in S \ S'`. Hales's own
   `vol Omega + A` is positive in his construction, but the criterion should not assume it
   silently. Is there a version that survives signed `A` with a bounded-below hypothesis?
4. **Bounded cluster size.** Listed as (C2) for clarity, but implied by (C1) and
   separation `>= 2`; confirm that the constant `Vmax` used in Step 2 is then not
   independent of `D`.
