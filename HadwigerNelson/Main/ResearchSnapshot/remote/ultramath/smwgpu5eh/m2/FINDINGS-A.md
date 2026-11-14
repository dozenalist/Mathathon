# Direction A — TYPE/BINDER + CONSUMER AUDIT of the packet

Member m2, swarm smwgpu5eh. **No build was run** (no `lean`, no `lake`). Everything below is
source reading, `rg`/`diff`/`sed`, and two Python one-liners over text (each < 0.2 s).
All paths are relative to the repo root. Nothing here is a compile claim.

---

## 0. Headline

1. `integration/AvoidingTrace.lean:148` `fixed_state_no_unit_three_centres` has a binder list and
   conclusion that are **character-for-character the same** as `States.lean:704`
   `strict_state_no_unit_support` once the section variable
   `variable {k : ℕ} {c : ℂ → Fin k} (hc : Measurable c)` (AvoidingTrace:46) is expanded, which is
   exactly what Lean does. Both original call sites keep **every argument unchanged**; the packet
   really does change only the identifier.
2. `integration/FourContinuity.lean:402` `four_support_sequence_no_unit` keeps the **original
   explicit `c`** binder and a signature that is identical to `FourContinuity.lean:441` after
   whitespace normalisation. Its two external consumers (`Accumulation.lean:103`,
   `FourTransport.lean:222`) need no change at all.
3. **No missed consumer.** All 20 name occurrences of the seven deleted declarations in the live
   library `lean/OAI` are accounted for; every one is either the declaration itself, a use inside
   another deleted declaration, or one of the four rerouted call sites. Verified by an exhaustive
   per-name scan of all 83 modules of `lean/OAI` (command in §4).
4. The private `integration/States.lean` is **exactly** the original with lines 524–721 removed
   (`diff` = empty), and that range is four *self-balanced* `noncomputable section … end`
   blocks whose only declarations are the seven named ones.

---

## 1. `States.lean:704` → `fixed_state_no_unit_three_centres`

### 1.1 Binder table (original vs packet)

`States.lean:704-711`:

```
lemma strict_state_no_unit_support {k : ℕ} {c : ℂ → Fin k}
    (hc : Measurable c) (hw : WeakColoring k c)
    {x : ℂ} {J K : Finset (Fin k)} {X : Fin k}
    (hlabels : ∀i, i∉J∪K ↔ i=X)
    {A B : Set ℝ} (hA : RealState hc x A J) (hB : RealState hc x B K)
    (hp : 0<volume A) {b d : ℝ}
    (hb : b∈(volume.restrict B).support) (hd : d∈(volume.restrict B).support) :
    ‖direction (b : Angles)-direction (d : Angles)‖≠1
```

`integration/AvoidingTrace.lean:148-154`, inside `section ThreeCentre` whose line 46 is
`variable {k : ℕ} {c : ℂ → Fin k} (hc : Measurable c)`:

```
theorem fixed_state_no_unit_three_centres (hw : WeakColoring k c)
    {x : ℂ} {J K : Finset (Fin k)} {X : Fin k}
    (hlabels : ∀ i, i ∉ J ∪ K ↔ i = X)
    {A B : Set ℝ} (hA : RealState hc x A J) (hB : RealState hc x B K)
    (hp : 0 < volume A) {b d : ℝ}
    (hb : b ∈ (volume.restrict B).support) (hd : d ∈ (volume.restrict B).support) :
    ‖direction (b : Angles) - direction (d : Angles)‖ ≠ 1
```

| binder | original | packet | same? |
|---|---|---|---|
| k | `{k : ℕ}` implicit | `{k : ℕ}` (section var) | ✔ |
| c | `{c : ℂ → Fin k}` **implicit** | `{c : ℂ → Fin k}` (section var) **implicit** | ✔ |
| hc | `(hc : Measurable c)` **explicit**, 1st explicit | `(hc : Measurable c)` (section var) **explicit**, 1st explicit | ✔ |
| hw | explicit | explicit | ✔ |
| x, J, K, X | implicit | implicit | ✔ |
| hlabels | explicit | explicit | ✔ |
| A, B | implicit | implicit | ✔ |
| hA, hB | explicit | explicit | ✔ |
| hp | explicit | explicit | ✔ |
| b, d | implicit | implicit | ✔ |
| hb, hd | explicit | explicit | ✔ |
| conclusion | `‖direction (b:Angles)-direction (d:Angles)‖≠1` | identical term | ✔ |

`lemma`→`theorem` is cosmetic (no effect on the type). `hc` remains explicit, so the call form is
`… hc hw …`, matching both call sites.

