# Pre-registration: continued adaptive k = 5 separation on the verified induced graph

Written **before** the run. ONE process, 60 s total, checkpoint per step.

## Grade change (upgrade, on the strength of independent verification)
`union_tau`'s edge list has now **PASSED independent local verification of all 548 628 pairs**, with a
checker that uses **no floating filter**: a strict expression parser, the field `Q(√3,√5,√11)`,
denominator bound 288, and a proven safe integer bound 5 632 740. Certificate
`certs/union_tau.json`, sha256 `cd3f9ff3a47f93d5ebb25946924531f0170a1b3fd22e1d41fcc59fd013ff7124`.

Therefore **`G_rep` = `G_ind`**: the 5487-edge graph on the 1048 points **is** the induced
unit-distance graph. Grade is upgraded from "reported embedded edge graph" to **verified induced
unit-distance graph**, and `chi = 5` holds for the true induced graph (not just the reported one).

The 17-witness / 16-step refinement also passed independent verification (110015 -> 1145 survivors,
entire list checked), so this block starts from a **verified** baseline, not a reported one.

## Reconciliation required before any new work
Two different counts were quoted for survivors with both indices `< 553`: **112** (mine) and **177**
(local). Both are computed and reported. My 112 used a provenance filter (`both endpoints A-only`),
which excludes pairs touching the 58-point overlap; the local 177 uses the index test `i, j < 553`.
These are different predicates and the difference should be the pairs with both indices `< 553` and at
least one endpoint in the overlap. **All of them are retained as candidates**; nothing is discarded on
either count.

## Restriction-map direction (kept as corrected last block)
`H` is induced in `G`. `Col(G)|_H ⊆ Col(H)`, hence **forced in `H` ⟹ forced in `G`**, equivalently
**non-forced in `G` ⟹ non-forced in `H`**. Since `H` has *no* forced pair at `k = 5`, this direction
**eliminates nothing** here. No survivor is removed by it, and no survivor is called forced.

## Rule (deterministic, adaptive)
* `W` = the 17 verified witnesses; classes are the equal-signature classes over `W`.
* `S` = set of non-adjacent pairs inside a class. Selection: lexicographic minimum of
  `(-class size, use[i]+use[j], i, j)` over untested pairs in `S` — so targets are always inside a
  remaining equal-signature class.
* Each target: solve with the combinatorial disequality constraint `c(i) != c(j)` (5 binary clauses;
  never a unit edge). On SAT verify the witness against **all 5487 edges**, retain it in full, update
  classes and `S` immediately, checkpoint. On UNSAT **stop**, save the exact CNF (and a proof only if
  the binding supports it in budget), record as **candidate only**.
* Caps: **at most 200 targets**, and stop on no survivors, first UNSAT, or the deadline.
* **Survivors are never claimed forced.** A zero survivor set is published as a no-forcing certificate
  for this graph at `k = 5`, with all witnesses as the certificate body.
