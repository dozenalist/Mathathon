# Experimental (role E)

Purpose: reconstruct the Hales local correction mechanism, and propose bounded
mechanisms that could remove real proof work. Owner: SAIR session
`i-ve-attached-thomas-4iws`. Reviewer: X (`i-ve-attached-viazovska-f7hh`).
Evaluator: C (`using-the-chats-in-mcl6`).

| File | Content | Status |
| --- | --- | --- |
| `LOCAL_CRITERION.md` | verbatim reconstruction of H05U Def 3.2 / Lemma 3.3; new cluster-averaged criterion with full proof; dodecahedral fixture; non-certifiability obstruction; the exposed open question | `K15-E001` PROVED, `K15-E002` PROVED, `K15-E003` PROVED, `K15-E004` OPEN |
| `CANDIDATES.md` | three candidate mechanisms, one per assigned route, each with object, theorem, normalisation, equality fixtures, evaluator, hardest lemma and counterexample test | E1 PROVED criterion / E2 SPECIFIED / E3 OBSTRUCTED |
| `CLAIMS_FOR_X.md` | precise attack list for the reviewer | review requested |
| `COMPUTE_REQUEST_K15-EXP-001.md` | two local jobs for Astra | REQUESTED |
| `scripts/icosa_cluster_test.py` | exact dodecahedron volume and icosahedral cluster cell volumes | reproduced to 1e-15 |
| `scripts/local_density_fixtures.py` | Monte Carlo of `delta_tet`, `delta_oct`, Hales extremal simplex | TESTED_FINITE |
| `SHELL_CONVERSION.md` | cap-inequality direction repaired; exact radius conversion for centres in `[2,2+delta]`; explicit 12-shell bound; equality fixtures | `K15-E010` PROVED, `K15-E011` PROVED, `K15-E012` PROVISIONAL, `K15-E013` OPEN |
| `ANALYTIC_LOCAL_MASS.md` | local-mass row outside ordinary CE, in measure form; proved `N(rho)`; sized evaluator for C | `K15-E020` SPECIFIED |
| `scripts/shell_conversion.py` | exact cap identity, conversion, delta table | exact, <1 s |
| `scripts/local_mass_search.py` | exploratory search for `N(rho)` | TESTED_FINITE, inadequate |
| `TAMMES13_ENCLOSURE.md` | frozen enclosure of `delta_13`; Taylor lemma; Barlow `K15-E013` closed | `K15-E013`/`E015` PROVED |
| `GEOMETRIC_OBSTRUCTION.md` | quantified obstruction to the icosahedral compensation | `K15-E040`/`E041`/`E042` |
| `REVIEW_CHECKLIST_X.md` | 21-item independent review checklist | for X |
| `LOCAL_ICOSA_SEARCH.md` | offload, blocked on authoring | REQUESTED |
| `scripts/{tammes13_enclosure,barlow_shell_check,shell_2p09_interval,interval_selfaudit,outer_cell_angular_bound,icosa_compensation_search,icosa_targeted_completion}.py` | all run clean | mixed; see individual docs |
| `evidence/` | captured outputs | — |

## Net result of this block

One proved component that removes proof work in principle (`K15-E001`: the pointwise
fcc-compatibility of Hales Def 3.2 may be replaced by a cluster-averaged condition with
the same conclusion), one exact obstruction that constrains every pointwise route
(`K15-E002`: the dodecahedral cell volume `5.5502910285155 < sqrt(32)`), one
methodological obstruction (`K15-E003`: cell-volume lower bounds are not certifiable by
truncation), and one closed route (`K15-E3`, Delaunay, refuted by a source configuration
we reproduced to Monte Carlo accuracy).

## Negative result worth keeping

`local_mass_search.py` finds only `N(2.0) = 7` by randomised search, whereas the true
value is the kissing number `12` (Schutte–van der Waerden). The extremal configuration is
a measure-zero object (12 points at distance exactly 2 on a sphere), so random search
cannot reach it. Consequence for `K15-E2`: the local-mass rows must come from
spherical-code / kissing-type bounds, not from search, and `N(rho)` for `rho` just above
2 is a kissing-with-tolerance problem whose optima are structured. The search harness is
retained only as a refutation device.
