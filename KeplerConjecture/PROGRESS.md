# KeplerConjecture progress

For an extensive plain-language account, read [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md).
The dated cumulative account remains in [PROGRESS_SUMMARY.md](PROGRESS_SUMMARY.md).
This technical chronology includes worker self-reports. A worker's status label
does not itself establish independent verification; the cumulative summary and
supervisor reviews identify which claims have actually been checked.

## Current state

| Item | Status | Evidence | Next owner |
| --- | --- | --- | --- |
| Problem 15 roadmap | Prepared research plan | ROADMAP.md and Literature/PROBLEM_SPEC.md | Main |
| Literature and modern obstructions | Source compilation | Literature/README.md and CORE_SOURCES.md | Main and Counterexamples |
| Earlier SAIR work | Recovered, reviewed and integrated through the 08:23 checkpoint; later inputs linked separately | Main/SYNC_2026-11-14_0823.json; PROJECT_OVERVIEW.md | Main and Counterexamples |
| New simpler general 3D proof | Open; no improved known packing bound accepted | PROJECT_OVERVIEW.md; Main/REVIEW_2026-11-14_0823.md | Main |
| Analytic controls | Finite grid outputs are not certificates; specific exact certificates independently reconstructed, all weaker than published controls | Main/REVIEW_2026-11-14_0308.md; Main/REVIEW_2026-11-14_0438.md | Computation and Counterexamples |
| Local Lean proofs | Targeted-import algebraic normalization passed locally; geometric bridges remain open | Lean/Review/README.md | Main and Astra |
| Publication and response logs | Main-branch publication authorized; reviewed source history plus extensive overview | Main/PUBLICATION_2026-11-14_OVERVIEW.md | Astra |
| Rejected certificates and software failures | Retained with exact witnesses; later targeted repairs do not establish generic soundness | Main/REVIEW_2026-11-14_0823.md; PROJECT_OVERVIEW.md | Counterexamples and Astra |
| Geometry and compensation | Specific fixtures and conditional arguments checked; universal geometric inequalities and global bridge remain open | Main/REVIEW_2026-11-14_0653.md; Main/REVIEW_2026-11-14_0823.md | Experimental, Computation and Main |
| New stability pilot | Implemented on later Main branch; floating arithmetic, rotation treatment and rigorous input bounds unresolved | PROJECT_OVERVIEW.md, section 9 | Main and Counterexamples |
| Review cadence | PAUSED by latest user request; Sair-Watch remains stopped; no further automatic assignments | Main/SUPERVISION.md | Astra |

## History

### K15-OVERVIEW-001 — 2026-11-14, main-branch publication request

Author: Astra; independent read-only factual audit by a second Codex reader.
The user requested an extensive plain-language overview, publication to main,
and cancellation of recurring check-ins. The official automation tool returned
`PAUSED`, confirmed against its saved configuration. No SAIR sends occurred.

`DOCUMENTED`: PROJECT_OVERVIEW.md consolidates the objective, literature,
specific exact analytic certificates, geometric fixtures, conditional transfer
arguments, rejected claims, checker defects, limited Lean result and remaining
proof obligations. It distinguishes the independently reviewed supervisor
checkpoint 872fa211ecc827c8d78f0c302c1f99c882cbd590 from four later worker heads.
Read-only inspection establishes that M-CERT-002 now exists and that Computation
implemented targeted volume-checker repairs; it does not certify their outputs
or general guarantees. No new mathematical acceptance is recorded.

`OPERATIONAL`: an isolated publishing worktree starts from origin/main
5746863f92b9d7dade5854c311b237ed04020106 and normally merges the supervisor
history. All publication changes are confined to KeplerConjecture. See the
publication record for scope and checks. Existing failed claims and authorship
are retained. Future research requires a new user instruction to resume
supervision; this entry does not create a follow-up assignment.

### K15-OPS-005 — 2026-11-14, 01:00 Pacific

Verified the stale Experimental watcher report for completion 41061 against
ownership, stopped state and live API history. No later user prompt exists;
the result is already pending for the next 45-minute scheduled review. The
watcher remains stopped and the 45-minute automation is active. No new research
prompt, local computation, or mathematical acceptance was triggered. Details
are in `Main/CALLBACKS.md`; this handling log and cumulative summary were
published on the Kepler feature branch.

### K15-OPS-004 — 2026-11-14, 00:53 Pacific

Latest user instruction replaces the briefly restored Sair-Watch approach with
checks every 45 minutes. The active automation's RRULE and target chat were
verified. All four restored monitor PIDs were stopped in the host context;
historical states, STOP files and reports were retained privately. No shared
supervision code or unrelated project was modified. Old callbacks are stale.

