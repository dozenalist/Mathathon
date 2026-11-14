# Rogers--Ramanujan / SAIR problem 127: progress

## Current state (2026-11-14, America/Los_Angeles)

| Area | State | Next action |
| --- | --- | --- |
| Target | Official formulation unchanged; seek a more natural first-identity bijection | Keep the objective explicit in every artifact |
| Coordination | Main + 4 Ultramath specialists (`smwfxwsqf`) run; 4 of 4 reports accepted | Next cycle: 2 specialists on R1/R2, plus Lean |
| Literature | BZ82 scan retrieved in full and read (all 3 pages); GM81a/GM81b full text still not retrieved | Resolve GM81b access before any novelty claim |
| Computation | Contract + six-method counts + working BZ82 reference map, verified `n <= 50` | Prove termination; add operation counts |
| Counterexamples | Independent checker PASS at `n = 30`; 5 registry entries; 2 obstructions PROVED | Audit any proposed preserved statistic first |
| Experimental | Level-splitting reformulation; 3 natural level rules refuted | Prove or refute Lemma LS exactly |
| Lean | 6 staircase theorems kernel-checked, axioms `{propext, Quot.sound}` | Fix toolchain mismatch; add `T`; add `Nat.Partition` bridge |
| Main result | No new natural bijection. Foundation complete, obstructions proved | Attack the residue-to-staircase step (R2) |

## Status at a glance

PROVED: RR-C003 (length), RR-C004 (largest part, all `n>=2`), RR-C008 (BZ82
`psi` involutive for all `n`), RR-C010 (cutoff witness).
LEAN_VERIFIED: RR-C005 (staircase bridge, 6 theorems).
TESTED_FINITE: RR-C002 (`n<=50`), RR-C006, RR-C007 (`n<=50`), RR-C009, RR-C011.
OPEN: RR-C012, the official objective.

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
