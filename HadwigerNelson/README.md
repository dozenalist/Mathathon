# Hadwiger–Nelson research

This folder collects Jarom's Hadwiger–Nelson Mathathon work through the research
snapshot of **14 November 2026 (Pacific time)**. It contains mathematical reports,
Lean sources and validation logs, exact computational certificates, independent
reviews, and preserved unsuccessful approaches. **This work does not establish a
new unrestricted chromatic bound or a global six-colouring of the plane.**

Start with [PROGRESS.md](PROGRESS.md) for the evidence and its limits, and
[ROADMAP.md](ROADMAP.md) for the remaining mathematical work.

| Area | Entry point |
| --- | --- |
| Proof explanations, worked examples, and interactive geometry | [Exposition/README.md](Exposition/README.md) |
| Research snapshot, provenance, and completeness | [Main/README.md](Main/README.md) |
| Formal proofs and validation | [Lean/README.md](Lean/README.md) |
| Exact graph and finite-family computations | [Computation/README.md](Computation/README.md) |
| Negative results and corrected claims | [Counterexamples/README.md](Counterexamples/README.md) |
| Candidate mechanisms and unfinished integrations | [Experimental/README.md](Experimental/README.md) |
| Source attribution | [Literature/README.md](Literature/README.md) |

The snapshot preserves the original directory structures so that reports can be
traced back to their inputs. `Main/ResearchSnapshot/local` contains the local
research workspace, `remote` contains the selected Open Math OS project files,
and `history` preserves distinct versions recovered from earlier downloads.
An older report or a worker's claim is not a current verification verdict; use
the evidence and corrections linked in PROGRESS.md.

The archived Lean work uses **Lean 4.34.1** and **mathlib
`d13f23b723b8a846827a245b89c10fc7d3f11612`**. The repository's existing root project
uses Lean 4.35.0. The archived proof modules are not integrated into that root
Lake target; running the root build does not validate this archive.

This is a point-in-time record. Research running in other chats may produce
later results that need another reviewed commit.
