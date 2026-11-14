# Integration packet: `AvoidingTrace` module + both consumers (block 23)

Complete private replacement sources. **No Lean run** (parent builds). Originals are read-only and
untouched; every replacement is a copy under `supervisor/simplify-lean/integration/`.

Grades: **[C] computed**, **[M] argument checked**, **[P] proposed/uncompiled**, **[S] reported**.

## 1. The four files

| file | role | sha256 |
|---|---|---|
| `integration/AvoidingTrace.lean` | **new** module, imports `BoundaryTrace` only | `087f55300f9f594a685b0b0a9a20e7eee23099f4cbca6555579344e590ab87ec` |
| `integration/FiveSupport.lean` | two neighbour lemmas move out; one import added | `cf3b95d62621947d34ac9f7003e6e2507b3d7492b39696a48aa49ac4c681a743` |
| `integration/Interfaces.lean` | fixed consumer swapped | `568fc119bee888946c7172992bcfd9796b5ffecc403007effa4ac049aa27f1ac` |
| `integration/FourContinuity.lean` | moving consumer swapped; unused uniform theorem removed | `8b24e593f6eb191378fc0953ce3bd66787a14c10f6b411c1cf40ef7ae6e84123` |

### `AvoidingTrace.lean` (236 lines, 8 declarations)

`palette_neighbor_real`, `palette_neighbor_disjoint` (moved **verbatim** out of `FiveSupport`),
`avoidingTraceCentre`, `triangle_no_unit_of_avoiding_traces`, `fixed_state_no_unit_three_centres`,
`avoidingTraceCentre_seqClosed`, `isClosed_avoidingTraceCentre`,
`strict_state_sequence_no_unit_three_centres`. Comment-stripped hole scan: 0/0/0/0.

Two variable blocks, deliberately different:

* the **neighbour lemmas** keep `variable {k : ℕ} (c : ℂ → Fin k) (hc : Measurable c)` — `c`
  **explicit** — because `FiveSupport`'s call site is `palette_neighbor_disjoint c hc hw x a` and must
  not change;
* the **three-centre** declarations use `variable {k : ℕ} {c : ℂ → Fin k} (hc : Measurable c)` — `c`
  **implicit** — because the `Interfaces` call site is `… hc hw hl …`, matching `States:704`'s own
  header.

That asymmetry is what keeps both call sites literally unchanged. It is not cosmetic.

## 2. [C] Exact diffs against the originals

`FiveSupport.lean` — `0a1` (import), `9,31d9` (the two lemmas, 23 lines). Nothing else.
`Interfaces.lean` — `0a1` (import), `277c278` (one identifier:
`strict_state_no_unit_support` → `fixed_state_no_unit_three_centres`, all nine arguments identical).
`FourContinuity.lean` — `0a1` (import), `361,400d361` (`strict_state_uniform_on_compact`, 40 lines),
`451,457c412,415` (the body of `four_support_sequence_no_unit`: 7 lines → 4).

Net: **−66 lines** (−23, −40, −3) and **+3 import lines**.

## 3. [C] Acyclicity

`AvoidingTrace → BoundaryTrace → {Rigidity, States}`; `closure(BoundaryTrace)` = 17 modules and
contains `PaletteTransport` (so `palette_smooth_transport` is reachable) but **not** `FiveSupport` and
**not** `Accumulation`. Therefore:

* `FiveSupport → {Accumulation, AvoidingTrace}` — no cycle (neither imports FiveSupport);
* `Interfaces → {AngularBoundary, AvoidingTrace}` — no cycle, and `Interfaces`' closure did **not**
  previously contain `FiveSupport`, so this does not drag it in;
* `FourContinuity → {States, AvoidingTrace}` — no cycle; `AvoidingTrace` does not reach `FourContinuity`.

In particular `FourContinuity` does **not** import `FiveSupport`, which would have cycled through
`Accumulation → FourTransport → FourContinuity`.

## 4. [C] The strict-state chain after integration

