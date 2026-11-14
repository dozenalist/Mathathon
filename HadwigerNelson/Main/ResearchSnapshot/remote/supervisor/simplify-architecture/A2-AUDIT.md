# A2 audit: the three-centre proof of fixed-state support exclusion

Source/analysis only. No build, no compute, no agents. Grades at §7.

## 0. Verdict

**A2 is sound at paper level.** Its statement is *identical* to `States.lean:704`
`strict_state_no_unit_support`; every one of its five analytic premises exists in the tree with the
hypotheses it needs; the finite-label forcing step is correct for **arbitrary** label cardinality; and
the three mechanical ingredients it silently needs (direction surjectivity, `liftPalette → palette`
transfer, `angularMeasure → volume` transport) are all present and are used in exactly this pattern
elsewhere. Its interface claim (`Interfaces.lean:266`) checks out: **one** call changes. Its
dependency claim (no call into `States:547/:683/:704` from the three ingredients) checks out at
declaration level.

The candidate **extension** (§5) is also contractible, and it does cover the `FourContinuity:452`
consumer — but it does **not** make `States:683` unused, because `FourContinuity:395` is a second
consumer (§6). So **no global `States` deletion** follows, as instructed.

## 1. Statement match, verified

`States.lean:704`:
```lean
lemma strict_state_no_unit_support {k : ℕ} {c : ℂ → Fin k}
    (hc : Measurable c) (hw : WeakColoring k c)
    {x : ℂ} {J K : Finset (Fin k)} {X : Fin k}
    (hlabels : ∀i, i∉J∪K ↔ i=X)
    {A B : Set ℝ} (hA : RealState hc x A J) (hB : RealState hc x B K)
    (hp : 0<volume A) {b d : ℝ}
    (hb : b∈(volume.restrict B).support) (hd : d∈(volume.restrict B).support) :
    ‖direction (b : Angles)-direction (d : Angles)‖≠1
```
A2's target is this, verbatim, for arbitrary `k` (not `k = 5`). ✓ Note `A` need not be periodic and
**no positivity of `B`** is assumed — A2 correctly keeps both facts.

`RealState` (`States.lean:92`): `MeasurableSet A ∧ ∀ i∈J, A ≤ᵐ[volume] liftPalette c hc x i`.
So `hA` gives, for each `i ∈ J`, `t ∈ A ⇒ t ∈ liftPalette x i` a.e. — A2's "one finite intersection
over labels in `J`" is exactly this finite `ae_all_iff` step. ✓

## 2. The proof, step by step

Let `‖direction b − direction d‖ = 1`, `y := x + direction b`, `z := x + direction d`. Then
`‖y − z‖ = 1` and `‖x − y‖ = ‖x − z‖ = 1`: a unit equilateral triangle, all three centres **fixed**.

1. **Traces at `y` and `z`.** `state_support_avoiding_trace` (`BoundaryTrace.lean:24`) has
   `(hw) {x} {A} {J} (hA : RealState hc x A J) {a} (ha : a ∈ (volume.restrict A).support) :
    ∃ b, IsTrace c hc (x + direction a) b ∧ ∀ i ∈ J, traceValue b i = 0` — **general in `k`** and
   taking exactly `RealState` + support membership. Applied with `hB` at `b` and at `d`: traces at
   `y`, `z` vanishing on `K`. ✓ (No positivity of `B` used — consistent with the statement.)
2. **Palette non-containment.** `avoiding_trace_palette` (`BoundaryTrace.lean:53`):
   `(hb : IsTrace c hc x b) (hJ : ∀ i∈J, traceValue b i = 0) : ∀ᵐ t ∂angularMeasure, ¬ palette x t ⊆ J`.
   Applied twice: a.e. `P_y(t) ⊄ K` and `P_z(t) ⊄ K`. ✓
3. **Three disjointness statements.** `palette_neighbor_disjoint` (`FiveSupport.lean:23`), general in `k`:
   `(hw) (x : ℂ) (a : ℝ) : ∀ᵐ t ∂angularMeasure, Disjoint (palette (x + direction a) t) (palette x t)`.
   * `(y,x)`: take base `x`, angle `b` — `x + direction b = y`. ✓
   * `(z,x)`: take base `x`, angle `d`. ✓
   * `(y,z)`: take base `y`, angle `α` with `direction α = z − y`, supplied by `direction_exists`
     (`WeakColoring.lean:145`: `(hu : ‖u‖ = 1) : ∃ t, direction t = u`) and `‖z − y‖ = 1`. ✓
   Each is a.e. for a **fixed** centre and angle, so the five conull sets (2 from step 2, 3 from here)
   can be intersected; no exceptional set depends on `t`. ✓
4. **Transport and selection.** All five are a.e. on `Angles`; pull back to `A ⊆ ℝ` by
   `angleMk_quasiMeasurePreserving.ae` — the same two-line pattern the tree uses in
   `five_support_prev` (`FiveSupport.lean:128–137`). Intersect with the finitely many a.e. statements
   from `hA`; the resulting conull set meets `A` because `volume A > 0`. **This is the only use of
   `hp`**, and it is essential. Pick `t`.
