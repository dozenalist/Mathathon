# Audit of `SEED-DESIGN-TAU.md` §1b / §2b: the one-point and multi-point gluing criterion

Read-only target: `supervisor/solve-geometry/SEED-DESIGN-TAU.md` (not edited). Analysis only: no solver,
no compute, no Lean. Grades in §8. **Nothing here is evidence of new forcing.**

**Version note (important).** The file was **edited by its owner during this block**: the version I read
in full was sha256 `6d764f92adc40a87bfe3473b980f1826fcac51bebccf5811272797540e448550` (236 lines); at the
end of the block the file on disk was `7a91d575ae76d544c37a6af9ef22c44ac917e61e015283c73766c33032e28a3a`
(242 lines). I re-checked the three defects below against the **current** file and all are still present:
**D1** at lines 159-160, **D2** at line 181, **D3** at line 179. So the audit is live against the version
on disk at hand-off, not only against the text I read. Line numbers refer to the current version.

> # WITHDRAWALS (later block): three of my own claims here are wrong
>
> **W1 — the diamond's forced-equal pair is the degree-2 pair, not the degree-3 pair.** In `K_4` minus an
> edge the two **degree-3** vertices are the *adjacent* pair (distance equal to the edge), and the two
> **degree-2** vertices are the non-adjacent pair at distance `sqrt3` which is forced equal at `k = 3`.
> My §4 sentence "its two degree-3 vertices `k, c` (distance `sqrt3`, non-adjacent)" is therefore
> self-contradictory and **withdrawn**. Consequence: **gluing degree-3 vertices pins nothing** — one must
> glue the **degree-2 forced-equal terminal** of one copy to the degree-2 forced-equal terminal of the
> other. The abstract argument in §4 is correct in *form* only once relabelled this way.
>
> **W2 — "the Moser spindle minus its closing edge" is not an induced unit-distance graph.** In the
> spindle embedding the omitted pair is still at unit distance, so the **induced** graph on those seven
> points has all eleven edges. The phrase "no accidental unit pair" is **withdrawn**, and with it the
> claim that the pair-forcing is realised geometrically. What survives is narrow: the *abstract* two-
> diamond gluing (10 edges) is a valid abstract counterexample to the abstract gluing proposition, but it
> is (i) not realisable as an induced unit-distance graph and (ii) not a *translate* gluing, which
> identifies `p0` with itself. So it does **not** refute `SEED-DESIGN-TAU.md`'s Proposition 2 in its stated
> geometric setting, and my "correction" of the worker's `(C1)` added nothing while introducing W1 and W2.
> The worker's own `R1` remains the accurate account of the one-point translate case.
>
> **W3 — "pair-separation says the pair projections are surjective".** False and withdrawn. Separation
> gives only: for each pair of vertices, *some* colouring separates them, i.e. the projection's image is
> not contained in the diagonal. It says nothing about realising every `(alpha,beta)`. Likewise no
> "near-rigidity" of `H553` is claimed anywhere: distinct signatures in a finite witness family is a
> statement about that family, not about the whole colouring set.
>
> **Superseding external result, recorded not re-derived.** The union `U` (1048 vertices) now has **34
> certified 5-colourings** whose signatures are **all 1048 distinct**, with 0 classes of size > 1, so
> *every* pair of distinct vertices — adjacent or not — is separated: no pair is pinned, and the **1145
> survivors are obsolete**. `U` stays **closed**; nothing in this directory reopens it. Source:
> `supervisor/solve-graphs/CERTIFICATE-union-no-forcing.md` with `certs/refine2_witnesses.txt` and
> `certs/union_tau_points.txt` (not re-verified by me).
>
> The remaining content of this file that stands: D1 (the swapped criteria), D2 (`tau=(0,10)` gives an
> empty overlap), the corrected `(K1)`/`(K2)` criterion, the multi-point `P/Q` distinction, and the
> soundness of the criteria under cross edges.

## 0. Verdict

The worker's own `E`/`N`/`F` table is **correct**. Three defects remain in the surrounding text, and I
confirm the two the supervisor named, plus one more in the same numbered item:

* **D1 — the two general criteria are swapped.** Verified; corrected statement in §2.
* **D2 — the `(0,10)` translate cannot share `p₀`.** Verified; the overlap is *empty*, so `(C1)` is
  void. Correct replacement in §4.
