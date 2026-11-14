# Seed design: when a translate `H ∪ (H+τ)` can create a new terminal relation

> **SUPERSEDED IN PART.** Sections 1b–3b below contain two reversed criteria, a self-contradictory
> geometric counterexample and an unjustified rigidity inference. They are superseded by
> `GLUING-CORRECTED.md`, which carries the retraction table; read that first. Section 0 (the retraction
> banner R1/R2 for Proposition 2 and the spindle-vs-Heule553 scope) still stands.


## 0. RETRACTIONS (added after review; the original text is kept below, marked)

| # | what I wrote | what is right |
|---|---|---|
| R1 | **Proposition 2**: "a single shared point `p₀` and no cross edges ⇒ no relation between `a ∈ V(M)∖{p₀}` and `b ∈ V(M+τ)∖{p₀}` is forced", justified by permutations of the `k` colours fixing `c₂(p₀)` | **FALSE.** Colour permutations fixing `p₀`'s colour preserve `c₂(p₀)`, so they cannot move *anything that is forced equal to `p₀`*, and they cannot merge two colours that are *forced different from `p₀`*. Consequently: a vertex forced equal to `p₀` in one copy and a vertex forced equal to `p₀` in the other are forced **equal** to each other across the copies; a vertex forced equal to `p₀` in one copy and forced different from `p₀` in the other are forced **different**. Both relations are new, neither copy has a cross edge, and the overlap is one point. What survives of the old proposition is only the *colourability* half (the union is `k`-colourable if the factor is, by colour-permutation gluing). The correct description is §1b. |
| R2 | I analysed the **7-vertex Moser spindle** and its four `Q(√3)`-only difference channels | The assigned current seed is **Heule553**, not the spindle. The axis computation of §3 is a statement about `M` only and **must not be transferred to `H553`**: `H553` has 553 vertices, no reason to contain the spindle's three vertex directions, and its `τ`-channel structure is a different question. §3 is hereby scoped to `M` and to nothing else. The actual union `H ∪ (H+τ₀)` with `τ₀ = (3/2, √3/2)` has, per the graph worker, **1048 vertices, 58 overlaps, 184 new cross edges** (counts quoted **[C-external]**, not verified here). |

Analysis only; no search, no run. Read-only inputs: `supervisor/solve-graphs/{SEED-S1.md,STATUS.json,
NEXTSTEP-CORRECTION.md,udg/build.py}`. Grades: **[P]** exact derivation below (hand arithmetic, `Q(√3,√11)`);
**[S]** read from source; **[X]** needs computation, not done here.

## 0. What the graph worker is testing, and the correction it already made [S]

`H` = Heule553, **5-chromatic** (certified 4-UNSAT) and **pair-separating at `k ≥ 5`** (34 five-colourings
whose signatures separate all 553 vertices). Because `H` is not 4-colourable, every "forced equality" at
`k = 4` would be vacuous (`NEXTSTEP-CORRECTION.md`), so the live object is a *different* seed: `S1 = V(M) ∪
(V(M)+τ)` with `M` the Moser spindle (`7` vertices, `χ = 4`) and `τ = (3/2, √3/2)`. So the analysis below is
about `M`, not about `H`; the same criterion applies verbatim to any frozen point set.

## 1. The exact objects [S]+[P]

`udg/build.py::moser` fixes, in `Q(√3, √11)`,

    K  = (0, 0),                       C1 = (√3, 0),            C2 = (5√3/6, √33/6),
    A1 = (√3/2, 1/2),                  A2 = (√3/2, −1/2)        (the two apexes of diamond K–C1),

with `|C1 − C2| = 1` asserted in the builder, `|K − Ci|² = 3` and `|Ai − K| = |Ai − C1| = 1`.
Consequences used below, all exact:

* `τ = (3/2, √3/2) = √3 · A1`, and `|A1| = 1`, so **`τ` is `√3` times a unit vertex of `M`**;
  `|τ|² = 3`, so `τ ∉ {unit vectors}` and no vertex is automatically at distance `1` from its image.