Before that cadence change, concise follow-ups were delivered to the four owned
sessions for completions M30821/C49543/E36801/X44182. The user's subsequent
30–90 minute budget (normally 60–90) was delivered to each session as steering,
with exact message IDs in `Main/ASSIGNMENTS_2026-11-14_0040.json`. Main leads
integration; C implements the missing benchmark, E the enclosure/partition work,
and X independent checking and its driver repairs. No extra research assignment
was sent after the final cadence instruction. Future checks will inspect actual
history and avoid interrupting busy work or duplicating those prompts.

This checkpoint changes supervision and documents delivery; it accepts no new
mathematical claim. Current research results remain pending the next scheduled
review. `supervision-state.json` is the authoritative private operational record.

### K15-HOURLY-001 — 2026-11-14, 00:08 Pacific scheduled review

Author/reviewer: Astra, with independent code and mathematical audits. Reviewed
owned completions M30102, C48443, E35401, X41644 at the immutable four branch
tips in `Main/HOURLY_SYNC.json`; a fresh fetch found no new source commits beyond
the prior synchronization. All changes remain confined to KeplerConjecture.

`REFUTED`: Computation's K21 Fourier polynomial is negative at the rational
point `57955199/21687900`. Independent SymPy reconstruction and the full rational
value are saved in `Computation/Reviews/48443/`. The quiet checker ignores
failures, and its odd-part routine loses the leading sign. The pi bracket
passes a separate exact check; this does not validate the candidate. Further
ladder runs were deferred because the certifier is unsound.

`REFUTED`: Counterexamples' fixed-family infeasibility conclusion. The exact
Gaussian pair `P=2-2s/3`, `Q=1+2v/3` is feasible. A local run reports a HiGHS
Model error, not infeasibility. Its density formula is too large by pi. Evidence
and frozen original sources are in `Counterexamples/Reviews/41644/`.

Reviewed narrow repairs to periodic approximation and fixed-coset counting;
flagged center-versus-spatial averages and overly broad hybrid exclusions.
Repaired the intended range of the radial shell argument and boundary-count
estimate; required an existential controlled partition instead of a false
universal cluster inequality. Added a hashed Tammes-13 primary source, with
its computer-assisted dependency explicit. Radius 2.09 and the shell-allowance
benchmark remain pending proof and numerical evaluation.

Both local diagnostic runs completed in under a second each. No new Lean
module or long-running task remains. Four focused follow-ups, at most 35 minutes
and checkpoint by 01:00 Pacific, were delivered to the existing owned chats at
00:25. Main integrates; delivery IDs and dedup evidence are recorded in the
hourly review. Watch-Sair remains stopped. No new Kepler bound is accepted.

### K15-HOURLY-001 publication supplement — 2026-11-14, 00:35 Pacific

The four agents completed the new block before publication. M30821/C49543/
E36801/X44182 correspond to sources `49c3d70e`/`8bb50f85`/`96fbf9bb`/`3831361a`.
These checkpoints were merged with authorship retained; historical progress
conflicts retain both sides. Full hashes and original reviewed inputs are in
`Main/HOURLY_SYNC.json`. They await the next scheduled full review; no second
prompt cycle was started.

Four local bounded checks completed. C's regression suite passes in 21 seconds
(finite samples are not a verifier proof). E's script computes the rational
shell endpoint and floating margin but does not supply a directed enclosure.
X's degree-six single iteration reproduces a Model error and no candidate;
an exact regression finds `kepler_ok(99/100,1)` incorrectly true because it
truncates the rationals. Logs, time caps and source hashes are in
`Main/LocalChecks/2026-11-14_0008/`. E's actual enclosure program and C's
strengthened benchmark are explicitly unwritten, so those requests require
implementation before execution. No local job remains running.

Main has integrated the principal retractions and narrowed its claims. Several
claims in X's new note remain false; specific objections are recorded in the
hourly review and prefixed to the report. The original exact audits are now
available at `b649a85`, resolving the workers' temporary inability to fetch
them. All four new completions are saved as pending for 01:00 Pacific.

### K15-HOURLY-SETUP — 2026-11-14, America/Los_Angeles

Applied the user's replacement of Sair-Watch with hourly reviews. Verified the
four owned watchers stopped, created the active hourly schedule, and documented
the override of older callback-cadence instructions. The latest four SAIR branch
tips were fetched and merged into the supervisor publication branch with source
authorship preserved. Only Kepler paths changed. Main, Experimental and
Counterexamples progress conflicts were retained in `Main/AgentProgress/`;
Computation's chronology merged directly.

Added the brief `HourlyUpdates/2026-11-14_00-00_PST.md`, the cumulative
`PROGRESS_SUMMARY.md`, a readable project index and an exact source manifest.
New SAIR research claims are synchronized as working evidence, not silently
accepted as proved. The next hourly review will examine them and prepare new
prompts without duplicating the assignments already delivered.

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

