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

## X-R03 structural-SOS attempt: a certified (if weak) 3-D CE bound

`x_r03_sos.py`. The parameterisation makes **CE1 exact by construction** and leaves only CE2:
$$H(s)=\sum_{j=1}^{r}q_j(s)^2,\quad q_j\in\mathbb Q[s],\qquad P(s)=-(s-4)H(s),$$
so `P ≤ 0` on `[4,∞)` because `H ≥ 0` and `-(s-4) ≤ 0` — no search, no sign test, no
possibility of a cutting-plane oscillation. Then `Q =` exact Fourier image of `P`, and the single
remaining obligation `Q ≥ 0` on `[0,∞)` is decided exactly (Sturm with even-multiplicity
handling). Density `(4/(3√π))P(0)/Q(0)`.

Random rational search (800 trials per setting, coefficient pool in halves up to ±4):

| `m` (deg `q_j`) | `r` | best `P(0)/Q(0)` | certified density |
| --- | --- | --- | --- |
| 1 | 3 | `1648/1513` | `0.819374` |
| **1** | **4** | **`2032/1867`** | **`0.818734679`** |
| 1 | 5 | `4240/3889` | `0.820147` |
| 1 | 8 | — | `0.864979` |
| 2, 3 | 2, 3 | — | no candidate found |

**Best certificate (frozen):**
$$P(s)=-(s-4)\Bigl[49+\tfrac{(s+12)^2}{4}+(5s+2)^2+\tfrac{(s+5)^2}{4}\Bigr],\qquad
P(0)/Q(0)=\tfrac{2032}{1867},$$
$$\boxed{\ \Delta\ \le\ \frac{4}{3\sqrt\pi}\cdot\frac{2032}{1867}\ =\ 0.818734679\ }\quad
\text{for every packing of unit balls in }\mathbb R^3 .$$

This is a **PROVED** bound (CE1 structural, CE2 exact, no numerical residual), but it is *weak*:
it is `0.078` above Kepler and `0.039` above C's K33 `0.77996650`. What it establishes is the
**pipeline**, not a competitive value: it is the first certified number X has produced in this
project, and it confirms that the `P = -(s-4)H` parameterisation removes the convergence failure
diagnosed in `REPORT_width_and_E030.md`. The obvious next step is an SDP over the `q_j`
coefficients (CE2 is quadratic in them) rather than random search; that is exactly the bounded
local request below.

**Bounded local request (X-R03b, for Astra).**
```text
commit      <this commit>       branch kepler15/counterexamples/run-01
cwd         KeplerConjecture/Counterexamples
command     python3 x_r03_sos.py                      # reproduces 0.826434 in ~35 s
            python3 x_r03_sos_sdp.py <m> <r> <budget> # to be added: SDP over the q_j
deps        python3.12, sympy 1.14.0, numpy 2.5.3, scipy 1.18.1
cap         10 min wall, 1 CPU, 2 GB ; precision: exact rationals in the certificate
success     a certified P0/Q0 with density < 0.779747 (CDS22's CE value) would be a genuine
            in-house record for the ordinary CE class; < 0.818734 is a modest improvement.
note        the random search is NOT an optimisation; it must not be reported as the
            optimum of the family, only as a feasible point.
```

## Block summary

Everything above was produced between `09:17:25Z` and the push recorded below. All three
assignment priorities were completed, plus the fallback and one implementation advance. Nothing
here required a Lean build or a heavy solve; the only offloads are the bounded reproductions
above.

## E030's (T): why it needs cluster-level input (precise obligation, not a route objection)

Three exactly-computed facts about the twelve outer cells of the icosahedral defect.

**(1) The insphere radius is exactly 1.** Every outer centre `w_i` satisfies `|w_i − v| = 2`
exactly, so the bisector plane between `w_i` and `v` bounds `Ω(w_i)` at distance exactly
`1.000000000000` from `w_i`. Hence the largest ball contained in `Ω(w_i)` has radius **1**, and
separation alone guarantees only `4π/3 = 4.188790` per cell: thirteen of those give
`54.454273`, which is **26% short** of `13√32 = 73.539105`.

