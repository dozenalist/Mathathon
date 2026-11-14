# Formalize the parallel constructions in the zeta 5 argument

Work for **90 minutes** on the correspondences in the zeta 5 argument. Use `https://github.com/dozenalist/Mathathon`, folder `ZetaFive`. The prepared source commit is `5f20e2fac14d7f38a56459a2e69d1dd406efaa5e`; inspect current repository state before editing and preserve other projects' work.

The user specifically requests lemmas for the **parallel constructions**, rather than a new proof of irrationality. Produce a small, compiling Lean library that shows how apparently separate functionals and determinant constructions represent common algebraic objects.

## Sources and scope

The reviewed [framework sources and manifest](../Literature/ParallelConstructions/README.md) are preserved in this repository. SAIR also received them directly in its ZetaFive VM project. The initial assignment was followed by a source-update message identifying the independently reviewed revision.

The accompanying `zeta5_unified_framework.tex` is **One summation functional, one Gram pencil**, dated 14 November 2026. Read Sections 1–4 and its correspondence table first. The PDF is a reading aid. `framework_checks.py` contains exact and numerical checks supporting the note; finite checks are not formal proofs.

Also read these repository files:

- `ZetaFive/PROOF_OVERVIEW.md`.
- `ZetaFive/ProofGuide/06_HANKEL_CONSTRUCTION.md`.
- `ZetaFive/ProofGuide/07_MOMENT_REPRESENTATION.md`.
- `ZetaFive/ProofGuide/08_READING_CAUTIONS.md`.
- `ZetaFive/ChatLogs/2026-11-14_research_chat_summary.md` for earlier context. The unified framework is newer than that summary.

The primary manuscript is Aabir Fauzan's 17 September 2026 version, https://zenodo.org/records/22826419. Source equation numbers in the unified note refer to this manuscript, not Lai's exposition.

Prioritize exact algebraic correspondences. The positive integral representation, analytic convergence, local valuation bounds, and energy estimates are separate dependencies. Do not treat a clear conceptual framework as verification of every quantitative certificate, or introduce the desired correspondences as axioms.

Use Lean and Mathlib **v4.35.0**, already pinned in Mathathon. Search the installed Mathlib API before inventing infrastructure. Check the Bernoulli convention explicitly: the note requires B₁ = −1/2.

## Freeze independent definitions

Keep the rational-function variable t, pullback variable x, and parameter X distinct.

Define the Bernoulli functional and its derivative transform on rational polynomials by

