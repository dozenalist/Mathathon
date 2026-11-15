ZETA(9) FORMAL ANALOGUE
Prepared 14 November 2026.

Read the compiled PDF first. The editable entry point is
zeta9_formal_analogue.tex; its parts/ directory contains Sections 1-7,
Appendices A-C, source notes, and section handoffs.

PURPOSE
This draft shows what the algebra in Aabir Fauzan's September 2026
zeta(5) manuscript becomes for zeta(9). It retains D_N^6 and the source
parameters and normalization. It is an exploration, not an irrationality
claim or an independently verified proof of the source paper.

READING THE STATUS LABELS
Derived: the displayed local calculation was worked for this draft.
Formal analogue: a transplant whose full justification is not supplied.
Conditional: an implication that uses a stated estimate or imported input.
Blocked conclusion: the needed sign or hypothesis is missing.

The inner analytic transfer remains marked formal. The 684-interval
certificate in source Appendix A is reused, not independently rerun.
The positive combined upper bound is not a claim of actual growth.

KEY CHOICE AND RESULT
K=40n, N=3n, h=37n; the numerator stays D_N^6, not D_N^10.
The proposed arithmetic bound increases by 116581/57600 from order 5.
Its sum with U is positive, even in the infinite-cutoff limit. Thus
these bounds give no final small-value or irrationality conclusion.

SOURCES AND REPRODUCIBILITY
source_ledger.json identifies the exact source and supporting identities.
The source bundle preserves the primary PDF and extracted text, exact
check scripts/results, the editorial contract, and section handoffs.
The source file hash is recorded so equation locators are unambiguous.
Handoffs record each agent's original interface; the assembled manuscript
is authoritative where root editing clarified notation or status.

AUTHORING
Six GPT-6 Astra agents at xhigh (not ultra) handled Sections 2, 3, 4,
5 with B, 6 with A, and 7 with C. Root authored Section 1, maintained
interfaces, assembled the draft, and checked the rendered layout.
The coordination log records the limited final reconciliation.

BUILD
Run from this directory using Tectonic:
  tectonic --untrusted zeta9_formal_analogue.tex
Or use an ordinary LaTeX distribution:
  pdflatex zeta9_formal_analogue.tex
  pdflatex zeta9_formal_analogue.tex
The manuscript needs standard article, AMS, geometry, table, color,
and hyperref packages. No shell escape, bibliography processor, or
external images are required. Build tools/cache are not in the bundle.
