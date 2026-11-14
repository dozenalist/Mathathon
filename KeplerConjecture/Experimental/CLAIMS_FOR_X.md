# Claims for independent review — role X

Each claim is stated so it can be attacked without reading the rest of my material.
Reviewer: X (`i-ve-attached-viazovska-f7hh`). Do not accept a claim because a computation
agrees; state which hypothesis fails if one does.

## K15-E001 — cluster-averaged criterion (status PROVED, argument in LOCAL_CRITERION.md §1)

Claim: let `Lambda` be saturated with separation `>= 2`; let `Pi` be a partition of
`Lambda` into finite clusters with `diam <= D` and `|K| <= Vmax`; let
`c(v) = vol Omega(v) + A(v)`. If `c(v) >= 0` for all `v`, `sum_{v in K} c(v) >=
sqrt(32)|K|` for all `K in Pi`, and `sum_{v in Lambda(x,r)} A(v) <= C1 r^2`, then
`delta(x,r,Lambda) <= pi/sqrt(18) + C/r` with `C` depending only on `C1, D, Vmax`.

**Attack points I want checked.**
1. Step 2's fibre bound: each `t in T` lies in exactly one cluster `K(t)`, and the
   preimage of `t` under `v |-> t(v)` is contained in `K(t)`. Is the partition hypothesis
   used correctly, or does it silently require `Pi` to be a *cover* with bounded
   multiplicity?
2. Step 3 uses `|Lambda cap B(y,rho)| <= (rho+1)^3`. Is that valid for all `rho >= 1` for
   a separation-`>= 2` set, and is the annulus estimate `(r+2+D)^3 - (r+1)^3 = O(r^2)`
   uniform in `r >= 1`?
3. The degenerate case `r = 1` and `D` large relative to `r`: does the constant `C`
   remain independent of `r`? My absorption step assumes `(1+3/r)^3 - 1 = O(1/r)`, fine,
   but the `C' r^2` term is compared against `vol B(x,r) ~ r^3` only for `r >= 1`, so the
   constant may blow up as `D -> infinity`. Confirm that `C` is allowed to depend on `D`
   but not on `r` or `x`.
4. Does `A` need to be measurable, bounded, or bounded below? (C3) is used for
   nonnegativity only.

## K15-E002 — dodecahedral fixture (status PROVED, exact)

Claim: the regular dodecahedron of inradius 1 has volume
`(15+7sqrt5)/4 * (4/sqrt(10+22/sqrt5))^3 = 5.5502910285155... < sqrt(32)`.
Consequence: no fcc-compatible `A` can be identically zero.

**Attack.** Is the icosahedral 13-cluster actually realisable as a subconfiguration of a
*saturated* packing? If not, the fixture is only a lower bound on cell volume over
non-saturable clusters and the conclusion "`A` cannot vanish" weakens to "`A` cannot
vanish on clusters that occur in saturated packings". Please settle the realisation
question explicitly, including whether the 12 outer centres (mutual distance
`~2.1029`) can be completed.

## K15-E003 — no numerical certification of cluster averages (status PROVED)

Claim: for `K subset K'`, `vol_{K'} Omega(v) <= vol_K Omega(v)`; hence finite
computations bound cell volumes from above and can only refute a cluster-average lower
bound. Our recorded values `8.69` (sparse completion) and `12.90` (denser randomised
completion) are upper bounds and must not be quoted as evidence for `K15-E004`.

**Attack.** Is monotonicity correct for *unbounded* cells, i.e. when `K` is not
saturating and `Omega_K(v)` is unbounded? My statement needs `vol_K Omega(v)` defined as
an extended value; if some cells are unbounded the comparison still holds but the
numbers are infinite, which only strengthens the point. Confirm the formulation.

## K15-E004 — the open question (status OPEN)

Claim: with `A = 0`, is `sum_{v in K} vol Omega(v) >= sqrt(32)|K|` for every cluster of
diameter `<= D` in every saturated packing? `D = infinity` is Kepler.

**Attack.** Try to refute at small `D`: two adjacent centres; the tetrahedral 4-cluster;
the icosahedral 13-cluster; a perturbed FCC with one centre displaced. If any cluster in
a saturable packing has average below `sqrt(32)`, the route needs a nonzero `A` and I want
the witness.

## K15-E2 — local-mass rows (status SPECIFIED, unevaluated)

Claim to audit: the rows `mu(B(0,rho)) <= N(rho)` are valid for *every* packing, hence
outside Li's obstruction, and `N(2) = 12` is tight on FCC, HCP and all Barlow stackings.

**Attack.** Confirm that `N(rho)` is a property of the packing class and not of a lattice;
confirm the kissing number is the correct value at `rho = 2` and not `13` at `rho = 2+eps`
in a way that would exclude the equality family. If an added row excludes HCP, the
candidate is dead by the equality-fixture test.

## K15-E3 — Delaunay obstruction (status OBSTRUCTED)

Claim: pure Delaunay per-simplex bounds fail at `(2,2,2,2,l,l)`, `l = sqrt(2(3+sqrt6))`,
density `~0.78469`. We reproduce `0.78317` by Monte Carlo (s.e. `~0.001`), consistent
but not resolved to five digits.

**Attack.** Verify the source locator (Hales unabridged Section 2.1) and whether the
simplex really occurs in a *saturated* packing; confirm that `l` is the value at which the
density crosses `delta_oct ~ 0.7209` (source says `x_0 ~ 2.504`). If the simplex cannot
occur, the obstruction is weaker than I state.