* `τ ∈ Q(√3)² ⊂ Q(√3,√11)²`: translation preserves the field, no extension, all tests exact.

## 2. The two channels, and what a union can and cannot do

Let `D(M) = {p − q : p, q ∈ V(M)}` (differences) and `X_τ = V(M) ∪ (V(M) + τ)` with the **induced**
unit-distance edge rule.

* **Overlaps** are exactly `{p ∈ V(M) : p − τ ∈ V(M)}`, i.e. `τ ∈ D(M)`.
* **Cross edges** are exactly the pairs `(p, q+τ)`, `p, q ∈ V(M)`, with `|p − q − τ| = 1`, i.e. the
  differences `p − q ∈ D(M)` at distance **exactly** `1` from `τ`.

**Proposition 1 (a disjoint union forces nothing) [P].** If `τ ∉ D(M)` and no `d ∈ D(M)` satisfies
`|d − τ| = 1`, then `X_τ` is a disjoint union of two copies of `M`, and

    C(X_τ) = C(M) × C(M+τ)      (every pair of proper k-colourings, no compatibility condition),

so (i) `X_τ` is `k`-colourable iff `M` is, and (ii) **no relation between a vertex of `M` and a vertex of
`M+τ` is forced** — the projection to either factor is surjective, so any prescribed colour can be given to
either point independently. *Proof:* the constraints of `X_τ` are exactly the union of the two copies'
constraints, which are disjoint. `square`

**Proposition 2 — RETRACTED, see §0 R1 and the replacement §1b.** The original text follows.
*(old, wrong)* A single shared point forces nothing either, for `k ≥ 3`. Suppose the copies meet in
exactly one point `p₀` and there are no cross edges. Then `C(X_τ) = {(c₁,c₂) ∈ C(M) × C(M+τ) :
c₁(p₀) = c₂(p₀)}`, and for every `a ∈ V(M)∖{p₀}`, `b ∈ V(M+τ)∖{p₀}` and every colour pair, some member of
`C(X_τ)` realises it (permute the colours of `c₂` by a permutation fixing `c₂(p₀)`, of which there are
`(k−1)! ≥ 2` when `k ≥ 3`). Hence no relation between such `a, b` is forced. `square`

**So the whole content of a union is carried by cross edges** — overlaps alone only impose agreement at
finitely many points, and colour permutations absorb that unless `k = 2`. **This is the "colour-extension
argument" that the phrase "a zero-cross-edge union is harmless" needs**: such a union is harmless *because*
the colouring set factors as a product and its projections are onto — and for the same reason it is
**useless**; harmlessness must be proved, not inferred from the word "union". Note also the asymmetry: a
cross-edge union is the useful one *and* the dangerous one — it may make `X_τ` non-`k`-colourable, which for
a `k = 4` gadget seed is a red flag to be re-examined, not a success.

## 3. What `τ = √3·A1` actually does: the axis computation [P]

Put `τ_k = k·A1` for `k > 0` and ask when a cross edge appears. For the four `Q(√3)`-only differences
(up to sign) `(√3,0)`, `A1`, `A2`, `(0,1)` the distances are exact quadratics in `k`:

| `d` | `|d − τ_k|²` | `= 1` iff |
|---|---|---|
| `(√3,0)` (= `C1 − K`) | `k² − 3k + 3` | `k ∈ {1, 2}` |
| `A1` (= `A1 − K`) | `(k − 1)²` | `k ∈ {0, 2}` |
| `A2` (= `A2 − K` = `C1 − A1`) | `k² − k + 1` | `k ∈ {0, 1}` |
| `(0,1)` (= `A1 − A2`) | `k² − k + 1` | `k ∈ {0, 1}` |

Readings, all exact:
* `k = 2` gives **two cross edges simultaneously** (from `k²−3k+3 = 1` and `(k−1)² = 1`): the unique
  positive `k` doing so on this axis.
* `k = 1` gives one cross edge but is degenerate: `τ = A1` is a **unit** translate, so *every* vertex `p`
  is at distance `1` from `p + τ`, i.e. the union carries `|V(M)|` automatic cross edges. Not a seed move.
