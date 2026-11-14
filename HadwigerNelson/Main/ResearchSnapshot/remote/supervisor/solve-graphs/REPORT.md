# Block report: explicit finite unit-distance obstructions (pilot)

Owner: `supervisor/solve-graphs`. Block: 2026-11-14 05:10–05:56 UTC. Everything here is
machine-checked exactly; nothing here is a statement about `chi(R^2)`.

## 1. What was built

* `udg/exact.py` — exact arithmetic in `Q(sqrt d_1,...,sqrt d_m)` (basis `{prod_{i in S} d_i}`,
  `Fraction` coefficients, no floating point, no division needed). Pairwise-coprime squarefree
  radicands are asserted to make the basis multiplicatively closed.
* `udg/graph.py` — point sets over that field, the **exact** unit-distance graph they define
  (edge iff `d^2 = 1` holds as a field identity), a second independent validation by 60-digit
  `mpmath` evaluation (`max |d^2-1|` over edges, `min |d^2-1|` over non-edges), K_4-freeness
  (max clique), exhaustive colouring *counting* with witnesses, a CNF encoder, and CDCL decisions
  with two independent solvers (`cadical153`, `minisat22`). SAT assertions are re-verified on the
  witness; UNSAT is cross-checked by the complete exhaustive count.
* `udg/build.py` — exact constructions: the diamond, the Moser spindle, spindle chains, and the
  "common unit neighbour" operation `add_diamond` (valid on segments of length^2 1 or 3, with exact
  post-conditions asserted: each new apex is at distance 1 from both ends, apex separation `sqrt(4-d^2)`).
* `pilot.py`, `certs/`, `logs/pilot.out`, `certs/table.md` — the experiment.

## 2. Verification status of the geometric objects

All graphs are realised in `Q(sqrt 3, sqrt 11)`; coordinates are exact field elements, never floats.
For every graph: all points distinct (coincidences merged and counted), every edge satisfies
`d^2 = 1` *identically* (numeric deviation `< 1e-60`), the closest non-edge has `|d^2-1| >= 0.372`,
and the clique number is 3 (unit-distance graphs are `K_4`-free; checked, not assumed).

## 3. The ladder (controls, with exact counts of proper colourings)

Number of proper `k`-colourings of the labelled graph (complete enumeration; 0 means UNSAT):

| graph | n | m | k=2 | k=3 | k=4 | k=5 | k=6 |
|---|---|---|---|---|---|---|---|
| diamond (`K_4` minus an edge) | 4 | 5 | 0 | **6** | 48 | 180 | 480 |
| Moser spindle | 7 | 11 | 0 | **0** | 384 | 5040 | 31680 |
| double-lens (spindle + both unit neighbours of the closing pair) | 9 | 15 | 0 | **0** | 1536 | 45360 | 506880 |

Each row is also decided by the two CDCL solvers, agreeing with the count in every cell; every
nonzero cell has a witness colouring saved in `certs/*.colouring.json` and re-verified.
`chi = 3` for the diamond, `chi = 4` for the other two: the 3-UNSAT of the spindle is a genuine
4-chromatic certificate for a `K_4`-free unit-distance graph.

## 4. The amplification mechanism, and its exact point of failure

The spindle mechanism is the only known finite device that forces a *non-unit-distance* pair to be
equal: a **diamond** has an edge `ab` and two common unit neighbours `t1,t2` (so `|t1-t2| = sqrt 3`);
in any proper `k`-colouring `c(t1),c(t2)` avoid the two distinct colours of `a,b`.

**Proposition.** For `k >= 3` the diamond forces `c(t1) = c(t2)` iff `k = 3`; for `k >= 4` both
relations occur. Hence every graph built from diamonds and unit edges is at most 4-chromatic: the
spindle chain, iterated any number of times, can never reach 5 colours, let alone 6.
*Proof:* the two colours of `a,b` are distinct, so `t1,t2` range over the remaining `k-2` colours;
forced equality happens iff `k-2 = 1`. Both relations are realised for `k >= 4` (colour `t1 != t2`
with two fresh colours). Counts, verified exhaustively (`certs/pilot.json`, `diamond_tip_relation`):

