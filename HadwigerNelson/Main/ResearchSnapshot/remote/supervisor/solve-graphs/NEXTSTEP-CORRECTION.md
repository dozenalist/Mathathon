# Correction: the proposed k = 4 test on Heule553 is vacuous and is withdrawn

## What I proposed last block
"Run the same pre-registered pipeline at `k = 4` on this point set. Forced equalities are far more
plentiful at lower `k` (the diamond already forces one at `k = 3`), so the `k = 4` survivor set
should be nonempty..." — with the implication that a residue would be a candidate forced-equal pair.

## Why it is wrong
The definition of a forced-equal pair at `k` is:

> `G` is **`k`-colourable**, and `G + pq` is not.

The `k`-colourability hypothesis (H1) is not decoration. The 553-vertex graph is **5-chromatic**: its
4-UNSAT is certified (my own DRAT certificate, `certs/heule553_k4.drat`, verified by `drat-trim`).
So at `k = 4` clause (H1) **fails**. Running the pipeline at `k = 4` would return UNSAT for every
candidate pair, and the "survivor set" would be *all* non-adjacent pairs — the whole notion collapses.
Every equality claim extracted from it would be **vacuous**: it would report "forced" for pairs that
are forced only because no 4-colouring exists at all.

I had the monotonicity the wrong way round. Forced-ness is monotone **downward** in the sense that
the `k`-colourings are a subset of the `(k+1)`-colourings, so a `k`-forced pair stays forced at
`k+1`; but **the (H1) hypothesis runs the other way**, so lowering `k` below `chi(G)` destroys the
question instead of enriching it. The correct reading of my own certificate's corollary is therefore:
the corollary covers `k >= 5` because that is exactly the range where (H1) holds, and it says nothing
at `k = 4` — not because the question is open there, but because it is **not posed** there.

## What replaces it
A genuine `k = 4` forced-equality question needs a graph that is **4-colourable**. That is a
*different seed graph*, not a different threshold on this one. This is the missing interface
`GADGET_4`: a 4-colourable unit-distance graph with a pair `p, q` at distance `!= 1` such that
`G + pq` is not 4-colourable. See `SEED-S1.md`.

## Retained
The 34-witness certificate at `k >= 5` on this graph stands, independently re-verified. What it does
**not** do: it does not show that the *method* is exhausted, does not bound the technique (the
technique reduced an open 491-pair question to a 34-witness proof in 0.23 s and transfers to any
graph), and does not bear on other graphs or on `k = 4` questions posed for 4-colourable graphs.
