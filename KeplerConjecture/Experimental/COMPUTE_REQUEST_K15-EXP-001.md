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
source_commit= <filled at push; branch kepler15/experimental/run-01>
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

## Job B — certified cluster-average for the icosahedral 13-cluster (K15-E004)

Purpose: decide whether the icosahedral 13-cluster satisfies
`sum_{v in K} vol Omega(v) >= sqrt(32)|K|`, which is the first test case for the
cluster-averaged criterion `K15-E001`.

Blocking subtlety, already established (`K15-E003`): cell volume is monotone decreasing
under adding centres, so a finite cluster gives an **upper** bound. A certification must
therefore supply a *lower* bound for the worst completion, not a sampled value.

```text
command      = python3 Experimental/scripts/cluster_average_certify.py --cluster icosa13 \
                 --outer-mode certified-taylor --rho-outer 6.0 --precision 1e-12
parameters   = core = origin + 12 icosahedron vertices at circumradius 2;
               outer region radius 6; interval arithmetic with directed rounding
resources    = 4 threads, 8 GB RAM, 2 h cap
outputs      = Experimental/evidence/icosa13_cluster_average.json
success      = interval [lo,hi] for sum_{v in K} vol Omega(v) over all separations-2
               completions; decide lo >= sqrt(32)*13 or hi < sqrt(32)*13
certification= rigorous interval bound only if the outer optimisation is enclosed
remaining    = whole-packing statement is NOT implied either way
```

If Job B is infeasible, the fallback is a one-sided refutation: search for a completion
whose 13-cluster average is `< sqrt(32)`, which would refute `K15-E004` at `D >= 4` and
redirect the route. Report infeasibility honestly rather than a sampled value.

## What is NOT requested

No Lean build this cycle; no change to root build files; no dimension-8 computation.
The heavy CE/3-point SDP work for `K15-E2` belongs to C, not here.
