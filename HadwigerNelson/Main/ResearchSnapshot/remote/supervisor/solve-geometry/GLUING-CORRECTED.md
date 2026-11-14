# Corrected note: cross-copy binary colour relations in a gluing at one vertex

Analysis only; no computation, no run. Supersedes `SEED-DESIGN-TAU.md` §1b–§3b. Grades: **[P]** exact
derivation written here; **[C]** cited, not verified; **[X]** needs computation.

## 0. Retractions of the previous block

| # | what I wrote | what is right |
|---|---|---|
| R1 | "`a,b` **forced equal** ⟺ `R_a[α] ∩ R_b[α] = ∅` for every `α`" and "**forced different** ⟺ both are the same singleton for every `α`" | **Reversed.** Disjointness at every feasible `α` means the colours can *never* agree, i.e. **forced different**; being the same singleton at every feasible `α` means they always agree, i.e. **forced equal**. (The `E`/`N` table below was correct; only those two bullets were wrong.) |
| R2 | geometric counterexample (C1): "second copy at `τ = (0,10)`, no overlap beyond `p₀` …, tracked vertices forced equal" | **Self-contradictory, retracted.** Translating the second copy by `(0,10)` moves `p₀` to `p₀ + (0,10)`; the copies then have *empty* intersection, and "the two tracked vertices are both forced equal to `p₀`" is meaningless. No isometry may be asserted without an exact verification that the overlap is exactly the intended set and the cross-edge set is exactly known. Replaced by an abstract-graph example in §3. |
| R3 | "`H`'s colouring space is near-rigid, since the 34 witnesses separate all 553 vertices" | **Not implied.** Separation of witnesses says: for every pair of vertices some witness distinguishes them — a property of the *witness set* (the map vertex ↦ colour-signature is injective). It says nothing about how many `k`-colourings exist, nor about how strongly a 58-point boundary pins a colouring. Rigidity of the boundary is exactly what the `R`-sets of §1 measure, and it must be computed, not inferred. |

## 1. The object, and the correct criteria

**Setting.** One shared vertex `p₀`, **no cross edges**. A colouring of the union is a pair `(c₁,c₂)` of
proper `k`-colourings of the factor with `c₁(p₀) = c₂(p₀)`. For a factor vertex `a` and a colour `α` put

    R_a[α] := { β ∈ [k] : some proper k-colouring of the factor has c(p₀) = α and c(a) = β }.

Every `α` is *feasible*: `R_a[α] ≠ ∅`, because permuting colours maps any colouring with `c(p₀) = α₀` to one
with `c(p₀) = α`. The realisable colour pairs are exactly

    Poss(a,b) = ⋃_{α ∈ [k]} R_a[α] × R_b[α]        (correct as stated last block),

and therefore, **with the two bullets now in the right order**,

* `a, b` are **forced DIFFERENT** ⟺ `Poss(a,b) ∩ Δ = ∅` ⟺ `R_a[α] ∩ R_b[α] = ∅` for every `α`;
* `a, b` are **forced EQUAL** ⟺ `Poss(a,b) ⊆ Δ` ⟺ for every `α`, `R_a[α]` and `R_b[α]` are both the same
  singleton;
* otherwise nothing is forced.

Here `Δ = {(γ,γ)}`. Note the asymmetry that made the old statement slip: `Poss` is a union of *products*,
so "disjoint fibres" is the *negative* conclusion and "singleton fibres" the *positive* one.

## 2. `E`/`N`/`F` — and a classification that removes the ambiguity in `F` [P]

Call `a` **`E`** if `R_a[α] = {α}` for all `α`; **`N`** if `R_a[α] = [k] ∖ {α}` for all `α`; **`F`**
otherwise. Then, **for `k ≥ 3`**:

| `a` | `b` | conclusion |
|---|---|---|
| `E` | `E` | forced **equal** (`{α} ∩ {α} = {α} ≠ ∅`, both singletons) |
| `E` | `N` | forced **different** (`{α} ∩ ([k]∖{α}) = ∅` for every `α`) |
| `E` | `F` | nothing forced |
| `N` | `N` | nothing forced **for `k ≥ 3`** (both differ from `p₀`, and there are `k − 2 ≥ 1` further colours, so they may agree or not) |
| `N` | `F` | nothing forced |
| `F` | `F` | nothing forced |

*`k = 2` is different, and the difference is exactly one row.* `N` then means `R_a[α] = {β}` with
`β ≠ α` the *other* colour, so `R_a[α] = R_b[α] = {β}` — the same singleton — and by §1 `a, b` are
**forced EQUAL**. So the `N`/`N` row (and only that row) requires `k ≥ 3`; the `E`/`E`, `E`/`N` and all
`F*` rows read the same at `k = 2`.