### 1.2 Mechanical confirmation

```
python3 -  # normalise both headers (strip all whitespace, cut at ':= by', strip 'lemma|theorem'+name)
ORIG: {k:ℕ}{c:ℂ→Fin k}(hc:Measurable c)(hw:WeakColoring k c){x:ℂ}{J K:Finset(Fin k)}{X:Fin k}(hlabels:∀i,i∉J∪K↔i=X){A B:Set ℝ}(hA:RealState hc x A J)(hB:RealState hc x B K)(hp:0<volume A){b d:ℝ}(hb:b∈(volume.restrict B).support)(hd:d∈(volume.restrict B).support):‖direction (b:Angles)-direction (d:Angles)‖≠1
PACK: (hw:WeakColoring k c){x:ℂ}{J K:Finset(Fin k)}{X:Fin k}(hlabels:∀i,i∉J∪K↔i=X){A B:Set ℝ}(hA:RealState hc x A J)(hB:RealState hc x B K)(hp:0<volume A){b d:ℝ}(hb:b∈(volume.restrict B).support)(hd:d∈(volume.restrict B).support):‖direction (b:Angles)-direction (d:Angles)‖≠1
MATCH with section prefix '{k}{c}(hc)': True
```

Note the section-variable prefix insertion is the only thing that is *not* literal text; that step is
Lean's documented behaviour for section variables used in a declaration's type, not an assumption of
mine. Nothing else differs.

### 1.3 Call sites — argument-by-argument

`diff <(sed '1i import OAI.Geometry.PlaneColoring.AvoidingTrace' lean/.../FiveSupport.lean) integration/FiveSupport.lean`:

```
10,32d9      <- the two palette_neighbor_* lemmas (23 lines)
145c122
<   exact strict_state_no_unit_support hc hw hX (fiveState_represents c hc hw hx j)
---
>   exact fixed_state_no_unit_three_centres hc hw hX (fiveState_represents c hc hw hx j)
```

Nothing else in the file changes; the two continuation lines are untouched, so all nine arguments
`hc hw hX (…) (…) hp hi hs (direction_sixty_unit_real a)` are literally the same tokens.
`hi : a ∈ fiveSupport c hc x i` is accepted where `b ∈ (volume.restrict B).support` is expected
because `FiveSupport.lean:83` defines
`fiveSupport x i := (volume.restrict (fiveRealState c hc x i)).support` — delta only.

`diff … lean/.../Interfaces.lean integration/Interfaces.lean` output in full:

```
278c278
<   exact strict_state_no_unit_support hc hw hl (four_state_represents_of_group hc hg r)
---
>   exact fixed_state_no_unit_three_centres hc hw hl (four_state_represents_of_group hc hg r)
```

**One line, one identifier, everything else byte-identical** — exactly as claimed.

If FiveSupport's `hl`/`hw`/`hc` had changed shape the call would break, but they did not: the
statement of `five_support_no_sixty` (packet:115) is identical to the original
(`hw : WeakColoring 5 c) {x : ℂ} (hx : FiveCenter c x) {a : ℝ} {i : Fin 5} (hi : a∈fiveSupport c hc x i) : a+sixty∉fiveSupport c hc x i`),
and so is `interfaceStateSupport_no_unit` (packet:266 vs original:265).

---

## 2. `FourContinuity.lean:441` → packet `four_support_sequence_no_unit`

Packet line 402, in the same `noncomputable section … namespace EuclideanFiveColor` with
`variable (c : ℂ → Fin 5) (hc : Measurable c)` (packet:373, original:413). **The explicit `c` binder
is retained** and the argument order is untouched; normalised comparison of the two headers:

```
4C ORIG: (hw:WeakColoring 5 c){x:ℕ→ℂ}{y:ℂ}(hx:∀n,FourCenter c (x n))(hy:FourCenter c y)(hxt:Tendsto x atTop (𝓝 y)){s:Fin 3}(hs:s≠0){b d:ℕ→ℝ}{b₀ d₀:ℝ}(hb:Tendsto b atTop (𝓝 b₀))(hd:Tendsto d atTop (𝓝 d₀))(hbs:∀n,b n∈fourSupport c hc (x n) s)(hds:∀n,d n∈fourSupport c hc (x n) s):‖direction (b₀:Angles)-direction (d₀:Angles)‖≠1
4C PACK: (identical)
4C MATCH: True
```

Full `diff` of the packet copy against the original (import inserted at line 1) has **exactly two
hunks**:

```
362,401d361        # 40 lines: strict_state_uniform_on_compact (orig 361-400)
452,458c412,415    # the body only: 7 lines -> 4
```

