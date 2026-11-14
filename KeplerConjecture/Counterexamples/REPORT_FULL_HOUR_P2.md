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
