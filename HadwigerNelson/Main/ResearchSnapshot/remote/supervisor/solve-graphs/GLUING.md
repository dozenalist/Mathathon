# Can gluing a unit-distance graph create a new constraint? (mechanism block)

Scope: this file is about **finite unit-distance point graphs** only. It says nothing about
`chi(R^2)` and asserts no bound on it. Inherited results are marked; new results are Theorems A–C.

Not inherited / not used here: the other worker's 73-cell **cell-conflict** 6-UNSAT graph is a
statement about tiling *cells*, valid for `a in (1/sqrt28, 1/sqrt19)`; it is a different object from
a unit-distance point graph and **its chromatic bound is not transferred**. The trace branch's
retracted inferences (false compactness, every-centre circle admissibility, global-range vs
pointwise palette) are **not** used; I only use their surviving reading that the palette is a
radius-one cluster trace, which is a Lean-source fact.

## 0. The operator, stated exactly

**Gluing.** Given unit-distance graphs `G1, G2` realised in the plane, a gluing is a choice of
points `K = V(G1) ∩ V(G2)` (shared vertices). Geometry then supplies **cross edges for free**: any
`u in V(G1)\K`, `v in V(G2)\K` with `|u-v| = 1` is an edge of the union whether or not the
construction intended it. This free-edge phenomenon is what makes unit-distance gluing different
from abstract gluing, and it is why Theorem A does not settle the question.

## Theorem A (clique interface cannot increase chi)

Let `G = G1 ∪ G2`, `V(G) = V1 ∪ V2`, `K = V1 ∩ V2`, and suppose

* `K` induces a **clique**, and
* there are **no edges between `V1\K` and `V2\K`** (the amalgam / clique-sum condition).

Then `chi(G) <= max(chi(G1), chi(G2))`.

*Proof.* Put `k = max(chi G1, chi G2)` and take proper `k`-colourings `phi1, phi2`. On the clique
`K` both are injective, so `|phi1(K)| = |phi2(K)| = |K|` and `tau(phi1(x)) := phi2(x)` is a
well-defined bijection; extend `tau` to a permutation `sigma` of `[k]`. Define `psi = phi1` on `V1`
and `psi = sigma^{-1} o phi2` on `V2`; on `K` these agree. Every edge lies inside `V1` or inside
`V2` by hypothesis, and `psi` is proper on each, so `psi` is a proper `k`-colouring of `G`. ∎

**Consequence (explains block 1).** Every specimen in my block-1 family — the Moser spindle, the
double-lens, the spindle chain, the diamond decorations — is an amalgam of diamonds/spindles over
clique interfaces (a single point, a unit edge, or a unit triangle). By Theorem A none of them can
exceed the maximum of its pieces. The block-1 observation "nothing is forced at `k >= 4`" is
therefore a consequence of Theorem A, not a small-search artifact. **`chi = 3` (diamond),
`chi = 4` (spindle, double-lens).**

## Theorem B (palette-exclusion forcing dies at k = 4)

**Definition.** Let `G` be a unit-distance graph with non-adjacent marks `p, q`. A set
`S ⊆ V(G)\{p,q}` is a **palette excluder** for `(p,q)` if `S` is a clique and every `s in S` is
adjacent to both `p` and `q`. Then in every proper `k`-colouring `c(p), c(q) ∉ c(S)`, so
`{c(p),c(q)} ⊆ [k] \ c(S)`, a set of size `k - |S|`.

**Theorem B.** In a unit-distance graph every palette excluder has `|S| <= 2`. Consequently the
palette of a non-adjacent pair has size at least `k - 2`, and **palette exclusion can force
`c(p) = c(q)` only when `k <= 3`.**

*Proof.* Every `s in S` satisfies `|s-p| = |s-q| = 1`, so `S` lies in `N(p) ∩ N(q)`, the
intersection of the two unit circles about `p` and `q`. Two distinct circles meet in at most two
points (two circles about distinct centres are distinct), so `|S| <= 2`. Then `|[k]\c(S)| >= k-2`,
which equals `1` only if `k <= 3`. ∎

