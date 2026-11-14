# KeplerConjecture progress

## Current state

| Item | Status | Evidence | Next owner |
| --- | --- | --- | --- |
| Problem 15 roadmap | Prepared research plan | ROADMAP.md and Literature/PROBLEM_SPEC.md | Main |
| Literature and modern obstructions | Source compilation | Literature/README.md and CORE_SOURCES.md | Main and Counterexamples |
| Earlier SAIR work | First coordinator checkpoint reviewed; corrections required | Main/SUPERVISOR_REVIEW_23906.md | Main and Counterexamples |
| New simpler general 3D proof | Open | No accepted new theorem at setup | Main |
| Numerical reproduction | Main bug reproduced; three independent CE grid controls run locally; no certificate | Computation/Reviews/27616/README.md | Computation and Counterexamples |
| Local Lean proofs | Targeted-import algebraic normalization passed locally; geometric bridges remain open | Lean/Review/README.md | Main and Astra |
| Publication and response logs | Setup published in draft PR #1; save and push every final response | Main/SUPERVISION.md and ChatLogs/ | Astra |

## History

### K15-REVIEW-003 — 2026-11-13, America/Los_Angeles

Astra checked an old Main watcher error alert and found the replacement alive,
waiting and already holding new completion 27616. All four owned watchers were
alive; no restart or uncertain resend was needed. Exact project/session and
completion binding was verified against state, ownership and live history.

Reviewed Main source `a08f378be6a03f80ac075b34f8ba99aeb8201d9e` with an
independent mathematical auditor. Several earlier corrections are sound, but
the exported proofs retain counting, denominator and hybrid-sign gaps. The
finite-zero objection was narrowed to preserve the stronger Fourier-positive
theorem's hypotheses. See `Main/SUPERVISOR_REVIEW_27616.md`.

Local computation reproduced an omitted Fourier-positivity constraint in
Main's script, invalidating C014. The separate Computation code was executed
at degree/grid (31,1200), (31,4000), and (41,4000). Its values approach the
published control but all tested candidates retain sign violations. Status is
`TESTED_FINITE`, with no new certified bound. The updated targeted-import Lean
normalization passed under the pinned toolchain, with no geometric bridge
claimed. Source hashes, commands, exact versions and output logs are committed.

Main lacks a tool for contacting its existing workers. Astra therefore sent
the four owned sessions coordinated 90-minute assignments directly and
confirmed their delivered records. Main owns integration. The IDs and prior
completion sequences are recorded in the review for duplicate suppression.
The next block repairs the evidence and advances a concrete local geometric
candidate plus a distinct strengthened analytic candidate, with heavy execution
offloaded locally. No new chats or historical swarms were started.

### K15-OPS-002 — 2026-11-13, America/Los_Angeles

Astra verified that the newly delivered Main callback is a duplicate of
completion 23906. The existing correction assignment
`oc_e8673863f6cd86d0` is confirmed in live session history as delivered at
sequence 23908. GitHub still exposes the already-reviewed source revision.
No additional assignment or duplicate computation was started. The identity,
encoding reconciliation, delivery evidence and watcher check are recorded in
`Main/CALLBACKS.md`. This is an operational verification, with no new theorem
or numerical certificate. The existing 90-minute correction task remains the
next work package for Main.

### K15-REVIEW-001 — 2026-11-13, America/Los_Angeles

Author: Astra supervisor `01a1d8c0-f50f-7352-a61a-3927660a8eea`.
Independent reviewer: separate mathematical audit agent. Status: corrections
required; no new Kepler theorem accepted. Reviewed Main completion 23906 and
source commit `c91007ff11844f179921fadfb2e90d352b8c0090` on `kepler15/main`.
The detailed review records false rational-point and finite-bandwidth claims,
an inequality-sign error, incomplete CE hypotheses, a numerical normalization
mismatch, and evidence/certification gaps. These are not accepted obstructions
to entire research routes. Main owns corrections and independent re-review.

