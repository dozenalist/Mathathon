# Recent AI-assisted literature and Hexagon search

Reviewed 2026-11-13, America/Los_Angeles. Source discovery and inspection are
recorded here. Mathematical claims from newly posted manuscripts require
independent review before use as established inputs.

## Search record

Hexagon is the mathematical repository at [hexagonmath.org](https://hexagonmath.org/).
Its [public API](https://hexagonmath.org/api/v1) supports metadata searches.
The following requests were read successfully through HTTPS on the review date.
Every response had `has_more=false` and `next_cursor=null`.

| Query | Hits | Relevant identifiers or exclusions |
| --- | ---: | --- |
| [Kepler](https://hexagonmath.org/api/v1/works?q=Kepler&limit=100) | 2 | `2611.00136v2`, `2610.00483v1`, concerning celestial mechanics and polynomial roots |
| [sphere packing](https://hexagonmath.org/api/v1/works?q=sphere%20packing&limit=100) | 2 | `2610.00330v1`, `2610.00289v1` |
| [circle packing](https://hexagonmath.org/api/v1/works?q=circle%20packing&limit=100) | 1 | `2610.00330v1` |
| [Cohn](https://hexagonmath.org/api/v1/works?q=Cohn&limit=100) | 5 | `2611.00340v1`, `2611.00154v1`, `2610.00330v1`, `2610.00248v1`, `2610.00021v1` |
| [Viazovska](https://hexagonmath.org/api/v1/works?q=Viazovska&limit=100) | 1 | `2610.00330v1` |
| [packing](https://hexagonmath.org/api/v1/works?q=packing&limit=100) | 12 | Includes `2611.00390v1`, `2610.00479v1`, `2610.00330v1`, `2610.00289v1`, `2610.00021v1` |

These searches cover metadata, so body-text references can be missed. Web
queries also included `"Hexagon" "sphere packing" AI`,
`site:hexagonmath.org "three" "sphere"`,
`site:github.com/openai/math "sphere" "packing"`, and
`Kepler conjecture simpler proof 2025 2026 sphere packing`.
The review identified promising leads for bounded investigation. It established
no simpler complete three-dimensional proof.

## HEX26 — coefficient constructions in dimensions 8 and 24

**A construction of the sphere-packing magic functions in dimensions 8 and 24**,
contributed by Thomas Hales, `hexagon:2610.00330v1`, October 18, 2026, 51 pages,
CC BY 4.0. The record declares primarily AI-generated text and partial human
understanding. Its provenance statement attributes generation to ChatGPT-6
Astra with prompting from Hales. [Versioned record](https://hexagonmath.org/2610.00330v1)

The abstract and TeX source were inspected, especially the introduction,
the coefficient-construction statements, and Section 12, *The remaining sign
problem*. The paper constructs normalized functions through an infinite linear
system, then uses a boundary problem, a rank-six holomorphic vector bundle,
Riemann–Roch, and uniqueness. Global sign inequalities are supplied by comparison
with the existing magic functions. The source explicitly leaves independent sign
proofs open. [TeX source](https://hexagonmath.org/api/v1/works/2610.00330v1/source?path=magic-8-24.tex)

Precise TeX locators are `thm:main`, `thm:inverse`, `thm:eight`,
`sec:comparison`, `sec:eight`, `sec:signs`, and `app:motivation`.
The [source manifest](https://hexagonmath.org/api/v1/works/2610.00330v1/source)
reports entry point `magic-8-24.tex`, 184869 bytes, SHA-256
`032ff73ed7fe39128ecdb1a91be6e46e4cbfb1c17b046440cd027b6bacfdb8f9`.
That is the publisher's manifest hash. A local archive/hash check has not been
performed in this review.

**Assessment for this project.** A bounded experiment could test whether the
Gaussian inversion and coefficient basis in Appendix A yields useful functions
in dimension 3. The first deliverable must include actual 3D numerical evidence
and the missing sign/tail obligations. The full construction imports substantial
complex analysis and modular geometry, so its simplicity advantage remains
unestablished. Main should compare dependency counts and certificate size with
the chosen classical baseline before expanding this route. The November 12
Pittsburgh seminar announcement independently confirms the topic and intended
construction. [Seminar announcement](https://www.mathematics.pitt.edu/content/sphere-packings-8-and-24-dimensions-new-construction)

## OAI26 — a planar Fourier certificate

**A sharp Fourier certificate for planar circle packing**, OpenAI, September 23,
2026. Inspected the manuscript README, verification README, and source inventory
at repository commit `4eaee87548250b2682affda7d05d947c05554bae`.
The parent repository describes manuscripts with varying verification coverage.
[Versioned paper directory](https://github.com/openai/math/tree/4eaee87548250b2682affda7d05d947c05554bae/preprints/A-sharp-Fourier-certificate-for-planar-circle-packing-September-23-2026)

The public verifier uses Python 3 and `python-flint==0.9.0`. Its README specifies
finite matrix, residual, Bernstein, and scalar checks. Analytic quadrature,
continuum, and infinite-tail arguments remain in the article. This literature
review did not run the verifier or audit those arguments. Useful source paths
include `build/sections/signs.tex`, `build/sections/certificates.tex`,
`build/sections/independent-certification.tex`, and
`verification/verify_all.py`.
[Verification coverage](https://github.com/openai/math/blob/4eaee87548250b2682affda7d05d947c05554bae/preprints/A-sharp-Fourier-certificate-for-planar-circle-packing-September-23-2026/verification/README.md)

**Assessment for this project.** Bernstein positivity, exact finite matrices,
and explicit tail control could inform our local certificate pipeline. Any
transfer needs a fresh 3D theorem, normalization audit, and numerical comparison.
The dimension-2 claim and its finite checker do not discharge those tasks.
Assign a short independent review only when an explicit reusable component has
been identified.

## Other screened leads

| Record | Scope and inspection level | Kepler use |
| --- | --- | --- |
| [The 24-cell conjecture in the all-contact case and near D4, `2611.00390v1`](https://hexagonmath.org/2611.00390v1) | November 12, 2026, Tejasvi Singh Tomar, 24 pages, mixed text, declared full human understanding. Abstract claims two restricted 4D classes, with computer assistance and partial Lean formalization. Record and references read, proof and certificates unchecked | Possible local rigidity/volume-expansion ideas. The applicability hypotheses and computational load need independent audit |
| [A Fourier Consequence for Lattice Kissing Numbers and Average Contacts, `2610.00021v1`](https://hexagonmath.org/2610.00021v1) | Scott Kominers, October 2, 2026, 9 pages, mixed text, declared full human understanding. API abstract read. Asymptotic contact bounds built on another AI preprint | Secondary high-dimensional lead. A finite-dimensional density consequence must be derived and checked separately |
| [Linchpin Theorems, `2610.00289v1`](https://hexagonmath.org/2610.00289v1) | Thomas Hales, October 16, 2026, 26 pages. API abstract read. Auditable theorem statements linking formal infrastructure to intended mathematics | Useful for checking the meaning of Lean statements |
| [Densest packings of two translates of a lattice in five dimensions, `2610.00479v1`](https://hexagonmath.org/2610.00479v1) | Metadata only | Restricted periodic families in another dimension. Deferred |
| [Improved Kissing Numbers in Nineteen and Twenty-One Dimensions, `2610.00248v1`](https://hexagonmath.org/2610.00248v1) | API abstract read. Explicit higher-dimensional constructions | Lower bounds for kissing configurations. Deferred |

The primary-source search also located Cohn–de Laat–Salmon's three-point bounds
and its public data, which belong in the core hybrid route. The separate core
source notes supply their mathematical scope.
[Paper](https://arxiv.org/abs/2206.15373) ·
[Numerical data](https://dspace.mit.edu/entities/product/d32e22af-d2e4-4084-abd9-998c9604e0b1)

## Promotion and refresh procedure

1. Preserve the exact version, contributor/provenance, source URL, license,
   theorem locator, and every dependency actually used.
2. Extract the proposed 3D statement and assign its proof and computation to an
   independent reviewer. Record the difference between declared verification
   and checks performed by this team.
3. Compare proof length, prerequisites, cases, numerical variables, and certificate
   size with the nearest existing route. Require a concrete simplicity benefit.
4. For a Cohn–Elkies-like proposal, reproduce a 3D bound and its precision/error
   budget locally before promoting it. Record sampling, certified intervals,
   and remaining analytic obligations separately.
5. Repeat the metadata queries and targeted body-text searches at a major
   strategy change and before the final novelty claim. Preserve the earlier
   dated search record.
