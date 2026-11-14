# The equality-to-chromatic amplifier: a rigorous LOWER-BOUND theorem

Replaces the previous version of this file. Analysis only, no computation. Grades: **[P]** exact
derivation below; **[C]** cited from the record; **[X]** not established. **No forcing pair exists in the
project's evidence**, and nothing here asserts one does.

## 0. Corrections to the previous version (kept visible)

| # | what I wrote | what is right |
|---|---|---|
| A1 | "in every proper `k`-colouring all points of the chain have the same colour" | **Only the distinguished chain vertices `p + j(q−p)`, `j = 0,…,n`, are forced equal.** Inside one copy, (H2) equalises only `p` and `q`. The copy's other `V − 2` points are **not constrained by (H2)** — in general they need not differ in colour from the anchors either (they may be at distance `≠ 1` from both). The monochromatic set is the `n+1` distinguished vertices, nothing more. |
| A2 | chain "`|C_n| = nV − (n−1)`" | **`|C_n| ≤ nV − (n−1)`**: extra overlaps between non-consecutive copies are possible and only reduce the count. |
| A3 | "`|E(X)| ≤ 2nE + 1`" | **False for the induced unit-distance graph**: accidental unit distances between the two chains (and between far-apart copies) add edges. Correct statement: the **selected generating edges** form a multiset of `2nE + 1` entries (the `nE` images in each chain plus the final unit edge); their **distinct** number is at most that, and the induced edge set is a superset. No upper bound on `|E(X)|` is claimed. |
| A4 | "`D > 1/2` strictly; `D = 1/2` degenerates" | **`D = 1/2` is allowed.** At `D = 1/2` the angle is `θ = π`; the two far ends are `n v` and `−n v`, which are **distinct** (`|nv| = D = 1/2 ≠ 0`) and exactly `1` apart (`2D = 1`). Overlaps between the chains do not affect the argument, because each copy is restricted to separately. Condition: `D ≥ 1/2`. |
| A5 | "`(H4)` upgrades the union to `χ = k+1`" | **Withdrawn.** (H4) is a statement about `G`; it says nothing about the extra constraints created by overlaps and accidental unit edges in the union, so it cannot certify that the *induced* union is `(k+1)`-colourable. The upper bound needs per-instance verification, which is not supplied. What is free (A6) is existence of an exactly `(k+1)`-chromatic *subset*. |
| A6 | "`χ(X) = k+1`" as a theorem | Replaced by: `X` is not `k`-colourable, and by **vertex-minimality** `X` contains a finite point subset whose induced unit-distance graph has chromatic number **exactly** `k+1`. No extra hypothesis. |
| A7 | "adjoin `d = ‖v‖` first; field `K(√(4n²d²−1))`" | **Unnecessary.** Use the displacement `v = q − p` directly: the chain translations `jv` lie in `K²`, and the rotation coefficients depend only on `D² = n²‖v‖² ∈ K`. No square root of `‖v‖²` is ever needed. |
| A8 | "absence of forcing pairs is exactly as hard as `χ(ℝ²) ≤ 6`"; "the amplifier is not reversible" | **Both removed.** Only the one-way implication is proved. No hardness or reversibility claim is supported. |

## 1. Hypotheses and notation

* **(H1)** `G` is a finite **unit-distance point graph**: `P ⊂ K²` with `|P| = V`, `K ⊂ ℝ` a number
  field of finite degree over `ℚ`, and the edge set is *all* pairs of `P` at distance exactly `1`.
  `G` is properly `k`-colourable. (`k ≥ 3` in every interesting case; the Theorem below needs only that
  (H1) and (H2) be consistent.)
* **(H2)** `p, q ∈ P`, `p ≠ q`, and **every** proper `k`-colouring `c` of `G` has `c(p) = c(q)`.
* `v = q − p ≠ 0`, `V_e = |E(G)| = E` (generating edges), `‖v‖² ∈ K` (coordinates in `K`).
* Translate so that `p = 0` (all statements are translation-invariant).

Non-adjacency of `p, q` is automatic: if `‖v‖ = 1` then `pq ∈ E` and (H2) contradicts (H1).

## 2. The construction

