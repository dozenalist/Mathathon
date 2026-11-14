# X full-hour block, part 2 — Main's `shell_check` and E030's partition

Continuation of `REPORT_FULL_HOUR_20261114.md` within the same 60-minute block
(start `09:17:25Z`, earliest finish `10:17:25Z`). Ultramath not active.

## Priority 2b — Main `bbad129d`, `Computation/shell_check.py`: ACCEPTED on all tested points

Main uses a **third** convention, which is where a cross-convention error would hide:
`u = π|x|²`, `f = P(u)e^{−π|x|²}`, `f̂ = Q(u)e^{−π|x|²}` — the same variable on both sides.
That is coherent because the Laguerre basis in `u` is `L_k^{1/2}(2u)`, a polynomial in `u` with
rational coefficients, and `ψ̂_k = (−1)^kψ_k`. Interaction with C's convention: `u = t/2`,
`p(t) = P(t/2)`, coefficient-wise `p_k = P_k/2^k` — and Main's `interface_xcheck.py` states
exactly this, correctly.

**1. `fourier_map(K)` verified against direct 3-D radial quadrature** (my own quadrature, four
distinct rational coefficient vectors, `T ∈ {0, 0.37, 0.9, 1.4}`): max relative error
**`4.9e-15`**. The matrix for `K=3` is
```
[ 1   3/2  15/4  105/8 ]
[ 0   -1   -5   -105/4 ]
[ 0    0    1    21/2  ]
[ 0    0    0    -1    ]
```
whose first two columns `(1,0,…)` and `(3/2,−1,…)` match my hand derivation from
`L_0 = 1`, `L_1 = 3/2 − t` with `t = 2u`. **The Fourier matrix is correct.**

**2. π enclosure and threshold direction — verified exactly.** `PI_LO` and `PI_HI` are the
29-decimal rationals `314159265358979323846264338327/10²⁹` and `…329/10²⁹`. Against my own
independent 70-term Machin enclosure `[π_lo, π_hi]` (width `1e-67`):
`PI_LO ≤ π_lo` and `π_hi ≤ PI_HI`, so `PI_LO < π < PI_HI` **exactly**. Hence
`T_LO = 4·PI_LO ≤ 4π`, and the tested domain `[T_LO, ∞)` **contains** `[4π, ∞)`: the condition
verified is *stronger* than required, which is the safe direction. Correct.

**3. `_odd_part` — even multiplicities correctly excluded.** Verified on five fixtures:
`−(u−3)² ↦ 1` (no root counted), `−(u−3) ↦ u−3` (root at 3 counted), `−(u−3)²(u−5) ↦ u−5`
(root at 5), `(u−2)² ↦ 1`, `u−3 ↦ u−3`. So a certificate whose `q` *touches* zero is not
wrongly rejected, and a genuine sign change is not missed.

**4. Their self-test exits 0** and its summary is honest about the conditional constant: `n = 12`
is conditional on the Tammes-13 enclosure (`K15-C019`), `n = 27` is unconditional at
`ρ = 2.05` from the volume bound `⌊(ρ+1)³⌋−1`. That matches my independent finding that
`n = 12` needs Musin–Tarasov, while `n = 27` needs only counting.

*Not audited:* the shell-density theorem statement itself (I audited the checker, not the
write-up). Recorded as the remaining Priority-2 gap.

## Fallback — E030's partition: disjointness and coverage are fine; the content is (T)

* **Disjointness** holds by construction: an assigned centre is removed from the pool.
* **Coverage** holds by construction: every unassigned centre becomes a singleton.
* **No hidden obligation from swallowed defects:** if a defective `w` is absorbed into an
  earlier block `C(v)`, it never forms `C(w)`, so the only blocks are `C(v)`'s and singletons,
  and (T) for the `C(v)`'s plus soundness of singletons is exactly what E asserts. The rule is
  therefore *logically complete*, and (T) is the single geometric obligation — as E states.
* **The exact size of (T).** With `13√32 = 73.5391052`, `V_dod = 5.5502910`, (T) for the
  icosahedral block is equivalent to
  $$\frac{1}{12}\sum_{i=1}^{12}\operatorname{vol}\Omega(w_i)\ \ge\ 5.6657345
   \;=\; V_{\mathrm{dod}}\,(1+0.020804).$$
  **So (T) says: the twelve outer cells of an icosahedral defect must exceed the dodecahedral
  minimum by at least 2.08% on average.** That is a sharp, checkable reformulation; the
  dodecahedral theorem supplies `0%`, and a computation in a completion cannot certify it
  (monotonicity gives upper bounds). Any proposed proof must therefore exhibit *explicit
  disjoint bodies* inside the twelve outer cells of total volume `≥ 67.9888142`, and the
  natural candidates are the inner ball plus caps cut by the bisector planes to the twelve
  neighbours — the local geometry of the `1+12` cluster is the only input available.

