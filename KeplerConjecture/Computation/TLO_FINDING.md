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

## Consequence for the record

* `0.78062816` (`K = 21`, `T_LO = 4π_lo`, `n = 27`, `ρ = 2.05`, **unconditional**) is the best
  exactly-certified shell-route bound, and it is **0.11%** above Cohn–Elkies' `0.779747` rather
  than 7% above it.
* The remaining 0.11% is the cost of the mandatory `ε_q ≥ 1e-5` margin on `q ≥ 0` alone, since
  the `T_LO` cost has now been removed.
* Anyone quoting a shell-route number computed with `T_LO = 12` should scale it: the true
  strength of the route is ~6.7% better than that number suggests.