**Sharpness.** `k = 3` is attained: the diamond has `|S| = 2` and forces its tips equal — exact
counts 6 vs 0 at `k=3` (block 1). So Theorem B is tight and cannot be improved by a better
choice of clique.

Note this is a statement about the **mechanism**, not about all unit-distance graphs: it says the
direct palette operator is capped, and it does **not** say no unit-distance graph forces equality at
`k >= 4`.

## Theorem C (the diamond is the unique 2-clique excluder; verified at scale)

For a non-adjacent pair `p,q` with exactly two common neighbours `c1, c2`, the segment `c1c2` is
perpendicular-bisected by `pq`, so `|c1c2|^2 = 4 - |pq|^2`. Hence `c1c2` is a **unit edge if and only
if `|pq|^2 = 3`**, i.e. only in the diamond.

*Exact check* (`check_geometry.py`, `Q(sqrt3,sqrt5,sqrt11)`, no floats): for the unit triangle
`(0,0),(1,0),(1/2,sqrt3/2)` the only two points at distance 1 from both of the first two vertices are
`c` itself (distance 0 from `c`) and its reflection (distance `sqrt3` from `c`). So **a unit triangle
has no common unit neighbour at all** — a fortiori no excluder of a triangle. Combined with Theorem B:
the plane offers no way to exclude three colours from a pair, which is what a forcing at `k = 4`
would need.

*One benchmark* — the registered computation, on the **real, validated** 553-vertex 5-chromatic
graph (see `PREREGISTRATION-census.md`). This is evidence that Theorem C holds on that object; it is
not a survey and not a minimality statement. All three predictions held:

| prediction | result |
|---|---|
| P1 `omega <= 3` | `0` K4 witnesses, `1093` triangles, max clique `3` ✓ |
| P2 every non-adjacent pair has `<= 2` common neighbours | max `2` over `149906` pairs; histogram `{0:132261, 1:9744, 2:7901}` ✓ |
| P3 two common neighbours ⟺ `|pq|^2 = 3`, and then they are a unit edge | `7901` pairs, **0** failures ✓ |

Run: `python3 census.py` (1.24 s). One implementation bug found and fixed: my first P1 test counted
*triangles* as `K_4` and reported 102 "witnesses"; that was a coding error (P1 is a plane fact —
four pairwise equidistant points do not exist), corrected in `fix_p1.py` and recorded in
`certs/census_heule553.json` under `P1_note`. P2/P3 were unaffected and were not recomputed.

## The candidate construction: non-clique gluing at a sqrt3 pair

Since Theorem A only kills clique interfaces, the smallest legal escalation is a **non-clique**
interface. The one I register as the branch's candidate:

* **Pieces.** Two copies `D, D'` of the double-lens (9 vertices, 15 edges, `chi = 4`, all edges
  exactly unit, block 1).
* **Anchor interface.** The two vertices of a **sqrt3 pair** `p, q` (`|p-q|^2 = 3`), shared between
  the copies. `p,q` are non-adjacent, so the interface is *not* a clique: Theorem A does not apply.
* **Field.** `Q(sqrt3, sqrt11)`, 4 basis elements. All coordinates exact (block-1 field; no new
  arithmetic needed).
* **Cross-edge rule (all of them).** After placing `D'` by an isometry of the plane, the cross edges
  are **exactly** `{uv : u in V(D)\{p,q}, v in V(D')\{p,q}, |u-v| = 1}`, computed by exact field
  identity `d^2 = 1`; there are no other rules. Because geometry supplies them for free, the union
  generally has *more* edges than the abstract amalgam, and this is the only channel by which the
  chromatic bound could rise.
* **Why it is not merely a clique-sum.** `V(D) ∩ V(D') = {p,q}` with `pq` **not** an edge, so the
  hypothesis of Theorem A fails, and there are cross edges. Both copies independently constrain the
  same non-clique pair, so the colouring question is a genuine list-intersection problem, not a
  relabelling.

