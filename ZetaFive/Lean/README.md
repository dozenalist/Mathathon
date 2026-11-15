# Uniform zeta Hankel formalization

This directory develops the square-node Hankel argument for integer zeta weights
`2 ≤ k ≤ 5`. The definitions and algebraic results are parameterized by `k`;
there are no four copied versions of the determinant proof.

**Checked partial formalization, not a complete proof of the paper.** The
general pole-moment identity and the global arithmetic and analytic estimates
remain unproved here. `Main.lean` states them explicitly in
`FamilyEstimates k parameters`; `PaperEstimates k` is the Lai specialization.
No value of that structure has been constructed, including for `k = 5`.
Consequently, `irrational_two_through_five_of_estimates` is a conditional
theorem, not an unconditional proof of irrationality. There are no proof holes
or extra axioms standing in for these estimates.

## Organization

- `Common/`: arguments independent of the zeta index: square-node algebra,
  partial fractions, affine determinants, Gram positivity, denominator clearing,
  Gamma integrals, exponential estimates, and the final irrationality criterion.
  `Common/Arithmetic/` contains the valuation and integral-polynomial toolkit.
- `Family/`: one family with a variable natural index `k`, its rational moments,
  positive density, Hankel matrix, normalization, and degree. `Parameters.lean`
  supports both Lai's `K=40n, N=3n, h=37n` and Calegari's
  `K=12n, N=n, h=11n`, with numerator exponent six.
- `LICENSES/`: licenses for adapted upstream proofs.

The target `ZetaFive.zeta k` is the real Dirichlet series. The theorem
`ZetaFive.riemannZeta_eq` identifies it with Mathlib's complex `riemannZeta`
for `2 ≤ k`. This connection is part of the formal statement, rather than an
informal identification of an abstract constant.

## What is proved

| Argument | File(s) | Status |
| --- | --- | --- |
| Denominator polynomials, simple roots at negative squares, residues and partial fractions | `Common/SquareNodes.lean`, `Common/PartialFractions.lean` | Proved |
| Affine determinant coefficients and weighted Vandermonde nonvanishing | `Common/AffineDeterminant.lean` | Proved independently of `k` |
| Positive Gram determinants and the integer-polynomial irrationality criterion | `Common/Gram.lean`, `Common/Criterion.lean` | Proved independently of `k` |
| Andréief's multiple-integral identity | `Common/Andreief.lean` | Proved independently of `k` |
| Rational moments, harmonic sums, affine pole values and Hankel polynomials | `Family/Moments.lean`, `Family/Construction.lean` | Defined uniformly; algebraic identities proved |
| Exact degree of the normalized polynomial | `Family/Degree.lean` | Proved: `37n` for Lai's parameters, `11n` for Calegari's |
| Positive density and exponential upper bound | `Family/Weight.lean`, `Family/WeightBound.lean` | Proved; the upper bound is uniform for `2 ≤ k ≤ 5` |
| Differentiation of the exponential series and adjacent-weight recurrence | `Family/WeightDerivative.lean` | Proved for `k ≥ 1` and `y > 0` |
| Polynomial moment integrals | `Family/PolynomialMoments.lean` | Proved for every `k ≥ 2`, using Gamma integration and Euler's even-zeta formula |
| Bernoulli cancellation and polynomial-moment valuations | `Common/Arithmetic/Bernoulli.lean`, `Family/MomentValuation.lean` | Proved uniformly in `k` |
| Harmonic-sum and pole-value denominator bounds | `Common/Arithmetic/NaturalValuation.lean`, `Family/PoleValuation.lean` | Proved uniformly in `k` |
| Rational-function moment representation and determinant positivity | `Family/Positivity.lean` | Proved **assuming** `PoleMoments k` |
| The actual Hankel determinant as a multiple integral | `Family/DetIntegral.lean` | Proved **assuming** `PoleMoments k` |
| Logarithmic weight and multiple-integrand upper bounds | `Family/AnalyticEstimates.lean` | Proved uniformly for `1 ≤ k ≤ 5`; the global energy bound remains open here |
| Final irrationality deduction | `Common/Normalization.lean`, `Main.lean` | Proved **assuming** the listed estimates |

For example, the formal polynomial-moment formula is

\[
\mu_k(t^e)=(-1)^e B_{2e+2}
  \frac{(2e+k)!}{(k-1)!(2e+2)!}.
\]

