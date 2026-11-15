THE DETERMINANT ARGUMENT FOR THE IRRATIONALITY OF ZETA(5)
Concise reading version, 14 November 2026

READ FIRST
  zeta5_full_argument.pdf -- 21 pages (previous reading draft: 46 pages).
  Sections 5-7 give the main analytic and arithmetic estimates, with
  their logic, constants, and precise references to supporting proofs.

DETAILED COMPANION
  zeta5_detailed_companion.pdf -- the preserved 46-page complete version.
  Section 5: analytic bounds and the potential certificate.
  Sections 6-7: local arithmetic and prime-sum estimates.
  Appendix C: all 125 exact inner arithmetic pieces.
  zeta5_detailed_companion_sources.zip reproduces that version's sources.

The concise version keeps the integral representation in detail and
condenses the long estimate calculations. The companion supplies the
supporting proofs; these are explicitly identified where used.
Both versions use K=40n, N=3n, h=37n, cutoff M=400, capped inner weights,
and the full outer rank loss from Firsching's revised argument.

ATTRIBUTION
Persiflage guides the exposition. Prevost, Fauzan, Firsching, Lai, and
other relevant sources are credited at their points of use, in the
bibliography, and in source_ledger.json. The parallel-constructions chat
supplies explanatory organization, not a new quantitative estimate.
Persiflage's post precedes Lai; no dependence on Lai is asserted.

BUILD THE CONCISE PDF
  tectonic --untrusted zeta5_full_argument.tex
Keep parts/ beside the entry point. The three *_concise.tex files are the
active estimate sections; the longer originals are retained for reference.

REPRODUCE THE CHECKS (Python 3.10+, standard library only)
  python checks/analytic_certificate.py
  python checks/growth_exact.py
  python checks/local_checks.py
The first verifies all 684 analytic intervals with exact interval arithmetic.
The second verifies and integrates the rational arithmetic profiles.
The third supplies finite consistency checks supplementing the local proofs.
The verifiers and quantitative inputs are unchanged from the checked
complete version. The new rounded budget table is checked in
checks/condensed_budget.json.

RESULTS
  Analytic leading coefficient < -1.3669955.
  Arithmetic leading coefficient <= 1.348003127429204... < 1.35.
  Eventually 0 < Q_n(zeta(5)) <= exp(-16 n^2), with deg Q_n=37n.

VERIFICATION AND LICENSE
See VERIFICATION.txt for the scope of review and executed checks.
The complete Lean project was not rebuilt locally. The new prose is not
itself formally verified. The upstream excerpt is supplied under the
preserved Apache-2.0 license in LICENSE.upstream.txt. Original papers are
linked, not republished. The source package includes the detailed companion
and its source archive. Earlier workspace versions remain in previous versions/.
