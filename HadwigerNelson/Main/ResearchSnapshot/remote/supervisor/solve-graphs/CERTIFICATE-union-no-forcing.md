# Finite certificate: the 1048-vertex union has NO forced-equal non-adjacent pair at k = 5

## Statement
Let `U` be the **verified induced** unit-distance graph on the 1048 points of
`V(H) ∪ (V(H)+τ)` (`H` = frozen Heule553, `τ = (3/2,√3/2)`), with 5487 edges, 58-point overlap and
184 new cross edges; `chi(U) = 5`. Its induced completeness has now passed independent verification of
all 548 628 pairs (checker without any floating filter, field `Q(√3,√5,√11)`).

Then:

> For **every** non-adjacent pair `{i,j}` of `U` there is a proper 5-colouring separating them.
> Hence **no non-adjacent pair of `U` is forced equal at `k = 5`.**

Stronger, and what actually holds: the 34 witnesses give **1048 distinct vertex signatures on
1048 vertices**, so every class has size 1. Every pair of distinct vertices — adjacent or not — is
separated by some witness. No pair is pinned at all.

## Certificate body
34 proper 5-colourings in `certs/refine2_witnesses.txt` (one line per witness, 1048 entries), plus the
edge list `certs/union_tau_edges.txt` (5487 edges) and the point bundle
`certs/union_tau_points.txt` (1048 points with provenance and exact coordinates). Checkable with no
solver.

## Proof from the certificate
If two vertices had equal colour in all 34 witnesses they would share a signature; all signatures are
distinct, so no two vertices do. A pair equal in every witness can therefore never be an edge (each
witness is proper), and the empty set of such pairs ranges over non-adjacent pairs vacuously: every
non-adjacent pair is separated by a proper 5-colouring. ∎

## Verification performed
Independent script over the raw files, no solver and no reuse of run state:
34 witnesses, **0** with a monochromatic edge out of 5487; **1048 of 1048** signatures distinct;
**0 classes of size > 1**; of **543 141** non-adjacent pairs, **0** lack a separating witness.

## Reconciliation of the two survivor counts (112 vs 177)
Both are correct and both are reproduced:
* **177** = survivors with both **indices** `< 553`;
* **112** = survivors with both endpoints labelled **`A`-only** (my earlier filter);
* difference **65** = the pairs with both indices `< 553` that have at least one endpoint in the
  58-point overlap (`A+B`), which the `A`-only filter excluded.

Different predicates, not a contradiction. Nothing was discarded on either count. The restriction-map
direction gives no elimination here (`H` has no forced pair, and the valid implication runs
`forced in H ⟹ forced in U`), so all 1145 baseline survivors were retained as candidates and all were
separated by the 17 new witnesses.

## Trajectory
`1145 -> 687 -> 648 -> 171 -> 158 -> 89 -> 52 -> 42 -> 33 -> 19 -> 17 -> 7 -> 6 -> 5 -> 3 -> 2 -> 1 -> 0`
in 17 adaptive targets, 3.65 s total, no UNSAT at any step.

## Scope
This is about `U` at `k = 5`. It does **not** say that no unit-distance graph has a forced-equal pair,
does not bound the method, and makes no claim about `chi(R²)`. A forced pair elsewhere would still give
an explicit 6-chromatic graph through the geometry branch's amplifier — useful, but not a new
6-vs-7 bound.
