# The equality-to-chromatic amplifier: from a forced-equal pair to a `(k+1)`-chromatic finite unit-distance graph

Analysis only, no computation. Grade: **[P]** exact derivation written out below; **[C]** cited from the
record; **[X]** not established. **No forcing pair is asserted to exist**; everything is conditional on
the hypotheses (H1), (H2), (H4). The construction's validity is *checked* by deriving the Moser spindle
from it (k = 3), with its known 7 vertices, 11 edges and field `Q(√3, √11)`.

## 0. The question, and the answer in one paragraph

Given a finite `k`-colourable unit-distance point graph `G` with distinct non-adjacent points `p, q`
forced to carry the same colour in **every** proper `k`-colouring, and `d = |p − q| > 0`: yes, there is
a constructive amplifier. Translate `n` copies of `G` along `u = (q−p)/d`, identifying `q` of one copy
with `p` of the next: the whole chain is monochromatic in every `k`-colouring, so its two ends are an
equal-coloured pair at distance `D = n·d`, and any `D > 1/2` is available by taking `n` large enough.
Then take two copies of that chain sharing one end and rotated by `θ` with `2D sin(θ/2) = 1`; the two
far ends are equal-coloured and exactly 1 apart. So the union is not `k`-colourable. It is
`(k+1)`-colourable under one further, checkable hypothesis (H4), which makes it `(k+1)`-chromatic. All
coordinates lie in a number field that is at most a quadratic extension of the gadget's field, so every
distance can be certified exactly.

## 1. Hypotheses, stated once

* **(H1)** `G = (P, E)` is a finite **unit-distance point graph**: `P ⊂ ℝ²`, `|P| = V`, and
  `E = {{x,y} : |x−y| = 1}` (we take the full induced unit-distance graph). `G` is `k`-colourable.
* **(H2)** `p, q ∈ P`, `p ≠ q`, and **every** proper `k`-colouring `c` of `G` has `c(p) = c(q)`.
  *Note:* non-adjacency is automatic — if `|p−q| = 1` then `p,q ∈ E` and (H2) would contradict (H1).
* **(H4)** (needed only for the *upper* bound) for every pair of colours `(a,b) ∈ [k+1]²`, `G` has a
  proper `(k+1)`-colouring with `c(p) = a` and `c(q) = b`.
* `d = |p − q| > 0`, `u = (q − p)/d`.

## 2. Step 1 — the chain, and the distance `D ≥ 1/2`

Set `P_i = P + i d u` for `i = 0, …, n−1`, and identify `q + i d u` with `p + (i+1) d u` (they are the
same point, since `q = p + d u`). The chain `C_n = ⋃_i P_i` has

    |C_n| = nV − (n−1)      points,      nE      unit edges (translations preserve every distance),

and its two end points are `p` and `p + n d u`, at distance `D = n d`.

**Lemma 1 [P].** In every proper `k`-colouring of `C_n`, all points of the chain have the same colour
`α`, and in particular the two ends do. *Proof.* The `i`-th copy `P + i d u` is an isometry of `P`, so
the restriction of `c` to it is a proper `k`-colouring of `G`; by (H2) `c(p + i d u) = c(q + i d u)`.
Since `q + i d u = p + (i+1) d u`, induction gives `c(p) = c(p + d u) = … = c(p + n d u)`. `square`

So for every `n ≥ 1` we get an equal-coloured pair at distance `n d`, and choosing

    n* = min{ n : n d > 1/2 }

gives `D = n* d > 1/2`. **Strictness matters**: at `n d = 1/2` the required angle below is `θ = π`, the
two rotated copies are antipodal and the construction degenerates (the point set becomes symmetric about
the shared end, with coincidences). The condition `D > 1/2` is exactly the solvability condition
`2D ≥ 1` for a chord of length `1` on a circle of radius `D`, made strict to keep `0 < θ < π`.

## 3. Step 2 — the two rotated copies, and the unit edge

Put `p = 0` by translation (harmless: the construction is invariant under translation). Let `R_θ` be
the rotation about `0` by `θ` with

    cos θ = 1 − 1/(2D²),        sin θ = √(4D² − 1)/(2D²).

Then `|D u − D R_θ u| = D·2 sin(θ/2)` and `sin(θ/2) = √((1 − cos θ)/2) = 1/(2D)`, so

    |D u − D R_θ u| = 1        exactly.

Define `X = C_n ∪ R_θ C_n`, both containing the shared point `0`. Its ends are `D u` and `D R_θ u`.

    |X| ≤ 2|C_n| − 1 = 2nV − 2n + 1,        |E(X)| ≤ 2nE + 1

(the `−1` is the shared point; the `+1` is the final unit edge; equality holds iff there are no
accidental coincidences or accidental unit distances — see §5).

## 4. Non-`k`-colourability, and `(k+1)`-chromaticity

**Theorem [P].** Under (H1), (H2): `X` is **not** `k`-colourable. Under (H1), (H2), (H4) with
`k + 1 ≥ 3`: `χ(X) = k + 1`.

