# Integration and deletion map (source-level candidate; no build performed)

Companion to `MANUSCRIPT-REPLACEMENT.md`. All line numbers measured this block by `rg` over
`lean/OAI/Geometry/PlaneColoring/`. **End lines are estimates** (next declaration's start minus one);
counts are therefore estimates pending a build and a dependency dump.

## 1. Two different things, kept apart

* **Root-unreachable.** A declaration none of whose proof terms occurs on a used path from the main
  theorem. Removing such a declaration does not change the root's proof term.
* **Still elaborates.** A declaration that remains in the source is still *compiled*; its proof still
  needs every name it mentions. So a root-unreachable theorem can keep a *build* dependency alive.

An unused wrapper therefore does not keep a **used** path alive, and it does not disappear on its own.

## 2. Declaration map

| declaration | file:line | role | after the replacement |
|---|---|---|---|
| `two_state_impossible` | `States.lean:243` | older triangle/density argument; used by `fourState_diagonal_positive` for the positivity of the complementary state | **retained** |
| `varying_pullback_L1` | `States.lean:389` | feeds only the strict-state local proof | root-unreachable → removable candidate (26 lines est.) |
| `indicator_inter_positive` | `States.lean:415` | used at `FourContinuity.lean:326` in `support_lower_semicontinuity` | **retained** (external consumer) |
| `circleEndpoint_identity_neighborhood` | `States.lean:449` | strict branch only | removable candidate (16 est.) |
| `near_identity_circle_in` | `States.lean:465` | strict branch only | removable candidate (62 est.) |
| `nonparallel_neighborhood` | `States.lean:527` | strict branch only | removable candidate (20 est.) |
| `strict_state_sequence_local_false` | `States.lean:547` | the local moving-state contradiction | removable candidate (95 est.) |
| `positive_state_support_point` | `States.lean:642` | strict branch only | removable candidate (22 est.) |
| `support_density_direction` | `States.lean:664` | strict branch only | removable candidate (8 est.) |
| `support_density_sequence` | `States.lean:672` | strict branch only | removable candidate (11 est.) |
| `strict_state_sequence_false` | `States.lean:683` | global moving-state contradiction | root-unreachable after both replacements; still elaborates (21 est.) |
| `strict_state_no_unit_support` | `States.lean:704` | fixed-state exclusion | replaced by Corollary 6.10; becomes unused (≈10 est.) |
| `support_lower_semicontinuity` | `FourContinuity.lean:311` | general support API, carries `indicator_inter_positive` | **retained** |
| `support_sequence_continuity` | `FourContinuity.lean:336` | general support API | **retained** |
| `strict_state_uniform_on_compact` | `FourContinuity.lean:361` | **no consumers measured** (single `rg` hit = its declaration) | root-unreachable; still elaborates (~40 est.) |
| `four_support_sequence_no_unit` | `FourContinuity.lean:441` | consumer of `strict_state_sequence_false` at `:452` | body replaced by Theorem 6.11; statement unchanged (16 → 2 lines) |
| `interfaceStateSupport_no_unit` | `Interfaces.lean:266` | consumer of `States:704` at `:277` | body's last line replaced by Corollary 6.10; statement unchanged (3 → 1) |

**Consumers measured** (`rg`): `States:704` ← `FiveSupport.lean:144` (already replaced by the banked
joint-pair lemma) and `Interfaces.lean:277`. `States:683` ← `FourContinuity.lean:395` (inside the
unconsumed `strict_state_uniform_on_compact`) and `:452`. `States:547` ← only inside `States`.

## 3. Corrected accounting: the packet is net POSITIVE today

The formal worker's integration packet (`supervisor/simplify-lean/INTEGRATION-PACKET.md`, read-only
here) is measured precisely: `FiveSupport` `9,31d9` (−23), `FourContinuity` `361,400d361` (−40) and
`451,457c412,415` (−3), plus three import lines ⇒ **−66**; and it **adds** `integration/AvoidingTrace.lean`
at **236 lines** (8 declarations). So the packet as it stands is

```
   −66  (three diffs + 3 import lines)
  +236  (new module)
  ----
  +170  net, i.e. an INCREASE
```

Neither the worker's `−66` nor my earlier `−288` estimate is an achieved figure. The `AvoidingTrace`
module measured by comment class: **26** comment/docstring lines, **20** blank, **189** code.

## 3bis. Declaration-level removal budget for the strict-state branch

