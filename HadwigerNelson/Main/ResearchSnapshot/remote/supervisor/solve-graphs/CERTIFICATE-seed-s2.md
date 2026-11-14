# Seed S2 = H ∪ R90(H): exact induced certificate, and why the seed FAILED its purpose

## The object (exact, all-pairs, no floating prefilter)
`R90(x,y) = (−y,x)` about the origin. `S2` = induced unit-distance graph on
`V(H) ∪ R90(V(H))`.

| quantity | value |
|---|---|
| points before dedup | 1106 |
| **distinct points** | **1105** |
| **overlap** | **1** (the origin, a vertex of `H`) |
| denominator lcm of all coordinates | **288** |
| pairs exact-checked (all pairs) | **609 960** |
| **induced edges** | **5444** |
| A-side / B-side / genuine cross | 2684 / 2684 / **0** |
| proper 5-colouring | **found and edge-checked (0 monochromatic)** |
| elapsed | **0.63 s** of the 60 s budget |

Method: coordinates scaled by 288 to `int64`, squared distance computed as an exact bilinear form
`d²(p,q)_m = G_m[i][i] + G_m[j][j] − 2G_m[i][j]` over all pairs at once, edge iff
`D[0] = 288²` and `D[m] = 0` for `m ≥ 1`. **Complete by construction** — there is no candidate filter
whose completeness needs proving, so the induced-edge certificate is genuine, not "reported".

Validation inside the same single job:
* all 5444 edges re-verified by the independent `udg.exact.Field` path — **0 failures**;
* the 2722 frozen `H`-edges reproduced **exactly** (0 missed, 0 extra edges inside `H`), which is what
  would expose an incorrect multiplication table;
* vertices distinct after exact dedup.

One bug was caught by that validation and fixed: the per-component conditions were OR'd instead of
AND'd, which initially claimed all 609 960 pairs as edges. The validation refused the result, which is
why it runs inside the job.

## The seed failed its purpose — stated plainly
**S2 is a clique-sum.** Its interface is the single point `(0,0)` (a clique of size 1) and there are
**zero** edges between the two sides' interiors. By **Theorem A**, `chi(S2) = max(chi H, chi H) = 5`,
which the verified 5-colouring confirms. So S2 adds no constraint of the kind sought, and by our own
theorem it cannot raise the chromatic number.

**Cause, and it is my design error:** `0 = (0,0)` is a vertex of `H` (line 1 of
`refs/heule_553.vtx`), so `R90` fixes it. Rotating about a *vertex* therefore yields an
overlap of exactly 1 point — a clique interface. To get a non-clique interface from a rotation the
centre must **not** be a vertex, e.g. about `(1/2, 0)` or a point at distance `√3/2` from a vertex.

## Correction of a count in the run record
The job first reported `new_edges = 38`, and a recount gave 76; **both are artifacts**. The origin has
provenance `A|B`, so every edge incident to it is misclassified as cross: 38 `H`-edges at the origin
plus their 38 `R90`-images give 76. Recounted among `A`-only to `B`-only pairs: **0**. Both figures are
kept in `certs/seed_s2.json` with the correction attached.

## What is and is not claimed
* **Claimed:** an exact induced-edge certificate for a 1105-vertex unit-distance graph (5444 edges,
  609 960 pairs decided exactly), with a verified proper 5-colouring, and `chi = 5` by Theorem A.
* **Not claimed:** any chromatic improvement, any forced-equal pair, any `chi(R²)` statement. No
  UNSAT was reached, so no proof obligation arose.
