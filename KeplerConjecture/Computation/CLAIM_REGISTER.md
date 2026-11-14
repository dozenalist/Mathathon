# Computation claim register — after review 0353-C

Single place for Main to see every claim I hold, its status, and its evidence. Statuses follow the
roadmap vocabulary with two additions used only where the reviewer required them: `TESTED_FAMILY`
(finite search over a parameter family; **no** optimality or closure implied) and
`PENDING_MAIN_FIX` (evidence depended on Main's `shell_check`, unsound per review 0138-C).

## Exactly verified

| claim | status | statement | evidence |
| --- | --- | --- | --- |
| `K15-C-VERIFIEDCERT-001` | `VERIFIED_EXACT` | `Δ ≤ 0.77996622` for every unit-sphere packing in `R³`; degree-33 rational certificate accepted by two checkers sharing no code | `out/verified_certificate_K33b.json`, `verify_certificate.py`, `exactcert_oracle.py` |
| `K15-C-REVALIDATE-001` | `VERIFIED_EXACT` | four shell-route verdicts survive my checker after exact basis conversion: `0.78037032` (`n=27`) and `0.78033446` (`n=12`), both `η` variants | `REVIEW_0138.md` §2 |
| `K15-C-BOTHSIDES-QUINTIC-001` | `VERIFIED_EXACT` | quintic both-sides Gram: `Δ ≤ 1.33982381256`, two squares in `σ₀`, Cramer for `(f,i)`; `−p = (u−12)·(sum of squares)` and `q = σ₀ + uσ₁` make the signs structural. **Above the trivial bound 1** — a format demonstrator | `sos_both_sides_quintic2.py` |
| `K15-C-SOSQSIDE-004` | `TESTED_FINITE` | explicit-Gram Fourier-side (**all above 1**, demonstrator only): `1.99064200` from the plain hill-climb (a *local* optimum), `1.37125723` after basin-hopping, `1.33982382` on the `p` side. **Best found, not optimal** | `out/hop2_23.json`, `out/ps3.json` |
| `K15-C-SOSFAMILY-001` / `SOSGRAM2-001` | `VERIFIED_EXACT` | explicit rational square on the `p` side: `5.99152482` (cubic) / `6.73788568` (quintic) | `sos_family.py`, `sos_family2.py` |
| `K15-C-SOSSHELL-002` | `PROVED` (family) | in the cubic family every admissible shell allowance is `> 0` (`sup p > 0`), so every shell member is strictly worse than `η = 0`. The earlier "`η*` smallest/attained" and the repair `η ≥ p(T)` are both **false** and recorded as such | `sos_shell_variant.py`, `tests_0138.py` T4 |
| `K15-C-POSCERT-001` | `PROVED` (elementary) | `c=(4,1)` ⟹ `Δ ≤ 44π/15 = 9.215339` | `CERTIFIER.md` |
| `K15-C-FOURIER-AUDIT-001` | `PROVED` A1/A2, `TESTED_FINITE` A3 | Main's `fourier_map` correct: 49/49 exact agreement, `M² = I`, quadrature to `1e-13` | `audit_fourier.py` |

## Proved this cycle: the cut/flow geometry

| claim | status | statement, with its hypotheses visible | evidence |
| --- | --- | --- | --- |
| `K15-C-TRANSFER-DENSITY-002` | `PROVED` | a bounded antisymmetric transfer (`|φ| ≤ Φ`, `div ≥ b`) on a packing of finite upper density **that is `D`-saturated for some finite `D`** implies `ρ ≤ 1/√32`. No periodicity of `φ`. The saturation hypothesis is proved necessary for the argument (LEMMA S, LEMMA B), not decorative | `transfer_necessity.py` |
| `K15-C-CUTIMPLIES-003` | `PROVED` | the **finite-`U`** cut condition at any one finite capacity `Φ` on a `D`-saturated packing already forces `ρ ≤ 1/√32` — because `U = Λ ∩ B` *is* finite. No transfer on the infinite graph, no compactness, no period | same file, Corollary 1 |
| `K15-C-DECOUPLE-001` | `PROVED` | in the 13-cluster fixture copies are ≥ 12 apart while `R ≤ 3`, so every finite `U` splits into copies and `Σ_U b/|δ⁺(U)|` is a weighted average of copy ratios: the patch extremum equals the infinite-packing extremum | `cut_flow.py`, `period_convention.py` Q1 |
| `K15-C-PERIODCONV-001` | `PROVED` Q1/Q2, `TESTED_FINITE` per-cell | **Q1:** `diam X = 4`, so for `R ≤ 3` only the zero lattice shift occurs — the periodic graph is the plain register graph. **Q2:** torus cells partition the cube, so `Σ vol = 4096` exactly and the central cell is the true dodecahedron; the twelve ring cells are congruent — the octahedral group preserves register and lattice and acts transitively (orbit size 12) — so each has volume `(4096−V_dod)/12 = 340.870809080957`, measured to `3.4·10⁻¹³` by half-space intersection | `period_convention.py` |
| `K15-C-DUALITY-001` | `TESTED_FINITE` | the patch's minimum capacity from the LP (`0.008880610465967038`, bisection) and `t*` from the exhaustive cut scan (`0.008880268414739160`) agree to `3.4·10⁻⁷`, in the direction LP duality allows; the residual is `linprog`'s float tolerance. Every returned flow passes the exact verifier | `tests_cut_flow.py` S14 |
| `K15-C-CUTBLOB-001` | `PROVED` (fixture) | for the period-16 13-cluster and `R ∈ {2, 2.1029, 3}`, over **all 8191** subsets: `t* ∈ [0.008880268414739, 0.008880268414739]`, **width `8.3·10⁻²³`**, same maximizer (`{0}`) in both scans — pinned from both sides. A per-fixture constraint, **not** a universal capacity | `cut_flow.py`, `bracket_t_star` |
| `K15-C-HIGHDENS-001` | `PROVED` | `R`-saturated ⇒ `Ω(v) ⊆ B(v,R)` ⇒ `b(v) ≥ √32 − (4π/3)R³`. Hence every packing with covering radius `≤ R_Φ = ((√32−12Φ)·3/(4π))^{1/3}` fails C044 at capacity `Φ`; `R_0 = 1.105339`. No packing is constructed | `highdensity_cut.py`  The same bound gives **HD3**: at `R < R_0` every vertex has `b(v) > 0`, so `Σ_U b` over a box grows like `L³` while `|δ⁺| = O(L²)` and the ratio tends to infinity — the condition fails at **every finite `Φ`**, with no kissing-number input (needs `L > ΦCR/b_min(R)`, e.g. `L > 108` at `Φ = 1`, `R = 1.10`). |
| `K15-C-ISOPERIM-001` | `TESTED_FINITE` | FCC kissing-graph profile: `|δ⁺U|/|U|` has exponent `−0.3230 ≈ −1/3`, `|δ⁺|/|U|^{2/3} → 16.1`, on one complex. A mechanism for the open perimeter lemma, not a proof | `cut_isoperimetry.py` |

## The cut/flow API contract (X-C034 / D8)

| claim | status | statement | evidence |
| --- | --- | --- | --- |
| `K15-C-CUTFLOWAPI-001` | `VERIFIED_EXACT` | the public contract of `cut_flow.py`, checked three ways on 66 cases: the vertex set is `range(len(b))` and never the edge list; malformed edges (self-loop, duplicate in either orientation, out of range, non-pair) raise `FixtureError`; a flow must be antisymmetric with keys on edges only; an isolated vertex with `b(v) > 0` is infeasible at **every** Φ; `t* = +∞` there and `max(0, sup)` otherwise | `audit_cut_flow_api.py` (hand expectation + exact Fourier–Motzkin oracle + implementation), `tests_cut_flow.py` S16–S18, witness `out/fixture_C034_witness.json` |
| `K15-C-D4RECON-001` | `PROVED` | the period-16 13-cluster's cut condition reduces to **one** inequality: over all 8191 subsets exactly one has `Σ_U b > 0`, the singleton `{0}`, since any subset containing a ring vertex has `Σ_U b ≤ −335.1`. The fixture is unsaturated (`max hole ≥ 12.327`) so it supports no Hales-type argument, but its torus cells are bounded (they sum to 4096), so `b` is finite and the fixture *is* a legitimate C044 test set | `cut_flow.py`, `period_convention.py`, `REVIEW_0523.md` §4 |
| `X-C034 / D8` | `CLOSED` | `verify_flow_exact` false-accepted an isolated positive-deficit vertex; `feasible_flow` and `find_violating_cut` shared the defect. Repaired at `ae545b9`; the witness is retained and every path now rejects it, including the `PATCH_FEASIBLE` output | `audit_cut_flow_api.py` §A |

## Exact geometry of periodic fixtures (this block)

| claim | status | statement | evidence |
| --- | --- | --- | --- |
| `K15-C-EXACTVORONOI-001` | `VERIFIED_EXACT` | an exact rational Voronoi-cell engine for periodic packings: rational half-spaces, exact vertex enumeration, volume as `Σ|det|/6` over hull triangles. Reproduces the known cells (`2Z³` → 8, BCC → `a³/2`), satisfies the partition identity `Σ vol = |det L|`, and agrees with an independent Sobol sampler to 0.2σ on random 1-, 2- and 4-site packings. Refuses a too-small `rmax` explicitly instead of crashing inside qhull | `fixture_nonuniform.py` §A/E |
| `K15-C-NONUNIFORM-001` | `VERIFIED_EXACT` (fixture) + `TESTED_FAMILY` (the 2-point claim) | the smallest nonuniform periodic fixture has **three** points per cell: `L = 4Z³`, `(0,0,0), (2,0,0), (0,2,0)`, minimum separation exactly 2, **exact** cell volumes `16, 24, 24`, period volume 64. Every 2-point periodic packing tried has congruent cells. All its deficits are negative, so its cut condition is vacuous — unequal cells alone give the criterion nothing | `fixture_nonuniform.py` §B, `out/fixture_nonuniform_3pt.json` |
| `K15-C-CLUSTER-ROBUST-001` | `PROVED` | the 13-cluster's positive deficit is **not** an artefact of its empty void: adding any set of points in `[4,12]³` pairwise at distance `≥ 2` leaves the central cell unchanged (bisector planes at `≥ 3.46` against the dodecahedron's circumradius `1.2584`) and keeps the minimum separation `≥ 2` (triangle inequality on exact rational data). So the singleton bound `0.008880268414739` survives the filling. Not a saturation result — the void is ~12.3 wide | `fixture_cluster_robust.py` |
| `K15-C-NEARCONTACT-001` | `TESTED_FINITE` (500 instances) | for FCC at nearest-neighbour distance `d` the cell is `d³/√2`, so `b > 0` needs `d < 2`. A single-site displacement changes the cell by `≈0.7δ²` while the contact slack is `ε = d−2`; taking `δ` to the exact bisected maximum at four values of `ε`, `b(0)/ε → −12/√2 = −8.485` (measured −8.4926) and `b < 0` at every vertex. `nearcontact_scan.py` scans **500** instances in five families — FCC `x`-displacements, tetragonal FCC (unequal cells), random rational directions, two-site and three-site displacements — at densities 0.6206–0.7392: **0 instances with `t* > 0`**. Conditional: five families, not all packings | `nearcontact_scan.py`, `out/nearcontact_scan.json` |