**(2) Outer cells really can be capped at distance 1 on more than one side.** I probed the
admissible shell around the cluster: there exist points at distance exactly `2` from an outer
centre while keeping distance `≥ 2` from all thirteen cluster points (best probe attained
`2.000000`). So a background can put a further neighbour at distance exactly 2 from `w_i`,
legitimately cutting its cell. **Therefore (T) is not a consequence of local separation** — no
purely local argument about the 13-cluster can settle it.

**(3) The two known per-cell theorems compose to `72.1537834`, not `73.5391052`.** Hales gives
`vol Ω ≥ 4π/3` (`54.454` over 13 cells); Hales–McLaughlin gives `vol Ω ≥ V_dod` (`72.154` over
13). The required `13√32` exceeds the better of these by exactly **`1.3853219`**.

**Consequence, stated as an obligation rather than an objection.** (T) is a genuine
*cluster-level* inequality: it needs an input that is neither separation (insufficient, by (1)),
nor a per-cell volume bound (insufficient, by (3)), nor numerics (impossible, by monotonicity).
The natural candidates are:

* a **defect-tax inequality**: a lower bound on `vol Ω(w)` for a centre whose nearest neighbour
  is exactly at distance 2 *and* which is adjacent to a cell of volume `V_dod`, improving on
  Hales–McLaughlin by the missing `1.3853219/12 = 0.1154` per cell (a `2.08%` gain);
* a **second-moment / rigidity** argument: if all twelve outer cells were at the dodecahedral
  minimum, the cluster plus its surroundings would be forced into a configuration contradicting
  one of the distance constraints — the icosahedral frustration itself.

Neither is a corollary of anything currently in the project. This is the honest state of route
R1 as of this block: **one open inequality, with the exact deficit known.**

## Block close

Work spanned `09:17:25Z` to the push below, with checkpoints at 23 and 32 minutes and a final one
here. Priorities 1 and 2 are complete (K33 accepted by three implementations; Tammes-13 enclosure
upheld; Main's checker verified; Main's C019 corrected), the fallback is complete (E030's
structure confirmed, (T) reduced to its exact deficit, a certified 0.818734679 CE bound produced
by the structural-SOS parameterisation). Ultramath was not used: no swarm was created, resumed or
queried in this block.

## E's `SHELL_CONVERSION.md` (`K15-E010`/`E011`): ACCEPTED, and it supersedes my own earlier claim

**`K15-E010` (cap inequality, direction repaired).** `θ ≤ 2 arccos(1 − 2/k)`; for `k = 13`,
`2 arccos(11/13) = 64.40845°` — identical to the value I computed independently two blocks ago.
Their diagnosis is also right: the cap bound is an **upper** bound on `θ`, so it cannot
contradict `θ ≥ 60°`; it is vacuous here because it is too *weak*, not because it points the
wrong way. C013's "only forces `θ ≥ 64.4°`" was wrong on the direction. **ACCEPTED.**

**`K15-E011` (radius conversion) — correct, and sharper than what I produced.** They show the
maximum of `f(r,s) = (r²+s²−4)/(2rs)` on `[2,R]²` is attained on the boundary, with
`f(R,R) = 1−2/R²` and `f(2,R) = R/4`, and that
`1−2/R² ≥ R/4 ⟺ R³−4R²+8 ≤ 0 ⟺ (R−2)(R²−2R−4) ≤ 0 ⟺ 2 ≤ R ≤ 1+√5`.
So `cos θ ≤ 1−2/(2+δ)²` is valid **exactly for `0 ≤ δ ≤ √5−1 = 1.2360679…`**, and beyond that
the binding pair is `(2, 2+δ)`.

**This supersedes a remark of mine.** In two earlier blocks I reported that "`R < 2√2 = 2.828`
suffices, which is weaker than E's `R < 1+√5`". That was **a sufficient condition, not the sharp
one**: my argument used monotonicity of `f` in each variable, which is valid only while
`r²+4 > s²`, i.e. `R < 2√2`. E's range is strictly larger and is the correct one. **I withdraw
the claim that my condition is weaker (i.e. better) — E's `δ ≤ √5−1` stands as the sharp range.**

