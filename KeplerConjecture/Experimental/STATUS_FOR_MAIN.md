# Status summary for Main — role E, 2026-11-14 full-hour block

> **Superseded in part.** This page describes the `K15-REVIEW-0138-E` block. For the current
> block see `REVIEW_0308.md` (authoritative) and `CLAIM_LEDGER.md`. The two headline changes:
> `(Q)` is settled **YES** (`K15-E070`), and `(P')` survives at the icosahedral pair with
> margin `+0.134590` rather than `+0.500` (`K15-E077`/`E078`, `REVIEW_0308.md` §18).

One page. Branch `kepler15/experimental/run-01`, latest `1be2c51` (then any later commit in
the final report). Everything below is under `KeplerConjecture/Experimental/`.

## Proved

| id | statement | why it matters |
| --- | --- | --- |
| `K15-E001` | cluster-averaged correction criterion implies `delta <= pi/sqrt18 + C/r`; Hales Lemma 3.3 is the singleton case | **conditional accounting lemma only** — removes the need for an explicit transfer formula, does not reduce the geometry |
| `K15-E002` | dodecahedron of inradius 1 has volume `5.5502910285155 < sqrt32` | no fcc-compatible `A` vanishes identically |
| `K15-E003` | cell volume monotone under adding centres; a bounded cell with a complete 4-neighbourhood is certified exactly | correct form of the certification obstruction |
| `K15-E010` | cap bound is `theta <= 2 arccos(1 - 2/k)` (upper bound) | repairs the reversed direction in C013 |
| `K15-E011` | `max(f) = max(1 - 2/R^2, R/4)`; equal-radius formula valid exactly for `0 <= delta <= sqrt5 - 1` | repairs the wide-shell error |
| `K15-E012`/`E015` | `delta_13 < 57.138726938 deg` by rational interval arithmetic; margins `+4.94e-04` at `rho=2.09`, `+1.85e-02` at `2.05`, kissing number at `rho=2` | the enclosure itself |
| `K15-E013` | every Barlow stacking has exactly 12 centres in `[2,2.09]` | equality family preserved |
| `K15-E014` | at most 12 centres in `[2,2.09]`, and in `[2,2.05]` | the thin-shell count |
| `K15-E032` | `R2'` partition with adjacency threshold `4.18`: disjoint, covers, `diam <= diam(C) + 4.18` | the block rule is well posed |
| `K15-E041` | `12 V_dodeca = 66.6035` against `67.9888` required, shortfall `2.04 %` | kills per-cell-independent arguments |
| `K15-E045a` | `Omega(c) subset D` for the icosahedral centre in **any** 2-separated superset | **unconditional**, elementary; this is what `(Q)` uses |
| `K15-E048` | for estimators in the family F (uniform floor, single-radius count): `tau <= 1.045` everywhere, so the bound is `<= 4.780105486` | ceiling for **family F only**; not a closure of per-cell methods |
| `K15-E042` | the computed angular bound is `4.734076`, within `1 %` of that ceiling | the optimisation was exhaustive |
| `K15-E049` | the count-12 radius is capped at `2.091145548` by Tammes-13, so the ceiling is `4.787969853`, i.e. `15.49 %` short | **NARROWED**: a ceiling for the uniform-floor directional estimator family (F1-F3) only, not a closure of per-cell methods |
| `K15-E045b` | `vol Omega(c) = V_dodeca` | **CONDITIONAL** on the imported dodecahedral theorem (`<=` is `E045a` + `vol D`; `>=` is McLaughlin) |

## Obstructed / withdrawn

- `K15-E040` icosahedral compensation: not decidable from certified data.
- `K15-E030`/`K15-E031` block rule R1: **withdrawn**, precise arithmetic failure (singleton
  block gives `5.5503 >= 5.6569`, false).
- `K15-E046` perturbation heuristic: **withdrawn**, non-additive.
- `K15-E047` the angular technique is *weaker* than quoting the dodecahedral theorem.
- `K15-E043` my earlier "implausible" reading of `(T')`: **withdrawn**. Note: the reason I gave
  ("`(T')` has `44 %` slack") is **itself withdrawn** (`K15-E062`) — those figures came from the
  broken buffer flag. `(T')`/`(H_R)` currently have **no numerical evidence either way**.
  in every completion examined (`98.007` against `67.989`), so it is plausibly *true*.
- `K15-E3` pure Delaunay: obstructed by a source-documented configuration.
- `K15-E020` local-mass row: **blocked**, no three-point evaluator exists in these artifacts.

## The single next missing inequality

Either

1. **a sharper count**: fewer than twelve centres in `[2, 2.09]` around an outer centre, i.e. a
   spherical-code statement at radius `2.09` with one neighbour fixed at distance `2`; or
2. **a collective block inequality** over two shells, `(T'-2) S2(C) >= D(C)`, with no per-cell
   bound at all.

`K15-E048`/`K15-E049` show that **(1) is impossible for the uniform-floor directional
estimator family**: the count `12` cannot hold beyond `2 + delta_0 = 2.091145548`, so the floor
is at most `1.045573` and such bounds are at most `4.787970` against `5.665734` required.

**That is a ceiling for one family, not a closure of the route.** Still open: multi-radius
counts (allowing `N(rho)` centres in `[2,rho]` for `rho > 2.09`, which raises the floor at the
cost of more caps), convexity-based per-cell bounds that do not integrate a directional
envelope, and every collective argument. `(T'-R2')` and `(H_R)` remain unproved, and Section 5
of `REVIEW_0138.md` retracts the numerical slack I previously offered for them.

**Sharpest remaining question: `(Q)`** — does a *saturated* packing contain a cell below
`sqrt32`? `(Q) = no` would give the bound immediately via the per-cell inequality, but it also
implies Kepler, so it is strictly stronger than the target and must not be adopted as a
strategy.

## Requests outstanding

- `LOCAL_ICOSA_SEARCH.md` (`K15-EXP-003`): **BLOCKED on authoring** — `icosa_dense_optimize.py`
  does not exist. Not runnable as filed.
- `LOCAL_LEAN_REQUEST.md` (`K15-EXP-004`): `R2'` partition lemma, `PROPOSED`, awaiting X to
  freeze the statement.
- `REVIEW_CHECKLIST_X.md`: 21 items covering the source locator, root identification, rational
  `pi`/trigonometric bounds and every interval direction assumption.

## Reviewer asks

X: the checklist items, especially (C) the interval direction assumptions and (A4) the
uniqueness argument. Main: decide whether to pursue (1) or (2) above, and note that the
geometric route is retained but is **not** presently a route to a bound.