## Status

| Item | Status |
| --- | --- |
| Main `shell_check.fourier_map` | **VERIFIED** (quadrature ≤`4.9e-15`; matrix matches hand derivation) |
| Main π constants and threshold direction | **VERIFIED EXACTLY** (`PI_LO < π < PI_HI`; `T_LO ≤ 4π`, safe) |
| Main `_odd_part` (even multiplicities) | **VERIFIED** (5 fixtures) |
| Main self-test | exits 0; constants honestly conditional |
| Main shell-density theorem write-up | **NOT AUDITED** (gap) |
| E030 disjointness / coverage | **CONFIRMED** by construction; no hidden obligation |
| E030 (T), exact form | **`outer mean ≥ V_dod·(1+0.020804) = 5.6657345`** — 2.08% above the dodecahedral minimum |
| Ultramath | **not active** |

## Next task

Audit Main's shell-density theorem write-up, then attempt the disjoint-bodies proof of (T):
inner ball plus bisector-plane caps inside the twelve outer cells, with the 2.08% target as the
acceptance criterion.

## Fallback (continued) — a dense-completion test of E's (T)

`Reviews/E030/t_test.py`. The 13-cluster (centre + 12 at distance exactly 2, outer mutual
distance `2.102924`) is embedded in a dense FCC background of minimum separation 2: 512
background points kept out of 555 inside radius 9, all pairwise distances `≥ 2.000000000000`.
Voronoi cell volumes computed by convex hull of each cell.

| quantity | value |
| --- | --- |
| `vol Ω(centre)` | **5.5502910** (= `V_dod` exactly — a self-check: the twelve tangent neighbours pin the regular dodecahedron, and the background does not cut it further) |
| `Σ_{i=1..12} vol Ω(w_i)` | **122.3902491** (mean `10.1991874`) |
| (T) threshold | `67.9888142` |
| margin | **`+54.4014349`** |

**Reading.** (T) does not come close to failing in a dense completion: the required 2.08%
surplus over the dodecahedral minimum is dwarfed by the observed ~80% surplus. Two caveats,
both required:

1. **This is an upper bound, not a proof.** By monotonicity (E003) any finite completion gives
   `vol Ω ≥` the saturated value is false the other way: adding centres only shrinks cells, so
   the computed volumes are *upper* bounds on the saturated ones. A positive margin is therefore
   evidence of plausibility, not a certificate.
2. **The completion is dense but not maximal.** The icosahedral cluster is frustrated — there
   are voids behind the twelve outer spheres that the FCC background cannot fill while keeping
   separation 2 (points closer than 2 to a cluster centre were excluded). A truly saturated
   completion would fill what it can, so the saturated sum is *smaller* than `122.39`, by an
   amount this computation does not bound.

**Strategic conclusion for E.** (T) is *not* numerically knife-edge, so the difficulty is
structural rather than quantitative: what is missing is a **lower** bound mechanism, and the
only available one is explicit disjoint bodies inside the twelve outer cells. The natural
candidate is the inner ball `B(w_i,1)` (volume `4.18879`, giving only `50.27` in total — 26%
short) plus the caps cut by the bisector planes to the eleven other outer centres and to
`v`. Those caps are where the 2.08% must come from, and their size is governed by the
`2.102924` opening angle rather than by `2` — which is exactly why the icosahedral cluster's
frustration is the crux.

## Third-opinion cross-check of K33 through *Main's* implementation

`Reviews/crosscheck_K33_via_main.py`. C's certificate lives in `t = 2π|x|²`; Main's checker
lives in `u = π|x|²`. The conversion is exact: `P(u) = p(2u) = Σc_kL_k(2u)`, so I expanded C's
34 coefficients into Main's monomial basis in `u` and ran **Main's** routines.

1. **Main's `fourier_map(33)` reproduces my direct `L_k(2u)` expansion exactly** on this real
   degree-33 vector (`b_M − b_mine = 0` componentwise). A much stronger test of their matrix
   than my `K=3` quadrature check.
2. **Main's checker accepts the converted certificate**: `_ray(a, T_LO) = True` (CE1),
   `nonneg_on_half_line(b) = True` (CE2), `p(0) > 0`, `q(0) > 0`.