**K15-C014 withdrawn (My bug).** `Computation/ce_laguerre.py` built `M_hat_s`
and never passed it to either `linprog` call, so Fourier positivity was not
imposed; both calls also used a box `|a_k| ≤ 10⁶`, so the large negative
objective was a bounded optimum, not an unbounded ray. The script is kept in the
tree with the bug and a withdrawal note (K15-C014r). The review's repaired rerun
gives `f(0) = 0.21820243547088458` at degree 8 — not the floor `3/(32π)` — and
still fails global Fourier positivity. Lesson recorded: grids are exploratory;
exact sign decisions (Sturm) are the acceptance test.

**K15-C002b / C003r.** Two proof gaps in the recovered m2 argument repaired: the
periodic-approximation estimate now uses `#C_in ≤ vol/S³` with additive errors and
a separate `c = 0` case; the count-price indexing now fixes `l` (not `j`), which
gives `≤ n` bad pairs per base centre and `≤ nk` overall. Both statements survive.

**K15-C005r.** One score frozen and both signs derived: the off-diagonal score
`S_f(v) = Σ_{μ≠v} f(v−μ) ≤ 0` at every vertex of every packing, so a centred
score `vol Ω + κS_f ≥ V_0` forces `V_0 ≤ V_dod` (no improvement), while keeping
the self-term gives only `V_0 ≤ V_dod + κf(0)` (strictly worse for `κ > 0`).
Also proved: `f(0) + 12f(2) ≥ f̂(0)/(4√2)` for every admissible `f`, so the raw
score is positive at the icosahedral cluster — the fact the earlier ledger stated
with the wrong sign. D12 freezes the score definitions.

**K15-C010r / C013r.** The bandwidth claim is refuted only in its hypothesis-free
form (the product counterexample destroys Fourier positivity); in the
Fourier-positive class `‖f̂‖₁ = f(0)` and the log term vanishes, so the budget is
`R ≥ K log2/(2π r_K) − o(1)` and its usefulness is open. Counting envelope: 12 is
both an upper bound for thin shells and attained (icosahedral twelve, mutual
distance 2.1029); the cap inequality gives `θ ≤ 2 arccos(11/13)`, not `≥`; the
exact threshold is `δ < ∛28 − 3`.

**Integrated worker evidence** (read from their branches, not accepted wholesale):
E's cluster-averaged criterion `K15-E001` (relaxes Lemma 3.3 to cluster averages)
and E's `K15-E003` monotonicity obstruction (finite-cluster volumes are upper
bounds, so sampling can only refute) → K15-C015, now the lead local route (D11).
X's registry: X-C001 (contact-shell Laplacian forced positive somewhere), X-C002
(3D maximisers not unique: HCP and the Barlow family), X-C003 (icosahedral cell
`V_dod`, deficit 0.106563), X-C007 (grid feasibility ≠ certificate) and X-C008
(exact Sturm certification) → K15-C016. C's controls: `Δ = 0.779702445785607`
(K=31/g1200) and `0.779745768082807` (K=41/g4000), `TESTED_FINITE`, `min f̂` of
order `1e−6`, no certificate.

**Queue consolidated** with distinct IDs (`Main/LOCAL_COMPUTE_REQUESTS.md`):
`M-LEAN-001` complete, `C-NUM-001` complete/exploratory, `C-CERT-001`,
`E-CERT-001`, `X-R01` open, `M-NUM-002` respecified (rational threshold `t ≥ 25`
or formal `π`), old `K15-COMPUTE-001/002` retired.

**Handoff questions** Q1–Q6 in `Main/TASKS.md`: C's `r ∈ [1,5]` grid versus the
`r ≥ 2` contract; C's Sturm driver; E's choice of cluster-volume machine; X's
audit of C002b/C003r/C005r/C015; the quantitative Tammes-13 literature; and
routing of the three open requests.

Not done: no certificate, no new bound, no worker contact (no channel). Next: X
audits the four repaired items; C delivers the Sturm driver; E prices a cluster
lower bound at `D = 2`.

### K15-MAIN-005 — 2026-11-14 00:08 PST — hourly review integration

Author **M (Main)**. Reviewed completion `30102`, source
`0c3ee751254b1b61f16eb175d9bd8d571f842b18`. Supervisor branch fetched at
`0e28e093fbe13fdc4e7aad684536547e3f539e06`. No chat created; no swarm; nothing
run on the VM.

* **K15-C017 (new, `REFUTED`)**: Computation's K21 certification is withdrawn.
  Its checker reports failures only under `if verbose` — the impossible input
  `[2, −1]` passes — and the rebuilt `q` has ten simple positive roots with
  `q(57955199/21687900) ≈ −3.876231892749308e−5`. No accepted bound near
  `0.78010544`. The π interval passes its own audit; its upward rounding does not.