*Justification of the `F` rows, which the previous version asserted without proof.* Colour symmetry gives
the identity `R_a[σ(α)] = σ(R_a[α])` for every permutation `σ` of `[k]` (apply `σ` to a colouring and to
its inverse). Hence `R_a[α₀]` is invariant under the stabiliser of `α₀`, i.e. under the full symmetric
group on `[k] ∖ {α₀}`, whose only invariant subsets of a set of size `k − 1 ≥ 2` are `∅` and the whole set.
So, up to relabelling, **a factor vertex is exactly one of three kinds**:

* `E`: `R_a[α] = {α}` — its colour is forced to *equal* `p₀`'s, whatever that is;
* `N`: `R_a[α] = [k] ∖ {α}` — forced *different* from `p₀`'s, and otherwise unconstrained;
* `F*`: `R_a[α] = [k]` — its colour and `p₀`'s are completely independent.

So `F` is not an open-ended class: it is the single kind `F*`, for which every fibre is the whole colour
set. That is why all `F`-rows force nothing, and the proof is now a proof rather than an assertion. (For
`k = 2` the stabiliser is trivial, but the classification still yields exactly `{α}`, `{β}`, `[k]`.)
**Caveat:** this classification is about the relation to the *single* point `p₀`; it says nothing about how
`a`'s colour relates to other vertices' colours.

## 3. Abstract-graph examples (no geometry, no isometry asserted)

**A1 — forced equality across a one-vertex gluing.** Let `D` be the abstract graph on `{p₀, b₁, b₂, a}` with
edges `p₀b₁, p₀b₂, b₁b₂, ab₁, ab₂`. At `k = 3`, `b₁,b₂` differ, `p₀` takes the third colour, `a` likewise,
so `c(a) = c(p₀)` in every proper 3-colouring: `a` is `E`. Glue two copies of `D` at `p₀`. By the `E`/`E`
row the two copies' `a`-vertices are **forced equal**, with one shared vertex and no cross edges. This is
the corrected replacement for the retracted (C1): it needs no coordinates at all.

**A2 — forced difference across a one-vertex gluing.** Copy 1: `D` with `a` of type `E`. Copy 2: the single
edge `{p₀, u}`, whose `u` is of type `N` (it must differ from `p₀`, and by symmetry takes any other colour).
By the `E`/`N` row, `a ≠ u` is **forced**. Again abstract.

**What a geometric realisation would additionally require** (and why (C1) failed): an exact verification
that the two copies' point sets meet in *exactly* the intended point and that the cross-edge set is exactly
the claimed one. Both are finite exact computations; neither may be assumed.

## 4. Multi-point boundaries: common feasible data, and why cross edges are joint

With `|I| > 1` and overlap `I`, a colouring of the union is a pair agreeing on `I`; write
`γ = c|_I ∈ [k]^I` for the boundary datum and

    R_a[γ] := { β : some proper colouring of the factor extending γ on I has c(a) = β }.

Then, and this is the point the previous version fudged,

    Poss(a,b) = { (β,β') : ∃ γ ∈ [k]^I with β ∈ R_a[γ] and β' ∈ R_b[γ] },

**one and the same `γ` for both factors**. Products over *different* boundary data are not admissible:
choosing `γ₁ ≠ γ₂` would describe two colourings that disagree on `I`, which the gluing forbids. Feasibility
of `γ` is therefore a *joint* condition — `γ` must be extendible in copy 1 *and* in copy 2 (and, in general,
the two extension sets are different, since the identifications pair different vertices of the factor
across the two copies).

**Why the cross edges add joint constraints, not factor constraints.** A cross edge is a pair
`(x, y+τ)` at distance exactly `1`; it requires `c₁(x) ≠ c₂(y)`. That is a relation between the *two
colourings*, so it is invisible to `R_a` and to `R_b` separately: it cuts the joint set `C₁ × C₂`, not either
factor. Two consequences: (i) a cross edge can destroy feasibility of a boundary datum that each factor
admits alone; (ii) a cross edge can force a binary relation even when both vertices are of type `F*`, because
the constraint is not of the "agree at `p₀`" form. Conversely, when a crossing-free gluing happens to force a
relation, that relation is already readable from the `R`-sets — which is exactly the `E`/`E` and `E`/`N` rows.

## 5. Status

* §1 criteria, §2 classification and table, §3 A1/A2: **[P]**, exact, no computation, and independent of
  any geometry.
* §4: **[P]** restatement of the joint structure; the specific counts (1048 vertices / 58 overlaps / 184
  cross edges) are **[C-external]** and unverified here.
* Retracted: the two reversed bullets (R1), the `(0,10)` geometric example (R2), and the near-rigidity
  inference from the 34 separating witnesses (R3).
* Not claimed: that any specific pair in any seed is forced; colourability of any union; any palette,
  chromatic or plane-level conclusion. No geometric proposal is made in this block.
