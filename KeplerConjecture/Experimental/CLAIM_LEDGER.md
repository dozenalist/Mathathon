# Corrected claim ledger — role E

> **Supervisor review, 06:08 Pacific:** generic interval-volume and region
> certification at d289bef is suspended pending norm, boundedness/radius and
> coverage repairs. Passing named controls and reproducing one box do not
> validate those proofs. Preserve the author claims below as historical work.
> See [the exact witnesses and scope](../Main/REVIEW_2026-11-14_0608.md).

Updated 2026-11-14T10:0xZ (see git commit timestamp). Supersedes statuses in
`CANDIDATES.md`, `STATUS_FOR_MAIN.md` and `GEOMETRIC_OBSTRUCTION.md` where they conflict.
Reviewer: X. Withdrawn and narrowed claims are kept, not deleted.

## Proved

| id | statement | scope / hypotheses | independent content |
| --- | --- | --- | --- |
| `K15-E001` | cluster-averaged criterion ⟹ `δ ≤ π/√18 + C/r` | any saturated 2-separated `Λ`; `(C1)-(C5)` as stated | **conditional accounting lemma**; no geometry removed |
| `K15-E002` | dodecahedron inradius 1 has volume `5.5502910285155 < √32` | exact | none |
| `K15-E003` | cell volume monotone under adding centres; a bounded cell with complete 4-neighbourhood is certified exactly | any 2-separated set | none |
| `K15-E010` | cap bound is `θ ≤ 2 arccos(1 − 2/k)` (upper) | `k` points on `S²` | repairs C013's reversal |
| `K15-E011` | `max_{r,s∈[2,R]} (r²+s²−4)/(2rs) = max(1−2/R², R/4)`; equal-radius valid iff `0 ≤ δ ≤ √5−1` | any two centres in the shell | repairs the wide-shell error |
| `K15-E012` | count `12` holds for `ρ < 2+δ₀ = 2.091145548` | conditional on `θ₁₃ < 57.1367°` | conversion = `K15-E011` |
| `K15-E013` | every Barlow stacking has exactly 12 centres in `[2, 2.09]` | all hex-layer stackings | open shell `(2, 2√2)` |
| `K15-E014` | at most 12 in `[2,2.09]` and in `[2,2.05]` | any 2-separated set | exact rationals `23681/43681`, `881/1681` |
| `K15-E015` | `δ₁₃ < 57.138726938°` by rational interval arithmetic | **arithmetic only**; `d₁₃ = δ₁₃` is the imported Theorem 1 | computer-assisted source charged |
| `K15-E032` | blocks with adjacency `τ = 4.18` are disjoint, cover, `diam ≤ diam(C)+4.18` | any 2-separated set | tested (overlap 0) |
| `K15-E041` | `12 V_dodeca = 66.6035 < 67.9888`; shortfall `2.04 %` | imports the dodecahedral theorem | kills per-cell-independent bounds using `V_dodeca` |
| `K15-E045` | `Ω(c) ⊆ D` unconditional; `vol Ω(c) = V_dodeca` **conditional on the imported theorem** | see review §2 | **not** unconditional — corrected |
| `K15-E048` | for estimators satisfying (F1)–(F3): `vol Ω ≥ (1/3)∫τ³ ≤ 4.787969853` | **estimator family F only** | ceiling, `15.49 %` short |
| `K15-E049` | the ceiling is attained by the Tammes-capped radius | `ρ ≤ 2+δ₀` | **narrowed**: not "the per-cell route is closed" |
| `K15-E050` | icosahedral fixture: edge `4√2/√(5+√5)`, `cos(angle) = edge/4`, tangency `|c−w_j| = 2` exact | exact arithmetic | reusable |
| `K15-E060` | two-shell blocks need `τ = 8.36`; `diam ≤ diam(C)+4ρ`; boundary stays `O(r²)` | any 2-separated set | thresholds forced, not chosen |
| `K15-E061` | under Hall `(H_R)`: skew transfer ⟹ pointwise FCC-compat., exact cancellation, `O(r²)` negligibility, (C3) automatic; `A ≡ 0` on FCC/HCP | `(H_R)` unproved | **repackages, does not reduce**, the content |
| `K15-E063` | A15 (β-W) scaled to separation 2 is the project's first **saturated** fixture: cells `7.8125`, `8.0625`, extents `1.443 < 2`, density `0.523599`; **no defective cell** | exact coordinates, tested | first valid test of the extent criterion; does not answer `(Q)` |
| `K15-E070` | **`(Q)` is YES**: there is a *saturated* 2-separated set with `vol Omega(c) < sqrt32` | Zorn extension of the 13-cluster; `K15-E045a`; `vol D < sqrt32` | **imports nothing**; settles `(Q)` and decides the case split in favour of (b) |
| `K15-E071` | under `(H_R)` for finite `S` and bounded degree `<= kappa`, a global transfer exists (compactness) | `kappa <= 12` from `K15-E014` | the transfer form needs **no** bound on component diameter |
| `K15-E072` | four families of per-cell sufficient condition for the cut are quantitatively excluded; best `66.916356` against `67.988814` required | `S = {c}`; the families are balls, `V_dodeca`, the outward collar, and finite constraint sets | the shortfall is `1.072458` (`1.577 %`) at best |
| `K15-E074` | **(P') pair conjecture**: adjacent cells satisfy `vol Ω(v) + vol Ω(w) ≥ 2√32 = 11.3137084990`; implied by nothing available, implies the cut with `1.72 %` margin, and is **attained exactly** by every fcc and hcp pair | unproved | sharp at the equality family, so unimprovable; survives all fixtures |
| `K15-E076` | a legal completion of `w_1` attains `vol Omega(w_1) = 6.730974`, above the `5.763417` that `(P')` requires, so `(P')` survives its strongest test; margin `0.968` | `TESTED_FINITE`, upper bound | trajectory `13.51 -> 11.01 -> 8.543 -> 6.731` recorded as a warning, not a proof |
| `K15-E075` | two adjacent centres cannot both be dodecahedral: the two icosahedral rings clash at distance `1.056487696` against a required `2`, for every relative twist | proved (exact computation) | hence `2 V_dodeca = 11.100582` is unattainable and `(P')` is strictly stronger than the one-cell bound |
| `K15-E073` | on components, `(H_R)` is monotone in `R` because no defective centre lies within `R` of a component | `tau = 2R` exactly | enlarging `R` only helps; as `R -> infinity` the condition degenerates to the density bound |
| `K15-E080` | **frozen icosahedral-payer fixture**, exact coordinates in `Q(√5, √(10+2√5), √55)` — **degree 8**, because `sin 72° = √(10+2√5)/4` is a nested radical: `c`, 5 ring at `2.102924`, pentagon at radius exactly `2` with `cos θ = −3/8` (`θ = 112.0248°`), azimuth `36+72k`, south pole `(0,0,4)` | 78 pairs all `>= 2` incl. pairs against `w1`; added-vs-rest margin `2.171229792`; `0 ∈ int conv{n_i}` so the cell is bounded; `max|vertex| = 1.301723 < 2` so the ball is inactive | `Experimental/scripts/c5_fixture.py`, `evidence/c5_fixture.json`; `vol Ω(w1) = 5.898017371803720` confirmed to `1.4e-15` by float hull vs 40-digit mpmath face decomposition |
| `K15-E081` | **the cell of the frozen fixture is EXACT, not an upper bound**: for every 2-separated `Λ` containing the twelve centres, `Ω_Λ(w1)` is the twelve-face polytope | certified covering radius `41.85°` (mesh diameter `2.369°`, raw max `39.480°`) against the `48.88°` needed; worst `|z−s|² = 3.0437 < 4` over `2 ≤ ρ ≤ 2.603447` | hence a **saturated** packing containing the cluster has `vol Ω(w1) = 5.8980173718` exactly (Zorn). Separates the finite-cluster bound from a saturated completion |
| `K15-E082` | **angular exclusion for a ring face**: a centre cutting a ring face at distance `b = 1.051462` must satisfy `ρ < 2.6039` and be `>= 48.88°` from the ring direction, while the face subtends only `35.57°` from its normal | `ρ/2 < max|vertex|`; `cos α <= (ρ²+0.422310)/(2·2.102924·ρ)` | rules out head-on attack on a ring face; does **not** rule out corner-shaving |
| `K15-E088` | the family optimum is **attained by an exactly-specified configuration**: `cos θ = −13/35` (`θ = 111.8037°`, `sin = 4√66/35`, coordinates in `Q(√5, √(10+2√5), √66)`) gives `vol = 5.897967157`, `max|vertex| = 1.303944`, kill `3.0529 < 4`, i.e. the family minimum to `3.5e-8` and an exact cell | same covering argument as `K15-E081` | the frozen fixture's `5.0e-5` excess over the optimum is a choice of field, not a limit |
| `K15-E086` | the **symmetric family is fully resolved**: `(θ, φ) = (111.7975°, 36°)` minimises `vol Ω(w1) = 5.897967122`; `φ = 36°` is the exact mirror axis (`35.5`/`36.5` and `35`/`37` give identical volumes) and `φ` cannot drop below `≈22°` (legality); `θ*` from a parabolic fit to a `0.05°` sweep, on which every legal point is exact | `θ` re-optimised at each of 13 azimuths; `θ` grid `106..120` step `1`, then `0.05` near the optimum | block 0308 had only compared `φ ∈ {0,36}`, and the `1°` grid's argmin `112°` was resolution, not the optimum |
| `K15-E087` | **Barlow theorem verified out of sample**: 488 layers over 52 random legal stackings of period 3-20 all have `vol = 4√2`, 12 contacts at `2`, next distance `2√2`, and an fcc/hcp fingerprint matching the `±1`-step rule | `scripts/barlow_random_stackings.py`; centres pruned to `|z-v| < 3` (valid since `max|vertex| = √2`, checked `< 1.5` per cell) | independent of Main's six named stackings; my first version fingerprinted the wrong twelve normals and called every cell fcc |
| `K15-E091` | **first rigorous component of the interval branch-and-bound: a certified cell-volume enclosure.** Two rational polytopes bracket the true cell, `{y·n_i' ≤ b_i' − (R e_i + f_i)} ⊆ Ω ⊆ {y·n_i' ≤ b_i' + (R e_i + f_i)}`, and each bracketing volume is exact (Cramer over `Fraction`s, boundary triangulated as signed determinants) | `rational_interval.py` + `rigorous_cell_volume.py`; π by Machin, sin/cos by Taylor, both with rational remainder bounds; **no floating-point sign test anywhere** | controls all pass in 6.6 s: cube `8` exact, fcc/hcp `4√2` to `1e-18`, C5 fixture `5.898017371803720` to `8.7e-19`. Supersedes `barlow_contact_cell.py` for volume questions |
| `K15-E092` | the sandwich is **point-tight and box-blind**: a `0.2°×1°` box in `(θ,φ)` certifies only `[5.7281, 6.0663]`, width `0.338`, because each interval centre's error is multiplied by `R` and summed over twelve constraints | `box_volume` in `rigorous_cell_volume.py` | the B&B needs an explicit box-width/number-of-boxes curve before it can be scoped — `COMPUTE_REQUEST_0523.md` |
| `K15-E094` | **first certified continuum statements**: (a) every `(θ,φ)` in `[110.4°,110.6°]×[35.4°,35.6°]` has `vol Ω(w1) ∈ [5.873007762, 5.926242378]`; (b) every `(θ,φ)` in `[110°,111°]×[35°,36°]` — one full square degree — has `vol Ω(w1) ∈ [5.872109779, 5.927479312]`, lower end `0.108692` above the threshold | `scripts/certify_region.py`, 4 and 100 boxes of `0.1°`, sandwich valid for each whole box | a 2-parameter slice of the completion space, not the space itself; margin `0.109` against a box contribution of `0.053`, which is why the coarse grid closes |
| `K15-E093` | **correction to `K15-E075`**: the two-dodecahedra clash distance is `1.125554845`, not `1.056487696` (my script minimised over twists where the statement needs the maximum). Matches Main's independent `1.12555484451` | recomputed independently | conclusion unchanged: both `< 2`, so no twist admits two dodecahedral cells and `2V_dod` stays unattainable |
| `K15-E090` | **scope of the fixture, made explicit**: the icosahedral group acts transitively on the twelve outer centres and fixes `c`, so the twelve pairs `(c, w_i)` are congruent and the local problem is one problem; and the fixture is a *local witness* around `w_1` (its five pentagons would clash if repeated for all twelve), so it tests `(P')` and says nothing about simultaneous compensation of the cluster, which is what `(CUT)` needs | group action; the clash is the `K15-E040` frustration | prevents the fixture being read as a completion of the cluster |
| `K15-E089` | **bounded global search finds no better completion**: 2 × 900 s annealing over up to 10 free centres in `2 ≤ |z−w1| ≤ 2.8`, hard legality filter, reaches `5.898473397` (from empty) and `5.898007181` (from C5); neither beats the symmetric optimum `5.897967122`, neither refutes `(P')` | `scripts/c5_global_search.py`, seeds 1 and 2, `evidence/c5_global_search_*.json` | both settle at 6 free centres, i.e. the pentagon + south pole; the unseeded run misses the optimum by `5.1e-4`, more than the `(P')` margin — so this search is weak evidence and is not load bearing |
| `K15-E085` | **the exact-cell property is not a knife-edge**: for the pentagon family at radius exactly 2 with azimuth `36+72k` plus the south pole, **every legal `θ ∈ [106°,120°]`** (15 of 23 grid angles) has `Ω(w1)` exactly the twelve-face polytope; the family minimum is `5.898007181` at `θ = 112°`; the legal window closes on contacts at both ends | `scripts/c5_family.py`; covering bound recomputed per `θ` | the fixture's `5.898017372` sits `1.0e-5` above the family optimum; `(P')`'s margin is therefore a property of a whole `14°` window, not of one angle |
| `K15-E084` | **Barlow audit, volume table and saturation range**: Main's crack-packing table reproduced exactly at `d=2.4` — crack faces `6.985349063` (`b=-1.328494813`), bulk `sqrt32` in every layer; saturation bound `d <= 2H = 3.265986` is **sharp** because the covering radius of `Lambda u (Lambda+T)` is exactly `2/sqrt3`; `2.09`-graph disconnection threshold is really `d > 1.742113` (Main's `d > 2.09` is sufficient but unsharp) | independent enumeration, all centres within `5.5`, vertex enumeration + hull | two of my own slips (`2.946278` from a non-site, `9.81` from a dropped layer) were caught by the `V_dodeca = 5.550291` floor |
| `K15-E083` | **Barlow audit, Lemma 1′**: the contact-only polytope `K` satisfies `K ⊆ B(v,√2)`, both local types — **exact, symbolic** | fcc and hcp: 14 vertices each in `Q(√2,√3)` (`H = √(8/3) = 2√6/3`), `|x|² ∈ {3/2,2}` with multiplicities `8,6` (exact), `vol K = 4√2` exactly by the divergence theorem | repairs the circularity in Main `b42c8d1` `BARLOW_CELLS.md` Lemma 1: redundancy of a non-contact half-space needs `K ⊆ H_c`, not `Ω ⊆ H_c`. Script `barlow_contact_cell.py`, exit 0 |
| `K15-E077` | **structured (C5-symmetric) completion of the cluster attains `vol Omega(w_1) = 5.898007181138`** | explicit 13-point legal set: `c`, 5 ring at `2.102924`, staggered pentagon at radius exactly `2` (polar `112 deg`, azimuth `36+72k`), south pole `(0,0,4)`; added-pair margin `2.170617`; Zorn-extendable | best legal value known; cuts the `(P')` margin at the icosahedral pair from `0.500` to **`0.134590`**; locally minimal (0 legal single additions in 5382 positions, 0 legal two-pentagon configurations, 8000-move anneal no gain) |
| ~~`K15-E078`~~ | ~~the five-ring dodecahedral excess is "irremovable"; `97.4 %` survives every completion~~ | **WITHDRAWN** (review 0353 §4): failed searches do not prove it, and the angular argument does not cover bisectors meeting the collar at a large angle to the face normal. What survives is `K15-E082` (head-on exclusion) and, for the frozen fixture only, the exact value `K15-E081` |
| `K15-E064` | a blind periodic relaxation over (4 positions, cell size) recovers fcc: `L = 2.828427276` vs `2√2 = 2.828427125`, density `0.740480371` vs `π/√18 = 0.740480490` (rel. err. `1.6e-07`), four equal cells `5.656855` vs `√32` | numerical | **calibration** of the evaluator chain; not evidence about `(Q)` |

## Open

| id | statement |
| --- | --- |
| `K15-E004` | existence of a partition with bounded diameter absorbing the dodecahedral defect. **Largely superseded**: the transfer form (`K15-E061`) restores the pointwise condition and needs no partition, so this is only needed if the block form is retained |
| `(T'-R2')` | `S(C) ≥ D(C)` on one-shell blocks — equivalent to `(H_R)` (Section 3.5 of `REVIEW_0138.md`), so proving either suffices |
| `(H_R)` | Hall condition, any `R >= 2.09`. **No numerical evidence either way** (`K15-E062` retracts the earlier slack). Best available indication is exploratory and one-sided (`REVIEW_0308.md` §12: completions give payer cells `8.5`–`12`, all upper bounds) |
| **`(P')`** | the pair conjecture `K15-E074`: sharp at fcc/hcp, implies the cut, survives every legal test. **IN DOUBT, now with a sharp witness**: at the icosahedral pair it needs `vol Omega(w_1) >= 5.763417`; the C5 family attains `5.897967122` at `(theta,phi) = (111.7975, 36)` (`K15-E086`), **with the cell exact, not an upper bound** (`K15-E081`: no legal centre can cut it, so a *saturated* packing realises the value). Margin `+0.134549`. The earlier "margin halves at each search" reading is superseded: `8.543 -> 6.731 -> 6.264` were basin artefacts. `K15-E078` ("97.4 % irremovable") is **withdrawn** — that global claim is open. Still unproved: no lower bound above `V_dodeca` |
| **`(S_dod)`** | **stability version of the dodecahedral theorem**: any cell not in the exact icosahedral configuration has volume `>= V_dodeca + 0.1154435`. Identified in `REVIEW_0308.md` §10 as the precise missing input; no evidence either way |
| `K15-E013'` | the count at `ρ > 2.0911` (needs a sharper spherical-code input) |
| `K15-E020` | local-mass row; **blocked**, no three-point evaluator exists in these artifacts |
| **`(Q)`** | ~~unanswered~~ — **SETTLED YES** by `K15-E070`. Consequence: the per-cell inequality `vol Ω(v) ≥ √32` is **false** for saturated packings, so the compensation apparatus is necessary. The earlier framing ("`(Q)=no` would collapse the route") is retained for the record but is moot |

## Withdrawn / narrowed (kept for the record)

| id | old claim | disposition |
| --- | --- | --- |
| `K15-E030`, `K15-E031` | block rule R1 | **withdrawn**; singleton block gives `5.5503 ≥ 5.6569`, false |
| `K15-E040` | icosahedral compensation | not decidable from certified data |
| `K15-E043` | "`(T')` is implausible" | **withdrawn** at the time because `(T')` appeared to have `+44 %` slack — but that slack is itself now retracted (`K15-E062`), so `(T')` currently has **no numerical evidence either way** |
| `K15-E046` | perturbation heuristic | **withdrawn**; non-additive to `V_dodeca` |
| `K15-E047` | angular technique as a route | **withdrawn**; `4.734 < 5.550291`, weaker than the import |
| **`K15-E049` as originally worded** | "closes the per-cell route" | **narrowed to family F**; see `REVIEW_0138.md` §1 |
| `STATUS_FOR_MAIN` "only (2) remains" | — | **corrected**: multi-radius counts, convexity-based per-cell bounds and collective arguments all remain open |

## Retraction of the empirical slack claim (`K15-E062`)

The values `S - D = +50` to `+95`, and the "factor `470`-`880`" quoted in completion 51140 as
evidence that `(H_R)`/`(T')` hold with room to spare, are **withdrawn**. They were produced by
`vor_volumes` with a broken buffer flag: the flag tested "vertex radius > `R - 1e-6`" with the
buffer sphere at `R = 26`, which never fires because the buffer points themselves have unbounded
cells and core cells are truncated at radius `~18`. Diagnosed from the fcc control: largest
"boundary" cell volume `602.709` with maximum vertex radius `17.9205`, and `3000` unbounded
regions reported.

The flag now tests the saturation criterion `extent <= 2`, valid because `Omega(v) subset B(v,2)`
in any saturated packing. With that, **every** non-vacuous block is flagged unreliable
(`icosa_fill` 126/131 cells, `two_icosa` 241/281, `icosa_fcc_shell` 188/189). Since computed
volumes are upper bounds and the inflated cells are exactly the payers, `S` is overestimated
without bound and the true `S - D` could be small or negative.

The obstruction is genuine rather than a coding slip: no constructible completion of the
icosahedral cluster is locally saturated, because the motif is frustrated (outer centres at
`2.1029` cannot be closed up) and RSA reaches density `0.10` against `0.177` for fcc. So the
configuration that would make `(T')` testable is the one that cannot be built.

**Survives the retraction** (does not depend on volume accuracy): the statements of `(T')` and
`(H_R)` and their equivalence; the transfer theorem (`K15-E061`) including exact cancellation and
the `O(r^2)` boundary; the disjointness/overlap results and the `4.18` / `8.36` thresholds, which
use distances only; the transfer code check (`c + A >= sqrt32`, `|sum A| <= 1.4e-17`, `A = 0` on
fcc/hcp), which validates the implementation rather than the geometry.

## Reporting correction

Completion 51140 reported "40 minutes, finished 09:56Z". The official history (receipt
09:15:53Z, completion 09:41:19Z, ~25 minutes, Ultramath runtime) supersedes this. The error
came from inferring elapsed time from `date -u` output rather than API timestamps.
