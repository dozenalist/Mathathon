# Exact auxiliary functions for dimension 4

**Assessment:** an exact, angle-dependent **three-point lattice** certificate for
$D_4$ is a credible research target. The ordinary two-point Cohn–Elkies method
is provably insufficient. No exact certificate or solution of unrestricted
four-dimensional sphere packing is claimed here.

Read the [feasibility report](REPORT.md) for the conclusion, mathematical
obstructions, computational findings, and proposed next experiments.

This folder contains the results of a one-hour research sprint on 14 November
2026, beginning at 19:44:55 UTC. The work is motivated by the
[Mathathon Kepler problem](https://competition.sair.foundation/competitions/mathathon/problems/15?q=kepl).
The target is Cohn–de Laat–Salmon's Conjecture 6.1, which concerns lattices.

| Artifact | Contents |
|---|---|
| [Feasibility report](REPORT.md) | Main conclusions and research plan |
| [Literature audit](notes/literature-audit.md) | Primary sources, exact scope, and recent-claim checks |
| [Theory assessment](notes/theory-assessment.md) | Proofs of class obstructions and a matrix-Gaussian framework |
| [Cardinal near-certificate](notes/cardinal-near-certificate.md) | Exact Fourier positivity and lattice zeros, with an explicit sign failure |
| [Angular harmonic lifts](notes/harmonic-lift.md) | Explicit 8/24-dimensional Fourier bridge, class obstructions, and local profiles |
| [Numerical assessment](notes/numerical-assessment.md) | Exact finite algebra and its limitations |
| [Computation instructions](computation/README.md) | Reproducible standard-library Python diagnostics |
| [Published solution inspection](computation/UPSTREAM_REPRODUCTION.md) | Reconstructing the authors' first-shell angular slice from bounded archive reads |
| [Claim ledger](CLAIMS.md) | What is proved, computed, observed, or still proposed |

From this directory, run:

```sh
python computation/run_diagnostics.py
python computation/verify_rank_witnesses.py
python experiments/angular_profiles.py
```

These offline scripts verify finite algebra and necessary interpolation
conditions. An optional, separately documented network command inspects the
authors' stored numerical solution. No script optimizes a new semidefinite
bound or proves global sign inequalities. Published density bounds remain
identified as published data.
The mathematical arguments have been independently reviewed within this sprint;
they have not been formalized in Lean.