3. Recomputing the bound with *Main's* π constants gives `0.779966497784296` in both
   directions, and C's `delta_upper_exact` still dominates it.

So `K15-C033` is now verified by **three independent implementations in two coordinate systems**
(mine, C's `exactcert` + `sympy_oracle`, Main's `shell_check`), with a lossless exact conversion
between conventions. That is the specific protection the assignment asked for: two checkers
sharing a sign misconception cannot explain this agreement, and my eight controls — including
the discriminating simple-vs-double-root cases — show the sign logic is exercised in both
directions.

## Main `K15-C019` (shell count = a Tammes-13 number): ACCEPTED, one algebra correction

Their lemma: for `2 ≤ |y_i| ≤ ρ` with `|y_i − y_j| ≥ 2`, the directions satisfy
`⟨u_i,u_j⟩ ≤ f(r_i,r_j) = (r_i²+r_j²−4)/(2r_ir_j)`, and `f` is increasing, so
`f ≤ f(ρ,ρ) = 1 − 2/ρ²`, giving `θ ≥ arccos(1 − 2/ρ²)` and hence `n(ρ) ≤ 12` whenever
`θ₁₃ < arccos(1 − 2/ρ²)`. **This is exactly the reduction I derived independently** in two
earlier blocks; the monotonicity step and the partial derivative `∂_a f = (a²−b²+4)/(2a²b)`
agree.

*Sharpening of their hypothesis.* They require `ρ ≤ √6 ≈ 2.449` (from `a²+4 ≥ 8 > ρ² ≥ b²`).
The condition actually needed is `a² + 4 > b²` in the worst case `a = 2, b = ρ`, i.e.
**`ρ < 2√2 = 2.828`**. Their bound is sufficient but not sharp.

*Correction to the mixed-case remark.* They write that `f(2,ρ) = ρ/4 < 1 − 2/ρ²` holds
"exactly when `ρ² − 4ρ + 8 > 0`, true for all `ρ`". That polynomial has discriminant `−16`, so it
is *always* positive and **cannot be the criterion**. Exactly:
$$1-\frac{2}{\rho^2}-\frac{\rho}{4} = -\frac{(\rho-2)(\rho^2-2\rho-4)}{4\rho^2},$$
whose roots are `2` and **`1+√5 = 3.236`**. So the mixed case is subdominant precisely for
`2 < ρ < 1+√5` (verified: true at `ρ = 2.09, 2.5, 3.2`; false at `3.3, 3.5`). **The conclusion
is unaffected for `ρ = 2.09`**, but the stated reason is wrong and the sharp admissible range of
`C019` as proved is
$$\boxed{2<\rho<\min\{2\sqrt2,\,1+\sqrt5\}=2\sqrt2=2.828},$$
not "all ρ". Anyone extending the shell bound to larger ρ must redo the mixed case.

## Final status of this block

| Item | Status |
| --- | --- |
| `K15-C033` (K33 certificate) | **ACCEPTED by 3 independent implementations in 2 conventions** |
| `K15-C033` near-tangency metadata | **CORRECTED** (`min q ≈ 3.7e-06`, not `3.5e-29`) |
| K33 minimal witness | `c₅ −= 3/2²¹` breaks it (fragility `1.431e-06`) |
| `K15-E015` Tammes-13 enclosure | **UPHELD** (`δ₁₃ ≤ 57.1448° < 57.1709°`); justification `E2`-only corrected |
| `K15-E030` partition structure | **CONFIRMED** (disjoint, covering, no hidden obligation) |
| `K15-E030` (T) | **OPEN**; exact form: outer mean `≥ V_dod(1+0.020804)`; dense completion gives `122.39` vs threshold `67.99`, so not knife-edge |
| Main `shell_check` | **ACCEPTED** (Fourier matrix, π enclosure, threshold direction, odd-part) |
| Main `K15-C019` | **ACCEPTED** with sharper hypothesis `ρ < 2√2` and corrected mixed-case algebra (`ρ < 1+√5`) |
| Main shell-density *write-up* | **NOT AUDITED** (only the checker and C019; the optimisation spec was read, not verified) |
| Ultramath | **not active** (no swarm created, resumed or queried) |

## Next task

Either (i) prove `K15-E030`'s (T) by exhibiting disjoint bodies in the twelve outer cells — the
`2.08%` surplus and the `50.27 < 67.99` ball-only shortfall show the caps must carry the whole
weight; or (ii) run the X-R03 SDP with `P = −(s−4)H`, `H` SOS, which is the only route on my
side that can still produce a certified 3-D CE number.
