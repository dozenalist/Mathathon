# Rogers--Ramanujan / SAIR problem 127: progress

## November 13, 2026 PST — publication and synchronization review

The current synthesis is [Main/RESULTS.md](Main/RESULTS.md); older entries below
are historical checkpoints. Imported cycle-4 SAIR commit
`d8684a9384edc52e5960733a4f92bf8c207083db`, preserving its corrections and
honest remaining proof gaps. The supervisor reproduced all 13 regression
checks, the independent checker through weight 20, and the Lean 4.35.0 named
build. The saved n<=50 endpoint census contains 1,065 objects at weight 50;
its separate signed-state census stops at 25. Corrected stale current tables
and family boundary text. No new full bijection or all-input phi proof is claimed.

This publication brings the project checkpoint and current summary onto the
GitHub `main` branch and retains `rr127/main` for research. SAIR must synchronize
against the confirmed public commit; the final supervisor response records the
verified publication/synchronization outcome. No additional worker round is
launched by this documentation and repository-sync request.

## 2026-11-13 23:10 PST / supervisor review of completions 26480–31032

This current review supersedes incompatible status tables below. Imported and
verified cycle-3 tip `980e4cdcc4e91c79977697f127ef48252c0f15e5`; all four SAIR
workers are reported collected. The integrated `ShiftT.lean` source passes the
named `lake build RogersRamanujan` target on Lean 4.35.0, six jobs, exit 0.
Its two subtype inverse laws and weight preservation prove the known D/B shift
with permitted axioms; they do not prove the full A/D bijection.

Repaired the fast psi regression to require success for every in-domain state:
all eleven checks pass, including phi and psi on 3,198 states each at weight
<=18. Repaired MX.3's incorrect all-integer monotonicity argument. Independently
reproduced `(4^3,1^62)`: B endpoint `(25,17,8,8,8,8)`, D image
`(30,20,9,7,5,3)`, inverse correct, 1,910 edges / 1,911 trace states. Main's
rejection of the B endpoint and five-step report were mistaken. RR-C021 remains
TESTED_FINITE until its all-input proof is available; C020's endpoint scope and
family boundary table need repair. See `Main/SUPERVISOR_REVIEW_26480.md`.

At 23:08:52 PST the supervisor sent a detailed 90-minute continuation to the
same assigned coordinator; history confirms sequence 31033. The new block
prioritizes the phi slot and branch proof, a stable family formula and inverse,
independent adversarial checking, and the conditional finite alternating-path
theorem. RR-C012 remains OPEN. The exact target watcher remains active. This
checkpoint and the dated ChatLogs report are being published to `rr127/main`;
the supervisor's final response records confirmed push status.

## 2026-11-13 22:25 PST / supervisor review of completion 19046

The cycle-2 export was retrieved and its bundle verified. Python checks and the
independent endpoint checker pass at `n=30`. The exported named Lean build fails
because its glob requests a nonexistent module; removing that glob makes
`lake build RogersRamanujan` pass on Lean 4.35.0 (22:28 PST, exit 0). The exported phi skeleton checker crashes and is not
accepted evidence. RR-M004 remains finite evidence: the all-input obligation
is not closed by that census. A proposed case proof is supplied for independent
review in [Main/SUPERVISOR_REVIEW_19046.md](Main/SUPERVISOR_REVIEW_19046.md),
along with exact commands, remaining gaps and corrections. Swarm `smwg03n61`
still needs its completed reports collected. The older current-state table
below is a historical cycle-1 snapshot pending Main's reconciliation.

## Current state (2026-11-14, America/Los_Angeles; cycle 3)

| Area | State | Next action |
| --- | --- | --- |
| Target | Official formulation unchanged; a more natural first-identity bijection | Objective **OPEN**; do not claim it |
| Coordination | Swarm `smwg03n61` closed 4/4 accepted; swarm `smwg1kdjq` running for cycle 3 | Collect and review; no duplicate swarms |
| Literature | BZ82 read in full (pp.313-315); GM81a/GM81b still abstract-only | Locate full GM81b or record the access limit precisely |
| Computation | Six-method counts; BZ82 map verified `n <= 50`; secondary implementation agrees on every object | Fast regression script; repair `phi_skeleton.py` |
| Counterexamples | Independent checker PASS `n=30`; 7 registry entries | Audit the `phi` inverse branches |
| Experimental | Theorems F/G closed forms on two rays; the `s=0 (5)` two-step obstruction | A valid two-parameter family with >1 object per weight |
| Lean | Staircase **equivalence** (order proved); named target `lake build RogersRamanujan` passes for the six base declarations | Formalize `T`; rebuild target with new modules |
| Main result | Baseline proved and audited; `psi` proved all `n`; first new subfamily theorems | `phi` inverse branches remain the blocker |

## Status at a glance (reconciled, cycle 3)

