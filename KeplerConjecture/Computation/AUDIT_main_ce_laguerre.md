# Audit: `Main/ce_laguerre.py` (Main commit `a08f378`)

Read against the supervisor review. I confirm the review's central finding and add one
further reason its conclusion is invalid.

## 1. The Fourier-positivity matrix is built and then never used

`M_hat` and `M_hat_s` are constructed (the `q >= 0` constraint matrix) and then appear in
**neither** `linprog` call:

* `res_free` passes `A_ub=M_f_s` only;
* `res_floor` passes `np.vstack([M_f_s, ...])` only.

So condition (A2), `fhat >= 0`, is enforced nowhere. Half of the Cohn–Elkies hypotheses
are missing from both runs.

## 2. The reported "unbounded ray" cannot exist

`bounds=B = [(-1e6, 1e6)] * (n+1)` is a bounded box, so the feasible set is bounded and no
unbounded ray exists; the recorded HiGHS status is `0` (optimal), not "unbounded". The
`conclusion` string therefore mis-describes the solver output on two counts, and the
inference "the grid conditions are vacuous / do not submit grid baselines" does not follow.
With (A2) restored the grid LP is well posed — my own baseline (`ce3_baseline.py`) solves
the two-sign version and returns `Delta <= 0.7797`, and now an exact checker
(`exactcert.py`) certifies `Delta <= 0.78011` with no grid assumption at all.

## 3. Further defect: the "rigorous floor" is misapplied

The floor used is `f(0) >= 3/(32 pi)`, from `fhat(0) = int f = 1` and `f <= 0` off `B_2`,
via `1 <= f(0) vol(B(0,2))`. This is a valid bound on `f(0)` for a *fully feasible* CE
function, but as implemented it is added as an extra constraint on a relaxation that is
missing (A2); in that setting it is not a floor on the object being optimised, and the
report that the floored optimum "is the floor itself" reflects the missing constraint, not
a property of grids.

## 4. Conventions: reconciled, and they agree

Main's basis and mine are the same object under `x -> 2x`:

| | Main | Computation |
| --- | --- | --- |
| separation | 2 | 1 |
| sign region | `t >= 8*pi` | `t >= 2*pi` |
| objective | `c = 3*Delta/(4*pi)` (centre density) | `rho_A` (centre density) |
| relation | `t_main = 4 * t_comp`, `rho_A = 8 * c` | |
| density | `Delta = (4*pi/3) c` | `Delta = (pi/6) rho_A` |

Both give `Delta = (4*pi/3) f(0)/fhat(0)` in their own convention, and
`(4*pi/3)(f(0)/fhat(0))_sep2 = (pi/6)(f(0)/fhat(0))_sep1` under `g(x) = f(x/2)`, since
`ghat = 8 fhat(2·)`. **The conventions are consistent; only Main's missing constraint and
conclusion are wrong.**

## 5. Not in dispute

The docstring's warning that a discretised LP is not a certificate is correct and is the
reason `exactcert.py` exists: it removes the discretisation from the *verification* while
leaving it in the *search*.
