# Correspondence lemmas for the ζ(5) argument

These modules formalize the **exact algebraic correspondences** of the note
*One summation functional, one Gram pencil* (14 November 2026,
`formalization_inputs/2026-11-14-parallel-01a1dc21/zeta5_unified_framework.tex`;
its SHA-256 hash was checked against `source-manifest.json`).

They are **correspondence lemmas, not a proof that ζ(5) is irrational**, and not
a verification of any analytic, local or quantitative certificate of Fauzan's
manuscript (Zenodo record 22826419, 17 September 2026). Equation numbers refer
to that manuscript as quoted by the note.

## Modules

| Module | Contents |
| --- | --- |
| `Correspondences/Basic.lean` | `H5`, `L`, `τ`, `μcoeff`, `μpoly`, `pull`. Shared definitions only. |
| `Correspondences/Transport.lean` | Target 1: monomial calculus, `μpoly_eq_τ_pull`, sanity values, the partial fraction, `τ_X` on its domain and the pole-value comparison. |
| `Correspondences/AffineParameter.lean` | Target 2: the domain `Rep`, `Λ`, `μ_·`, the affine parameter identity, Laurent expansions. |
| `Correspondences/Matrix.lean` | Target 3: weight cancellation, the affine Gram pencil, `det(CᵀGC)`, `det(A+δB)`. |
| `ZetaFive.lean` | Library root / aggregator. |

## Conventions checked rather than assumed

* **Bernoulli numbers.** Mathlib's `bernoulli` is defined by
  `x/(e^x - 1) = Σ B_n x^n/n!`, so `B_1 = -1/2` — the convention the note
  requires. `τ_X_pow_four` is the explicit check: `τ(x⁴) = 4·3·2·B_1/24 = -1/2`
  is false with `B_1 = +1/2`. `τ_X_pow_three` (`= 1/4`) and `μpoly_one`
  (`= 5/12`) are the other two requested sanity values.
* **Variable separation.** `PolyT = ℚ[t]`, `PolyX = ℚ[x]`, parameter `u : ℚ`.
  The two polynomial names denote the same ring; they are a documentation
  device, and every statement names its variable. `pull` is `t ↦ -x²`.
* **No circular definitions.** `μ` comes from its own monomial values
  (`μcoeff`); `τ_X` at simple poles comes from `H_{d(r)}^{(5)} - X`; the pole
  value of `μ_X` comes from its own displayed formula. `pull` occurs only in the
  *statement* of the transport theorem, never in a definition of `μ`, so the
  transport theorem is not the unfolding of a definition.

## Target 1 — weighted transport

* `μpoly_eq_τ_pull : μpoly P = τ (x^5 * pull P)` for all `P : ℚ[t]`
  (note: `eq:pullback`, `eq:EM`, §2.1 monomial formula). Proved by
  `Polynomial.induction_on'`; the monomial step is `τ_C_mul_X_pow`,
  `τ(C c * x^(k+3)) = c(k+1)(k+2)(k+3)B_k/24`.
* `rat_pole_identity : x^5/(j²-x²) = -x³ - j²x - (j⁴/2)(1/(x-j) + 1/(x+j))`
  over any field of characteristic zero with `x±j ≠ 0` and `j²-x² ≠ 0`. Being
  field-generic, this is the rational-function identity itself rather than an
  identity about one ad-hoc encoding. The substitution into `RatFunc ℚ` is not
  formalized (`OBL-ratfunc`).
* `τX_single_pole_transport`: `τ_X` on the transported simple pole `c/(t+j²)`,
  i.e. `τ(-c(x³+j²x)) + (-c j⁴/2)(H_j - X) + (-c j⁴/2)(H_{j-1} - X)`, equals
  the independently defined `μ_X` pole value `c·(j⁴(X - H_j^{(5)}) - 1/4 + 1/(2j))`.
  The `-1/4` is `τ(-x³)`; the harmonic increment `H5_increment`
  (`H_j - H_{j-1} = j^{-5}`) turns the two half-pole terms into `1/(2j)`.
* `d_natCast`, `d_neg_natCast` fix the index map `d(r) = r` (`r ≥ 0`),
  `d(r) = -r-1` (`r < 0`), so `d(-j) = j-1`.

**Not assembled.** `μ_X(R) = τ_X(x^5 R(-x²))` for *general* `R` follows from the
polynomial case, the single-pole case and additivity over a finite pole list.
Both ingredients are proved; the list-induction assembly (`OBL-assembly`) is
not yet formalized, so the general statement is **not** exported and is not
asserted anywhere in the library.

## Target 2 — one parameter controls one residue functional

* `Rep` is the domain: polynomial part in `t` plus a finite association list of
  simple poles at `t = -j²`, with `1 ≤ j` stored in the structure (`Rep.hpos`),
  so a pole at `t = 0` is not representable.
* `Rep.mu u R` evaluates `μ_u` from its pole formula; `Rep.Lambda R = Σ_j c_j j⁴`.
* `mu_affine : R.mu u = R.mu v + (u - v) * R.Lambda` for all `u v : ℚ`, and
  `mu_sub_eq` in difference form. Proof: the list induction `list_pole_affine`.
  The parameter enters only through `j⁴u`, so the slope is exactly the residue
  functional.
