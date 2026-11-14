# Local request — angular neighbour-count vs cell volume (K15-E040)

```text
request_id   = K15-EXP-003
status       = REQUESTED
owner        = i-ve-attached-thomas-4iws (E)
reviewer     = i-ve-attached-viazovska-f7hh (X); Astra executes
claim_id     = K15-E040 (icosahedral compensation), K15-E014 (count 12)
source_commit= <this block's commit; see final report>
branch       = kepler15/experimental/run-01
workdir      = KeplerConjecture/Experimental
inputs       = scripts/icosa_compensation_search.py       (already run, 10.5 s)
               scripts/icosa_targeted_completion.py       (already run, 1.4 s)
dependencies = python3, numpy, scipy (present on VM); no Lean
```

## Question

Determine the infimum of `sum_{i=1..12} vol Omega(w_i)` over **saturated** completions of
the icosahedral 13-cluster, to within a certified bracket. Decisive threshold
`67.9888142149` (mean `5.665734518`).

This decides `(T')`. Note the one-sidedness: a completion below the threshold **refutes**
`(T')`; no computed value can prove it.

## Why the existing runs are not enough

Both existing scripts are undersaturated: `155` centres in a ball of radius `7.2`, density
`0.10` against `0.177` for fcc, giving sums `98`–`108`. The threshold is `68`, so the search
must be roughly `30 %` denser in the shells that bound the twelve outer cells, and must
place centres *cooperatively* across neighbouring outer centres rather than one at a time.

```text
command    = python3 Experimental/scripts/icosa_dense_optimize.py \
               --saturated-shells 3 --max-centres 700 --seed 1..16 \
               --local-search basin-hopping --steps 200000
resources  = 8 threads, 8 GB RAM, 45 min cap, checkpoint every 5 min
outputs    = Experimental/evidence/icosa_dense_optimize.json
success    = either (a) a 2-separated completion with verified minsep >= 2 and
             sum12 < 67.9888142149  => (T') REFUTED; or
             (b) a documented lower bound >= 67.9888142149 over the searched family
certification = (a) is rigorous if the completion is exact rational and the Voronoi
             volumes are computed with certified arithmetic; (b) is exploratory only
remaining  = icosa_dense_optimize.py is NOT yet written. It needs a cooperative
             placement strategy and certified volume computation; until it exists this
             request is BLOCKED on authoring, not on compute.
```

## Lean

No Lean request this block. The only stable statement worth formalising later is the
elementary count lemma `K15-E014` conditional on the external `delta_13` bound; it is not
yet independent enough of the source's enumeration to be worth kernel time.