`rg` over the integrated copies plus the untouched tree:

| declaration | consumers before | consumers after |
|---|---|---|
| `strict_state_sequence_false` (:683) | States:704, FourContinuity:395 (inside the uniform theorem), FourContinuity:452 | **States:704 only** |
| `strict_state_uniform_on_compact` (:361) | none in the source | **deleted** (confirmed no consumers by exact-name `rg` over all 83 modules) |
| `strict_state_no_unit_support` (:704) | FiveSupport:144, Interfaces:277 | **FiveSupport:144 only** |

So both consumers named in the task are rerouted, and the uniform theorem — which had no consumers at
all — is removed. The chain survives solely through `FiveSupport:144`, which the **banked pair-support
replacement** (already passing locally, `9a904d4d…`) covers; that patch is not re-derived here.

`indicator_inter_positive` is **not** deleted: `FourContinuity:326` uses it in
`support_lower_semicontinuity`. `four_support_continuity`, `four_realState_continuity` and
`varying_pullback_L1` are likewise left in place.

**Do not read this as a completed deletion.** The claim is: after both patches land, the used paths to
the chain are gone; the declarations themselves remain until a compiler dependency dump is reviewed.

## 5. [C] Proposed build closure

Reverse-dependency closure of the four changed/new modules: **20 of 84**.

`AvoidingTrace` (new), `FiveSupport`, `Interfaces`, `FourContinuity`, `Accumulation`, `FourTransport`,
`CyclicCore`, `ContinuumLimits`, `FullApproximation`, `DiskAverages`, `DiskExtension`, `Mesh`,
`GraphCuts`, `GraphPatches`, `GraphRealization`, `HoleApproximation`, `PlanarCovers`, `Five`,
`Chromatic`, `NullSetRobust`.

From-scratch ancestor closure of the four: **26 modules** (the 20 above plus their 6 non-rebuilt
ancestors). Suggested queue order: build `AvoidingTrace` alone first (it depends only on the 17
modules of `closure(BoundaryTrace)`), then the other three, then the remaining 16 descendants.

Minimum check that the reduction is real: `Five`, `Chromatic`, `NullSetRobust` must still compile —
they are the modules that would notice a statement change.

## 6. [P] Remaining risks (all name/instance level)

1. `choose β hβ hβK using hy` in `avoidingTraceCentre_seqClosed` — fallback `Classical.choose`;
2. `IsSeqClosed.isClosed` needs the `FrechetUrysohnSpace ℂ` instance;
3. `AvoidingTrace` assumes `palette`, `mem_palette`, `liftPalette`, `palette_smooth_transport`,
   `ae_sin_sub_ne_zero` are reachable from `BoundaryTrace` — `closure(BoundaryTrace)` is 17 modules
   including `PaletteTransport`, so they should be, but the two moved lemmas were written in
   `FiveSupport`'s context and may need an `open` adjustment;
4. the two variable blocks must stay as delivered, or one of the two call sites breaks.

## 7. What is deliberately not done

* No shared file edited; no deletion outside the private copies.
* The `FiveSupport:144` reroute is not re-derived (banked pair covers it).
* No manuscript Lemma 6.7 claim: `five_support_step_ban` is retained and used.
* No global or `Interfaces`-margin consequence claimed. The moving theorem is a statement about
  converging centres in the local/angular model; it is not a result about weak colourings of the plane
  at large, and `6 ≤ χ(ℝ²) ≤ 7` is unchanged.

---

# Block 24 corrections and the States removal

## A. Two concrete AvoidingTrace defects fixed

1. **`{c}`-implicit call sites.** The three-centre declarations are declared with `{c}` implicit, so
   their local calls take `hc` only. Fixed: `triangle_no_unit_of_avoiding_traces c hc hw …` →
   `… hc hw …` (2 sites), `avoidingTraceCentre c hc K` → `avoidingTraceCentre hc K` (8 sites, which
   also covered the two `isClosed_avoidingTraceCentre c hc K` occurrences), and
   `avoidingTraceCentre_seqClosed c hc K` → `… hc K`. The **neighbour** lemmas keep `c` explicit and
   are still called `palette_neighbor_disjoint c hc hw x a` — that asymmetry is unchanged and
   deliberate.