5. **Forcing.** `J ⊆ P_x(t)` from `hA`; `P_y(t)` disjoint `P_x(t)`; `P_y(t) ⊄ K`. Choose `i ∈ P_y(t) \ K`;
   `i ∉ J` by disjointness; `i ∉ J ∪ K`; `hlabels` gives `i = X`; so `X ∈ P_y(t)`. Same argument with
   `z` gives `X ∈ P_z(t)`, contradicting `P_y(t) ∩ P_z(t) = ∅`. ∎

**The finite-label fact is correct and needs no cardinality bound and no `J ∩ K = ∅`:** if
`(J ∪ K)ᶜ = {X}`, then from `i ∈ Q \ K` and `Q ∩ P = ∅` and `J ⊆ P` we get `i ∉ J`, hence
`i ∈ (J ∪ K)ᶜ = {X}`. ✓ Only finiteness of the label type (for `J ∪ K` to have a complement of the
stated form) is used, and that is `Fin k`. ✓

## 3. Retained vs removed, at declaration level

**Retained (called by the three ingredients):** `RealState` (`States:92`), `mem_palette`, `liftPalette`,
`ae_circle_palette_exclusion`, `ae_circle_typicalSampling`, `sample`, `support_good_sequence`,
`isCompact_univ`/`isSeqCompact` on `TraceVector k`, `trace_of_realization`, `traceCode_tendsto_iff`,
`traceValue_sampleCode`, `trace_bounds`, `tracePositive_le_palette`, `palette_neighbor_real`
(`FiveSupport:9`), `palette_smooth_transport` (PaletteTransport), `direction_exists`, plus the L²
(`Lp`) plumbing those use. That is: weak-trace compactness, fixed-palette L¹ transport, spectral
smoothing and the general weak-colouring assumptions are all **kept**.

**Removed from this theorem's dependencies:** `strict_state_sequence_local_false` (`States:547`),
`strict_state_sequence_false` (`States:683`), `strict_state_no_unit_support` (`States:704`) and their
descendants are **not** invoked by the three ingredients. I verified the two `BoundaryTrace` bodies and
`palette_neighbor_disjoint` at source: none mentions `strict_state_*`.

**Caveat, and A2 states it correctly:** `BoundaryTrace` *imports* `States` (for the `RealState` API).
Importing a module is not invoking its declarations; the strict-sequence chain stays outside the
declaration-level dependency cone of this replacement. That distinction is the whole point and it is
honest as written.

## 4. Interface application (`Interfaces.lean:266`) — verified

```lean
lemma interfaceStateSupport_no_unit (hw : WeakColoring 5 c) {x : ℂ}
    (hg : ∀ᵐ t ∂angularMeasure, fourGroup (fourState c hc x t) ⊆ palette c hc x t)
    {s : Fin 3} (hs : s ≠ 0) {t u : Angles}
    (ht : t ∈ interfaceStateSupport hc x s) (hu : u ∈ interfaceStateSupport hc x s) :
    ‖direction t - direction u‖ ≠ 1
```
* `hg` constrains the palette by the **current state's group**; it does **not** provide `FourCenter`
  (no `TransitionEdge` anywhere in the hypothesis). ✓ A2's claim confirmed.
* The proof's last line is the *only* call: `exact strict_state_no_unit_support hc hw hl
  (four_state_represents_of_group hc hg r) (four_state_represents_of_group hc hg s)
  (angle_state_preimage_positive … (four_state_diagonal_positive_of_group hc hw hg r hr)) hb hd`
  (`Interfaces.lean:277–279`). Its arguments are exactly a `RealState` for `fourGroup r`, a `RealState`
  for `fourGroup s`, a positivity, and two support memberships — i.e. the A2 theorem's hypothesis list,
  with `hl : ∀ i, i ∉ fourGroup r ∪ fourGroup s ↔ i = 4` from the file's own `by decide` fact. **Drop-in
  replacement.** ✓
* The alternate route is indeed not independent: `four_support_no_sixty` (`FourTransport.lean:218`)
  *takes* `hx : FourCenter c x`, which `hg` does not give; and its downstream
  `four_support_sequence_no_unit` calls `strict_state_sequence_false` at `FourContinuity.lean:452`.

## 5. The candidate extension: `Z_K` closed, and the `FourContinuity:441` consumer

Define, for a finite label set `K`,
```
Z_K := {x : ℂ | ∃ b : TraceVector k, IsTrace c hc x b ∧ ∀ i ∈ K, traceValue b i = 0}.
```

**Contract for `Z_K` closed.** Take `x_n → x` with `x_n ∈ Z_K`, witnesses `b_n`.
1. `TraceVector k` is compact: the tree already uses
   `(isCompact_univ : IsCompact (Set.univ : Set (TraceVector k))).isSeqCompact` at
   `BoundaryTrace.lean` (inside `state_support_avoiding_trace`). So pass to `b_{φ n} → b`. ✓
2. `IsTrace c hc x b` by `isClosed_traceGraph` (`Compactness.lean:284`,
   `IsClosed {p : ℂ × TraceVector k | IsTrace c hc p.1 p.2}`) applied via `mem_of_tendsto` with
   `(x_{φ n}, b_{φ n}) → (x, b)` — the exact usage pattern already present at `Compactness.lean:292`
   (`(isClosed_traceGraph c hc).mem_of_tendsto (hx.prodMk_nhds hb) …`). ✓
3. The zero constraints are closed: `∀ i ∈ K, traceValue b i = 0` is a finite intersection of
   preimages of `{0}` under the maps `b ↦ traceValue b i`, whose continuity in `b` is what
   `traceCode_tendsto_iff` supplies (it converts `b → b'` into coordinate convergence of every
   `traceValue`). ✓