## A nonvacuous 3-D fixture (this block)

| claim | status | statement | evidence |
| --- | --- | --- | --- |
| `K15-C-DENSESHELL-001` | `VERIFIED_EXACT` | a legal packing of unit spheres with **rational** coordinates on which the cut condition is **nonvacuous**: a central vertex with a 12-point icosahedral shell at radius 2.0005, period `8Z³`. Exact cell volumes (rational): central `5.554454804529 < √32`, shell `42.203795432955` each, summing to 512. `b(0) = 0.102399444964 > 0`; `Σ_v b = −438.46`. The cut fails for every `Φ < t* = 0.008533287080295` and holds at `Φ = t*` with the explicit radial flow `φ(0,j) = b(0)/12`, so the patch minimum is **exactly** `t*` | `fixture_dense_shell.py`, `out/fixture_dense_shell.json` |
| `K15-C-DENSESHELL-002` | `VERIFIED_EXACT` | the nonvacuous window: `b(0) > 0` for shell radius `r ≤ 2.01236…` and `< 0` above, bracketed with exact rational volumes to `9.3·10⁻¹¹`; `t*` falls from `8.53·10⁻³` at `r = 2.0005` to `3.9·10⁻⁷` at the crossing. Cross-check: the irrational 13-cluster at `r = 2` has `t* = 8.880·10⁻³`, consistent with monotonicity | same file §B |
| `K15-C-DENSESHELL-003` | `PROVED` (obstruction) | the shell cannot be filled further: the icosahedral covering radius `37.377°` puts any point at radius 2 within `2·2·sin(37.377/2) = 1.2817 < 2` of a shell vertex, so no legal 13th neighbour exists. Hence `b(0)` cannot be raised by adding contacts in this construction; the window of `-002` is the whole family | same file §A3 |
| `K15-C-VORONOI-COMPLETE-001` | `PROVED` | the exact volume algorithm's completeness: the cell is computed facet by facet from the enumerated planes (no float hull, no qhull), and the plane set is certified by (C1) every vertex satisfies every enumerated plane, (C2) every discarded plane contains every vertex, (C3) the hull is non-degenerate. Redundant planes are allowed; dropping a *facet* is caught (control fires) | `fixture_nonuniform.py` |
| `K15-C-FUZZ-001` | `TESTED_FINITE` | 26 000 random instances (`n ≤ 4`, `b ∈ {−2..2}`, random edges, rational `Φ`), each decided three ways — exact cut scan, exact Fourier–Motzkin, and the interface — with **0 disagreements**: every returned flow verifies exactly, every witness is a genuine violation, `t*` separates feasible from infeasible. Evidence for generic soundness, **not** a proof: it samples a distribution, and the oracle returns `None` rather than blowing up on hard instances | `fuzz_cut_flow.py` |
| `K15-C-TWOSITE-001` | `PROVED` | **two-site congruence**: with exactly two points `A,B` per cell, `σ(x) = A+B−x` descends to the torus (`σ(x+n) = σ(x)−n`, `−L = L`), is an isometry, and swaps the distance functions, so it maps `cell(A)` onto `cell(B)`. Hence `vol Ω(A) = vol Ω(B)` and a nonuniform 2-point periodic fixture cannot exist — the smallest nonuniform fixture has three points | `fixture_nonuniform.py` §B2, exact check on three cases |