* **D3 — `(C1)` also mislabels the pinned pair.** In the diamond given, the two apexes
  `t₊=(1/2,√3/2)`, `t₋=(1/2,−√3/2)` are at distance **exactly 1**, hence adjacent, hence forced
  **different**, not equal. The forced-equal pair there is `(K, C1)`, at distance `√3`. So `(C1)` fails
  twice independently.
* `(C2)` is **sound** (I re-checked its three cross distances exactly, §5).

## 1. Setting, with the quantifiers made explicit

`H` a finite graph, `k >= 1`, `C := C_k(H)` the set of proper `k`-colourings. Two copies `H₁, H₂` of
`H`. A **gluing datum** is a finite index set `I` with, for each `p ∈ I`, a vertex `v(p) ∈ V(H)` in
`H₁` and a vertex `w(p) ∈ V(H)` in `H₂`, identified at a point `p`; together with a **cross-edge set**
`E_× ⊆ V(H) × V(H)` (an edge between `x` in `H₁` and `y` in `H₂`). The joint colouring set is

    J = { (c₁,c₂) ∈ C × C :  c₁(v(p)) = c₂(w(p))  for all p ∈ I,
                             c₁(x) ≠ c₂(y)        for all (x,y) ∈ E_×  }.

For `a ∈ V(H₁)`, `b ∈ V(H₂)` put `Poss(a,b) := {(c₁(a), c₂(b)) : (c₁,c₂) ∈ J} ⊆ [k]²`.

**(Non-vacuity.)** `J != ∅` is a *hypothesis*, not a consequence. If `J = ∅` the union has no proper
`k`-colouring and every statement of the form "… is forced in every colouring" is vacuous — in
particular "forced equal" and "forced different" both become true, which is a red flag, not a result.

## 2. D1: the exact criterion (the worker's two lines are interchanged)

The worker writes, for the one-point case (`I = {p₀}`, boundary colour `α`, `R_x[α]` as defined there):

> `a`,`b` **forced equal** ⟺ `R_a[α] ∩ R_b[α] = ∅` for every `α`;
> `a`,`b` **forced different** ⟺ for every `α`, `R_a[α] × R_b[α] ⊆ {(β,β)}`.

Both are the wrong way round. Since `Poss(a,b) = {(β,β') : ∃α, β ∈ R_a[α], β' ∈ R_b[α]}`:

* **forced equal** means every element of `Poss` is diagonal, i.e. for every feasible `α` the product
  `R_a[α] × R_b[α]` is contained in the diagonal;
* **forced different** means no element of `Poss` is diagonal, i.e. `R_a[α] ∩ R_b[α] = ∅` for every
  feasible `α`.

**Standalone criterion (both cases, exact quantifiers).**

> **(K1)** `(a,b)` is **forced equal**  ⟺  `∀(c₁,c₂) ∈ J : c₁(a) = c₂(b)`.
> **(K2)** `(a,b)` is **forced different**  ⟺  `∀(c₁,c₂) ∈ J : c₁(a) ≠ c₂(b)`.
> Otherwise **nothing is forced**: both relations are individually realisable, i.e. there are
> `(c₁,c₂), (c₁',c₂') ∈ J` with `c₁(a) = c₂(b)` and `c₁'(a) ≠ c₂'(b)`.

`(K2)` is a `∀∀` statement: *every* joint colouring separates. Equivalently by the fibre-product form:
with `P_a(γ) := {c₁(a) : c₁ ∈ C, c₁∘v = γ}` and `Q_b(γ) := {c₂(b) : c₂ ∈ C, c₂∘w = γ}` (note: **two
different vertex sets**, `v` for copy 1 and `w` for copy 2 — see §3),

> `(a,b)` forced equal ⟺ for every *feasible* boundary datum `γ` (one arising from some member of `J`),
> `P_a(γ) = Q_b(γ) = {β}` for a single `β`; forced different ⟺ `P_a(γ) ∩ Q_b(γ) = ∅` for every feasible `γ`.

**Why the worker's table survived the swap.** The table only uses the two extreme types, where the
product conditions and the intersection conditions happen to be *decided by the same data*: for `E/E`
both `R`'s are `{α}`, so the product is `{(α,α)}` (diagonal → equal) and the intersection is `{α}`
(non-empty → not different); for `E/N` the intersection is empty (→ different) and the product is
`{α} × ([k]∖{α})`, disjoint from the diagonal (→ not equal). The two predicates are complementary on
those two rows, so a swap is invisible. It becomes visible on `F` and `N/N` rows, and in general.

