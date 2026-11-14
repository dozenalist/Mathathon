# Correction: my restriction-map implication was stated backwards

## What REFINE-PREREG.md section 2 says
> "Every proper 5-colouring of `G_rep` restricts along `iota : V(H) -> V(G_rep)` to a proper
> 5-colouring of `H`. Hence for a pair `{p,q} ⊆ iota(V(H))`: **non-forced in `H` implies non-forced
> in `G_rep`**."

**That implication is wrong and is retracted.** The restriction map does not give it.

## Why it is wrong
Restriction gives an inclusion the other way round: `Col(G_rep)|_H ⊆ Col(H)`, i.e. the colourings of
the *subgraph* form the superset. A separating `H`-colouring `phi` with `phi(p) != phi(q)` need not
extend to `G_rep`, so it certifies nothing about `G_rep`. Confusing these is reading a subset relation
backwards.

## The correct statement
> **Fact.** `H` is an induced subgraph of `G_rep`. Hence `Col(G_rep)|_H ⊆ Col(H)`. Therefore for a
> pair `{p,q} ⊆ iota(V(H))`: **forced in `H` implies forced in `G_rep`** — the property "`c(p) = c(q)`"
> holds for every member of `Col(H)`, hence for every restriction of a `G_rep`-colouring.
> Equivalently: **non-forced in `G_rep` implies non-forced in `H`.**

So forcedness does only increase when passing from an induced subgraph to the supergraph, and the
restriction map is the reason — but the direction matters, and mine was inverted.

## Consequence for this block's numbers
`H` has **no** forced pair at `k = 5`, and by the correct implication that says nothing about
`G_rep`: transferring a *negative* result needs the opposite map. So the **112 survivors whose two
endpoints are both A-only are NOT eliminated** by the `H`-certificate. The survivor count stays
**1145**, and all 1145 remain untested candidates.

## What this does not change
The refinement run is unaffected: it used only witnesses of `G_rep` and only the reported edge list,
so its eliminations stand. Only the prose inference was wrong — and it was wrong in the direction that
would have *overstated* progress, by justifying the silent discarding of 112 candidates. Recorded, not
deleted.
