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

## Corrections to the first (provisional) checkpoint — 2026-11-14, supervisor review

The first checkpoint overstated three things and omitted the earliest source gaps.
The statements themselves are unchanged; these scope notes are binding.

**Overstated: representation encoding.** `XRep` (Transport.lean) and `Rep`
(AffineParameter.lean) are *polynomial-plus-association-list* data with an
explicitly defined evaluation (`XRep.tauX`, `Rep.mu`, `Rep.Lambda`). There is no
`RatFunc ℚ` evaluation of them, and no theorem that the evaluation is
independent of the chosen representation (e.g. that `[(j,c)]` and `[(j,c/2),(j,c/2)]`
agree, or that a repeated or out-of-order list gives the same value). Theorems
about these structures are theorems about the *encoding*; descending them to
rational functions is (new obligation) `OBL-encoding`:

* `OBL-encoding` — decide a normal form for `Rep`/`XRep` (e.g. `Finsupp ℕ ℚ` for
  coefficients, no duplicate indices), prove the evaluation well-defined on it,
  and prove it agrees with evaluation in `RatFunc ℚ` under the map
  `t ↦ RatFunc.X`, `(j,c) ↦ c/(X+j²)` away from the poles.

**Overstated: general transport.** `μ_X(R) = τ_X(x^5 R(-x²))` for general `R` is
**not** proved. Proved are the polynomial case (`μpoly_eq_τ_pull`) and a single
simple pole (`τX_single_pole_transport`); the list-induction assembly is
`OBL-assembly`, unchanged.

**Overstated: parameter type and Gram form.**
`mu_affine` and `gramMatrix_affine` are stated over `u v : ℚ`. The source writes
`X` as an indeterminate and works in `ℚ[X]` with a subsequent real evaluation.
The discrete data (pole values, `Λ`) are `ℚ`-linear in the parameter, so a
polynomial-valued statement would be `mu_affine_poly : ℚ[X]`-affine.

**STATUS: OPEN.** No `ℚ[X]`-valued version of this law compiles. An attempt was
made and removed; there is no declaration `mu_affine_polynomial` anywhere in the
tree, and this ledger previously claimed one existed — that claim was false and
is retracted here. The only proved parameter statements remain
`mu_affine`/`mu_sub_eq` over `u v : ℚ`, and `muP_affine`/`muP_eq_zero_add` over
`U V : ℚ[X]` in `Restrict.lean`, *if and only if* that module is present and
builds (check the aggregator before citing it).
Passing from `ℚ[X]` to `ℝ` by evaluation, and comparing with the frozen
`Rep.mu`/`XRep.tauX`, is `OBL-parameter`.

Second: `gramMatrix_affine` takes an *arbitrary* `ι → ι → Rep` array. It is not
the concrete bilinear Gram form of `eq:twoobjects`, `G_K(X)_{ij} = μ_X(W_K p_i p_j / T_K)`,
because that requires (i) `W_K p_i p_j / T_K` to lie in the domain
(`OBL-weight`) and (ii) `μ_X` evaluated on that particular rational function
(`OBL-encoding`). Until those, read `gramMatrix_affine` as an abstract affineness
statement about domain-valued arrays, **not** as the manuscript's Gram pencil.

**Convention fix (comment only).** `τ(x³) = 1/4` tests `B₀ = 1` only; it is
`τ(x⁴) = -1/2` that tests the sign convention `B₁ = -1/2`. The docstrings in
`Transport.lean` were corrected accordingly; both theorems and their proofs are
unchanged.

**Earliest gaps omitted by the first checkpoint.** The ledger began at the
monomial calculus, but the source's *first* claims (§2.1, `eq:EM`, `eq:symbol`,
`eq:difference`, `eq:reflection`, before `eq:poles`) were missing from it:

| Id | Source claim | Status |
| --- | --- | --- |
| `EARLY-1` | `eq:EM`: the terminating polynomial identity `τ(P) = (1/24)Σ_k B_k/k!·P^{(k+3)}(0)` and its equivalence with the frozen `L(P''')/24` | see early-block ledger below |
| `EARLY-2` | `eq:difference`: `τ(P(x+1) − P(x)) = P''''(0)/24` for `P ∈ ℚ[x]` | see below |
| `EARLY-3` | `eq:reflection`: `τ(P(−1−x)) = −τ(P(x))` | see below |
| `EARLY-4` | `eq:symbol`: `τ(e^{ux}) = u⁴/(24(e^u−1))` as a generating identity | see below |
| `EARLY-5` | Prop. 1 uniqueness/existence: the pole values are *derived* from `eq:difference` + `eq:reflection` + `eq:basepole`, not postulated | see below |
| `EARLY-6` | Simple-pole extension: `a_{r−1} − a_r = −r^{-5}`, `a_r = H_r^{(5)} − X` for `r ≥ 0` | see below |

## Early-block ledger (source-ordered) — swarm `smwh2nngu`, 2026-11-14