**Table re-verified** (I derived each row independently): `E/E` equal; `E/N` different; `E/F` nothing;
`N/N` nothing (needs `k >= 3` so that `[k]∖{α}` has two elements); `F/·` nothing. All five rows correct.

## 3. The multi-point form: one definition is not enough

The worker's §2b(a) replaces `α` by `γ = c|_I ∈ [k]^I` and writes `R_a[γ]` for both copies. That is an
**ambiguity that matters as soon as `I` has more than one point**: in copy 1 the datum constrains the
vertices `{v(p) : p ∈ I}` and in copy 2 the vertices `{w(p) : p ∈ I}`, and for a translation gluing
`w(p) = v(p) − τ ≠ v(p)`. Writing one `R_a[γ]` silently imposes the boundary on the same vertex set in
both copies, which is the `τ = 0` case. The correct form is the `P_a/Q_b` pair of §2. (When `|I| = 1`
and `v(p₀) = w(p₀) = p₀` they coincide, which is why the error is invisible in §1b.)

With `P`, `Q` distinguished, the worker's qualitative claim in §2b(a) is right and worth keeping: for
`|I| > 1` the pinning must hold *uniformly over the extensions of each feasible `γ`*, which is strictly
stronger than per-vertex pinning.

## 4. D2 and D3: `(C1)` is void twice over; the correct counterexample is the spindle minus its edge

**D2.** In `(C1)` the factor is the diamond with vertices `(0,0), (1,0), (1/2,√3/2), (1/2,−√3/2)` and the
second copy is placed at `τ = (0,10)`. Overlap is `{p ∈ P₁ : p − τ ∈ P₁}`; for `τ = (0,10)` the four
candidates `p − τ` are `(0,−10), (1,−10), (1/2,√3/2−10), (1/2,−√3/2−10)`, none of which lies in `P₁`.
So the intersection is **empty**: the copies are disjoint, `p₀` is in copy 1 only, and Proposition 1
(which is correct) applies — the colouring set is the full product and *nothing* is forced. The
sentence "no overlap beyond `p₀`" asserts an overlap that does not exist.

**D3.** `(C1)` also calls `t₊ = (1/2,√3/2)` and `t₋ = (1/2,−√3/2)` "the two tips" and asserts they
"carry the same colour in every proper 3-colouring". Their difference is `(0,1)`, of norm **1**: they are
**adjacent**, so in every proper colouring they carry *different* colours. `a = t₋` is therefore
different-pinned (`N`), not equal-pinned (`E`), relative to `p₀ = t₊`. In that diamond the forced-equal
pair is `(K, C1) = ((0,0), (1,0))`, whose distance is `√3`.

**Corrected counterexample (abstract graphs, then geometric).** Let `D` be a diamond `K₄` minus an edge,
with its two degree-3 vertices `k, c` (distance `√3`, non-adjacent) — in every proper **3**-colouring,
`c(k) = c(c)`.

* *Abstract.* Two copies `D₁, D₂`; identify `k₁` with `c₂`; add **no** cross edge. Then every proper
  3-colouring satisfies `c(k₁) = c(c₁)`, `c(c₂) = c(k₂)`, and `c(k₁) = c(c₂)` by the identification, so
  `c(c₁) = c(c₂)`: a **cross-copy forced equality with a one-point overlap and zero cross edges**.
  `c₁` and `c₂` are distinct and non-adjacent, so this is a genuine new relation. `(K1)` applied to the
  abstract datum: `J` is the set of pairs agreeing at the identified point; `P_{c₁}` and `Q_{c₂}` are
  each the singleton `{β}` for the boundary value `β`, hence equal → forced equal ✓.
* *Geometric.* Realise it with unit distances: take two unit diamonds sharing a vertex, rotated. This is
  the **Moser spindle minus its closing edge**: 7 vertices, `4+4−1`, and `5+5 = 10` edges, no accidental
  unit pair (the spindle has 11 edges and the eleventh is precisely the closing edge `c₁c₂`).
* *And the spindle itself is the point:* `|c₁ − c₂| = 1` in the spindle's geometry, so adding that edge
  turns the forced equality into a contradiction and the graph is **not 3-colourable**. So the
  forced-cross-copy-pair mechanism is exactly what makes the spindle 4-chromatic — which is the
  amplifier argument of `AUDIT.md` in miniature, and the reason this channel matters.

