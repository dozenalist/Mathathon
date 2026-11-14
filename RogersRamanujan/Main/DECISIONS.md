# RR127 decisions log

Owner: M (Main). Append-only. Each decision records what was frozen, why, and
what would have to change to revisit it.

## D-1 (2026-11-14) Contract frozen as specified by the roadmap.

Representation: a partition is a **descending tuple of positive integers**;
`()` is the unique partition of 0. `A_n` = parts in {1,4} mod 5 with multiplicity
allowed; `D_n` = `lambda_i >= lambda_{i+1} + 2`, smallest part 1 allowed.
The eight interface functions are `is_partition`, `weight`, `is_residue`,
`is_gap`, `enumerate_residue`, `enumerate_gap`, `forward`, `inverse`, plus
`trace`. Implemented once in `Computation/rr_core.py` (canonical) and
independently re-derived in `Counterexamples/checker.py` (adversarial).
Invalid input raises `ValueError`; nothing is silently sorted, deduplicated or
truncated.

## D-2 No length preservation and no largest-part preservation.

`n = 2` gives `A_2 = {(1,1)}`, `D_2 = {(2)}`, so length cannot be preserved by
*any* weight-preserving bijection. Independently, largest-part cannot be
preserved, and the obstruction is an all-n theorem, not a finite accident:
`(1^n) in A_n` for every `n >= 2` (since `1 = 1 mod 5`), while a partition in
`D_n` with largest part 1 is `(1)` or `()`, of weight at most 1. Hence for every
`n >= 2` at least one `A_n` object is *forced* to change largest part.
Verified with witnesses in `Counterexamples/REGISTRY.md` (RR-C003, RR-C004).
Consequence: "fix the intersection A_n cap D_n" stays a **candidate design
choice**, not a requirement; the intersection is empty at `n = 2,3,8` and has
size 1 at `n = 0,1,4,5,6,7,9,12,13`.

## D-3 BZ82 phi, Case II: the scan is underdetermined; one rule reconstructed.

BZ82 p.314 prints `m = Max{z <= a+2j-2 : z + lam(a+2j-1-z) <= t+5j-2}` and
creates parts `m` and `t+5j-3-m`. That printed rule is not consistent with the
paper's own examples:

* its admissible set is **empty** at `(0;(2,1,1,1))`, which the printed chain of
  example (3) must send to `(-1;(1,1))`;
* at the same time `z = 0` occurrences are needed, i.e. the index
  `a+2j-1-z` reaches 0.

Since the two created parts enter only as the unordered pair `{m, hi-m}` with
`hi = t+5j-3`, the choice of `m` is invisible whenever both are positive, and
the two readings differ only where the pair degenerates. Decision: take
`m = Max{1 <= z <= a+2j-2 : ...}`, and **default to `m = 0` when that set is
empty**, which degenerates the pair to the single part `hi` (or to nothing when
`hi = 0`). This is the unique completion under which `phi` is an involution.

Evidence: exhaustive census over all 33 329 Case-II states of weight <= 30.
Under this rule `phi(phi(s)) = s` on **every** state of its declared domain for
`n <= 25` (0 defects), `psi(psi(s)) = s` on **every** state of its domain for
`n <= 25` (0 defects), and all three printed examples reproduce exactly,
including the full nine-state chain of example (3). Under the literal printed
rule, `phi` has 2 692 defects at `n <= 18` and the inverse iteration cycles.
Label: **implementation with one reconstructed rule**, not a verbatim
transcription; recorded in `Literature/READING_NOTES.md` follow-up RR-L004.

## D-4 Lean target reduced to a Mathlib-free staircase module.

`import Mathlib` does not complete on this VM: a trivial `import Mathlib` file
exceeded 240 s with only 1.5 s user time and 27 s sys time (6.4 GB of olean
reads against 15 GB RAM, 0 GB free, 7 GB available, while a background job also
ran). `lean` startup for a core-only file is ~5-14 s. Decision: `Lean/Staircase.lean`
imports only `Init` and uses only `omega`/`simp`. Consequence, stated as a gap:
the file does **not** connect to `Nat.Partition`, and the `T`/`B_n` bridge is not
yet formalized. `lake build` is **not** claimed; the recorded verification
command is `lean RogersRamanujan/Lean/Staircase.lean`.

## D-5 Route selection for the next cycle.

Keep R1 (simplify the BZ82 orbit segments) and R2 (residue multiplicities versus
Dyson/Durfee coordinates). Stop the "rank-matching" control: it is a
control experiment, not progress on the objective. Do not pursue HEX26 until an
invertible weight-compatible bridge to `A_n`/`D_n` exists. Reason: the whole
value of the checkpoint is that the reference map now runs, so the productive
next question is *why* it needs an orbit of length Theta(n) at all.