Authoritative source: `formalization_inputs/2026-11-14-parallel-01a1dc21/reviewed/`
(hash-verified against its own `source-manifest.json`:
tex `31748e32…`, pdf `a5d7a775…`, checks `6e2aeb24…`).

Build: **Lean/Mathlib v4.35.0, repository pin unchanged**, task-local elan at
`.scratch/elan` (former from `releases.lean-lang.org`), Mathlib artifacts from
the official cache (`lake exe cache get`, 9031 files). `lake build ZetaFive`
→ **exit 0, 9058 jobs**. Axiom audit `ZetaFive/Main/early-axioms.txt`: 22
declarations, 21 with `[propext, Classical.choice, Quot.sound]`, 1 with
`[propext, Quot.sound]`. No sorry/admit/native_decide/new axiom anywhere.

### Source-ordered checklist (earliest first)

| # | Source claim (§2.1 unless noted) | Declaration | Status |
| --- | --- | --- | --- |
| 1 | `eq:difference` polynomial case: `τ(P(x+1) − P(x)) = P⁗(0)/24` | `M1.τ_comp_X_add_one_sub` | **PROVED** |
| 2 | core law `L(Q(x+1) − Q(x)) = Q'(0)` | `M1.L_comp_X_add_one_sub` | **PROVED** |
| 3 | binomial–Bernoulli sum `Σ_{k≤n} C(n,k)B_k − B_n = [n=1]` | `M1.sum_range_choose_bernoulli_sub` | **PROVED** (from Mathlib `sum_bernoulli`) |
| 4 | `eq:reflection` `τ(P(−1−x)) = −τ(P)` | `M3.τ_reflect` | **PROVED** |
| 5 | `L(P(−1−x)) = L(P)` (invariance) | `M3.L_reflect`, `M3.L_neg_one_sub_X_pow` | **PROVED** |
| 6 | reflection on pole data `τ_X(g(−1−x)) = −τ_X(g(x))` | `M3.tauX_reflect`, `M3.d_neg_one_sub` | PROVED **on `XRep` representation** (inherits `OBL-encoding`) |
| 7 | Prop. 1 derivation: `a_{r−1} − a_r = −r⁻⁵` on ℤ | `M4.H5Z_diff` | **PROVED** |
| 8 | Prop. 1: `a` with `a₀ = c` + recursion + reflection ⟹ `a_r = c + H^{(5)}_{d(r)}` | `M4.eq_sub_H5Z`, `M4.pole_values_unique` | **PROVED** |
| 9 | consistency of those hypotheses (existence) | `M4.H5Z_satisfies_diff`, `M4.H5Z_satisfies_refl` | **PROVED** |
| 10 | harmonic increments `H_j − H_{j−1} = j⁻⁵` | `H5_increment` (committed earlier) | PROVED |
| 11 | harmonic bounds `1 ≤ H5 j < 2`, Cauchy tail | `M4.H5_ge_one`, `M4.H5_lt_two`, `M4.H5_cauchy` | PROVED |
| 12 | **`eq:EM` terminating series** `τ(P) = (1/24)Σ_k B_k/k!·P^{(k+3)}(0)` | — | **OPEN — EARLIEST GAP** |
| 13 | `eq:symbol` `τ(e^{ux}) = u⁴/(24(e^u−1))` | — | OPEN |
| 14 | `eq:poles` as a *derived* theorem for a functional on `RatFunc` | — | OPEN (blocked on `OBL-encoding`) |
| 15 | weighted transport `μ_X(R) = τ_X(x⁵R(−x²))`, general `R` | — | OPEN (polynomial case proved: `μpoly_eq_τ_pull`) |

**Earliest unproved step: #12, `eq:EM`.** Its prerequisites are *not*
substantial infrastructure: the derivative factors `B_k/k!` and the falling
factorial `P^{(k+3)}(0)` are elementary and every input (`L`, `τ`,
`derivative`, `Polynomial.sum`) already exists. The gap is that no one has yet
connected the frozen `τ = L(P‴)/24` to the operator form; this is the natural
first task of the next block. #14 is the one claim that genuinely needs new
infrastructure (`OBL-encoding`).

### Distinguishing reused Mathlib results from new correspondence lemmas

Reused, not reproved: `sum_bernoulli`, `bernoulli_zero`, `bernoulli_one`,
`bernoulli_eq_zero_of_odd`, `bernoulli_eq_sum_choose_bernoulli'`,
`coeff_X_add_one_pow`, `Polynomial.induction_on'`, `sum_eq_of_subset`,
`derivative_comp`, `derivative_C_mul_X_pow_succ`-analogue via `derivative_pow`,
`Finset.sum_range_succ`, `Matrix.det_mul`/`det_transpose`/`mul_nonsing_inv`,
`monotone_nat_of_le_succ`, `strictMono_nat_of_lt_succ`.

