> Historical snapshot. Superseded by ../RESULTS.md; retained for provenance.

# RR127 results, checkpoint 2 (2026-11-14, America/Los_Angeles)

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

## 3a. Withdrawals made in cycle 2

Three statements from checkpoint 1 were wrong or overstated, and are withdrawn
here rather than edited away silently.

1. **The claim that BZ82's printed `phi` Case II formula is defective is
   RETRACTED.** It rested on a `z >= 1` restriction that I had added to the
   printed range `0 <= z <= a+2j-2`. With the printed range, the rule is complete:
   0 defects in `phi(phi(s)) = s` over all 66 658 in-domain states of weight
   `<= 30`, and the admissible set is nonempty on all 10 285 Case-II states of
   weight `<= 25`. The state I offered as a counterexample,
   `(0;(2,1,1,1))`, is *correctly* sent to `(-1;(1,1))` by `z = 0`. My
   implementation was behaviourally faithful all along (0 discrepancies) because
   its fallback to `m = 0` exactly compensated. Correction found by the
   supervisor. Full record: `Counterexamples/REGISTRY.md` RR-X005,
   `Main/DECISIONS.md` D-3.
2. **"`Theta(n)` empirically" and "roughly linearly" are withdrawn.** Thirty-one
   data points, with the maximum non-monotone in `n`, cannot support a growth
   class. RR-C011 now records raw maxima, means and extremal objects only.
3. **"Six independent counting methods" is corrected** to the honest grouping:
   the power-series product and the residue coin-change DP are the same
   recurrence and cross-check transcription, not mathematics. The genuinely
   informative comparisons are the gap recurrence, the `q`-series
   `sum_t x^{t^2}/(x;x)_t` (whose equality with the product *is* the identity),
   and the unconditional all-partitions filter for `n <= 20`.

Also corrected: a hand-recalled sequence table inside `rr_core.py` is retired
(no remembered table is used as an oracle), and `run_checks.py` now actually tests
the generic-filter gap count it computes, which checkpoint 1 omitted.

## 4. What the artifact does *not* show

Equal counts, an equal-rank matching, a finite success, a fast implementation or
a successful build of unrelated modules does **not** establish the research
claim. Specifically this checkpoint does **not** show:

* that BZ82's map is correct for all `n` (only `n <= 50`, plus source fidelity);
* that the iteration terminates in general — measured trace lengths reach 646
  edges at `n = 30` (see RR-C011, raw data only; an earlier "`Theta(n)`" phrasing
  is withdrawn), and nothing here proves a bound;
* that any map is "more natural" — no candidate beats BZ82 on the criteria;
* anything about `Nat.Partition` or a full `lake build` (section 6).

## 5. The remaining gap, stated precisely

**Scope warning about this section.** The four criteria listed below are this
project's own working criteria for judging a candidate construction. They are
**not** requirements imposed by the official problem, and satisfying them is not
the definition of "natural". The official statement asks for "a more natural
bijection" without defining naturalness, so a candidate that fails one of these
criteria — for instance by using transparent recursion, bounded local
iteration, or a small auxiliary state — may still be a substantive and
publishable answer. Conversely, meeting all four is not proof of interest. They
are a checklist for comparison, not a filter.


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
* Lean: the supervisor compiled `Lean/Staircase.lean` (SHA256
  `C7ACBCD74866958596ACC458A7231939EBE01969A0723179BFDAAF263CBEB280`) with the
  **pinned** Lean 4.35.0 (commit `eb6cafb7290e8bd5f2937522d8d804f58f02bafc`),
  exit 0, axioms `[propext]` for `subStair_addStair` and
  `[propext, Quot.sound]` for the other five. The local VM's executable is
  4.33.1, which produced the same axiom sets. The cycle-1 "toolchain mismatch"
  caveat is therefore retired; what remains is that weak-decreasingness is not
  yet formalized, so the six declarations are not yet a staircase equivalence.
* `import Mathlib` could not be elaborated here (measured, D-4), so
  `Lean/Staircase.lean` is Mathlib-free and **no `lake build` is claimed**.
* All timings are wall-clock on this shared VM and include contention with a
  background job; they are reproducibility notes, not benchmarks.

---

## 7. Cycle 4: corrections to this document

This section exists because the earlier sections, while labelled with their scope,
contained claims that turned out to be wrong. They are corrected here rather than
edited away.

**7.1 `B` is not `D`.** `B_n` = partitions whose smallest part is at least their
length; `D_n` = partitions with successive gaps at least 2. `T` (RR-C006) bridges
them, and every statement must name which side it is on. A `B`-object need satisfy
no gap condition at all: `(25,17,8,8,8,8)`, adjacent differences `8,9,0,0,0`, is a
valid `B_74` element.

**7.2 The cycle-3 rejection of a worker's witness is retracted.** Main reported
that the committed map gives `(30,20,9,7,5,3)` "in 5 steps" for `(4^3,1^62)` and
that the worker's `(25,17,8,8,8,8)` "cannot be an image". Both halves were wrong:
* `(25,17,8,8,8,8)` is the **`B`-endpoint** (`pi_forward`), correct and valid
  in `B_74`; `(30,20,9,7,5,3)` is the **`D`-image** (`forward = T^{-1} ∘ pi_forward`),
  and `T^{-1}(25,17,8,8,8,8) = (30,20,9,7,5,3)` entry by entry. Main tested a
  `B`-object with the `D` predicate `is_gap`.
* "5 steps" was a measurement bug: `tr, _ = pi_forward(p)` binds the **endpoint**
  to `tr`, so `len(tr)-1` was the endpoint's part count. The trace is
  **1 911 states = 1 910 edges**.
The worker's P3 refutation therefore stands, in `B`-space, with its own witness.

**7.3 The R2 slot identities are TESTED_FINITE, not proved.** They were briefly
labelled PROVED on the strength of a Main-run census, while the worker's artifact
said "NOT PROVED; reduced to R2". What is now verified finitely, over all in-domain
states of `weight <= 23` (6 224 each way), is R2.1 as a **multiset** with virtual
slots, R2.2, and both Case-I duals R2.1′/R2.2′. R2.3/R2.3′ are not re-checked and
no all-input proof exists. A created part may tie with a decremented one or be `0`
in a virtual slot, so a *positional* statement is ill-defined under ties while the
*multiset* statement is tie-invariant — that is the form a proof should target.

**7.4 Overstatements removed.** "`z ↦ z+λ(k−z)` is monotone on all of `Z`" is false
across `z = k`, where `λ(0) = 0` makes it step down (`k=10, λ(1)=5`: `f(9)=14 >
f(10)=10`); it is monotone only on `z <= k-1`, which is the printed range.
"Non-preservation of length shows it cannot be a progress measure" is also too
strong: what is true is that `t` is not monotone along a path. The claim that the
Case-I insert count needed a divisibility-by-five check was simply wrong.

**7.5 Current status of the objective.** Unchanged and open. What cycle 4 adds is
negative knowledge and a cleaner gap: `phi` is a *reduction* (R1 inequalities plus
R2 multiset identities) rather than a proved involution; the family `(4^r,1^s)` has
closed forms for `phi` and `psi∘phi` on all parameters but no inverse
characterisation of its image, and its cost varies from two edges to beyond a
20 000-edge cap. No candidate map is more natural than BZ82 on this project's
criteria, and no comparison with Garsia–Milne is possible because GM81b remains
inaccessible.
