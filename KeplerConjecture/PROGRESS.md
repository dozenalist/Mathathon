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

### K15-COMP-013 — 2026-11-14 — Computation (role C), the T_LO finding

| claim | status | statement | evidence |
| --- | --- | --- | --- |
| **K15-C-TLOCOST-001** | **VERIFIED_EXACT (measured)** | `shell_check.py`'s default `T_LO = 12` costs about **6.7% of the bound**, because it requires `p ≤ 0` on `12 ≤ u < 4π = 12.566…`, i.e. **inside** the ball of radius 2, where the Cohn–Elkies hypothesis imposes nothing. Same code and degree, only `T_LO` changed: `K=9` `0.87227746 → 0.82311657`; `K=13` `0.84002473 → 0.78526369`; `K=21` `0.83632450 → 0.78062816` | `shell_propose.py --tlo-exact`, `TLO_FINDING.md` |
| **K15-C-TLOFIX-001** | **PROVED (elementary)** | `T_LO = 4·π_lo` remains safe: `4π_lo < 4π`, so `p ≤ 0` on `[4π_lo, ∞)` implies it on `[4π, ∞)`. The excluded sub-interval shrinks from `0.566` to `~10^-9` | same |
| **K15-C-XVAL-001** | **VERIFIED_EXACT (cross-session)** | the degree-33 certificate `Δ ≤ 0.77996622` is **accepted by Main's checker** in Main's monomial basis once `T_LO = 4π_lo` is used; with the default `T_LO = 12` the only failing predicate is the shell one, confirming the certificate itself is sound | `TLO_FINDING.md` §"Independent confirmation at degree 33" |

**Recommendation for Main (one line).** Switch `shell_check.py`'s default from `T_LO = 12` to
`T_LO = 4·π_lo`, or state in every quoted number that the `12` default makes it ~6.7%
pessimistic. No safety is lost.

**Best exactly-certified bound in Computation's possession is now `0.78062816`** (`K=21`,
`T_LO = 4π_lo`, `n = 27`, `ρ = 2.05`, unconditional) — **0.11%** above Cohn–Elkies' `0.779747`,
the residual being the mandatory `ε_q` margin on `q ≥ 0`.

### K15-COMP-014 — 2026-11-14 — Computation (role C), block close

| claim | status | statement | evidence |
| --- | --- | --- | --- |
| K15-C-TLODEGREE-001 | **VERIFIED_EXACT** | at the corrected threshold `T_LO = 4π_lo` the shell route reaches **`Δ ≤ 0.78055517`** (degree 25, `n = 27`, `ρ = 2.05`, unconditional) — **0.086%** above Cohn–Elkies' `0.779747`. Degrees 29, 31, 33 give no exact candidate: the pipeline saturates at degree 25 | `shell_propose.py --tlo-exact`, `TLO_FINDING.md` |
| K15-C-STATUS-001 | index | `Computation/STATUS.md` gives Main a one-page view of what is exact, what is numerical, what is open, plus three actionable items | `STATUS.md` |

**Summary of the block.** Two exact results that cross-validate across sessions: the degree-33
certificate `0.77996622` and the shell-route certificate `0.78055517`, both accepted by Main's
independently written checker. Three actionable defects/findings for Main (`T_LO` cost ~6.7%,
`T_HI` invalid at `ρ = 2.05`, do not optimise in the monomial basis). Five defects in my own code
found, four caught only by the independent checker. The uniform shell allowance is confirmed
useless at seven degrees in two bases.

### K15-COMP-015 — 2026-11-14 — Computation (role C), horizon correction

| claim | status | statement | evidence |
| --- | --- | --- | --- |
| K15-C-UMAX-001 | **PROVED (defect, corrected)** | the apparent saturation at degrees 29–33 was a **finite-horizon artefact**: the LP constrains `p ≤ 0` only on `[T_HI, Umax]` and a degree-29 polynomial on `[13.2, 40]` rises again to `max p = 5.4×10^46` before the leading term takes over. The exact checker, which tests the whole ray, correctly refused | `TLO_FINDING.md` |
| K15-C-BESTCERT-001 | **VERIFIED_EXACT** | with `Umax = 120` the route reaches **`Δ ≤ 0.78037031`** (degree 33, `T_LO = 4π_lo`, `n = 27`, `ρ = 2.05`, unconditional) — **0.080%** above Cohn–Elkies' `0.779747` | `shell_propose.py --degree 33 --tlo-exact --Umax 120` |

