# Exact certificate: chi(H ∪ (H + τ)) = 5

## Object
`H` = the frozen Heule 553-point set (`refs/heule_553.vtx`, `refs/heule_553.edge`, unmodified,
sha256 `7e43a025…` / `b339b6a7…`). `τ = (3/2, √3/2)`, exact in
`Q(√3, √5, √11)` with basis `{1,3,5,11,15,33,55,165}`; verified `|τ|² = 3` exactly.

`U` = the induced unit-distance graph on `V(H) ∪ (V(H) + τ)`, deduplicated by exact field equality.

## Counts (all exact)
| quantity | value |
|---|---|
| points before dedup | 1106 |
| **points after exact dedup** | **1048** |
| **overlap** `V(H) ∩ (V(H)+τ)` | **58** (A-only 495, B-only 495, shared 58) |
| edges (A-internal / B-internal / new) | 2722 / 2722 / **184** |
| **total edges** | **5487** |
| overlap is a clique? | **No** |
| Theorem A (clique-sum) applies? | **No** — 184 new cross edges *and* non-clique overlap |

The 58-point overlap means `τ` is close to a symmetry of this point set; that is why the union is
not a disjoint pile and why 184 new unit edges appear.

## The two halves of `chi = 5`
* **`chi >= 5`.** `H` is an induced subgraph of `U`: the A-copy edges number exactly 2722 `= |E(H)|`,
  with no extra A-internal edges. `H` is not 4-colourable — certified independently by
  `certs/heule553_k4.drat`, verified by `drat-trim` (`s VERIFIED`). Hence `U` is not 4-colourable.
* **`chi <= 5`.** An explicit proper 5-colouring of `U` is stored in `certs/union_tau.json`
  (`witness`) and in `certs/union_tau_witness.txt`. Re-checked independently: **0 monochromatic edges
  of 5487**, and its restriction to `H` has 0 monochromatic edges of 2722.

So `chi(U) = 5`, verified, **not a candidate**.

## Exactness and prefilter completeness
Every edge decision is an exact field identity: all 5487 edges re-verified exactly, **0 failures**.
Floats were used only to nominate candidates, in a band `|d²−1| < 10⁻⁶`. Soundness evidence:
* the maximum float error over the 2722 known unit edges is **7.77 × 10⁻¹⁶**, ten orders of magnitude
  inside the band;
* all 2722 known `H`-edges are recovered by the prefilter (**0 missed**);
* of the rejected candidates, the 400 *closest to distance 1* were re-checked exactly and **none** is
  a unit pair; the smallest `|d²−1|` among rejected candidates is **8.9 × 10⁻⁵**, i.e. 89× the band,
  so there is no borderline region.

## Check it
```
cd supervisor/solve-graphs
python3 verify_union.py      # no solver; prints VERIFIED: True
```

## What this is and is not
* It **is** an exactly validated, non-clique-sum unit-distance graph with `chi = 5`, and therefore a
  legitimate seed for a `k = 5` forced-equality search: adding the B-copy vertices adds constraints,
  so a pair could in principle be forced equal here even though `H` has none.
* It **is not** a new lower bound: `chi = 5` was already known. It is a structural object.
* **No forced-pair search was run** (excluded this block). Nothing here asserts or denies that any
  pair of `U` is forced equal at `k = 5`.
* No claim about `chi(R²)`.
