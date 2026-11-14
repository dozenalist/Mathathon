# Proof-gap ledger

Every open obligation, its owner, and precisely what would close it. "Closed"
means an artifact exists and has survived review; nothing here is closed by
assertion. Maintained by M; reviewer X.

| # | Gap | Blocks | Owner | What closes it | Status |
| --- | --- | --- | --- | --- | --- |
| G1 | Periodic → arbitrary packings: K15-C002b's estimate is repaired but unaudited | every CE-type bound, incl. `VERIFIED_CROSS` C023's scope | X | line-by-line audit of Lemma 1.2 as repaired (`#C_in ≤ vol/S³`, additive errors, `c = 0` case) | open |
| G2 | Tammes-13 directed enclosure `θ₁₃ < arccos(1 − 2/ρ²)` | shell count 12 | E → M audited (K15-C027) | done at `ρ = 2.09` subject to Musin–Tarasov Thm 1; X to check the transcription of the defining equations | closed pending X |
| G3 | Contact number `n = 12` on a shell of positive width | K15-C018 sharp form | E → M audited | G2 (`ρ = 2.09`, unconditional in the arithmetic) | closed pending X |
| G4 | Specified partition rule for the cluster criterion (the universal form is false) | K15-C025 H2 | E | a rule + boundary estimate, checked on the icosahedral 13-cluster | open |
| G5 | Analytic cluster-volume lower bound at `D = 2` | K15-C025 H3 | E | a Rogers-simplex or Fejes Tóth type inequality restricted to the cluster, with the constant exhibited | open |
| G6 | Negligibility of the correction `A` | K15-C025 H4 | E/M | an explicit `A` with `Σ A ≤ C₁r²` proved, not sampled | open |
| G7 | A value `V_0 > 5.550291` for the cluster inequality | beating the dodecahedral barrier | E | G4+G5+G6 and a computation of the cluster minimum | open |
| G8 | Independence audit of the two exact checkers | `VERIFIED_CROSS` C023's status | X | confirm C's `exactcert` and Main's `shell_check` share no code path and agree on adversarial vectors (the interface test `interface_xcheck.py` is a start) | open |
| G9 | Lean: ball-volume identity and counting-to-volume bridge | any Lean-verified density claim | Astra (local) | a pinned build of a module proving `volume (ball 0 1) = 4π/3` and the count bound; current `Normalisation.lean` proves neither | not started |
| G10 | Shell-allowance gain: is it 0 in reality or only at degree 21 / grid 500? | whether the shell route is dead | C, or M's duality sketch | an exact-certified `η > 0` candidate at any degree, or a duality argument that the CE optimum's shell multiplier vanishes | open (measured 0 once; the count is no longer the obstruction after G2/G3) |

## Rules the ledger enforces

1. No gap is closed by a finite grid (review 27616).
2. A failed search is evidence about the search, never an impossibility theorem
   (K15-C014r, the shell benchmark's gain 0).
3. A bound enters `Main/CLAIMS.md` only as `VERIFIED_CROSS` (two independent
   exact implementations) or `PROVED`; `TESTED_FINITE` never enters `RESULTS.md`
   as a bound.
4. Every status change names the artifact and its hash.
