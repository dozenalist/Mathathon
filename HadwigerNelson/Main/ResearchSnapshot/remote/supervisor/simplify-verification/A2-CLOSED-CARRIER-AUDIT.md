# Audit: A2 extension (closed set of centres with avoiding traces) — claim by claim

Block 22. Source reading and proof analysis only. No builds, no computation. Grades **[S]** source read,
**[S+]** source read and the claim follows at the quoted line, **[P-v]** I checked the mathematics,
**[R]** correction of my own earlier text, **[C]** my reading.

## 0. Correction accepted: my "traceValue is continuous" justification was wrong

**[R]** In block 21 §6 I wrote that "`traceValue` is entrywise continuous, so the zero-on-`K` carrier is a
finite intersection of closed fibres". The referee is right that `traceValue` into **norm** L² is not continuous
in general in the weak trace topology, so that justification does not stand, and the conclusion must be rebuilt
from evaluation continuity. The correct argument, which needs only the *evaluations*:

* `isClosed_traceGraph : IsClosed {p : ℂ × TraceVector k | IsTrace c hc p.1 p.2}` (`Compactness.lean:284`), and
  `trace_limit` (`:289`) turns `x_n → y`, `β_n → β`, `IsTrace at x_n` into `IsTrace at y`;
* for `i ∈ K` the hypothesis is `traceValue β_n i = 0` *as a vector*, so `⟪traceValue β_n i, v⟫ = 0` for
  **every** test `v` and every `n`. Taking the limit with the single test `v := traceValue β i` and using
  continuity of the evaluation functional (`Compactness.WeakBall.continuous_eval`, or equivalently
  `traceCode_tendsto_iff`) gives `⟪traceValue β i, traceValue β i⟫ = 0`, hence `traceValue β i = 0` by
  `inner_self_eq_zero`;
* so zero-*vectors* do give a closed condition in the weak topology — but the proof must go through
  evaluations, not through continuity of `traceValue` into the norm.

Net effect on verdicts: **the closedness conclusion survives; my stated reason is retracted and replaced** by
the above. This is exactly A2-ext's §1 argument, and it is the right one.

## 1. Claim-by-claim review of A2-ext

|c #|claim|verdict|
|---|---|---|
|1|`Z_K = {y : ∃ β, IsTrace c hc y β ∧ ∀ i ∈ K, traceValue β i = 0}` is closed, defined in the plane and depending only on `c, K`|**[S+] TRUE** by the §0 argument; `ℂ` is metrizable so sequential closedness suffices, and the closed-projection formulation is equivalent|
|2|"this is not a claim that angular state supports vary upper semicontinuously"|**correct and important**: `Z_K` is a *larger* closed set containing the relevant points; no continuity of `A ↦ supp(volume|A)` is asserted|
|3|(S): `b ∈ supp(volume|B)` with `B` represented by `K` ⟹ `x + direction b ∈ Z_K`|**[S+] TRUE**: verbatim `state_support_avoiding_trace` (`BoundaryTrace.lean:24-27`), general in `k`, hypothesis is support membership|
|4|(E): for `y, z ∈ Z_K` with `|y-x| = |z-x| = 1`, `|y-z| ≠ 1`, given a positive `J`-state at `x` whose complement `J ∪ K` is `{X}`|**[P-v] TRUE**, and the proof-by-contradiction is what supplies the third *unit* displacement `z - y` needed by `palette_neighbor_disjoint` at base `y`. The unique-outsider forcing is elementary and needs neither palette cardinality nor `Disjoint J K`|
|5|(E) makes `Z_K ∩ ∂B(x,1)` compact and unit-distance-free|**TRUE** — `Z_K` closed and `∂B(x,1)` compact ⟹ closed subset of a compact set|
|6|converging-centre theorem: `x_n → x`, `B_n` represented by `K`, `A` represented by `J` with `volume A > 0`, `b_n, d_n ∈ supp(volume|B_n)` with `b_n → b`, `d_n → d` ⟹ `‖direction b − direction d‖ ≠ 1`|**[P-v] TRUE**: (S) puts `y_n, z_n ∈ Z_K`, closedness gives `y, z ∈ Z_K`, both at distance 1 from `x`, then (E). The two avoiding traces at the limits may come from *different* subsequences — legitimate because each is an actual trace at its own centre and the building blocks are `∀ᵐ` statements with finite intersections afterwards|
|7|contract change: adds `x_n → x` and a positive `J`-state **at** `x`; removes all `A_n` and their L¹ convergence; the two contracts are *not* claimed equivalent|**honest and correct as stated**; no equivalence is asserted|
|8|`FourContinuity:441` instance: `r = 2` if `s = 1`, `r = 1` if `s = 2`, `K = fourGroup s`, `J = fourGroup r`, `X = 4`|**[S+]** the `hl` computation is exactly the one already in the file (`FourContinuity.lean:447-449`, `by decide`)|
|9|`B_n = fourRealState (x_n) s` is represented by `K` via `fourState_represents` (`States.lean:333`), needs `FourCenter c (x_n)` — supplied as `hx n`|**[S+] TRUE**, signature `(hx : FourCenter c x) (s : Fin 3) : RealState hc x {t | fourState … = s} (fourGroup s)`|
|10|`A = fourRealState y r` represented by `J` at `hy`, positive by `FourContinuity:419 four_realState_positive`|**[S+] TRUE**; `four_realState_positive (hx : FourCenter c x) (hs : s ≠ 0)`|
|11|positivity routes through `fourState_diagonal_positive` (`States.lean:351`) whose proof uses `two_state_impossible` (`States.lean:243`), not any strict-sequence theorem|**[S]** `two_state_impossible`'s own hypothesis is `hcard : (Finset.univ \ (J ∪ K)).card ≤ 2` — an older triangle/density argument, no strict-sequence call. **This is the one place a transitive check was genuinely needed and it passes**|
|12|§9 finite-graph form: for a finite family `y_v ∈ Z_K` at unit distance from `x`, the unit-distance graph on `{y_v}` is colourable by labels in `L = Fin k \ (J ∪ K)`; for `|L| = 1` this is (E); for `|L| = 2` only bipartiteness follows, and the one-circle unit graph is already bipartite (orbits of rotation by `π/3` are **6**-cycles, and `C₆` is bipartite)|**[P-v] TRUE**, including the limitation. The parity point is easy to get wrong — `C₆` is even, so bipartite — and the conclusion "no six-colour contradiction from the one-circle residual argument with two residual labels" is correctly scoped|