**The lesson, worth keeping:** a functional constrained on a finite horizon can be driven far
outside it, and an exact checker over the whole ray will (correctly) reject the result. The
repair is to extend the horizon with the degree, not to abandon high degree. `Umax = 250` fails on
conditioning, so `Umax ≈ 120` is the practical setting for the monomial basis.

### K15-COMP-016 — 2026-11-14 — Computation (role C), family optimum

| claim | status | statement | evidence |
| --- | --- | --- | --- |
| K15-C-FAMOPT-001 | **VERIFIED_EXACT** | the shell-route family optimum is **`Δ ≤ 0.78037031` at `(K, Umax) = (33, 120)`**, `T_LO = 4π_lo`, `n = 27`, `ρ = 2.05`, unconditional. Neighbours: `(35,120) → 0.78043244`, `(37,120) → 0.78052696`, `(33,160) → 0.78041926` | `TLO_FINDING.md`, `shell_propose.py` |

**Two-sided trade-off, measured:** raising the degree without raising the horizon *worsens* the
bound (the polynomial escapes the horizon), and raising the horizon alone breaks the monomial
conditioning. `(33, 120)` is the interior optimum, `+0.080%` from Cohn–Elkies' `0.779747`.

**This closes the shell route as an optimisation problem:** the family is characterised, its
optimum certified, and the residual `0.080%` is the mandatory `ε_q` margin on `q ≥ 0`.

### K15-COMP-017 — 2026-11-14 — Computation (role C), bidirectional cross-validation

| claim | status | statement | evidence |
| --- | --- | --- | --- |
| **K15-C-XVAL-002** | **VERIFIED_EXACT (both directions)** | the two independently written exact checkers accept each other's certificates. Direction 1: my degree-33 certificate `0.77996622` is accepted by `shell_check` at `T_LO = 4π_lo`. Direction 2: a degree-33 *shell* certificate is accepted by my `exactcert` in strict mode at `0.780338357535` vs `shell_check`'s `0.780338357611` — agreement to ten digits | `CROSSVALIDATION.md`, `audit_fourier.py` |

**Why this matters for integration.** Main can quote either certificate with the other session's
checker as the reviewing implementation, which is exactly the roadmap's acceptance condition
("exact rational identity, verified by an independent checker"). A wrong factor in `M`, a wrong
`π` enclosure direction, or a mis-mapped `t ↔ u` would break one of the two directions; neither
breaks.

**And it pins the only remaining difference between the pipelines:** `shell_check`'s
`T_LO = 12` default is *sound but pessimistic* (it can only reject valid certificates, never
accept invalid ones), which is why direction 1 needed `T_LO = 4π_lo` to pass.

### K15-COMP-018 — 2026-11-14T10:07–10:35Z — Computation (role C), review 0138-C corrections