Conditional on the **last `FiveSupport` consumer** being replaced (the banked
`five_support_no_sixty_joint_pair`, local Lean pass, not yet integrated). With `States:704`'s consumer
at `FiveSupport.lean:144` gone as well, the whole branch is root-unreachable. Exact ranges measured in
`lean/OAI/Geometry/PlaneColoring/States.lean`; each end is the line before the next declaration, so the
namespace-closing `end` lines stay.

| declaration | exact range | lines | external consumers |
|---|---|---|---|
| `varying_pullback_L1` | 389–414 | 26 | **none** |
| `circleEndpoint_identity_neighborhood` | 449–464 | 16 | **none** |
| `near_identity_circle_in` | 465–520 | 56 | **none** |
| `nonparallel_neighborhood` | 527–539 | 13 | **none** |
| `strict_state_sequence_local_false` | 547–635 | 89 | only inside `States` |
| `positive_state_support_point` | 642–663 | 22 | **none** |
| `support_density_direction` | 664–671 | 8 | **none** |
| `support_density_sequence` | 672–682 | 11 | **none** |
| `strict_state_sequence_false` | 683–703 | 21 | consumers are `FourContinuity:395` (deleted by the packet) and `:452` (swapped) |
| `strict_state_no_unit_support` | 704–718 | 15 | `FiveSupport:144` (pending swap), `Interfaces:277` (swapped by the packet) |
| **total declarations** | | **277** | |
| scaffolding, if the emptied blocks go too | ≈ 6 | | `noncomputable section` / `open` / `variable` / `end` around 639–720 |

**Retained inside the same file, verified:** `two_state_impossible` (243–307) — used at
`States.lean:378` inside `fourState_diagonal_positive`, the positivity input; `indicator_inter_positive`
(415–441) — external consumer `FourContinuity.lean:326`.

**Net after both stages:** `+170 − 277 = −107` (≈ `−113` with the scaffolding), not `−288`, not `−66`.
The two consumption swaps themselves may add a line each; the figure is an integration-time measurement,
not a build-verified count.

## 3ter. The conceptual simplification, independent of the line count

The line budget is the wrong headline. What the replacement changes in kind:

* **Two objects instead of a sequence.** The old branch carried a moving family `{(x_n, B_n)}` with
  `L¹`-pullback, density-point selection and subsequence bookkeeping. The new argument needs one *fixed*
  geometric object — the closed set of centres at which a `K`-avoiding trace exists — and one *fixed*
  point `x` carrying the complementary state. Convergence is used once, through closedness.
* **Three local facts replace a multi-step estimate.** Trace compactness, closedness of the trace
  relation, and palette disjointness at unit distance. Each is already in the paper; none is new
  analysis. In particular no `L¹` continuity of ambient state sets is used anywhere.
* **The forcing step is now a colouring statement.** Corollary 6.12 says: finite unit graphs on the
  circle about a positive complementary-state centre are properly colourable by the residual label set.
  `|L| = 1` is the support exclusion; `|L| = 2` gives only bipartiteness, and on one circle the unit
  graph *is* bipartite — a precise negative boundary that the old formulation could not express.
* **Hypotheses are preserved, not weakened.** The fixed-state statement keeps the original header
  exactly (independently confirmed locally: exact old/new type equivalence, binder flags, and the
  transitive forbidden-dependency check, 51 271 fixed / 61 231 moving constants).

## 4. Minimum acyclic module move

Measured edges: `FourContinuity → States`; `FourTransport → FourContinuity`; `Accumulation →
Exclusion, FourTransport`; `FiveSupport → Accumulation`; `BoundaryTrace → Rigidity, States`;
`Rigidity → PaletteTransport`; `AngularBoundary → BoundaryTrace`; `Interfaces → AngularBoundary`.

New module `OAI.Geometry.PlaneColoring.AvoidingTrace`, importing **BoundaryTrace** (which already
supplies `PaletteTransport` through `Rigidity`), containing:
1. the two general neighbour-palette results **relocated** from `FiveSupport.lean:9–32`;
2. the carrier `Z_K` and its closedness, Lemma 6.8 (restated), Lemma 6.9, Theorem 6.11.
Then `FourContinuity` and `Interfaces` import it; `FiveSupport` re-exports the relocated pair.
**Do not** import `FiveSupport` into it — `FiveSupport → Accumulation → FourTransport → FourContinuity`
would close a cycle. That is the entire reason the two lemmas are moved rather than imported.

## 5. What is *not* exported to the manuscript

`Lemma 6.7` and `five_support_step_ban` stay exactly as they are; the five-cycle §6.3.4 text and its
`(6.6)`-based bookkeeping are untouched. No manuscript statement is deleted by this map; §6.3.3bis is
an *addition* whose Corollary 6.10 and Theorem 6.11 replace the role previously played by the
moving-state argument.