## Finite-search evidence — **not** optima, **not** closures

| claim | status | statement |
| --- | --- | --- |
| `K15-C-FAMTESTED-001` | `TESTED_FAMILY` | best value found in the tested `(K, Umax)` grid is `0.78037032` at `(33,120)`. The ladder is non-monotone, so the search is **not** exhaustive |
| `K15-C-SHELLGAIN-002/003` | `TESTED_FAMILY` | the *uniform* `n`-neighbour allowance was not used by the LP in the cases tested. Says **nothing** about local/configurational strengthenings |
| `K15-C-SHELLBENCH-001` | `TESTED_FINITE` | grid LP, `η = 0` throughout; held-out tests exposed under-resolution at `K ≥ 21` |
| `K15-C-CUTJAM-001` | `TESTED_FINITE` (negative) | FCC/HCP at separation 2 are jammed (12 contacts at exactly 2), so no perturbation preserves separation: **no near-Kepler cut fixture by perturbation** |
| `K15-C-SOSIRRED-001` | `TESTED_FAMILY` (negative) | LP-optimal certificates are irreducible over `Q` at degrees 5, 7, 9, 13, 33 |
| `K15-C-SATURATION-001` | `TESTED_FAMILY` | the Laguerre pipeline's best is at degree 33 (`0.77996622`); degree 37–41 failed at every grid/margin tried |