* **`k = √3` — the S1 choice — is silent on all four channels**: `k² − 3k + 3 = 6 − 3√3 ≈ 0.804`,
  `(k−1)² = (√3−1)² ≈ 0.536`, `k² − k + 1 = 4 − √3 ≈ 2.268`, none equal to `1`. So `S1`'s cross edges, if
  any, can only come from the differences carrying `√11` (`C2`, `B±`), and none of the four diamond
  channels fires.

**One `√11` channel computed [P].** For `d = C2 − K = C2`:

    |C2 − τ|² = 6 − (5/2)√3 − (1/2)√11 ≈ 0.0116,        |C2 − τ| ≈ 0.108 .

So `K + τ` lands **0.108** from `C2`: not an overlap (so no identification) and not an edge (distance
`≠ 1`). Two consequences worth reporting to the seed's owner: (i) `τ` is *not* in `D(M)` through this
route, and (ii) the configuration is a **near-coincidence**, so the union's edge set is a discontinuous
function of `τ`: any float or rounded `τ` could turn that 0.108 into an accidental overlap. The exact build
is therefore not a nicety. The remaining `√11` differences need the same exact test at run time [X].

## 4. The selected alternative: `τ_alt = 2·A1 = (√3, 1)` [P]

Justification, in order of strength:

1. **Two cross edges by construction, no search.** `k = 2` is the unique positive `k` on the `A1` axis with
   both `|C1 − K − τ| = 1` and `|A1 − K − τ| = 1` (§3). Explicitly, with `K' = K + τ_alt = (√3,1)`:
   `|K' − C1| = |(0,1)| = 1` and `|K' − A1| = |(√3/2, 1/2)| = 1`. So the translated hub is at unit
   distance from two vertices of `M`, and `{K', C1, A1}` is an equilateral triangle of side `1`. That is
   exactly the "new diamond" the seed asks for — obtained by solving the crossing equations, not by
   guessing.
2. **No degenerate scaling.** `|τ_alt| = 2 > 1`, so no vertex is adjacent to its own image; and `τ_alt` is
   not in `{Q(√3)`-only differences`}` by §3 values, so no overlap arises from the four diamond channels.
   Whether any `√11` difference equals `τ_alt` is a one-line exact test at run time [X].
3. **Same field, exact.** `τ_alt ∈ Q(√3)² ⊂ Q(√3,√11)²`; no extension, no floats. `τ_alt = 2A1` is also a
   lattice-class vector (Eisenstein norm `4`) while `τ = √3 A1` is norm `3`, so the two seeds probe
   different commensurability classes rather than rescalings of one another.
4. **A distinct isometry variant, for the block after:** `R_{60°} τ = (0, √3)` (computed: `ω(1+ω) = i√3`),
   same norm `√3`, same field. It is a genuinely different placement unless `M`'s vertex set is invariant
   under `R_{60°}`, which it is not (the spindle has a mirror symmetry, not a rotation symmetry), so it is a
   second independent probe rather than a relabelling.

**Recommended next parameter: `τ_alt = (√3, 1)`**, with `R_{60°}τ = (0, √3)` as the follow-up.

## 5. What this does not do, and what must still be computed [X]

* It does not show `S1` or `S1(τ_alt)` is `4`- or `5`-colourable, does not produce a forced-equal pair, and
  says nothing about `k = 5` or `6`.
* It does not compute the full cross-edge count or the overlap set for either `τ`: only the four
  `Q(√3)`-only channels are settled by hand; the `√11` channels (`C2`, `B±` versus every vertex) remain.
* The *usefulness* test is unchanged and must be run: cross-edge count `0` ⟹ by Prop. 1 or 2 the seed is
  inert; cross edges `> 0` ⟹ the seed is coupled and the colouring questions become real. A non-4-colourable
  union is a stop-and-check signal, not a result.
* No plane-level or chromatic-number claim of any kind is made here.

