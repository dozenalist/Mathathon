# Kepler Conjecture — Mathathon problem 15

The project seeks a simpler proof that the maximum density of congruent sphere
packings in three dimensions is `pi/sqrt(18)`. That theorem is already proved;
the research challenge is to make its proof more understandable.

Start with the [extensive plain-language overview](PROJECT_OVERVIEW.md), which
explains the accomplishments, failed approaches and remaining proof obligations.
The project has no accepted simpler Kepler proof or improved known packing bound.
Recurring check-ins were paused at the user's request on November 14, 2026;
Sair-Watch remains stopped. The user explicitly authorized publication on main.

The [cumulative progress summary](PROGRESS_SUMMARY.md) retains the history. The
[hourly updates](HourlyUpdates/) explain each checkpoint in plain language.
The [roadmap](ROADMAP.md) and [literature index](Literature/README.md) describe
the research plan and sources. [Technical progress](PROGRESS.md),
[claim ledger](Main/CLAIMS.md), and [supervisor reviews](Main/) preserve the
detailed evidence and corrections.

The main-branch publication includes the reviewed supervisor checkpoint through
08:23 Pacific, with authorship retained in Git history. The corresponding
[source manifest](Main/SYNC_2026-11-14_0823.json) identifies its worker revisions.
The overview separately links newer, unvalidated worker revisions; those are
not silently substituted for the reviewed snapshot. Importing a working result
does not certify its mathematics.
Agent reports may label a result proved before the supervisor has independently
checked it; the cumulative summary states the reviewed status.

## Historical artifact warnings

The historical `Computation/ce_laguerre.py` retains a known missing-constraint
bug for provenance. Its claimed negative result was withdrawn. Use the review
in `Computation/Reviews/27616/` to understand that failure and the canonical
Computation requests for subsequent work.

The November 14 hourly review also rejected the submitted K21 certificate.
The unsound original is frozen with [the exact rejection](Computation/Reviews/48443/README.md).
The repaired checker at that checkpoint passed its local regression suite but
still awaited independent validation. The [Gaussian-driver audit](Counterexamples/Reviews/41644/README.md)
documents a separate normalization and solver-status failure; the repair then
retained a rational-truncation bug described in [the 00:08 checks](Main/LocalChecks/2026-11-14_0008/README.md).
Frozen source copies exist solely to reproduce the original failures.