**PROVED:** RR-C003 (length not preservable), RR-C004 (largest part not
preservable for all `n>=2`), RR-C008 (BZ82 `psi` involutive for all `n`, amended
argument, independently audited, empty gap list, tie-breaks forced),
RR-C010 (cutoff witness), RR-C013 (Theorem F, all-ones ray closed form),
RR-C014 (Theorem G, all-fours ray), RR-C015 (`>2` step lower bound for
`s = 5k, k >= 6`), RR-C017 (Case-I deletion trap, by witness), and **MX**
(`Main/LEMMA_MAXEXIST.md`: the Case-II maximum exists on every state, is
non-negative exactly on `phi`'s domain, and `a = mu` is impossible in Case I).

**LEAN_VERIFIED:** RR-C005 staircase equivalence — order statement proved and
non-vacuous; base module compiled on pinned Lean 4.35.0 by the supervisor, named
target `lake build RogersRamanujan` exit 0 at `731b457`. The order module has
been compiled on 4.33.1 (Main) and on **4.35.0 by the supervisor** for the bytes
`5EFBAF6A...0AAA829E`.

**TESTED_FINITE:** RR-C002 (counts `n<=50`), RR-C006 (`T`), RR-C007 (the map,
`n<=50`; BZ82's theorem is PROVED in the literature and attributed), RR-C009
(`phi`, `n<=30`), RR-C011 (path lengths, raw data only).

**RETRACTED:** RR-X005 (my claim that BZ82's `phi` Case II formula is defective).

**OPEN:** RR-C012 (the Mathathon objective), RR-C016 (mechanisms M1/M2).

**Superseded statements, kept rather than deleted:** "six independent counting
methods" (cycle 1) -> corrected grouping in RR-C002; "`Theta(n)` empirically" and
"roughly linearly" (cycle 1) -> raw data in RR-C011; "the `z >= 0` lower bound is
part of the printed rule" (cycle 2) -> MX.3, where the lower bound is a
*consequence* on the domain; "the maximum fails to exist off the domain" ->
MX.3(3), where it exists and is negative; "path length `<= 6` throughout `s<=60`"
(cycle 2) -> corrected to the four derived classes; both extremizers in
`(4^r,1^s)` -> only the `n=30` one; `(5^k)` as a residue family -> it is not in
`A_n`; `-13`/`-10` numerical repair (cycle 1) -> the amended boundary arguments
in `AMENDED_PROOF.md`; toolchain-mismatch and missing-build-target statuses
(cycle 1) -> resolved by the supervisor's pinned build.

**Dates:** the cycle-2 review was **November 13, 2026, ~22:25 PST** (the UTC date
was already November 14, which is why earlier entries disagree). Entries below
keep their original stamps; this table is the current view.

## 2026-11-14 / RR-M001 / checkpoint 1: contract, BZ82 reference map, staircase in Lean

- **Agent and reviewer:** M (Main, coordinator); X-role review is
  `Counterexamples/checker.py`; worker reports refereed by M.
- **Status:** PROVED for RR-C003/004/008/010; LEAN_VERIFIED for RR-C005;
  TESTED_FINITE for RR-C002/006/007/009/011. The official objective (RR-C012) is
  **OPEN**; nothing here is presented as a natural bijection.
- **Statement and hypotheses:** see `Main/CLAIMS.md`. In one line: the BZ82 1982
  reference map now runs in both directions with a stated inverse, verified on
  every object for `0 <= n <= 50`; the staircase reduction is kernel-checked;
  and two candidate design requirements (preserve length, preserve largest part)
  are refuted for all `n`.
- **Evidence/artifacts:** `Main/CLAIMS.md`, `Main/DECISIONS.md`,
  `Main/RESULTS.md`, `Computation/{rr_core,bz82,run_checks}.py`,
  `Computation/results.json`, `Counterexamples/{checker.py,REGISTRY.md}`,
  `Lean/Staircase.lean`, `Lean/README.md`. Sources: BZ82 (full scan, pp.313-315),
  BP06 and PAK06 as read in the preparation bundle.
- **Source work:** retrieved and read the complete BZ82 scan
  (`https://sites.math.rutgers.edu/~zeilberg/mamarimY/rrDG.pdf`,
  sha256 `403543088ed9465bc8e3f9918defd22a57c86a21493226c9852729af614483c6`).
  All three printed examples on p.315 reproduce exactly, including the nine-state
  chain of example (3). One printed rule is underdetermined; the reconstruction
  and its justification are `Main/DECISIONS.md` D-3.
- **Reproduction commands:**
  `python3 RogersRamanujan/Computation/run_checks.py 30` -> 4.3 s, all checks true.
  `python3 RogersRamanujan/Computation/run_checks.py 50` -> 257 s, bijection
  verified through weight 50.
  `python3 RogersRamanujan/Counterexamples/checker.py 30` -> PASS, 0 fails.
  `lean RogersRamanujan/Lean/Staircase.lean` -> exit 0, ~14 s.
- **Environment:** Python 3.12.14 (stdlib only). `lean --version` = **4.33.1**,
  which does **not** match the pinned `v4.35.0`; `import Mathlib` could not be
  elaborated on this VM (measured thrash on the 6.4 GB olean import), so the Lean
  module is Mathlib-free and **no `lake build` is claimed**.
- **What this establishes:** a reviewable foundation and two closed routes.
- **What remains unproved/untested:** all-n termination of the BZ82 iteration;
  the `phi` involution for all `n`; the `T`/`Nat.Partition` Lean bridge; and the
  actual objective.
- **Worker reports (swarm `smwfxwsqf`, all 4 accepted):** m1 counts (independent
  reproduction, identical table); m2 largest-part obstruction (reproduced by M,
  promoted to an all-`n` proof); m3 `psi` involution (all-`n` written argument,
  refereed and promoted to PROVED); m4 level-splitting reformulation with three
  refuted candidate level rules.
- **Next action / owner / dependency:** R2 on the residue side: can residue
  multiplicities determine the level `k` and the residual partition without a
  global search? Owner: next Experimental specialist, with Main. Dependency:
  `T` formalized, and GM81b text for a fair naturalness comparison.

## 2026-11-13 / PREP-001 / research preparation

- **Agent:** Codex, preparing the Ultramath handoff.
- **Status:** DOCUMENTED (planning/literature work, not mathematical discovery).
- **Base commit:** `e511044`; repository was clean before this preparation.
- **Evidence:** [ROADMAP](ROADMAP.md), [problem specification](Literature/PROBLEM_SPEC.md),
  [reading notes](Literature/READING_NOTES.md), [catalog](Literature/sources.json),
  [bibliography](Literature/references.bib), and [Hexagon review](Literature/HEXAGON_REVIEW.md).
- **Source checks:** Read the official problem in the SAIR interface. Read relevant
  sections of the accessible classical/modern sources; cards distinguish these
  from abstract-only access. Examined the BZ82 first-page scan to confirm the
  intermediate-family transformation. Inspected the local Lean/mathlib v4.35.0
  partition API and root build configuration.
- **Hexagon:** Public metadata searches returned 0 matches for `Rogers`, 7 for
  `Ramanujan`, 0 for `partition bijection`, 10 for `biject`, and 38 for
  `partition`. All returned pages were complete for those queries. A separate
  web full-text search located the relevant Riordan-paths preprint. Its TeX
  source was saved unchanged and its SHA-256 matched the source manifest.
- **Scope:** The Hexagon paper is adjacent work, not a solution of problem 127.
  No claim of an exhaustive worldwide literature search is made. Full-text
  access to the two 1981 competition references remains limited as described
  in the notes; their bibliographic records and abstracts were read.
- **Next:** Main starts P0; C and X build independent checks; L formalizes the
  intermediate bridge; E proposes a bounded set of mechanisms.
- **Documentation validation:** parsed both JSON files, matched all 11 source
  IDs to BibTeX entries, checked 28 local Markdown links, and verified the
  preserved source hash. A temporary independent enumeration also checked the
  small fixtures and the roadmap's staircase/shift formulas through weight 30
  (893 gap partitions); these are finite sanity checks of standard formulas,
  not a new bijection or an all-weight proof. No Lean build is claimed.

## Entry template

Append major findings; retain failed or superseded claims with their scope.
Workers append entries on their own branches; Main merges them and updates the
current-state table. Push at major milestones and at least every 30--60 minutes
of active work, as specified in ROADMAP.

```text
## YYYY-MM-DD HH:MM TZ / RR-<role><number> / short finding
- Agent and reviewer:
- Status: PROPOSED | TESTED_FINITE | PROVED | LEAN_VERIFIED | REFUTED | BLOCKED
- Statement and hypotheses:
- Evidence/artifacts and source IDs:
- Commit or run ID:
- Reproduction command, environment, seed, exact bounds:
- What this establishes:
- What remains unproved or untested:
- Next action / owner / dependency:
- GitHub checkpoint: branch and successful push, or explicit failure:
```

## 2026-11-14 / RR-M001-PUSH / checkpoint 1 push status: FAILED (credentials)

- **Status:** BLOCKED for upload; the mathematical work is complete and committed.
- **Local commit:** `c007d4d3e84cae69fc6627f212520db536449105` on local branch
  `rr127/main`, branched from the assigned base `79df0e4`.
- **Base check:** the remote HEAD at assignment time was `79df0e4`; the fetched
  remote still reports `79df0e4`, so the branch is a fast-forward of the remote
  `main` and needs no rebase.
- **Exact failure:**
  `git push -u origin rr127/main` ->
  `remote: No anonymous write access.`
  `fatal: Authentication failed for 'https://github.com/dozenalist/Mathathon/'`
- **Cause:** this environment has anonymous read access to the public repository
  (clone and `git ls-remote` succeed) and no write credential. The platform's
  connected-GitHub service is **not** connected for this project:
  `github_status` returns `github_not_connected: Connect a GitHub repository in
  project settings.` No support for asking for a token or SSH key exists here,
  and none was requested.
- **To unblock (human action, one of):** connect the repository in project
  settings, or push the commit manually:
  `git push origin refs/heads/rr127/main:refs/heads/rr127/main`.
- **Nothing is lost:** all artifacts are in the working tree and in
  `c007d4d`, which is a fast-forward of `origin/main`; the branch is ready to be
  pushed or to become a pull request unchanged.

## 2026-11-14 / RR-M002 / tie-breaks proved forced; worker statement correction

- **Agent and reviewer:** M, reviewing the full text of the four accepted worker
  reports (the first checkpoint had only their summaries).
- **Status:** strengthens RR-C008 (still PROVED); new REFUTED entry RR-X006.
- **Statement:** flipping any of the three `psi` tie-breaks in DECISIONS D-3
  destroys the involution: 1120 failures for equality-to-I(b) (first witness
  `n=4`, `(0;(2,2))`), 374 for equality-to-II(b) and 374 for keeping a created
  part 0 (both first at `n=3`, `(-1;())`), against 0 for the chosen reading,
  over all 3198 in-domain states of weight `<= 18`. Verified by Main by patching
  `bz82.py` directly; worker m3 reported the same witnesses independently.
- **Correction recorded:** the task question "does every orbit reach
  `{0} x A_n`?" is mis-posed; orbits of an involution are 2-cycles and the
  correct statement is `X(n) = ({0} x A_n)` disjoint-union 2-cycles. Caught by
  m3, adopted in CLAIMS and DECISIONS D-3a.
- **Reproduction:** `python3 RogersRamanujan/Computation/run_checks.py 30`
  (0 failures on the chosen reading); the flipped readings are recorded as a
  table in `Counterexamples/REGISTRY.md` RR-X006.
- **Not changed:** no claim is promoted by this entry; it removes the main
  soft spot in D-3 rather than adding a new result.
- **GitHub checkpoint:** committed locally; push still blocked (see RR-M001-PUSH).

## 2026-11-14 05:5x America/Los_Angeles / RR-M003 / cycle-2 checkpoint: source-faithful BZ82, retraction of RR-X005

- **Author / reviewer:** Main; independent review by the supervisor (externally
  re-ran `run_checks.py 30` and compiled the Lean file with the pinned toolchain)
  and by the cycle-2 worker swarm `smwg03n61`.
- **Status:** RR-C009 stays TESTED_FINITE but is upgraded in *kind* (faithful
  transcription, no reconstruction); RR-C005 LEAN_VERIFIED on the pinned
  compiler with reduced scope; RR-C008 PROVED with an amended argument, under
  audit; **RR-X005 RETRACTED**.
- **Retraction (the important item).** Checkpoint 1 claimed BZ82 p.314's `phi`
  Case II formula is defective. That was my error: I had silently imposed
  `z >= 1` on the printed range `0 <= z <= a+2j-2`. With the printed range the
  rule is complete — 0 defects in `phi(phi(s)) = s` over 66 658 in-domain states
  of weight `<= 30`, admissible set nonempty on all 10 285 Case-II states of
  weight `<= 25`, and the alleged counterexample `(0;(2,1,1,1))` is correctly
  mapped to `(-1;(1,1))` by `z = 0`. My implementation was behaviourally faithful
  throughout (0 discrepancies with the printed rule) because its empty-set
  fallback to `m = 0` exactly compensated. **No computed number changes; a
  claim about the source does.** Record: REGISTRY RR-X005 (kept, marked
  retracted), DECISIONS D-3 (rewritten).
- **Amended proof of RR-C008.** Two boundary errors in the worker argument are
  repaired: (1) case stability of II(b) needs a separate argument when `m0 = 0`
  (`t0' = t0`, e.g. `(-1;()) -> (0;(3))`), where `j <= -1` follows because the
  excluded `j = 0` case is exactly `{0} x A_n`; (2) the branch-inverse bound for
  II(a) with `nu = 0` must be `m3' <= m3`, not `m3' <= m3 - 5`, since
  `(0;(3,3)) -> (-1;(3))` retains `m3' = 3`; the weaker bound gives
  `m3'+5(j-1)-3 <= -5 < 0 = m0'` and the restoration still works.
- **Withdrawals:** "`Theta(n)` empirically" / "roughly linearly" (RR-C011 now raw
  max/mean/extremizers); "six independent counting methods" (corrected grouping);
  the unsourced "widely quoted table value" remark; and the recalled A003114
  array in `rr_core.py`, retired with no oracle substituted.
- **Code repairs:** `bz82.py` states the printed Case-II set; `phi`/`psi` now
  validate their state and name the excluded set on violation; the cycle
  detector is keyed on (parity, state) so the next involution is part of the key;
  header corrected (`psi`, not `phi`, is the Jacobi-triple-product-equivalent
  involution; images are complements, not intersections); `run_checks.py` tests
  the generic-filter gap count it computes and reports raw orbit statistics,
  extremal objects and two labelled traces.
- **Evidence:** `results.json` (`bz82_bijection.ok` through `n = 30`,
  `involution_structure.ok` through `n = 30`, `counts_all_agree`),
  `Counterexamples/checker.py 30` -> PASS 0 fails; supervisor's own run of
  `run_checks.py 30` and pinned-compiler Lean compile.
- **Open:** existence of the `phi` maximum for all `n`; weak-decreasingness in
  Lean; `T` and the `Nat.Partition` bridge; a named build target; and the
  Mathathon objective itself (RR-C012 OPEN).
- **GitHub checkpoint:** local commits only; push blocked (no credential).
  Bundle export for the supervisor is under `.sair/exports/`.

## 2026-11-14 / RR-M004 / phi maximum exists exactly on the domain (cycle-2 worker audit)

- **Agent and reviewer:** worker m3 (swarm `smwg03n61`, direction A/`Computation/cycle2/`),
  re-derived independently by Main.
- **Status:** closes the cycle-1 "existence of the `m` maximum" obligation in the
  sharp form; no claim promotion beyond RR-C009's scope.
- **Statement:** over all Case-II states of weight `<= 30`, BZ82's printed
  admissible set `{0 <= z <= a+2j-2 : z + lam(a+2j-1-z) <= t+5j-2}` is empty for
  893 states and every one lies outside `phi`'s domain (`0 x B(n)`); it is empty
  for **0** of the 33 329 in-domain Case-II states. Hence the maximum exists
  exactly where the rule applies, and "non-existence" is the domain boundary
  rather than a defect.
- **Evidence:** `Computation/cycle2/results_cycle2.json`
  (`case_ii.empty_admissible = 893`, `empty_admissible_in_domain = 0`,
  `empty_iff_offdomain_off = 893`, `exhaustive_ok = true`, `failures = []`),
  plus Main's own re-derivation (same three numbers).
- **Also independently reproduced by m3:** `exhaustive_ok = true` with
  `nmax = 30`; all three printed BZ82 examples; branch census
  (`phi_caseI = phi_caseII = 33 329`, `phi_a_eq_mu = 6 458`,
  `phi_virtual_zero = 2 605`, `psi_Ia = 2`, `psi_IIa = psi_IIb` paired at
  3 405/4 298 with 1 949 deletions matched by 1 949 creations); extremal path
  `n = 30`, `(4,4,4,4,4,4,4,1,1)`, 646 steps.
- **Reproduction:** `cd RogersRamanujan/Computation/cycle2 && python3 run_audit.py`
  (7.6 s) and Main's inline check.
- **Remaining:** an all-`n` version of the same equivalence; the other three
  cycle-2 worker directions were still running when this entry was written.

## 2026-11-14 / RR-M005 / psi proof audited with empty gap list; phi existence reduced to two inequalities

- **Agent and reviewer:** worker m1 (swarm `smwg03n61`, direction B,
  `Counterexamples/cycle2/`), refereed and machine-re-derived by Main.
- **Status:** RR-C008 **PROVED (amended, independently audited, gap list empty)**;
  RR-C009 documentation defect fixed.
- **New content.** (1) `Counterexamples/cycle2/AMENDED_PROOF.md`: the full
  all-`n` proof with named lemmas, repairing the supervisor's E1/E2 and supplying
  two items the cycle-1 text left silent: **E3** `II(a)` cannot be selected with
  `m3 = 0` (its guard would force `j >= 1` against `j <= 0`), and **E3'** `I(b)`
  cannot be selected with `m2 = 0`, which makes its multiplicity a non-negative
  integer. So "replace `m3`" and "delete `m2`" always act on real parts.
  (2) **Monotonicity lemma**: the Case-II admissible `z`-set is a down-set, so
  `m` exists iff `a+2j-2 >= 0` and `lambda(a+2j-1) <= t+5j-2`.
- **Verification (Main, independent of the worker's code).** Over all 33 329
  in-domain Case-II states of weight `<= 30`: down-set property 0 failures;
  the existence criterion 0 failures; `II(a)` with `m3 = 0` 0 occurrences;
  `I(b)` with `m2 = 0` 0 occurrences. Worker scripts rerun here:
  `psi_audit.py 30` and `phi_skeleton.py 30` (0 failures on skeleton steps P0-P9,
  `a = mu` on 6 458 states, all Case II) and `crosscheck.py 26` (26 248 states,
  0 value and 0 domain disagreements against `Computation/bz82.py`).
- **Pinned spec ambiguity.** `t*` = `t` real slots plus one virtual slot at each
  of `a`, `mu` exceeding `t`; the rival "pad to length `t*`" reading breaks weight
  preservation. The committed code already used the correct reading.
- **Reproduction:** `cd RogersRamanujan/Counterexamples/cycle2 && python3
  psi_audit.py 30 && python3 phi_skeleton.py 30 && python3 crosscheck.py 26`.
- **Still open:** all-`n` `phi` case stability and `phi^2 = id`; tying the two
  inequalities above; tie-breaks used but not derived from inverseness; and the
  Mathathon objective.

## 2026-11-14 / RR-M006 / Lean: the missing order statement is proved; staircase is a genuine equivalence

- **Agent and reviewer:** worker m2 (swarm `smwg03n61`, direction D,
  `Lean/cycle2/`), integrated and independently verified by Main.
- **Status:** RR-C005 upgraded from "six lemmas, order missing" to
  **LEAN_VERIFIED staircase equivalence**, with a toolchain caveat.
- **New theorems** (`Lean/StaircaseOrder.lean`, integrated): `subStair_weakDec`
  (`Pos + Gap => WeakDec (subStair l)`, the half missing since cycle 1),
  `addStair_pos`, `addStair_gap`, `addStairMap_subStairMap`,
  `subStairMap_addStairMap` on the subtypes `StairGap = {l // Pos l ∧ Gap l}` and
  `StairCoord = {m // WeakDec m}`, `stairBridge`, `subStairMap_facts` (length
  retained, `sum = n-k*k`), and `allZero_of_weakDec_zero` / `subStair_zero_tail`
  making the zero padding a terminal block.
- **Non-vacuity verified by Main** with a separate importing file: the kernel
  evaluates `subStair [7,3,1] = [2,0,0]`, `addStair [5,3,3] = [10,6,4]`,
  `subStair (addStair [4,0,0]) = [4,0,0]`; `subStairMap ⟨[7,3,1],_⟩ = ⟨[2,0,0],_⟩`
  by `rfl`; both subtype round trips fire at concrete elements; the order
  statement holds where claimed. The worker's sharp witnesses are confirmed:
  `¬ WeakDec (subStair [1,3])` (so `Gap` is genuinely needed) and
  `addStair [1] ≠ addStair [1,0]` (so padding carries the length).
- **Axioms:** `[propext, Quot.sound]` or none, for all 22 declarations; no
  `sorryAx`, no `Classical.choice`, no `native_decide`.
- **Toolchain, stated precisely:** the order module compiles on the VM's Lean
  **4.33.1** only. The cycle-1 base module was separately compiled on the pinned
  4.35.0 by the supervisor. So the pair is LEAN_VERIFIED modulo the pin, i.e.
  Lean-conditional on a 4.35.0 run of `StaircaseOrder.lean`.
- **Build:** `RogersRamanujan.lean` now imports both modules; named target
  `lake build RogersRamanujan` still unverified here (no `.lake` checkout).
- **Two integration fixes by Main:** import the real `RogersRamanujan.Lean.Staircase`
  instead of a byte-identical copy; and `def StairGap`/`def StairCoord` ->
  `abbrev`, because with `def` the subtypes are opaque to importers.
- **Still open:** `T` and `B_n`; the `Nat.Partition` bridge; a 4.35.0 run; and
  nothing here touches `A_n`, `phi`, `psi`, so the objective is untouched.

## 2026-11-14 / RR-M007 / first new mathematics: closed form on the all-ones ray, and where BZ82's cost lives

- **Agent and reviewer:** worker m4 (swarm `smwg03n61`, direction C,
  `Experimental/cycle2/`), independently verified by Main against the committed
  implementation.
- **Status:** RR-C013, RR-C014 **PROVED** (written residue-class case analysis,
  endpoint values verified by Main, individual QEDs not line-by-line refereed);
  RR-C015 PROVED lower bound + TESTED_FINITE lengths; RR-C016 OPEN.
- **Theorem F.** For `s >= 3`, `phi(0;(1^s)) = (-1;(s-3))`, so the whole ray
  reduces to `psi` on a **singleton**, which is closed form in all five residue
  classes of `p mod 5`, one class needing a six-step chain. Endpoints
  `b(1^s)` are `(s)` for `s=3 (5)`, `(s-2,2)` for `s=2,4 (5)`, `(s-4,4)` for
  `s=1 (5), s>=11`, and an explicit arithmetic progression on `(5^{s/5})` for
  `s=0 (5), s<=25`; exceptions `s=4 -> (3,1)`, `s=6 -> (4,2)` (and `s=2 -> (2)`,
  which the worker's prose omits - Main's correction). Path length <= 6.
- **Main's verification.** Forward images computed for all `s <= 60` with the
  committed `bz82.py`: every value matches. Path lengths 2 generically, 6 for
  `s = 1 (5), s >= 11`.
- **Theorem G.** `phi(0;(4^r))` is undefined for `r <= 4` (because
  `(4^r) in 0 x B(n)`), equals `(1;(5^{r-2},1^{8-r}))` for `5 <= r <= 8`, and
  `(-1;(r-6,3,3^r))` for `r >= 9`. Verified exactly for `r <= 12`.
- **The obstruction (the valuable half).** For `s = 0 (5)` the two-step output is
  `(5^{s/5})`, which lies in `B` iff `5 >= s/5`, i.e. iff `s <= 25`. So for
  `s >= 30` that class provably cannot close in two steps. Measured lengths at
  `s = 30,35,40,45,50,55,60`: 220, 574, 124, 452, 44, 454, 672, against <= 6 for
  every other class. This locates BZ82's cost structurally: cheap and closed-form
  on four residues of the all-ones ray, provably expensive on the fifth.
- **Refuted, kept:** `b(5k) = (5^k)` for `k >= 6` (7/7 fail); `b(5k)` affine in
  `k`; `len(b(4^r)) <= 2` (fails `r=7`); `kappa` a function of `s mod 5`; and no
  rule for `(4^r,1^s)`. M1/M2 both remain open with L-M1 the named blocking
  lemma, and neither meets the objective.
- **Reproduction:** `cd RogersRamanujan/Experimental/cycle2 && sh run_all.sh`
  -> "ALL LEMMA CHECKS PASS", "Theorem F end-to-end: claimed s = 0..120,
  mismatches = 0", "TOTAL failures ... 0"; plus Main's independent `s <= 60`
  comparison.
- **Scope:** this is roadmap level 2 (proved infinite-subfamily result). It is
  **not** a new bijection and does not by itself advance RR-C012.

## 2026-11-14 / RR-M008 / secondary implementation: 0 discrepancies over 66 658 states; Case-I deletion trap recorded

- **Agent and reviewer:** worker m3 (swarm `smwg03n61`, direction A,
  `Computation/cycle2/`), independently re-run and extended by Main.
- **Status:** strengthens RR-C007's faithfulness evidence (still TESTED_FINITE);
  new RR-C017 (trap, PROVED by witness). Swarm `smwg03n61` closed: 4 of 4
  directions accepted.
- **Independence result.** `bz82_audit.py` was written from the BZ82 scan
  **without reading `Computation/bz82.py`**. `compare_bz82.py 30` ->
  `phi 66658, psi 66658, domains 67551+67551, forward 893, onto-D 31/31,
  examples 3`, **DISCREPANCIES 0**; at `n <= 40`, 541 114 states, 0.
  The 893 is the sum of `|A_n|` for `n <= 30`, so the forward map agrees on every
  single object, not merely in count.
- **Third independent confirmation of RR-X006.** Negative controls reproduce
  exactly the 1120 / 374 / 374 failure counts at `n <= 18` for the three
  alternative `psi` tie-breaks.
- **F1/F7** re-confirm, from a third implementation, that the admissible set is
  empty **iff** the state lies outside `phi`'s domain, and that m1's existence
  criterion holds.
- **RR-C017, `phi` Case I deletion trap.** BZ82 says delete the parts `lambda(a)`
  and `lambda(mu)`; deleting position `a` and then position `mu` against the
  shortened list removes the wrong part. Main implemented the trap: 172 differing
  states at `weight <= 25`, **all with weight broken**, first witness `(-1;())`
  giving `(0;(1,1,1,1))` instead of `(0;(1,1,1))`; m3 reports 371 witnesses over a
  wider range. The committed code collects both slots first, so it was never
  affected.
- **Reproduction:** `cd RogersRamanujan/Computation/cycle2 && python3
  compare_bz82.py 30 && python3 negative_control.py 18`.
- **Still open:** no all-`n` theorem, no termination proof, no new bijection.
  RR-C012 **OPEN**.

## Swarm smwg03n61 close-out (cycle 2)

| member | direction | delivered | verdict |
| --- | --- | --- | --- |
| m1 | B proof audit | amended all-`n` `psi` proof, empty gap list, monotonicity lemma | accepted |
| m2 | D Lean | `subStair_weakDec` and the staircase equivalence, non-vacuous | accepted |
| m4 | C experimental | Theorems F/G closed forms; the `s=0 (5)` obstruction | accepted |
| m3 | A computation | independent implementation, 0 discrepancies; Case-I trap | accepted |

Four of four accepted. What the block produced: one retraction (my own), one
completed proof (psi), one completed formalization step (staircase equivalence),
the first new mathematics (two rays plus a structural obstruction), and a
secondary implementation that removes the faithfulness bottleneck.

## 2026-11-14 / RR-M009 / cycle-3 checkpoint: merged supervisor branch; maximum-existence PROVED

- **Date/time:** 2026-11-14, America/Los_Angeles (cycle 3).
- **Author / reviewer:** Main. Independent review of the case argument: Main,
  case by case, plus a 25-assertion machine check. The case split is the
  supervisor's (SUPERVISOR_REVIEW_19046.md, reviewed Nov 13 22:25 PST).
- **Status:** **PROVED** — `Main/LEMMA_MAXEXIST.md` (Lemma MX). Plus two
  statement-level corrections to a worker proof and a `phi` slot lemma.
- **Git integration.** Merged `origin/rr127/main` (`731b457`, the supervisor's
  review + Lean glob fix) and `origin/main` (`e6656d4`, watcher outage fix +
  ASTRA.md) into the research branch by **normal merge**, preserving
  `ef6826a`, `f8d372b`, `3379ab3`, `06d07a4`. No reset, no force push. The
  supervisor's `lakefile.toml` glob fix is retained (the explicit
  `RogersRamanujan.Lean.*` glob requested a nonexistent module).
- **Lemma MX (proved, all inputs).** In Case II the admissible set for `z` is an
  initial segment, so the printed maximum exists **iff** `k >= 1` and
  `lam(k) <= R`. The case analysis (`a <= t` split by `mu <= t` or `mu > t`;
  `a = t+1` split by sign of `j`; `a > t+1` impossible) is complete, with
  `a = mu` impossible in Case I. Every inequality is checked; the full proof is
  in `Main/LEMMA_MAXEXIST.md`.
- **What Main corrected in the process** (these supersede cycle-2 wording):
  * the printed rule has **no lower bound** on `z`; the scan prints only
    `z <= k-1`. The lower bound is a *consequence* on the domain, which is what
    MX.3(2) establishes;
  * read literally over all integers, the maximum **exists on every Case-II
    state**; off `phi`'s domain it is *negative* and one created part is
    non-positive (first witnesses `(0;())` -> `m=-2`, part `-1`; `(0;(1))` ->
    `-1,-1`). So "the maximum fails to exist off the domain" is wrong; the
    right statement is that it is negative there;
  * `a = mu` occurs on 6 458 states of weight `<= 30` and **all are Case II**
    (0 in Case I), so the cycle-2 second-removal fallback in `Computation/bz82.py`
    is unreachable.
- **Machine verification (Main, independent of the argument).** 25 assertions
  over every Case-II state of weight `<= 30` (34 222 states): **0 failures**.
  Cases: 1 -> 32 480, 2 -> 513, 3 -> **0**, 4 -> **0**, 5 -> 336, 6 -> 893. The
  zero counts for cases 3 and 4 are *required* by the proof (they contradict
  Case II), and `32 480+513+336 = 33 329` is exactly the in-domain count, with the
  893 excluded states being exactly Case 6. In-domain, `max over Z` equals
  `max over z >= 0` on all 33 329 states (0 disagreements).
- **Worker-proof corrections** (`Counterexamples/cycle2/AMENDED_PROOF.md`,
  amended in place with the amendment marked): Lemma 1.2 stated the `|lambda|`
  change as `-5j+3` for I(a)/II(a) while its own calculation gives `5j-3`;
  corrected. Lemma 2.3 stated that the output is "a partition of weight `n`";
  corrected to preservation of the signed weight `|lambda| + P(j)`, since after
  `j -> j+1` the partition alone has weight `n - P(j+1)`.
- **Corrections to cycle-2 summaries** (superseded text kept, see the reconciled
  table above): both extremizers in `(4^r,1^s)` — only the `n=30` one is;
  `(5^k)` as a residue family — it is not in `A_n`; "path length `<= 6`
  throughout `s <= 60`" — the bound is derived only for `s = 1,2,3,4 (mod 5)`;
  exact `>2` lower bound separated from measured lengths, with no growth claim.
- **Reproduction:** the 25-assertion check is inline in this entry's session; the
  reusable form is in `Computation/cycle3/` (worker task C). Fast regression:
  `python3 RogersRamanujan/Computation/run_checks.py 30`.
- **Explicitly NOT established:** `phi`'s Case-I insert count integrality, case
  stability, `phi^2 = id`, the alternating endpoint theorem, `T` and `B_n`, the
  `Nat.Partition` bridge — and the Mathathon objective itself.
- **GitHub:** local merge only; export bundle below.

## 2026-11-14 / RR-M010 / case stability both directions; fast regression; a-shift symmetry

- **Author:** Main. **Reviewer:** machine checks; the proof auditor (cycle-3
  swarm `smwg1kdjq`, member m4) is assigned the written proof of the same facts.
- **Status:** **TESTED_FINITE** for the transitions, **PROVED** for the weight
  identity. New file `Computation/cycle3_fast_regression.py` (0.11 s, 11 checks).
- **Case stability holds in BOTH directions, with no overlap:** over all
  10 285 Case-I and 10 285 Case-II states of `weight <= 26`, every Case-I state
  maps to a state selecting Case II (10 285/10 285) and every Case-II state maps
  to a state selecting Case I (10 285/10 285).
- **New structural fact, the `a`-shift symmetry.** Case I gives `a' = a-1` and
  Case II gives `a' = a+1`, each in 10 285/10 285 states. So `phi`'s two branches
  are inverse *at the level of the index `a`*: `phi` deletes/recreates the slot
  pair in a mirror image. This is the structural reason `phi(phi(s)) = s`, and it
  is the thing a written proof should explain. Recorded in
  `Main/LEMMA_MAXEXIST.md` as Lemma CI.2 and Lemma CII.
- **Honest statement of the remaining difficulty:** `t' - t` is NOT a simple
  function (measured range `-24..+2`, spread), because the created parts `m` and
  `t+5j-3-m` may be `1`s while decremented parts vanish. So the *length* is not
  preserved and cannot serve as a progress measure; a proof of `phi^2 = id` must
  track the multiset of values. This is why the naive "same length" argument
  fails, stated precisely.
- **Fast regression** (`Computation/cycle3_fast_regression.py`, 0.11 s, exit 0):
  the three printed examples incl. the nine-state chain, `T(7,3,1)=(5,3,3)`,
  `phi^2 = psi^2 = id` to weight 18, both bijection laws `A_n <-> D_n` to
  weight 18, the `n=0,2` fixtures, Lemma MX.2's criterion (1 739 Case-II states),
  and both `a`-shift facts. Deliberately small bounds: a smoke test, not evidence.
- **Reproduction:** `python3 RogersRamanujan/Computation/cycle3_fast_regression.py`

## 2026-11-14 / RR-M011 / cycle-3 swarm status: RUNNING at handoff (not a completed fleet)

- **Swarm:** `smwg1kdjq`, 4 members, launched for cycle 3. **State at this
  handoff: all four still running, 0 submissions received**, with about 49
  minutes of its own budget left. Per the supervisor's rule, an artifact written
  while its author is running is **not** an accepted audit, so nothing from this
  swarm is promoted below. Disposition:

| member | direction | board state | artifact on disk | verdict |
| --- | --- | --- | --- | --- |
| m2 | Lean `T` bridge | running | `Lean/cycle3/ShiftT.lean` (growing) | not submitted |
| m3 | computation regression | running | `Computation/cycle3/` (empty) | not submitted |
| m1 | `(4^r,1^s)` family | running | `Experimental/cycle3/` (absent) | not submitted |
| m4 | `phi` inverse proof | running | `Counterexamples/cycle3/` (absent) | not submitted |

- **One verified snapshot, recorded as evidence only.** At an intermediate state,
  `Lean/cycle3/ShiftT.lean` compiled here: `lean ShiftT_test.lean` exit 0, and all
  14 `RR127.Shift.*` declarations used `[propext]`, `[propext, Quot.sound]` or no
  axioms — no `sorryAx`. It formalizes the same-weight shift as
  `shiftT l = (subStair l).map (· + l.length)`, i.e. `T(lam)_i = mu_i + k`
  literally, with `sum_shiftT` (weight preserved exactly), `mem_shiftT_ge`
  (image entries `>= k`, i.e. the `B_n` condition), and both inverse laws
  `shiftInv_shiftT`, `shiftT_shiftInv`. **Main confirmed it is non-vacuous** with
  a separate importing file: `shiftT [7,3,1] = [5,3,3]` and
  `shiftInv [5,3,3] = [7,3,1]` by `rfl` (the contract's own example),
  `shiftT [9,4,1] = [7,4,3]` with sum 14, and both inverse laws discharged at
  concrete values. The worker's file then **grew another block** (a second
  `namespace Shift` with `weakDec_map_add`), so the file is a moving target and
  has **not** been integrated into the project or the named target. Once the
  worker submits, Main should re-verify, replace the inlined copy of
  `Staircase.lean` with `import RogersRamanujan.Lean.Staircase`, and rebuild
  `lake build RogersRamanujan`.
- **Why this is recorded rather than promoted:** the supervisor's rule is
  explicit that a running worker's partial file is not an accepted audit. The
  snapshot above is reproducible and useful, and it is labelled as a snapshot.

## 2026-11-14 / RR-M012 / worker skeleton auditor: P3 fails, confirming Lemma MX.5's boundary

- **Source:** `smwg1kdjq` member m3's `Computation/cycle3/phi_skeleton_c3.py`
  (still running; observed on disk, not a submitted audit).
- **What it does:** a per-step assertion skeleton P0-P9 over all in-domain states
  to weight 30, with a cross-check against `Computation/bz82.py`. Its last
  observed run: **0 cross-check mismatches over 66 658 states**, P0-P2 and P4-P9
  PASS, **P3 FAIL with 5 565 failed assertions**.
- **P3 as written is too strong.** It asserted "`a = mu` implies `a > t`, i.e.
  both slots are virtual". Minimal witness `j = 1, lam = (2,)` (weight 4): there
  `a = mu = 1`, `L = 2 = 2j`, and `a = 1 = t`, so the surviving slot is **real**.
- **This confirms rather than threatens Lemma MX.5.** That witness is Case II
  (`L + lam(mu) = 4 < 5j + t* = 6`), and MX.5 constrains `a = mu` only *inside*
  Case I, where it proves `a = mu` cannot occur. So the correct statement is: the
  Case-I double deletion always acts on two distinct slots; `a = mu` is possible
  in Case II, where no deletion happens. Recorded in `LEMMA_MAXEXIST.md`.
- **Value:** a third independent implementation cross-checking the map (0
  mismatches over 66 658 states), and an honest self-reported failure that
  sharpened a boundary claim rather than being hidden.

## 2026-11-14 / RR-M013 / RR-C006 promoted: T is LEAN_VERIFIED (4.33.1; pin pending)

- **Agent and reviewer:** cycle-3 worker m2 (swarm `smwg1kdjq`, direction B);
  every claim below re-verified independently by Main.
- **Status:** RR-C006 **TESTED_FINITE -> LEAN_VERIFIED**, with the toolchain
  caveat stated. This is a real ledger promotion, the first since RR-C005.
- **What is proved** (`Lean/ShiftT.lean`): `sum_shiftT` (weight preserved
  exactly, `k*k` cancels, no inequality needed), `mem_shiftT_ge` (image entries
  `>= k`, the `B_n` condition), `weakDec_shiftT` (image is a partition — the
  substantive half), `shiftInv_shiftT` and `shiftT_shiftInv` (both laws, length
  kept as data), plus `shiftInv_pos`, `shiftInv_gap` and the subtype bijection
  `toB : DGap -> BSmall` with `toD_toB`, `toB_toD`, `weight_toB`.
- **Main's verification.** `lean RogersRamanujan/Lean/ShiftT.lean` exit 0, 0
  errors, no `sorryAx`; 41 `#print axioms` directives print 40 results, 33 with
  axioms (`[propext]` 7, `[propext, Quot.sound]` 26) and 7 with none — all inside
  the allowed set. `python3 Lean/cycle3/check_encoding.py` exit 0, **10 checks,
  0 FAIL**, 197 `D`- and 197 `B`-objects at `n <= 20`, including the important
  row **`T(D_n) = B_n` as sets for every `n <= 20`** — surjectivity, so this is a
  genuine bijection, stronger than the brief asked for.
- **Three hypothesis-necessity witnesses kernel-checked by Main** in a separate
  file (exit 0): `(shiftT [1,3]).sum ≠ 4` with `[1,3]` `Pos` but not `Gap`;
  `shiftT [0] = shiftT [1]`, so `Pos` is needed for injectivity; and
  `shiftInv [2,5] = [3,4]` which is `¬ Gap`, so the entry bound alone does not
  land in `D_n`. The hypotheses are load-bearing, not decoration.
- **Correcting one of my own earlier readings:** when I first tested an
  intermediate state of the worker's file I recorded "33 axiom lines, not 40" and
  treated that as a reporting discrepancy. That was my error: 33 was only the
  "depends on axioms" subset, and 33+7 = 40 is exactly what the worker claimed.
  No defect in their report.
- **Integration fixes by Main:** the delivered file inlined a verbatim copy of
  `Staircase.lean`, which re-defines `Pos`/`Gap`/`subStair`/`addStair` and so
  cannot be imported alongside the original; Main replaced it with
  `import RogersRamanujan.Lean.Staircase` and added the module to
  `RogersRamanujan.lean`. The aggregator now compiles exit 0 with all three
  modules.
- **Reproduction:** `lean RogersRamanujan/Lean/ShiftT.lean`;
  `cd RogersRamanujan/Lean/cycle3 && python3 check_encoding.py`.
- **Remaining:** a 4.35.0 run of this file (the supervisor has the pinned
  toolchain); `lake build RogersRamanujan` with the new module; the
  `Nat.Partition` bridge; `phi`/`psi` untouched by this module; RR-C012 OPEN.

## 2026-11-14 / RR-M014 / slot identities R2 verified: the phi^2 = id mechanism is now explicit

- **Agents:** cycle-3 swarm `smwg1kdjq` — m4 (direction A', phi obligations) and
  m1 (direction D, the `(4^r,1^s)` family). Both reports refereed and
  independently re-checked by Main. Two more members collected; m3 still running.
- **The key result (RR-C021).** Over all 10 285 Case-II states of weight `<= 26`,
  at the image `lam'(a') = m` (10 285/10 285) and `lam'(mu') = p2`
  (10 285/10 285). With the `a`-shift (`a'=a-1` for Case I, `a'=a+1` for Case II),
  this is the complete mechanism of `phi^2 = id`: Case II creates `m` and `p2`, they
  land exactly at slots `a'` and `mu'`, and Case I applied there deletes exactly
  them and increments back. The missing step is no longer a search — it is R2 plus
  the inequalities R1. **The composition itself is still not proved.**
- **RR-C022 (PROVED, all n).** `N >= 0` is Case I's own guard; both deletions are
  valid and `a != mu` in Case I (m4's proof, cleaner than Main's MX.5: `a = mu`
  gives `2j = L`, so `j >= 1`, while Case I forces `t* <= -j <= -1`); `p2 >= 0`
  from `m <= R` plus the Case-II dichotomy excluding `m = R`; signed weight
  preserved by identity. **Essential caveat:** `a = mu` *does* occur in Case II
  (6 458 states, e.g. `j=1, lam=(2,)`) — a same-swarm worker's assertion failed
  precisely by omitting the Case-I restriction.
- **RR-C020 (PROVED).** `phi`, `psi∘phi` and the `r=1` two-step endpoint are
  closed-form on the **whole** `(4^r,1^s)` family, all four regimes, plus Lemma 2
  (`()`,`(1)`,`(4^r)` for `r<=4` are off-domain) which *derives* RR-C014's
  `r <= 4`. Main re-implemented all regimes and compared with `bz82.py` for
  `r <= 10`, `s <= 25`: **280/280 agree**.
- **RR-C023 (headline on cost).** On this family BZ82 is much more expensive than
  on the ones-ray: 21 of 80 parameters in the `r=1, s = 0,4 (5)` classes exceed a
  20 000-step cap, finite chains to 18 702 and 15 452, against 672 for `(1^60)`.
  First measurement of BZ82's cost on a family with more than one object per
  weight, and it shows the difficulty is not confined to the ones-ray.
- **RR-C024 CONJECTURE** `b(4^2,1^s) = (s-1,6,3)` for `s = 2 (5)`: 80 held-out
  parameters, 0 failures. Not a theorem.
- **RR-C025 REFUTED, with a corrected witness.** The analogous `r=3` shape holds at
  `s = 27..57` and fails at `s = 62`, but the worker's printed image
  `(25,17,8,8,8,8)` after 1911 steps is wrong on two counts: the committed map
  (verified by Main: valid gap partition, weight 74, inverse recovers) gives
  `(30,20,9,7,5,3)` in **5** steps, and the reported tuple has adjacent
  differences `8,9,0,0,0` — it is not a gap partition and cannot be any image.
  The refutation stands; the witness does not. Their check tested only whether the
  conjectured shape fails, not what the actual image is.
- **Reproduction:** `python3 RogersRamanujan/Experimental/cycle3/fam45.py`
  (9/9, 4.5 s, 0 mismatches vs `bz82.py`).

## 2026-11-14 / RR-M015 / swarm smwg1kdjq closed 4/4; phi obligation (i) proved, dead code retired

- **Swarm `smwg1kdjq` closed: 4 of 4 directions accepted** (m1 family, m2 Lean T,
  m3 computation, m4 phi obligations). Every claim below re-checked by Main.
- **RR-C022(i) PROVED** (worker m3). Since `t+5j-3 = R-1`, obligation (i) is
  exactly `m <= R-1`. With `f(z) = z + lam(k-z)` strictly increasing on
  `0 <= z <= k-1` (and stepping **down** at `z = k`, which is the trap), the two
  cases `k <= t` and `k > t` both give `m <= R-1`, hence `p2 >= 0`. Main checked
  the 9 constituent assertions separately over 13 124 in-domain Case-II states:
  0 failures.
- **The bound is sharp**: `slab_c3.py`'s minimum `p2 = 0` is attained at
  `j = -4, lam = (1^23)`. Recorded because a bound never approached is worth less
  than one attained.
- **RR-C026, dead code retired.** `a = mu` cannot occur in Case I, so the two
  deletions always act on distinct slots. Two independent proofs (Main's MX.5 and
  the worker's shorter route via `2j = L`) and two independent censuses (Main: 6 458
  hits, all Case II; worker: 0 hits in 1 746 369 states) agree. The defensive
  `if drop:` fallback in `Computation/bz82.py` Case I is **now an assertion**;
  regression re-run clean (11 checks, 0 failed; `run_checks.py 18` passes).
- **Reconciliation of two apparently contradictory reports.** The supervisor
  reported `Counterexamples/cycle2/phi_skeleton.py` failing with
  `KeyError: 'a==mu'`; worker m3 reported it exiting 0 at bounds 2 and 30. **Both
  are right about different revisions:** at checkpoint `8d72419` the file indexes
  the `'a==mu'` key unconditionally in two places (Main extracted that revision to
  confirm), and the fix landed in later commits. The current tree exits 0 and
  independently reproduces Main's MX.5 figure (`a = mu` on 6 458 states, all
  Case II). Recorded with both revisions so neither silently supersedes the other.
- **Honest limits stated by the worker and retained:** obligations (ii), (iv), (v)
  were not attempted as proofs and P8 is finite evidence only. So `phi` remains a
  **reduction** (R1 inequalities + R2 slot identities) rather than a proved
  involution, and RR-C012 stays OPEN.

## 2026-11-14 / RR-M016 / cycle 4: B/D retraction, full R2 checked, six evidence repairs

- **Author / reviewer:** Main. Supervisor's `SUPERVISOR_REVIEW_26480.md` merged
  (origin/rr127/main `c8eeb4a`). Ultramath is OFF per user instruction; this block
  was Main solo, no live workers at handoff.
- **RETRACTION (the important item).** Cycle 3 "corrected" worker m1's P3 witness.
  **That correction is withdrawn and the worker was right.** `(25,17,8,8,8,8)` is
  the **`B`-endpoint** from `pi_forward` — a valid `B_74` object (length 6, smallest
  part 8) that is not required to have gaps. Main applied the `D_n` gap test to a
  `B`-object, and separately mis-measured the path: `tr, _ = pi_forward(p)` binds
  the **endpoint** to `tr`, so the reported "5 steps" was
  `len((30,20,9,7,5,3)) - 1`. The true figures are **1 910 edges / 1 911 states**.
  `T^{-1}(25,17,8,8,8,8) = (30,20,9,7,5,3)` entry by entry, so both tuples are
  correct and live on opposite sides of `T`. The P3 refutation stands, in `B`-space.
- **Repairs applied** (all in `Main/CLAIMS.md`): psi check was `psi_ok > 0` and is
  now full equality against its denominator, with two negative controls (deliberate
  `j`-sign slips in psi and phi) required to be detected on every state — 224/224
  each, 13 checks, 0 failed; MX.3's "monotone on all of `Z`" corrected (false across
  `z = k`, counterexample `k=10, lam(1)=5`: `f(9)=14 > f(10)=10`); **RR-C021
  downgraded PROVED -> TESTED_FINITE**; `PROOF_fam45.md` Lemma 1 split at `s=1`,
  `a != mu` restricted to Case I, the two-step endpoint claim restricted to the
  derived classes; the bogus divisibility-by-five obligation removed; the
  "length cannot be a measure" overstatement weakened to "`t` is not monotone";
  RR-C019 given the clean **real-slot** witness `j=0, lam=(4,1,1)` with `mu'=mu=1`,
  and the mathematical counterexample separated from any claim about the printed
  symbol (not visually verified).
- **New finite evidence (widening R2).** Over all in-domain states of
  `weight <= 23` — 6 224 Case-II and 6 224 Case-I — **0 failures** for: (R2.1) as a
  multiset with virtual slots, (R2.2), (R2.1') `{m',p2'} = {L,lam(mu)}`, and (R2.2')
  `#{x in lam' : x=1} = N`. So the whole of R2.1/R2.2 both ways is now supported,
  not just one inequality pair. **Still TESTED_FINITE**; R2.3/R2.3' not re-checked.
- **Proof hint recorded (not a proof):** a created part may tie with a decremented
  one, and may be `0` in a virtual slot, so a *positional* statement must say which
  copy sits at `a'` — ill-defined under ties. The **multiset** statement is exactly
  the form that survives ties, and since Case I deletes both slots, order is
  irrelevant. A proof should go through the multiset, not sorted positions.
- **Decisions:** D-9 (never conflate `B` and `D`; name the side in every statement
  and test; report states and edges separately) and D-10 (read what a worker claims
  before promoting; a Main-run census cannot lift a claim past TESTED_FINITE).
- **Lean:** supervisor confirms `ShiftT.lean` passes the named
  `lake build RogersRamanujan` on Lean 4.35.0, six jobs, exit 0. RR-C006 supported
  on the pin for its list/subtype `D`/`B` statement. It does **not** formalize
  `phi`, `psi` or `A`/`D`.
- **Still open:** all-input proof of R2 and R1, hence `phi^2 = id`; the alternating
  endpoint theorem; and **RR-C012**, the objective.
