# Finite certificate: this 553-vertex graph has no forced-equal non-adjacent pair at any k >= 5

## Statement
Let `G` be the unit-distance graph on Heule's 553 published points
(`refs/heule_553.vtx`, `refs/heule_553.edge`, both unmodified third-party files), with exact
coordinates in `Q(sqrt3, sqrt5, sqrt11)`, 553 vertices, 2722 edges, **149906** non-adjacent pairs.
Then:

> For **every** non-adjacent pair `{i,j}` there is a **proper 5-colouring** `c` of `G` with
> `c(i) != c(j)`.

Consequently **no non-adjacent pair of `G` is forced equal at `k = 5`**, and, because a proper
5-colouring is also a proper `k`-colouring for every `k >= 5` (it uses colours `0..4` inside
`0..k-1`), **no non-adjacent pair of `G` is forced equal at any `k >= 5`.**

This is a statement about **this graph only**. It says nothing about `chi(R^2)`, nothing about other
unit-distance graphs, and nothing about forced *inequalities*.

## The certificate
34 proper 5-colourings, stored in `certs/adaptive_k5.json` under `witnesses`. Every one was checked
against all 2722 edges and has **zero** monochromatic edges. For each of the 149906 non-adjacent
pairs, at least one of the 34 witnesses separates it. The certificate is therefore finite and
explicit: no search is needed to check it, only the 34 vectors plus the edge list.

## Proof of the statement from the certificate
`S := intersection over all 34 witnesses of {pairs given equal colours}` was recomputed from scratch
and is **empty**. A pair is in that intersection exactly when every witness colours it equally; since
every witness is a proper colouring, a pair in the intersection can never be an edge, so the
(empty) intersection consists of non-adjacent pairs only. Hence every non-adjacent pair is separated
by some witness, which is a proper 5-colouring. ∎

For `k > 5`, the same witness is a proper `k`-colouring, so the same separation applies. ∎

## How it was obtained (adaptive class-refinement chase, `PREREGISTRATION-adaptive.md`)
Baseline of 18 saved witnesses gave `|S| = 491`. Those 491 pairs are exactly the within-class pairs of
**24 colour-signature classes** (vertices with identical colour vectors across the witnesses), with
sizes 19, 17, 14, 9, 6, 5, 4, 4, 3, 3 and fourteen of size 2 — reproducing the reported structure
exactly, which is an independent check of the baseline. Selection was **adaptive**, recomputed at
every step (largest surviving class, then least-used endpoints, then smallest indices), never a
frozen list. Each step required its witness to split its target pair by the combinatorial
**disequality** edge `c(p) != c(q)`; since every survivor satisfies `|p-q| != 1`, that edge is never a
unit edge and **no coordinate was changed**.

Elimination trajectory (survivors after each of 16 steps):
`491, 380, 360, 298, 164, 138, 99, 44, 33, 29, 18, 14, 6, 4, 2, 1, 0`.
Total wall time **0.23 s** for the whole run (generation, all 16 solver calls, all edge checks).

## Verify
```
cd supervisor/solve-graphs
python3 verify_certificate.py     # reads refs/heule_553.edge directly, no solver
```
It re-checks all 34 witnesses, recomputes the intersection, and independently loops over all
non-adjacent pairs confirming each has a separating witness. Last run:
`witnesses 34; all proper (0 monochromatic of 2722); survivors 0; non-adjacent pairs with no
separating witness: 0 (of 149906); CERTIFICATE HOLDS: True`.

## What this rules out, and what it does not
* **Ruled out:** this point set as a source of a forced-equal distinct pair at `k >= 5`. The geometry
  branch's finite amplifier needs a genuine forced-equal distinct pair, so **this graph cannot
  supply one at `k >= 5`** and a different seed is needed.
* **Not ruled out:** forced equalities in other graphs; forced inequalities (the orientation used by
  the earlier probes); anything at `k = 4` (a different question, not computed here); any statement
  about `chi(R^2)`.
* The disequality edges used to drive the chase are **combinatorial test constraints**, not unit
  edges, and they appear only inside the solver calls — never in the graph.
