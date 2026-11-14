# ZetaFive progress

## 14 November 2026

Published an [exponent catalog](EXPONENT_CATALOG.md) for the original $K=40n$, $N=3n$, $h=37n$, $D_N^6$, $M=200$ construction and its proposed extension from $k=5$ to $k=7$.

- The catalog preserves the comparison table, links the relevant results in Fauzan and Lai, and derives the contributions from small primes, the compact inner range, the tail, the outer range, and the real estimate.
- Exact rational reconstruction gives an arithmetic increase of $751/768$, and the adapted final upper-bound coefficient is $+0.960456781075\ldots$. This estimate does not establish the decay needed for irrationality.
- `node ZetaFive/Computation/exponent_catalog.mjs` passes: it reconstructs the inner integral on 143 intervals, both outer integrals, the row-weight costs, and the reported totals without floating-point arithmetic.
- Claim status: the $k=7$ local determinant estimates still require uniform verification. The computation verifies the accounting, not a proof of irrationality or an impossibility result for other constructions.

## 2026-11-14 — Correspondence lemmas for the parallel constructions

**Outcome.** Added a small compiling ZetaFive Lean library that proves the exact
algebraic correspondences of *One summation functional, one Gram pencil*
(14 November 2026), requested as correspondence lemmas rather than a new
irrationality proof. New modules under `ZetaFive/Lean/Correspondences/`
(`Basic`, `Transport`, `AffineParameter`, `Matrix`) plus the aggregator
`ZetaFive.lean` and a `ZetaFive` Lake target in `lakefile.toml` (existing
targets untouched).

Proved (20 declarations, axioms only `propext`, `Classical.choice`,
`Quot.sound`, no `sorry`/`admit`/`native_decide`):

* Target 1: `μpoly_eq_τ_pull` (`μ(P) = τ(x^5 P(-x²))` on `ℚ[t]`), the monomial
  calculus `τ_C_mul_X_pow`, the partial fraction
  `x^5/(j²-x²) = -x³ - j²x - (j⁴/2)(1/(x-j)+1/(x+j))`, the pole-value
  comparison `τX_single_pole_transport` (recovers
  `j⁴(X-H_j^{(5)}) - 1/4 + 1/(2j)` via `H_j - H_{j-1} = j^{-5}`), and the sanity
  values `τ(x³) = 1/4`, `τ(x⁴) = -1/2`, `μ(1) = 5/12` (the last two pin the
  Bernoulli convention `B_1 = -1/2`).
* Target 2: `mu_affine` (`μ_u(R) = μ_v(R) + (u-v)Λ(R)`) with `Λ(R) = Σ c_j j⁴`,
  plus `laurent_pole_expansion`/`laurent_pole_coeff` giving the explicit finite
  expansion behind the `[t^{-3}]_∞` reading.
* Target 3: `weight_cancellation` (`D_N^6/D_K = W/T`), `gramMatrix_affine`
  (entrywise pencil `G(u) = G(v) + (u-v)M` for domain-valued entries),
  `det_congruence` (`det(CᵀGC) = (det C)² det G`), and
  `det_add_smul_eq_det_mul`.

**Not proved (visible obligations, nothing assumed).** Assembly of the general
representation-level transport `μ_X(R) = τ_X(x^5R(-x²))` from its polynomial and
single-pole cases (`OBL-assembly`); the `RatFunc ℚ` reading of the partial
fraction; a Laurent-coefficient functional; concrete `D_m, W_K, T_K` and domain
membership of `W_Kpq/T_K`; and everything analytic, spectral, p-adic and
energetic. Full list in `ZetaFive/Main/CORRESPONDENCES_STATUS.md`.

**Build.** Six modules elaborated with `lean` (exit 0 each) against the
Mathlib 4.33.1 snapshot at `/opt/mathlib`, with the repo root on `LEAN_PATH`;
log in `ZetaFive/Main/correspondences-build-log.txt`. `lake build ZetaFive`
could not run here: the checkout pins toolchain v4.35.0 and Mathlib v4.35.0,
which are absent from this VM, and Lake begins by cloning and building Mathlib
(hours). Re-running `lake build ZetaFive` with the pinned toolchain is the
outstanding build step.

**Review.** No delegation tool was available, so the coordinator, functional
worker, matrix worker and reviewer roles were executed sequentially by one
agent. Signs, the Bernoulli convention, zero denominators, the `1 ≤ j`
restriction, and variable naming were re-checked by hand; the transport theorem
is not definitional in `μ`, and `pull` never occurs in a definition.
