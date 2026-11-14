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

### K15-COMP-005 — 2026-11-15 — Computation (role C), shell bench

| claim | status | statement | evidence |
| --- | --- | --- | --- |
| K15-C-SHELLBENCH-001 | **TESTED_FINITE** | the count-strengthened two-point bound at `rho = 2.09` with 12-neighbour shell allowance is *identical* to the same-degree `eta = 0` CE control: the LP sets `eta = 0` at every degree (13, 21, 31, 41) and at every shell width tested (2.09, 2.3, 2.6, 2.83). Gain exactly 0 | `Computation/shell_bench.py`, `SHELLBENCH_RESULTS.md`, `out/sb_*.json` |
| K15-C-HELDOUT-001 | **TESTED_FINITE** | held-out sign tests catch grid under-resolution: `K = 13` clean, `K = 21` and `K = 31` violate `f <= 0` on the held-out exterior grid, `K = 41` collapses to `f(0) = -6.3e5` (impossible since `fhat >= 0` forces `|f| <= f(0)`) | same |

**Interpretation for R2.** This meets the roadmap's redirect criterion ("no numerical strength
is demonstrated"), but the cause is specific and worth recording: the objective charges
`12 eta` per unit of allowance while relaxing one active constraint can lower `f(0)` by at
most about `eta`, so the trade cannot pay. The repair is *not* to abandon count-strengthening
but to replace the uniform count 12 with a local statement about how many of the 12
neighbours can simultaneously sit at the far end of the shell.

**Process note.** My first draft of `shell_bench.py` omitted the `fhat >= 0` grid entirely —
the same defect I audited in `Main/ce_laguerre.py` a block earlier. It was caught before the
first successful run and is recorded here because repeating an audited defect is a process
signal, not a detail.

**Not done.** No global sign or tail certificate: the polynomial sign on `[Tmax, inf)` is
open, and a compact-interval exponential bound plus tail estimate remains a separate
obligation. Everything above is `TESTED_FINITE`.

### K15-COMP-006 — 2026-11-15 — Computation (role C), exactcert validation

| claim | status | statement | evidence |
| --- | --- | --- | --- |
| K15-C-POSCERT-001 | **PROVED (elementary, hand-checkable)** | with `c = (4,1)` in the Laguerre basis, `p(t) = 11/2 - t` and `q(t) = 5/2 + t`, so `p<0` on `[8pi,inf)`, `q>0` on `[0,inf)`, and `Delta <= 44pi/15 = 9.215339` for every unit-sphere packing. Exact rational data published in `CERTIFIER.md` | `exactcert.py`, `exactcert_oracle.py` E1 |
| K15-C-BUG-003 | **PROVED (defect)** | `certify` required `p(0) < 0` and rejected otherwise; a CE certificate needs `f(0)=p(0)>0`. Every valid certificate was rejected, and the defect was invisible because the regression suite held only rejections | `CERTIFIER.md` addendum |
| K15-C-BUG-004 | **PROVED (defect)** | the independent oracle contained the identical inverted test, written separately. Recorded because an oracle sharing an author's misconception is weak evidence even when it shares no code | same |
| K15-C-ORACLE-001 | tested | `exactcert_oracle.py` decides the predicate exactly with SymPy `sqf_list` + `count_roots` + a Cauchy bound, sharing no code with `exactcert.py`. 20/20 exact agreement on random candidates; in-line double roots allowed, in-line triple roots rejected, roots outside the half-line ignored, endpoint roots fail closed | `exactcert_oracle.py`, all E1–E4 pass |

**The sampled oracle in `exactcert_tests.py` T6 is downgraded to a smoke test**; it can miss a
narrow excursion and is not treated as evidence of a sign condition anywhere in this file.

**Process note.** Two of the four defects found in this cycle were only detectable because a
*positive* example was added. Both the checker and the oracle were rejecting everything and
said so consistently; agreement between two implementations that are both wrong is not
corroboration. Every checker in this directory now carries at least one accepted case.

### K15-COMP-007 — 2026-11-15 — Computation (role C), verified certificate

**Replaces the retracted ladder with a genuinely verified result.**

