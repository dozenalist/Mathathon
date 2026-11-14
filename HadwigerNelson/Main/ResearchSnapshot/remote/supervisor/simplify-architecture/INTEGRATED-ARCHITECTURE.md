# One argument for both consumers: avoiding-trace centres + triangle forcing

Human integrated architecture. No build, no compute, no edits to originals. All line numbers measured
this block by `rg`/`sed` over `lean/OAI/Geometry/PlaneColoring/`.

## 1. The one principle

Fix `c : ℂ → Fin k` measurable with `hw : WeakColoring k c`, and a label set `K`.

**Carrier.** `Z_K := {y : ℂ | ∃ β : TraceVector k, IsTrace c hc y β ∧ ∀ i ∈ K, traceValue β i = 0}` —
a subset of the **plane**, depending only on `c` and `K`, with no base centre and no angular state set.

> **(P1) `Z_K` is closed.** `TraceVector k` is compact (`isCompact_univ`, used already inside
> `state_support_avoiding_trace`); the trace graph is closed (`isClosed_traceGraph`,
> `Compactness.lean:284`, with the `mem_of_tendsto` pattern at `:292`); the conditions
> `traceValue β i = 0` are closed preimages under the continuous maps `β ↦ traceValue β i`
> (`traceCode_tendsto_iff`). Metrisability of `ℂ` makes sequential closedness enough.

> **(P2) Supports map into the carrier.** If `B` is a `RealState` at `x` represented by `K`, then
> `b ∈ (volume.restrict B).support ⇒ x + direction b ∈ Z_K` — this is `state_support_avoiding_trace`
> (`BoundaryTrace.lean:24`) verbatim, with **no** density, state continuity or L¹ input.

> **(P3) Triangle forcing.** Let `A` be a positive-measure `RealState` at `x` represented by `J`, with
> `(J ∪ K)ᶜ = {X}`. Then for `y, z ∈ Z_K` with `‖y − x‖ = ‖z − x‖ = 1`:
> `‖y − z‖ ≠ 1`.
>
> *Proof.* Pick K-avoiding traces at `y`, `z`. `avoiding_trace_palette` (`BoundaryTrace.lean:53`) gives
> `P_y ⊄ K`, `P_z ⊄ K` a.e.; `palette_neighbor_disjoint` (`FiveSupport.lean:23`, general in `k`) gives
> `P_y ⊥ P_x`, `P_z ⊥ P_x`, and — using `direction_exists` (`WeakColoring.lean:145`) with the unit
> vector `z − y` — `P_y ⊥ P_z`, all a.e. in one angular parameter `t`; four conull sets intersect.
> Transport to `ℝ` (`angleMk_quasiMeasurePreserving.ae`), intersect with the finitely many a.e.
> statements that `RealState hc x A J` supplies (`States.lean:92`), and choose `t ∈ A`
> (**this is the only use of `volume A > 0`**). Pick `i ∈ P_y(t) \ K`; disjointness gives `i ∉ J`; so
> `i ∈ (J ∪ K)ᶜ = {X}`; hence `X ∈ P_y(t)`, and symmetrically `X ∈ P_z(t)`, contradicting
> `P_y(t) ⊥ P_z(t)`. ∎

> **(P4) Finite-graph form.** For any finite family `{y_v} ⊆ Z_K` on the unit circle about `x`, the
> unit-distance graph on `{y_v}` is **properly colourable by labels of `L := (J ∪ K)ᶜ`** — take, for a
> common conull `t`, one label of `P_{y_v}(t) ∩ L` per vertex; adjacency forbids repetitions.
> `|L| = 1` recovers (P3).

**Limitation, stated exactly (A2 §9).** For `|L| = 2` this yields only *bipartiteness*. Unit chords on
one circle join angles differing by exactly `60°` (`‖2 sin(θ/2)‖ = 1 ⇔ θ = 60°`), so each orbit of
rotation by `π/3` is a 6-cycle and the graph is a disjoint union of 6-cycles — bipartite. Hence this
principle supplies **no** six-colour contradiction when two residual labels remain. That is a statement
about this principle on one circle, **not** about the full six-colour problem, and not about transports
between different circles.