so `four_support_sequence_no_unit`'s **signature lines are not in the diff at all**. Its consumers
therefore need no edit, and in the live tree they are:

* `Accumulation.lean:103` — `exact four_support_sequence_no_unit c hc hw hyn hx hy ht hvlim hdt hvn hdn (direction_sixty_unit_real a)`
  (11 explicit binders `c hc hw hx hy hxt hs hb hd hbs hds`, plus the final `hu` argument obtained
  by unfolding `≠1` into `= 1 → False`; `b₀`/`d₀` are fixed by `direction_sixty_unit_real a`);
* `FourTransport.lean:222` — same shape.
  These are real **code** dependencies on the *declaration*, and they survive because the statement
  is unchanged.

New body's argument mapping (checked by hand against the new theorem's binder order):
`hc hw hxt hl` → `hc hw hxt hlabels`; `(fun n => fourState_represents … (hx n) s)` → `hB` with
`K := fourGroup s`; `(fourState_represents … hy r)` → `hA` with `J := fourGroup r`;
`(four_realState_positive … hy hr)` → `hp : 0 < volume A` with `A := fourRealState c hc y r`;
`hb hd` → `hb hd`; `hbs hds` → `hbs hds` (`fourSupport x s := (volume.restrict (fourRealState c hc x s)).support`,
`FourContinuity.lean:415`, so delta only). Order matches, arity matches (11 explicit).
`four_realState_positive` is at packet:380, i.e. **before** the lemma at 402 — no forward reference
(`rg -n '^(def fourRealState|lemma four_realState_positive|lemma four_support_sequence_no_unit)'` →
375, 380, 402).

---

## 3. The dropped `hL1` hypothesis

`strict_state_sequence_false` had an L¹-convergence hypothesis plus a continuity hypothesis; the new
`strict_state_sequence_no_unit_three_centres` has neither. The rerouted body therefore supplies
nothing for them and does not need `four_realState_continuity`. Consequences I can state without a
build: `four_realState_continuity` (original:424, packet:384) is **no longer used by
`four_support_sequence_no_unit`**; its only remaining use in the packet copy is line 401, inside
`four_support_continuity`, which is why the packet correctly does not delete it.

---

## 4. Consumer enumeration — all eight names, live tree

Command (one `rg`, 0.1 s), scope = the whole built library `lean/OAI` (83 modules):

```
rg -n -g 'lean/**/*.lean' '\b(strict_state_no_unit_support|strict_state_sequence_false|strict_state_sequence_local_false|nonparallel_neighborhood|positive_state_support_point|support_density_direction|support_density_sequence|strict_state_uniform_on_compact)\b' lean/
```

20 hits, all in `lean/OAI/Geometry/PlaneColoring/`, all classified by a Python one-liner that walks
back to the enclosing declaration:

| name | occurrence | kind | enclosing declaration | after integration |
|---|---|---|---|---|
| `nonparallel_neighborhood` | States:527 | decl | — | deleted |
| | States:567, 568 | code use | `strict_state_sequence_local_false` | deleted with it |
| `strict_state_sequence_local_false` | States:547 | decl | — | deleted |
| | States:702 | code use | `strict_state_sequence_false` | deleted with it |
| `positive_state_support_point` | States:642 | decl | — | deleted |
| | States:701 | code use | `strict_state_sequence_false` | deleted with it |
| `support_density_direction` | States:664 | decl | — | deleted |
| | States:677 | code use | `support_density_sequence` | deleted with it |
| `support_density_sequence` | States:672 | decl | — | deleted |
| | States:697, 698 | code use | `strict_state_sequence_false` | deleted with it |
| `strict_state_sequence_false` | States:683 | decl | — | deleted |
| | States:713 | code use | `strict_state_no_unit_support` | deleted with it |
| | FourContinuity:395 | code use | `strict_state_uniform_on_compact` | deleted with it (40-line hunk) |
| | FourContinuity:452 | code use | `four_support_sequence_no_unit` | **rerouted** ✔ |
| `strict_state_no_unit_support` | States:704 | decl | — | deleted |
| | FiveSupport:144 | code use | `five_support_no_sixty` | **rerouted** ✔ |
| | Interfaces:277 | code use | `interfaceStateSupport_no_unit` | **rerouted** ✔ |
| `strict_state_uniform_on_compact` | FourContinuity:361 | decl | — | deleted |

**Zero consumers outside this table. Nothing missed.**
The four external consumers are exactly the four the packet reroutes or deletes with, and the five
intra-chain names close over each other and over nothing else.

