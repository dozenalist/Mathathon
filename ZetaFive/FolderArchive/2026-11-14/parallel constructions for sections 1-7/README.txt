PARALLEL CONSTRUCTIONS FOR SECTIONS 1-7
Explanatory draft, 14 November 2026

Read lai_parallel_constructions.pdf (6 pages).
The editable source is lai_parallel_constructions.tex.

SOURCE AND SCOPE
Chun Wing Lai, On Fauzan's Proof that zeta(5) is Irrational,
version 1, 29 September 2026:
https://ai.vixra.org/pdf/2609.0080v1.pdf

Source references are to Lai's sections 1-7, not the different numbering
in Fauzan's manuscript or the earlier unified-framework companion.
The draft explains the functional, weighted pullback, rational modifier,
Hankel/Gram/affine matrix, continuous/discrete pairings, and normalization.
It excludes the later prime estimates, energy argument, and perturbations.
Stieltjes-transform, coefficient-functional, and coordinate language are
explanatory reorganizations derived from the definitions.

VALIDATION
Independently reviewed for mathematical correctness and scope.
Compiled with Tectonic; all six rendered pages visually inspected.
This is an explanatory draft, not verification of the later estimates.

BUILD
Use a standard LaTeX distribution with the AMS, geometry, booktabs, array,
xcolor, and hyperref packages:
  pdflatex lai_parallel_constructions.tex
  pdflatex lai_parallel_constructions.tex

Or use Tectonic:
  tectonic --untrusted lai_parallel_constructions.tex