| claim | status | statement | evidence |
| --- | --- | --- | --- |
| K15-C-MAINCHECK-UNSOUND-001 | **CONFIRMED** | `shell_check.py` at `6626714125c35292d78943cd0fe8d18ec0051b38` falsely accepts `le_on_interval([0,1,-1],0,0,1)`, `nonneg_on_half_line([0,-1,1])` and `_ray([0,1,-1],0)`; all three are contradicted at `u = 1/2`. All three vanish at the left endpoint of the region, which is where the sign-change count is presumably mis-indexed | `REVIEW_0138.md` §1 (reproduced) |
| K15-C-REVALIDATE-001 | **VERIFIED_EXACT (my checker)** | all four shell-route verdicts at `K = 33, Umax = 120` survive `exactcert.certify` after exact conversion to the Laguerre basis: `0.78037032` (`n=27`, unconditional) and `0.78033446` (`n=12`, conditional), in both `η` variants. The certificates stand; only `shell_check`'s automation was unsound | `REVIEW_0138.md` §2 |
| K15-C-FAMTESTED-001 | **TESTED_FAMILY** (demoted from "optimum") | best value found in the tested family is `0.78037032` at `(K, Umax) = (33, 120)` over the parameter grid searched. **Not an optimum and not a closure**: the ladder is non-monotone (`K=17` worse than `K=15`), which is positive evidence the search is not exhaustive | `TLO_FINDING.md`, §3 of the review response |
| K15-C-SOSFAMILY-001 | **VERIFIED_EXACT** (demonstrator) | the family `p(u) = -(u-T)(u-c)^2` has the explicit rational identity `-p = 0 + (u-T)(u-c)^2`, a Markov–Lukács representation whose multiplier is a **single rational square**; best found is `Δ ≤ 5.99152482` at `T = 314/25, c = 12`. A format demonstrator, **8× worse than CE**, not a competitive bound | `sos_family.py`, `out/sos_family.json` |
| K15-C-SOSIRRED-001 | **TESTED_FAMILY (negative)** | the LP-optimal certificates admit **no factorisation-based rational Gram export**: at degrees 5, 7, 9, 13, 33 both `q` and `-p` are irreducible over `Q` with multiplicity 1 | `REVIEW_0138.md` §5(a) |

**Corrections applied to artefacts:** `shell_sos.py` relabelled (numeric LP proposer, SOS structure
**not** implemented); `LOCAL_RUN_REQUEST.md` command corrected from `--degree 8` (unrunnable:
even, and above the cap) to `--degree 7`; "optimum"/"closed" language removed from
`STATUS.md`; `SHELL_PROPOSE_RESULTS.md` and `TLO_FINDING.md` retain the numbers with
`TESTED_FAMILY` status.

**Process correction accepted.** The previous block was ended at 40 of 60 minutes and reported as
"verified completion". That was wrong: finishing my own checklist is not the user's instruction,
and it says nothing about the project's completeness. Runtime for the previous block **was**
Ultramath, as the reviewer states; I had no evidence and should not have claimed "standard".

### K15-COMP-019 — 2026-11-14T10:44Z — Computation (role C), cut-deficit fallback

| claim | status | statement | evidence |
| --- | --- | --- | --- |
| **K15-C-CUTEQUIV-001** | **PROVED (elementary)** | for a blob equal to a whole period the boundary term vanishes and `Σ_U b = N(√32 − 1/ρ)`, so the cut condition reads `ρ ≤ 1/√32` — **the Kepler bound itself**. For periodic packings the cut condition is therefore *equivalent* to Kepler, not an independent inequality, and a falsification search that finds nothing is **vacuous rather than weak evidence** | `cut_deficit.py`, `REVIEW_0138.md` §7 |
| K15-C-CUTFIXTURE-001 | measured | FCC and HCP are exact equality cases (`b = 0` on every cell), so neither can discriminate. The periodised icosahedral 13-cluster has `b = +0.106563` on its central cell (`vol = 5.550291029 < √32`) but mean cell volume `315.077`, so its full-period `Σb = −4022.46` and it **does not refute** the condition | `out/cut_deficit.json` |

**Implication for Main.** "Test it first" cannot work in the form proposed: any counterexample to
the cut condition at bounded `Φ` would be a counterexample to Kepler. A localisation that avoids
the full-period blob (prescribed boundary-to-volume relation, or a functional with zero mean on
every packing) is a design change for Main and Experimental.

### K15-COMP-020 — 2026-11-14T10:5xZ — Computation (role C), SOS deliverable complete