Outside `lean/OAI`, every occurrence of these eight names is a `.md`/`.txt` document or a docstring:
`supervisor/simplify-lean/INTEGRATION-PACKET.md`, `THREE-CENTRE-PLAN.md`, `JOINT-PAIR-AUDIT.md`,
`DOWNSTREAM-INTEGRATION-PLAN.md`, `MOVING-EXTENSION-PLAN.md`, `supervisor/simplify-architecture/*`,
`supervisor/simplify-verification/*`, `sprint/**` (historical snapshots, not under `lean/`), plus
docstrings only in `supervisor/simplify-lean/threecentre/*.lean` and
`supervisor/simplify-lean/jointpair/JointPairSupport.lean` (`:28`, `:34` — comment). The check harness
`supervisor/simplify-lean/lean/{AxiomRoots,BinderAudit,SignatureEquivalence,SignatureCheckFresh,EnergyShort}.lean`
contains **none** of the eight names, so the rename does not disturb it.

Inside the packet's own five files the only occurrence of any of the eight names is the docstring at
`AvoidingTrace.lean:147` ("Same statement as `States.lean:704` `strict_state_no_unit_support`").
That is a comment, not a dependency.

---

## 5. The deletion range 524–721 — structural check

* `diff <(sed '524,721d' lean/OAI/Geometry/PlaneColoring/States.lean) integration/States.lean` →
  **IDENTICAL**. So the private copy is exactly the original minus that range, nothing else (the
  import line and lines 722–764 are untouched; the 566 = 764 − 198 accounting holds).
* The range contains exactly four blocks, each self-balanced:
  `524 noncomputable section / 526 namespace EuclideanFiveColor / … / 540-541 end end`,
  `543 / 546 / … / 636-637`, `639 / 641 / … / 658-659`, `661 / 663 / … / 719-720`, 721 blank.
  Because each opened scope is closed inside the range, the join leaves a well-formed file.
* Declarations inside the range: `nonparallel_neighborhood` 527, `strict_state_sequence_local_false`
  547, `positive_state_support_point` 642, `support_density_direction` 664,
  `support_density_sequence` 672, `strict_state_sequence_false` 683, `strict_state_no_unit_support`
  704 — the packet's list is exact, and it is the complete list.
* `rg` for the seven names in `integration/States.lean` → 0 hits, so no retained declaration in the
  private copy dangles.

---

## 6. Side checks that bear on usability (kept short; B owns the full import argument)

* Moved-lemma name identity: `integration/AvoidingTrace.lean` opens `namespace OAI` /
  `noncomputable section` / `namespace EuclideanFiveColor` and its `section Neighbor` variable line
  `variable {k : ℕ} (c : ℂ → Fin k) (hc : Measurable c)` (line 15) is byte-identical to
  `FiveSupport.lean:8`, so `OAI.EuclideanFiveColor.palette_neighbor_real` and
  `palette_neighbor_disjoint` keep their fully-qualified names, their **explicit `c`**, and their
  statements. Their only live-tree consumers are `FiveSupport:29` (moves out with them) and
  `FiveSupport:101` `palette_neighbor_disjoint c hc hw x a` — unchanged call form, and FiveSupport
  now imports AvoidingTrace (line 1), through which the names are reachable.
* `closure(BoundaryTrace)` recomputed over the 83 modules = does **not** contain FiveSupport,
  Accumulation, FourContinuity, Interfaces or AvoidingTrace; it does contain PaletteTransport,
  Palettes, PaletteDensity, Coloring, WeakColoring, Compactness, States, Rigidity, BinaryPalettes.
  Every name AvoidingTrace itself uses (`palette_smooth_transport`, `ae_sin_sub_ne_zero`,
  `palette`, `mem_palette`, `liftPalette`, `paletteSet_measurable`, `ae_angular_of_ae_line`,
  `angleMk_quasiMeasurePreserving`, `ae_circle_palette_exclusion`, `RealState`, `IsTrace`,
  `TraceVector`, `traceValue`, `trace_limit`, `traceCode_tendsto_iff`,
  `state_support_avoiding_trace`, `avoiding_trace_palette`, `trace_bounds`, `direction_*`, `sixty`)
  is defined inside that closure. The names it does **not** reach (`FiveCenter`,
  `fiveState_represents`, `fiveState_diag`, `five_adj_four`, `stateSupport_nonempty_measure`,
  `four_realState_positive`, `direction_sixty_unit_real`) are used only by the three consumers,
  each of which has its own unchanged import set. No cycle: none of FiveSupport / Interfaces /
  FourContinuity is in `closure(BoundaryTrace)`.
