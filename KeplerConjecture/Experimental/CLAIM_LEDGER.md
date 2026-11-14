# Corrected claim ledger — role E

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
| `K15-E064` | a blind periodic relaxation over (4 positions, cell size) recovers fcc: `L = 2.828427276` vs `2√2 = 2.828427125`, density `0.740480371` vs `π/√18 = 0.740480490` (rel. err. `1.6e-07`), four equal cells `5.656855` vs `√32` | numerical | **calibration** of the evaluator chain; not evidence about `(Q)` |

## Open

| id | statement |
| --- | --- |
| `K15-E004` | existence of a partition with bounded diameter absorbing the dodecahedral defect. **Largely superseded**: the transfer form (`K15-E061`) restores the pointwise condition and needs no partition, so this is only needed if the block form is retained |
| `(T'-R2')` | `S(C) ≥ D(C)` on one-shell blocks — equivalent to `(H_R)` (Section 3.5 of `REVIEW_0138.md`), so proving either suffices |
| `(H_R)` | Hall condition, any `R >= 2.09`. **No numerical evidence either way** (`K15-E062` retracts the earlier slack). Best available indication is exploratory and one-sided (`REVIEW_0308.md` §12: completions give payer cells `8.5`–`12`, all upper bounds) |
| **`(P')`** | the pair conjecture `K15-E074`. The cleanest open target this directory has: a two-cell isoperimetric statement, sharp at fcc/hcp, implying the cut. Survives every legal test (`E076`), **at risk at the icosahedral pair** where it needs `vol Omega(w_1) >= 5.763417` |
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
