# Rogers–Ramanujan — Mathathon problem 127

**The requested more natural bijection remains open.** The project has a
Lean-verified staircase equivalence and same-weight D/B shift, an executable
classical reference bijection with finite validation through weight 50,
local proof lemmas, obstruction proofs, and partial family formulas.

Read the **[current results summary](Main/RESULTS.md)** for achieved results,
supporting evidence, corrections and remaining gaps. Reviewed November 13,
2026, America/Los_Angeles.

- [Progress and research history](PROGRESS.md)
- [Claim ledger](Main/CLAIMS.md)
- [Problem and conventions](Literature/PROBLEM_SPEC.md)
- [Literature and attribution](Literature/README.md)
- [Dated supervisor responses](ChatLogs/)

From the repository root, with the pinned Lean 4.35.0 toolchain:

```text
lake build RogersRamanujan
python RogersRamanujan/Computation/cycle3_fast_regression.py
python RogersRamanujan/Counterexamples/checker.py 20
```

The formalized modules prove standard staircase and D/B bridges. They do not
prove the full A/D bijection or the Mathathon's proposed improvement.