* **K15-C018 (new, `PROPOSED`)**: the shell-allowance benchmark
  `f̂ ≥ 0`, `f ≤ η` on `[2, ρ]`, `f ≤ 0` beyond `ρ`, count 12
  `⟹ δ ≤ (4π/3)(f(0)+12η)/f̂(0)`; proof is K15-C003 + K15-C002b. `ρ = 209/100`
  is pending a Tammes-13 enclosure and E's repaired radial argument. Attribution:
  CE truncation, DLOV14, Musin–Tarasov. Not a three-point SDP.
* **K15-C005r corrected twice**: lattice identity is
  `S_f = c Σ_{ξ∈L*} f̂(ξ) − f(0) ≥ c f̂(0) − f(0)` (not an average over cells, and
  not an equality); the conclusion is narrowed to pointwise-sign hybrids.
* **K15-C010r**: `− o(1)` removed (finite Jensen estimate).
* **K15-C013**: angular lemma scope `0 ≤ δ ≤ √5 − 1`; boundary count
  `(r+D+2)³ − r³ ≤ 3(D+2)(r+D+2)²`.
* **K15-C015 refuted as universal** (singleton cluster at the icosahedral vertex:
  `5.55029 < √32`) and repaired to a specified-partition statement; the geometric
  route stays open (D14).
* **K15-C002b and K15-C003r kept** as narrow positive results, hypotheses intact.
* X's Gaussian driver: factor-`π` density error; a HiGHS "Model error" was read as
  infeasibility although `P = 2 − 2s/3`, `Q = 1 + 2v/3` is feasible.
* `D13` claim-admission rules; `D14` portfolio = one benchmark + one geometric
  target. `Main/INTEGRATION_0008.md` records sources and hashes.

Not fetchable at this checkpoint: `Main/HOURLY_REVIEW_2026-11-14_0008.md` and
`Computation/Reviews/48443/` (announced, absent from `0e28e09`). K15-C017's
witness is therefore carried from the assignment text (`M-QUEUE-001`).

### K15-COMP-004 — 2026-11-15 00:08 Pacific — Computation (role C), review 48443

**RETRACTION.** `K15-C-EXACTCERT-001` is **REFUTED** and withdrawn in full. No bound in
`Computation/` is currently proved.

| claim | status | detail |
| --- | --- | --- |
| K15-C-EXACTCERT-001 | **REFUTED** | the `K = 21` certificate has ten simple positive roots of `q`; `q(57955199/21687900) ≈ -3.8762318927e-05 < 0`. Witness reproduced exactly by `exactcert_tests.py` T5 |
| the certified ladder (`0.82276` … `0.78011`) | **REFUTED** | all seven stored candidates (`out/certificate_K9..K21.json`) are rejected by the repaired checker, by A1 or A2. Retained as evidence, not deleted |
| K15-C-BUG-001 | **PROVED (defect)** | `certify_relaxed` had `if verbose: print(...); return rec`, placing `return` inside the `if`: failures were swallowed whenever `verbose=False`, and the success path then set `ok=True` with the failure `reason` still attached |
| K15-C-BUG-002 | **PROVED (defect)** | `yun_odd_part` returned a monic odd part and discarded `lc(p)`, so `-t-1` mapped to `t+1` and the sign of the polynomial was lost |
| K15-C-CHECKER-001 | repaired, tested | single-return-path verdict computed before any printing; `yun_odd_part` returns `(c, u)` with `sign(p) = sign(c)·sign(u)`; constants, zero polynomials and endpoint roots handled explicitly and fail closed |
| K15-C-TESTS-001 | tested | `exactcert_tests.py`: verbosity invariance over 7 candidates, the review's `[2,-1]` case rejected in both modes, sign-preservation of the odd part, degenerate-input fail-closed, the `K21` counterexample and its witness, and 24 random candidates cross-checked against an independent SymPy oracle with no false acceptance. All pass |
| K15-C-ROUNDUP-001 | repaired | bounds are rendered from `4·PI_HI·p0/(3·q0)` by exact ceiling division (`delta_upper_decimal`), so the displayed value is an upper bound rather than a truncation of a float |
| K15-C-ODDDEG-001 / K15-C-STRICTLOSS-001 | retained | still correct and independent of the bug |

**What the review corrected that I had asserted wrongly.** (i) I reported `ok=true` while the
`reason` field said "A2: 10 simple root(s) of the odd part on the half-line" — the JSON
contradicted itself and I did not read it back. (ii) I displayed `0.78010544`, a truncation of
my own float, as a certified bound. (iii) I described the `K=9` disagreement between strict and
squarefree paths (`2.50596` vs `0.82276`) as evidence the strict test was "useless", when in
fact the squarefree verdict was itself unsound.

