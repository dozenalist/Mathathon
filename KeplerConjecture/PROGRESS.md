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

### K15-EXP-004 — 2026-11-14, America/Los_Angeles — role E (Experimental)

Continuous block. Branch `kepler15/experimental/run-01`, supervisor source
`ec2596dce67a4c6a93157d291c2f8e2e58f5cfc3`. Ultramath not used; runtime mode unconfirmed.

**`K15-E015` — PROVED (arithmetic).** `tammes13_enclosure.py` implemented and RUN on the
SAIR VM in 0.25 s: rational interval arithmetic only (Fraction endpoints, `pi` enclosed by
`333/106 < pi < 355/113`, Taylor sin/cos with explicit alternating remainder, no floating
point in any decision). Root selection proved analytically: `g'(a) < 0` on `(0,pi/2)`
because both terms are strictly negative, so `g` has at most one root; sign change
certified on `[12113/10000, 12114/10000]`. Comparison made in cos-space, so no arccos
occurs in the certificate. Result: `delta_13 < 57.146323807 deg` and
`theta_min > 57.170897332 deg`, margin `+3.826e-04 > 0` CERTIFIED.

**`K15-E014` — PROVED.** At most 12 centres of a 2-separated set lie in `[2, 2.09]`.
Dependency disclosed: `d_13 = delta_13` is Theorem 1 of arXiv:1002.1439v3, proved there by
computer enumeration of irreducible contact graphs; this block certifies only the
arithmetic of the constant.

**`K15-E031` — R1 withdrawn, precise failure.** (T) is not preserved under truncation: if
all 12 neighbours of a defective centre are absorbed by earlier blocks the block is the
singleton `{v}` and (T) reads `5.5502910285 >= 5.6568542495`, false. Rule R2 (components of
the defective graph, block = `C union N(C)`) replaces it and reduces the route to two
checkable statements: `(T') S(C) >= D(C)` and `(T'') diam(C) <= D_0`. Both open; the
icosahedral component requires `S(C) >= 0.1065632`.