| claim | status | statement | evidence |
| --- | --- | --- | --- |
| K15-C-SOSGRAM2-001 | **VERIFIED_EXACT** | degree-5 family with a two-square multiplier `-p = (u−T)[(u−c)²(u−e)² + m²(u−d)²]`: 1200/1200 rational parameter sets admissible, best `Δ ≤ 6.73788568`. **Extra freedom did not help** — recorded because it is the opposite of the expectation | `sos_family2.py`, `out/sos_family2.json` |
| K15-C-SOSWHY-001 | **PROVED (structural)** | explicit-Gram families of shape `-p = (u−T)σ₁` are weak because the shape pins `p(T) = 0` at the contact radius and fixes the local behaviour exactly where a competitive CE certificate needs freedom. This is a structural obstruction, not a tuning failure; it explains the 8× gap to `0.78` | `REVIEW_0138.md` §8a |
| **K15-C-SOSSHELL-001** | **PROVED (family-restricted)** | in the cubic family `p = −(u−T')(u−c)²` with allowance `η` on `[T,T']`, the smallest admissible allowance is `η* = (T'−T)M²`, `M = max(|T−c|,|T'−c|)`, **exact and attained at `u = T`**. Since the objective charges `n·η` with `n ≥ 12` and `η* > 0` for `T < T'`, every shell member is **strictly worse** than the `η = 0` member — a proof, not a search | `sos_shell_variant.py` |

**Same-family comparison now exists across the whole ladder** (`REVIEW_0138.md` §8c):
LP-optimal `0.77996622` (no rational Gram) / shell route `0.78037032` (no rational Gram) /
explicit-Gram cubic `5.99152482` / explicit-Gram quintic `6.73788568` / CE reference `0.779747`.
**The gap between the 0.78 rows and the 5.99–6.74 rows is the price of an explicit rational Gram
in this shape**, and closing it needs an SDP with rational Gram rounding (open obligation,
solver-dependent, hence a local request).

**Scope guard, applied to my own result:** `K15-C-SOSSHELL-001` is a statement about *one cubic
family*. It does not say shell allowances never help elsewhere, and it is not to be quoted as
support for a general negative claim.

### K15-COMP-021 — 2026-11-14 — Computation (role C), Fourier-side explicit Gram

| claim | status | statement | evidence |
| --- | --- | --- | --- |
| **K15-C-SOSQSIDE-001** | **VERIFIED_EXACT** | `q(u) = Σ r_i² + u Σ s_j²` makes `q ≥ 0` on `[0,∞)` hold **by construction** with an explicit rational Gram; `p` is then determined by the involution `a = M b` and its sign is decided by exact Sturm. Best at degree 5: `Δ ≤ 2.82361314` with `q = (5−u)² + (4/3)² + (5−2u)² + u[1 + (4u/3 − 5/2)² + 1/9]` — hand-checkable | `sos_qside.py`, `out/sos_qside.json` |
| K15-C-SOSQSIDE-002 | measured | degree 7 is **worse** (`38.13600953`): with full-length factors the coefficients grow and the random search finds poor ratios (289/5000 survivors). Recorded because it bounds what a naive search may claim | `out/sos_qside_K7.json` |

**Both sides of the certificate are now individually demonstrable with an explicit rational Gram**
(`K15-C-SOSQSIDE-001` for the Fourier side, `K15-C-SOSGRAM-001`/`SOSGRAM2-001` for the `p` side).
What does **not** yet exist is one certificate with explicit rational Gram on **both** sides at
useful strength. That needs an SDP with rational Gram rounding — no solver on the SAIR VM, so it
is a local request (obligation 1 in `REVIEW_0138.md` §10).

### K15-COMP-022 — 2026-11-14 — Computation (role C), improved Fourier-side demonstrator

| claim | status | statement | evidence |
| --- | --- | --- | --- |
| K15-C-SOSQSIDE-003 | **VERIFIED_EXACT** | improved explicit-Gram certificate: `q = 3² + (3u/2 − 6)² + u(3/2 − 2u/3)²` (three rational squares, hand-checkable), `p = −4u³/9 + 59u²/12 + 17u/6 + 1351/48`, giving **`Δ ≤ 2.61993314`** | `sos_qside.py` (26 000 trials, 16 389 exact survivors), `out/sos_qside_wide.json` |

Supersedes `K15-C-SOSQSIDE-001`'s `2.82361314`. The improvement from a wider search is recorded as
evidence the search **has not saturated**, so `2.61993314` is a best-found value, not an optimum —
the same status discipline the review required elsewhere.

