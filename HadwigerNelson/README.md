# Hadwiger–Nelson: a checked reading of the five-colour proof, and local results

**No global chromatic result.** The bounds $6\le\chi(\mathbb R^2)\le7$ come from the supplied OpenAI proof (*The Euclidean plane is not five-colorable*, 23 September 2026) and the classical seven-colouring. Nothing here changes them.

## What the team contributed

Each status label comes from [RESULTS-LEDGER.md](RESULTS-LEDGER.md), which gives every result its hypotheses, file paths and SHA-256 hashes. `LEAN_VERIFIED` there means a local Lean 4.34.1 compile using only the standard axioms. Nothing has yet been rebuilt under the event's Lean 4.35.0 ([LEAN-435](RESULTS-LEDGER.md#lean-435), open).

- **A shorter Lean proof of the supplied theorem.** The proof is 150 lines shorter in total, `LEAN_VERIFIED`:
  - the encoding refactor removes 126 lines ([ENC-R4](RESULTS-LEDGER.md#enc-r4));
  - the three-centre integration removes 24 more ([R1](RESULTS-LEDGER.md#r1)).
  
  R1's contract and dependency gates pass ([R1-GATES](RESULTS-LEDGER.md#r1-gates), `TESTED_FINITE`). Two further deletion passes are in progress and are not counted: [S1](RESULTS-LEDGER.md#s1) (−265 lines, `CANDIDATE`) and S2, which is still compiling and has no ledger entry yet.
- **CC60, a closed $60^\circ$ cone obstruction** ([CC60](RESULTS-LEDGER.md#cc60), `LEAN_VERIFIED`). Suppose sets meet at one centre in a weak measurable colouring, their approach directions fit in a closed $60^\circ$ arc, and each set excludes some labels from its straddle region. Then at least three labels are excluded by none of them.
- **Refereed paper results** (`PROVED_PAPER_REVIEWED`):
  - CC60 cannot be widened for arbitrary finite palettes ([SHARPNESS-20](RESULTS-LEDGER.md#sharpness-20), a 20-colour construction).
  - In a weak measurable six-colouring, no centre carries the canonical paired palette ([A5-FOUR-LIST](RESULTS-LEDGER.md#a5-four-list)).
  - The closed-$120^\circ$ form of MC120 is false ([MC120-ENDPOINT](RESULTS-LEDGER.md#mc120-endpoint), a 19-colour counterexample).
- **Finite certificates** (`TESTED_FINITE`). These are exact checks of unit-distance graphs, censuses and direction grids, for example [HEULE-UNION](RESULTS-LEDGER.md#heule-union), [FIXED-PHASE-CENSUS](RESULTS-LEDGER.md#fixed-phase-census) and [DIR-FILTER](RESULTS-LEDGER.md#dir-filter). Each tests only the object it names.
- **A six-lesson reader of the supplied proof.** An independent referee checked each lesson against the manuscript and its Lean sources, and every figure was checked by script against what it depicts.

## Start here

| What | Where |
| --- | --- |
| Final report (PDF; the self-contained LaTeX source sits beside it) | [Exposition/Submission/report.pdf](Exposition/Submission/report.pdf) |
| Slides (PDF) | [Exposition/Submission/slides.pdf](Exposition/Submission/slides.pdf) |
| The supplied proof, one idea at a time (six lessons) | [Exposition/ProofWalkthrough.md](Exposition/ProofWalkthrough.md) |
| Every result, with its status, hypotheses, paths and hashes | [RESULTS-LEDGER.md](RESULTS-LEDGER.md) |
| Evidence summary and its limits | [PROGRESS.md](PROGRESS.md) |
| Remaining mathematical work | [ROADMAP.md](ROADMAP.md) |

## More detail

This folder collects Jarom's Hadwiger–Nelson Mathathon work. It covers the research snapshot of **14 November 2026 (Pacific time)** and the import of **15 November 2026** ([`Main/ResearchSnapshot/import-20261115/`](Main/ResearchSnapshot/import-20261115/)). It contains:
- mathematical reports;
- Lean sources and validation logs;
- exact computational certificates;
- independent reviews;
- preserved unsuccessful approaches.

| Area | Entry point |
| --- | --- |
| Research snapshot, provenance, and completeness | [Main/README.md](Main/README.md) |
| Formal proofs and validation | [Lean/README.md](Lean/README.md) |
| Exact graph and finite-family computations | [Computation/README.md](Computation/README.md) |
| Negative results and corrected claims | [Counterexamples/README.md](Counterexamples/README.md) |
| Candidate mechanisms and unfinished integrations | [Experimental/README.md](Experimental/README.md) |
| Source attribution | [Literature/README.md](Literature/README.md) |

The snapshot keeps the original directory structures, so reports can be traced back to their inputs.
- `Main/ResearchSnapshot/local` contains the local research workspace.
- `remote` contains the selected Open Math OS project files.
- `history` preserves distinct versions recovered from earlier downloads.
- `import-20261115` adds the 15 November work that the results ledger cites.

An older report, or a worker's claim, is not a current verification verdict. Use the results ledger and the corrections it links.

The archived Lean work uses **Lean 4.34.1** with **mathlib `d13f23b723b8a846827a245b89c10fc7d3f11612`**. The repository's root project uses Lean 4.35.0. The archived proof modules are not part of that root Lake target, so running the root build does not validate this archive.

This is a point-in-time record. Research running in other chats may produce later results, and those need another reviewed commit.