Gaps: independent re-run and reading of the Taylor remainder argument (Astra/X);
`K15-E013` Barlow shell check; (T') unproved; `K15-E020` still blocked on a three-point
evaluator that my artifacts do not contain.

### K15-EXP-005 — 2026-11-14, America/Los_Angeles — role E (Experimental)

Continuation of the same block (timing extension). Branch `kepler15/experimental/run-01`.
Ultramath not used.

| claim | status | note |
| --- | --- | --- |
| `K15-E015` | PROVED (arithmetic) | bracket refined by bisection: `delta_13 < 57.138726938 deg` (was `57.1463`), margin `+4.94e-04`; runtime 0.43 s |
| `K15-E013` | **PROVED / CLOSED** | every Barlow stacking has exactly 12 centres in `[2,2.09]`; open shell is `(2, 2 sqrt2)` and `2.09 < 2.8284` |
| `K15-E014` | PROVED | unchanged conclusion, stronger arithmetic backing |
| Taylor lemma | PROVED | remainder bound stated and proved for `x <= 8/5`, `N >= 2`; hypothesis met with margin |
| `(T')` icosahedral | OPEN | quantified: outer cells must average `5.66573451791`, i.e. `0.157 %` above an fcc cell; inscribed balls fall `19.0848` short |

`K15-E013` proof: adjacent-layer heights `h = 2 sqrt(2/3)`, hollow offsets of modulus
`2/sqrt3`; nearest `|u+delta|^2 = 4/3` gives distance `2`, next `16/3` gives `2 sqrt2`;
in-plane `2`, `2 sqrt3`; two layers `2h = 3.266`. No spectrum value in `(2, 2 sqrt2)`.
Numerical cross-check `barlow_shell_check.py` on `ABC`, `AB`, `ABCB`, `ABAC` all return 12.
Two construction bugs were found and fixed (wrong hollow shift; reference centre in the
bottom layer) and are recorded in the doc.

`(T')` narrowing: inscribed-ball bounds are excluded with exact arithmetic
(`13 * 4pi/3 = 54.454` against `73.539` required, shortfall `19.085`), so any proof must be
a neighbour-count-versus-volume estimate. Recorded along with the incomplete `t(u)` route.

Gaps: `(T')` open; `(T'')` diameter bound not attempted; `K15-E020` still blocked on a
three-point evaluator; the Taylor lemma and the enclosure want independent review.

### K15-EXP-006 — 2026-11-14T09:16:38Z America/Los_Angeles — role E (Experimental)

Full 60-minute block, task `K15-HOUR-20261114-E`. Ultramath not used; no swarm created or
resumed. Standard runtime.

**Frozen and extended (`K15-E015`).** Count-12 at BOTH radii, no floating estimate:

| radius | exact cos(theta_min) | margin | verdict |
| --- | --- | --- | --- |
| `2.05` | `881/1681 = 0.524092802` | `+1.854e-02` | CERTIFIED |
| `2.09` | `23681/43681 = 0.542135024` | `+4.939e-04` | CERTIFIED |

Equal-radius case verified to bind exactly at both radii (`thr >= R/4`). `delta_13 <
57.138726938 deg`. Both comparisons made in cos-space, so no arccos enters either
certificate. Review checklist for X in `REVIEW_CHECKLIST_X.md`.

**Geometric route (`K15-E040`, OBSTRUCTED quantitatively).** Proved that local distance data
can give only `vol Omega(w) >= 4 pi/3`: for every direction either a known neighbour forces
`t >= 1` or no known neighbour constrains `t` at all. So inscribed bodies inside the outer
cells cannot close `(T')`, which falls short by `19.08483258`. Bracketed the infimum over
completions in `[4.188790205, 8.167277]` per cell (window factor `1.987`) with the threshold
`5.665734518` inside it, so `(T')` is not decidable from certified data. Noted that the
threshold is only `2.080 %` above the dodecahedral floor, which makes `(T')` implausible.
Derived the corrected condition `(T'-2) S2(C) >= D(C)` over two shells, strictly weaker.
Targeted completions (rings at distance 2 in the free outward hemisphere) did not reduce
the sum below `99.8`; random completions reach `98.0`.

Gaps: `(T')`/`(T'-2)` unproved; the upper bounds are `TESTED_FINITE` and undersaturated
(density `0.10` vs `0.177`); the next missing inequality is an angular
neighbour-count-versus-volume estimate. Offload `LOCAL_ICOSA_SEARCH.md` filed.

### K15-EXP-007 — 2026-11-14, America/Los_Angeles — role E (Experimental)

Same 60-minute block (start 09:16:38Z), continuing after the first two pushes.

**`K15-E032` — R2 disjointness threshold corrected.** Following the instruction to check
block disjointness/coverage, R2 as stated was wrong: with adjacency at `2.09`, two defective
centres at distance in `(2.09, 4.18]` lie in different components yet a shared sound centre
lies in both neighbourhoods, so the blocks overlap and the family is not a partition. The
overlap only removes surplus, so `(T')` need not survive. Corrected adjacency threshold
`tau = 2*2.09 = 4.18`, with disjointness, coverage and `diam Block <= diam(C) + 4.18`
proved. `(T')` at `2.09` withdrawn as ill-posed.

**`K15-E041` — second obstruction.** `12 * V_dodeca = 66.6034923422` against the required
`67.9888142149`, shortfall `1.385321873` (`2.0376 %`). So no argument bounding the twelve
outer cells independently by the single-cell minimum can work; configuration-specific data
is required, and the dodecahedral theorem is itself computer-assisted.

**`K15-E042` — angular estimate attempted, failed.** Bound
`vol Omega(w) >= (1/3) int min(min_6 d_j/(2cos phi_j), 1.045)^3 du` gives `4.733968`
(optimised over the six free neighbour directions), an improvement of `13.0 %` on the
inscribed ball but `16.4 %` short of the threshold. A direction error (`max` instead of
`min` in the fallback) initially reported `5.943752`, above threshold; caught and recorded
in both the doc and the evidence file.

**Interval self-audit.** `interval_selfaudit.py`: 118 point-interval soundness checks
against 60-digit mpmath, all pass; monotone-wrapper endpoints pass; a too-tight corruption
is detected `50/50`; the `Iv` constructor rejects `lo > hi` structurally; `pi` enclosure
verified.

Artifacts: `GEOMETRIC_OBSTRUCTION.md` extended, `REVIEW_CHECKLIST_X.md`,
`LOCAL_ICOSA_SEARCH.md`, `scripts/{interval_selfaudit,outer_cell_angular_bound}.py`,
`evidence/{icosa_compensation_search,icosa_targeted_completion,outer_cell_angular_bound}.txt`.

Gaps: `(T'-R2')` open; best certified per-cell bound `4.733968` vs required `5.665735`;
`icosa_dense_optimize.py` unauthored (`LOCAL_ICOSA_SEARCH.md` BLOCKED on authoring).
