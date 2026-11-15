THE DETERMINANT ARGUMENT FOR THE IRRATIONALITY OF ZETA(5)
Detailed exposition, 14 November 2026.

Read zeta5_detailed_argument.pdf (13 pages).

Pages 1-9 contain the main argument, with the algebraic and analytic
transitions expanded. Page 6 gives every equality between G_K(xi), the
entrywise matrix integral, and the quadratic-form integral.

Appendix A (pages 10-11) derives the classical kernel, Euler's even-zeta
formula, and the required Hurwitz formula. Appendix B (page 12) proves
exact degree. Appendix C (page 13) proves the weighted pullback identity.

The arithmetic and real-decay estimates are explicitly assumed, not
re-proved. The source qualification from the shorter overview remains:
Fauzan's original arithmetic bound is an additional input beyond Lai's
sections 8-11 as literally printed. The source note explains why.

EDITABLE SOURCES
zeta5_detailed_argument.tex is the entry point and includes
appendix_classical.tex and appendix_algebra.tex.
Keep these three files in the same folder.

BUILD
  tectonic --untrusted zeta5_detailed_argument.tex
Or compile twice with pdflatex, using standard AMS, geometry, xcolor,
and hyperref packages.

REVIEW
The expanded derivations received an independent mathematical review.
All thirteen rendered pages were visually inspected.
Borrowed arithmetic and energy estimates were not independently proved.
