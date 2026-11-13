# Rogers--Ramanujan / SAIR problem 127: progress

## Current state (2026-11-13, America/Los_Angeles)

| Area | State | Next action |
| --- | --- | --- |
| Target | Official formulation verified: seek a more natural first-identity bijection | Main freezes interfaces |
| Coordination | Five Ultramath role assignments and staged roadmap prepared | Human lead instantiates the roles |
| Literature | Source notes, machine-readable catalog, bibliography, and Hexagon source/search log prepared | Read core sources; resolve full-paper access gaps if needed |
| Computation | No project enumerator or baseline map implemented yet | C implements and X independently checks |
| Counterexamples | No new research claim refuted in this preparation | X audits candidate claims and Soodak's conjecture |
| Experimental | Routes proposed; no new candidate established | E supplies forward/inverse specifications |
| Lean | Local pinned library inspected; no project proof added | L defines families and proves the staircase bridge |
| Main result | No new all-n bijection or theorem claimed | Develop a proved component or precisely scoped partial result |

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
