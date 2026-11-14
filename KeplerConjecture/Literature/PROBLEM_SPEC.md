# Problem 15 — Kepler conjecture

Prepared 2026-11-13, America/Los_Angeles, for the `KeplerConjecture` project in
[dozenalist/Mathathon](https://github.com/dozenalist/Mathathon).
The assigned official task is [Mathathon problem 15](https://competition.sair.foundation/competitions/mathathon/problems/15?q=kepler).

## Source and access status

The user's assignment supplies the research objective and detailed methodological
guidance below. On the preparation date, the official problem and participant-rule
URLs failed in the text browsing tool. Direct HTTPS retrieval of the problem URL
returned the application's generic HTML shell. The problem's rendered contents
have therefore not been independently reread in this review. The public event
overview was accessible and displayed a submission deadline of November 15,
2026, 20:00 UTC, corresponding to noon Pacific.
[Official overview](https://competition.sair.foundation/competitions/mathathon/overview)

`ASTRA.md` contains an earlier November 13 verification of the rules and schedule.
Its recorded milestones are listed below so agents can plan within the assigned
window. Refresh the rendered official pages before submission preparation.

| Milestone | America/Los_Angeles | UTC |
| --- | --- | --- |
| Round 1 starts | November 13, 2026, 8 p.m. | November 14, 04:00 |
| Problem selection locks | November 14, 2026, 11:59 p.m. | November 15, 07:59 |
| Submission closes | November 15, 2026, noon | November 15, 20:00 |
| Presentations | November 15, noon–3:30 p.m. | November 15, 20:00–23:30 |

The overview independently confirms the closing time. The other times in this
table retain the provenance of the `ASTRA.md` rules snapshot.
[Participant rules](https://competition.sair.foundation/competitions/mathathon/participant-rules) ·
[Judge rules](https://competition.sair.foundation/competitions/mathathon/judge-rules)

## Mathematical objective

For packings of congruent spheres in three-dimensional Euclidean space, the
maximum upper density is

\[
\delta_3=\frac{\pi}{\sqrt{18}}=\frac{\pi}{3\sqrt2}.
\]

The project seeks a proof with a clearer conceptual explanation and a smaller
computational burden. Hales's established proof and Flyspeck provide the
benchmark. Viazovska's dimension-8 proof and the dimension-24 extension provide
inspiration for auxiliary-function constructions. Attribution and precise source
locators are maintained in the literature index.

Use congruent unit-radius balls, hence pairwise centre distances at least 2, as
the initial convention. Define upper density and justify every passage from
finite or periodic configurations to arbitrary packings. A different scale is
acceptable after stating the conversion explicitly. The eventual claim must
identify whether it concerns all packings, periodic packings, lattices, or a
restricted family.

## Research priorities supplied by the user

1. Compare Hales's local auxiliary-function criterion, cited by the user as
   Chapter 3, Lemma 3.3 of the unabridged proof, with the Cohn–Elkies Fourier
   linear programming bound. Verify the edition and locator before importing
   its hypotheses. Track exactly where the expensive computation enters.
2. Seek a dimension-3 auxiliary bound with fewer numerical obligations. Explore
   modular constructions and other highly symmetric function classes as
   testable possibilities.
3. Explore hybrids of local geometric information with Fourier or higher-point
   bounds. Give higher dimensions a bounded share of effort when they clarify
   a mechanism that could help the 3D problem.
4. Begin with diverse mathematical approaches. Preserve an alternative geometric
   or combinatorial route alongside analytic candidates. Review progress using
   actual evidence and the size of the remaining obstruction.
5. Require numerical evidence in dimension 3 before treating a Cohn–Elkies-like
   reduction as a promising improvement. Report the achieved density bound,
   comparison baseline, arithmetic precision, feasibility checks, and outstanding
   continuum/tail conditions. Elegance of a reduction alone supplies insufficient
   evidence for promotion.
6. Keep a complete record of sources used or built upon. Search recent LLM-based
   repositories, including Hexagon. Adopt a result only after checking its
   mathematical scope and whether it provides a concrete simplicity benefit.
   See [HEXAGON_REVIEW.md](HEXAGON_REVIEW.md).
7. Treat the suggested approaches as provisional. Revise or abandon them when
   evidence identifies a more productive route.

## Agent and computation constraints

The user authorizes multiple Ultramath chats inside the KeplerConjecture SAIR
project with **at most four active chats at any time**, including the coordinator
and any delegated sessions. Time-slice the five logical roles in `ASTRA.md` to
respect this cap. Main must record the actual session identifiers and delegation
evidence.

Lean compilation and heavy computation should be offloaded to the local
supervisor. A request must include a pushed commit, exact files, pinned
dependencies, reproduction commands, anticipated resources, expected outputs,
and a precise question. The supervisor returns logs and results tied to that
commit. Until the local run succeeds, compilation and numerical certification
remain pending. Remote agents can continue independent mathematical work while
waiting for the result.

All research changes, attachments, and prompts belong to the assigned Kepler
project. Every significant result needs an entry in `PROGRESS.md`, evidence,
an independent reviewer, and a GitHub checkpoint. Follow `ASTRA.md` for watcher
ownership, completion review, and follow-up timing.

## Success and reporting

A full result proves the sharp bound for arbitrary three-dimensional packings
and explains the simplification relative to existing proofs. A useful partial
result may supply a new proved local inequality, a smaller certificate, a
quantitatively effective hybrid, a reusable formal lemma, or an explicit
obstruction to a defined function class. State each contribution's exact scope
and remaining proof obligations.

Use the repository's evidence statuses consistently. Keep empirical feasibility,
rigorous numerical certificates, written proofs, and kernel-checked Lean claims
traceable to their actual artifacts. Assess novelty against the closest known
result after translating normalization and notation. The human project lead
handles official selection and final competition submission.