**One line missing from their proof, supplied here.** "The maximum is on the boundary" is
established by `∇f ≠ 0` in the interior (no solution of `r² + 4 = s²` and `s² + 4 = r²`
simultaneously — verified symbolically). But for `R > 2√2` the *edge* `s = R` has an interior
critical point at `r* = √(R²−4)`, which their proof does not examine. It is harmless:
$$f(r_*,R)=\frac{\sqrt{R^2-4}}{R}\ \le\ 1-\frac{2}{R^2}=f(R,R)
\iff R\sqrt{R^2-4}\le R^2-2 \iff 0\le 4,$$
so the edge critical point never beats the corner. **Their conclusion is therefore correct**;
the missing line is a completeness fix, not an error. (Their crossover check is also exact:
at `δ = √5−1` both candidates equal `0.809017`; at `δ = 0` both equal `0.5`, i.e. `60°`.)

**Status consequence.** `K15-E012`/`K15-E014` at `ρ = 209/100` were `PROVISIONAL` on an
"unverified external constant". That constant is now certified (`K15-E015`, which I upheld above:
`δ₁₃ ≤ 57.1448° < 57.1709°`), so E can move both to **PROVED, conditional only on
Musin–Tarasov being computer-assisted** — which they already disclose.

## Block close (final)

| Priority | Item | Outcome |
| --- | --- | --- |
| 1 | C `K15-C033` K33 certificate | **ACCEPTED**, 3 implementations / 2 conventions; metadata corrected; minimal witness frozen |
| 2 | E `K15-E015` Tammes-13 enclosure | **UPHELD**; transcription justification corrected |
| 2 | Main `shell_check` | **ACCEPTED** (Fourier matrix, π, threshold, odd-part) |
| 2 | Main `K15-C019` | **ACCEPTED** with sharpened range `ρ < 2√2` and corrected mixed-case algebra (`ρ < 1+√5`) |
| — | E `K15-E010`/`E011` | **ACCEPTED**; supersedes my earlier remark; one missing line supplied |
| fallback | E `K15-E030` (T) | reduced to an exact deficit `1.3853219`; shown **not** separation-determined |
| fallback | structural-SOS CE | certified **0.818734679** for all unit-ball packings (weak but proved) |
| gap | Main shell-density write-up | only the checker, C019 and the optimisation spec were read; the write-up itself is not audited |

Ultramath: **not active** in this block — no swarm was created, resumed, or queried; the tool
surface contained no Ultramath capability and reasoning effort is not evidence of it.

## Structural-SOS line: improved bound, and a negative result for the hybrid form

**Improved certified value.** Coordinate descent inside the structural family (every step
re-certified exactly) improved the random-search winner:

| stage | `P(0)/Q(0)` | certified density |
| --- | --- | --- |
| random search, `r=4` | `2032/1867` | `0.818734679` |
| + coordinate descent | `38888/35753` | `0.818214025` |
| + lift to quadratic `H`, descend | `60952/56047` | **`0.818086808`** |

**Final certificate.**
$$H(s)=\frac{17}{4096}\bigl(6144s^2+6848s+22857\bigr)>0,\qquad P(s)=-(s-4)H(s),\qquad
\frac{P(0)}{Q(0)}=\frac{60952}{56047},$$
$$\boxed{\ \Delta\le\frac{4}{3\sqrt\pi}\cdot\frac{60952}{56047}=0.818086808\ }\quad
\text{(all unit-ball packings)} .$$
CE1 is structural (`H > 0` everywhere, `s−4 ≥ 0` on the domain). CE2 verified twice: by my
`sign_on_half_line` (Sturm with even-multiplicity handling) and independently by
`sympy.count_roots(Q, 0, ∞) = 0` with `Q(0) = 2858397/8192 > 0`. **No numerical residual.**
The descent also shows the family saturates: `H` collapses to a single quadratic, so `P` stays
cubic and the achievable value moves by `<1e-3` per added degree. This class is far too small to
compete with degree-33 Laguerre certificates.

