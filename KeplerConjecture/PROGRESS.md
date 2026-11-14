# KeplerConjecture progress

## Current state

| Item | Status | Evidence | Next owner |
| --- | --- | --- | --- |
| Problem 15 roadmap | Frozen research plan | `ROADMAP.md`, `Literature/PROBLEM_SPEC.md` | Main |
| Mathematical contract | Frozen; conversion rules recorded | `Main/CLAIMS.md` K15-C001, K15-C007 | Main |
| Claim ledger, decision record, task board | Created | `Main/CLAIMS.md`, `Main/DECISIONS.md`, `Main/TASKS.md` | Main |
| Recovered pre-setup notes | Recovered to Git, `PENDING_REVIEW` | `Literature/RECOVERED.md` (6 files, checksums) | X |
| Two-point bound for all packings | Proof written, Main-audited, awaiting X | `Main/RESULTS.md` §1, K15-C002 | X |
| Truncated/hybrid bound with a count price | Proof written, awaiting X | K15-C003 (`smwg019eu` m2 §2) | X |
| Additive CE+Voronoi hybrids | Obstructed (cannot beat 5.550291) | K15-C005, `m1/verify.py` | X to confirm |
| Contact-sphere relaxation | Refuted as stated, repaired | K15-C004, K15-C011 | X |
| Frontier anchor below 0.770271 | Fixed at 0.754697399337 | K15-C008 | X to confirm no better exists |
| Numerical baseline | Not reproduced locally | `Main/LOCAL_COMPUTE_REQUESTS.md` K15-COMPUTE-001 | C and Astra |
| Lean definitions module | Drafted and pre-checked on Lean 4.33.1 | `Lean/Kepler15/Normalisation.lean` | Astra (pinned 4.35.0) |

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

### K15-MAIN-002 — 2026-11-14, America/Los_Angeles — Main checkpoint 1

Author **M (Main)**, session `based-on-the-chats-e0wz`. Independent reviewer for
every mathematical claim below is **X** (`i-ve-attached-viazovska-f7hh`);
nothing is marked `PROVED` on Main's reading alone. Branch `kepler15/main`,
based on setup commit `69f3213aa6f2b636ec1b0e25a7394acfecae986b`.

Recovered and committed six unpushed pre-setup artifacts verbatim, with
SHA-256 checksums (`Literature/RECOVERED.md`). Two of the checksums match the
supervisor's archived copies in `Literature/PRIOR_WORK.md` exactly, which fixes
their provenance. All six are `PENDING_REVIEW`.

Created `Main/CLAIMS.md` (K15-C001…C012 plus K15-R001…R005 for recovered
material), `Main/DECISIONS.md` (D1–D9), `Main/TASKS.md` (T1–T10) and
`Main/RESULTS.md`.

Audited the two recovered swarms read-only; they were interrupted by a VM
restart and were not resumed, per instruction. Re-ran both verifiers in
`smwg019eu` from their own directories: `m1/verify.py` reports 30/30 checks
passing (dodecahedral constant, icosahedral cell, fcc/bcc/Z³ face counts,
admissible `f` family, obstruction items H1–H4); `m2/verify.py` reports 41/41
(benchmark constants, thresholds, truncation-price ratios). Findings:

* The two-point bound's missing step — periodic packings are dense in all
  packings — now has a written proof with explicit losses `O(S/R)+O(1/S)`
  (K15-C002). This is a clarity contribution, not a new constant.
* A truncated/hybrid bound with a **local count** price is proved and strictly
  generalises it (K15-C003). The integral-tail interface proposed in the earlier
  brief is not locally certifiable; the local route loses a factor 1.3505 and a
  refutation of the integral form must beat the two-point optimum by 5.30%.
* Correction to Main's own earlier brief: for `k > 1` translates the Poisson
  phases do **not** obstruct the argument; they combine into
  `|sum_j e^{2pi i <v_j,t>}|^2 >= 0` (K15-C009, `REFUTED` as written before).
* Correction to the recovered Theorem B's corollary: "empty interior" must read
  "closed with empty interior", otherwise a dense `A` is a counterexample
  (K15-C004 `REFUTED`, K15-C011 repaired).
* Obstruction kept: additive two-point corrections to Voronoi volume cannot
  beat `V_HM = 5.550291028515510` (K15-C005), so that hybrid family is closed.

Drafted `Lean/Kepler15/Normalisation.lean`: frozen objects (`IsPacking`,
`localDensity`, `upperDensity`, `centreDensity`, `volB1`, `countIn`,
`HasContactNumber`) and `centreDensity_eq : centreDensity Λ = 3*upperDensity Λ/(4*pi)`.
Elaborated on the VM with Lean 4.33.1 (exit 0, no diagnostics);
`#print axioms` returns exactly `[propext, Classical.choice, Quot.sound]`. This
is a **pre-check only**: the pinned build under Lean/Mathlib v4.35.0 is request
`K15-COMPUTE-002` and the module stays `LEAN_CONDITIONAL` until it runs.

Submitted two local requests: `K15-COMPUTE-001` (certified two-point LP in the
Laguerre basis, degrees 12–40) and `K15-COMPUTE-002` (pinned Lean build).

Not done: no new numerical bound; CDS22 Table 1.1 has not been reproduced
locally; Li's 0.18398089 is quoted, not reproduced; X's reviews are outstanding.
Next: X audits K15-C002/C003/C005 and Li's scope; C runs 001; E answers whether a
tolerance kissing bound with `n < 26` exists for shells of width below 0.0366.