*Proof.* Suppose `c` is a proper `k`-colouring of `X`. On each chain Lemma 1 makes `c` equal `α` on all
its points, so both ends `D u` and `D R_θ u` have colour `α`; but they are at distance `1`, which a
proper colouring forbids. For the second part: by (H4) with `a = b = α`, each copy of `G` in the chain
admits a proper `(k+1)`-colouring with both `p` and `q` coloured `α`; gluing copies along the shared
points (which all receive `α`) gives a proper `(k+1)`-colouring of `C_n` with both ends `α`. Colour
`R_θ C_n` by the same rule *except* that the copy containing the far end is coloured with (H4) at
`(α, β)` for a colour `β ≠ α` distinct from the first chain's end colour; taking `β' ≠ β` on the two
chains makes the final unit edge proper, which needs `k + 1 ≥ 3`. `square`

**What the amplifier converts.** (H1)+(H2) give *not `k`-colourable*; only (H4) upgrades that to
`χ = k+1`. (H4) is a real obligation: it says the gadget's forced equality can be *broken* once one
more colour is available, which is automatic for the diamond but must be checked per gadget.

**Consequence worth recording [P].** At `k = 6`: a forced-equal pair in a 6-colourable finite
unit-distance graph would produce a finite unit-distance graph that is not 6-colourable, hence of
chromatic number `≥ 7`, hence — by passing to a vertex-minimal subgraph of chromatic number `≥ 7` — one
with chromatic number exactly 7. Contrapositive: if `χ(ℝ²) ≤ 6` then **no** 6-colourable finite
unit-distance graph has such a forcing pair. So an equality certificate at `k = 6` is a *sufficient*
route to `χ(ℝ²) = 7`, and a negative answer to the forcing-pair question is exactly as hard as
`χ(ℝ²) ≤ 6`. **No such pair is claimed to exist here.**

## 5. Coincidences, accidental unit edges, and why the angle is not free

The angle `θ` is **forced** by the unit-edge requirement, so there is no generic-placement escape at
this step. Three classes of accident must be handled by exact enumeration, not by a genericity claim:

1. **Coincidences inside the chain.** If `x − y = m d u` for some `x, y ∈ P` and integer `m ≠ 0`, then
   copies overlap in more than the intended point and `|C_n| < nV − (n−1)`. This only *adds*
   constraints (never weakens the lower bound) but it changes the vertex count and can break (H4)'s
   gluing, so it must be checked.
2. **Coincidences between the two chains.** A point of `C_n` can coincide with a point of `R_θ C_n`
   only if two distances and the angle conspire; each such equation is algebraic in `cos θ, sin θ` and
   hence decidable exactly. Identifications only strengthen the lower bound; if the identified points
   are forced to different colours under (H2), the graph is not `k`-colourable *a fortiori*.
3. **Accidental unit distances between the two chains.** Every other cross-distance is
   `|x − R_θ y|`, a continuous function of `θ`; with `θ` fixed, each is decidable exactly. Accidental
   unit edges help the lower bound and can only hurt (H4)/(k+1)-colourability, so the (k+1)-colouring
   must be verified for the actual point set, not an idealised one.

The freedom that remains is combinatorial: `n` (hence `D`, hence `θ`), the sign of `sin θ` (mirror
image), and which end of each chain is shared. Accidents can sometimes be removed by changing `n`.

## 6. Exact field requirements

Let `P ⊂ K²` for a number field `K ⊂ ℝ` of finite degree over `ℚ` (for the record's gadgets,
`K = ℚ(√3, √11)`), and suppose `d ∈ K` and `u = (q−p)/d ∈ K²`. Then every chain point lies in `K²`.
By §3,

    cos θ = 1 − 1/(2n²d²) ∈ K,        sin θ = √(4n²d² − 1)/(2n²d²),

so the rotation lives in `K' = K(√(4n²d² − 1))`, a field extension of degree at most 2. **Every**
coordinate of `X` lies in `K'²`, hence every squared distance is an element of `K'`, and each test
"distance `= 1`" (and each coincidence test) is an exact comparison in `K'`. If `d ∉ K`, adjoin `√(d²)`
first: one further quadratic extension, still finite and exact. No floating point is required at any
stage.

## 7. Validation: the construction at `k = 3` is the Moser spindle

Take for `G` the **diamond**: `P = {(0,0), (1,0), (1/2, √3/2), (3/2, √3/2)}` — two equilateral
triangles sharing an edge — `p = (0,0)`, `q = (3/2, √3/2)`, so `d = √3`.

* (H1) `k = 3`: the diamond is 3-colourable [P] (`V = 4`, `E = 5`).
* (H2): in every proper 3-colouring the two base vertices differ, so each tip must take the third
  colour; hence `c(p) = c(q)` [P]. `p, q` are at distance `√3 ≠ 1`, non-adjacent ✓.
* `n* = min{n : n√3 > 1/2} = 1`, so `D = √3 > 1/2` ✓ — no chaining needed.
* `cos θ = 1 − 1/6 = 5/6`, `sin θ = √11/6`, so `K' = ℚ(√3)(√(4·3−1)) = ℚ(√3, √11)` — **the field the
  project already uses for its exact Moser certificate** [C].
* Counts: `|X| = 2·4 − 1 = 7` and `|E(X)| = 2·5 + 1 = 11` — the **7 vertices and 11 edges of the Moser
  spindle** [P]. The record's exact certificate states that all eleven edges have squared length exactly
  1, i.e. no accident occurs and (H4) holds with 4 colours [C].

So the amplifier's arithmetic reproduces the classical object exactly: the spindle *is* this
construction at `k = 3`, `n = 1`. That is the strongest available check of the formulas in §2-§3 and of
the vertex/edge bound in §6.

## 8. What a user of this must supply, and what is not claimed

To turn an equality certificate into a `(k+1)`-chromatic finite unit-distance graph, one must supply:
(i) the gadget with exact coordinates in a number field and a proof that it is `k`-colourable;
(ii) a proof of (H2) — that *every* proper `k`-colouring equalises `p, q` (this is the hard, non-local
part: it is a statement about all colourings, not about one);
(iii) a check of (H4) at `k+1` colours;
(iv) the exact distance verification of §5-§6 for the actual `θ` and `n`.
Not claimed: that any such pair exists at `k = 6`; that the amplifier is reversible (a 7-chromatic
graph does not give a forcing pair); that any of this bears on `χ(ℝ²)` unless (i)-(iv) are discharged.