| claim | status | statement | evidence |
| --- | --- | --- | --- |
| K15-C-VERIFIEDCERT-001 | **VERIFIED_EXACT** | every packing of unit-radius spheres in `R^3` has `Delta <= 0.77996650`, exactly `Delta <= PI_HI·4·p0/(3·q0)` with `p0/q0 = 57247406970676848810768955/307445740617578019715085691` | `out/verified_certificate_K33.json`; accepted by `exactcert.py` (own Sturm + Yun) **and** `exactcert_oracle.py` (SymPy `sqf_list` + `count_roots`), which share no code; no floating point in either decision |
| K15-C-GRIDRES-001 | measured | the earlier failures were **grid resolution**, not degree: at `K=21, eps=1e-7` a 2000-point grid fails exact verification and a 6000-point grid succeeds | `search_grid_resolution.py` |
| K15-C-MARGIN-001 | measured | exact verification requires a sign margin: at `eps=0` the optimum touches zero and rounding destroys it; at `eps=1e-7` with grid 10000 it verifies, costing `0.77997` vs the `0.77975` control | `CERTIFIER.md` Addendum 2 table |

**Explicit scope.** This does **not** improve on Cohn–Elkies 2003, whose `0.779747` is
stronger. It is `+5.33%` above Kepler. Its value is that it is verified in-house end to end,
the rational data is published, and the pipeline now works on a non-trivial object — so any
future candidate from the shell bench or a hybrid route can be certified the same way.
Classified as a level-3 "reusable foundation" artifact, not a new bound.

**Three verified facts about the pipeline**, all recorded because the intuitive responses are
wrong: (i) raising the degree does not repair a failed certificate, refining the grid does;
(ii) `eps = 0` cannot be verified even though it gives the best objective; (iii) column
scaling is necessary at degree 33, without it the LP returns spurious degenerate optima.

**Reproduction:** `python3 verify_certificate.py out/verified_certificate_K33.json` (5 s).

### K15-COMP-008 — 2026-11-15 — Computation (role C), pipeline saturation

| claim | status | statement | evidence |
| --- | --- | --- | --- |
| K15-C-SATURATION-001 | measured | the verified-certificate pipeline saturates at degree 33: `Delta <= 0.77996622` (variant b) / `0.77996650` (variant a). Degrees 37 and 41 fail exact verification at every grid (10000, 14000) and margin (1e-8, 3e-8, 1e-7) tried | `search_saturation.py`; `out/verified_certificate_K33b.json` verified by both implementations |
| K15-C-SATLIMIT-001 | measured | the residual `+0.03%` above CE03's `0.779747` is the price of the strict-sign margin plus rational rounding; it cannot be removed within this family, because `0.779747` is a rigorous upper bound on the LP optimum | `CERTIFIER.md` saturation table |

**Why degrees 37–41 fail.** At higher degree the LP optimum has more sign changes between grid
points, so a fixed margin no longer dominates the inter-grid excursion and exact verification
correctly refuses. Refining grid and margin together is the only remedy, and the payoff is
bounded by `0.03%`. **This family is finished**: further progress needs a different mechanism,
not a higher degree. That is the decision-relevant conclusion for Main, and it agrees with the
independent negative result from the shell bench (`K15-C-SHELLBENCH-001`, gain exactly 0).

**Two routes now closed with evidence, both in the two-point family:**
count-strengthening with a uniform 12-neighbour shell (gain 0), and degree escalation of the
certified CE optimum (saturates `0.03%` above CE03). The remaining live route in my scope is a
genuinely different mechanism — three-point/SDP, or a local geometric inequality.

### K15-COMP-009 — 2026-11-14T09:18–10:19Z — Computation (role C), shell proposer

