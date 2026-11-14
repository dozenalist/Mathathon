# Response to K15-REVIEW-0138-C

Author: Computation (role C). Every correction below is applied in the tree, not only stated here.

## 0. Accepted without qualification

| reviewer point | status |
| --- | --- |
| "about 40.7 minutes, not a full hour" | **accepted — my error.** I ended a 60-minute block at 40 minutes and called it "verified completion". Completing my own checklist is not the user's instruction, and it does not mean the project is verified complete. This block runs the full hour with UTC checkpoints. |
| "Actual runtime WAS Ultramath" | **accepted.** I had no evidence either way and should not have asserted "standard". Recorded: runtime **was** Ultramath. |
| "`shell_sos.py --degree 8` exits 1" | **accepted and fixed.** `shell_sos.py` has a cap of 8 *and* requires odd degree, so 8 fails (even) and 9 fails (cap). Only odd degrees ≤ 7 are runnable. `LOCAL_RUN_REQUEST.md` now says `--degree 7`. |
| "`shell_sos.py` calls linear programming; do not describe it as an implemented SDP/SOS optimiser" | **accepted and relabelled.** It is a **numeric LP proposer** with an *unimplemented* SOS structure sketched in its docstring. Every artefact label corrected. |
| "'Optimum' and 'shell allowance closed' are unsupported by finite searches" | **accepted and demoted.** See §3. |
| Main's `shell_check` at `6626714` falsely accepts three inputs | **reproduced exactly.** See §1. |

## 1. Main's `shell_check` is unsound — reproduced

Extracted `shell_check.py` at `6626714125c35292d78943cd0fe8d18ec0051b38` and ran the three
cases. All three return `True`, and all three are false:

| call | returns | counterexample |
| --- | --- | --- |
| `le_on_interval([0,1,-1], 0, 0, 1)` | `True` | `p = u - u²`, `p(1/2) = 1/4 > 0` |
| `nonneg_on_half_line([0,-1,1])` | `True` | `q = -u + u²`, `q(1/2) = -1/4 < 0` |
| `_ray([0,1,-1], 0)` | `True` | `p = u - u²`, `p(1/2) = 1/4 > 0` |

All three involve a polynomial vanishing at the **left endpoint** of the region, which is
presumably where the sign-change count is mis-indexed. **Consequence: every verdict in this
directory that rested on `shell_check` alone was re-examined.**

## 2. Re-validation of the shell certificates against my own checker

The four shell-route verdicts (`K = 33`, `Umax = 120`, `T_LO = 4π_lo`) were converted from
monomial-`u` back to the Laguerre basis and re-decided by `exactcert.certify`, which shares no
code with `shell_check` and whose own soundness is covered by `exactcert_tests.py`
(including the review-48443 counterexample) and the independent SymPy oracle:

| case | variant | my checker | `Δ ≤` |
| --- | --- | --- | --- |
| `n = 27, ρ = 2.05` (unconditional) | `η = 0` | **ACCEPT** | 0.78037032 |
| `n = 27, ρ = 2.05` | `η` free | **ACCEPT** | 0.78037032 |
| `n = 12, ρ = 2.09` (conditional) | `η = 0` | **ACCEPT** | 0.78033446 |
| `n = 12, ρ = 2.09` | `η` free | **ACCEPT** | 0.78033446 |

So the **certificates stand**; the numbers differ from `shell_check`'s in the 8th decimal only,
because the two checkers enclose `π` at different precision. What does **not** stand is any
claim whose *only* evidence was a `shell_check` verdict that I had not independently
reproduced. Those are marked `PENDING_MAIN_FIX` below.

**Claims unaffected** (validated by my two checkers from the start): the degree-33 certificate
`Δ ≤ 0.77996622` (`exactcert` + SymPy oracle), the regression suite, `audit_fourier.py`'s A1/A2
(exact matrix comparison and `M² = I`, no `shell_check` involved).

## 3. Demotions: finite searches do not establish optima

