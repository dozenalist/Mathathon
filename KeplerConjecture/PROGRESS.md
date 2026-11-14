# KeplerConjecture progress

## Current state

| Item | Status | Evidence | Next owner |
| --- | --- | --- | --- |
| Problem 15 roadmap | Frozen research plan | `ROADMAP.md`, `Literature/PROBLEM_SPEC.md` | Main |
| Mathematical contract | Frozen; conversion rules recorded | `Main/CLAIMS.md` K15-C001, K15-C007 | Main |
| Claim ledger, decision record, task board | Created; revised after review | `Main/CLAIMS.md`, `Main/DECISIONS.md`, `Main/TASKS.md` | Main |
| Independent review of checkpoint 1 | 10 objections, all answered | `Main/CLAIMS.md` "Correction log" | X |
| Recovered pre-setup notes | Recovered to Git, `PENDING_REVIEW` | `Literature/RECOVERED.md` (6 files, checksums) | X |
| Two-point bound for all packings | Proof written, Main-audited, awaiting X | `Main/RESULTS.md` §1, K15-C002 | X |
| Truncated/hybrid bound with a count price | Proof written, awaiting X | K15-C003 (`smwg019eu` m2 §2) | X |
| Additive CE+Voronoi hybrids | **Obstruction withdrawn, route re-opened** | K15-C005 | unowned |
| Contact-sphere relaxation | Closed (proof restored after Main's error) | K15-C004 | X |
| Frontier anchor | 0.754697399337; Rogers 0.779636 < CE 0.779747 (order fixed) | K15-C008, `Main/RESULTS.md` §4 | X |
| Counting envelope for shells | Upper bound proved; exact 12 for thin shells proved; explicit width open | K15-C013 | E / X |
| Grid-sampled CE values | Closed (LP unbounded below) | K15-C014, `Computation/ce_laguerre.py` | C |
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

### K15-MAIN-003 — 2026-11-14, America/Los_Angeles — review repair checkpoint

Author **M (Main)**, session `based-on-the-chats-e0wz`. Source revision of the
reviewed checkpoint: `c91007ff11844f179921fadfb2e90d352b8c0090`. Independent
review: Astra plus a separate mathematical audit (10 required corrections). Every
objection is accepted; dispositions are tabulated in `Main/CLAIMS.md`
("Correction log"). No worker chat was created or contacted: this environment
exposes no delegation tool that reaches the other three assigned sessions
without starting a new one, so this block is a coordinator synthesis plus the
mathematical repairs that did not need a worker (see "Blocked" below).

Corrections made at source, with the old versions quoted in place:

* **K15-C004 restored.** Main's checkpoint-1 "counterexample" `A = Q³∩{|x|≥2}`
  was wrong: the complement of a set with empty interior is dense, which is the
  hypothesis the proof needs. **K15-C011 withdrawn** (the closedness repair was
  unnecessary). The contact-shell route stays closed for the right reason.
* **K15-C005 obstruction withdrawn.** The inequality had been read backwards:
  `V_0 ≤ vol Ω(v) + κB_κ(v)`, so a positive correction at the icosahedral cell
  permits a *larger* `V_0`. The two raw sign computations stand; the exclusion
  does not. **D6 re-opened.**
* **K15-C010 refuted as stated.** Finitely many prescribed zeros impose no
  bandwidth bound (`f = g·∏(|x|²−r_j²)` with `supp ĝ` arbitrarily small). The
  repaired form keeps the `log(‖f̂‖₁/f(0))` term, which checkpoint 1 dropped.
* **K15-C002 restated** with continuity of `f` and `f̂` and the separate
  hypothesis `f̂(0) > 0`.
* **K15-C013 added**: the counting envelope `n ≤ ⌊(3+δ)³⌋−1` is an *upper*
  bound (checkpoint 1 said lower), and the exact value is 12 for all
  sufficiently thin shells (compactness + kissing number); an explicit width is
  open.
* **K15-C014 added** (negative result): the submitted grid-discretised CE LP is
  unbounded below, and with the rigorous floor `f(0) ≥ 3/(32π)` it attains the
  floor with fine-grid violations of order `10¹⁰`. Grid sampling cannot produce a
  CE value; the SOS identity is mandatory.
* **RESULTS.md** ordering fixed (`Rogers 0.779636 < CE 0.779747`), novelty
  language removed, `n ≥ 26` corrected.
* **LOCAL_COMPUTE-001 rev. 2**: `s = |x|² ≥ 4`, `t = 2πs ≥ 8π` (not 4); exact
  rational SOS identity required; no implied convergence to Li's `0.18398089`.
* **Evidence exported** to `Main/Evidence/` (5 swarm files + outputs, hashes in
  `MANIFEST.txt`); `Computation/ce_laguerre.py` is runnable (sha256
  `b17badb…`) with measured runtime 1.1 s.

Run on the VM this block: `python3 Computation/ce_laguerre.py --degree 8
--grid 1200 --tmax 40` (1.1 s, exploratory, negative result), both swarm
verifiers re-run earlier in the cycle (30/30 and 41/41). Not run: the pinned Lean
build (request `K15-COMPUTE-002`, unchanged; the module's only edit since the
Lean 4.33.1 pre-check is a docstring). The unit-ball volume identity is **not**
proved in `Normalisation.lean` and the file says so.

Blocked / not done: no worker contact (no delegation tool reaching the three
other sessions without creating a chat); no independent review of the repaired
statements yet; no certified CE value; no new bound. Next assignment: X audits
K15-C002/C003/C004/C013 and the K15-C005 withdrawal; E takes the two candidate
mechanisms (local counting with an explicit width, and a strengthened analytic
route) with the count-price theorem as the interface; C implements the exact SOS
identity of request rev. 2 for `n ≤ 12`.
