# Theorem and status ledger — ZetaFive correspondence lemmas

Date: 2026-11-14. Checkout: `dozenalist/Mathathon` @ `5f20e2fac14d7f38a56459a2e69d1dd406efaa5e`,
folder `ZetaFive`. Branch: `codex/zeta5-correspondences-2026-11-14`.

Source note: *One summation functional, one Gram pencil* (14 Nov 2026),
Sections 1–4; equation labels below are the note's `\label`s, which refer to
Fauzan's 17 Sep 2026 manuscript.

**Reviewer.** No delegation was available in this session (no sub-agent tools),
so all stages — definitions, functional algebra, matrices, review — were
executed sequentially by one agent and reviewed by self-check. Every claim below
was re-derived by hand and machine-checked; the "hypotheses" column is what the
Lean statement actually requires, not what the note requires.

`#print axioms` was run for all 20 declarations (`correspondences-axioms.txt`);
each output is `depends on axioms: [propext, Classical.choice, Quot.sound]`.
That string is abbreviated below as **AX3**.

| # | Mathematical statement | Lean declaration | Source | Hypotheses | Reviewer | Axioms |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `H_j^{(5)} - H_{j-1}^{(5)} = j^{-5}` | `H5_increment` | §2.1 proof of `prop:axioms` | `1 ≤ j` | self | AX3 |
| 2 | `τ(C c · x^{k+3}) = c(k+1)(k+2)(k+3)B_k/24` | `τ_C_mul_X_pow` | `eq:EM` | none | self | AX3 |
| 3 | `μ(P) = τ(x^5 P(-x^2))` for `P ∈ ℚ[t]` | `μpoly_eq_τ_pull` | `eq:pullback` | none | self | AX3 |
| 4 | `τ(x^3) = 1/4` | `τ_X_pow_three` | §2.1 example | none | self | AX3 |
| 5 | `τ(x^4) = -1/2` (checks `B_1 = -1/2`) | `τ_X_pow_four` | §2.1 example | none | self | AX3 |
| 6 | `μ(1) = 5/12` | `μpoly_one` | §2.1 (`e=0` of the `μ(t^e)` formula) | none | self | AX3 |
| 7 | `x^5/(j²-x²) = -x³ - j²x - (j⁴/2)(1/(x-j)+1/(x+j))` | `rat_pole_identity` | §2.1 displayed partial fraction | field, `[CharZero F]`, `x-j ≠ 0`, `x+j ≠ 0`, `j²-x² ≠ 0` | self | AX3 |
| 8 | `d(j) = j` for `j : ℕ` | `d_natCast` | `eq:poles` | none | self | AX3 |
| 9 | `d(-j) = j-1` | `d_neg_natCast` | `eq:poles` + reflection | none (j = 0 handled) | self | AX3 |
| 10 | `τ_X` of the transported pole `c/(t+j²)` equals `c(j⁴(X-H_j) - 1/4 + 1/(2j))` | `τX_single_pole_transport` | §2.1, `eq:poles`, `eq:pullback` at a pole | `1 ≤ j` | self | AX3 |
| 11 | pole part of `μ_u - μ_v` is `(u-v)Σ_j c_j j⁴` | `list_pole_affine` | `eq:mastermu` (algebraic half) | none | self | AX3 |
| 12 | `μ_u(R) = μ_v(R) + (u-v)Λ(R)` | `mu_affine` | `eq:mastermu` (algebraic half) | `R` a domain element | self | AX3 |
| 13 | `μ_u(R) - μ_v(R) = (u-v)Λ(R)` | `mu_sub_eq` | as row 12 | `R` a domain element | self | AX3 |
| 14 | `(t+jj)^{-1} = t^{-1} - jj t^{-2} + jj² t^{-3} - jj³/(t³(t+jj))` | `laurent_pole_expansion` | §4.1 (`[t^{-3}]_∞`) | field, `[CharZero F]`, `t ≠ 0`, `t+jj ≠ 0` | self | AX3 |
| 15 | same with `jj = j²`, i.e. `t^{-3}` coefficient `j⁴` | `laurent_pole_coeff` | §4.1 | field, `[CharZero F]`, `t ≠ 0`, `t+j² ≠ 0` | self | AX3 |
| 16 | `D_N^6/D_K = D_N^5/(D_K/D_N)` | `weight_cancellation` | §1 (`D_N^6/D_K = W_K/T_K`) | field; `D_N ≠ 0`, `D_K ≠ 0` recorded (unused: total division) | self | AX3 |
| 17 | `D_K/D_N ≠ 0` | `weight_denom_ne_zero` | §1 | `D_N ≠ 0`, `D_K ≠ 0` | self | AX3 |
| 18 | `G(u) = G(v) + (u-v)M` entrywise | `gramMatrix_affine` | §4.1 (`eq:masterform`), Appendix C | entries given as a `Rep`-valued family | self | AX3 |
| 19 | `det(CᵀGC) = (det C)² det G` | `det_congruence` | §5.2 (`eq:congruence`) | commutative ring, `[Fintype n]`, `[DecidableEq n]` | self | AX3 |
| 20 | `det(A+δB) = det A · det(I + δ A⁻¹B)` | `det_add_smul_eq_det_mul` | §4.2 (`eq:pencil`, factorization step) | field, `IsUnit A.det` | self | AX3 |