## 2. Both consumers are instances of (P1)–(P3)

**Fixed centre — `Interfaces.lean:266` `interfaceStateSupport_no_unit`.** `hw`, `hg` (the current
state's `fourGroup ⊆ palette`), `s ≠ 0`, two points of `interfaceStateSupport x s`. Set
`r := 2 if s = 1 else 1`, `K := fourGroup s`, `J := fourGroup r`, `X := 4`; the file's own `by decide`
fact gives `(J ∪ K)ᶜ = {4}`. `four_state_represents_of_group hc hg` supplies both `RealState`s at the
**same** `x`; positivity of the `r`-state is `four_state_diagonal_positive_of_group` +
`angle_state_preimage_positive`; `angle_support_lift` moves the two angular points to `b, d ∈ ℝ`. Apply
(P3) with `y, z` the two unit points. **No `FourCenter` is used** — `hg` never supplies one.

**Converging centre — `FourContinuity.lean:441` `four_support_sequence_no_unit`.** `hx : ∀n,
FourCenter c (x_n)`, `hy : FourCenter c y`, `x_n → y`, `b_n → b₀`, `d_n → d₀`, and support memberships
`b_n, d_n ∈ fourSupport (x_n) s`. Same `r, K, J, X = 4`. For each `n`, (P2) applied **at `x_n`** gives
`x_n + direction b_n ∈ Z_K` and `x_n + direction d_n ∈ Z_K`; the limits `y + direction b₀`,
`y + direction d₀` lie in `Z_K` by (P1); both are at distance one from `y`; positivity of the `r`-state
at the limit is `four_realState_positive` (`FourContinuity.lean:419`). (P3) gives the conclusion.
**No `A_n`-L¹ input, no `four_realState_continuity`, no `strict_state_sequence_false`.**

Note the two limit traces may come from *different* subsequences. That is legitimate: each is an actual
trace at its own limit centre, and (P3) only needs the two entire palettes at those centres, plus a
finite intersection of conull constraints afterwards. It is **not** a claim that unrelated angular state
values form one joint word.

## 3. Exact statement chain (measured)

Root-side, Interfaces:

```
interfaceStateSupport_no_unit      Interfaces:266   -> (P3) at a fixed centre
  interfaceStateSupport_margin     Interfaces:281   (compact_no_unit_margin)
    four_interface_word_data       Interfaces:395   (uses margin at :406)
      no_four_interfaces           Interfaces:516   (uses word_data at :520)
        ... forest argument ...
```

Root-side, FourContinuity:

```
four_support_sequence_no_unit      FourContinuity:441 -> (P1)+(P2)+(P3) at the limit
  four_support_no_sixty            FourTransport:218  (constant sequence; consumer at :222)
  four_endpoint_sequence_false     Accumulation:32    (direct call at Accumulation:103)
    four_normalized_sequence_false Accumulation:233   (calls :241-245)
      four_sequence_no_accumulation Accumulation:246  (calls :267)
        four-centre discreteness / compact finiteness -> CyclicCore
```

## 4. Root dependency versus library content, measured

`rg -n "strict_state_uniform_on_compact" lean/` returns **one** line: its own declaration,
`FourContinuity.lean:361`. It has **no consumers**. Its body is where the last remaining call to
`States.lean:683` sits (`FourContinuity.lean:395`).

Two distinct notions, which must not be conflated:

* **Root / proof-term dependency.** After the two replacements, no *used* path reaches `States:683`:
  its consumers are `FourContinuity:395` (inside the unconsumed `strict_state_uniform_on_compact`) and
  `FourContinuity:452` (inside `four_support_sequence_no_unit`, replaced by §2). So the main theorem's
  proof term would no longer mention the strict-sequence chain.
* **Build / elaboration dependency.** `strict_state_uniform_on_compact` is still a *declaration* in the
  file; Lean still elaborates it, so its proof still needs `States:683` to exist. Deleting `States:683`
  would force deleting or re-proving that wrapper — an unused declaration does not "keep a used path
  alive", but it does keep a *compilation* dependency alive.

So the correct claim is: **the strict-sequence chain becomes root-unreachable while remaining
library content.** A compiler-level dependency audit (not performed here) is what would license any
deletion.

## 5. Minimum acyclic module move

Measured import edges: `FourContinuity → States`; `FourTransport → FourContinuity`;
`Accumulation → Exclusion, FourTransport`; `FiveSupport → Accumulation`; `BoundaryTrace → Rigidity,
States`; `Rigidity → PaletteTransport`; `AngularBoundary → BoundaryTrace`; `Interfaces → AngularBoundary`.

Therefore, in particular, **`PaletteTransport` is already upstream of `BoundaryTrace`** (through
`Rigidity`), and `FourContinuity` is nowhere upstream of `BoundaryTrace`.

**The move.** Create one module, say `OAI.Geometry.PlaneColoring.AvoidingTrace`, importing
`BoundaryTrace`, containing:
1. `palette_neighbor_real` and `palette_neighbor_disjoint` — **relocated** from `FiveSupport.lean:9–32`
   (they are general in `k` and need only `palette_smooth_transport`, available upstream);
2. the new `Z_K`, (P1), (P2) restated, (P3), and the converging-centre theorem.

Then let `FourContinuity` and `Interfaces` import it, and let `FiveSupport` re-export the two
relocated lemmas (or keep one-line aliases) so its own consumers are untouched.

*Acyclicity:* `AvoidingTrace → BoundaryTrace → {Rigidity → PaletteTransport → …, States → BinaryPalettes
→ …}`, none of which reaches `FourContinuity`. So `FourContinuity → AvoidingTrace` is acyclic.
**Do not import `FiveSupport` into `AvoidingTrace`**: `FiveSupport → Accumulation → FourTransport →
FourContinuity` would close a cycle. That is precisely why the two neighbour lemmas must be *moved*
rather than imported.

## 6. Preservation list (do not delete)

* `indicator_inter_positive` (`States.lean:415`) — still consumed by `FourContinuity.lean:326` inside
  `support_lower_semicontinuity`. **Keep.**
* Ordinary support continuity — `support_sequence_continuity`, `support_lower_semicontinuity`,
  `four_realState_continuity`, `stateSupport_local_pred`: general-purpose, keep even where the new
  proof no longer calls them.
* `circleEndpoint_identity_neighborhood`, `near_identity_circle_in`, `nonparallel_neighborhood`,
  `positive_state_support_point`, `support_density_direction`, `support_density_sequence`,
  `varying_pullback_L1`: currently feed only the strict-state branch; they become unused but are **not**
  deleted in this packet.
* The five-cycle lineage: Lemma 6.7 (`five_support_step_ban`), `FiveComb`, `CyclicCore` — untouched.

## 7. Grades

| item | grade |
|---|---|
| (P1) `Z_K` closed | [argued here] ingredients cited (`Compactness:284,292`; `traceCode_tendsto_iff`; `isCompact_univ`); **not** Lean-checked |
| (P2) support → carrier | [read] `BoundaryTrace:24` hypothesis shape |
| (P3) triangle forcing | [read] premise-by-premise against `BoundaryTrace:53`, `FiveSupport:23`, `WeakColoring:145`, `States:92` |
| (P4) and the `\|L\| = 2` limitation | [argued here] the 6-cycle/bipartite computation is exact |
| both consumer instances | [read] `Interfaces:266,281,395,516`; `FourContinuity:419,441`; `FourTransport:218,222`; `Accumulation:32,103,233,246` |
| `strict_state_uniform_on_compact` unconsumed | [measured here] single `rg` hit = its declaration |
| import edges / acyclicity | [measured here] `rg ^import` per module |
| root-vs-build distinction | [argued here] |
| local Lean status of A2 parts | [reported] fixed three-centre theorem and the contact-ban pair pass locally under 4.34.1/d13f23b with standard axioms; the carrier/converging-centre lemmas are **paper only** |