**Process change adopted.** The checker now has a regression suite that must pass before any
bound is reported, and `ok=true` with a non-null `reason` is impossible by construction.

**Deliberately not attempted in this block:** the strengthened 3D benchmark (shell-count
`<=12` to `rho = 2.09`, objective `(4*pi/3)(f(0)+12 eta)/fhat(0)`). Per the assignment the
checker repair takes precedence; the specification and handoff are in
`Computation/REQUESTS/K15-C-REQ-003.md` for the next block.

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

### 2026-11-14 01:22 Pacific — supervisor: actual Ultramath confirmed

Operational result, not a new mathematical claim. The explicit user request
triggered one new full-hour assignment in each owned session after checking
ownership, live history and prior prompt IDs. Existing completions triaged:
Main34587, Computation52418, Experimental41061, Counterexamples48644. The
Computation turn completed naturally before its new prompt; no busy turn was
interrupted. All four later model-call records report `reasoning_mode=ultramath`.

| Role | Delivered user message | Delivery sequence | Verified model-call sequence |
| --- | --- | --- | --- |
| Main | u-f9028ce9-bef1-4af4-9072-0e2151fa012d | 34589 | 39012 |
| Computation | u-df2e68fa-7592-4aa0-8647-c074ad101c7b | 52420 | 54459 |
| Experimental | u-79202358-2ba4-4eb6-887c-21de92cec54e | 41063 | 43870 |
| Counterexamples | u-616f57fc-f1e6-40a3-b5d1-251f112abbc9 | 48646 | 50313 |

Evidence and exact source hashes: `Main/ASSIGNMENTS_2026-11-14_0112.json`.
Prompts: `Main/Prompts/FullHour-2026-11-14_0112/`. All delivered prompt text
matches the saved files after newline normalization. Required elapsed work is
60 minutes per receipt, with useful fallbacks and checkpoints; full-hour
completion is not yet observed. Latest activity was ongoing in all four chats.

The 45-minute automation remains active and now explicitly verifies actual
Ultramath records and checks early completions. Sair-Watch remains stopped.
The documented API has no mode selector, so these sends used the official UI;
read-only verification used the official API and the existing protected key.
No new sessions, historical swarm restarts or new mathematical acceptance.

Fetched worker revisions contain further research claims pending review:
Main bbad129d, C50727f1d, E8aca235e, X237cc3bd. Main is assigned to reconcile
normalizations and source provenance; X independently audits C's new rational
control and E's directed enclosure; E continues the geometric compensation
problem; C implements a structured strengthened benchmark. The original failed
certificate and subsequent corrections remain retained. No new local heavy or
Lean job was launched by this operational checkpoint.

### 2026-11-14 01:38 Pacific - Main source synchronization

Imported Main revision 6626714125c35292d78943cd0fe8d18ec0051b38. Its full conflicting progress record is preserved in Main/AgentProgress/Main-66267141.md; all prior supervisor and worker records are retained. Research claims await the current review. K15-C029 has an invalid signed-subset summation step and is not accepted; Main has been assigned its correction.

### 2026-11-14 01:38 Pacific - Computation source synchronization

Imported revision 92def301dee4ac9445d60f3a233f77aca79f993f. Full conflicting worker progress retained in Main/AgentProgress/Computation-92def301.md. Existing supervisor and other worker histories are preserved. Imported claims remain subject to this checkpoint's independent review.

### 2026-11-14 01:38 Pacific - Experimental source synchronization

Imported revision 2f69047778590880124c9126de10741694285d02. Full conflicting worker progress retained in Main/AgentProgress/Experimental-2f690477.md. Existing supervisor and other worker histories are preserved. Imported claims remain subject to this checkpoint's independent review.

Supervisor sync 2026-11-14 01:38 PST: retained Main progress from 96419eaa2067ea7baedc4608215fa6b6d7c7b6a7 in KeplerConjecture/Main/AgentProgress/Main-96419eaa.md; review status is recorded in Main/REVIEW_2026-11-14_0138.md.

Supervisor sync 2026-11-14 01:38 PST: retained Computation progress from a13efc877eb3d22fc0a59176b1cdef4a74396557 in KeplerConjecture/Main/AgentProgress/Computation-a13efc87.md; review status is recorded in Main/REVIEW_2026-11-14_0138.md.

Supervisor sync 2026-11-14 01:38 PST: retained Main progress from 9461aae1d57b17f3497c60531e120d3807cf3e90 in KeplerConjecture/Main/AgentProgress/Main-9461aae1.md; review status is recorded in Main/REVIEW_2026-11-14_0138.md.

Supervisor sync 2026-11-14 01:38 PST: retained Computation progress from 447da323575b71d94a8997d882293ba4c82d52d5 in KeplerConjecture/Main/AgentProgress/Computation-447da323.md; review status is recorded in Main/REVIEW_2026-11-14_0138.md.

