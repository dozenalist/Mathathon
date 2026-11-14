# Local computation handoff

The Astra supervisor runs Lean and heavy numerical work on the user's local
computer. Main collects requests from the four Kepler sessions and maintains
this queue. Submit the source and request in a pushed Kepler-only checkpoint,
then end the research turn when results are needed to proceed. The continuous
completion watcher wakes Astra to review the request and execute it locally.
Continue independent mathematical work while an already-submitted job runs.

## Queue

No computational request has been submitted at setup. No new Kepler theorem
has been locally compiled or numerically certified at this checkpoint.

## Required request record

```text
request_id = K15-COMPUTE-001
status = REQUESTED | RUNNING | COMPLETE | FAILED | NEEDS_REVISION
owner = SAIR session ID and role
reviewer = independent session ID and role
claim_id = precise claim or baseline tested
source_commit = full pushed Git commit
branch = exact branch
working_directory = repository-relative path
input_files = explicit KeplerConjecture paths and checksums where useful
command = complete reproducible command with arguments
dependencies = pinned Lean/mathlib or numerical package versions
resources = requested wall time, threads, peak RAM, disk estimate
parameters = dimension, scale, degree, grid, precision, seed, tolerances
expected_outputs = explicit KeplerConjecture paths
success_criteria = expected assertions, residuals, signs, or theorem names
certification = exploratory floating point, interval, exact, or Lean kernel
remaining_obligations = global signs, tails, realization, proof gaps
```

For Lean, identify the actual `.lean` module, imports, exact target statements,
and declarations for `#print axioms`. The pinned project toolchain is Lean
v4.35.0 with Mathlib v4.35.0. Build/cache preparation is a local supervisor task.
Record compile exit status, complete relevant diagnostics, toolchain, source
hash, and axiom output. A successful unrelated root build gives no evidence
about an unimported Kepler file.

For numerical work, save compact coefficients and solver output along with
the generator. Report density normalization, objective, primal and dual
residuals, global-sign/tail certification status, and independent validation.
Request an initial small instance with a measured resource budget before
expanding a large solve. The supervisor will run feasible requests and return
logs or a concrete local limitation. Unexecuted jobs remain pending.

Main owns integration of this queue. Workers can put standalone requests in
their own role directories and identify them in the final response for Main
or Astra to collect.
