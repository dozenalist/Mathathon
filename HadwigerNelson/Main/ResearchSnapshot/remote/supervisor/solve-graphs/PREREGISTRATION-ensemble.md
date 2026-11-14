# Pre-registration: bounded 5-colouring ensemble and the forced-equality question at k = 5

Written **before** execution. ONE process, 58 s internal deadline, checkpoint after every stage.
This supersedes `EXPERIMENT-disequality.md` as the block's single experiment; pair (0,39) is already
ruled out (supervisor-verified non-adjacent, separated in a checked colouring) and is not retested.

## Object
The validated Heule 553-vertex point set: 553 points in `Q(sqrt3, sqrt5, sqrt11)`, 2722 edges, every
edge exactly `d^2 = 1`, no non-edge at unit distance, vertices distinct; **149906** non-adjacent pairs.
Inputs `refs/heule_553.vtx`, `refs/heule_553.edge` are unmodified third-party files.

## Question
Is there a **non-adjacent pair that is equal-coloured in every 5-colouring** of this graph, i.e. a
forced equality at `k = 5`? Equivalently, a pair `(p,q)` with `G` 5-colourable and `G + pq` not.

## Ensemble with documented diversification (at most 8 witnesses)
Naive repeated solving is worthless here, because **permuting the colour names gives a different
assignment but the same partition of the vertex set**, and the same-colour pair set is a function of
the partition only. So diversity is enforced on partitions, not on assignments:

1. Every solution is **canonically relabelled**: scanning `v = 0..552`, the first new colour class
   encountered gets `0`, the next new class `1`, and so on. Two colourings have the same canonical
   vector **iff** they induce the same partition — so the canonical vector is a unique name for the
   partition, and colour permutations cannot masquerade as diversity.
2. After accepting a witness, a **blocking clause** is added that forbids that canonical vector
   exactly (`not(v=0,c=canon[0]) or ...`). The next solve therefore returns a genuinely different
   partition, or UNSAT if fewer than the requested number exist.
3. Hard cap **8** witnesses. Each witness is verified against all 2722 edges before use; an
   unverified witness is discarded and stops the ensemble.

## Decision procedure
For each verified witness `w`, let `S_w` = set of non-adjacent pairs `(i<j)` with equal colours.
Let `S* = intersection over all witnesses`.
* `|S*| = 0` => the saved witnesses are, between them, a **certificate** that **no** non-adjacent
  pair of this graph is forced equal at `k = 5`: every non-adjacent pair is separated by at least one
  checked colouring. This is a finite, checkable statement about **this graph only**.
* `|S*| > 0` => the survivors are **untested candidates, not forcing evidence**. At most ONE is
  tested (below).

## Pre-registered survivor selection (only if survivors exist)
Rank survivors by (a) decreasing `|N(i) cap N(j)|`, then (b) increasing `i`, then (c) increasing `j`;
take exactly the first. **One pair only, no rescan, no second pick after seeing the result.**

## Pre-registered outcome meanings for the single survivor test
* **SAT** — a 5-colouring of `G + pq` exists with `c(p) != c(q)`; requires an independently
  re-checked colouring of `G + pq`, else solver-reported only. Means this pair is not forced equal
  either; `S*` shrinks by one and the rest stay untested.
* **UNSAT** — every 5-colouring of `G` has `c(p) = c(q)`: a genuine forced equality at `k = 5` on
  this point set. Requires a checkable certificate (DRAT + `drat-trim`); if none fits the budget the
  result is recorded as **solver-reported only** and is not a verified result.
* **TIMEOUT** — **inconclusive**, in either direction.

## Scope, stated to prevent over-reading
* The added `pq` is a **combinatorial disequality constraint**. In this embedding `|p-q| != 1`, so
  `pq` is not a unit edge and `G + pq` is not a unit-distance graph. This bounds nothing about
  `chi(R^2)`.
* A SAT outcome rules out forcing **by these 553 vertices**. It does **not** show the constraint
  `c(p) != c(q)` is unrealisable by geometry: extra vertices at exact unit distance from `p` and `q`
  could in principle shrink the two palettes until they are disjoint, as the diamond forces an
  equality at `k = 3` using no non-unit edge.
* No claim about the size or structure of the 5-colouring space is drawn from solver speed or from
  the count of equal-coloured pairs.
* No exhaustive sweep over pairs; no second pair tested.

---

## Implementation correction (added before the accepted run; the text above is unaltered)

The diversification mechanism as first written was **wrong**, and the first run exposed it: it added a
blocking clause forbidding the *canonical assignment*, but a colour-permuted copy of the same
partition is a different assignment, so it is not blocked; after canonicalisation it reappears as a
duplicate. Exactly the failure the pre-registration was meant to prevent. (Run 1 therefore produced 1
witness and re-tested the already-excluded pair (0,39); kept as
`certs/ensemble_k5_RUN1_buggy.json`.)

**Fix, faithful to the intent (distinct partitions, not distinct assignments).** Add the standard
first-occurrence symmetry-breaking constraints so that **each partition has exactly one admissible
assignment**:

* `c(0) = 0`;
* for every `v > 0` and every `t` in `1..4`: `c(v) != t` OR some `u < v` has `c(u) = t-1`.

These constraints do not change the set of partitions represented (every partition has exactly one
representative satisfying them), so the blockable assignment is now a genuine partition name.
Blocking the exact assignment then blocks that partition and no other.

**Also pre-registered here:** pair `(0, 39)` is excluded by the supervisor's verified ruling. If the
selection rule would pick it, the next survivor in the same ranking is taken instead.
