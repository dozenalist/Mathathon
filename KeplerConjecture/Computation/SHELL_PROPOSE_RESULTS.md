# Shell proposer — final status: exact candidates and a resolved answer

Supersedes the earlier "explicit failure" version of this file (kept in git history at
`5f2fb34`; the five defects it recorded are all real and are listed in §4 for the record).

## Headline

At degree 9, in Main's basis `u = π|x|²`, with verdicts from Main's own exact checker
`shell_check.py`:

| case | `η` chosen | exact verdict | `Δ ≤` |
| --- | --- | --- | --- |
| `n = 27`, `ρ = 2.05` (**unconditional**, K15-C013a) | 0 | PASS | **0.87227746** |
| `n = 27`, `ρ = 2.05`, allowance free | **0** | PASS | 0.87227746 |
| `n = 12`, `ρ = 2.09` (conditional, K15-C019) | 0 | PASS | **0.87227746** |
| `n = 12`, `ρ = 2.09`, allowance free | **0** | PASS | 0.87227746 |

**Gain from the allowance: exactly 0 in both cases.**

This is an *independent confirmation of `K15-C-SHELLBENCH-001`*: the earlier measurement was
made in the Laguerre basis in `t = 2π|x|²` with my own checker; this one is in Main's monomial
basis in `u = π|x|²` with Main's checker, a different Fourier matrix and different Sturm code.
Two independent implementations now agree that the shell allowance is not used.

**What the two numbers are worth.** `0.87227746` is a genuine exact certificate — every
packing satisfies it, the sign conditions being decided by exact Sturm over `Q` with rational
`π` enclosures in the safe direction. It is *far* worse than Cohn–Elkies' `0.779747` because
`T_LO = 12 < 4π = 12.566` and a margin `ε_q ≥ 1e-5` is needed on `q ≥ 0` for the rational
rounding to survive; both are costs of this route, not of the mathematics. It is **not** a
competitive bound and is not offered as one.

## 1. Why `η` is never used

The constraint set with an allowance is *weaker* than `η = 0` on the shell, but the objective
charges `n·η`. With `n = 12` or `27` the charge is large: to pay for `η`, relaxing the shell
would have to lower `p(0)` by more than `n·η`, and `p(0)` is only about `0.21`. For `n = 27` the
allowance must satisfy `η < 0.21/27 ≈ 0.008` before it can break even, and at such `η` the
relaxation buys nothing. The measurement here makes that quantitative rather than heuristic.

## 2. The architecture that works

`shell_propose.py`:
1. solve the LP in the **Laguerre basis** in `t = 2π|x|²` (well conditioned — see §3);
2. convert exactly to Main's monomial basis: `p(u) = Σ_k c_k L_k^{(1/2)}(2u)`, rational;
3. **cutting-plane refinement**: locate the narrow negative excursions of `q` that a uniform
   grid misses, add their midpoints as constraints, repeat;
4. margin `ε_q = 1e-5` on `q ≥ 0` so that a double root touching zero cannot be exploited
   (without it the LP parks `q` at `min q = -1.1e-07`, which exact Sturm correctly rejects);
5. verdict from `shell_check`'s parameterised predicates.

Step 3 was necessary and is not cosmetic: the final `q` has real roots at `u ≈ 21.504` and
`21.538`, a negative dip of width `0.034`, while a uniform grid at 1500 points has spacing
`0.027` — it can and does step over it.

## 3. `T_HI` is not `27/2` for every `ρ`  (K15-C-THIDEP-001)

`shell_check.check()` hardcodes `T_HI = 27/2`. That is valid at `ρ = 2.09`
(`πρ² = 13.72`) but **invalid at `ρ = 2.05`** (`πρ² = 13.20 < 13.5`). `shell_propose.py`
therefore calls the parameterised predicates (`le_on_interval`, `_ray`) with
`T_HI(ρ) = ⌊π_lo ρ²⌋`. No defect in Main's file — only in using its default outside its range.

## 4. Five defects in my own code, four caught only by the independent checker

1. `T_HI` default misapplied to `ρ = 2.05` (§3).
2. **Even degree is impossible in Main's basis too.** `M` is upper triangular with diagonal
   `(−1)^i`, so `lc(q) = (−1)^K a_K` and `lc(p) = a_K`; `p ≤ 0` at infinity needs `a_K ≤ 0`,
   `q ≥ 0` needs `(−1)^K a_K ≥ 0`. Only `K` odd works. Verified numerically: `M[K][K] = (−1)^K`.
3. **The `q(u)` coefficient row is `mono(u)·M`, not `mono(u)·Mᵀ`.**
4. **Column-scaling recovery is `c = x/c_w`, not `x·c_w`** — I inverted it in the wrong
   direction mid-block and the checker caught it at once (`q(0) = 1.62` where `1` was imposed).
5. **The `η ≥ 0` row had coefficient `+1`,** enforcing `η ≤ 0`; the objective then drove `η` to
   the `−10⁵` box bound and the candidate was rejected with a huge negative "objective".

Defect 5 is the one that mattered most: it is why the earlier version reported "no exact pass
for `η_free`". It is also a warning about negative objectives — a candidate with
`Δ = −4660662` should have been recognised as nonsense immediately, by me, before the checker.

## 5. What is and is not claimed

* Claimed: for every packing of unit spheres in `R³`, `Δ ≤ 0.87227746`, **exact**, conditional
  only on the cited Cohn–Elkies theorem. Also: at degree 9, `η` free gives the identical value,
  so the allowance is not used.
* **Not** claimed: any improvement on Cohn–Elkies. The number is loose by construction.
* **Not** claimed: that `n = 12` at `ρ = 2.09` is available — it remains conditional on the
  Tammes-13 enclosure (K15-C019). The `n = 27, ρ = 2.05` row is unconditional and is the one
  to quote.