## Status summary

Proved and exported: rows 1–20. Rows 3, 10 constitute Target 1 on `ℚ[t]` and on
a single pole; rows 11–13 are Target 2; rows 16–20 are Target 3.

Not proved, recorded as obligations (none of them is assumed anywhere):

| Id | Obligation |
| --- | --- |
| `OBL-assembly` | Assemble rows 3 and 10 over a finite pole list to obtain `μ_X(R) = τ_X(x^5 R(-x²))` for general domain elements. |
| `OBL-ratfunc` | Read row 7 inside `RatFunc ℚ` (substituting `x ↦ RatFunc.X`, `j ↦ C j`), making the rational-function reading formal. |
| `OBL-laurent` | Define the `t^{-3}` Laurent coefficient at infinity as a functional and identify `Λ` with it; rows 14–15 are the finite expansion that supports the reading. |
| `OBL-products` | Instantiate `D_m = ∏_{j=1}^m (t+j²)`, `W_K = D_N^5`, `T_K = D_K/D_N` as concrete polynomials and prove `D_K = D_N T_K`, simplicity of the poles, nonvanishing. |
| `OBL-weight` | Show `W_K p q/T_K` lies in `Rep`'s domain for `p,q ∈ E_K` (division by monic `D_K`, `N < K`). |
| `OBL-analytic` | The positive integral `μ_ξ(R) = ∫₀^∞ R(y²)w(y)dy`, positivity of `w`, Stieltjes/Andréief identities. |
| `OBL-bases` | `p`-adic unit and valuation statements for the three bases, i.e. `v_p(det C)` for the small/inner/outer frames. |
| `OBL-spectral` | `G ≻ 0` at `X = ξ`, symmetric square root, `∏(1+δβ_j)`, real roots, `dist(ξ, roots) = ‖B‖^{-1}`. |
| `OBL-padic` | Volkenborn completion, distribution relation and the forced constant `Y = p^5X + C_p`. |
| `OBL-kernel` | Cotangent/Eisenstein kernel `w(y) = (i/π)y^5E_5(iy)` and the energy certificates of §6. |
| `OBL-periodic` | Periodic Bernoulli primitives `F, P, C` of the tail estimates. |
| `OBL-invariant` | The primitive-normalization invariant `J_ξ` and the irrationality criterion. |

## Build evidence

`ZetaFive/Main/correspondences-build-log.txt`; `lake build ZetaFive` could not be
completed in this VM (toolchain v4.35.0 absent, full Mathlib build required) and
the log records the attempted command and its output. All six modules were
elaborated with `lean` against the pinned-API Mathlib 4.33.1 snapshot in
`/opt/mathlib`; exit status 0 for each.