The setup checkpoint `69f3213aa6f2b636ec1b0e25a7394acfecae986b` was confirmed
on GitHub branch `kepler15/setup-01a1d8c0` and is exposed in
[draft PR #1](https://github.com/dozenalist/Mathathon/pull/1). Its validation
included source-card review, catalog parsing, PDF checksums, local Markdown
links, secret-pattern checks and `git diff --check`. The compiled bibliography
contains 16 source records and three selected accessible primary-source PDFs.

Four existing Kepler SAIR sessions received bounded research assignments with
local Lean/heavy-computation offload. Ultramath-selected UI follow-ups were
submitted, but activation in the running model calls remains unconfirmed.
Continuous watchers save and queue completion reports; automatic resume after
idle has not yet been observed successfully. See `Main/SUPERVISION.md` for the
precise ownership and operational limitations. The user stopped Computer Use
with Escape and browser operations ended.

The new standing requirement to report progress, save the exact final response
in dated `ChatLogs/` files, and push before idle is recorded in
`Main/SUPERVISION.md`. The current mathematical objective remains open.

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

### K15-COMP-001 — 2026-11-14, America/Los_Angeles — Computation (role C)

Branch `kepler15/comp-01a1d8c0`, based on `69f3213aa6f2b636ec1b0e25a7394acfecae986b`.
Artifacts: `Computation/` (scripts, `INTERFACE.md`, `RESULTS_baseline.md`,
`REQUESTS/K15-COMPUTE-001.md`, `out/*.json`). Everything below is **TESTED_FINITE**;
no certificate is claimed.

**Recovered earlier work.** The 2026-11-14 CE3/Gaussian–Laguerre experiments and shell
diagnostics were recovered from the pre-restart VM (`sharp-bounds-in-dimension-3.md`, the
`dim3` scripts, and the interrupted swarm `smwfyzz1k`), re-expressed on the unit-radius
contract, and re-implemented in tracked form. The historical transcript's dual-shell
enumeration bug is now covered by fixture F5.

| claim | status | statement | evidence | remaining obligation |
| --- | --- | --- | --- | --- |
| K15-C-CONV-001 | PROVED (elementary) | `Delta = (pi/6) rho_A = (4 pi/3) rho_B`; FCC `rho_A = sqrt2`, `rho_B = 2^(-5/2)` | `Computation/k15conv.py` four assertions; `fixtures.py` F4 counts 864 points and recovers both densities exactly | none; X to re-derive |
| K15-C-POIS-001 | TESTED_FINITE | Poisson identity on FCC holds for a Gaussian to `2.0e-29` | `fixtures.py` F5 | interval proof if it is to be cited as more than a check |
| K15-C-CONTROL-001 | TESTED_FINITE | CE LP in `d=3`: `Delta <= 0.7797024` at `K=31`, grid 1200 | `Computation/out/ce3_K31_g1200.json` | grid refinement + interval certification (request 001) |
| K15-C-BRACKET-001 | TESTED_FINITE | `0.770657 (Li) <= 0.7797024 (ours) <= 0.779747 (CE03)` | `Computation/RESULTS_baseline.md` table | the upper comparison needs CE03 read in its own units; recorded as a rounding audit |
| K15-C-INVERSE-001 | REFUTED (as a route) | prescribing the equality-case zero sets does **not** approach Kepler; it raises the bound from `+5.30%` to `+8%` / `+14%` / `+22%` | `ce3_constrained.py`, `out/constrained_K25.json` | none; useful negative result |
| K15-C-CE03ROUND-001 | source audit | CE03 Table 3 `0.18616` and CDS22 `0.779747` describe the same quantity but differ by `4.9e-05` relative, because CE03 round a rigorous upper bound up at five decimals | `k15conv.py` rounding audit | X to check against the printed page |

**Why the control matters and what it does not show.** It reproduces the published
Cohn–Elkies value to `0.006%` and brackets it against Li's floor, so it is a usable control
with a known strict gap. It is *not* a route to `pi/sqrt(18)`: `+5.3%` is a property of the
two-point linear program, not of our basis. Any candidate bound must come from a different
mechanism.

**Interfaces handed over.** E receives a callable evaluator (`Computation/evaluator.py`,
documented in `INTERFACE.md` §2) that converts any radial candidate into `Delta`, the gap to
Kepler, and sign diagnostics. X receives the checker inputs (`INTERFACE.md` §3): the four
conversion assertions, fixtures F1/F2, the Poisson fixture F5 that guards the historical
bug, the stored coefficients for solver-free re-evaluation, and the two sign violations
(`max f = +2.5e-11` at `r = 1.640`; `min fhat = -1.43e-08` at `s = 1.304`) to be confirmed
as tangency artefacts by grid refinement.

**Next bounded task.** `K15-COMPUTE-001` (fine grid, `K = 41`, plus the `r0 = 2^(1/6)`
variant) is submitted for local execution. Meanwhile Computation specifies the three-point
formulation and the mixed cell-wise/Fourier hybrid; neither depends on those numbers.

### K15-COMP-002 — 2026-11-14, America/Los_Angeles — Computation (role C), continuation

Branch `kepler15/comp-01a1d8c0`, commit `f33e814e46b4b6f6ca6b9e84b3d84ba7d841d549`
(pushed) plus this entry.

| claim | status | statement | evidence |
| --- | --- | --- | --- |
| K15-C-DLOV-SRC-001 | source audit | CDS22 Table 1.1's `Delta^str_2 = 0.773080` is "the strengthening given in [24]", and [24] is de Laat, de Oliveira Filho, Vallentin, *Upper bounds for packings of spheres of several radii*, Forum Math. Sigma 2 (2014) e23, arXiv:1206.2608. That paper's stated subject is several radii; the equal-radius strengthening is a specialisation, so citing it as an "equal-sphere two-point bound" is imprecise | `cds.txt` Table 1.1 caption and reference [24]; `k15conv.py` entry corrected and annotated |
| K15-C-3PT-SPEC-001 | SPECIFIED | the truncated three-point evaluator, free of implementation: CDS22 Theorem 1.1 on the unit-radius contract, with the two structural constraints (`f3(0,0) > 0` required, and truncation required by CDS Lemma 1.2) and a four-test acceptance protocol whose first test recovers the two-point control exactly | `Computation/REQUESTS/K15-COMPUTE-002.md` |

**The decisive test for any three-point implementation** is recorded explicitly because it is
the one that catches the two errors that would otherwise look like progress: with the kernel
set to zero the code must reproduce `0.779747` (CE03), and any solution below that value must
have `f3(0,0) > 0` — otherwise it is a two-point certificate and contradicts Li's theorem,
which would mean the code is wrong rather than the mathematics.

**Status of the route.** The three-point bound `0.770271` is the only published mechanism
that provably improves on ordinary two-point positivity here, so it is the correct second
evaluator and the correct baseline for Experimental's hybrid. It is *reproduction*, not
improvement, and is labelled as such.

### K15-COMP-003 — 2026-11-14/15, America/Los_Angeles — Computation (role C), review 27616

Branch `kepler15/comp-01a1d8c0`, base `4b509e33fe1f5d50d37f7dd19b698d708312d35a`.

| claim | status | statement | evidence |
| --- | --- | --- | --- |
| K15-C-EXACTCERT-001 | **PROVED** (conditional on citing Cohn–Elkies only) | every packing of unit spheres in R^3 has occupied-volume density `Delta <= 0.78010544` (= Kepler +5.351%) | `Computation/exactcert.py` + `gen_candidate.py` + `out/certificate_K21.json`; verification is exact rational arithmetic (Sturm over Q, Yun squarefree decomposition), no floating point in the test, no grid assumption in the proof |
| K15-C-EXACTDESIGN-001 | design note | coefficient field Q, `t = 2 pi |x|^2`, exact rational Fourier map `p -> q` with eigenvalue `(-1)^k`, half-line endpoints `[8*pi, inf)` and `[0, inf)` with `pi` enclosed in the safe direction, and an exact-multiplicity design via Yun so that double zeros (forced at an optimum) are accepted while odd crossings are rejected | `Computation/CERTIFIER.md` |
| K15-C-ODDDEG-001 | PROVED (elementary) | with strict signs, `lc(p) = (-1)^K c_K/K! < 0` and `lc(q) = c_K/K! > 0` force `K` odd; no even-degree strict-sign certificate exists in the Laguerre basis | `gen_candidate.py` refuses even degree; derivation in `CERTIFIER.md` §2 |
| K15-C-STRICTLOSS-001 | measured | the strict "no root on the half-line" test is not merely conservative but useless: at `K=9` it certifies `2.50596` where the squarefree route certifies `0.82276` | `CERTIFIER.md` §3; both paths in `exactcert.py` |
| K15-C-MAIN-AUDIT-001 | audit (confirms supervisor) | `Main/ce_laguerre.py` builds `M_hat_s` and passes it to neither `linprog`, so Fourier positivity is absent from both runs; the `(-1e6,1e6)` box rules out the reported unbounded ray, and HiGHS status 0 is optimal; the "grids are vacuous" conclusion is invalid | `Computation/AUDIT_main_ce_laguerre.md` |
| K15-C-CONVRECON-001 | PROVED (elementary) | Main's separation-2 and Computation's separation-1 conventions agree under `x -> 2x`: `t -> 4t`, `rho_A = 8c`, both giving `Delta = (4pi/3)f(0)/fhat(0)` | same file §4 |
| K15-C-R0BUG-001 | **REFUTED and repaired** | `ce3_baseline.py` omitted the `r0^3` sphere-volume factor, so the `r0 = 2^(1/6)` variant was understated by `2^(1/2)`; now `rho_A = r0^3 f(0)/fhat(0)` and the JSON records `r0_scale_factor` | code + `REQUESTS/K15-C-REQ-001.md` correction notice |
| K15-C-ROUNDING-001 | repaired | coefficients were stored at 12 digits while `Delta` was reported from the unrounded values; now stored at full double precision and `Delta_from_stored_coefficients` is recorded so the JSON is self-consistent | `ce3_baseline.py` |
| K15-C-SCOPE-001 | corrected wording | the grid LP value is **not** "numerically optimal": it is the best value found in a truncated family on a finite grid, and grid refinement *raises* it toward the family optimum. Li gives `>= 0.770657` and CE03 `<= 0.779747` as the only rigorous brackets | `RESULTS_baseline.md`, `INTERFACE.md` |

**Withdrawals.** (i) The claim that refined grids approach the CE optimum with any
certifying force is withdrawn: a grid value is neither a rigorous upper nor lower bound for
the LP optimum, because the function achieving it satisfies the sign conditions only on the
grid. (ii) The phrase "numerically optimal" is withdrawn everywhere.

**Certified ladder** (`exactcert.py`, all exact): `K = 9, 11, 13, 15, 17, 19, 21` give
`0.82276, 0.79724, 0.78487, 0.78251, 0.78229, 0.78095, 0.78011`. Monotone, and approaching
the CE control `0.779747` from above as it must.

**Next bounded task.** `K15-C-REQ-002`: reproduce the ladder locally, locate the plateau,
and have X independently re-verify one certificate (e.g. `out/certificate_K21.json`) with a
non-shared implementation. Secondary: compare E's local-mass/three-point candidate against
FCC/HCP/Barlow fixtures and the zero-kernel degeneration, on a matched family.
