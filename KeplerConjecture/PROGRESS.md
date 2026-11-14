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

### K15-X-001 — 2026-11-14, America/Los_Angeles — Counterexamples (X), run-01

Source commit `69f3213aa6f2b636ec1b0e25a7394acfecae986b`, branch
`kepler15/counterexamples/run-01`. Reviewer for all entries: Main (M), except
X-C007 (Computation) and X-C008 (Computation). Detailed statements, proofs and
locators: `Counterexamples/REGISTRY.md`; machine-checkable evidence in
`Counterexamples/evidence/`.

| Claim | Status | Exact statement (short) | Evidence |
| --- | --- | --- | --- |
| K15-X-SRC-01 | PROVED (source) | Hales Def 3.2 / Lemma 3.3 read at printed p34 / PDF p46: thresholds are `sqrt(32)=4 sqrt2`, not `32`; text extraction drops the radical. `pi/sqrt18 = (4pi/3)/sqrt32`. | page image + exact check |
| K15-X-SRC-02 | VERIFIED (source) | Li Thm 6.1: CE 3D optimum `> 0.18398089` in center-density units; a lower bound on the CE optimum, ordinary 2-point single-function class only. | paper §6 + conversion check |
| K15-X-C001 | PROVED (new) | Contact-shell Laplacian positivity: a sharp certificate satisfies `Delta f(lambda) > 0` for some contact vector, so `Hess f` is not negative semidefinite there. Replaces retracted Prop. 4.7 with a positive statement. | written proof; exact 1D witness `f''=-2d_0+d_-1+d_1` |
| K15-X-C002 | PROVED (new) | The 3D maximizer is not unique: HCP attains `pi/sqrt18` and is not a lattice; Barlow family contradict every FCC-uniqueness step. | exact `Q(sqrt3)` computation |
| K15-X-C003 | PROVED (new) | Icosahedral 13-ball cluster forces `A >= 4sqrt2 - V_dod = 0.106563` for every fcc-compatible `A`; cell-volume-only bounds are capped at `0.754697`, strictly above Kepler. | hull volumes + closed forms |
| K15-X-C005 | REFUTED | "Li obstructs all higher-point methods": false; CDS22 3-point `0.770271 < 0.779747` CE. Lattice-only `0.741506` is domain-restricted. | Table 1.1 + conversions |
| K15-X-C006 | REFUTED | "No smooth sharp certificate exists": false (X-C001 + Viazovska's Schwartz `g`). Original claim preserved. | X-C001 |
| K15-X-C007 | REFUTED (negative) | Grid-LP feasibility is not feasibility: 8 of 9 LP-"feasible" 3D candidates fail exact Sturm certification; LP must impose `f(0)>0`. | `evidence/ce_lp_search.out` |
| K15-X-C008 | PROVED (scheme) | Laguerre-Gaussian family in 3D admits an exact, grid-free, tail-free CE certificate via Sturm sequences; eigenbasis verified to `4.6e-15`. | `evidence/ce_laguerre_exact.out` |

Normalization is frozen and independently rechecked by `Counterexamples/normalization_check.py`
(28 exact checks, all passing): unit balls, separation 2, `f^(t)=int f e^{-2pi i<x,t>}`,
`Delta <= (4pi/3) f(0)/f^(0)`, and `2^{-5/2} = 1/(4sqrt2)` is FCC's center density at
separation 2. Offload requests X-R01 (exact semialgebraic CE optimum) and X-R02 are in
`Counterexamples/local-requests/`. Earned level: **3 (reusable foundation)** — a proven partial
result X-C001/X-C003 plus three refutations and a certified control scheme; no progress toward
the full theorem, and two explicit obstructions now rule out whole strategy classes.

Unresolved objections: O1 distributional form of X-C001; O2 whether Barlow difference sets give
a *soft* proof of CE non-sharpness in 3D (replacing Li's 7000-digit certificate) — the most
promising open question found; O3 the exact form of the sparse-defect statement; O4 **E's and
C's current candidates are unaudited** (no artifacts on the setup commit).