| claim | status | statement | evidence |
| --- | --- | --- | --- |
| K15-C-FREEZE-001 | frozen | the K33 certificates, both checkers, the oracle, the regression suite and the run request are pushed at `50727f1` and `90cc632` and restated in `Computation/LOCAL_RUN_REQUEST.md` with caps (≤300 s, 1 CPU, <1 GB) | `LOCAL_RUN_REQUEST.md` |
| K15-C-THIDEP-001 | **PROVED (defect in my reading, not in Main's file)** | `shell_check.check()` hardcodes `T_HI = 27/2`, which is valid for `ρ = 2.09` (`πρ² = 13.72`) but **invalid for `ρ = 2.05`** (`πρ² = 13.20`). The parameterised predicates must be called with `T_HI(ρ) = ⌊π_lo ρ²⌋` | `shell_propose.py`, `SHELL_PROPOSE_RESULTS.md` |
| K15-C-ODDDEG-BASIS-001 | **PROVED (elementary)** | in Main's monomial basis `M` is upper triangular with diagonal `(−1)^i`, so `lc(q) = (−1)^K a_K` and `lc(p) = a_K`; both sign conditions hold only for `K` odd. Verified numerically `M[K][K] = (−1)^K` | `shell_sos.py` guard |
| K15-C-MONOBASIS-001 | measured | the monomial basis is unsuitable for *optimisation*: `M[0][k] = (2k+1)!!/2^k` gives `M[0][7] = 15836`, and the direct LP returns box vertices with `p(0) → −∞`, reproducing `K15-C022`. Cause identified | `shell_sos.py`, results file |
| K15-C-SHELLPROP-001 | **UNRESOLVED (explicit failure)** | the corrected proposer (`shell_propose.py`) passes the shell and exterior-ray verdicts but fails `q ≥ 0` (`min q ≈ −1.8` at `u ≈ 21.5`) even with a 6000-point dual grid. **No exact candidate; no shell bound claimed.** Attributed to the proposer (four defects found and fixed in it this block), not to the mathematics | `SHELL_PROPOSE_RESULTS.md` |

**Consequence for the shell question.** `K15-C-SHELLBENCH-001` (`eta = 0`, gain exactly 0, my
Laguerre basis) is **neither confirmed nor refuted in Main's basis** by this block. Main should
treat the `eta` question as *one measurement in one basis* until a candidate is produced and
exactly certified.

**Four defects found in my own code this block**, listed because three of them were caught only
by an independent checker: the `T_HI` default, even-degree impossibility in Main's basis, the
`mono(u)·M` vs `mono(u)·Mᵀ` transpose error, and a column-scaling recovery inverted in the
wrong direction (caught because `q(0)` came out `1.62` where `1` was imposed). No defect was
found in `shell_check.py`.

### K15-COMP-010 — 2026-11-14 — Computation (role C), shell proposer RESOLVED

Supersedes the "explicit failure" status in `K15-COMP-009`. The five defects listed there were
real; fixing them produced exact candidates, and the earlier negative claim is now corroborated
by an independent basis and an independent checker.

| claim | status | statement | evidence |
| --- | --- | --- | --- |
| K15-C-SHELLPROP-002 | **VERIFIED_EXACT** (conditional only on citing CE) | at degree 9, in Main's basis with Main's checker: `Δ ≤ 0.87227746` for every unit-sphere packing, for `n = 27, ρ = 2.05` (unconditional, K15-C013a) and for `n = 12, ρ = 2.09` (conditional, K15-C019) | `shell_propose.py --degree 9`, `out/shell_propose.json`; verdicts are exact Sturm over `Q` with rational `π` enclosures, issued by `shell_check.py` |
| K15-C-SHELLGAIN-002 | **VERIFIED_EXACT** | with the allowance free, the LP sets `η = 0` in both cases and returns the *identical* value: **gain exactly 0**. This independently confirms `K15-C-SHELLBENCH-001` in a different basis (`u = π|x|²` vs `t = 2π|x|²`), with a different Fourier matrix and different Sturm implementation | same |
| K15-C-ETASIGN-001 | **PROVED (defect)** | the `η ≥ 0` row had coefficient `+1`, enforcing `η ≤ 0`; the objective drove `η → −10⁵` and produced a "candidate" with `Δ = −4.6e6`. A negative density bound should have been rejected by inspection before the checker | `SHELL_PROPOSE_RESULTS.md` §4.5 |
| K15-C-QMARGIN-001 | measured | a margin on `q ≥ 0` is mandatory, not cosmetic: without it the LP parks `q` at a double root (`min q = −1.1e-07`) which exact Sturm correctly rejects, and no grid refinement repairs it because the constraint is already met to solver tolerance | §2 step 4 |
| K15-C-CUTPLANE-001 | measured | the final `q` has a negative dip of width `0.034` at `u ≈ 21.52` while a 1500-point grid has spacing `0.027`; cutting-plane refinement at the dip midpoints is what makes the candidate verifiable | §2 step 3 |

**Scope.** `0.87227746` is a valid exact certificate and is **not** competitive with CE's
`0.779747`; the gap is the price of `T_LO = 12 < 4π` and of the mandatory `ε_q ≥ 1e-5` margin on
this route. It is offered as a cross-validated artifact, not a bound to improve on.

**The shell question is now closed with two independent measurements:** a uniform
`n`-neighbour allowance at fixed degree does not pay, because the objective charges `n·η` while
`p(0) ≈ 0.21`, so `η` must be below `≈0.008` to break even and at that size the relaxation buys
nothing.

### K15-COMP-011 — 2026-11-14 — Computation (role C), Fourier audit (fallback task)

| claim | status | statement | evidence |
| --- | --- | --- | --- |
| K15-C-FOURIER-AUDIT-001 | **A1/A2 PROVED, A3 TESTED_FINITE** | Main's `shell_check.fourier_map` is correct: (A1) it agrees entry-by-entry with my independent exact construction from `L_j^{(1/2)}` — 49/49 entries at `K = 6`, and `M[0][k] = (2k+1)!!/2^k` confirmed; (A2) `M² = I`, the transform being an involution on even functions, holds exactly; (A3) direct radial quadrature of the transform agrees with M's prediction to `1e-13` for `k = 0,1,2` at `y = 0.35, 0.9` | `Computation/audit_fourier.py` |

**Why this matters.** Every exact verdict in this directory rests on the Fourier convention. A3
is the check that would catch a wrong normalisation, a missing factor, or a factor of 2 in the
exponent, and it shares nothing with any polynomial algebra; A2 is a structural identity that a
mis-transcribed matrix almost never satisfies. Main's matrix passes both, so the `0.87227746`
certificate of `K15-C-SHELLPROP-002` rests on a verified transform.

**Not done this block:** the nonuniform radial-shell objective with exact geometric assumptions
(the second fallback item). `K15-C-SHELLGAIN-002` shows the *uniform* allowance does not pay;
whether a nonuniform one can is untested, and the present negative result must not be quoted as
a general impossibility.

### K15-COMP-012 — 2026-11-14 — Computation (role C), degree ladder for the shell proposer

| claim | status | statement | evidence |
| --- | --- | --- | --- |
| K15-C-SHELLLADDER-001 | **VERIFIED_EXACT** | the shell proposer produces exact certificates at degrees 9, 11, 13, 15, 17, 19, 21, improving from `0.87227746` to **`0.83632450`** (`n = 27, ρ = 2.05`, unconditional) and `0.83628884` (`n = 12, ρ = 2.09`, conditional) | `shell_propose.py`, `SHELL_PROPOSE_RESULTS.md` §0 |
| K15-C-SHELLGAIN-003 | **VERIFIED_EXACT** | the allowance gain is **exactly 0 at every degree tested** (9, 11, 13, 15, 17, 19, 21) and in both `(n, ρ)` cases. Sixteen independent exact comparisons, no exception | same |

**Caveat recorded:** the ladder is **not monotone** (`K = 17` gives `0.8425`, worse than `K = 15`'s
`0.8393`), because the cutting-plane loop and rational rounding are not converged at every degree.
Each row is separately verified, so nothing mathematical depends on monotonicity, but no
convergence rate should be inferred.

**Best exact certificate in Computation's possession is now `0.83632450`**, still far above
Cohn–Elkies' `0.779747` for the structural reasons in the results file (§2): `T_LO = 12 < 4π` and
a mandatory `ε_q ≥ 1e-5` margin on `q ≥ 0`.