## Supervisor checkpoint: November 14, 01:38 Pacific

Main's C029 signed-subset proof was rejected and withdrawn. Exact local tests
found false accepts in Main's old checker, its first repair, and X's old
irrational-root predicate. Acceptance based only on those general checkers is
suspended; see Main/REVIEW_2026-11-14_0138.md for exact witnesses and scope.
The actual K33/K33b files passed Computation's strict and SymPy checks locally.
Tammes core arithmetic reproduced, with the primary theorem dependency explicit.
Finite shell, Barlow, transfer and cluster results are not universal certificates.
M-LEAN-002 reached local resource caps without theorem verification. All submitted
local batches for the frozen snapshots have finished; later work remains pending.

Four full-hour continuations were delivered in the existing Ultramath chats after
observed early completions; evidence-only steering did not reset busy assignments.
Every delivery ID, actual runtime observation, start and earliest finish is in
Main/ASSIGNMENTS_2026-11-14_0138.json. No full-hour completion or improved Kepler
result is claimed. Sair-Watch stays stopped; the 45-minute schedule continues.
Authored source history is retained through the full hashes in
Main/SYNC_2026-11-14_0138.json, including preserved conflicting progress snapshots.

Supervisor sync 2026-11-14 02:23 PST: retained Main progress from e76a15709c5907f76bbbf482755e916c71be76d4 in KeplerConjecture/Main/AgentProgress/Main-e76a1570.md; independent status is in Main/REVIEW_2026-11-14_0223.md.

Supervisor sync 2026-11-14 02:23 PST: retained Computation progress from dbeb320fb80be64799fc722174367ac61c387480 in KeplerConjecture/Main/AgentProgress/Computation-dbeb320f.md; independent status is in Main/REVIEW_2026-11-14_0223.md.

## Supervisor checkpoint: November 14, 02:23 Pacific

Merged all four frozen source checkpoints and Main's completed report 201974b,
preserving authorship and conflicting progress histories. Independently verified
X-C013's particular SOS/Fourier/rational bound below 0.794809295672; it is weaker
than K33b and known results. Main's current checker has another exact false accept:
q=(u-7/5)^2-2/10^40. Its general soundness and dependent Main-only verdicts remain
suspended. Exact witnesses and acceptance scope are in Main/REVIEW_2026-11-14_0223.md.

Ten local jobs finished. Geometric controls/search are finite and inconclusive;
the submitted SDP did not improve the bound. CubeDiff exceeded the monitored
1 GiB cap without theorem verification. The C035 constant and universal-cut
quantifiers remain pending. Full commands, versions, resource measurements and
logs are under Main/LocalChecks/2026-11-14_0223.

Main completion 58136 arrived after 45.573 minutes; a new full-hour assignment
was delivered at 10:35:02.848 UTC, earliest finish 11:35:02.848 UTC. The other
three owned chats remain on their existing assignments. Actual Ultramath calls
are verified for all four; no completed full hour is asserted. Prompt text and
delivery/mode evidence are in Main/ASSIGNMENTS_2026-11-14_0223.json. Main integrates,
Counterexamples reviews, and the 45-minute schedule continues without watchers.


Supervisor sync 2026-11-14 03:08 PST: Main source 7c56c5ee retained in Main/AgentProgress/Main-7c56c5ee.md; current independent review in Main/REVIEW_2026-11-14_0308.md.


Supervisor sync 2026-11-14 03:08 PST: Computation source 9d9ff682 retained in Main/AgentProgress/Computation-9d9ff682.md; current independent review in Main/REVIEW_2026-11-14_0308.md.


Supervisor sync 2026-11-14 03:08 PST: Experimental source 9a46efcb retained in Main/AgentProgress/Experimental-9a46efcb.md; current independent review in Main/REVIEW_2026-11-14_0308.md.


Supervisor sync 2026-11-14 03:08 PST: Main correction f1e4d8b4 retained in Main/AgentProgress/Main-f1e4d8b4.md; rejected and pending claims remain explicit in Main/REVIEW_2026-11-14_0308.md.


## Supervisor checkpoint: November 14, 03:08 Pacific

Merged completed sources Main 7c56c5ee, Computation 9d9ff682, Experimental
9a46efcb and Counterexamples 6535e768, plus Main's subsequent correction
f1e4d8b4. Original commits and conflicting progress snapshots are preserved.
C081's upper-to-lower deficit inference was rejected and Main withdrew it.
The replacement singleton floor and its per-fixture/universal quantifiers remain
under review. C079's arbitrary-cut boundary claim was narrowed.

