# Shell-bench: the count-strengthened two-point bound in dimension 3

`shell_bench.py`, run 2026-11-15. **Every number here is `TESTED_FINITE`.** The shell
hypothesis is **CONDITIONAL**. Nothing below is a certificate.

## What is computed

Unit balls, separation 2. With `fhat >= 0`, `eta >= 0`, `f <= eta` on `2 <= |x| <= rho`,
`f <= 0` for `|x| >= rho`, and the **conditional** assumption that at most 12 centres lie
within distance `rho` of any centre, the chain derived in the file header gives

\[
\Delta \;\le\; \frac{4\pi}{3}\,\frac{f(0)+12\eta}{\widehat f(0)} .
\]

Framework: de Laat–de Oliveira Filho–Vallentin count-strengthening, Forum Math. Sigma **2**
(2014) e23, arXiv:1206.2608. Same Laguerre basis and same degree as the `eta = 0` control,
so the comparison is not confounded with degree.

## Headline result: the shell allowance is not used

| degree | `eta` chosen | `eta`-shell bound | same-degree `eta=0` control | gain | held-out signs |
| --- | --- | --- | --- | --- | --- |
| 13 | 0 | 0.78496246 | 0.78496246 | **0** | both pass |
| 21 | 0 | 0.78017286 | 0.78017286 | **0** | exterior FAILS |
| 31 | 0 | 0.77977709 | 0.77977709 | **0** | exterior FAILS |
| 41 | 0 | degenerate (objective −629021) | same | **0** | both FAIL |

And at fixed degree 21, sweeping the shell width:

| `rho` | `eta` chosen | gain |
| --- | --- | --- |
| 2.09 | 0 | 0 |
| 2.30 | 0 | 0 |
| 2.60 | 0 | 0 |
| 2.83 | 0 | 0 |

**So the count-strengthening with 12 neighbours buys exactly nothing in this family, at
every degree and every shell width tested.** The LP sets `eta = 0` and returns the ordinary
CE optimum. This meets the roadmap's R2 redirect criterion — "no numerical strength is
demonstrated" — and the reliable reading is *not* "the framework is empty" but "the
multiplier 12 is too large relative to what relaxing one constraint can buy": the objective
charges `12 delta` per unit of allowance, whereas relaxing a single active constraint can
lower `f(0)` by at most about `delta`. To make the trade favourable one needs the count to
enter with a much smaller coefficient, i.e. a *local* statement about which of the 12
neighbours can be at the far end of the shell, not a uniform count.

## The held-out tests earn their place

`eta = 0` is only half the story. At `K = 13` the held-out shell and exterior sign checks
both pass. At `K = 21` and `K = 31` the **exterior held-out check fails**: the optimised
candidate is positive somewhere on `[2*pi*rho^2, Tmax]` at points the optimisation grid did
not sample. At `K = 41` the LP collapses to `f(0) = -6.3e5`, which is impossible for a real
certificate (`fhat >= 0` forces `|f| <= f(0)`), and the held-out test catches it too.

The lesson is the one the roadmap asks to keep explicit: **raising the degree only helps if
the grid is refined with it**, and a finite-grid objective can be driven below any target by
under-resolution. The only value in this table that is both feasible-looking and
sign-clean on held-out points is `Delta <= 0.78496246` at `K = 13` — still `+4.45%` above
Kepler and still not a certificate.

## What was actually run

```bash
cd KeplerConjecture/Computation
python3 shell_bench.py --degree 13 --grid 500 --n-shell 250 --out out/sb_K13.json
python3 shell_bench.py --degree 21 --grid 500 --n-shell 250 --out out/sb_K21.json
python3 shell_bench.py --degree 31 --grid 500 --n-shell 250 --out out/sb_K31.json
python3 shell_bench.py --degree 41 --grid 500 --n-shell 250 --out out/sb_K41.json
for R in 2.09 2.3 2.6 2.83; do
  python3 shell_bench.py --rho $R --degree 21 --grid 500 --n-shell 250 --out out/sb_rho$R.json
done
```

Each run is under 2 s and under 200 MB. The defaults (`--degree 13 --grid 600 --n-shell 300
--Tmax 120`) are the small local instance the assignment asked for.

## Implemented details the assignment required

* **Row and column scaling.** Columns are scaled by their sup-norm over all three grids,
  rows by their post-column-scaling sup-norm; both exponents are written to the JSON
  (`column_scaling`).
* **Three grids**: the shell `[8pi, 2pi rho^2]`, the exterior `[2pi rho^2, Tmax]`, and the
  dual grid for `fhat >= 0` on `[0, Tmax]`. The dual grid was missing from my first draft —
  without it the LP has no Fourier positivity at all, the same defect I audited in
  `Main/ce_laguerre.py`, so it is worth recording that I reproduced it and caught it here.
* **Held-out sign tests** on grids from a *different* sampling scheme (uniform on the shell,
  power-law on the exterior), disjoint from the optimisation grid, plus the values at the
  contact radius `|x| = 2` and at `|x| = rho`.
* **Honest solver statuses**: `solver_status` and `solver_message` are stored per case, and
  infeasible/degenerate outcomes are kept rather than dropped.
* **Coefficients, objective and gap** are stored per case, in occupied-volume density, with
  gaps to Kepler and to `0.779747`.
* `conditional_on_shell_count = true` is written into every JSON.

## Not done, and honestly so

* No global sign or tail certificate: the polynomial sign on `[Tmax, infinity)` is not
  discharged, and a compact-interval exponential bound plus tail estimate is a separate
  obligation. Polynomial-only checking does not close it.
* The shell lemma at `rho = 2.09` remains Experimental's task. Everything here is
  conditional on it.