Fix `n ≥ 1` with `D := n‖v‖ ≥ 1/2` — i.e. `4n²‖v‖² ≥ 1`, an **exact** condition in `K`, no square
root needed. (An `n` always exists with `4n²‖v‖² ≥ 1`; if `4‖v‖² ≥ 1` then `n = 1` already works.)

**Chain.** `C_n = ⋃_{j=0}^{n−1} (P + j v)`. Consecutive copies satisfy `q + jv = p + (j+1)v`, so they
share that point; the chain's ends are `p = 0` and `nv`.

**Rotation.** Let `θ` be defined by

    cos θ = 1 − 1/(2D²) = 1 − 1/(2n²‖v‖²)  ∈ K,        sin θ = √(4D² − 1)/(2D²),

which is real because `D ≥ 1/2`. Then, using `sin(θ/2) = 1/(2D)`,

    |n v − R_θ(n v)| = ‖nv‖ · |u − R_θ u| = D · 2 sin(θ/2) = 1        exactly.

**The point set.** `X_n = C_n ∪ R_θ C_n`, the two chains sharing the point `p = 0`.

## 3. Theorem (lower bound) [P]

**Theorem.** Under (H1) and (H2), the induced unit-distance graph on `X_n` is **not** `k`-colourable.

*Proof.* Let `c` be a proper `k`-colouring of the induced unit-distance graph on `X_n`. For each
`j ∈ {0,…,n−1}` the image `P + jv` is an isometric copy of `P`; because `G` is the *full* induced
unit-distance graph on `P`, the induced unit-distance graph on `P + jv` is isomorphic to `G`. The
restriction of `c` to `P + jv` is therefore a proper `k`-colouring of (a copy of) `G`, so (H2) gives

    c(p + jv) = c(q + jv) = c(p + (j+1)v),

and by induction `c(p + jv) = c(p) =: α` for all `j = 0,…,n`. In particular `c(nv) = α`, and — since
`0 ∈ R_θ C_n` too — the same argument on the rotated chain gives `c(R_θ(nv)) = c(0) = α`. But
`|nv − R_θ(nv)| = 1` and both points lie in `X_n`, so a proper colouring must separate them.
Contradiction. `square`

*Two points of rigour that the previous version got wrong.* (i) The induction only ever uses the two
distinguished points `p + jv`, `q + jv` of each copy — never the other `V − 2` points, whose colours are
unconstrained (A1). (ii) The restriction argument is applied to the isometric image `P + jv` **alone**, so
it is unaffected by overlaps between different copies (A2, A4); it needs only that the map `P → P + jv`
be injective, which an isometry is.

## 4. Corollary: an exactly `(k+1)`-chromatic finite point set, without (H4) [P]

**Corollary.** Under (H1), (H2) there is a finite `Y ⊆ X_n`, with the induced unit-distance graph on
`Y` having chromatic number exactly `k+1`.

*Proof.* Let `Y` be minimal by inclusion among subsets of `X_n` whose induced graph is not
`k`-colourable (non-empty by the Theorem, and `X_n` is finite). For every `y ∈ Y` the set `Y ∖ {y}` is
`k`-colourable, i.e. `χ ≤ k`; and `χ(Y) ≥ k+1`. Adding one vertex raises the chromatic number by at
most one, so `χ(Y) ≤ 1 + max_{y} χ(Y∖{y}) ≤ k+1`. Hence `χ(Y) = k+1`. `square`

This is the exact version of the "upper bound" the previous draft tried to get from (H4): it needs no
colouring hypothesis at all, and it does **not** claim that `X_n` itself is `(k+1)`-colourable — which
may fail through accidental edges (A5).

## 5. Counts, overlaps, and what is not bounded [P]

* Chain: `|C_n| ≤ nV − (n−1)`. **Equality holds iff the only overlaps are precisely the intended
  ones** — the `n−1` consecutive identifications `q + jv = p + (j+1)v` inside the chain, and the single
  shared point `0` between the two chains — and no others (A2). Any further coincidence of two points
  from different copies, or from the two chains, strictly decreases the count.