**Scope note on "not realisable".** `pq` is not a unit edge in this embedding, so adding it is not a
unit-distance constraint. It is **not** true that the constraint `c(p) != c(q)` is unrealisable by
geometry: extra vertices at exact unit distance from `p` and `q` can in principle shrink the two
palettes until they are disjoint, exactly as the diamond forces an equality at `k = 3` with no
non-unit edge. Whether such a forcing set exists is open.

**Why I do not run it, and the limitation proved instead.** By Theorem B each copy gives
`{c(p),c(q)} ⊆` a set of size `k-2` (`k=4`), i.e. exactly the palette cap; intersecting two such
2-sets has no forced outcome, and at 16 vertices the object is far below the scale at which
`chi = 5` first appears (the smallest published 5-chromatic unit-distance graphs have 553–1581
vertices, per Heule/de Grey; the 553 case I validated above). So the predicted outcome is
`4`-colourable and therefore **uninformative**. Running it would be a variant of block 1 with a
different glue, which is exactly what this block was told not to do.

## The precise missing interface

> **GADGET_k.** A unit-distance graph `G` with marks `p, q` at distance `d != 1` such that
> `G` is `k`-colourable and `G + pq` is **not**, while `k - |N(p) ∩ N(q)| >= 2`.

By Theorem B the second clause is automatic in the plane, so GADGET_k is exactly "a forced-equality
pair that does **not** arise from excluding a common neighbourhood". I have not constructed such a
gadget for any `k >= 4`, and Theorems A and B show that the two operators analysed here cannot
produce one. That is a statement about these operators, **not** a claim that no such gadget exists:
I ran no literature audit and I have no exhaustive classification of the routes by which a forced
equality could arise.

**One named escape route, not a classification.** The colour of `p` could be pinned by neighbours
whose own colours are pinned by *their* neighbours, so that the constraint arrives from graph
distance >= 2. I call this a *cascade*. Whether every escape from Theorem B is of this shape is an
open question I am not able to settle here.

## Corrections to the previous version of this file

Four claims in the previous block were under-supported and are withdrawn or weakened. They are
listed here rather than silently edited.

1. **Withdrawn: the 553-vertex census as a "scale verification" of Theorem C.** It is one benchmark,
   not a minimality or universality theorem. It shows Theorem C holds on one real 5-chromatic graph;
   it says nothing about whether other gadgets or other graphs exist. The correct grade for that
   computation is [A] for the arithmetic on that object, and nothing more.
2. **Withdrawn: "No GADGET_k is known for k = 4, 5 or 6" as a literature claim.** I performed no
   literature audit, so I cannot assert what is or is not known. What is supported: *I have not
   constructed one, and the two operators analysed here provably cannot produce one for k >= 4.*
3. **Withdrawn: "the only escape from Theorem B is a cascade".** A cascade of length >= 2 is **one**
   named escape route from the palette cap; it is not an exhaustive classification of the ways a
   forced equality could arise, and I have no argument that exhausts them. Theorem B constrains the
   direct common-neighbour mechanism only.
4. **Retained:** Theorem A, Theorem B, Theorem C, the sharpness of B at k = 3, and the corrected
   non-adjacent-pair count **149906** for this graph.

## Honest status

* New and proved here: Theorems A, B, C, with C's three predictions exactly verified on one real
  5-chromatic graph (one benchmark; not a minimality theorem).
* Inherited, kept separate: the 553-vertex 4-UNSAT control (block 2, DRAT-verified), the block-1
  counts and the `iff k=3` diamond proposition.
* **Not established:** any 6-chromatic unit-distance graph, any bound `chi(R^2) >= 6` or `>= 7`.
  No assertion of `chi >= 7` is made or implied.
* The census is one benchmark. It does not show that no other gadget exists, and the escape-route
  discussion names one route without claiming it is the only one.
* See `EXPERIMENT-disequality.md` for the one bounded point-graph experiment of the current block.