2. **Section balance.** The delivered file opens exactly two sections, `Neighbor` (14) and
   `ThreeCentre` (45), and closes each once (`end Neighbor` 41, `end ThreeCentre` 232). There is no
   `end Generic` in this file — that string belonged to the earlier `MovingThreeCentres.lean`, not to
   `integration/AvoidingTrace.lean`. If a downloaded copy shows one, it is from the pre-fix upload.

`integration/FourContinuity.lean` already calls the local moving theorem as
`strict_state_sequence_no_unit_three_centres hc hw hxt hl …` — `hc` only — while the enclosing
`lemma four_support_sequence_no_unit` keeps the original consumer's **explicit** `c` binder untouched.

## B. Correction to the net line count

My block-23 figure of −66 was wrong: it omitted the new module. Corrected accounting, per file:

| file | original | now | delta |
|---|---|---|---|
| `AvoidingTrace.lean` (new) | — | 235 | **+235** |
| `FiveSupport.lean` | 376 | 354 | −23 (moved lemmas) + 1 (import) … net **−22** |
| `Interfaces.lean` | 527 | 528 | **+1** |
| `FourContinuity.lean` | 551 | 509 | **−42** |
| `States.lean` (private) | 764 | 566 | **−198** |

**Net across the whole packet: −27 lines** (+235 −22 +1 −42 −198), before any further helper removal.
So the honest statement is: the packet is very nearly line-neutral and its value is structural, not
linear.

## C. `five_support_no_sixty` rerouted

`FiveSupport.lean`'s `five_support_no_sixty` now ends with
`exact fixed_state_no_unit_three_centres hc hw hX (fiveState_represents c hc hw hx j)
(fiveState_represents c hc hw hx i) hp hi hs (direction_sixty_unit_real a)` — the same nine arguments
as the old `strict_state_no_unit_support` call, one identifier changed. This is the **last** code
consumer of `States:704`, and it is now gone. (The banked contact-ban patch remains an equally valid
route; this one is shorter and uses the already-proved theorem.)

## D. Private `States.lean` with the strict-state branch removed

`integration/States.lean` (566 lines, sha256 `904ba7ca7462856079999a8e6aa80fb64d1231f744392f7cca15f6e7f3ecf567`)
deletes **source lines 524–721**, 198 lines, containing exactly seven declarations:

`nonparallel_neighborhood` (527), `strict_state_sequence_local_false` (547),
`positive_state_support_point` (642), `support_density_direction` (664),
`support_density_sequence` (672), `strict_state_sequence_false` (683),
`strict_state_no_unit_support` (704).

**Verification before removal [C].** A whole-tree consumer scan over the *integrated* tree (my four
replacement copies substituted for the originals) found external consumers:
`strict_state_sequence_local_false` 0, `positive_state_support_point` 0, `support_density_direction` 0,
`support_density_sequence` 0, `strict_state_sequence_false` 0, `strict_state_no_unit_support` 0 code
consumers (the single hit is a docstring reference in `AvoidingTrace`), `nonparallel_neighborhood` 0.

**Retained, deliberately:** `indicator_inter_positive`, `varying_pullback_L1`,
`circleEndpoint_identity_neighborhood`, `near_identity_circle_in`, `complex_unit_orthogonal` (used by
`Sectors:157`), `ae_direction_nonorthogonal` (five consumers), and every ordinary continuity lemma.
The first four also scan as unconsumed, but they lie among declarations I have not individually
audited, so they are **staged, not removed** — a second, narrower pass can take them once their
neighbourhood is checked.

**Scope.** Removing the branch is safe on exact-name evidence only; no compiler dependency dump has
been run. The declarations must not be deleted from the shared tree until such a dump is reviewed.
