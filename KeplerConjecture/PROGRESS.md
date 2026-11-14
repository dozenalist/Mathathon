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

### K15-EXP-002 — 2026-11-14, America/Los_Angeles — role E (Experimental)

Second block, following review 27616. Branch `kepler15/experimental/run-01`, based on
Main checkpoint `a08f378be6a03f80ac075b34f8ba99aeb8201d9e`. Ultramath not used; no swarm
started or resumed.

| claim | status | change |
| --- | --- | --- |
| `K15-E010` | PROVED | cap inequality direction repaired: it is `theta <= 2 arccos(1-2/k)`, an upper bound; `13*2pi*(1-11/13) = 4pi` exactly |
| `K15-E011` | PROVED | exact radius conversion for centres of differing radius in `[2,2+delta]`; binding case at the largest radius; `theta_min` decreasing, `60 deg` at `delta = 0` |
| `K15-E012` | PROVISIONAL | explicit 12-shell bound with `delta_0 = sqrt(2/(1-cos theta_13)) - 2`; numeric `0.0911455` depends on an **unverified** Tammes-13 constant |
| `K15-E013` | OPEN | Barlow compatibility of the 12-shell; FCC/HCP safe up to `delta < 0.8284` |
| `K15-E020` | SPECIFIED | local-mass row `n_v(rho) <= (rho+1)^3 - 1` in measure form; validity proved from C013(a); strength unevaluated; slack 14 at the contact shell |
| `K15-E001` | PROVED (conditional) | burden quantified: removes the explicit transfer formula, does not remove `K15-E004`, cannot be certified numerically |
| `K15-EXP-001` Job B | WITHDRAWN | unauthored driver removed; replaced by two proved lemmas and a precise enclosure problem |

Reconciliation of the 27616 review: the cap reversal is accepted and repaired
(`K15-E010`); the "twelve-contact Fourier sum" objection is accepted and the analytic
candidate is reformulated as an integral constraint on the pair measure (`K15-E020`),
which does capture distant completions. The `delta < 0.0366` rounding is replaced by the
exact `28^(1/3) - 3 = 0.0365889718757`, verified to `1e-12`.

Negative results retained: the cap bound alone yields `delta_0 < 0`, so the thin-shell
route needs a genuine Tammes-13 input and a count bound rather than a volume bound;
C013(a)'s volume count is vacuous for `n <= 12` (`13^(1/3) - 3 < 0`).

Artifacts: `Experimental/SHELL_CONVERSION.md`, `Experimental/ANALYTIC_LOCAL_MASS.md`,
`Experimental/scripts/shell_conversion.py`,
`Experimental/evidence/shell_conversion.txt`, plus the revised `LOCAL_CRITERION.md` §5.

### K15-EXP-003 — 2026-11-14 00:08 America/Los_Angeles — role E (Experimental)

Hourly block. Branch `kepler15/experimental/run-01`, parent `b84f9a05eebf810a5522bd9c275df0a1e77d3fce`.
No Ultramath; runtime mode unconfirmed; no swarm started or resumed.

Five review corrections accepted and repaired:

| id | correction | disposition |
| --- | --- | --- |
| `K15-E011` | varying-radius max is `max(1-2/R^2, R/4)`; equal-radius formula valid only for `0<=delta<=sqrt5-1` | **PROVED**, range stated, review's `delta=2` ray counterexample recorded |
| `K15-E001` | boundary count must not subtract upper bounds | **PROVED**, now `|T| <= (r+D+2)^3 - r^3 <= 3(D+2)(r+D+2)^2` via disjoint unit balls avoiding `B(x,r)` |
| `K15-E004` | universal "every cluster" fails for all `D` (singleton dodecahedral cell) | **OPEN**, restated as existence of a suitable partition |
| `K15-E003` | "not certifiable by truncation" too broad | **PROVED**, corrected: a bounded cell with a complete `4`-neighbourhood does certify |
| `K15-E020` | averaged pair mass is necessary, not equivalent | **SPECIFIED**, corrected; also no implemented 3-point SDP in my source |

New artifacts: `Experimental/SHELL_2P09.md` (`K15-E014`, thin shell at `rho=209/100`,
`cos theta_min = 23681/43681` **exact rational**, `theta_min = 57.1709021867 deg`, slack
`0.0342 deg` over the rounded Tammes value), `Experimental/scripts/shell_2p09_interval.py`
(runs, exact rational check), `Experimental/GEOMETRIC_PARTITION.md` (`K15-E030` block rule;
target inequality (T); equality on FCC/HCP; icosahedral block reduces (T) to
`mean outer volume >= 5.6657345`, **unproved**; ordering defect `K15-E031` OPEN),
`Experimental/LOCAL_SHELL_2P09.md` (request, BLOCKED on transcribing the extremal
configuration).

Shell-allowance theorem stated with attribution to DLOV14 and its four undischarged
hypotheses listed. No 3D number produced; `K15-E020` remains UNEVALUATED and now also
blocked on an evaluator that my artifacts do not contain.

Gaps: `K15-E014` inherits Musin–Tarasov's computer-assisted enumeration and needs a
directed enclosure (rounded 57.1367 deg is not an upper bound); `K15-E030` target (T) is
open; `K15-E031` ordering defect unrepair.