$$
L(P)=\sum_k [x^k]P\,B_k,\qquad \tau(P)=L(P''')/24.
$$

Define μ independently by linearity from

$$
\mu(t^e)=(-1)^e B_{2e+2}(2e+3)(2e+4)(2e+5)/24.
$$

For positive integer j, define

$$
\mu_X((t+j^2)^{-1})=j^4(X-H_j^{(5)})-\tfrac14+\tfrac1{2j}.
$$

Define τₓ on simple integer poles independently by

$$
\tau_X((x-r)^{-1})=H_{d(r)}^{(5)}-X,\qquad
d(r)=\begin{cases}r&r\ge0,\\-r-1&r<0.\end{cases}
$$

Here H₀⁽⁵⁾=0 and Hⱼ⁽⁵⁾ is the finite sum of inverse fifth powers from 1 to j. Use a precise domain: polynomial parts plus finitely supported simple-pole coefficients. A representation datatype is acceptable initially if its interpretation as a rational function is explicit. Distinguish theorems about representation data from theorems descended to rational-function equality. Do not define μ as the pullback of τ and then call the transport theorem independent verification.

## Target 1 Weighted transport

Prove for every P in Q[t]

$$
\mu(P)=\tau(x^5P(-x^2)).
$$

Start with the general monomial calculation. For positive integer j, prove the rational-function identity

$$
\frac{x^5}{j^2-x^2}
=-x^3-j^2x-\frac{j^4}{2}
\left(\frac1{x-j}+\frac1{x+j}\right).
$$

Use the finite harmonic increment to recover the independently defined μₓ pole value. Extend by finite linearity to the chosen simple-pole domain:

$$
\mu_X(R)=\tau_X(x^5R(-x^2)).
$$

Include exact examples τ(x³)=1/4, τ(x⁴)=−1/2, and μ(1)=5/12 as sanity checks supplementing the general proofs.

## Target 2 One parameter controls one residue functional

For R=P+Σⱼcⱼ/(t+j²), define Λ(R)=Σⱼcⱼj⁴. Prove the affine parameter identity with correctly typed polynomial parameters, and then after real evaluation:

$$
\mu_u(R)=\mu_v(R)+(u-v)\Lambda(R).
$$

Identify Λ(R) with the coefficient [t⁻³] at infinity if suitable Laurent-series infrastructure is readily available. Otherwise prove the explicit finite expansion supporting that interpretation and record the remaining semantic bridge separately.

This is the algebraic content of the note's positive-measure-plus-residue formula. Its analytic integral identity remains a separately named dependency; do not silently assume its proof.

## Target 3 One matrix in different coordinates

Define the bilinear form using the rational modifier W/T, where W=D_N⁵ and T=D_K/D_N. Prove the cancellation identity D_N⁶/D_K=W/T with the necessary nonzero polynomial hypotheses.

Use target 2 to prove an entrywise affine-pencil identity

$$
G(u)=G(v)+(u-v)M,
$$

where G(u) is the matrix of μᵤ(Wpᵢpⱼ/T) and M is the matrix of Λ(Wpᵢpⱼ/T). State and justify membership in the functional's domain rather than silently applying it to arbitrary rational functions.

Formalize the change-of-basis identity

$$
\det(C^{\mathsf T}GC)=\det(C)^2\det(G)
$$

with explicit ring/field and finite-index hypotheses. Explain how it accounts for different arithmetic bases; p-adic unit and valuation claims remain additional obligations.

If time permits, prove for invertible A

$$
\det(A+\delta B)=\det(A)\det(I+\delta A^{-1}B).
$$

The symmetric square-root normalization, eigenvalue product, real-root assertion, and quantitative root-exclusion radius are later targets unless fully justified in this block.

## Work division and review

Use one coordinator, a functional-algebra worker, a matrix worker, and an independent reviewer if delegation is available. Workers own separate modules. The coordinator owns shared definitions and build integration. If delegation is unavailable, execute those stages sequentially and report that fact.

Complete transport and affine-parameter lemmas before expanding the scope. Record precise later obligations for the Hurwitz/Stieltjes samples and asymptotic moments, cotangent/Eisenstein kernel, Volkenborn completion and distribution, Andréief integral, periodic Bernoulli primitives, primitive-normalization invariant, and energy certificates.

## Deliverables and acceptance

Create modules under `ZetaFive/Lean/Correspondences/`, explanatory notes in `ZetaFive/Lean/CORRESPONDENCES.md`, and a theorem/status ledger under `ZetaFive/Main/`. The inspected repository has no ZetaFive Lean target yet. Add a named `ZetaFive` Lake target and aggregator through a minimal coordinated root change, preserving all existing targets.

For each exported theorem record its mathematical statement, Lean declaration, source equation, hypotheses, reviewer, and `#print axioms` output. A completed theorem must compile without `sorry`, `admit`, added axioms or `native_decide`. Standard axioms may be `propext`, `Classical.choice`, and `Quot.sound`. Explicit hypotheses are acceptable when accurately reported, but must not assume the correspondence being claimed.

Run the actual module builds and `lake build ZetaFive`; save commands and exit statuses. Review signs, Bernoulli convention, zero denominators, positive-integer restrictions, variable names, and circular definitions. Ensure claimed rational-function equalities are not merely equalities of a convenient unvalidated encoding.

Append the outcome and remaining obligations to `ZetaFive/PROGRESS.md`. Commit only this project's changes and necessary build integration on an isolated `codex/zeta5-correspondences-...` branch. Push using the VM's existing authorized GitHub access if available, then verify the remote commit. Otherwise retain a patch and local commit and report the blocker; do not modify authentication settings or embed credentials in source files.

End the 90-minute block after collecting and reviewing worker outputs. Return the proved correspondence list, unresolved dependencies, build and axiom evidence, files, full commit hash, push status, and the single most useful next formalization task. These results should be described as correspondence lemmas, not as a complete irrationality proof.