**Is `(C1)`'s failure avoidable?** Not within the diamond: every difference of the diamond's vertex set
has norm `1` (the five edges) or `√3` (the tips), so any `τ` creating an overlap is either a unit vector
(degenerate: every vertex is adjacent to its own image) or a tips difference, which I checked creates
cross edges. A translation gluing with one-point overlap *and* no cross edges therefore needs a factor
with more room; forcing a pair far from the boundary is the natural way to get it. This is a real
limitation of the *translate* channel, worth recording.

## 5. `(C2)` verified

`u = p₀ + (0,1) = (1/2, √3/2 + 1)`, `p₀ = t₊ = (1/2,√3/2)`, so `u` is adjacent to `p₀` and hence
different-pinned; `a = t₋` is — in the corrected reading, also **different**-pinned (D3), so the cited
conclusion (`a ≠ u` forced) is *true but for a different reason* than stated, and it is not an example of
crossing an `E` against an `N`. Exact cross distances: `|u − t₋| = √3 + 1`; `|u − (0,0)| = |u − (1,0)| =
√(2+√3)`; none equals 1 ✓. So no unintended cross edge, and the claim stands as a *different-pinned vs
different-pinned* non-result. It should be re-founded on a genuine `E` vertex (e.g. `a = C1` against
`p₀ = K`) to illustrate `E/N → different`.

## 6. What stays sound once cross edges couple the factors — and why pair-separation does not help

**Sound.** `(K1)`, `(K2)` and the `P/Q` form are stated over `J`, and `E_×` only *shrinks* `J`. So every
criterion remains valid verbatim; adding cross edges can only create forcing, never destroy it. Nothing
in §2-§4 changes. What breaks is only the *hand computation*: the colour-permutation argument that makes
a one-point gluing inert ("permute copy 2's colours") is destroyed by cross edges, because a cross
inequality `c₁(x) ≠ c₂(y)` is preserved only by permutations applied to **both** copies simultaneously,
while the boundary agreement survives a permutation of copy 2 alone only if it fixes every boundary
value pointwise. With `E_× != ∅` the surviving symmetry is the subgroup fixing the boundary pointwise
**and** preserving all `|E_×|` cross inequalities — usually trivial.

**Marginal blindness: pair-separation of `H` does not make the union inert.** This is the point on which
I agree emphatically with the graph worker's own `CORRECTION-restriction-map.md`, and it is worth stating
as a lemma because it is the trap:

> **Lemma (marginals do not see the coupling).** Let `H` be pair-separating at `k`: for all `x != y`
> there is `c ∈ C_k(H)` with `c(x) != c(y)`. This is a statement about the **marginal** `C_k(H)`: it says
> the projections `C_k(H) → [k]²` onto coordinate pairs are surjective. It says **nothing** about `J`,
> which is a subset of the **product** `C_k(H) × C_k(H)` cut out by boundary equations and cross
> inequalities, nor about the projection of `J` onto `{(a in H₁), (b in H₂)}`. Hence no cross-copy pair
> may be discarded on the grounds that each copy is pair-separating.

Two independent reasons, either sufficient: (i) `a` and `b` live in *different* copies, so "separation of
`a` and `b`" is not even a statement about `H`; (ii) even for within-copy pairs the correct transfer
direction is the one the graph worker retracted his way into: `H` induced in `G_rep` gives
`C(G_rep)|_H ⊆ C(H)`, so **forced in `H` ⟹ forced in `G_rep`**, and since `H` has *no* forced pair at
`k = 5` that implication eliminates **nothing**. The converse (non-forced in `H` ⟹ non-forced in `G_rep`)
is false, as that file already records.

## 7. The 1145 union candidates: what can be certified, and what cannot

`supervisor/solve-graphs/CORRECTION-restriction-map.md` reports `1145` survivors, all untested, after
correctly withdrawing the inference that would have discarded 112 of them. My conclusion:

**(a) No certified elimination is available from the data in hand, and I can say exactly why.** Every
elimination must be an `∃`-witness: a joint colouring `(c₁,c₂) ∈ J` exhibiting the *other* relation.
`J` is cut out by 58 boundary equations and 184 cross inequalities **[C-external counts]**. The only
complete colouring data held anywhere in the project are the 34 verified 5-colourings of `H` — single
objects, elements of `C_k(H)`, not of `J`. For a pair `(w,w') ∈ W × W` to certify anything it must lie in
`J`, which requires 58 specific equalities `w(v(p)) = w'(w(p))` to hold; a colouring pair meeting 58
prescribed coincidences is a measure-zero accident, so `J ∩ (W × W)` is generically empty. **Therefore
the 34 witnesses are not merely insufficient in principle — they are essentially silent about `J` in
practice.** Additional colourings are necessary, and they must be colourings of the **union** (or of `H`
under each boundary datum `γ`), not of `H` alone.

**(b) The one thing that *is* certified, and it is negative.** The transfer filter is
`forced in H ⟹ forced in G_rep`, and `H` has no forced pair at `k = 5`. So the `H`-certificate certifies
that **all 1145 must be tested**: the count cannot be reduced by any argument from `H`. That is a real
certified statement about the budget, even though it eliminates nothing.

**(c) A cheap sound refutation test, if colourings of `J` are ever produced.** For a candidate `(a,b)`
and any `(c₁,c₂) ∈ J`, look for a colour permutation `π` with: `π` fixes every boundary value `γ(p)` and
every colour appearing on the cross-inequality endpoints in a way that preserves `E_×` (in the
`E_× = ∅` case, any `π` fixing `γ` pointwise), and `π(c₂(b)) != c₂(b)`. Then `(c₁, π∘c₂) ∈ J` and the
two joint colourings exhibit *both* `c₁(a) = c₂(b)`-type and differing pairs, so `(a,b)` is neither
forced equal nor forced different. This is sound, costs one colouring per candidate, and — unlike the
`H`-witness route — actually prunes. Its weakness is stated honestly: with 184 cross inequalities the
permutation group that preserves them is typically trivial, so the test bites only for pairs whose
cross-constraints are sparse.

**(d) Red flag, pre-registered.** By the non-vacuity note of §1, the first thing any joint enumeration
must report is `J = ∅` or not. If `J = ∅` the union is not 5-colourable, i.e. a 1048-vertex
6-chromatic unit-distance graph — which must be treated as a solver artefact pending DRAT
(`AUDIT.md`'s protocol and the graph worker's stage 3), never as a result.

## 8. Grades

| item | grade |
|---|---|
| D1 (criteria swapped), with the corrected `(K1)`/`(K2)` and `P/Q` form | **PROOF** (direct from the definition of `Poss`); the worker's `E/N/F` table is independently re-derived and **correct** |
| D2 (`τ = (0,10)` gives empty overlap) | **PROOF**, exact rational arithmetic on four candidate points |
| D3 (`t₊, t₋` are adjacent, so `N` not `E`; the pinned pair is `(K,C1)`) | **PROOF**: `|t₊ − t₋| = 1`, `|K − C1| = √3` |
| corrected counterexample (spindle minus closing edge: 7 vertices, 10 edges, one shared point, no cross edges, forced cross equality at `k=3`) | **PROOF** (abstract) + **PROOF** of the geometric realisation given the spindle's edge count (11 = 10 + 1); I did not re-run the builder |
| `(C2)` | **PROOF** of its distances; its *role* is mislabelled (D3) |
| cross edges preserve `(K1)`/`(K2)` | **PROOF** (`E_×` only shrinks `J`) |
| marginal-blindness lemma | **PROOF** |
| 1145: no elimination available from `H`'s certificate | **PROOF** (transfer direction) + **argument**, not proof, for "`J ∩ (W×W)` is generically empty" |
| 58 / 184 / 1048 / 1145 counts | **C-external**, the graph worker's measurements, not re-verified here |
| any forcing, any chromatic claim | **none** |

**Limitations.** I did not construct a translation gluing with one-point overlap and no cross edges
(§4 argues the diamond cannot, which is not a general impossibility). I did not enumerate `J`, and the
"measure-zero" language in §7(a) is heuristic — the rigorous content is only that no witness pair is
*known* to lie in `J`. The `(c)`-test is sound but unexercised.

## 9. Reproduce

No computation was run. Everything above is hand arithmetic and definition-chasing; the three exact
figures used (`|t₊−t₋| = 1`, `|K−C1| = √3`, and the four `p−τ` candidates at `τ=(0,10)`) are checkable
by hand.
