# Task board — Kepler problem 15

Cycle 1 (2026-11-14). Owner columns: **M** = Main/Lean planning
(`based-on-the-chats-e0wz`), **C** = Computation (`using-the-chats-in-mcl6`),
**E** = Experimental (`i-ve-attached-thomas-4iws`), **X** = Counterexamples
(`i-ve-attached-viazovska-f7hh`). At most four sessions run at once.

| # | Task | Owner | Reviewer | Status | Artifact |
| --- | --- | --- | --- | --- | --- |
| T1 | Freeze contract, claim ledger, decisions, task board | M | X | **DONE** | `Main/CLAIMS.md`, `Main/DECISIONS.md`, this file |
| T2 | Recover earlier unpushed notes into Git with checksums | M | X | **DONE** | `Literature/RECOVERED.md` |
| T3 | Reproduce the published `d=3` two-point value `0.779747` | C | X | BLOCKED on local run | `Computation/` (C's branch) |
| T4 | Certified two-point LP at degree `n ≤ 40` in the Laguerre basis | C | X | BLOCKED on local run | `K15-COMPUTE-001` |
| T5 | Test `(LC(A,n))` for shells around fcc/hcp/Barlow; decide if any `A` can pay | E | X | OPEN | `Experimental/` |
| T6 | Multiplicative (per-cell normalised) hybrid to replace the killed additive one | E | X | OPEN | `Experimental/` |
| T7 | Independent audit of Li Thm 6.1 scope and normalisation | X | M | OPEN | `Counterexamples/` |
| T8 | Audit K15-C004/C011 repair and K15-C002 Lemmas 1.1–1.3 | X | M | OPEN | `Counterexamples/` |
| T9 | Lean: exact `V_HM` + `δ = (4π/3)c` + count `⌊(3+δ)³⌋−1` | M → local | X | **DRAFTED, awaiting local compile** | `Lean/Kepler15/Normalisation.lean`, `K15-COMPUTE-002` |
| T10 | Decide whether the "finite certificate" route (SOS in the Laguerre basis) is worth a second numerical block | M | C | OPEN | decision after T4 |

## Next bounded package (highest value)

1. **X** audits K15-C002/C003/C005 and Li's theorem; returns objections with
   witnesses. Without this, nothing in the ledger moves to `PROVED`.
2. **C** runs `K15-COMPUTE-001` (certified two-point LP, degrees 12–40) and
   reports the degree-versus-constant curve in both normalisations.
3. **E** answers T5: whether a *tolerance* kissing-type bound exists for shells
   of width `δ ∈ (0, 0.0366)` with `n < 26`. This is the one place where a new
   local theorem would re-open a closed route (D5).
