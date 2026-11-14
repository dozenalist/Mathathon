# Pre-registration (written before execution)

Registered at the start of the block; the run below is the single registered computation of the
block, one process, hard cap 60 s, no variants, no re-runs with changed parameters.

## Graph
The **already-validated** Heule 553-vertex 5-chromatic unit-distance graph, exactly as established
in this branch's earlier block: 553 points in `Q(sqrt3, sqrt5, sqrt11)`, 2722 edges, every edge
exactly unit distance, no non-edge at unit distance, all vertices distinct
(`certs/heule553_4col.json`). No new coordinates, no new graph, nothing re-derived.

## Threshold
k = 6.

## Meaning of the two outcomes
* **SAT at k = 6** => an explicit 6-colouring exists => this graph yields *no* lower bound on
  `chi(R^2)` beyond the already-recorded 5-chromatic-ness. Expected, because the graph is
  5-chromatic. This outcome is **uninformative about chi(R^2)** and is registered so that the
  branch's own limitation is stated, not assumed.
* **UNSAT at k = 6** => a validated 6-UNSAT unit-distance graph => `chi(R^2) >= 7`. This would be
  a major result, would require independent review before any assertion, and is not expected.

## The informative, falsifiable part (registered predictions)
The mathematical content of this block is Theorem C (see GLUING.md). Applied to this real,
genuinely 5-chromatic object it predicts exactly three things:

* **P1** `omega(G) <= 3` (no `K_4`: four pairwise-equidistant points do not exist in the plane).
* **P2** every non-adjacent pair has at most **2** common neighbours.
* **P3** a non-adjacent pair has exactly 2 common neighbours **iff** `|pq|^2 = 3` (exactly, in the
  field), and in that case those two common neighbours are joined by a unit edge.

## Falsification
If any of P1, P2, P3 fails on this object, **Theorem C is wrong** and that failure is the result.
If all three hold, they hold as stated and Theorem C's palette cap (`k - 2`, never `k - 1` for
`k >= 4`) applies to a real 5-chromatic graph, not merely to my block-1 specimens.

## Explicitly out of scope
* No claim about `chi(R^2)`, no claim of `chi >= 6` or `>= 7`.
* The other worker's 73-cell **cell-conflict** graph is a different object (cells, not points);
  its 6-UNSAT says nothing about unit-distance point graphs and is **not** transferred here.
