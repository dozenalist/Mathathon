# Local request — directed Tammes-13 enclosure for K15-E014

```text
request_id   = K15-EXP-002
status       = IMPLEMENTED — awaiting independent re-run
owner        = i-ve-attached-thomas-4iws (E)
reviewer     = i-ve-attached-viazovska-f7hh (X); Astra executes
claim_id     = K15-E014 (thin shell at rho=209/100), blocks K15-E030 target (T)
source_commit= b84f9a05eebf810a5522bd9c275df0a1e77d3fce (parent checkpoint)
branch       = kepler15/experimental/run-01
workdir      = KeplerConjecture/Experimental
inputs       = scripts/shell_2p09_interval.py (exact rational endpoint, already run)
dependencies = python3 + mpmath (or python-flint 0.9.0 for directed rounding)
```

## Question

Produce a **certified upper bound** `theta_13^+ < 57.1709021867 deg` (equivalently
`< arccos(23681/43681)`) for the maximal minimal angular separation of 13 points on
`S^2`. Target: a bound below `57.16 deg`, giving at least `0.01 deg` of slack.

The margin is only `0.0342 deg`, so a floating-point recomputation is not acceptable.

## Two acceptable routes

**Route A — directed enclosure from Musin–Tarasov's configuration.** Take the extremal
13-point configuration from arXiv:1002.1439v3 Theorem 1 (Section 2, printed p. 3). If its
coordinates are algebraic or determined by polynomial systems, enclose the minimal angle
with interval arithmetic (`python-flint` or `mpmath` with explicit directed rounding),
verifying the defining equations by exact residual bounds.

**Route B — independent enclosure.** Recompute the minimal angle of that configuration
from its defining equations with certified interval Newton / Krawczyk iteration, and
enclose all 13 choose 2 pairwise angles.

```text
command    = python3 Experimental/scripts/tammes13_enclosure.py --target-deg 57.16 \
               --precision 1e-12 --method interval-newton
resources  = 1 thread, 2 GB RAM, 10 min cap
outputs    = Experimental/evidence/tammes13_enclosure.json
success    = an interval [lo,hi] for the minimal angle with hi < 57.16 deg, plus
             residuals of the defining equations all below 1e-10
certification = rigorous interval bound only; a float value does NOT satisfy this
remaining  = RESOLVED: tammes13_enclosure.py is written and has been RUN on the SAIR
             VM in 0.25 s (permitted: exact rational interval arithmetic, no heavy solve).
             It does not transcribe the extremal configuration at all; it uses the
             analytic equations (E1)/(E2) from the source Remark, so no transcription is
             needed. Astra is asked only to RE-RUN independently and to check the Taylor
             remainder argument. Command:
               python3 Experimental/scripts/tammes13_enclosure.py
             Expected: 'margin = +3.826e-04  (>0 CERTIFIED)', exit 0.
```

## Dependency disclosure

Musin–Tarasov's theorem is computer-assisted (case enumeration). Even with a certified
enclosure of the angle, `K15-E014` inherits that dependency, and the enclosure certifies
only the arithmetic of the final comparison, not the enumeration. Recorded in
`SHELL_2P09.md`.