* `laurent_pole_expansion`, `laurent_pole_coeff`:
  `1/(t+j²) = 1/t - j²/t² + j⁴/t³ - j⁶/(t³(t+j²))` — every term of order `≥ -3`
  displayed, remainder of order `t^{-4}`.

**Semantic bridge (`OBL-laurent`).** The library does not build a
Laurent-coefficient-at-infinity functional: no API in this snapshot provides it
and we declined to invent infrastructure for it. What is proved is the explicit
finite expansion; it exhibits the `t^{-3}` coefficient `j⁴` and shows the
remainder is `O(t^{-4})`, and the polynomial part has no negative powers. `Λ` is
defined as that coefficient and `mu_affine` shows it is the slope. So the
identification is a proved computation plus a definitional reading — but the
reading is prose, not Lean.

**Analytic half (`OBL-analytic`).** `μ_ξ(R) = ∫₀^∞ R(y²)w(y)dy`, positivity of
`w`, and the Stieltjes/Andreief statements are neither proved nor assumed here.
Nothing in the library depends on them.

## Target 3 — one matrix in different coordinates

* `weight_cancellation : D_N^6/D_K = D_N^5/(D_K/D_N)` in any field. The
  hypotheses `D_N ≠ 0`, `D_K ≠ 0` are those under which `T_K = D_K/D_N` is a
  nonzero rational function; they are recorded, not used, because Lean's
  division is total — the honest content is `weight_denom_ne_zero`. The concrete
  polynomials `D_m`, `T_K`, `W_K` are not instantiated (`OBL-products`).
* `gramMatrix_affine : gramMatrix A u = gramMatrix A v + (u-v) • residueMatrix A`,
  entrywise, for a **domain-valued family** `A : ι → ι → Rep`. Membership in the
  domain is a hypothesis of the construction, so the pencil is never applied to
  an arbitrary rational function.
* `det_congruence : det(Cᵀ G C) = (det C)² det G` over a commutative ring, finite
  index type. The p-adic unit/valuation statements for the three bases of the
  manuscript (`OBL-bases`) are untouched.
* `det_add_smul_eq_det_mul : det(A + δB) = det A · det(I + δ A⁻¹B)` for
  invertible `A`. Square-root normalization, `∏(1+δβ_j)`, real-rootedness and
  the root-exclusion radius are **not** formalized (`OBL-spectral`).

**Membership obligation for the actual weight (`OBL-weight`).** That
`W_K p q / T_K` is the value of some `Rep` is not proved: it needs division of
`W_K p q D_N` by the monic `D_K`, simplicity of the poles at `-j²`
(`∏_{i≠j}(i²-j²) ≠ 0`), and `N < K`. The pencil theorem is stated so that this
stays a visible input.

## Build and axiom evidence

`ZetaFive/Main/CORRESPONDENCES_STATUS.md` is the ledger;
`ZetaFive/Main/correspondences-build-log.txt` records commands and exit
statuses; `ZetaFive/Main/correspondences-axioms.txt` has `#print axioms` for all
20 exported theorems (only `propext`, `Classical.choice`, `Quot.sound`). No
`sorry`, `admit`, `native_decide` or new axiom occurs in the modules.

**Toolchain caveat.** The checkout pins `leanprover/lean4:v4.35.0` with Mathlib
`v4.35.0`. This VM has Lean 4.33.1 and a built Mathlib snapshot at `/opt/mathlib`
(4.33.1). A fresh clone's `lake build ZetaFive` starts by cloning Mathlib and
would need a full Mathlib build (hours), so it was not completed here; every
module was elaborated with `lean` against that snapshot with the repository root
on `LEAN_PATH`. Re-running `lake build ZetaFive` where the pinned toolchain and
a built Mathlib v4.35.0 exist is the outstanding build step. An API name could
differ between 4.33.1 and 4.35.0; the proofs themselves are version-independent.

## Early block (`smwh2nngu`) — §2.1 foundations

Source: the **reviewed** note (`formalization_inputs/2026-11-14-parallel-01a1dc21/reviewed/`).

| Module | New content | Namespace |
| --- | --- | --- |
| `Candm1.lean` | `eq:difference`: `L(Q(x+1)−Q(x)) = Q'(0)`; `τ_comp_X_add_one_sub`; binomial–Bernoulli sum | `M1` |
| `Candm2.lean` | nondegeneracy: `L`, `τ`, `μ` nonzero; `B_{2n} ≠ 0` as an explicit hypothesis, not assumed | `M2` |
| `Candm3.lean` | `eq:reflection`: `τ(P(−1−x)) = −τ(P)`; `L`-invariance; pole-level reflection | `M3` |
| `Candm4.lean` | H5 calculus (`1 ≤ H5 j < 2`, Cauchy tail); `H5Z_diff` (`−r⁻⁵`); `eq_sub_H5Z`, `pole_values_unique` | `M4` |

**Earliest unproved step: `eq:EM`**, the terminating series
`τ(P) = (1/24)Σ_k (B_k/k!)·P^{(k+3)}(0)`. It is elementary and every input
exists; it is merely not yet connected to `eq:symbol` and the operator form.
