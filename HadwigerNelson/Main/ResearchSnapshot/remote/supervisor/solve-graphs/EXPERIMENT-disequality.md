# Pre-registration: one bounded equality-forcing test at k = 5

Written **before** execution. One process, wall cap 60 s, no variants, no second pair.

## Object
The already-validated Heule 553-vertex unit-distance graph: 553 points in `Q(sqrt3,sqrt5,sqrt11)`,
2722 edges, every edge exactly `d^2 = 1`, no non-edge at unit distance, vertices distinct
(`certs/heule553_4col.json`). Non-adjacent pairs: **149906** (corrected count, retained).

## What kind of edge is being added
The added edge `pq` is a **combinatorial disequality constraint**, not a unit-distance constraint.
`p` and `q` were chosen non-adjacent, so `|p-q| = d != 1`, and no unit-distance realisation can
enforce `c(p) != c(q)` at a pair at distance `d`. Adding `pq` therefore does **not** produce a new
unit-distance graph and asserts nothing about `chi(R^2)`. What it tests is whether the *coordinate
point set* already carries an **equality-forcing gadget** at `k = 5`: if `G + pq` is not
5-colourable, then every 5-colouring of `G` has `c(p) = c(q)`, i.e. the points force an equality that
no unit edge enforces.

## Steps and selection rule (fixed in advance)
1. Find one 5-colouring `c` of `G` by CDCL (`cadical153`). The graph is 5-chromatic, so one exists.
2. **Independently verify** `c` edge by edge with `verify_colouring` (a direct check, not a solver
   claim). If it fails, the experiment stops with `INVALID_WITNESS`.
3. Candidate set = non-adjacent pairs `(i<j)` with `c(i) = c(j)` — the pairs *not already witnessed
   different* by this colouring. Pairs with `c(i) != c(j)` are discarded, since `G + pq` is then
   trivially 5-SAT and the test carries no information.
4. **Selection rule (deterministic):** rank candidates by (a) decreasing `|N(i) ∩ N(j)|`
   (most locally constrained first — where a forcing gadget is most plausible), then (b) increasing
   `i`, then (c) increasing `j`. Take exactly the first. **No scan over all 7901 diamond pairs**, no
   second pair, no re-selection after seeing any result.
5. Decide `G + pq` at `k = 5`.

## Meaning of the outcomes
* **SAT** — a 5-colouring of `G + pq` exists, i.e. `c(p) != c(q)` is compatible with `G`. The pair is
  **not** forced equal at `k = 5`; this coordinate set yields no equality-forcing gadget at this pair.
  Requires an **independently re-checked** 5-colouring of `G + pq` (edge-by-edge), otherwise the
  result is solver-reported only.
* **UNSAT** — every 5-colouring of `G` has `c(p) = c(q)`: a genuine forced-equality pair at `k = 5`
  on this point set. This is a real finding and would need a **checkable certificate** (DRAT +
  `drat-trim`). If no certificate can be produced inside the 60 s budget, the result is recorded as
  **solver-reported only** and is not a verified result.
* **TIMEOUT** — **inconclusive**. Recorded as such; not evidence in either direction.

## Explicitly out of scope
* No new unit-distance graph, no new coordinates, no claim about `chi(R^2)`, no `chi >= 6` or `>= 7`.
* No claim that the chosen pair is the best possible, and no claim about the 7900+ other equal-colour
  pairs.
* The other worker's 73-cell cell-conflict 6-UNSAT graph is a different object and is not used.

---

## Correction added later (the pre-registered text above is left unaltered as the record)

Line 12 says "no unit-distance realisation can enforce `c(p) != c(q)`" at a pair at distance
`d != 1`. **That is too strong and is withdrawn.**

The correct statement is narrower: in the **fixed embedding** of these 553 points, `p` and `q` are at
distance `d != 1`, so `pq` is not a unit edge and adding it is not a unit-distance constraint. It
does **not** follow that the constraint `c(p) != c(q)` is unrealisable by geometry. Adding further
vertices at exact unit distance from `p` or `q` can in principle narrow the palettes at `p` and `q`
until they are disjoint, which *would* enforce the disequality by unit-distance constraints alone —
the same way the diamond enforces an equality at `k = 3` without any non-unit edge. Whether such a
forcing set exists for a given pair is an open question, not a consequence of `d != 1`.

Consequently this experiment tests one thing only: whether the 553-point set **as it stands** already
forces `c(p) = c(q)` at `k = 5`. A SAT outcome rules out forcing *by these vertices*; it does not
rule out forcing by a larger unit-distance graph on the same two points.
