# Computation results — CE control and strengthened-candidate evaluator 1

Status of every number below: **TESTED_FINITE**. Sign conditions are checked on finite
grids; none of these is a certificate. Branch `kepler15/comp-01a1d8c0`, source commit
`69f3213aa6f2b636ec1b0e25a7394acfecae986b`.

## 1. The CE control, reproduced

`ce3_baseline.py`, radial Gaussian–Laguerre basis `L_k^{1/2}(2 pi r^2) e^{-pi r^2}` with
eigenvalue `(-1)^k`, degree `K` odd, sign conditions on a `grid`-point grid over
`r in [1, 5]` and `s in [0, 5]`, HiGHS LP, `f(0) = 1`.

| K | grid | `rho_A <=` | `Delta <=` | gap to Kepler | reference |
| --- | --- | --- | --- | --- | --- |
| 11 | 400 | 1.4920159 | 0.7812177 | +5.501% | |
| 25 | 900 | 1.4891 | 0.7797128 | +5.297% | |
| 31 | 1200 | 1.4891220 | **0.7797024** | **+5.297%** | |

Reference values in the same units (`k15conv.py`):

| quantity | `Delta` | `rho_A` | gap to Kepler |
| --- | --- | --- | --- |
| Kepler (exact) | 0.740480490 | 1.414213562 | 0 |
| CDS22 lattice-only three-point | 0.741506 | 1.416172 | +0.139% |
| dodecahedral (Hales–McLaughlin) | 0.7546974 | 1.441366 | +1.920% |
| CDS22 general three-point | 0.770271 | 1.471109 | +4.023% |
| **Li 2024 lower bound on the CE optimum** | **0.770657** | **1.471847** | **+4.080%** |
| DLOV14 strengthened two-point | 0.773080 | 1.476474 | +4.403% |
| CE03 published (`m = 6`) | 0.779747 | 1.489207 | +5.303% |
| **this computation, `K = 31`** | **0.7797024** | **1.4891220** | **+5.297%** |

Reading of the table, which is the substantive point of the control:

* Our numerically optimised value lies **just below** CE03's `0.779747` (by `0.006%`), and
  **above** Li's rigorous floor `0.770657`. Both inequalities are in the correct direction
  and together they say: the CE LP optimum in `d = 3` is within about `0.006%` of CE03's
  `m = 6` construction, and is at least `4.08%` above the Kepler density. **The CE route is
  closed as a route to the bound**, exactly as Li's Theorem 6.1 requires.
* Our value is *not* rigorous. CE03's is. The comparison is informative only because the
  two are different kinds of object, and the note above says so.

Sign diagnostics for the stored `K = 31` optimum (`out/ce3_K31_g1200.json`):
`max f = +2.50e-11` at `r = 1.640` on `[1, 12]`; `min fhat = -1.43e-08` at `s = 1.304`
on `[0, 12]`. Both are near-tangency artefacts of a solution that is pushed against its
constraints; they are the reason the status is `TESTED_FINITE`.

## 2. Strengthened-candidate evaluator 1: the equality-case-constrained inverse problem

Route R3 as usually proposed: if a sharp certificate must vanish on every FCC shell and its
transform on every dual BCC shell (Cohn–Elkies 2003 §5), *prescribe those zeros* and solve
the inverse problem. `ce3_constrained.py`, `K = 25`, grid 900, same grid as the control:

| additional constraints | `Delta <=` | ratio to Kepler |
| --- | --- | --- |
| none (control) | 0.7797128 | 1.0530 |
| `f = 0` on the first 2 FCC shells | 0.7993396 | 1.0795 |
| `f = 0` on the first 4 FCC shells | 0.8001330 | 1.0806 |
| `fhat = 0` on the first 2 dual shells | 0.8417867 | 1.1368 |
| `fhat = 0` on the first 4 dual shells | 0.8455793 | 1.1419 |
| both, 1 shell each | 0.8051097 | 1.0873 |
| both, 2 shells each | 0.8752871 | 1.1821 |
| both, 3 shells each | 0.9056000 | 1.2230 |

**Result: negative, and quantified.** Prescribing the *necessary* zero conditions does not
approach the Kepler density; it moves the value from `+5.30%` to `+8%` (primal zeros only),
`+14%` (dual zeros only) or `+22%` (three shells of each). This is not a numerical accident:
the constraints shrink the feasible set of a minimisation, so the optimum can only increase.
The table's value is that it prices the route: the equality-case data are not merely
unattainable (Li), they are *expensive*, and the dual (Fourier-side) conditions cost about
twice as much as the primal ones.

Consequence for the project, to be recorded as a claim: **an "inverse problem" that starts
from the forced zero set cannot produce the Kepler bound, and its failure is monotone in the
number of imposed shells.** Any route that earns the bound must add information *beyond*
ordinary two-point positivity (a local/geometric constraint, a higher-point kernel, or a
genuinely different mechanism), which is the same conclusion Li's obstruction forces from
the other side.

## 3. What this directory does not do

* No rigorous bound: no global sign argument, no interval covering, no certified tails.
* No three-point or higher-point optimisation (the evaluator that would risk beating `0.770271`).
  That is request `K15-COMPUTE-002`, and it is the natural next evaluator.
* No claim about non-periodic packings: the CE theorem itself covers them, but nothing here
  re-proves that extension.