* Union: `|X_n| ≤ 2|C_n| − 1 ≤ 2nV − 2n + 1` (the `−1` is the shared point `0`).
* Generating edges: the multiset `{image of e in copy} ∪ {image of e in rotated copy} ∪ {nv ∼ R_θ nv}`
  has exactly `2nE + 1` entries; the number of **distinct** unit edges among them is at most that, and
  the induced edge set `E(X_n)` **contains** it. No upper bound on `|E(X_n)|` is claimed (A3): accidental
  unit distances only add edges, which can only strengthen the lower bound but may destroy
  `(k+1)`-colourability.
* Hence a size bound of the form `|X_n| ≤ 2nV`, `|E(X_n)| ≥` (distinct generating edges), with
  `n = min{n : 4n²‖v‖² ≥ 1}` — the cost of the amplifier is `O(V / ‖v‖)` vertices.

## 6. Exact field statement [P]

All chain coordinates lie in `K²` (`jv ∈ K²`). The rotation matrix has entries
`cos θ = 1 − 1/(2n²‖v‖²)` and `±sin θ = ±√(4n²‖v‖² − 1)/(2n²‖v‖²)`, both in

    K' = K( √(4n²‖v‖² − 1) ),        [K' : K] ≤ 2,

**provided only that `‖v‖² ∈ K`** (true since `p, q` have coordinates in `K`); the square root of `‖v‖²`
is never needed (A7). Therefore `X_n ⊂ K'²`, every squared distance between points of `X_n` is an
element of `K'`, and each test "distance `= 1`" — every generating edge, every accidental edge, every
coincidence — is an exact comparison in `K'`. No floating point at any stage.

## 7. Validation: the construction at `k = 3` reproduces the Moser spindle [P]+[C]

`G` = diamond: `P = {(0,0), (1,0), (1/2, √3/2), (1/2, −√3/2)}`, two equilateral triangles sharing the
edge `(0,0)-(1,0)`; `V = 4`, `E = 5`; `p = (1/2, √3/2)`, `q = (1/2, −√3/2)` (the two tips).

* (H1): `G` is 3-colourable. (H2): in every proper 3-colouring the base edge uses two colours and each
  tip is adjacent to both base vertices, so both tips take the third colour [P].
* `v = q − p = (0, −√3)`, `‖v‖² = 3 ∈ ℚ` ✓. `4·1·3 = 12 ≥ 1`, so `n = 1`, `D = √3`.
* `cos θ = 1 − 1/6 = 5/6`, `sin θ = √11/6`, so `K' = ℚ(√3)(√11) = ℚ(√3, √11)` — the field the project
  already uses for its exact spindle certificate [C].
* Counts: `|X| ≤ 2·4 − 2 + 1 = 7` and `2E + 1 = 11` generating unit edges — the 7 vertices and 11 edges
  of the Moser spindle; the record's exact certificate has all eleven at squared length exactly `1`, so
  for this instance there is no accidental coincidence [C].
* The Theorem then says the spindle is not 3-colourable, and Corollary 4 gives a subset with chromatic
  number exactly 4. That the spindle *itself* is 4-chromatic needs the separate upper bound: the record
  notes that any graph built from diamonds and unit edges is at most 4-chromatic [C], which applies
  here — but it is a fact about this instance, not a consequence of the amplifier.

## 7b. The reusable validator (`checks/amp_cert.py`, exact, one process) [A]

A constructor/validator for this construction, exact in `Q(√p, √m)` with `Fraction` coefficients
(basis `1, √p, √m, √(pm)`), which builds the point set, enumerates **all** induced unit edges, checks
distinctness and the counts of §5, verifies the final endpoint distance exactly, and decides
non-`k`-colourability by exhaustive bounded enumeration. Three instances, all passing:

| instance | `k` | `n` | `D` | `|X|` (bound) | induced edges | generating (distinct/total) | final edge unit | proper `k`-colourings | field, `cos θ`, `sin θ` |
|---|---|---|---|---|---|---|---|---|---|
| `k2-path-n3` | 2 | 3 | `3/4` | 13 (13) | 13 | 13/13 | yes | **0** of `2^13` | `Q(√7,√5)`, `1/9`, `(4/9)√5` |
| `k2-path-n2-D-half` | 2 | 2 | **`1/2`** | 9 (9) | 9 | 9/9 | yes | **0** of `2^9` | `Q(√7)`, `−1`, `0` |
| `k3-diamond-n1` | 3 | 1 | `√3` | 7 (7) | 11 | 11/11 | yes | **0** of `3^7` | `Q(√3,√11)`, `5/6`, `(1/6)√11` |

