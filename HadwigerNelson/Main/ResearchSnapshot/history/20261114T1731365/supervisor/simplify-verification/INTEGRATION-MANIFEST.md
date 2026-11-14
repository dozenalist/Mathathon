# Private-integration verification manifest (three-centre replacement)

Block 23. Source reading and manifest construction only; no build, no computation. Grades **[S]** source read,
**[S+]** follows at the cited line, **[C]** my reading, **[U]** not determined by me.

## 1. Statement-comparison targets, including implicit binders

The gate is **type identity**, not "same-looking statement": compare `#check @OLD` with `#check @NEW` and
require the printed types to be identical, and separately compare `#print axioms`.

| # | OLD (FQ name, source span) | NEW (candidate) | comparison mode |
|---|---|---|---|
| S1 | `OAI.EuclideanFiveColor.strict_state_no_unit_support`, `States.lean:704-723` **[U end]** | `OAI.EuclideanFiveColor.fixed_state_no_unit_three_centres` (`supervisor/simplify-lean/threecentre/MovingThreeCentres.lean:142-153`) | **identical type required.** Binder pattern of the old one (read verbatim): `{k : ℕ} {c : ℂ → Fin k}` implicit, `(hc : Measurable c) (hw : WeakColoring k c)` explicit, `{x : ℂ}` implicit, `{J K : Finset (Fin k)}` implicit, `{X : Fin k}` implicit, `(hlabels : ∀ i, i ∉ J ∪ K ↔ i = X)` explicit, `{A B : Set ℝ}` implicit, `(hA : RealState hc x A J) (hB : RealState hc x B K)` explicit, `(hp : 0 < volume A)` explicit, `{b d : ℝ}` implicit, `(hb : b ∈ (volume.restrict B).support) (hd : d ∈ …)` explicit, conclusion `‖direction (b : Angles) - direction (d : Angles)‖ ≠ 1`. The new file's docstring claims exactly this; the type comparison is what settles it |
| S2 | `OAI.EuclideanFiveColor.four_support_sequence_no_unit`, `FourContinuity.lean:441-…` **[U end]** | same name, new proof | **type identical, body replaced.** Its binders (`hx`, `hy`, `hxt`, `hs`, `hb`, `hd`, `hbs`, `hds`) are all explicit; the new proof must not add `FourCenter` hypotheses beyond `hx`/`hy`, which are already there |
| S3 | `OAI.EuclideanFiveColor.interfaceStateSupport_no_unit`, `Interfaces.lean:266-277` | same name, body: replace only the final `exact strict_state_no_unit_support …` at `:277` | type identical; the six preceding lines (`angle_support_lift`, `four_state_represents_of_group`, `four_state_diagonal_positive_of_group`, `angle_state_preimage_positive`) stay |
| S4 | `OAI.EuclideanFiveColor.five_support_no_sixty`, `FiveSupport.lean:138-147` | same name, body via the joint-pair theorem already banked (sha `9a904d4d…`) | type identical |

## 2. Forbidden transitive constants (namespace-qualified)

`OAI.EuclideanFiveColor.strict_state_sequence_local_false` (`States.lean:547`),
`OAI.EuclideanFiveColor.strict_state_sequence_false` (`States.lean:683`),
`OAI.EuclideanFiveColor.strict_state_no_unit_support` (`States.lean:704`).

**Re-introduction risks** (a retained declaration whose *body* still calls one of them):
`OAI.EuclideanFiveColor.strict_state_uniform_on_compact` (`FourContinuity.lean:361`, calls `:683` at `:395`),
`OAI.EuclideanFiveColor.four_support_sequence_no_unit` (old body, `:452`),
`OAI.EuclideanFiveColor.five_support_no_sixty` (old body, `:144`),
`OAI.EuclideanFiveColor.interfaceStateSupport_no_unit` (old body, `:277`).

## 3. Required retained constants (namespace-qualified, all in `OAI.EuclideanFiveColor` unless noted)

`state_support_avoiding_trace` (`BoundaryTrace.lean:24`), `avoiding_trace_palette` (`:53`),
`palette_neighbor_real` (`FiveSupport.lean:9`), `palette_neighbor_disjoint` (`:23`),
`trace_limit` (`Compactness.lean:289`), `isClosed_traceGraph` (`:284`),
`fourState_represents` (`States.lean:333`), `fourState_diagonal_positive` (`:351`),
`two_state_impossible` (`:243`), `four_realState_positive` (`FourContinuity.lean:419`),
`angle_preimage_positive`, plus the types `RealState` (`States.lean:92`), `TraceVector`, `IsTrace`,
`traceValue`, `liftPalette`.

## 4. Minimal acyclic import placement