Independent exact checking verifies X-C014 below 0.780718153344 and C's
both-sides Fourier/Gram identities below 2.0017173734. These are controls,
not new best bounds. Main's repaired checker passes the nine independent cases
and the 35-case suite; general soundness stays pending. All ten local jobs ended:
seven completed normally; three polish pilots hit 90-second caps. The rescaled
SDP pilot produced only weaker proposals. No new Lean result is accepted.

All four previous blocks fail the substantive-hour requirement: three early
endings and Experimental's 281 seconds of explicit sleep-padding. Four new
Ultramath assignments were delivered; Main ended again after 12.614 minutes,
so it received a longer self-contained proof package. Evidence steering does
not reset busy worker clocks. Exact delivery/runtime records and current
deadlines are in Main/ASSIGNMENTS_2026-11-14_0308.json; decisions and limitations
are in Main/REVIEW_2026-11-14_0308.md. The 45-minute cadence remains active and
Sair-Watch remains stopped.

Supervisor sync 2026-11-14 03:53 PST: Computation 4bcbd3a0 progress retained in Main/AgentProgress/Computation-4bcbd3a0.md. Fixture claims require corrections; see Main/REVIEW_2026-11-14_0353.md.

Supervisor sync 2026-11-14 03:53 PST: Computation 790efa73 progress retained in Main/AgentProgress/Computation-790efa73.md. Fixture claims require corrections; see Main/REVIEW_2026-11-14_0353.md.

## Supervisor checkpoint: November 14, 03:53 Pacific

K15-SUP-0353-01 independently verifies X-C015/016/017 from exact rational Gram
matrices and an independent Fourier recurrence; X-C017 gives density strictly
below 0.782267220134, weaker than known/project controls. The tested C fixture
has a false volume enclosure, premature ring edges, a broken FCC constructor
and unsaturated scope; exact threshold promotion is suspended (-02). Main
repaired the cut/flow draft after four objections; X reviews the precise
hypotheses (-03). Negative eta independently reproduces an old checker false
accept; the repaired 37-case suite passes, general soundness pending (-04).
Barlow proof, crack geometry and C5 numerical candidate retain independent
geometric obligations (-05). No new best bound, simpler proof or Lean result.

C/E/X completions 76816/92900 (plus stale-job 93074)/83471 were early at
49.738/47.894/41.969 minutes. Fresh full-hour tasks were delivered through the
website; actual model calls verify Ultramath. Main's existing hour continues
with evidence steering. Full delivery IDs, times, source hashes, local limits
and decisions are in Main/ASSIGNMENTS_2026-11-14_0353.json,
Main/SYNC_2026-11-14_0353.json and Main/REVIEW_2026-11-14_0353.md.
All local jobs ended; two searches reached caps. Watchers remain stopped.

## Supervisor checkpoint: November 14, 04:38 Pacific

Integrated Main 7ba7146, C 6fbd0a1, E 498cfc3 and X d64de36 with original
authorship. K15-SUP-0438-01 verifies the smaller rational Gram certificate
strictly below 0.782267254857. Named C input repairs pass (-02). X independently
reviews the repaired graph theorem, conditional on the geometric cuts (-03).
E's unsupported irremovable-excess claim is withdrawn; Barlow contact-cell and
C5 geometry scripts pass but floating filters prevent fully exact certification
from those runs alone (-04). Five local foreground jobs completed. Seven capped
local search seeds remain an explicit private task; no Lean build was requested.

Main completions 102385/102479 were deduplicated and a new full-hour website
assignment delivered, with actual Ultramath verified. C/E/X remained busy;
interim completions did not trigger duplicate assignments. Main received local
results at its next step without resetting its new hour. Exact IDs and times:
Main/ASSIGNMENTS_2026-11-14_0438.json. Detailed scope, sources and pending jobs:
Main/REVIEW_2026-11-14_0438.md. No new best bound or simpler Kepler proof accepted.

## Supervisor checkpoint: November 14, 05:23 Pacific

Merged M c4134c2, C a25f5be, E 93c61a8, X a35b713 with original authorship.
K15-SUP-0523-01 independently reproduces isolated-vertex and edgeless false
accepts in the flow checker; generic acceptance is suspended. The exact
FCC/HCP contact-polytope calculation passes (-02), and 52 half-line plus 50
interval checker vectors agree (-03, finite tests only). All eight bounded
local geometry pilots finished without refutation (-04). Main's C106-C108
pair bridge/compactness statements retain independent proof obligations (-05).
No new best bound, simpler Kepler proof or Lean result is accepted.

All four chats received one fresh full-hour assignment, and actual model calls
verify Ultramath. Earlier wall-clock spans do not establish 60 substantive
minutes. Prompt IDs, actual starts and earliest finishes are recorded in
Main/ASSIGNMENTS_2026-11-14_0523.json. Sources, rejected artifacts and limitations
are in Main/SYNC_2026-11-14_0523.json and Main/REVIEW_2026-11-14_0523.md.
All local jobs ended; 45-minute checks persist and watchers remain stopped.

