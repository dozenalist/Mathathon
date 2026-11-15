ZETA(5) TO ZETA(7): INDEPENDENT EXPLORATION
14 November 2026

Start with output/zeta7_argument_audit.pdf (11 pages).
Pages 2-4 follow the opening equations in order. Pages 5-8 locate the
arithmetic failure. Page 9 shows that the leading real bound survives.
Page 10 tests the D_N^8 repair, and page 11 records sources and checks.

Main findings

1. The correct zeta(7) functional retains a positive moment representation,
   a nonzero determinant, and the same degree. It introduces no other odd
   zeta values.
2. An unchanged local bound is false: for K=40, N=3, p=29, it predicts
   valuation at least -60, whereas the constant determinant coefficient
   has exact valuation -82. Two independent exact algorithms agree.
3. Correcting the arithmetic raises the explicit K^2 normalization bound
   by 751/768. The final coefficient becomes +0.960456781075... rather
   than -0.017407802258... . This is failure of the specified upper-bound
   argument, not a lower bound on the actual determinant values.
4. The D_N^8 variant improves arithmetic but changes the real problem.
   With the original comparison measure and the specified arithmetic
   bound, a single-point rational interval certificate proves that the
   final certificate coefficient must exceed 1.3.

Reproduce the exact checks (Python 3, standard library only)

  python experiments/exact_checks.py
  python arithmetic_costs.py
  python arithmetic_exact_inner.py
  python experiments/single_point_certificate.py
  python experiments/main_measure_certificate.py

The third command regenerates arithmetic_variant_results.json and
checks the complete rational value of the source's equation (5.18).
The fourth uses this JSON and produces a rational interval witness.
The fifth shows that sharper enclosures of the original comparison
measure cannot rescue the fixed D_N^6 local-valuation certificate either.
The first writes experiments/exact_checks.json, including both rational
Gaussian-elimination and modular-valuation results.

Detailed derivations

  algebra_notes.txt
  arithmetic_notes.txt
  arithmetic_variant_notes.txt
  additional_checks.txt

Sources

  sources/source_ledger.json
  sources/Fauzan_2026_zeta5.pdf
  sources/Fauzan_2026_zeta5.txt

The source ledger preserves URLs, manuscript version, audit scope, and
SHA-256/MD5 hashes. The report distinguishes literature inputs from the
new transfer calculations. No previous chat analysis was used.

Supplementary numerical exploration

  python experiments/energy_probe.py
  python arithmetic_variant.py

These optional probes use NumPy. The final conclusions do not rely on
the sampled potential maximum. The exact interval check is separate.

Report generation

  python build_report.py

The authoring script uses ReportLab and the Windows Cambria fonts. This
dependency is only for regenerating the PDF, not for the mathematical
checks. The report was rendered and visually checked before delivery.

Scope

This exploration diagnoses the specified transfer of Fauzan's argument.
It does not prove zeta(7) irrational, prove that the true determinant
values grow, or exclude better arithmetic bounds, measures, or parameters.