Proposed module **M**: imports `BoundaryTrace` (which imports `States` and `Rigidity`) and `Compactness`;
contains the two general neighbour lemmas (moved from `FiveSupport`) plus the closed-set lemmas and the three
theorems. Then `FourContinuity` and `Interfaces` import **M**, and `FiveSupport` imports **M** instead of
defining the neighbour lemmas itself.

**The one import-graph item I could not verify [U]**: whether `palette_neighbor_real`'s proof needs anything
from `PaletteTransport`/`Accumulation` that is *not* reachable from `BoundaryTrace`. It uses
`palette_smooth_transport` (PaletteTransport) and `ae_sin_sub_ne_zero`; if `PaletteTransport` is not upstream
of `BoundaryTrace`, then M must import it too, and the acyclicity argument needs re-checking. **Check this
before writing M.**

**Current fact worth recording**: `MovingThreeCentres.lean:28-30` imports `FiveSupport`, `BoundaryTrace` and
`FourContinuity`. That is legitimate for a private validation file, but it means `States:704` is *in scope*
there. The dependency gate must therefore test **proof terms** (`#print axioms`, dependency dump), never
imports.

## 5. How removing the unused `strict_state_uniform_on_compact` enables the deletion cascade

Exact consumers (spans, from a name grep, not counts):

| declaration | span | consumers (exact sites) |
|---|---|---|
| `strict_state_sequence_local_false` `:547` | `547-~680` **[U end]** | `States.lean:702` only — inside `:683` |
| `strict_state_sequence_false` `:683` | `683-702` (its last line `:702` calls `:547`) | `States.lean:713` (inside `:704`), `FourContinuity.lean:395` (inside `strict_state_uniform_on_compact`), `FourContinuity.lean:452` (inside `four_support_sequence_no_unit`) |
| `strict_state_no_unit_support` `:704` | `704-~723` **[U end]** | `Interfaces.lean:277`, `FiveSupport.lean:144` — **no others** |
| `strict_state_uniform_on_compact` | `FourContinuity.lean:361-…` | **none** — only its own declaration |

**Cascade.** Replace the two `:704` consumers (S3, S4) and the `:452` consumer (S2) ⟹ `:704` unused ⟹ delete
`704-~723` ⟹ `:683` still used by `:395` ⟹ **that is exactly why removing the unused
`strict_state_uniform_on_compact` is required** ⟹ with `:395` gone, `:683` unused ⟹ delete `683-702` ⟹ with
`:702` gone, `:547` has no consumer ⟹ delete `547-~680`.

**Helper spans inside that block** (each used at exactly one span, all inside the deleted ranges):

| helper | used at | enclosing |
|---|---|---|
| `varying_pullback_L1` | `States.lean:601` | inside `:547` ✓ |
| `near_identity_circle_in` (`:465`) | `:569` | inside `:547` ✓ |
| `nonparallel_neighborhood` | `:567`, `:568` | inside `:547` ✓ |
| `support_density_direction` | `:677` | inside `:547` (before `:683`) ✓ |
| `support_density_sequence` | `:697`, `:698` | inside `:683` ✓ |
| `positive_state_support_point` | `:701` | inside `:683` ✓ |
| `circleEndpoint_identity_neighborhood` (`:449`) | `:480` | **inside `near_identity_circle_in`** [C] — I infer the span, since `:465` opens it and the next declaration is later; **verify before deleting** |

**Must NOT be deleted** (they have consumers outside the block): `indicator_inter_positive` (`:415`, used at
`FourContinuity.lean:326`), `four_support_continuity` (L¹ machinery, retained), `four_realState_continuity`.
No blanket removal of `States.lean` or of ordinary continuity lemmas is implied by anything above.

## 6. Circularity review of `MovingThreeCentres.lean` (259 lines)

* `four_realState_positive` (`FourContinuity.lean:419-423`) — body read verbatim: `angle_preimage_positive`
  applied to `fourState_diagonal_positive`. **No strict-state constant.** ✓
* `fourState_diagonal_positive` (`States.lean:351`) → `two_state_impossible` (`States.lean:243`), whose body
  uses `ae_all_iff` and `ae_lineDensityZero_compl`. **No strict-state constant.** ✓
* Therefore the new proof's use of `four_realState_positive` at
  `MovingThreeCentres.lean:247` is **not circular**, and the positivity chain is
  `four_realState_positive → fourState_diagonal_positive → two_state_impossible`, all upstream and clean.
* The file's own `#print axioms strict_state_sequence_no_unit_three_centres` (`:254`) is the right gate.

**Caveats flagged, not objections:** (i) the file imports `FiveSupport`, so `:704` is in scope — a
proof-term gate is mandatory (§4); (ii) `triangle_no_unit_of_avoiding_traces` takes the two avoiding traces as
*arguments* (`hty`, `htz`, `hKy`, `hKz`), which is the right factoring: no hidden re-derivation of the trace
existence inside the core.