* Explicit-status of the moved/delegated calls in AvoidingTrace is consistent with the callee
  declarations: `state_support_avoiding_trace c hc …`, `avoiding_trace_palette c hc …`,
  `trace_limit c hc …` (`BoundaryTrace:10` and `Compactness:254` both declare
  `variable {k : ℕ} (c : ℂ → Fin k) (hc : Measurable c)`, i.e. `c` **explicit**), while the local
  `{c}`-implicit declarations are called with `hc` only (`triangle_no_unit_of_avoiding_traces hc hw …`,
  `fixed_state_no_unit_three_centres hc hw …`, `avoidingTraceCentre hc K`,
  `avoidingTraceCentre_seqClosed hc K`, `strict_state_sequence_no_unit_three_centres hc hw …`).
  I did **not** find a residual `c hc` misuse; that is the already-fixed item (a) and I am not
  re-reporting it, only confirming I did not contradict it.

---

## 7. One delivery discrepancy (flagged once, not part of direction A)

The brief says AvoidingTrace has exactly two sections each closed once. The delivered file has
`section Neighbor:14 / end Neighbor:41 / section ThreeCentre:45 / **end Generic:230** / end ThreeCentre:232`,
i.e. an `end Generic` with no matching `section Generic`, in a file with only one copy on disk
(`rg --files -g '*.lean' | rg -i avoiding` → 1 hit; the repo has no git history: `fatal: your current
branch 'main' does not have any commits yet`). The packet itself anticipates this ("If a downloaded
copy shows one, it is from the pre-fix upload").
I treat the artifact on disk as the pre-fix upload, and nothing in §1–§6 depends on that line.
If the parent's compiled copy is the one without it, the only consequence for this audit is that the
line numbers I cite above (all ≥ 46 and ≤ 232 except the section table itself) are shifted by at
most one after its removal — the declaration *texts* are unaffected.

---

## 8. What I could not settle without a build

Exactly two things, both elaboration-level, neither a suspected defect:

1. Whether `hA.2 i hi` supplies the `∀ᵐ` shape that the packet's `hJae` block (AvoidingTrace:99-106)
   expects from `RealState hc x A J` (`States.lean:92`: `MeasurableSet A ∧ ∀ i∈J, A ≤ᵐ[volume] liftPalette c hc x i`).
   This is a proof-term question (B), not a type/binder question: the *statement* of
   `fixed_state_no_unit_three_centres` is unaffected either way.
2. Whether the four-line replacement body of `four_support_sequence_no_unit` elaborates. The
   statement is unchanged (§2), so even if the body failed, the consumer audit would be unaffected;
   only the packet's proof would be.

A precise statement of the residual risk, therefore: **the packet's interface work is correct as far
as text can establish it — identical binders, identical statements, no missed consumer, exact
deletion.** What remains unverified is proof-term elaboration, which this task forbids me to test.

---

## 9. Consumer side of the *new* API (no orphans, no stray users)

`rg -c '\b<name>\b' supervisor/simplify-lean/integration/*.lean` for the eight new declarations:

| new declaration | occurrences |
|---|---|
| `fixed_state_no_unit_three_centres` | AvoidingTrace 1 (decl), **Interfaces 1**, **FiveSupport 1** |
| `strict_state_sequence_no_unit_three_centres` | AvoidingTrace 1 (decl), **FourContinuity 1** |
| `triangle_no_unit_of_avoiding_traces` | AvoidingTrace 3 (decl + :158 + :228) |
| `avoidingTraceCentre` | AvoidingTrace 7 |
| `avoidingTraceCentre_seqClosed` | AvoidingTrace 2 |
| `isClosed_avoidingTraceCentre` | AvoidingTrace 3 |
| `palette_neighbor_real` | AvoidingTrace 2 (decl + :37) — no external user |
| `palette_neighbor_disjoint` | AvoidingTrace 4 (decl + :78 + :81 + :92), **FiveSupport 1** (:101) |

So each new theorem has exactly the callers the packet claims, the moved
`palette_neighbor_disjoint` keeps its one real caller in `FiveSupport:101` with the unchanged
argument list `c hc hw x a`, and `palette_neighbor_real` is purely internal after the move. No
declaration in the packet is orphaned, and no module outside the packet names any of the new
declarations (so nothing outside has to learn the new identifier).

Note (non-issue): `supervisor/simplify-lean/threecentre/FixedStateThreeCentres.lean:44` declares a
same-named `fixed_state_no_unit_three_centres`. It lives outside `lean/OAI` and is not imported by
anything in the library, so it cannot clash with the packet's declaration; it would only clash if
both were dropped into the same module path, which the packet does not propose.