| k | # colourings with `c(t1)=c(t2)` | with `c(t1)!=c(t2)` |
|---|---|---|
| 3 | 6 | **0** (forced equal) |
| 4 | 24 | 24 |
| 5 | 60 | 120 |
| 6 | 120 | 360 |

**Secondary geometric fact (falsifies local iteration).** Let `U(p,q)` be the two common unit
neighbours of a unit pair. `U` applied twice returns the original pair: on the closing edge `(C1,C2)`
of the Moser spindle the two new points of `U(U(C1,C2))` coincide exactly with `C1` and `C2`. My
construction detects this (2 coincident points merged), so the "lens stack" is an involution, not an
amplifier, and `+d2 == +d1` as graphs. This is why decorating cannot be iterated.

**Forced-pair census (exhaustive, scope-limited).** For every non-adjacent pair of every graph above
(10–21 pairs per graph) and each `k in {3,4,5,6}` I decided both `G/pq` (is `c(p)=c(q)` possible?)
and `G+pq` (is `c(p)!=c(q)` possible?). Result: at `k >= 4` **no pair is forced either way** in any
of these graphs; the only forced pair in the whole family is the diamond's tips at `k = 3`.
A reported forced relation was re-derived by a complete exhaustive count and had to be 0.

## 5. Honest accounting and non-claims

* The three "different" spindle graphs I built are only **three** distinct graphs: the "spindle
  triangle" (3 tips, diamonds on two consecutive `sqrt 3` segments, closing unit edge) is
  **isomorphic to the Moser spindle** (same degree sequence `(4,3,3,3,3,3,3)`, same 11-edge
  structure through the hub), which is a correctness signal for the chain reading, not a new graph.
  The double-lens is the genuine new member (9 vertices, 15 edges, `chi = 4`).
* **Nothing here is evidence about the plane.** No 5-chromatic or 6-chromatic unit-distance graph was
  produced; the family is far too small and too structured.
* A **finite 6-chromatic unit-distance graph exists** — not from this search, but as a corollary of
  prior verified work: `OAI.EuclideanFiveColor.no_proper_five_coloring` (Lean 4.34.1, axioms
  `[propext, Classical.choice, Quot.sound]`) plus de Bruijn–Erdos compactness of finite
  colourability, with algebraic coordinates by T1 (`results/T1-algebraic-plane.md`). The open problem
  is *extraction* of a witness, and any explicit search is a search for that witness.
* For calibration: the smallest known 5-chromatic unit-distance graphs in the literature have hundreds
  of vertices (de Grey 1581, Heule 826, later records ~509). That is quoted from memory of the
  literature and was **not** verified in this block; it also means the `k=4` control ladder here is
  small, and a `k=5` positive control needs published coordinates plus exact re-validation.

## 6. Declared next search space (shards, each with an explicit cap)

Prepared for up to four subagents, disjoint paths under `supervisor/solve-graphs/shards/<name>/`,
each with exact validation and per-generation checkpoints:

* **A. Closure growth.** Start from the double-lens point set; each generation adds
  `U` of every pair with `d^2 in {1,3}`, canonicalises, stops at 60 points or 12 generations.
  Decide `k=6` (CNF, checkpoints per generation) and run the forced-pair census at `k=6`.
  Falsifier: any generation that is 6-UNSAT, or any pair forced at `k=6`, is a new object.
* **B. Literature positive control.** Reconstruct one published 5-chromatic unit-distance graph
  (Heule/Parts family) from its published description in `Q(sqrt3, sqrt11)`, validate every edge
  exactly, and certify 4-UNSAT with the same pipeline. Falsifier: failing exact validation means the
  published coordinates are float-only and must be re-derived symbolically.
* **C. Lattice-ball straight edge.** The exact unit-distance graph on `Z^2 cap [-12,12]^2` and on the
  triangular lattice ball of radius 8: certify 6-colourability with an explicit colouring and record
  the forced-pair census (expected: nothing forced). Cheap, gives a scale test of the pipeline.
* Out of scope: a complete enumeration of unit-distance graphs on `<= 8` vertices (needs a separate
  feasibility study, not a bounded search).

## 7. Reproduce

```
cd supervisor/solve-graphs
python3 pilot.py            # writes certs/pilot.json, certs/*.colouring.json, certs/table.md
```
Runtime ~8 s on this VM; no background jobs; peak memory < 200 MB.
