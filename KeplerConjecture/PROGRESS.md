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
