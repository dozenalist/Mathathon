# Shell proposer, block K15-HOUR-20261114-C — status: no exact candidate (explicit failure)

**Bottom line: the proposer is implemented and runnable, and it produced no candidate that
Main's checker accepts.** The failure is attributed to the proposer, not to the mathematics:
four implementation defects were found and fixed in this file alone during the block, so a
fifth is the more likely explanation than a mathematical obstruction. The earlier Laguerre
result (`K15-C-SHELLBENCH-001`: `eta = 0`, gain exactly 0) therefore stands **unconfirmed and
unrefuted in Main's basis** — it is not corroborated by this block.

## What was built

| file | role |
| --- | --- |
| `shell_propose.py` | proposer: solves the LP in the well-conditioned Laguerre basis, converts exactly to Main's monomial basis `u = π|x|²`, hands the result to `shell_check` for the verdict |
| `shell_sos.py` | the same LP built *directly* in Main's monomial basis — retained because it reproduces the `K15-C022` failure mode and documents why that architecture does not work |

Both take `--checker /path/to/shell_check.py`, use Main's own exact predicates
(`nonneg_on_half_line`, `le_on_interval`, `_ray`), and label the count hypothesis
(`n=27, ρ=2.05` unconditional by `K15-C013a`; `n=12, ρ=2.09` conditional on `K15-C019`).

## The four defects found (all in my code, none in Main's checker)

1. **`T_HI` is not `27/2` for every `ρ`.** `shell_check.check()` hardcodes `T_HI = 27/2`,
   valid for `ρ = 2.09` (`πρ² = 13.72`) but **invalid for `ρ = 2.05`** (`πρ² = 13.20 < 13.5`).
   `shell_propose.py` therefore calls the parameterised predicates with
   `T_HI(ρ) = ⌊π_lo ρ²⌋` computed from a rational lower bound for `π`.
2. **Even degree is impossible in Main's basis too.** `M` is upper triangular with diagonal
   `(−1)^i`, so `lc(q) = (−1)^K a_K` and `lc(p) = a_K`; `p ≤ 0` at infinity needs `a_K ≤ 0`
   while `q ≥ 0` needs `(−1)^K a_K ≥ 0`. Both hold only for `K` odd. Verified numerically:
   `M[K][K] = (−1)^K`. Both scripts now refuse even degree.
3. **The `q(u)` coefficient row is `mono(u)·M`, not `mono(u)·Mᵀ`** — since
   `q(u) = Σ_k a_k (Σ_i M_{ik} u^i)`. The transpose version silently constrained a different
   polynomial.
4. **Column-scaling recovery is `c = x/c_w`, not `x·c_w`.** I "fixed" this in the wrong
   direction mid-block and the checker caught it immediately (`q(0) = 1.62` where `q(0) = 1`
   was imposed). Recorded because the checker catching my inversion is exactly what it is for.

## The remaining failure

With the corrected proposer the exact verdicts are: **shell constraint PASS, exterior ray
PASS, `q ≥ 0` FAIL**, with `min q ≈ −1.8` near `u ≈ 21.5` although the LP constrains `q ≥ 0`
on a grid of ~5000 points over `u ∈ [0, 40]`. Densifying the dual grid to 6000 points did not
fix it, which points to a still-unresolved mismatch between the grid the LP constrains and the
polynomial the checker evaluates — not to a genuine obstruction. **Unresolved.**

## Why the monomial basis is the wrong place to optimise (independent of my bugs)

`M[0][k] = (2k+1)!!/2^k`, so `M[0][7] = 15836`: producing a small `p(0)` requires cancelling
large coefficients, and `p` is a polynomial in `u` whose values at `u = 40` are ~`40^K`. The
LP built directly in that basis (`shell_sos.py`) returns box vertices with
`p(0) → −∞` — a re-derivation of `K15-C022`. Main's `C-SHELL-001c` note warns of this; the
measurement here confirms it and gives the cause.

**Recommendation for Main:** keep `shell_check.py` as the *certifier* (it is exact and its
parameterised predicates are usable), but do not optimise in its basis. The architecture in
`shell_propose.py` — propose in Laguerre, convert exactly, certify in the monomial basis — is
the right one and needs one more debugging pass, not a redesign.

## What is *not* claimed

No bound from the shell hypothesis. `n = 12` remains conditional on the Tammes-13 enclosure;
`n = 27` at `ρ = 2.05` is unconditional but the proposer produced nothing for it to apply to.