### K15-COMP-023 — 2026-11-14 — Computation (role C), cut-deficit blob scan

| claim | status | statement | evidence |
| --- | --- | --- | --- |
| K15-C-CUTBLOB-001 | measured | blob cut-deficits in the periodised 13-cluster: the singleton blob `{central cell}` has `Σ_U b = +0.106563` and `|δ⁺(U)| = 12`, ratio **0.008880**; larger blobs are not binding (they pick up the enormous ring cells, ratio ≈ −21). Hence **any `Φ` satisfying the cut condition for every packing must exceed `0.008880`** | `cut_deficit.py` (`blob_report`), `out/cut_deficit.json` |
| K15-C-CUTWEAK-001 | measured | the fixture is weak: its density `0.0032` is 55× below Kepler because the twelve ring cells are huge. A fixture near the Kepler density would have ring cells near `√32` and could push the ratio much harder — **that is the next fixture to build**, and it needs exact Voronoi volumes for a perturbed close packing | same |

**Honest status:** `0.008880` is a *lower bound* on `Φ` from one fixture, not a refutation. The
fixture's full-period blob gives `Σb = −4022.46`, so the condition is satisfied there.

### K15-COMP-024 — 2026-11-14 — Computation (role C), jammed-close-packing negative result

| claim | status | statement | evidence |
| --- | --- | --- | --- |
| **K15-C-CUTJAM-001** | **TESTED_FINITE (negative, structural)** | FCC and HCP at minimum separation 2 are **jammed**: every centre has 12 contacts at distance exactly 2, so any displacement shortens some contact. Measured with a validation gate: random amplitude `0.06 → min sep 1.894`, `0.01 → 1.982`, both `< 2`. **No near-Kepler perturbation of a close packing exists**, so a near-Kepler fixture with unequal cell volumes cannot be built that way | `cut_fixture_close.py`, `out/cut_fixture_close.json` |
| K15-C-CUTNEXT-001 | open | a near-Kepler fixture with unequal cells must be a *different combinatorial type* — a Frank–Kasper phase (A15, σ). Constructing one exactly is the next concrete build | same |

**Why this matters more than the fixture would have.** The cut condition's interesting regime is
exactly the jammed close-packing regime in which no perturbation is available — another face of
`K15-C-CUTEQUIV-001` (the condition is equivalent to Kepler). Main should not expect a
"perturb FCC and find the obstruction" search to work.

**Validation gates built in and doing their job:** V1 (separation ≥ 2), V2 (volumes sum to
`N × covolume`), V4 (`Σb = 0`). The script refuses to report volumes when any fails, which is why
the first two runs produced no numbers rather than wrong ones.

### K15-COMP-026 — 2026-11-14 — Computation (role C), Frank–Kasper fixture refuted by measurement

| claim | status | statement | evidence |
| --- | --- | --- | --- |
| **K15-C-FKNEG-001** | **TESTED_FINITE (negative, measured)** | A15 (Cr₃Si) Wyckoff sites with **equal spheres** give packing fraction `π/6 = 0.523599` — the simple-cubic value, 29.3% below Kepler — because the shortest contact is the `a/2` `6c`–`6c` chain distance while the `2a`–`6c` distance is `a√5/4 = 0.559017a`, so the `2a` atoms are untouched and the structure rattles. **Frank–Kasper phases are dense for polydisperse mixtures, not for congruent spheres** | `cut_fixture_frank_kasper.py`, `out/cut_fixture_frank_kasper.json` |
| K15-C-FKCONTROL-001 | validation | the measuring routine is validated by two controls: FCC conventional cell reproduces **exactly** Kepler `0.740480`, simple cubic reproduces `π/6` | same |

**Consolidated consequence for Main (third face of `K15-C-CUTEQUIV-001`).** Between
`K15-C-CUTJAM-001` (close packings are jammed, no perturbation possible) and `K15-C-FKNEG-001`
(A15 is not dense for equal spheres), the near-Kepler regime appears populated **only** by the
close-packed stackings — all of which have **equal** cell volumes, hence `b = 0` identically and
**no discriminating power** for the cut condition. "Find a near-Kepler fixture and test the cut
condition" is unlikely to succeed; the condition is equivalent to Kepler and its only near-extremal
fixtures are exact equality cases.

