# RR127 results, checkpoint 1 (2026-11-14)

Relation to the official objective, stated first and without inflation:
**the requested more-natural bijection is not solved.** What this checkpoint
establishes is (i) a frozen contract, (ii) a running, exhaustively verified
reconstruction of the Bressoud--Zeilberger 1982 reference map, (iii) a
kernel-checked staircase bridge, and (iv) two proved obstructions that delete
candidate design requirements from the search space. This is roadmap level 3
(reusable foundation) plus two level-2 obstruction theorems.

## 1. What is proved (written argument, all declared inputs)

**RR-C003.** Length is not preserved. `A_2 = {(1,1)}`, `D_2 = {(2)}`.

**RR-C004.** Largest part is not preserved, for every `n >= 2`.
`(1^n) in A_n` because `1 = 1 (mod 5)`. If `lambda in D_n` has `lambda_1 = 1`
then `lambda` is `()` or `(1)`, so `|lambda| <= 1 < n`. Hence `(1^n)` has no
image in `D_n` with the same largest part.
This is stronger than the finite table in ROADMAP and kills a whole class of
proposals: any rule of the form "keep the largest part, rearrange the rest" is
dead. It also explains why the largest-part-cutoff refinement cannot work
(RR-C010), so a finitized identity needs different boundary conditions.

**RR-C010.** At `n = 5`, largest-part cutoff 4: `|A_5^{<=4}| = 2`, `|D_5^{<=4}| = 1`.

## 2. What is kernel-checked (Lean)

`Lean/Staircase.lean`, `lean RogersRamanujan/Lean/Staircase.lean`, exit 0:

| theorem | statement |
| --- | --- |
| `head_bound` | `Pos (a::rest) -> Gap (a::rest) -> 2*rest.length+1 <= a` |
| `addStair_subStair` | `addStair (subStair l) = l` on positive gap partitions |
| `subStair_addStair` | `subStair (addStair l) = l`, no hypothesis |
| `sum_addStair` | `(addStair l).sum = l.sum + l.length * l.length` |
| `weight_subStair` | `lam.sum = n -> (subStair lam).sum = n - lam.length * lam.length` |
| `subStair_nonneg` | every staircase coordinate is `>= 0` |

`#print axioms` reports `[propext, Quot.sound]` for all six — inside the event's
allowed set, no `sorryAx`. Compiler: Lean 4.33.1 (see section 6).
These are the standard reductions, **not** a new result; the contribution is a
machine-checked, hypothesis-explicit version usable as project infrastructure.

## 3. What runs and is exhaustively verified (finite, not a proof)

**The BZ82 reference map.** `Computation/bz82.py` implements
`X(n) = {(j; lam) : |lam| + j(5j-1)/2 = n}` with BZ82's two involutions `phi`
(Jacobi triple product side) and `psi` (residue side), iterates `phi, psi, phi,
...` to the endpoint, and transports through `T^{-1}` to give
`forward : A_n -> D_n` and `inverse : D_n -> A_n`.

Verified for **every** `0 <= n <= 50`: forward is injective, lands exactly in
`D_n`, is deterministic and weight-preserving; inverse lands exactly in `A_n`;
both compositions are the identity. 374 objects at `n = 50`; total run 257 s.

**Faithfulness to the source.** All three printed examples of BZ82 p.315
reproduce exactly, including the full nine-state chain
`(0;4,1) -> (1;1,1,1) -> (0;2,1,1,1) -> (-1;1,1) -> (0;3,1,1) -> (1;2,1) ->
(0;2,2,1) -> (1;3) -> (0;3,2)`, and `pi((4,1)) = (3,2)`. The one place where
the scan is underdetermined is recorded as decision D-3 with a demonstration
that the literal printed rule contradicts the paper's own example.

**Interesting by-product.** On the printed examples the map *fixes* `(4,1)`
(`T^{-1}(3,2) = (4,1)`), which is consistent with `(4,1) in A_5 cap D_5`.

**Counts.** `|A_n| = |D_n|` for `0 <= n <= 50` by six independent methods; the
power-series and `q`-series methods are logically independent of both
recursions. Independent worker reproduction (m1) agrees exactly. A commonly
recalled table value (55 at `n = 24`) is wrong for this family; all six methods
give 54.

**Obstruction census.** For each `n <= 14` the number of `A_n` objects whose
largest part never occurs in `D_n` is 1,1,1,1,1,2,3,3,3,3,4,7,8 for
`n = 2..14`, with minimal witnesses (`(1^n)`, then `(4,1^{n-4})`, ...).
Independent worker m2 produced the same table; M reproduced it from scratch.

## 4. What the artifact does *not* show

Equal counts, an equal-rank matching, a finite success, a fast implementation or
a successful build of unrelated modules does **not** establish the research
claim. Specifically this checkpoint does **not** show:

* that BZ82's map is correct for all `n` (only `n <= 50`, plus source fidelity);
* that the iteration terminates in general — `Theta(n)` growth is measured
  (max 646 steps at `n = 30`), never proved;
* that any map is "more natural" — no candidate beats BZ82 on the criteria;
* anything about `Nat.Partition` or a full `lake build` (section 6).

## 5. The remaining gap, stated precisely

BZ82's map is an **iterated pair of involutions**, not a structural rule. Its
cost profile is the obstruction to naturalness: the number of `phi`/`psi` steps
grows roughly linearly in `n` (RR-C011), each step inspects residue classes mod 5
(`psi`) or the staircase head (`phi`), and the intermediate states have auxiliary
parameter `j` that a reader cannot interpret combinatorially. To improve on it
one must exhibit a rule where:

1. the forward direction is a bounded number of local moves (no orbit search);
2. the inverse is recoverable from the `D`-side object alone — no saved trace,
   no global enumeration;
3. a terminating measure is explicit, and the intermediate objects are of size
   `O(n)` or smaller and interpretable;
4. at least one structural consequence is transported (a statistic, a
   refinement, or a recognizable subfamily explained uniformly).

The two obvious shortcuts are now closed: length (RR-C003) and largest part
(RR-C004) cannot be preserved, and equal largest-part cutoffs are not an identity
(RR-C010). So any successful rule must move both the largest part and the length
for at least some objects — which is exactly why the naive "sort and adjust"
proposals fail, and why the residue-to-staircase step is the hard part.

## 6. Build and environment identity

* Python 3.12.14, stdlib only for the mathematics.
* `lean --version` = **4.33.1**, while `lean-toolchain` pins `v4.35.0` and
  `lake-manifest.json` names mathlib `56a0058...`. The Lean evidence in this
  checkpoint was produced with 4.33.1, so it is version-mismatched with the
  repository pin. Reported, not papered over.
* `import Mathlib` could not be elaborated here (measured, D-4), so
  `Lean/Staircase.lean` is Mathlib-free and **no `lake build` is claimed**.
* All timings are wall-clock on this shared VM and include contention with a
  background job; they are reproducibility notes, not benchmarks.
