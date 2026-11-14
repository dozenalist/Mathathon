# Local checks for the 02:23 Pacific review

`environment.json` records the immutable worker revisions, source-file SHA256
hashes and base Python environment. `solver_environment.json` records the separate
private CVXPY environment used only for the submitted SDP job. `jobs.json` records
commands, elapsed times, exit codes, observed memory and resource caps. Each job
has its complete stdout/stderr log alongside it. Produced JSON data from the six
geometric/family jobs is retained under `ProducedOutputs`, with hashes.

Nine jobs completed normally; the CubeDiff Lean job reached its monitored memory
limit. No job remains running. A zero exit from `independent_exact` means the
specific certificate verified and the reported false accepts were reproduced;
it does not mean the generic checker is sound. Other worker outputs retain their
original claim labels and must be interpreted using
[the supervisor review](../../REVIEW_2026-11-14_0223.md).

The exact independent check needs Python 3.12, SymPy 1.14 and a directory containing
the frozen `KeplerConjecture` source tree:

```text
python independent_checks.py PATH_TO_FROZEN_KeplerConjecture
```

The Windows batch runner accepts a new private snapshot parent, a text file
containing the matching cached Lean import path and the private solver dependency
directory. It refuses to overwrite a snapshot. It reuses the preceding review's
Windows resource-measurement definitions, sets one CPU/BLAS thread, and monitors
one GiB and per-job time caps. Its external total cap is 900 seconds. The source
snapshot, environment and exact commands should be retained together when rerun.

The local audit copy `CubeDiffAudit.lean` appends only `#print axioms` to the
submitted module. Reaching the memory cap produced no verified theorem/axiom
report. The earlier algebraic normalization result is unaffected.
