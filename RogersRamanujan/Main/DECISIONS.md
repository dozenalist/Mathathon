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

## D-3 (REWRITTEN 2026-11-14) BZ82 phi Case II: no defect; a cycle-1 error retracted.

**Cycle 1 recorded that BZ82 p.314's `phi` Case II rule is underdetermined and
that one rule had to be reconstructed. That decision was wrong and is withdrawn.**

What happened: in transcribing
`m = Max{z <= a+2j-2 : z + lambda(a+2j-1-z) <= t+5j-2}` I silently added a lower
bound `z >= 1`. That made the admissible set empty on `(0;(2,1,1,1))`, which I
then reported as a defect in the paper. The printed rule has no lower bound
beyond `z` being a nonnegative integer, and with `0 <= z <= a+2j-2` the index
`a+2j-1-z` ranges over `1..a+2j-1`, i.e. exactly the padded range of `lambda`.

Corrected position, now adopted everywhere:

* **The printed rule is complete as printed.** 0 defects in `phi(phi(s)) = s`
  over all 66 658 in-domain states of weight `<= 30`; the admissible set is
  nonempty on every one of the 10 285 Case-II states of weight `<= 25`.
* **No reconstructed rule is used anywhere.** `RR-C009` is a faithful
  transcription, not a transcription plus a tie-break.
* **The cycle-1 implementation was behaviourally correct** (0 discrepancies with
  the printed rule over the same range) because it fell back to `m = 0` when its
  restricted set was empty. So no computed number, table or verdict in cycle 1
  changes; only the *claim about the source* does.
* **The "existence of the maximum" question is answered sharply** (worker m3,
  re-derived by Main): the admissible set is empty exactly on the states outside
  `phi`'s domain — 893 such states among the Case-II states of weight `<= 30`,
  all of them in `0 x B(n)`, and 0 of the 33 329 in-domain Case-II states. So the
  maximum exists exactly where the rule is meant to apply, and its non-existence
  is the domain boundary. Verified finitely (`n <= 30`); the all-`n` statement is
  the same equivalence and remains to be written as a lemma.
* **Sharp form of the existence question (cycle 2, worker m1, verified by Main).**
  The Case-II admissible set is a **down-set** in `z`, so `m` exists **iff**
  `a+2j-2 >= 0` and `lambda(a+2j-1) <= t+5j-2`. Both halves verified by machine
  over all 33 329 in-domain Case-II states of weight `<= 30` with 0 failures. So
  the residual obligation is two explicit inequalities, not a search.
* **`t*` convention pinned.** `t*` = `t` real slots plus one virtual slot at each
  of `a`, `mu` exceeding `t`. The rival "pad to length `t*`" reading breaks
  weight preservation; the committed code already used the correct reading.

Retraction is recorded at REGISTRY RR-X005 with the mistaken interpretation and
its resolution, per the project's rule that refuted and superseded claims are
kept with their scope.

The forced tie-breaks of D-3a are unaffected: they concern `psi`, not `phi`.

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

## D-3a (2026-11-14, after the first checkpoint) The D-3 tie-breaks are forced, not chosen.

Worker m3's report prompted a direct test. Each `psi` comparison was flipped in
turn and the involution census rerun on all 3198 in-domain states of weight
`<= 18`: the chosen reading gives 0 failures, flipping the I(a) tie gives 1120
(first witness `n=4`, `(0;(2,2))`, where `I(b)` would need `k = -1` copies of 5),
flipping the II(a) tie gives 374 (first witness `n=3`, `(-1;())`), and keeping a
created part 0 in II(a) also gives 374 at the same first witness. So the `>=`
readings are the unique ones under which `psi` is a well-defined involution on
`X(n) \ {0} x A_n`. This matters because RR-C008's step (d) *uses* the tie-breaks:
without the forcing argument, that proof would be about a variant of BZ82's map
rather than about BZ82's map. Registered as RR-X006.

Also recorded: my original task statement to worker m3 asked whether "every
orbit reaches `{0} x A_n`". That question is **mis-posed** — the orbits of an
involution are 2-cycles and never reach the fixed set; the correct statement is
the disjoint decomposition `X(n) = ({0} x A_n) ⊔ 2-cycles`. The worker caught
this. Same correction applies to the earlier phrasing in `Main/CLAIMS.md` RR-C008.

## D-6 (2026-11-14, cycle 2) Route status after the subfamily results.

R1 ("simplify a recurring orbit segment with a proved arithmetic rule") is
**partially achieved and closed on one ray**: Theorem F gives a closed form for
`(1^s)` in four of five residue classes with at most six steps, and RR-C015
proves the fifth class cannot close in two steps for `s >= 30`. So the segment
`(0;(1^s)) -> (-1;(s-3)) -> ...` is understood rather than merely tabulated.

What this does and does not buy:
* It is a **proved infinite-subfamily result**, which is roadmap level 2, and it
  is the first project result that engages the naturalness question with a
  theorem.
* It does **not** give a new bijection: it describes BZ82's own endpoints on a
  thin ray. Nothing here replaces iteration globally.
* The obstruction is the useful part: the difficulty is concentrated in
  `s = 0 (mod 5)`, and RR-C015 says why (`(5^{s/5})` leaves `B` exactly when
  `s > 25`). Any future closed-form proposal for a family should be tested
  against that same `B`-membership criterion first.

Route selection for cycle 3: **stop** broad mechanism search (M1/M2 both blocked
on a named lemma, and 4 refutations on held-out parameters are recorded);
**continue** only the `B`-membership-criterion route on families, and put the
effort saved into the two open proof obligations (all-`n` `phi` case stability
and `phi^2 = id`), because those are now the only things between this project and
a completely proved reference map.
