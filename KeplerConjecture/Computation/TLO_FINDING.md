# `T_LO = 12` costs 6.7% of the bound — use `T_LO = 4·π_lo`

**Actionable finding for Main.** `shell_check.py` uses `T_LO = 12` and documents it as a
conservative rational threshold (`12 ≤ 4π`, so requiring `p ≤ 0` on `[12, ∞)` implies it on
`[4π, ∞)`). The implication is correct — the check is *safe* — but it is **not free**. Requiring
`p ≤ 0` on `12 ≤ u < 4π = 12.566…` constrains the polynomial **inside** the ball of radius 2,
where the Cohn–Elkies hypothesis imposes nothing at all. That extra constraint costs about
**6.7% of the bound**.

Measured, same code, same degrees, same checker, only `T_LO` changed
(`shell_propose.py --checker … --degree K [--tlo-exact]`):

| `K` | `T_LO = 12` | `T_LO = 4·π_lo = 12.566370614` | improvement |
| --- | --- | --- | --- |
| 9 | 0.87227746 | **0.82311657** | 5.6% |
| 13 | 0.84002473 | **0.78526369** | 6.5% |
| 21 | 0.83632450 | **0.78062816** | 6.7% |

All rows are `EXACT PASS` from `shell_check`; the allowance gain stays exactly 0 in every row.

**The recommended threshold.** `T_LO = 4·π_lo` with `π_lo = 31415926535/10^10` is still
*conservative in the safe direction*: `4π_lo < 4π`, so requiring `p ≤ 0` on `[4π_lo, ∞)` implies
it on `[4π, ∞)`. Nothing about safety is lost — the sub-interval excluded is measured in
`10^-9` rather than in `0.57`. Main should switch the default, or at least record that the
`12` default makes published numbers pessimistic by ~6.7%.

## Independent confirmation at degree 33

A separate check, which is stronger evidence than the table because the certificate was built by
a different route and is much sharper:

* Take the verified degree-33 certificate `out/verified_certificate_K33b.json`
  (`Δ ≤ 0.77996622`, itself accepted by two independent exact checkers in the Laguerre basis).
* Express it in Main's monomial basis `u = π|x|²`: `a` from `p(u) = Σ_k c_k L_k^{(1/2)}(2u)`,
  then `q = M a` with Main's own `fourier_map(33)`.
* Run Main's predicates.

Result:

| predicate | `T_LO = 12` | `T_LO = 4·π_lo` |
| --- | --- | --- |
| `q ≥ 0` on `u ≥ 0` | PASS | PASS |
| `p ≤ 0` on `[T_LO, 27/2]` | **FAIL** | PASS |
| `p ≤ 0` on `[27/2, ∞)` | PASS | PASS |
| verdict | reject | **ACCEPT, `Δ ≤ 0.77996622`** |

So the degree-33 certificate is valid, Main's checker **agrees** once its own conservative
threshold is not the binding constraint, and the only reason for the earlier rejection was the
`T_LO` default. This is the strongest cross-validation in this directory: a certificate produced
by my Laguerre/Sturm/Yun pipeline, verified exactly, then accepted by another session's
independently written monomial-basis checker.

## Extending the degree at the corrected threshold

Single runs (`shell_propose.py --tlo-exact --degree K`), `n = 27`, `ρ = 2.05`, all
`EXACT PASS`:

| `K` | `Δ ≤` | gap to CE `0.779747` |
| --- | --- | --- |
| 21 | 0.78062816 | +0.11% |
| **25** | **0.78055517** | **+0.086%** |
| 29 | no exact candidate | — |
| 31 | no exact candidate | — |
| 33 | no exact candidate | — |

**Correction — the "saturation" was a finite-horizon artefact, not a limit.** At first degrees
29–33 produced no exact candidate. The cause was located: the LP constrains `p ≤ 0` only on
`[T_HI, Umax]`, and a degree-29 polynomial constrained on `[13.2, 40]` can rise again before the
leading term takes over — measured `max p = 5.4 × 10^46` on `[T_LO, 400]`, far outside the
horizon the LP ever saw. The exact checker, which tests the whole ray, correctly refused.

Raising the horizon repairs it:

| `K` | `Umax` | `Δ ≤` | gap to CE |
| --- | --- | --- | --- |
| 29 | 40 | no exact candidate | — |
| 29 | 120 | 0.78039846 | +0.084% |
| **33** | **120** | **0.78037031** | **+0.080%** |
| 29, 33 | 250 | no exact candidate | numerical conditioning fails at large `u` |

So the limit is conditioning of the monomial basis at large `u`, not a mathematical bound, and
`Umax = 120` is the useful setting. Anyone extending this should raise `Umax` with the degree
rather than concluding that high degree is hopeless.

**The optimum of the family, swept:** `(K, Umax) = (33, 120)` gives `0.78037031`; `(35, 120)`
gives `0.78043244`; `(37, 120)` gives `0.78052696`; `(33, 160)` gives `0.78041926`. Raising the
degree without raising the horizon *worsens* the bound, and raising the horizon alone breaks
conditioning — a genuine two-sided trade-off. **`0.78037031` at `(33, 120)` is therefore the best
exact certificate this pipeline yields**, at `+0.080%` from Cohn–Elkies.

## Consequence for the record

* **`0.78037031` (`K = 33`, `Umax = 120`, `T_LO = 4π_lo`, `n = 27`, `ρ = 2.05`,
  unconditional)** is the best exactly-certified shell-route bound: **0.080%** above
  Cohn–Elkies' `0.779747`, rather than 7% above it.
* The remaining 0.11% is the cost of the mandatory `ε_q ≥ 1e-5` margin on `q ≥ 0` alone, since
  the `T_LO` cost has now been removed.
* Anyone quoting a shell-route number computed with `T_LO = 12` should scale it: the true
  strength of the route is ~6.7% better than that number suggests.
