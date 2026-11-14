# Exact removal budget for the strict-state branch of `States.lean`

Member `m1`, swarm `smwgpubt5`, direction d2 (accounting, assignment A).

Every number below is printed by `accounting.py` in this directory; `accounting.out` is its
verbatim output (`python3 .ultramath/smwgpubt5/m1/accounting.py`, run from the repo root,
read-only, no build). Line numbers are 1-based and inclusive throughout.

Sources read: `supervisor/simplify-lean/INTEGRATION-PACKET.md` (186 lines),
`supervisor/simplify-lean/integration/{AvoidingTrace,FiveSupport,Interfaces,FourContinuity,States}.lean`,
and the originals `lean/OAI/Geometry/PlaneColoring/{States,FiveSupport,Interfaces,FourContinuity,Sectors,Accumulation,Exclusion,FourTransport,CyclicCore}.lean`.

---

## 1. The removed block: what is actually deleted

`difflib` edit script, original against the private copy (`accounting.out` §2):

```
States.lean   delete  old 525-722 (198 lines)   new 525-524 (0 lines)
```

**The packet's range is off by one.** §D says "source lines 524–721"; the 198 deleted lines are
**525–722**. 524 is `noncomputable section` and stays; 722 is a second `noncomputable section`
and goes. The count (198) is right, the boundaries are not.

Per-declaration budget (§3 of the output). The block is 198 lines = 173 declaration lines +
21 structural lines + 4 blank lines:

| declaration | lines | count |
|---|---|---|
| `nonparallel_neighborhood` | 527–539 | 13 |
| `strict_state_sequence_local_false` | 547–635 | 89 |
| `positive_state_support_point` | 642–657 | 16 |
| `support_density_direction` | 664–671 | 8 |
| `support_density_sequence` | 672–682 | 11 |
| `strict_state_sequence_false` | 683–703 | 21 |
| `strict_state_no_unit_support` | 704–718 | 15 |
| structural (section/open/namespace/end) | 525,526,540,541,543,544,545,546,636,637,639,640,641,658,659,661,662,663,719,720,722 | 21 |
| blank | 542, 638, 660, 721 | 4 |

So "seven declarations" is correct but understates what goes: **21 structural lines ride along**
(four `noncomputable section`, three `open`/`open scoped`, four `namespace EuclideanFiveColor`,
four `end EuclideanFiveColor`, four bare `end`). They are re-supplied by the surviving blocks, and
the private copy is scope-balanced: openers `namespace OAI`, `noncomputable section`,
`namespace EuclideanFiveColor`, `section Neighbor`, `section ThreeCentre`; closers
`end Neighbor`, `end ThreeCentre`, `end EuclideanFiveColor`, `end`, `end OAI` — 5 and 5,
`unclosed=0`, no errors (`accounting.out` §8). The block contains **no `variable`, no `attribute`,
no `instance`, no `set_option`**, so no binder or instance is silently lost for later declarations —
this is the one structural risk of excising a contiguous range, and it is absent here.

`States.lean` has exactly one import (`OAI.Geometry.PlaneColoring.BinaryPalettes`, line 1), so no
import can be dropped and none is added.

---

## 2. Consumer ledger, by declaration NAME

Whole-tree exact-name scan over all 83 `lean/**.lean` files; "in D" = enclosing declaration.

### 2.1 The seven removed declarations — every occurrence in the tree

| removed declaration | consumers (before the patch) |
|---|---|
| `nonparallel_neighborhood` | `strict_state_sequence_local_false` (States:567, 568) — **inside the removed block** |
| `strict_state_sequence_local_false` | `strict_state_sequence_false` (States:702) — inside the block |
| `positive_state_support_point` | `strict_state_sequence_false` (States:701) — inside the block |
| `support_density_direction` | `support_density_sequence` (States:677) — inside the block |
| `support_density_sequence` | `strict_state_sequence_false` (States:697, 698) — inside the block |
| `strict_state_sequence_false` | **`strict_state_uniform_on_compact` (FourContinuity:395)**; **`four_support_sequence_no_unit` (FourContinuity:452)**; `strict_state_no_unit_support` (States:713) |
| `strict_state_no_unit_support` | **`interfaceStateSupport_no_unit` (Interfaces:277)**; **`five_support_no_sixty` (FiveSupport:144)** |