New here (manuscript-specific): the frozen functionals `L`, `τ`, `μ`, `pull`,
`H5`, `d`, `XRep`, `Rep`; the transport theorems; the pole recursion and its
uniqueness; the reflection and difference laws *for these functionals*; the
affine pencil and determinant corollaries.

### Swarm record

`smwh2nngu`, model `deepseek/deepseek-v4.1-flash`, reasoning effort `max`,
4 members × 60 steps, 35-minute budget, ended solved with 4/4 accepted.
m1 → `Candm1.lean` (`M1`: eq:difference), m2 → `Candm2.lean` (`M2`:
nondegeneracy), m3 → `Candm3.lean` (`M3`: reflection), m4 → `Candm4.lean`
(`M4`: H5 calculus, pole recursion, uniqueness). Coordinator compiled each
under the pinned 4.35.0 toolchain and read each proof before accepting.
Modules were namespaced `M1`–`M4` on integration because m1 and m3 independently
defined `L_X_add_one_pow` in a shared `Cand` namespace — a real collision caught
by the pinned build, not by the members' 4.33.1 prototypes.

**Reviewer limitation, stated plainly:** m4 was assigned as reviewer *and* as a
worker, so the independent-review role was not cleanly separated this block; the
coordinator performed the review of all four submissions. Also, m4's file
carries the `Cand` namespace as delivered; the coordinator rewrote only the
namespace lines, not the proofs.

### Post-block review notes (from the members' own reports, recorded here on purpose)

**Sign reading of the pole values.** `M4.eq_sub_H5Z` states `a r = c + H5Z r`
with `c = a 0`. m4 flagged the risk: substituting `c = −X` gives
`a_r = H_r^{(5)} − X`, i.e. `eq:poles` — the sign is correct **only because `c`
already carries the minus**. Written as `c + H5Z r` the theorem is right, but a
reader who supplies `c = X` will silently get `H_r^{(5)} + X`, the wrong sign.
When this is restated for the rational domain, state it as
`τ_X(1/(x−r)) = H_{d(r)}^{(5)} − X` directly rather than through `c`, or name the
constant `c = −X` in the statement.

**Known duplicate left in the tree.** `M3.d_neg_one_sub` and `M4.d_reflect`
(`Candm4.lean:230`) are identical statements, `d (−1 − r) = d r`. Both are
committed because each candidate file is preserved verbatim as its member
delivered it; `M4.H5Z_reflect` is the only consumer. A later integration should
keep `M3.d_neg_one_sub` (which m3 also uses inside `poleSum_reflect`) and delete
`M4.d_reflect`. This is cosmetic, not a soundness issue — flagged rather than
silently tidied, so the record shows the candidates are unedited.

## Supervisor corrections — 2026-11-15 (applied at the start of the block)

1. **Retracted a false claim.** This ledger previously said the `ℚ[X]` affine law
   was "proved as `mu_affine_polynomial` in `AffineParameter.lean`". No such
   declaration exists — the attempt was removed and the prose survived it. The
   `ℚ[X]`/`ℝ` parameter extension is **OPEN** (`OBL-parameter`). Lesson recorded
   here deliberately: prose in this file must be re-verified against the compiled
   tree before it is committed, not carried forward from intent.
2. **Bernoulli convention wording fixed in `Basic.lean`.** `τ(x³) = 1/4` tests
   `B₀ = 1`; it is `τ(x⁴) = −1/2` that tests `B₁ = −1/2`. Both module headers in
   `Candm1.lean`/`Candm3.lean` said "prototype only / 4.35.0 not installed"; both
   now record that they are validated under the pinned v4.35.0 build.
3. **`.scratch-elan-setup.sh` made reproducible.** It now: `cd`s to its own
   checkout; searches `ELAN_HOME`, `<checkout>/.scratch/elan`,
   `<project>/.scratch/elan` and `~/.elan` for a *validated* installation
   (contains the pinned toolchain) before bootstrapping from the official elan
   installer into a task-local dir; clears inherited `LEAN_PATH`; verifies
   `lean --version` is exactly 4.35.0 and that `lean` resolves inside
   `ELAN_HOME`; asserts `lean-toolchain` still pins v4.35.0; reuses an existing
   Mathlib cache instead of re-downloading. Tested with a deliberately polluted
   `LEAN_PATH=/opt/mathlib/...` → exit 0, pinned build.
4. **Axiom audit coverage corrected.** The first driver covered 22 declarations
   and this ledger implied completeness; it was 22 of 111 theorem/lemma exports.
   `ZetaFive/Main/full-axioms-driver.lean` is generated over every
   theorem/lemma in all eight modules and audits **111/111**:
   `full-axioms.txt` → 108 × `[propext, Classical.choice, Quot.sound]`,
   3 × `[propext, Quot.sound]`, **0 outside the allowed set**.
   Note `M2.L_ne_zero`/`tau_ne_zero`/`mu_poly_ne_zero` prove the functionals are
   nonzero; that is **not** nondegeneracy of a bilinear form, which is unproved.