## Supervisor checkpoint: November 14, 06:08 Pacific

Merged M 8dc264e, C bf7998c, E d289bef and X ee1848c with original authorship.
K15-SUP-0608-01 closes the named isolated/edgeless/negative-threshold flow
regressions: independent witnesses reject and 69 cases pass. Generic soundness
remains unproved. E's generic volume certification fails norm and boundedness
validation (-02); Main C112's certificate omits a constant term, selects the
opposite arcs and expands endpoints in the wrong direction (-03). Exact
witnesses and one reproduced volume-box output are saved; numerical agreement
does not validate either certificate. Broader geometric bridges, X's new
checker and face-count reductions remain pending (-04). No new best bound,
simpler proof or Lean result is accepted.

All four early completions received one fresh full-hour assignment. Actual
model calls verify Ultramath; Main also received evidence-only steering with
no clock reset. ASSIGNMENTS_2026-11-14_0608.json records exact IDs and timing.
All local jobs finished; the first box run's serialization failure and its
bounded successful retry are preserved. SYNC_2026-11-14_0608.json and
REVIEW_2026-11-14_0608.md record the sources, scope and next tasks. Checks stay
at 45 minutes; no watcher was launched or restarted.

## Supervisor checkpoint: November 14, 06:53 Pacific

Merged M 4dc1cc9, C 926cdb7, E e71a177, X 9577242 with original authorship.
K15-SUP-0653-01 records local reproduction of C's positive-deficit periodic
fixture and an independent exact legality/flow probe conditional on volume
data; the family scan hit 120 seconds and generic volume completeness remains
open. E's new origin-interior helper falsely accepts e1,e2,e3 (-02); its mesh
radius is still not rigorously bounded. Main's degree-12 and face-monotonicity
premises fail (-03); boundary and asymptotic-limit details remain open. The
repaired axial twist argument does not supply all-orientation near-contact
geometry (-04). No new best bound, simpler Kepler proof or Lean result accepted.

M/E ended at 20.504/40.461 elapsed minutes; fresh full-hour tasks and actual
Ultramath calls are recorded in ASSIGNMENTS_2026-11-14_0653.json. X received
evidence without a clock reset; C stayed busy without duplicate assignment.
Its heavy VM scan violates the standing offload instruction and is recorded
for the next review. All local jobs stopped. Source hashes and limits are in
SYNC_2026-11-14_0653.json and REVIEW_2026-11-14_0653.md. Watchers remain stopped.

## Supervisor checkpoint: November 14, 07:38 Pacific

Merged M 2c41311, C 2d6d640, E 6ae7dbf and X 8677a02 with authorship retained.
K15-SUP-0738-01 records local origin/radius repairs and a new exact duplicate-face
overcount (cube 8 becomes 28/3). The 12-face premise has an identified primary
source (-02), but the ring-excess proof remains open. Main's covering-radius
exclusion is pending review; its finite-ball inequality is still reversed (-03).
Face-class minima and generic rational-volume completeness remain unresolved
(-04). No new best bound, simpler proof or Lean result accepted.

All four completed early; one new full-hour assignment per owned session is
delivered and runtime-verified Ultramath. IDs, actual starts, earliest finishes
and previous duration audit are in Main/ASSIGNMENTS_2026-11-14_0738.json. Both
local jobs finished; the inconsistent/redundant premise scan is deferred with
its reason. See Main/REVIEW_2026-11-14_0738.md and SYNC_2026-11-14_0738.json.
The next review remains on the 45-minute schedule; watchers remain stopped.

## Supervisor checkpoint: November 14, 08:23 Pacific

Merged completed M 89a9c54 and E 814f213, plus busy C fbb124e and X c40fdcb
captured at review start. Main's colliding authored review is preserved exactly
under Main/AgentReports; all author commits are retained. K15-SUP-0823-01 closes
the named E duplicate-plane regression on local controls. C's 25 tests and
stored signed-volume reproduction pass, but two independent exact witnesses
break its standalone verifier (-02). Main corrects the old inequality and
minimum inference; its stability candidate and missing executable request
remain conditional/needs implementation (-03). X's one-cell weakening is false;
geometric scope and ring-face proof remain under audit (-04).

M/E ended early (43.812/21.538 minutes) and received new full-hour assignments.
C/X continued; C received next-step evidence without a clock reset. All new
deliveries and actual Ultramath calls are confirmed in Main/ASSIGNMENTS_2026-11-14_0823.json.
All four local jobs finished. No new best bound, simpler proof or Lean result
accepted. See Main/REVIEW_2026-11-14_0823.md and SYNC_2026-11-14_0823.json.
Checks stay every 45 minutes; no watcher started or resumed.