Exactly **five** external consumer sites exist, in four declarations: `strict_state_uniform_on_compact`
(which has itself no consumer anywhere — the packet's deletion of FourContinuity:361–400 is sound),
`four_support_sequence_no_unit`, `interfaceStateSupport_no_unit`, `five_support_no_sixty`.
No removed declaration carries an attribute (`@[...]`, `instance`, `simp`), so no simp-set or
typeclass surface is withdrawn.

### 2.2 The five sites after the patch (verified in the integration copies)

| site | before | after |
|---|---|---|
| FiveSupport:144 | `exact strict_state_no_unit_support hc hw hX (fiveState_represents c hc hw hx j) (fiveState_represents c hc hw hx i) hp hi hs (direction_sixty_unit_real a)` | FiveSupport:122–123, same nine arguments, head replaced by `fixed_state_no_unit_three_centres` |
| Interfaces:277 | `exact strict_state_no_unit_support hc hw hl (four_state_represents_of_group hc hg r) … hb hd` | Interfaces:278–281, `fixed_state_no_unit_three_centres`, same argument list incl. `angle_state_preimage_positive …` |
| FourContinuity:452 (in `four_support_sequence_no_unit`) | 7-line tail calling `strict_state_sequence_false` | FourContinuity:412–415, 4-line tail calling `strict_state_sequence_no_unit_three_centres hc hw hxt hl …`; the declaration's own hypothesis list (402–407 vs 441–446) is **byte-identical** |
| FourContinuity:395 (in `strict_state_uniform_on_compact`) | the only consumer of itself | declaration **deleted** with its 40-line block 361–400; it had zero consumers |
| States:713 (inside `strict_state_no_unit_support`) | — | both gone together |

Residual textual mention of a removed name anywhere in the integrated tree: **one**, a docstring,
`AvoidingTrace.lean:147` (`/-- Same statement as \`States.lean:704\` strict_state_no_unit_support. -/`).
It is a comment, not a dependency.

### 2.3 The preserved declarations, with named live consumers

* **`indicator_inter_positive`** (States:415–421; statement `∀ᶠ n in atTop, 0<μ (B n∩D n)`)
  → `support_lower_semicontinuity` (FourContinuity:326) → `support_sequence_continuity`
  (FourContinuity:350) → `four_support_continuity` (FourContinuity:437) →
  `four_endpoint_sequence_false` (Accumulation:59, 60) → `four_normalized_sequence_false`
  (Accumulation:233) → `four_sequence_no_accumulation` (Accumulation:246) →
  `fourCenter_discrete` (Accumulation:273). Live through the ordinary four-state chain only; the
  patch removes its *other* consumer (`strict_state_sequence_local_false`, States:612).
* **ordinary four-state support continuity**, all untouched by the patch:
  `support_lower_semicontinuity` (FourContinuity:311–318), `support_sequence_continuity` (:336),
  `four_realState_continuity` (:423–427), `four_support_continuity` (:432–436),
  `four_support_sequence_no_unit` (:441–446, hypotheses unchanged). Consumers:
  `four_realState_continuity` ← `four_support_continuity` (FourContinuity:440) — after the patch
  this is its **only** consumer, since `four_support_sequence_no_unit` no longer uses it;
  `four_support_continuity` ← `four_endpoint_sequence_false` (Accumulation:59, 60);
  `four_support_sequence_no_unit` ← `four_support_no_sixty` (FourTransport:222) and
  `four_endpoint_sequence_false` (Accumulation:103); `four_support_no_sixty` ←
  `four_support_union_proper` (FourTransport:224) → `four_gap_exists` (:257).
* **`two_state_impossible`** (States:243–249) → `fourState_diagonal_positive` (States:378) and
  `four_state_diagonal_positive_of_group` (Interfaces:139). The latter is used by
  `interfaceStateSupport_no_unit` (Interfaces:266) — i.e. by exactly the declaration that the
  patch reroutes — so the chain stays live only because the reroute keeps that declaration.
* **manuscript Lemma 6.7 = `five_support_step_ban`** (FiveSupport:90–92) → `five_opposite_contacts_false`
  (FiveSupport:220, 221) → `five_sequence_small_no_accumulation` (CyclicCore:99) →
  `five_sequence_no_accumulation` (CyclicCore:121) → `fiveCenter_discrete` (CyclicCore:136).
  Retained verbatim: the FiveSupport edit script has no hunk anywhere near it (only lines 1, 9–31,
  144 change). Its single in-module dependency `palette_neighbor_disjoint c hc hw x a`
  (FiveSupport:79) keeps the same argument list, which requires `c` to stay **explicit** in the
  moved lemma — the packet's asymmetry is load-bearing and is satisfied by
  `variable {k : ℕ} (c : ℂ → Fin k) (hc : Measurable c)` at `AvoidingTrace.lean:15`.
* Also retained with external consumers: `complex_unit_orthogonal` (States:726) ←
  `triple_orthogonal_cover` (Sectors:186); `ae_direction_nonorthogonal` (States:752) ← five sites
  (Exclusion:131, 150; Interfaces:78, 412; Sectors:117).

### 2.4 Declarations that go **dead** but are deliberately kept

`varying_pullback_L1` (States:389, only consumer States:601, inside the removed block),
`near_identity_circle_in` (States:465, only consumer States:569, inside the block) and
`circleEndpoint_identity_neighborhood` (States:449, only consumer `near_identity_circle_in`,
States:480). The packet lists the first and third; `near_identity_circle_in` is in the same
position and should be named too. None of the three has any external consumer.

---

## 3. The added module, split into code, comment and blank

`AvoidingTrace.lean` = **235 lines** (not 236: `wc -l` is 235; 236 is the count after splitting on
`\n` and keeping the empty tail — packet §1's figure).

| class | lines |
|---|---|
| code | 189 |
| — of which verbatim moved from FiveSupport:9–31 | 23 (byte-identical, checked) |
| — of which module scaffolding (1,3,5,6,7,8,14,15,41,45,46,230,232,233,234,235) | 16 |
| — of which genuinely new proof code | **150** |
| comment / docstring (`/-!`, `/--`, `--`) | 26 |
| blank | 20 |
| **total** | **235** |

The 8 declarations are `palette_neighbor_real`, `palette_neighbor_disjoint` (moved),
`avoidingTraceCentre`, `triangle_no_unit_of_avoiding_traces`, `fixed_state_no_unit_three_centres`,
`avoidingTraceCentre_seqClosed`, `isClosed_avoidingTraceCentre`,
`strict_state_sequence_no_unit_three_centres`.

Cross-module consumers of the new module (exactly three import edges — `FiveSupport`, `Interfaces`,
`FourContinuity` → `AvoidingTrace`):

| new declaration | consumers |
|---|---|
| `palette_neighbor_disjoint` | `triangle_no_unit_of_avoiding_traces` (AvoidingTrace:78, 81, 92); `five_support_step_ban` (FiveSupport:79) |
| `fixed_state_no_unit_three_centres` | `five_support_no_sixty` (FiveSupport:122); `interfaceStateSupport_no_unit` (Interfaces:278) |
| `strict_state_sequence_no_unit_three_centres` | `four_support_sequence_no_unit` (FourContinuity:412) |
| `triangle_no_unit_of_avoiding_traces` | `fixed_state_no_unit_three_centres` (:158); `strict_state_sequence_no_unit_three_centres` (:228) |
| `avoidingTraceCentre` | `avoidingTraceCentre_seqClosed` (:163), `isClosed_avoidingTraceCentre` (:184), `strict_state_sequence_no_unit_three_centres` (:202, 203, 218, 221) |
| `palette_neighbor_real` | `palette_neighbor_disjoint` (:37) |

Acyclicity is checkable statically and holds: `closure(BoundaryTrace)` is 18 modules and contains
neither `FiveSupport` nor `Interfaces` nor `FourContinuity` nor `Accumulation` (`accounting.out` §9),
so the three added imports create no cycle.

---

## 4. NET DIFF

Per file (`wc -l`):

| file | before | after | delta |
|---|---|---|---|
| `AvoidingTrace.lean` (new) | — | 235 | **+235** |
| `FiveSupport.lean` | 376 | 354 | −22 |
| `Interfaces.lean` | 527 | 528 | +1 |
| `FourContinuity.lean` | 551 | 509 | −42 |
| `States.lean` (private) | 764 | 566 | −198 |
| **total** | 2218 | 2192 | **−26** |

Additions and removals, itemised (this is the honest form: the new module is not free):

| addition | lines |
|---|---|
| `AvoidingTrace.lean` | 235 |
| three `import OAI.Geometry.PlaneColoring.AvoidingTrace` lines | 3 |
| two rewritten call sites (FiveSupport:122, Interfaces:278) | 2 |
| new body of `four_support_sequence_no_unit` (FourContinuity:412–415) | 4 |
| **additions** | **244** |

| removal | lines |
|---|---|
| `States.lean` 525–722 | 198 |
| `FiveSupport.lean` 9–31 (moved lemmas) | 23 |
| `FiveSupport.lean` 144 (old call) | 1 |
| `FourContinuity.lean` 361–400 (`strict_state_uniform_on_compact`) | 40 |
| `FourContinuity.lean` 451–457 (old body) | 7 |
| `Interfaces.lean` 277 (old call) | 1 |
| **removals** | **270** |

**NET DIFF = 244 − 270 = −26 lines.**

By class: code 198 added − 266 removed = **−68**; comment +26; blank 20 − 4 = **+16**; total −26.
So the branch removal is worth **68 lines of code** against 2218 original lines (−3.1 % of the code
in the four touched modules), and the raw −26 is −1.2 % of their line count.

**Correction to the packet.** Its table sums to −26, not −27
(`235 − 22 + 1 − 42 − 198 = −26`). −27 is right only for the **corrected** module: deleting the
spurious line in 5.2 below gives a 234-line `AvoidingTrace`, 243 additions, NET DIFF **−27** and
code −69. Both figures are stated here for what they are.

---

## 5. Defects found in the delivered packet

1. **Range off by one** (§D): deleted range is 525–722, not 524–721 (Section 1).
2. **`AvoidingTrace.lean:230` is `end Generic`, and nothing opens a `Generic` section.**
   The file opens five scopes (`namespace OAI` :3, `noncomputable section` :5,
   `namespace EuclideanFiveColor` :8, `section Neighbor` :14, `section ThreeCentre` :45) and closes
   six (`end Neighbor` :41, **`end Generic` :230**, `end ThreeCentre` :232,
   `end EuclideanFiveColor` :233, `end` :234, `end OAI` :235). `accounting.out` §8 reports exactly
   one balance error, at line 230, with `section ThreeCentre` innermost. That an `end` whose name
   matches no open scope is a hard error was checked with the installed toolchain on a 4-line file
   with no imports (`endcheck.lean`, run as `lean endcheck.lean`, 0.9 s):

   ```
   endcheck.lean:3:0: error: Invalid name after `end`: Expected `ThreeCentre`, but found `Generic`
   ```

   So **the module as delivered cannot elaborate**; every claim downstream of it is vacuous until
   that line is removed. This directly contradicts packet
   block-24 §A.2 ("There is no `end Generic` in this file … If a downloaded copy shows one, it is
   from the pre-fix upload"): the copy in `integration/` *is* the pre-fix upload.
3. **Packet §2 is stale.** It says FiveSupport's changes are only `0a1` and `9,31d9`; the delivered
   copy also rewrites line 144 (the `five_support_no_sixty` reroute), as §C describes. §2's
   "−66 (−23, −40, −3)" therefore does not describe the artifact.
4. **Arithmetic**: −27 vs −26 (Section 4).
5. **Line count of the new module**: 235 by `wc -l`, not 236 (Section 3).

Confirmed correct in the packet: the 198/22/1/42 per-file deltas, "seven declarations",
"eight declarations" in the new module, `strict_state_uniform_on_compact` having no consumers, and
`five_support_no_sixty` being the last code consumer of `States:704`.

---

## 6. Staged second pass (not in the −26)

With the branch gone, two self-contained blocks of `States.lean` are dead and can go without
touching anything live:

* `varying_pullback_L1`, 389–414 (declaration 389–413 + blank), 26 lines — the section header
  385–388 stays, it is shared with `indicator_inter_positive`;
* 445–522, 78 lines (`circleEndpoint_identity_neighborhood` 449–464,
  `near_identity_circle_in` 465–520, with the section header 445–448 and closers 521–522).

104 further lines, taking `States.lean` from 566 to **462** and the cumulative net from −26 to −130.
Both blocks are scope-balanced on their own (checked). They are excluded from the main budget
because the packet deliberately stages them.

---

## 7. Unresolved obligations

1. **No compiler dependency dump.** I am forbidden to build or run lake, so every consumer claim
   here is textual (exact-name scan). It cannot see a goal closed by `simp`/`aesop`/`exact?`/
   `solve_by_elim` that used one of the seven removed lemmas, nor `include`/`omit` effects. None of
   the seven carries an attribute line, which removes the usual mechanism for such silent use, but
   that is evidence, not proof. The removal must not land in the shared tree before a
   `lake build`/dependency dump is reviewed.
2. **`end Generic` (5.2) blocks everything.** It must be deleted before any build; the file is
   otherwise the 234-line artifact the packet describes.
3. **The explicit/implicit variable asymmetry** (needed for `palette_neighbor_disjoint c hc hw x a`
   and `fixed_state_no_unit_three_centres hc hw …` to both elaborate) is verified textually only,
   at the call sites and at `AvoidingTrace.lean:15, 46`. Elaboration is the only real check.
4. **The replacement theorem's contract** is identical to `States:704` binder for binder
   (`{k} {c} (hc) (hw) {x} {J K} {X} (hlabels) {A B} (hA) (hB) (hp) {b d} (hb) (hd) :
   ‖direction (b : Angles) - direction (d : Angles)‖ ≠ 1`), whitespace aside; I checked the binder
   lists literally. Whether the proof term is accepted is the parent's build, not this report.