**Nothing in §1–§5 adds a hypothesis to `four_support_sequence_no_unit`**: its binders (`hx`, `hy`, `hxt`,
`hs`, `hb`, `hd`, `hbs`, `hds`) map one-for-one onto the converging-centre contract, with `x := y` (the limit)
and the sequence `x n`.

## 2. Declaration-level forbidden-call audit (exact, from a name grep)

|declaration|calls `strict_state_sequence_false` (`States:683`)?|calls `strict_state_sequence_local_false` (`States:547`)?|calls `strict_state_no_unit_support` (`States:704`)?|
|---|---|---|---|
|`States:704` itself|yes (`:713`)|yes (`:702`)|—|
|`FourContinuity:361 strict_state_uniform_on_compact`|yes (`:395`)|no|no|
|`FourContinuity:441 four_support_sequence_no_unit`|yes (`:452`)|no|no|
|`Interfaces:277` (in `interfaceStateSupport_no_unit`)|no|no|**yes**|
|`FiveSupport:144` (in `five_support_no_sixty`)|no|no|**yes**|

So `States:683` has exactly **three** call sites (as A2-ext states), and `States:704` exactly **two**.
`strict_state_uniform_on_compact` has **no consumers** anywhere in `lean/OAI` — only its own declaration —
so it is unused library content, as claimed.

**`FourCenter` occurs 0 times in `Interfaces.lean`** (`grep -c` = 0), confirming both that
`interfaceStateSupport_no_unit` genuinely assumes no `FourCenter`, and that the FourTransport route was never
available there.

## 3. Minimal constant list for a future compiler dependency gate

If a gate is to check "no forbidden transitive call", the smallest set of names worth tracking is:

* **forbidden** (must not appear in the proof term of any retained root): `States.strict_state_sequence_local_false`,
  `States.strict_state_sequence_false`, `States.strict_state_no_unit_support`;
* **allowed inputs of the new route**: `BoundaryTrace.state_support_avoiding_trace`,
  `BoundaryTrace.avoiding_trace_palette`, `FiveSupport.palette_neighbor_real`,
  `FiveSupport.palette_neighbor_disjoint`, `Compactness.trace_limit`, `Compactness.isClosed_traceGraph`,
  `States.fourState_represents`, `States.fourState_diagonal_positive`, `States.two_state_impossible`,
  `FourContinuity.four_realState_positive`;
* **root statements whose axiom sets must be re-printed after the swap**: `FourContinuity.four_support_sequence_no_unit`,
  `Interfaces.interfaceStateSupport_no_unit`, `FiveSupport.five_support_no_sixty`, and the two local-banked
  declarations whose source hash is `9a904d4d…`.

That is nine positive names and three negative ones — a finite list, checkable by `#print axioms` on the five
roots plus a `grep`-free dependency dump, not by a broad search.

## 4. What this does not establish

* It is **not** a compiler dependency audit: no build was run and no declaration was swapped.
* It does **not** prove the generic `strict_state_sequence_false` under its unchanged hypotheses — A2-ext is
  explicit that the contract changed (convergence + positive complementary state at the limit), and the
  arbitrary-centre sequence theorem is untouched.
* `four_support_continuity` and `support_lower_semicontinuity` keep their L¹/`indicator_inter_positive`
  machinery; nothing there is removed.
* `States:704` and `:683` remain in the tree; deleting them needs the two consumer swaps **plus** the
  source-order question (BoundaryTrace imports States, so the new module must sit between them).
