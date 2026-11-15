ZETA(5) IRRATIONALITY ARGUMENT OVERVIEW
Draft prepared 14 November 2026.

Read zeta5_irrationality_overview.pdf.
Editable source: zeta5_irrationality_overview.tex.

This is a human-readable overview of the whole determinant argument.
The arithmetic and analytic estimates are stated before being used.
The exposition uses only the degree upper bound and rounded constants:
arithmetic cost 1.35 K^2, analytic decay -1.36 K^2, hence -16 n^2.

The short source note is substantive: Lai's printed arithmetic correction
has an inconsistent sign. The assumed arithmetic input is explicitly
Fauzan's original equation (5.21), not a claim that Lai's literal corrected
statement yields the same numerical bound.

CORRECTNESS REVIEW
The algebra and final implication were independently checked, including
the moment and pole identities, convergence, Gram positivity, degree,
factorial normalization, and exact rational rounding margins.
The review did not re-prove the borrowed arithmetic or energy estimates.
The opening now makes explicit that the arithmetic estimate is an additional
assumption beyond Lai's sections 8-11 as literally printed.

SOURCES
Chun Wing Lai, On Fauzan's Proof that zeta(5) is Irrational,
v1, 29 September 2026:
https://ai.vixra.org/pdf/2609.0080v1.pdf

Aabir Fauzan, zeta(5) is irrational, 17 September 2026:
https://zenodo.org/records/22826419

The earlier parallel-constructions companion remains in its own folder.

BUILD
  tectonic --untrusted zeta5_irrationality_overview.tex
Or compile twice with pdflatex using the standard AMS, geometry, xcolor,
and hyperref packages. No external images or bibliography files are needed.
