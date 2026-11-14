# Claims for independent review — role X

Reviewer: X (`i-ve-attached-viazovska-f7hh`). Each claim is stated so it can be attacked
without reading the rest of my material. **The 27616 review is accepted in full**; the
items below are the repaired and new claims, plus the four audit points the review asked
me to raise with X.

## K15-E001 — cluster-averaged criterion (PROVED)

Let `Lambda` be saturated, `Pi` a partition into clusters with `diam <= D`, `c(v) =
vol Omega(v) + A(v)`. If `c >= 0`, `sum_{v in K} c(v) >= sqrt(32)|K|` for all `K in Pi`,
and `A` is negligible, then `delta(x,r,Lambda) <= pi/sqrt(18) + C/r`. Hales's Lemma 3.3
is the singleton case.

**This is a conditional accounting lemma, not a density bound.** Review asks to quantify
the removed burden: what is removed is the explicit transfer formula (V-cells, Lemma 5.28,
the four-way cancellation of Lemma 7.10); what is *not* removed is the geometric
hypothesis `K15-E004`. See `LOCAL_CRITERION.md` §5.

**Audit points (the review's request).**
1. Step 2 needs each cluster meeting `Lambda \ S` to lie in `B(x, r+1+D)`. Does any step
   use cluster *convexity* rather than diameter?
2. Is saturation needed beyond `Omega(v) subset B(v,2)`? State the weakest form.
3. (C3) nonnegativity is used only to drop terms with `v in S \ S'`. Does a signed
   version with `A` bounded below survive?
4. (C2) is implied by (C1) plus separation `>= 2`; confirm `Vmax` may then depend on `D`.

## K15-E002 — dodecahedral fixture (PROVED, exact)

`V_dodeca = (15+7sqrt5)/4 * (4/sqrt(10+22/sqrt5))^3 = 5.5502910285155 < sqrt(32)`.
Hence no fcc-compatible `A` vanishes identically.

**Open sub-question.** Is the icosahedral 13-cluster realisable inside a *saturated*
packing? If not, the conclusion weakens to "no `A` vanishes on clusters that occur in
saturated packings". Settle this before `K15-E002` is cited.

## K15-E003 — no certification by truncation (PROVED)

Cell volume is monotone decreasing under adding centres, so finite computations give
upper bounds and can only refute `K15-E004`. Recorded values `8.69` (sparse) and `12.90`
(randomsed, denser) are uninformative upper bounds.

## K15-E004 — the open geometric question (OPEN)

With `A = 0`: is `sum_{v in K} vol Omega(v) >= sqrt(32)|K|` for every cluster of diameter
`<= D` in every saturated packing? `D = infinity` is Kepler.

**Refutation attempts wanted:** adjacent pair; tetrahedral 4-cluster; icosahedral
13-cluster; perturbed FCC. A witness inside a saturable packing redirects the route.

## K15-E010 — cap inequality direction (PROVED; repairs K15-C013)

For `k` points on `S^2` with minimal angular separation `theta`,
`k * 2pi(1 - cos(theta/2)) <= 4pi`, hence `theta <= 2 arccos(1 - 2/k)`. For `k=13`,
`theta <= 2 arccos(11/13) = 64.40845 deg`, and `13*2pi*(1-11/13) = 4pi` exactly.

This is an **upper** bound on `theta`. C013's "only forces `theta >= 64.4 deg`" has the
direction reversed. The cap bound is vacuous because `theta_min(delta) <= 60 deg` always,
and `64.408 > 60`.

**Attack:** check the cap-area formula (a cap of angular radius `phi` has area
`2pi(1-cos phi)`), and check that `theta/2` is the right radius, not `theta`.

## K15-E011 — radius conversion (PROVED)

For centres at radii `r, s in [2, 2+delta]` with mutual distance `>= 2` and angle `theta`,
`cos theta <= (r^2+s^2-4)/(2rs) <= 1 - 2/(2+delta)^2`. Proof: the right side is maximised
at `r = s = t` where it is `1-2/t^2`, increasing in `t`. Hence
`theta >= arccos(1-2/(2+delta)^2)`, which is decreasing in `delta`, `60 deg` at
`delta = 0`.

No assumption that centres share a sphere. Confirm that using the *weakest* per-pair
constraint is legitimate as a necessary condition.

## K15-E012 — explicit thin-shell count (PROVISIONAL)

If `theta_13` is an upper bound for the minimal angular separation of 13 points on `S^2`,
then for `delta < sqrt(2/(1-cos theta_13)) - 2` at most 12 centres lie in `[2, 2+delta]`.

**PROVISIONAL because** I did not verify `theta_13 = 57.1367 deg` from a primary source.
With it, `delta_0 = 0.0911455`. With the cap bound of `K15-E010`, `delta_0 = -0.1236`, no
information.

**X's task:** pin the primary locator for Tammes `N = 13` and re-evaluate, or replace
`K15-E012` by C013(a)'s unconditional `n <= (3+delta)^3 - 1`. I do not claim a new
threshold; `delta_0` is a derived function of a classical constant.

## K15-E013 — Barlow compatibility of the 12-shell (OPEN, for C/X)

Does every Barlow stacking have at most 12 centres in `[2, 2+0.0912]`? FCC and HCP do
(12 at `|y|=2`, next shell `2 sqrt 2 = 2.8284`, so the bound holds for `delta < 0.8284`).
A stacking with an unusually short next shell would break `K15-E012`'s equality fixture.
This is the concrete finite question that must be settled before `K15-E012` is used.

## K15-E020 — local-mass row (SPECIFIED; validity PROVED, strength UNEVALUATED)

Row: `n_v(rho) <= N(rho)` for every centre, with the proved choice
`N(rho) = (rho+1)^3 - 1` from C013(a). Stated as a constraint on the *pair measure*, not
on contacts, so it survives the review's objection that a twelve-contact sum misses
distant completions.

**Attack:** confirm the measure form is linear in the SDP variables; confirm the row does
not exclude FCC/HCP (slack 14 at `rho = 2.01`, so it does not); confirm the row cannot be
sharpened to the kissing value without `K15-E012`; and confirm I have not claimed novelty
over `DLOV14` Section 5.
