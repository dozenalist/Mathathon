# Expositions of the ζ(5) proof and attempts to go further

Search date: **14 November 2026**. The companion [proof overview](../PROOF_OVERVIEW.md) explains the argument backward using Lai’s lemma numbers.

**The central question for an extension is whether the arithmetic cost still fits inside the analytic decay.** The positive integral and determinant construction have analogues for higher zeta values. Producing integer polynomials that remain small is the difficult additional requirement.

The [exponent catalog](../EXPONENT_CATALOG.md) makes this comparison explicit for the original geometry at $k=5$ and its proposed $k=7$ adaptation. It links each contribution to the relevant theorem, separates the outer-range costs, and includes exact rational checks. The $k=7$ formulas are a research calculation with local estimates still to certify uniformly.

## Read these first

| Source | What it helps explain | Qualification |
| --- | --- | --- |
| Frank Calegari, [*zeta(5) is irrational*](https://galoisrepresentations.org/2026/09/24/zeta5-is-irrational/), 24 September 2026 | The most useful conceptual reconstruction found here. Connects the positive measure, rational modification, determinant and denominator savings to earlier work. | A mathematical blog exposition. Some historical connections are explicitly attributed to ChatGPT. Its illustrative parameters differ from Lai’s. |
| Bogdan Grechuk, [*Zeta(5) is irrational*](https://functor.network/user/3333/entry/1997), dated 29 September 2026 | A short introduction to the final integer contradiction and the three main tasks behind it. | Best for a first pass; it does not supply the difficult estimates. |
| Chun Wing Lai, [*On Fauzan’s Proof that ζ(5) is Irrational*, v1](https://ai.vixra.org/pdf/2609.0080v1.pdf), 29 September 2026 | The numbered reference used in our overview. Expands several calculations. | Its arithmetic correction has a sign inconsistency; its numerical potential check is not a proof of a uniform inequality. |
| Aabir Fauzan, [*ζ(5) is irrational*, v1](https://zenodo.org/records/22826419), 17 September 2026 | The original source, particularly the local arithmetic estimates and explicit comparison measure. | The Zenodo record describes an initial presentation. The record was accessible in this search, but its PDF was not successfully retrieved through the browser. |
| [mo271’s formalization and README](https://github.com/mo271/zeta5) | Explains which arithmetic estimates were changed and why a negative final margin survives. | Reports a complete Lean proof with a formalized prime number theorem. The build was not rerun for these notes. |
| [Dan Romik’s formalization and README](https://github.com/danromik/zeta5-irrationality) | Another detailed account of the proof’s components and dependencies. | Explicitly takes the prime number theorem as an external axiom. It therefore checks the implication from that theorem. The build was not rerun here. |

**Suggested reading order:** our backward overview → Grechuk for a short recap → Calegari for the design of the construction → the relevant detailed source when a specific estimate becomes the focus.

## What stops the direct move from ζ(5) to ζ(7)

### Positivity survives

Calegari writes down the moment functional for general integer k ≥ 2, with a positive weight wₖ. Consequently, the Gram-matrix argument still gives a positive determinant at ζ(k). The degree calculation also survives. A positive determinant by itself therefore does not explain why the method succeeds at 5 and struggles at 7. [Calegari, sections on Euler–Hermite formulas and Hankel determinants](https://galoisrepresentations.org/2026/09/24/zeta5-is-irrational/).

### The denominator burden changes

The simple-pole formula involves the finite sum

$$
H_j^{(k)}=\sum_{v=1}^{j}\frac{1}{v^k}.
$$

Increasing k raises the powers in these denominators. Other factors can cancel some of them, so the actual cost has to be calculated for the entire determinant.

**Structural inference:** for a fixed family of modifiers and fixed k, the positive weights all have the same main exponential tail, exp(−2πy). Changing a fixed polynomial factor in y affects lower-order terms after scaling; it does not automatically supply an equally large improvement in the leading quadratic decay rate. Thus the arithmetic can get worse without a matching analytic gain.

Carlos Toledo’s [*The Hankel-determinant method past ζ(5), measured*](https://carlostoledo.co/reports/zeta-hankel.html) directly investigates this imbalance. It reports exact coefficient normalization and interval evaluations for finite examples, together with a search across 323 families. The sampled ζ(7) families fail to achieve a negative normalized margin, and prime-factor calculations locate a substantial extra arithmetic cost.

**Scope:** this is computational evidence for the families and sizes tested. It is not a theorem that every possible Hankel construction for ζ(7) fails. Likewise, a negative value at a few sizes would not establish the eventual bound needed for irrationality.

### A specific claimed extension fails in its final arithmetic

Prince Anand’s September 2026 preprint claims an extension to ζ(7). An [October 3 issue on the associated Lean repository](https://github.com/gmDevi/zeta-7-21-lean/issues/1) identifies a discrepancy between the local valuation formulas and the table used to integrate them.

The reported recomputation gives an outer arithmetic contribution of approximately **+1.576**, whereas the paper uses approximately **−15.28**. With the corrected contribution, the final sum of arithmetic cost and analytic bound becomes positive. The desired decay no longer follows.

This is a particularly useful example to read alongside Step 2 of the overview: **the construction and local estimates can look plausible while the final cost comparison fails.** Toledo’s [independent audit](https://carlostoledo.co/reports/zeta7-anand.html) reports the same defect and tests several possible repairs. These are source-reported calculations, not computations rerun for these notes. They challenge that version of the argument; they do not establish that ζ(7) is rational.

## Later work that changes the question or construction

### More irrational odd zeta values without identifying the next one

Fischler, Lai, Sprang and Zudilin, [*Many more odd zeta values are irrational*, v1](https://arxiv.org/html/2611.16156v1), submitted **12 November 2026**, is a particularly relevant recent development.

It combines Hankel determinants with an elimination method to improve the asymptotic lower bound on how many odd zeta values are irrational. It does **not** single out ζ(7).

Read the introduction and Section 5. The functional differs substantially from Fauzan’s, and the associated measures can have both positive and negative weights. This removes the automatic positive-definiteness argument. A new nonvanishing argument guarantees a nonzero determinant for at least one size in a specified range.

This illustrates another failure point: changing the family to improve estimates can sacrifice positivity. The replacement construction must supply a new reason the determinant cannot vanish. The authors say they verified, simplified and rewrote the argument; this is a recent preprint.

### A smaller finite group on Hexagon

Shawn Krisman, [*One of ζ(7), ζ(9), …, ζ(21) is irrational*, v2](https://hexagonmath.org/2610.00516v2), uses a different construction based on derivatives of rational functions. The resulting linear forms omit ζ(3) and ζ(5). The page reports a Lean formalization and acknowledges an earlier result by CoolRmal.

Its relevance is the **change of target**: prove irrationality of at least one number in a finite group, rather than isolate ζ(7). It is not a successful substitution of 7 into Fauzan’s proof. The [paper’s introduction](https://hexagonmath.org/pdf/2610.00516v2) also distinguishes earlier results and repositories. Formalization claims here were read, not independently rebuilt.

### Related p-adic work on Hexagon

Antti Hippeläinen, [*On the irrationality of the 3-adic zeta value ζ₃(5)*, v2](https://hexagonmath.org/2610.00408v2), adapts a determinant construction and proves nonvanishing using an auxiliary prime.

The subscript matters: ζ₃(5) is a **p-adic value**, not the real number ζ(5). Its irrationality does not settle a higher real zeta value. It is useful for studying alternative nonvanishing mechanisms. The provenance statement says that no human expert has checked the proofs.

### A sharper bound for the same number

David Niedbala Giraudin, [*A new upper bound for the irrationality exponent of ζ(5)*](https://arxiv.org/abs/2611.01708), submitted **1 November 2026**, improves the exponent 260 to 171, conditional on Fauzan’s construction.

This concerns the extra approximation bound, not the basic irrationality criterion. It improves estimates for how the matrix changes near ζ(5), rather than proving irrationality of a new zeta value. It is useful when studying the perturbation branch omitted from the main overview.

## Earlier literature that explains the moving parts

| Read when the question is… | Source and useful location |
| --- | --- |
| Why do zeta tails have a positive moment representation? | Marc Prévost, [*Remainder Padé approximants for the Hurwitz zeta function*](https://arxiv.org/html/1709.05389v1), especially Theorem 1 and the integer cases. This predates the ζ(5) construction and treats approximations to ζ(2) and ζ(3). |
| Why can a determinant outperform one rational approximation? | Wadim Zudilin, [*A determinantal approach to irrationality*](https://arxiv.org/html/1507.05697v2), Sections 1–2. The later commentary discusses obstructions to extending the criterion. This is background, not an analysis of Fauzan’s specific family. |
| Where does the multiple integral come from? | Peter Forrester, [*Meet Andréief, Bordeaux 1886, and Andreev, Kharkov 1882–83*](https://arxiv.org/html/1806.10411v1), Section 2.2. Explains the determinant-to-integral identity. |
| Why do logarithmic distances and comparison measures appear? | E. B. Saff, [*Logarithmic Potential Theory with Applications to Approximation Theory*](https://arxiv.org/html/1010.3760v1), Sections 1 and 6. An introductory survey with examples; watch the sign convention for logarithmic energy. |
| Could a larger family of integrals help? | Francis Brown, [*Mellin transforms, transfinite diameter and rational approximations of integrals*](https://arxiv.org/abs/2604.20741), April 2026. Gives a multivariate framework and a worked ζ(2) application. It supplies a direction to investigate, not a demonstrated extension to ζ(7). |

A [MathOverflow question](https://mathoverflow.net/questions/515519/on-the-recent-irrationality-proof-for-zeta5) asks whether Fauzan’s construction can be located inside Brown’s larger families while retaining only powers of the desired zeta value. The page retrieved here supplies a question, not a completed construction.

## Problems in the linked exposition to keep separate from extension problems

These observations concern Lai’s **2609.0080v1**, not the correctness of every implementation of Fauzan’s method.

**The sign of the correction is internally inconsistent.** From m = ∏p⁻ᴸᵖ, decreasing a valuation lower bound increases the normalization cost. Lai’s negative discrepancy in Remark 8.6 therefore cannot be called favorable on that basis. The displayed final formula adds a positive correction, while the surrounding prose treats it as subtracted. This follows directly from the definition of m; it does not depend on a numerical experiment.

**The pointwise bound needs a proof between sampled points and beyond the grid.** A large grid and high decimal precision still leave those regions unchecked. Certified interval bounds and a tail argument can address them. The [mo271 README](https://github.com/mo271/zeta5) describes rigorous energy bounds and a modified arithmetic route using M = 400. Its reported proof does not validate Lai’s proposed correction.

**Large primes do not all disappear immediately above K.** Section 9.3 says that all factorial arguments are below K, but S includes factorials up to (2h−2)!, and 2h−2 can exceed K. For example, at K = 40, N = 3, h = 37, direct use of equation (75) gives v₄₁(S₄₀) = −32, not zero. Primes between K and 2h belong in the outer calculation.

The final two-decimal comparison is therefore the destination of substantial uniform estimates. Recomputing its printed constants cannot replace those estimates.

## What an extension must improve

Using the backward map, an attempted extension should answer four concrete questions:

1. **Integer coefficients:** what are the new denominator bounds, including common factors that can be removed?
2. **Nonvanishing:** does a positive moment representation survive? If it does not, what replaces it?
3. **Decay:** is the analytic upper bound uniform over the entire integration domain?
4. **Final comparison:** is the total quadratic exponent actually negative after all arithmetic costs and error terms are included?

The search covered the linked exposition, author explanations, arXiv, Zenodo records, Hexagon, formalization documentation, and public reports of extension failures. It found useful extensions of the method and a concrete obstruction in a claimed ζ(7) proof, but no independently verified proof of an individual higher real odd zeta value. Recent claims and finite searches are identified as such above.