## 1b. The correct description of cross-copy binary relations in a one-point gluing [P]

**Setting.** `P₁` a finite point graph (factor), `P₂ = P₁ + τ`, intersection `I = P₁ ∩ P₂ = {p₀}` (one
point), no cross edges. A colouring of the union is a pair `(c₁,c₂)` of proper `k`-colourings of the factor
with `c₁(p₀) = c₂(p₀)`.

**The right invariant is a relation, not a type.** For a vertex `a` of a factor put

    R_a[α] := { β ∈ [k] : some proper k-colouring of the factor has c(p₀) = α and c(a) = β }   (α ∈ [k]).

Every `α` occurs (`R_a[α] ≠ ∅` for all `α`, by permuting colours). Then the possible colour pairs for a pair
`(a, b)` drawn from the two copies are exactly

    Poss(a,b) = { (β, β') : ∃ α ∈ [k] with β ∈ R_a[α] and β' ∈ R_b[α] },

and therefore, **exactly**,

* `a` and `b` are **forced equal** ⟺ `R_a[α] ∩ R_b[α] = ∅` for every `α ∈ [k]`;
* `a` and `b` are **forced different** ⟺ for every `α`, `R_a[α] × R_b[α] ⊆ {(β,β) : β ∈ [k]}`,
  i.e. both are singletons with the same element.

**The three special cases, which is all a hand argument usually needs.**
Call `a` *equal-pinned* (`E`) if `R_a[α] = {α}` for all `α`; *different-pinned* (`N`) if
`R_a[α] = [k]∖{α}` for all `α` (this needs `k ≥ 3` for the symmetry used); *free* (`F`) otherwise, i.e. there
is `α` with `α ∈ R_a[α]` and there is `α` with `α ∉ R_a[α]`. Then

| `a` | `b` | conclusion |
|---|---|---|
| `E` | `E` | forced **equal** (`{α} ∩ {α} = {α} ≠ ∅`) |
| `E` | `N` | forced **different** (`{α} ∩ ([k]∖{α}) = ∅`) |
| `E` | `F` | nothing forced (`α ∈ R_b[α]` for some `α`, so equality is realisable; and `α ∉ R_b[α]` for another, so inequality is too) |
| `N` | `N` | nothing forced (both ≠ `p₀`; they may agree or not) |
| any `F` | any | nothing forced |

**Counterexamples to the retracted Proposition 2** (exact coordinates, `k = 3`).

* **(C1) forced equality across copies, one shared point, no cross edges.** Factor = the diamond
  `{(0,0), (1,0), (1/2,√3/2), (1/2,−√3/2)}`, in which the two tips `t₊ = (1/2,√3/2)`, `t₋ = (1/2,−√3/2)`
  carry the same colour in every proper 3-colouring. Take `p₀ = t₊` and `a = t₋`: `a` is equal-pinned
  (`E`). Place the second copy at `τ = (0,10)`: no overlap beyond `p₀`, and every cross distance is
  `≥ 10 − 1.733 > 1`, so there are no cross edges either. Nevertheless the two copies' `t₋`-images are both
  forced equal to `p₀` and hence **forced equal to each other**. The union is still 3-colourable (glue by
  permuting), so this is a genuine new terminal relation with no cross edge.
* **(C2) forced inequality across copies.** Copy 1 the same diamond with `p₀ = t₊`, `a = t₋` (`E`); copy 2 the
  single unit edge `{p₀, u}` with `u = p₀ + (0,1) = (1/2, √3/2 + 1)` (which is at distance `> 1` from
  `(0,0), (1,0), t₋`, so no unintended cross edge). `u` is different-pinned (`N`), so `a ≠ u` is **forced**.

So the honest statement is: *an overlap creates relations through the boundary pattern, whether or not
there are cross edges; cross edges are not the only channel* — the correct dichotomy is
"free vertices give nothing; pinned vertices give everything their pinning dictates".

## 2b. Multi-point, non-clique overlaps: what changes, and why the Heule seed is the right place to look [P]+[C]

**(a) The constraint becomes a fibre product over the whole overlap pattern.** With `|I| > 1` and no
cross edges, a colouring of the union is a pair `(c₁,c₂)` with `c₁(v(p)) = c₂(w(p))` for every `p ∈ I`, where
`v(p)` is the vertex of the factor occupying `p` in copy 1 and `w(p)` the vertex occupying it in copy 2
(`w(p) = v(p) − τ`). The one-point formula generalises by replacing the colour `α` with the *boundary datum*
`γ = c|_I ∈ [k]^I`:

    R_a[γ] := { β : some proper colouring of the factor extending γ on I has c(a) = β },

and then `Poss(a,b) = {(β,β') : ∃ γ ∈ C(I) with β ∈ R_a[γ], β' ∈ R_b[γ]}`. The two forcing criteria read
exactly as in §1b with `α` replaced by `γ`. **Per-factor pinning types are no longer enough**: the pinning
must hold uniformly over the *extensions of each boundary datum*, which is a strictly stronger requirement.

**(b) Non-clique is where the content is.** If the overlap `I` were a clique, properness would force distinct
colours on all its points, so `|I| ≥ k+1` would make the union immediately non-`k`-colourable and
`|I| ≤ k` would pin the boundary datum to an injection — both degenerate for a forcing argument. A **non-clique**
`I` is the only case where `C(I)` has internal freedom, which is exactly the freedom that a large overlap can
*remove* asymmetrically: the same pattern read through the two different vertex identifications
`v` versus `w` can admit different extension sets. That asymmetry is the mechanism by which a multi-point
overlap can create a relation that neither copy has.

**(c) Consequences for `H553 ∪ (H553 + τ₀)` [C-external counts: 1048 vertices, 58 overlaps, 184 cross edges].**
* The union's colouring set is `{(c₁,c₂) ∈ C(H)² : c₁(v(p)) = c₂(w(p)) ∀ p ∈ I, and c₁(x) ≠ c₂(y) for all
  184 cross unit pairs}` — 58 equations and 184 inequalities coupling two *different* 5-colourings of the same
  `H`, since the identifications pair different vertices of `H` in the two copies.
* That is a large coupling: `H`'s colouring space is highly structured (the 34 witnesses separate all 553
  vertices, so no two vertices are colour-indistinguishable over `C(H)`), and a 58-point overlap therefore
  constrains a large part of the pattern. This is the sense in which the multi-point overlap can support the
  seed: it is the channel through which the near-rigidity of `H` becomes a coupling between copies.
* **The practical filter, from §1b/§2b.** Of the `C(1048,2) ≈ 5.5·10^5` cross pairs, only those with a
  *pin* can be forced: if for some boundary datum `γ` both `R_a[γ]` and `R_b[γ]` contain two distinct colours,
  nothing is forced pair-wise. So the computation is: enumerate `C(H)` (or the union's joint set), tabulate the
  pinning of each vertex against the 58 boundary coordinates, and test only the pinned candidates. This is
  the same shape as the graph worker's existing equality pipeline and should be appended to it rather than
  run separately.
* **Red flag to state in advance.** If the 58 equations plus 184 inequalities are inconsistent, the union is
  not 5-colourable — a 1048-vertex 6-chromatic unit-distance graph, which would be extraordinary and must be
  treated as a solver artefact to be DRAT-checked (the graph worker's stage-3 protocol already says this), not
  as a result.

## 3b. Status of this block's claims

* §1b formula, the `E`/`N`/`F` table and counterexamples (C1), (C2): **[P]**, exact, checked by hand; the only
  ingredients are colour-permutation symmetry and the diamond's forced-equality at `k = 3`.
* §2b (a), (b): **[P]** restatement of the fibre-product structure; (c) depends on the **[C-external]** counts
  `1048/58/184`, which I have not verified and which are the graph worker's measurement.
* Not claimed: that the Heule union is or is not 5-colourable, that any specific pair is forced, any palette
  structure, any chromatic or plane-level conclusion. No further spindle-axis guesses are made, and no
  translate is proposed for `H553` in this block.