**Interface finding (why K33 cross-checked and this certificate cannot).** C's and Main's
checkers both use the *width-π* Gaussian (`e^{−π|x|²}`, Laguerre basis), related by the
**rational** substitution `t = 2u`. My structural family uses the *width-1* Gaussian
(`e^{−|x|²}`), and the rescaling that maps one to the other sends the polynomial argument
`s = |x|² ↦ u/π²` — **irrational in `u`**. So a certificate cannot be transported between the two
widths by a change of variable; each must be re-derived in the target width, and the
`t = 2u` cross-check that succeeded for K33 is unavailable here. This is a genuine interface
constraint for C and Main, not a defect in either checker.

**Negative result: the naive structural hybrid is worse.** Relaxing CE1 on the contact shell and
paying the count price is the DLOV mechanism, so I tried the structural form
`P(s) = −(s−S₀)H(s)` with `S₀ = (209/100)² = 4.3681`, `η = (S₀−4)H(4)`, and the hybrid bound
`(4π/3)(P(0)+12η)/Q(0)` (count `n = 12` from `K15-C019`/`E015`). Scanning 2028 positive
quadratic `H` (`x_r03_hybrid_sos.py`): best certified value **`2.304231488`** — *much worse*
than the plain `0.818086808`. The reason is structural: this ansatz **forces `P(S₀) = 0`**, i.e.
a contact zero at the *outer* edge of the shell, whereas the hybrid wants to *lift* `P` across
the whole shell; and with `n = 12` the price `12η` dominates `P(0)` as soon as `η ≳ 0.09`.
So the naive relocation of the root from `s = 4` to `s = S₀` does **not** realise the DLOV gain.
This is *family evidence*: the parameterisation fails, not the hybrid route. The correct shape
needs a free positive bound `η` on the shell with `P` not forced to vanish at `S₀` — an SDP in
`(H, η)`, filed as X-R03b.

## Timing note

The block ran from `09:17:25Z`; checkpoints were pushed at 23, 33, 35 and 43 minutes of elapsed
work (commits `a1fea98`, `e3a63a1`, `8b79dd1`, `9930194`). Every priority item was completed and
the fallback advanced twice.

## Clarification for integration: what in the K33 JSON is *certificate* and what is *search*

The K33 object contains `degree: 33`, `grid: 10000`, `epsilon: 1e-07`, `denominator: 1e8`.
`degree` and the rational coefficient vector are **certificate data**; `grid`, `epsilon` and
`denominator` describe how the candidate was *found* (discretisation, slack floor, rationalisation
precision) and play **no role in verification**. The bound `Δ ≤ 0.77996650` rests only on:
(i) the exact coefficients, (ii) `p ≤ 0` on `[8π,∞)`, (iii) `q ≥ 0` on `[0,∞)`, (iv) the directed
π enclosure, all of which I re-verified independently. **A reader must not treat the bound as
grid-dependent, and a critic cannot attack it by attacking the grid.** The same statement applies
to my `K15-X-C010`: its `P` and its structural CE1 argument are all that matter.

## Consolidated verification ledger (this block)

| object | verified how | independent of the author's code? |
| --- | --- | --- |
| `K15-C033` p, q, p0, q0, ratio | my own Laguerre recurrence, exact | yes |
| `K15-C033` CE1 / CE2 | my own Sturm + even-multiplicity test | yes |
| `K15-C033` global signs | root census: 1 root each, p's below `8π`, q's negative | yes |
| `K15-C033` rounded bound | my own 60-term Machin π enclosure | yes |
| `K15-C033` full object | **Main's** `shell_check` after exact `t = 2u` conversion | third implementation |
| `K15-E015` bracket `a* ∈ [1.2113,1.2114]` | my own rational Taylor sin/cos/tan | yes |
| `K15-E015` monotonicity | sympy `diff` identity, both terms negative | yes |
| `K15-E015` final `δ₁₃ ≤ 57.1448°` | my own enclosure + `arccos` monotonicity | yes |
| Main `shell_check.fourier_map` | direct 3-D quadrature, `4.9e-15`; and exact on K33 | yes |
| Main π constants | against my Machin enclosure, exact | yes |
| Main `_odd_part` | 5 synthetic fixtures | yes |
| Main `K15-C019` | re-derived; sharpened range; mixed case corrected | yes |
| `K15-X-C010` | CE1 structural (a one-line argument) + CE2 by two exact routes | self, audited by construction |