The `k = 2` gadget is the path `p – r – q` with `p = (0,0)`, `r = (1/8, (3/8)√7)`, `q = (1/4,0)`:
`|p−r| = |r−q| = 1`, `‖q−p‖² = 1/16`, and `p, q` share a colour in every proper 2-colouring because
both differ from `r` and there are only two colours. With `‖v‖² = 1/16` the smallest admissible `n` is
`2`, and `n = 2` gives **`D = 1/2` exactly**, i.e. `θ = π`: this is the promised edge case, and it
works — the two ends are `±(1/2,0)`, distinct and exactly `1` apart, and the induced graph has `0`
proper 2-colourings. In all three instances `|X|` attains the bound of §5, so there are no unintended
overlaps, and the induced edge count equals the generating count, so there are no accidental edges
either; neither fact is assumed, both are verified exactly.

Coordinates, edge lists and all checks are stored in `amp_certificates.json`.

**Corrections to the script made after review (no re-run in this block — analysis only).** (i) The
docstring mis-stated the middle instance's enumeration size (`2^5`); it is **`2^9`**, since that control
has 9 distinct points, and the per-instance sizes are now written out. (ii) The reported field
`chain_points` counted *occurrences* of chain points, not distinct chain vertices; it is replaced by
`chain_occurrences` and `chain_points_distinct`. Neither affected a verification result. (iii) **Audit of
`squarefree`:** the denominator branch used `1/i**(e//2)`, correct only for even `e`; odd `e` needs
`1/i**((e+1)//2)`. All three controls have denominators `4` and `16` (even exponents), so the branch never
fired and their certificates stand — but the routine's *generality* is retracted until the fixed version
is re-run. Hand checks of the fix: `1/2 → (2, 1/2)`, `5/4 → (5, 1/2)`, `1/12 → (3, 1/6)`. This is
exactly the sense in which controls do not establish a library.

## 8. What is NOT claimed

1. **No forcing pair at the target `k` is known.** Forcing pairs at `k = 2` and `k = 3` *are* known —
   they are the positive controls of §7 and of the validator (`checks/amp_cert.py`), and the statement
   is about the target, not about all `k`. `Heule553` cannot serve as the input either: it is
   independently certified **pair-separating** at `k ≥ 5`, i.e. it forces *distinct* colours, which is
   the opposite of (H2). Nothing here produces a forcing pair at `k = 6`, and no finite unit-distance
   graph of chromatic number `≥ 7` is exhibited or implied.
2. **No upper bound** on the chromatic number of `X_n`; (H4)-style reasoning is withdrawn (A5). Only
   the existence of an exactly `(k+1)`-chromatic *subset* (Corollary 4) is asserted.
3. **No equivalence or hardness claim** between the existence of forcing pairs and `χ(ℝ²) ≤ 6`; only
   the one-way implication in Corollary 4 is proved (A8).
4. **No reversibility.** Nothing is said about deriving a forcing pair from a `(k+1)`-chromatic graph.
5. Nothing here touches the plane's chromatic number unless (H1), (H2) are discharged for a concrete
   gadget at `k = 6`, which is not the case in any evidence on file.

## 9. Checklist for a user of the amplifier

(i) exact coordinates of `P` in a number field `K` and a proof that `G` is `k`-colourable;
(ii) a proof of **(H2)** for *every* proper `k`-colouring — the only non-local obligation;
(iii) the exact comparison `4n²‖v‖² ≥ 1` to fix `n`, then the exact edge/coincidence enumeration in
`K'` of §6 (generating edges, accidental unit edges, overlaps);
(iv) to state `χ = k+1` for a specific set, take the vertex-minimal subset of Corollary 4 and verify its
colouring; the amplifier alone does not deliver `(k+1)`-colourability.