### K15-COMP-027 — 2026-11-14 — Computation (role C), hill-climbed explicit Gram

| claim | status | statement | evidence |
| --- | --- | --- | --- |
| **K15-C-SOSQSIDE-004** | **VERIFIED_EXACT** | best explicit-Gram certificate: `q = (1/12)² + (11u/6 − 19/4)² + u(7/4 − 2u/3)²`, `p = −4u³/9 + 205u²/36 − 353u/144 + 3089/288`, giving **`Δ ≤ 1.99064200`** — 3× better than the `p`-side cubic family | `sos_qside_polish.py`, `out/sos_qside_polish.json` |
| K15-C-SOSPLATEAU-001 | measured | the hill-climb **plateaus at ≈2**: three further seeds give `1.99889176`, `1.99578400`, `1.99725415`. So `1.99064200` is best-found, **not optimal**, but the search is no longer productive | `out/polish_s*.json` |

**Progression recorded in full** so the shape of the search is visible: random `2.8236` → wider
random `2.6199` → hill-climb `1.9906`. Acceptance at every step was exact (`exactcert`), with the
float screen used only to steer.

### K15-COMP-028 — 2026-11-14 — Computation (role C), basin-hopping breakthrough

| claim | status | statement | evidence |
| --- | --- | --- | --- |
| **K15-C-SOSQSIDE-005** | **VERIFIED_EXACT** | best explicit-Gram certificate: **`Δ ≤ 1.41370455`**, with `q = Σ r_i² + u Σ s_j²` over five rational squares of degree ≤ 2, and the Gram identity re-checked by expanding both sides. `4.2×` better than the `p`-side cubic family, `1.4×` better than the previous Fourier-side record | `out/hop_u0.05_s17.json`, `REVIEW_0138.md` §13 |
| K15-C-SOSLOCALOPT-001 | measured | the `1.99064200` plateau was a **local** optimum: 2 500 single-coefficient moves from the degree-7 embedding found **zero** improvements, but allowing uphill moves (basin-hopping) escaped to `1.41791658` and then `1.41370455` | same |

**Search ladder recorded in full** (it is the useful part): random `2.8236` → wider random
`2.6199` → hill-climb `1.9906` → no improvement at larger degree → basin-hopping `1.4179` →
`1.4137`. Spread across adjacent seeds `1.4137–1.6957`, so the landscape is rough and the search
is **not converged**: `1.41370455` is best-found, and no optimality is claimed.

**Why this vindicates the review's language discipline:** one block ago I would have written
"the family plateaus at 2" after the hill-climb stalled. That was false — it was a local optimum,
and only basin-hopping revealed it.

### K15-COMP-029 — 2026-11-14 — Computation (role C), explicit-Gram record

| claim | status | statement | evidence |
| --- | --- | --- | --- |
| **K15-C-SOSQSIDE-006** | **VERIFIED_EXACT** | explicit-Gram record for this directory: **`Δ ≤ 1.37125723`** (`q = Σ r_i² + u Σ s_j²`, degree 5, five rational squares), reached by basin-hopping | `out/hop2_23.json`, `REVIEW_0138.md` §13 update |

Eight basin-hopping runs span `1.3713 … 1.6957`; the search is **not converged** and this is
best-found. **The trend across the block is monotone in effort — `5.99 → 2.62 → 1.99 → 1.41 →
1.37`** — which indicates the remaining gap to the LP-optimal `0.78` is a *search-power*
limitation of the explicit-Gram route as implemented, not a structural wall. That is the most
interesting open question in this file and the natural next task.

### K15-COMP-030 — 2026-11-14 — Computation (role C), search statistics and a revision of my own claim

