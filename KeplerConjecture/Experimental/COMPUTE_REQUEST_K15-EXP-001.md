# Local computation request — K15-EXP-001

Collected by Main into `Main/LOCAL_COMPUTE_REQUESTS.md`; executed by Astra on the user's
computer. Two independent jobs; either may run alone.

```text
request_id   = K15-EXP-001
status       = REQUESTED
owner        = SAIR session i-ve-attached-thomas-4iws (role E, Experimental)
reviewer     = SAIR session i-ve-attached-viazovska-f7hh (role X, Counterexamples)
claim_id     = K15-E002 (fixture, PROVED), K15-E003 (obstruction, PROVED),
               K15-E004 (cluster-average question, OPEN), pending K15-E2 rows
source_commit= 64f379f9da30e89b7b5c3ec4b991c0003a57f843 (parent checkpoint)
branch       = kepler15/experimental/run-01
workdir      = KeplerConjecture/Experimental
inputs       = scripts/icosa_cluster_test.py
               scripts/local_density_fixtures.py
dependencies = python3, numpy, scipy, sympy (available on the VM; pin locally)
```

## Job A — local-mass function `N(rho)` (for K15-E2)

Purpose: determine, to certified precision, the maximal number of centres of a
separation-`>= 2` set inside a ball of radius `rho` around a centre, for `rho` on a grid
in `(2, 3]`. This supplies the constraint rows `mu(B(0,rho)) <= N(rho)` of candidate
`K15-E2`; without certified values those rows are unproved.

```text
command      = python3 Experimental/scripts/local_mass_search.py --rho-max 3.0 --step 0.05 --jobs 8
parameters   = rho grid 2.00..3.00 step 0.05; separation target 2.0; tolerance 1e-9
resources    = 8 threads, 16 GB RAM, 4 h cap (stop early on convergence)
outputs      = Experimental/evidence/local_mass_N_of_rho.json
success      = for each rho, a configuration with N centres and an upper-bound
               certificate (e.g. spherical-cap / kissing-type argument or a certified
               branch-and-bound box search) proving no N+1 configuration exists
certification= rigorous for the reported N if the upper bound is certified; the
               search alone is exploratory
remaining    = values at rho > 3 not requested; the SDP may only use certified rows
```

Note: `N(2) = 12` is the kissing number (Schutte–van der Waerden) and should be recovered
as a control. Values just above 2 are the hard ones.

## Job B — WITHDRAWN, narrowed to a proved analytic lemma

The certification driver for the icosahedral cluster average is **withdrawn**. It was
labelled NEEDS_AUTHOR in the previous block and remains unauthored; per the review of
27616 it is not a runnable request and must not be counted as one.

It is replaced by two proved statements, neither of which needs execution:

**Lemma K15-E003 (PROVED).** For finite `K subset K'` and `v in K`,
`vol_{K'} Omega(v) <= vol_K Omega(v)`, so finite computations bound cell volumes from
**above** and can only refute a cluster-average lower bound. Hence no truncated
computation can certify `K15-E004`.

**Lemma K15-E002 (PROVED, exact).** The icosahedral 13-cluster's centre cell is the
regular dodecahedron of inradius 1, volume `5.5502910285155 < sqrt(32)`, so no
fcc-compatible `A` vanishes identically. Reproduced to `1e-15` by
`scripts/icosa_cluster_test.py`.

**Remaining enclosure problem, stated precisely.** To decide `K15-E004` on that cluster
one must bound
`inf over admissible completions Sigma of  sum_{v in K} vol_Omega_Sigma(v)`
from below, where the infimum runs over all 2-separated sets `Sigma` containing the
13 core points. This is an infinite-dimensional minimisation of a sum of Voronoi volumes,
and `K15-E003` shows it is not approachable by sampling. A rigorous route would need
either (a) a lower bound on `vol Omega(v)` in terms of finitely many neighbouring
distances (Rogers-simplex or Fejes Toth style, valid for every completion), or (b) a
certified branch-and-bound over the finitely many centres that can influence the core
cells — namely those within distance `2 + 4 = 6` of the origin, by the standard
`Omega(v) subset B(v,2)` bisector cut-off. Option (b) is finite but large, and would need
a genuine interval enclosure, not a float search.

## What is NOT requested

No Lean build this cycle; no change to root build files; no dimension-8 computation.
The heavy CE/3-point SDP work for `K15-E2` belongs to C, not here.