## Withdrawn / refuted (retained as evidence)

| claim | status | why |
| --- | --- | --- |
| `K15-C-CUTEQUIV-001` | `WITHDRAWN` | "the full-period blob makes the cut condition read `ρ ≤ 1/√32`, so the condition is equivalent to Kepler". Invalid: C044 quantifies over **finite** `U` and a period is not finite. The one-directional statement that survives is `K15-C-CUTIMPLIES-003`; the converse (Kepler ⇒ a finite `Φ` works) is **open** |
| `K15-C-TRANSFER-DENSITY-001` | `REFUTED` | the periodic-sum version: summing the divergence over one period needs `φ` periodic, and periodicity of the *packing* does not make `φ` periodic |
| `K15-C-TRANSFER-ROUTE-CIRCULAR` | `WITHDRAWN` | a sufficient condition implying Kepler is not thereby circular; it is circular only if its proof assumes Kepler. Correct statement: exhibiting a bounded transfer is **strictly stronger** than the density bound |
| `"η* = (T'−T)M² is the smallest, attained"` and the repair `η ≥ p(T)` | `REFUTED` | both false; the true statement is `sup p > 0` (`K15-C-SOSSHELL-002`) |
| `K15-C-BUG-006` | `PROVED` (defect) | `feasible_flow` claimed exact re-verification in its docstring but returned a `10⁻⁹`-rounded LP solution unchecked; exposed by a bisected minimum capacity `8.3·10⁻⁹` *below* `t*`, which duality forbids. Fixed: verify before returning | `cut_flow.py` |
| `K15-C-EXACTCERT-001` and the `K = 9…21` ladder | `REFUTED` | review 48443: ten simple positive roots of `q`; verbosity-gated return and a sign loss in `yun_odd_part`. All `out/certificate_K*.json` are failed candidates, retained |
| `"Ω(v) = B(v,1)"` (a criterion I carried in my own plan) | `REFUTED` | it would give `b(v) = √32 − 4π/3 = 1.468 > 0` at every vertex, contradicting `Σ_U b ≤ 0`; and a Voronoi cell of a discrete set is a polyhedron. See `period_convention.py` |

## Pending Main's checker fix

| claim | status | why |
| --- | --- | --- |
| shell-route numbers quoted from `shell_check` alone | `PENDING_MAIN_FIX` | `shell_check` at `6626714` falsely accepts three inputs (`REVIEW_0138.md` §1). The certificates themselves were re-verified and stand; only `shell_check`'s *agreement* is uninformative until the fix is audited |

## Open obligations

1. **A certificate with obvious rational Gram on BOTH sides at useful strength.** Each side is
   individually demonstrable; doing both needs an SDP with rational rounding — no solver here.
2. **A near-Kepler fixture with unequal cell volumes** for the cut-deficit scan. Perturbation is
   ruled out (`K15-C-CUTJAM-001`), so this needs an exactly constructed Frank–Kasper phase.
3. **Re-run every `PENDING_MAIN_FIX` item** after Main's `shell_check` fix is audited.
4. ~~Exact ring-cell volumes~~ — resolved: the cells are congruent (octahedral symmetry) and
   measured to `3.4·10⁻¹³`; the value is exact given the partition identity.