`Specializations.lean` simplifies it at each of `k = 2, 3, 4, 5`.
For primes `p > k-1`, the arithmetic result gives valuation at least `-1`,
improving to `0` when `2e+2 < (k-1)(p-1)`.

## Remaining proof obligations

1. Prove `PoleMoments k` for the actual density in `Weight.lean`. Integrability
   is established, but the value of the simple-pole integral is still an input.
2. Construct the normalizing factor and integer polynomials, with a sufficiently
   sharp global bound for the normalizer. Local moment valuations alone do not
   establish the residue-class, inner-range, outer-range, or prime-sum bounds.
3. Prove the global determinant upper bound through the potential/energy
   argument, and prove that its exponent plus the arithmetic exponent is
   negative. The elementary weight bound alone does not establish this.

`irrational_of_family_estimates` supports any parameter sequence with linearly
bounded matrix size. Both Lai and Calegari specializations are provided, without
assuming that their global estimates have already been proved.
The exponent in `FamilyEstimates` multiplies `n²`, whereas the paper often uses
`K²`. For Lai's `K = 40n`, constants must therefore be rescaled by `1600`.
The code does not attempt the paper's additional irrationality-measure claim.

### Why the fifth-weight normalizer cannot just be copied

The exact rational check
[`check_general_k_denominators.py`](../Computation/check_general_k_denominators.py)
uses the same definitions and scalar normalization as these Lean files. At
`k = 2, n = 1`, it computes

\[
v_{83}(F_2(0))=-11,\qquad K=40,\ N=3,\ h=37.
\]

The fifth-weight normalizer is supported at primes at most `2h = 74`. Such a
factor cannot clear this constant coefficient's denominator at `83`.
This rules out copying that all-index integrality statement unchanged.
It does **not** refute an eventual asymptotic statement, a different normalizer,
or the method itself. The script uses exact rational arithmetic via
`python-flint`; this finite check has been run but is not a Lean theorem.

## Build

From the Mathathon repository root, using its pinned Lean and Mathlib versions:

```text
lake exe cache get Mathlib
lake build ZetaFive
lake env lean ZetaFive/Lean/Audit.lean
```

Lean is pinned to `4.35.0`; Mathlib is pinned by the repository manifest to
`56a005855ea17e0b0958f73ec801ae140b0a1679` (`v4.35.0`).
Both `lake build ZetaFive` and the repository's default `lake build` pass.
The audit checks all 289 exported `ZetaFive` declarations and rejects any axiom
outside `propext`, `Classical.choice`, and `Quot.sound`; it passes. Standard
axiom dependencies do **not** remove explicit hypotheses from conditional
theorems.

`ZetaFive` is a default build target. On machines with limited memory, run
`./ZetaFive/Lean/Check.ps1` in PowerShell: it builds the modules in dependency
order before running the audit. The Mathlib cache is recommended before a first
build.

## Sources and scope

1. Chun Wing Lai, *On Fauzan's Proof that ζ(5) is Irrational*, v1,
   https://ai.vixra.org/pdf/2609.0080v1.pdf.
2. Frank Calegari, *zeta(5) is irrational*, September 24, 2026,
   https://galoisrepresentations.org/2026/09/24/zeta5-is-irrational/.
3. The Apache-2.0 Lean development https://github.com/mo271/Zeta5,
   pinned source commit `7fe736760f4b96bfdb4334b68e3b3124ecbe10b0`.
   Adapted files identify their provenance in their headers. Its license is
   preserved at `LICENSES/mo271-Zeta5.txt`.

The source repository's entire proof is not imported. The adapted central
lemmas are checked directly against Mathathon's Mathlib version. The existing
`ZetaFive/ProofGuide/08_READING_CAUTIONS.md` explains why the printed estimates
in Lai's v1 cannot simply be accepted as formal hypotheses and advertised as a
complete proof. A conditional theorem explicitly lists the estimates it needs.

The closest upstream boundaries for finishing the work are
`Apery.Norm.integral_mN` and `Apery.Growth.growth_mN` on the arithmetic side,
and `Apery.EnergyBound.log_Δ_le'` and `Apery.RealBound.real_bound'` on the analytic
side. Their full dependencies are not present here and have not been rebuilt
as part of this development. Several are specialized to the fifth zeta value;
renaming the index is not a proof of the corresponding general statement.