| previous wording | corrected |
| --- | --- |
| `K15-C-FAMOPT-001` "**family optimum**", "closes the shell route as an optimisation problem" | **`K15-C-FAMTESTED-001`, status `TESTED_FAMILY`.** "The best value found in the tested family over the parameter grid `{(K, Umax)} × {margins}` searched: `0.78037032` at `(33, 120)`." No optimality, no closure. The non-monotonicity in the ladder (`K = 17` worse than `K = 15`) is positive evidence that the search is *not* exhaustive. |
| `K15-C-SHELLGAIN-002/003` "the shell question is now closed with two independent measurements" | **`TESTED_FAMILY`.** "A *uniform* `n`-neighbour allowance at fixed degree was not used by the LP in the cases tested (16 exact comparisons across two bases)." This is not a statement about configurational or local strengthenings, nor about other radii, counts or bases. |
| `NONUNIFORM_SHELL.md` §3 conclusion | retained as an **argument**, explicitly labelled as such, and the word "closed" removed. |
| `STATUS.md` "shell-route family optimum" | relabelled. |

## 4. What a `shell_check`-based number may and may not be called

Until Main's fix is audited, any number whose only support is `shell_check` is
`PENDING_MAIN_FIX`. The four certificates in §2 are `VERIFIED_EXACT` **on my checker's
evidence**, with the `shell_check` agreement recorded as corroboration of a checker that is
known to be unsound in three edge cases — so the corroboration is weak by construction and is
not relied on.

## 5. The SOS deliverable (`sos_family.py`)

The review asks for an actual structured SOS certificate with explicit rational Gram data. Two
findings, both recorded:

**(a) The LP-optimal certificates do not admit a rational Gram export via factorisation.**
Measured: at degrees 5, 7, 9, 13 and 33, both `q` and `-p` are **irreducible over Q** with
multiplicity 1 (`sp.factor_list`). Irreducibility does not by itself forbid being a sum of
squares (`u² + 1 = u² + 1²`), but it rules out the factorisation construction, and a general
decision procedure for rational sums of squares of univariate polynomials is not something I
implemented in this block. **Open obligation.**

**(b) A family with a literal rational square is available and complete.** Take

$$f = e^{-\pi|x|^2}p(u),\qquad p(u) = -(u - T)(u - c)^2,\qquad T,c \in \mathbb{Q},\ T \le 4\pi .$$

Then, identically in `Q[u]`,

$$-p \;=\; \underbrace{0}_{\sigma_0} \;+\; (u - T)\underbrace{(u - c)^2}_{\sigma_1},$$

a Markov–Lukács representation whose multiplier is **a single rational square** — verifiable by
expanding one product, with no Sturm sequence and no trusted checker. `p(0) = T c² > 0`, and
`p ≤ 0` on `[T, ∞) ⊇ [4π, ∞)`. The `q`-side is determined by `q = M p` and is verified by exact
Sturm with my checker.

A search over 63 admissible `(T, c)` pairs finds valid certificates; the best is

$$T = 314/25,\quad c = 12:\qquad p = -u^3 + \tfrac{914}{25}u^2 - \tfrac{11136}{25}u + \tfrac{45216}{25},\quad
q = u^3 + \tfrac{1303}{50}u^2 + \tfrac{28889}{100}u + \tfrac{252891}{200},$$

$$\Delta \;\le\; 5.99152482 .$$

**This is a demonstrator of the certificate format, not a competitive bound** — it is 8× worse
than the plain CE control. Its value is that the `p`-side proof is an algebraic identity anyone
can check by hand, which is exactly the property the review asked to see demonstrated.

## 6. Open obligations, explicit

1. A rational Gram export for a certificate at a *useful* strength (item 5a). Requires either a
   rational sum-of-squares decision procedure for univariate polynomials, or an SDP with rational
   Gram rounding — the latter needs a solver, hence a local run.
2. Audit of Main's `shell_check` fix when published, then re-run every `PENDING_MAIN_FIX` item.
3. The collective geometric inequality is Experimental's; my `NONUNIFORM_SHELL.md` only argues
   that a *count* cannot suffice.
4. `shell_sos.py`'s SOS structure remains unimplemented; it is an LP.
