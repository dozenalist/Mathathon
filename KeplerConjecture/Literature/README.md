# Kepler problem 15 literature

Curated on November 13, 2026, America/Los_Angeles. Read the [problem specification](PROBLEM_SPEC.md), then the source cards in [CORE_SOURCES.md](CORE_SOURCES.md). The [machine-readable catalog](sources.json) and [BibTeX](references.bib) preserve source identities and versions. The [Hexagon review](HEXAGON_REVIEW.md) records the separate search of LLM-based mathematics sources. The [prior-work inventory](PRIOR_WORK.md) records the project's historical SAIR material and its verification status.

| Priority | Source IDs | Purpose |
| --- | --- | --- |
| All agents first | H05U, CE03, LI24 | Fix the local correction criterion, Fourier conventions, and the proven obstruction to exact ordinary two-point LP in dimension 3 |
| Main and Experimental | H05U, HM10, H12, V17, CKMRV17, CDS22 | Compare proof architecture and develop local, analytic, and hybrid candidates |
| Computation and Counterexamples | CDS22, LI24, DLOV14, DLM20 | Reproduce 3D benchmarks and build independent certificates |
| Lean | FLY17, FORM26 | Identify reusable formal infrastructure and audit theorem scope before porting |
| Secondary higher-dimensional work | DV15, CZ14, CKMRV17 | Study stronger hierarchies and transfer mechanisms with an explicit return to the 3D question |

The source cards distinguish statements checked in the paper from abstract-only leads. Three central open PDFs are retained locally as [Hales's unabridged proof](Papers/Hales2005-unabridged.pdf), [Cohn–Elkies](Papers/CohnElkies2003.pdf), and [Li's obstruction](Papers/Li2022-v3.pdf). Their download URLs and SHA-256 hashes appear in the catalog. Other papers and ancillary data are linked directly. Numerical values copied from a source retain that source's rounding and status. Local reproduction remains a research task until a run and certificate are recorded in `Computation/`.

Every new citation or borrowed construction must be added to this collection with its version, precise locator, access date, role in the argument, and limits. Record failed searches and inaccessible sources. Compare candidate complexity with the closest existing method using proof dependencies, geometric cases, certification workload, and actual exposition.
