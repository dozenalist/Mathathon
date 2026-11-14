# Maximal old-branch deletion: exact declaration boundaries, outside references, net accounting

Block 24. Source reading only; no build, no deletion. Grades **[S]** source read, **[S+]** follows at the
cited line, **[C]** my reading, **[U]** not determined.

## 0. Correction to my own previous report

My block-23 table listed `varying_pullback_L1`, `circleEndpoint_identity_neighborhood`, `near_identity_circle_in`,
`nonparallel_neighborhood`, `support_density_direction`, `support_density_sequence`,
`positive_state_support_point` under the heading "helper spans **inside** that block". That was wrong in form:
**all seven are top-level declarations with their own spans**, located *outside* `strict_state_sequence_local_false`
(`States:547–637`); they are merely *used* from inside it (or from inside another removable declaration). The
distinction matters because they are separate deletion targets with their own begin/end and their own reference
sets, and one of my enclosing attributions was actually wrong:

> **`support_density_direction` is used at `States:677`, which lies inside `support_density_sequence`
> (`States:672–682`)**, not inside `:547` as I wrote. Its deletion therefore depends on
> `support_density_sequence` going too, not on `:547`.

All spans below are `begin–end` computed as *declaration line* to *line before the next declaration* (section
headers and blanks included), so they are exact boundaries from the file's own declaration lines.

## 1. Removable declarations — exact spans and outside references

| # | declaration | file:span | lines | references | outside its own span? |
|---|---|---|---|---|---|
| 1 | `varying_pullback_L1` | `States.lean:389–414` | 26 | `States:601` | no — `:601` ∈ `:547–637` |
| 2 | `circleEndpoint_identity_neighborhood` | `States.lean:449–464` | 16 | `States:480` | no — `:480` ∈ `:465–526` (`near_identity_circle_in`) |
| 3 | `near_identity_circle_in` | `States.lean:465–526` | 62 | `States:569` | no — `:569` ∈ `:547–637` |
| 4 | `nonparallel_neighborhood` | `States.lean:527–542` | 16 | `States:567`, `:568` | no — both ∈ `:547–637` |
| 5 | `strict_state_sequence_local_false` | `States.lean:547–637` | 91 | `States:702` | no — `:702` ∈ `:683–703` |
| 6 | `positive_state_support_point` | `States.lean:642–660` | 19 | `States:701` | no — `:701` ∈ `:683–703` |
| 7 | `support_density_direction` | `States.lean:664–671` | 8 | `States:677` | no — `:677` ∈ `:672–682` (#8) |
| 8 | `support_density_sequence` | `States.lean:672–682` | 11 | `States:697`, `:698` | no — both ∈ `:683–703` |
| 9 | `strict_state_sequence_false` | `States.lean:683–703` | 21 | `States:713`, `FourContinuity:395`, `FourContinuity:452` | **yes, two of them** — see §2 |
| 10 | `strict_state_no_unit_support` | `States.lean:704–721` | 18 | `Interfaces:277`, `FiveSupport:144` | **yes, two** — the consumer swaps |
| 11 | `strict_state_uniform_on_compact` | `FourContinuity.lean:361–403` | 43 | — | **no reference at all** |

**Total removable: 288 lines in `States.lean` + 43 in `FourContinuity.lean` = 331 lines.**

Every reference listed is a *use site inside another declaration of this table*, except the three that are the
whole point of the exercise: #9's `FourContinuity:395` (inside #11) and `:452` (inside `four_support_sequence_no_unit`,
retained with a new body) and #10's two consumers. So the deletion is **closed under its own references** once
#11 is removed and the three bodies are swapped.

## 2. Ordering constraint (the cascade, now with exact spans)

1. swap #10's two consumers (`Interfaces:266–277` body, `FiveSupport:138–147` body) ⟹ #10 unused;
2. swap `four_support_sequence_no_unit`'s body (`FourContinuity:441–460`) ⟹ `:452` gone; delete #11
   (`FourContinuity:361–403`) — it has no consumer, and it is the last user of `States:395`;
3. now #9 (`States:683–703`) has no consumer ⟹ delete; ⟹ `:702` gone ⟹ #5 (`States:547–637`) unused ⟹ delete;
4. #6,#7,#8 (all `States:642–682`) are used only through #9 ⟹ delete the block `642–682`;
5. #1,#2,#3,#4 are used only through #5 and #2's own user (#3) ⟹ delete `389–414`, `449–542`.
   Note #2 and #3 are *before* #5, so a single text deletion must be done bottom-up or as separate hunks.

## 3. Not removable — explicit keep list (with the reason)

| declaration | span | why it stays |
|---|---|---|
| `indicator_inter_positive` | `States.lean:415–448` | used at `FourContinuity:326` inside `support_lower_semicontinuity` — **explicitly protected by the brief** |
| `support_lower_semicontinuity` | `FourContinuity.lean:311–335` | used at `FourContinuity:350` inside `support_sequence_continuity` |
| `support_sequence_continuity` | `FourContinuity.lean:336–357` | used at `FourContinuity:437` inside `four_support_continuity` |
| `angle_preimage_positive` | `FourContinuity.lean:407–413` | used by `four_realState_positive` (`:419-423`) on the new positivity route |
| `four_realState_positive`, `four_realState_continuity`, `four_support_continuity` | `FourContinuity.lean:419–440`, `432–460` | retained API; L¹ machinery deliberately kept |
| `complex_unit_orthogonal` | `States.lean:726–…` | **has a reference in another file** (`Sectors.lean:186`) — outside the branch, do not touch [S] |
| `indicator_inter_positive`'s neighbours `circleEndpoint…` etc. | — | covered above |

No blanket removal of `States.lean` is implied: `States` also exports `two_state_impossible` (`:243`),
`fourGroup`/`fourCanonical` (`:8-11`), `fourState` (`:325`), `fourState_represents` (`:333`),
`fourState_diagonal_positive` (`:351`), `RealState` (`:92`) — all on the new route and all retained.

## 4. Net accounting

| item | lines |
|---|---|
| deletable old branch (11 declarations) | −331 |
| new private module `MovingThreeCentres.lean` | +259 (my `wc -l`; the parent's 236 suggests a different/trimmed copy — **[U]**, flag before quoting a net figure) |
| `Interfaces:277` body swap | ±0 (one `exact` replaced by one `exact`) |
| `FiveSupport:138–147` body swap | −7 (a 3-line proof replacing 10 lines) [C] |
| **net** | **≈ −79** with 259-line module, **≈ −102** with 236-line module |

Neither figure should be quoted as certified: the module size discrepancy and the `FiveSupport` swap are not yet
settled. What *is* exact is the 331 deletable lines with their spans, and the fact that every one of them is
reachable only from inside the branch once #11 is removed.

## 5. What this block did not do

No deletion, no build, no dependency dump. The parent's compiler audit (51271/61231 constants, four forbidden
names and `sorryAx` absent) is treated as given: it establishes that the *new* proofs do not reach the old branch,
which is exactly what makes steps 1–2 of §2 safe. What remains is the mechanical hunk preparation, which the
spans above are meant to make exact.