So `Z_K` is closed, with **no** density or L¹ input. ✓ **This is the correct closed-projection
hypothesis**: compactness of the carrier plus closedness of the graph plus closedness of the linear
zero-conditions. All three are present.

**The application.** Let `x_n → x`, `x_n` four-centres, `b_n, d_n ∈` support of the `s`-state at `x_n`,
`b_n → b₀`, `d_n → d₀`, `‖direction b₀ − direction d₀‖ = 1`, and a positive `r`-state at the limit `x`.
Set `y_n := x_n + direction b_n`, `z_n := x_n + direction d_n`. Then `y_n → y := x + direction b₀` and
`z_n → z := x + direction d₀`, and `‖y − z‖ = 1`.

* **`y_n ∈ Z_K`**: apply `state_support_avoiding_trace` **at `x_n`** with the `s`-state `RealState` and
  `b_n ∈ supp` — it yields a trace at `y_n` vanishing on `fourGroup s`. Same for `z_n`. (Exactly the
  lemma A2 uses, applied per `n`; no limit input.)
* Hence `y, z ∈ Z_K` by closedness. **This replaces the missing support membership at the limit** —
  that is the whole idea, and it is sound.
* Then run A2's steps 2–5 with the *fixed* triple `x, y, z`: two traces at `y, z` avoiding `K` give
  `P_y ⊄ K`, `P_z ⊄ K`; three `palette_neighbor_disjoint` statements (with `direction_exists` for the
  `y,z` pair since `‖y − z‖ = 1`); `J ⊆ P_x(t)` a.e. from the limit state's `RealState` and its
  positivity; pick `t`; the finite-label fact gives `X ∈ P_y(t) ∩ P_z(t)`, contradiction.

**Conclusion:** the extension yields `four_support_sequence_no_unit` (`FourContinuity.lean:441`) with
**no** `A_n`-L¹ input and **no** call to `strict_state_sequence_false`. The `four_realState_continuity`
argument that the current proof passes in (`FourContinuity:455`) is not needed.

## 6. Consumer measurement — why no global deletion follows

Measured by `rg` over `lean/`:

| declaration | consumers |
|---|---|
| `strict_state_no_unit_support` (`States:704`) | `FiveSupport.lean:144` (in `five_support_no_sixty`), `Interfaces.lean:277`. **Both fixed-state** — both replaceable by A2. |
| `strict_state_sequence_false` (`States:683`) | `FourContinuity.lean:395`, `:452`. `:452` is `four_support_sequence_no_unit` (covered by §5); **`:395` is a second, different consumer** (subsequence form). |
| `strict_state_sequence_local_false` (`States:547`) | only inside `States` (proof of `:683`). |

So: A2 + the extension would make `States:704` unused and would remove one of `:683`'s two consumers,
but **`:395` keeps `:683` alive**. **No global `States` deletion is justified**, exactly as instructed.
A2's own recommendation — leave the old theorem present but unused by the fixed-state consumers, and
do the source-order refactor separately (since `BoundaryTrace` imports `States`, importing back would
cycle) — is the right disposition.

## 7. Grades

| item | grade |
|---|---|
| statement identity with `States:704` (incl. no `B`-positivity, no FourCenter/FiveCenter) | [read] `States.lean:92,704` |
| A2 steps 1–5, incl. the finite-label fact | [audited here, paper level] every premise cited to a line |
| the three mechanical ingredients (`direction_exists`, `liftPalette→palette`, `angularMeasure→volume`) | [read] `WeakColoring:145`, `States:92`, `FiveSupport:128–137` pattern |
| interface drop-in at `Interfaces:277` | [read] single call site, argument shapes match |
| `FourTransport:218` alternative is not independent | [read] it takes `FourCenter`; its downstream calls `States:683` at `FourContinuity:452` |
| `Z_K` closed (compactness + `isClosed_traceGraph` + closed zero-conditions) | [argued here] each ingredient cited; **not** Lean-checked |
| extension covers `FourContinuity:441` without `A_n`-L¹ | [argued here] |
| consumer counts / no global deletion | [measured here] by `rg` |
| machine verification | **none** in this block; A2 itself is pending independent review and Lean |

**Not claimed.** No analysis-free proof; no global `States` deletion; nothing here touches the
five-cycle branch or clause (V); no claim that the source-order refactor is unnecessary — only that it
is not needed for the mathematics.
