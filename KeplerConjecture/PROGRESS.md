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
| Grid-sampled CE values | Grid LP claim **withdrawn** (omitted Fourier positivity); grids exploratory only | K15-C014r | C |
| Cluster-averaged local criterion | Lead local route, `PROPOSED` | K15-C015 (E's `K15-E001`) | E, X |
| Exact Sturm certification | Adopted as the acceptance test | K15-C016, X-C008, D10 | C |
| CE controls | `TESTED_FINITE`: 0.7797024 (K=31), 0.7797458 (K=41) | `Computation/RESULTS_baseline.md` (C) | C |
| Numerical baseline | Not reproduced locally | `Main/LOCAL_COMPUTE_REQUESTS.md` K15-COMPUTE-001 | C and Astra |
| Lean normalisation module | **COMPLETE locally**: pinned Lean 4.35.0, exit 0, axioms `[propext, Classical.choice, Quot.sound]`. Algebraic identity only — no ball-volume or counting bridge | `Lean/Kepler15/Normalisation.lean` | — |

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

### K15-MAIN-004 — 2026-11-14, America/Los_Angeles — review 27616 repair

Author **M (Main)**, source revision reviewed `a08f378be6a03f80ac075b34f8ba99aeb8201d9e`.
Independent review: Astra, a mathematical audit agent and local execution. All
findings accepted; none contested. No chat was created and no swarm touched.

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

### K15-MAIN-006 — 2026-11-14 — continuous block: shell count reduced, checker written

Author **M (Main)**. Read: supervisor `ec2596dce67a4c6a93157d291c2f8e2e58f5cfc3`,
Computation `8bb50f85…`, Experimental `96fbf9bb…`, Counterexamples `3831361a…`,
`Main/LocalChecks/2026-11-14_0008/` and `Main/HOURLY_REVIEW_2026-11-14_0008.md`.
No chat created; no swarm; no heavy computation (one 1.3 s symbolic self-test).

* **K15-C019 `PROVED`**: the shell count is a single Tammes-13 inequality. If
  `2 ≤ |y_i| ≤ ρ` and `|y_i−y_j| ≥ 2` for 13 points, their directions are
  separated by `≥ arccos(1 − 2/ρ²)` (monotonicity of
  `(a²+b²−4)/(2ab)` on `[2,ρ]²`). Table: `ρ = 2.02/2.05/2.09` leaves
  `2.21°/1.26°/0.034°` margin over `θ₁₃`. Attainment of 12 by the icosahedral
  twelve recorded. Tammes value cited, not proved.
* **K15-C020 `PROPOSED` (pipeline)**: E encloses `θ₁₃` → M applies C019 with
  rational thresholds `12 ≤ 4π`, `27/2 ≤ πρ²` → C optimises → anyone verifies with
  the new checker. Honest calibration: the realistic target is the first certified
  number and at best `0.770271`; it is not a route past `0.754697` (DLOV14's whole
  gain is `0.0067` in `δ`, the gap to the dodecahedral bound is `0.025`).
* **New artifact `Computation/shell_check.py`** (exact checker, runnable):
  rational monomial basis `u = π|x|²`, rational Fourier map verified against the
  Hermite–Laguerre eigen-relation, exact Sturm verdicts for `q ≥ 0` on `u ≥ 0`,
  `p ≤ η` on `[12, 27/2]`, `p ≤ 0` on `[27/2, ∞)`, directed-`π` output interval,
  failure reporting unconditional (D13), and a self-test that *rejects* a
  deliberately bad profile. Reproduce: `python3
  KeplerConjecture/Computation/shell_check.py --self-test`.
* **K15-C021**: recorded checker defects — `kepler_ok` truncates positive
  rationals (`99/100` case returns true though `19602/625 > π³`); X's
  pair-average and existential-partition arguments remain wrong and are not
  imported; E's Tammes script is floating arithmetic with a reusable exact
  endpoint; C's regressions pass but `shell_bench.py` is unwritten.
* `D15` fixes `ρ = 2.05` as the first width to certify; `D16` makes
  `shell_check.py` the acceptance test for shell-allowance candidates.

Gaps: no Tammes enclosure yet (E), no candidate profile yet (C), so no bound. Next:
E encloses `θ₁₃` at `ρ = 2.05`; C runs the optimisation at `η = 0` versus small
`η` in the checker's format; X audits `shell_check.py`.
