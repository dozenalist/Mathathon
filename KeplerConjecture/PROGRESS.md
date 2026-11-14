# KeplerConjecture progress

## Current state

| Item | Status | Evidence | Next owner |
| --- | --- | --- | --- |
| Problem 15 roadmap | Prepared research plan | ROADMAP.md and Literature/PROBLEM_SPEC.md | Main |
| Literature and modern obstructions | Source compilation | Literature/README.md and CORE_SOURCES.md | Main and Counterexamples |
| Earlier SAIR work | Pending independent review | Literature/PRIOR_WORK.md | All four assigned sessions |
| New simpler general 3D proof | Open | No accepted new theorem at setup | Main |
| Numerical reproduction | Awaiting recovered inputs | Main/LOCAL_COMPUTE_REQUESTS.md | Computation and Astra |
| Local Lean proofs | No new module submitted | Lean/README.md | Main and Astra |

## History

### K15-SETUP-001 — 2026-11-13, America/Los_Angeles

Author is Astra supervisor `01a1d8c0-f50f-7352-a61a-3927660a8eea`, with
separate literature and roadmap drafting agents. Mathematical research claims
remain subject to independent review by the assigned Counterexamples session.

Prepared the seven-part research roadmap, source cards and bibliography,
Hexagon review, prior-work inventory, and local computation handoff. The goal
is a simpler proof of the general three-dimensional sphere-packing bound
`pi/sqrt(18)`, with useful proved partial results and reproducible obstructions
also recorded. Initial research uses four existing SAIR chats, a 90-minute
budget, diverse approaches, and numerical promotion gates for CE-like bounds.

Source checkpoint is `099c194972c54b9326b119fdd9ad93a09985b408`. Setup branch
is `kepler15/setup-01a1d8c0`. The isolated checkout, session IDs, completion
cursors, actual prompt message IDs, and confirmed push result are retained in
the supervisor's private run manifest. This entry does not assert delivery of
a prompt or a successful push before the API and GitHub confirm them.

Validation includes checking the primary-source locators, reconciling density
conventions, parsing the literature catalog, and reviewing the Kepler-only
Git diff. Existing SAIR notes were recovered for review and their hashes
recorded. No new Kepler proof or numerical certificate is claimed here.

Next work is to recover prior executable evidence, independently audit its
claims, reproduce a three-dimensional baseline locally, and compare a local
geometric route with a strengthened analytic/hybrid route. Main integrates
worker reports and updates this table and chronology at each checkpoint.

### K15-EXP-001 — 2026-11-14, America/Los_Angeles — role E (Experimental)

Author session `i-ve-attached-thomas-4iws`. Branch `kepler15/experimental/run-01`,
based on setup commit `69f3213aa6f2b636ec1b0e25a7394acfecae986b`. All tracked changes
under `KeplerConjecture/Experimental/`.

| claim | status | reviewer | headline |
| --- | --- | --- | --- |
| `K15-E001` | PROVED | X | cluster-averaged correction criterion; strictly generalises H05U Def 3.2 / Lemma 3.3 |
| `K15-E002` | PROVED (exact) | X | dodecahedron cell volume `5.5502910285155 < sqrt(32)`; `A` cannot vanish pointwise |
| `K15-E003` | PROVED | X | cell volume monotone under adding centres; cluster averages not certifiable by truncation |
| `K15-E004` | OPEN | X | is `sum_{v in K} vol Omega(v) >= sqrt(32)|K|` for every cluster of diameter `<= D`? |
| `K15-E1` | PARTIAL | X | candidate: local geometry, criterion proved, local lemma open |
| `K15-E2` | SPECIFIED | X | candidate: three-point + local-mass rows; outside Li's obstruction; unevaluated |
| `K15-E3` | OBSTRUCTED | X | candidate: pure Delaunay, refuted at `(2,2,2,2,l,l)`, `l=sqrt(2(3+sqrt6))` |

Mechanism reconstructed verbatim from `Literature/Papers/Hales2005-unabridged.pdf`
PDF p. 46 (printed p. 34). The accounting lemma uses only two geometric facts (ball
volume, `Omega(v) subset B(v,2)`); the entire geometric burden is in producing `A`.
`K15-E001` exploits that observation: replacing the pointwise condition by a
cluster-average with `sum_{v in K} c(v) >= sqrt(32)|K|` preserves the conclusion and
removes the need for an explicit transfer formula (Hales's V-cell construction,
Lemma 5.28, and the four-way cancellation of Lemma 7.10).

Evidence: exact dodecahedron volume reproduced to `1e-15` by
`Experimental/scripts/icosa_cluster_test.py`; Monte Carlo reproduction of
`delta_tet ~ 0.77898`, `delta_oct ~ 0.72243`, Hales extremal simplex `0.78317`
(source `~0.78469`), standard error `~0.001` — consistent, not resolved to five digits.

Negative result retained: randomised search gives `N(2.0) = 7` against the kissing value
`12`, so local-mass rows must come from spherical-code bounds, not search.

Local computation request `K15-EXP-001` (two jobs: certified `N(rho)` for `rho in (2,3]`;
certified icosahedral cluster average) filed in
`Experimental/COMPUTE_REQUEST_K15-EXP-001.md` for Main to collect.

Remaining gap: `K15-E004` is the whole content and is open; `K15-E001` does not shorten
the proof until a cluster-level local lemma is proved analytically. No claim of a
shortcut is made.