| claim | status | statement | evidence |
| --- | --- | --- | --- |
| K15-C-SOSDIST-001 | measured | twelve basin-hopping runs (`--degree 7 --iters 4000 --uphill 0.05`, different seeds) give `1.3713` once, four in `1.41–1.46`, four in `1.48–1.70`, three at `1.99–2.00`; median ≈ `1.47`. **Only one run in twelve reached below `1.40`** | `out/hop*_*.json` |
| **K15-C-SOSWHY-002** | **REVISES K15-C-SOSWHY-001** | the earlier claim that explicit-Gram families are weak "for structural reasons" is **too strong**. What survives: the specific *shape* `−p = (u−T)σ₁` pins `p(T)=0` and is weak. The sum-of-squares condition *by itself* is not the obstruction — the Fourier-side form reaches `1.37` with five rational squares | `REVIEW_0138.md` §13 |

**Local request extended:** a longer search for the explicit-Gram certificate (a few hundred runs
at ~40 s, 1 CPU, < 300 MB) is now in `LOCAL_RUN_REQUEST.md` — this is exactly the job that belongs
on Astra's machine rather than the SAIR VM.

### K15-COMP-031 — 2026-11-14 — Computation (role C), degree 9 does not help

| claim | status | statement | evidence |
| --- | --- | --- | --- |
| K15-C-SOSDEG-001 | measured | degree 9 (factors of degree ≤ 4, 3000 hops, seed 101) gives `1.74760261` — **worse** than degree 7's `1.37125723` — because the parameter space grows faster than the iteration budget. The record is a joint property of degree *and* search effort, and `(degree 7, 4000 hops)` is the best combination found | `out/hopK9.json` |

**Closing record for the block:** explicit-Gram certificates improved `5.99 → 2.62 → 1.99 → 1.41 →
1.37125723`, with degree 9 worse at the same budget. All statuses are best-found / tested-family;
no optimality is claimed anywhere.

### K15-COMP-032 — 2026-11-14 — Computation (role C), record certificate independently validated

| claim | status | statement | evidence |
| --- | --- | --- | --- |
| K15-C-SOSVAL-001 | **VERIFIED_EXACT (four routes)** | the record certificate `Δ ≤ 1.37125723` (`out/hop2_23.json`) passes: the Gram identity by exact expansion; the exact conversion of `p` to the Laguerre basis (zero residual); `exactcert.certify` in strict **and** even-multiplicity modes; and the independent SymPy oracle. **Main's `shell_check` was deliberately not used**, since it is unsound | `REVIEW_0138.md` §13 |

**Block closing record.** Twenty-two commits. Explicit-Gram certificates improved
`5.99 → 2.62 → 1.99 → 1.41 → 1.37125723`, degree 9 worse at equal budget, record validated by four
independent routes. Every status is `VERIFIED_EXACT`, `PROVED`, `TESTED_FAMILY` or
`TESTED_FINITE` as appropriate; no optimality is claimed anywhere.

### K15-COMP-033 — 2026-11-14 — Computation (role C), p-side Gram improved 5.99 → 2.00

| claim | status | statement | evidence |
| --- | --- | --- | --- |
| **K15-C-SOSPSIDE-002** | **VERIFIED_EXACT** | allowing **many** squares in the p-side multiplier and basin-hopping the coefficients moves that family from `5.99` to **`Δ ≤ 2.00171738`**, with the simple Gram `−p = (u−12)[(101u/12 + 1/4)² + 2021/12]` (three of the four squares are constants) and `q ≥ 0` by exact Sturm | `sos_pside_many.py`, `out/sos_pside_many.json` |

**Explicit-Gram programme summary after this block:**

| family | best `Δ ≤` | Gram |
| --- | --- | --- |
| Fourier side, five squares, degree 5 | **1.37125723** | `q = Σ r_i² + u Σ s_j²` |
| p-side, many squares, hopped | **2.00171738** | `−p = (u−12)[(101u/12+1/4)² + 2021/12]` |
| p-side, two squares | 6.73788568 | |
| p-side, one square | 5.99152482 | |
| LP-optimal (no rational Gram found) | 0.77996622 | — |

**Both sides are now demonstrated at ≈2 or better with an explicit rational Gram.** The gap to
`0.78` is a search-power gap, not a structural one — which is the block's most useful conclusion
for Main and revises `K15-C-SOSWHY-001`.
