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
