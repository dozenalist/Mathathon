# Local execution requests — committed and runnable

Both reference committed code; neither is a sketch. Collected by Main into
`Main/LOCAL_COMPUTE_REQUESTS.md`.

## K15-EXP-005 — dense completion search (replaces the previously BLOCKED request)

```text
request_id   = K15-EXP-005
status       = CODE COMMITTED; a run completed earlier this block (exit 0, ~4 min) and a
               confirmation run of the cache-fixed build was stopped at its 4-min cap
owner        = i-ve-attached-thomas-4iws (E)
reviewer     = X
claim_id     = K15-E040 / (H_R) / (T'-R2')
source_commit= a647706fc6ed2200a41c6c2c4e5197de92e026a5 (final block checkpoint)
branch       = kepler15/experimental/run-01
workdir      = KeplerConjecture
input_files  = Experimental/scripts/dense_completion_search.py
               Experimental/scripts/block_evaluator.py        (imported)
dependencies = python3, numpy, scipy.  No Lean.
command      = python3 Experimental/scripts/dense_completion_search.py \
                 --seconds 300 --seeds 4
outputs      = Experimental/evidence/dense_completion_search.json  (written by the script)
               stdout: one JSON record per seed, then a BEST block
resources    = 1 CPU, <= 1 GiB, hard cap 300 s (the --seconds argument; max 600)
parameters   = rmax 7.0, annealing temperature 5.0 -> 0, seed 0..3, separation 2.0
```

**Expected controls.**

| control | expected | meaning |
| --- | --- | --- |
| every returned set | `minsep >= 2.0` | legality |
| core cells | not buffer-touched | the 12 outer volumes are exact |
| `threshold_sum` | `67.9888142149` | matches `K15-E031`/`K15-E050` arithmetic |
| sparse baseline (`K15-E040`) | `sum12 ~ 98.0` | the harness must beat or match this |

**Success criteria.** Either

- **(a)** a legal set with `sum12 < 67.9888142149` → `(T')` **REFUTED** for that set, and the
  geometric route is redirected; or
- **(b)** `sum12` stays above the threshold for every seed → **inconclusive**, because computed
  volumes are upper bounds. Report the minimum found as the best known upper bound on the
  infimum, not as evidence that the inequality is true.

**Certification status.** `TESTED_FINITE` in either case. No output of this harness is a
certificate for any packing.

## K15-EXP-006 — Lean, deferred

The only stable formalisation target remains the `R2'`/`R2''` partition lemma
(`LOCAL_LEAN_REQUEST.md`, `PROPOSED`). It is unchanged this block. I am deliberately **not**
committing speculative Lean: the `Block`/`components` definitions must be frozen by X against
`GEOMETRIC_PARTITION.md` first, and a file with mismatched definitions would cost more to
repair than to write. No Lean request is made here, and I do not claim one is pending.

## What is *not* offloaded

`block_evaluator.py`, `transfer_evaluator.py` and `multi_defect_test.py` all run in under 10 s
on one CPU and were executed here; their outputs are committed under
`Experimental/evidence/`. Only the annealing search needs the longer cap.
