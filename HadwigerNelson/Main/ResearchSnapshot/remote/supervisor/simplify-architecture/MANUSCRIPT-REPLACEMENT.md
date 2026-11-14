# Manuscript replacement: two-state support exclusion by avoiding traces

Proposed text for §6.3.3 of *The Euclidean plane is not five-colorable* (OpenAI, 23 Sep 2026; PDF
sha256 `607c2601b5ae655c…`), replacing the moving-state step of the strict-state argument. Notation is
the manuscript's. Forward references are to the manuscript's own labels: `(5.3)` palette disjointness
at unit distance, `(5.7)` the label-exclusion, `(6.2)`/Proposition 5.6 (almost every palette is a
diagonal `D_i = {i, i+2}`), `(6.6)` adjacency of consecutive states, Lemma 6.3 (strict separation),
Lemma 6.7 (support contact bans an angular step — **retained**).

## 6.3.3bis Two-state support exclusion

Throughout, `c` is a weak measurable `k`-colouring, `H_i` the closed essential supports of the
labels, `P_x(e)` the palette at `x` in direction `e`, and `w_x(e)` the state at `x` in direction `e`.
For a finite label set `J` we say that a measurable set of directions `A` **carries the `J`-state at
`x`** if `J ⊆ P_x(e)` for almost every `e ∈ A`. (For a diagonal `J = D_i` this is exactly
`A ⊆ H_i` up to null sets, i.e. the manuscript's "state `i`".) A **`K`-avoiding trace at a point `y`**
is a trace `β` at `y` with `β_i ≡ 0` for every `i ∈ K`.

> **Lemma 6.8 (avoiding traces exist on supports).** Let `B` carry the `K`-state at `x`, and let
> `b ∈ supp B`. Then there is a `K`-avoiding trace at `x + e_b`, where `e_b` is the unit vector in
> direction `b`.
>
> *Proof.* This is the trace-existence argument already used inside the proof of Lemma 6.7: on a set
> of directions of positive measure near `b` the state set is `⊇ K`, so the typical sampling of the
> unit circle at `x + e_b` avoids every label of `K` almost everywhere; weak-`*` compactness of the
> trace space and closedness of the trace relation give a limit trace, which avoids `K` identically.
> The existence proof uses only the weak-trace compactness already invoked in Lemma 6.7; no density,
> no state continuity and no `L¹` convergence enters. ∎

> **Lemma 6.9 (three-centre exclusion).** Let `A` carry the `J`-state at `x` with positive angular
> measure, let `K` be a finite label set with `(J ∪ K)ᶜ = {X}`, and let `y, z` admit `K`-avoiding
> traces with `|y − x| = |z − x| = 1`. Then `|y − z| ≠ 1`.
>
> *Proof.* Suppose `|y − z| = 1`. By (5.3) applied at the three ordered pairs `(y,x)`, `(z,x)`,
> `(y,z)` — the last with the angle of the unit vector `z − y`, which exists because `|z − y| = 1` —
> the palettes `P_x(e)`, `P_y(e)`, `P_z(e)` are pairwise disjoint for almost every direction `e`;
> the three exceptional sets are null and may be intersected. By Lemma 6.8 and (5.7), `P_y(e)` and
> `P_z(e)` are not contained in `K` for almost every `e`; again take the common conull set. On `A`
> the `J`-state gives `J ⊆ P_x(e)`. Choosing a direction in the common conull set that also lies in
> `A` (possible because `A` has positive measure), pick `i ∈ P_y(e) ∖ K`. Disjointness from `P_x(e)`
> gives `i ∉ J`, hence `i ∈ (J ∪ K)ᶜ = {X}`, so `X ∈ P_y(e)`; the same argument gives `X ∈ P_z(e)`.
> But `P_y(e) ∩ P_z(e) = ∅`. Contradiction. ∎

> **Corollary 6.10 (fixed state).** If `B` carries the `K`-state at `x` and `b, d ∈ supp B`, then
> `|e_b − e_d| ≠ 1`.
>
> *Proof.* Lemma 6.8 at `b` and at `d` gives `K`-avoiding traces at `x + e_b` and `x + e_d`; both lie
> on the unit circle about `x`. Apply Lemma 6.9. ∎

> **Theorem 6.11 (converging centres).** Let `x_n → x`, let `B_n` carry the `K`-state at `x_n`, let
> `b_n, d_n ∈ supp B_n` with `b_n → b`, `d_n → d`, let `A` carry the `J`-state at `x` with positive
> angular measure, and let `(J ∪ K)ᶜ = {X}`. Then `|e_b − e_d| ≠ 1`.
>
> *Proof.* Let `Z_K` be the set of points of the plane at which a `K`-avoiding trace exists. `Z_K` is
> **closed**: if `y_n ∈ Z_K` and `y_n → y`, the witnessing traces lie in a compact space, so along a
> subsequence they converge to a trace at `y`; the trace relation is closed, and the conditions
> `β_i ≡ 0`, `i ∈ K`, are closed conditions on the trace. By Lemma 6.8, `x_n + e_{b_n}` and
> `x_n + e_{d_n}` lie in `Z_K` for every `n`; by closedness and continuity of the exponential, the
> limits `y = x + e_b` and `z = x + e_d` lie in `Z_K`, and both are at distance one from `x`. Apply
> Lemma 6.9. ∎

**Remarks.** (i) The two limit traces may be obtained from different subsequences. Each is an actual
trace at its own limit centre, and Lemma 6.9 uses only the two *whole* palettes at those centres plus
a finite intersection of conull conditions — not a joint selection of unrelated angular state values.
(ii) Theorem 6.11 adds convergence `x_n → x` and a positive `J`-state *at the limit* `x`; it removes
all assumptions on the sets `B_n` beyond the support memberships, in particular every `L¹`-continuity
hypothesis. (iii) Neither statement presumes a second cycle centre: `Z_K` is a set in the plane
defined from `c` and `K` alone.

> **Corollary 6.12 (finite unit graphs on one circle).** Let `A` carry the `J`-state at `x` with
> positive measure and put `L = (J ∪ K)ᶜ`. For any finite family `{y_v} ⊂ Z_K` on the unit circle
> about `x`, the unit-distance graph on `{y_v}` is properly colourable by labels of `L`.
>
> *Proof.* Choose a `K`-avoiding trace at each `y_v`; for a common conull direction `e`, each
> `P_{y_v}(e)` meets `L` and adjacent palettes are disjoint. Pick a label of `P_{y_v}(e) ∩ L` at each
> vertex. ∎
>
> **Limitation.** For `|L| = 1` this is exactly Lemma 6.9. For `|L| = 2` it yields only bipartiteness,
> and unit chords on a single circle join directions differing by exactly `60°`, so each orbit of the
> `60°`-rotation is a `6`-cycle and the graph *is* bipartite: this circle-local device supplies no
> exclusion when two residual labels remain. This is a limitation of the device, not a statement
> about the six-colour problem or about transports between different circles.

**Dependencies used, named.** (5.3) palette disjointness at unit distance, with its null exceptional
set of parallel directions; (5.7) label exclusion; (6.2)/Proposition 5.6 for the diagonal form of
almost every palette; the trace-existence and weak-`*` compactness argument of Lemma 6.7's proof.
**Retained unchanged:** weak-trace compactness, the fixed-palette `L¹` transport, spectral smoothing,
Lemma 6.3, and Lemma 6.7 itself (which remains the source of the angular step ban and is used in
§6.3.4 as before). **No longer used:** the moving-state `L¹`/density-point sequence argument.

## Accounting note (added block 24)

This section is an **addition** to the manuscript, not a substitution of text: the paper's §6.3.3 stays,
including Lemma 6.3, (6.6), the derivation `S(a) ∩ S(Ra) = ∅`, and Lemma 6.7 unchanged. On the
formalisation side the corresponding module is **new** (236 lines, 8 declarations), so the integration
packet currently nets **+170** lines; the declaration-level removals that this section makes possible
(277 lines in the strict-state branch, exact ranges in `INTEGRATION-MAP.md` §3bis) are a *later*,
still-conditional stage. The scientific gain is the conceptual one: one closed carrier and one forcing
step replace an ambient `L¹` sequence argument, and the finite-graph form of Corollary 6.12 states
exactly how far the residual-label device reaches.
