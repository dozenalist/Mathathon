# Local checks for the 03:08 Pacific review

The batch froze the four completed source revisions in `environment.json` and
hashed all source files it executed. Python and numerical library versions,
commands, per-job limits, elapsed time and observed memory are retained. The
separate solver environment is the same private CVXPY 1.9.2 environment recorded
in `solver_environment.json`. All jobs used one CPU and one BLAS thread with a
monitored 1 GiB cap and a 600-second total budget.

Seven jobs completed normally; three degree-seven polish pilots reached their
90-second caps. A timeout is not an infeasibility result. No local job remains
running. No Lean build was repeated in this checkpoint.

`independent_checks.py` reconstructs X-C014 and C's both-sides example without
using worker Fourier or sign code, and exercises the named Main checker failures.
X-C014 passes an exact polynomial root-count test and a rational Machin comparison,
giving density below 0.780718153344 under Cohn–Elkies. C's example is weaker than
density one. Main's finite controls do not establish generic soundness.

```text
python independent_checks.py PATH_TO_FROZEN_KeplerConjecture
```

The polish script hardcodes `/tmp/sc662.py`; `run_with_checker.py` maps only that
known import (or `/tmp/shell_check.py`) to the pinned local file. It logs the
substitution and leaves mathematical source unchanged. The three pilots use
seeds 100–102, degree seven, 4,000 iterations and uphill tolerance 0.05. They
produced no final JSON candidate before their caps.

`rescaled_pilot.py` calls the submitted worker implementation for the single
m=5, S=8 CLARABEL instance and three rational-factor denominator caps. It completed
in 34.985 seconds. Worker-accepted proposals near 0.78071821498 are weaker than
the frozen certificate and remain pending independent validation. Their factors
and output are retained under `ProducedOutputs`; no solver status is treated as
a proof. The supervisor review gives the acceptance scope for every log.
