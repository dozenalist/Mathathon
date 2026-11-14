# RR127 cycle 2 — Direction D (Lean): the missing order statement

Worker m2. Scope: `RogersRamanujan/Lean/Staircase.lean` only. No git commands, no
`lake build`, no Mathlib, no edit outside this folder.

## What was missing

`Lean/README.md` dependency table: "`subStair` is weakly decreasing | the other
half of 'mu is a partition' | **computational only (checker)**".
`Counterexamples/REGISTRY.md` standing objection: "the staircase group order
(weak decreasing) is verified computationally and partly in Lean; Lean currently
proves nonnegativity but not the order." Both are now closed by proof, for all
lists, not for a bounded range.

## Files

| file | role |
| --- | --- |
| `StaircaseBase.lean` | byte-identical copy of `RogersRamanujan/Lean/Staircase.lean`, sha256 `c7acbcd74866958596acc458a7231939ebe01969a0723179bfdaaf263cbeb280`. Copied because this VM has **no `.olean`** for that module (`lean` cannot `import` a source-only module: "object file ... does not exist"), and I am not allowed to write into `RogersRamanujan/Lean/`. |
| `StaircaseOrder.lean` | the new material: `import StaircaseBase`, then `WeakDec` + the order law + the equivalence + padding, with `#print axioms` for every new theorem. |
| `StaircaseMerged.lean` | the **proposed single-file merge**: `Staircase.lean` with this material spliced in before `end RR127`. Compiles, exit 0. sha256 `0f383a62a676fe01eb14c441e12264d5a900d9b461875c12c2636c1121e15f47`. |
| `check_statement_vs_python.py` | statement cross-check (not a proof): recomputes `stair` on all gap partitions for `n <= 22` and pins the two hypotheses the Lean file says are essential. |

## Exact commands and outputs

```sh
cd RogersRamanujan/Lean/cycle2
LEAN_PATH="$PWD:$LEAN_PATH" lean StaircaseBase.lean     # exit 0, axiom lines as in Lean/README.md
LEAN_PATH="$PWD:$LEAN_PATH" lean StaircaseOrder.lean    # exit 0, ~6 s
python3 check_statement_vs_python.py                    # exit 0
```

The first command is not decoration: `import StaircaseBase` needs a `.olean`, and
this VM has none for `Lean/Staircase.lean` or for its copy. Plain
`lean StaircaseBase.lean` emits no `.olean` (Lean 4 needs `-o`, or a `lake`
build), so the runnable form is

```sh
LEAN_PATH="$PWD:$LEAN_PATH" lean -o StaircaseBase.olean StaircaseBase.lean
LEAN_PATH="$PWD:$LEAN_PATH" lean StaircaseOrder.lean
```

`StaircaseBase.olean` is a build artifact and is not shipped here; regenerate it
with the line above. `StaircaseMerged.lean` needs no `.olean` at all
(`lean StaircaseMerged.lean`, `import Init` only) — which is why the merge in
item 1 of the proposals is the right end state.

sha256: `StaircaseOrder.lean` `85f48cecd85993858bd677743631aed8ca82e2f0129465e1ffaa280d9d6850c5`,
`StaircaseMerged.lean` `0f383a62a676fe01eb14c441e12264d5a900d9b461875c12c2636c1121e15f47`,
`StaircaseBase.lean` `c7acbcd74866958596acc458a7231939ebe01969a0723179bfdaaf263cbeb280`,
`check_statement_vs_python.py` `67c952d5c9736857974e85d9423f52e944f29312f02cb49bd572638607ba6822`.

`StaircaseOrder.lean` full output (exit 0):

```
'RR127.subStair_weakDec' depends on axioms: [propext, Quot.sound]
'RR127.addStair_pos' depends on axioms: [propext, Quot.sound]
'RR127.addStair_gap' depends on axioms: [propext, Quot.sound]
'RR127.allZero_of_weakDec_zero' depends on axioms: [propext, Quot.sound]
'RR127.subStair_zero_tail' depends on axioms: [propext, Quot.sound]
'RR127.subStair_length_sum' depends on axioms: [propext, Quot.sound]
'RR127.addStair_length_sum' depends on axioms: [propext, Quot.sound]
'RR127.addStairMap_subStairMap' depends on axioms: [propext, Quot.sound]
'RR127.subStairMap_addStairMap' depends on axioms: [propext, Quot.sound]
'RR127.nonneg_is_vacuous' does not depend on any axioms
'RR127.subStairMap_facts' depends on axioms: [propext, Quot.sound]
'RR127.witness_41' does not depend on any axioms
'RR127.witness_weakDec_41' depends on axioms: [propext, Quot.sound]
'RR127.witness_gap_hypothesis_needed' does not depend on any axioms
'RR127.witness_padding' depends on axioms: [propext, Quot.sound]
'RR127.witness_padding_carries_length' does not depend on any axioms
```

All sixteen compiled. No `sorry`, no `admit`, no `sorryAx` (the axiom lines would
show `sorryAx`), no custom axiom; `{propext, Quot.sound}` is inside the allowed
set. Nothing in this folder was taken on trust from a failed run: the only
failed elaborations during the work were my own first drafts (a `show` whose
arithmetic shape was not definitionally the goal, and `by decide` on `Gap`/
`WeakDec`, which have no `Decidable` instance here); both were fixed, and the
final file is the one that produced the output above.

## The statements that are now proved

```lean
def WeakDec : List Nat → Prop            -- weakly decreasing
theorem subStair_weakDec : ∀ l, Pos l → Gap l → WeakDec (subStair l)
theorem addStair_pos    : ∀ l, Pos (addStair l)              -- no hypothesis needed
theorem addStair_gap    : ∀ l, WeakDec l → Gap (addStair l)

def StairGap   := { l : List Nat // Pos l ∧ Gap l }          -- D-shaped, length kept
def StairCoord := { m : List Nat // WeakDec m }              -- coordinates, zeros kept
def subStairMap : StairGap → StairCoord
def addStairMap : StairCoord → StairGap
theorem addStairMap_subStairMap : ∀ l, addStairMap (subStairMap l) = l
theorem subStairMap_addStairMap : ∀ m, subStairMap (addStairMap m) = m
structure StairBridge := …               -- toFun/invFun/left_inv/right_inv (core Lean has no `Equiv`)
def stairBridge : StairBridge

theorem subStairMap_facts (l : StairGap) :
    (subStairMap l).1.length = l.1.length ∧
    (subStairMap l).1.sum    = l.1.sum - l.1.length * l.1.length
def AllZero : List Nat → Prop
theorem subStair_zero_tail : subStair lam = a :: rest → a = 0 → AllZero rest
```

So `subStair` and `addStair` are now inverse on the **correctly specified
subtypes**: `StairCoord` is not "multisets of positive integers" but
*length-k weakly decreasing lists of naturals, zeros allowed*. That is the
content of "keep the length retained and zero padding explicit":

* length is retained by the subtype (`subStairMap_facts`, first component);
* zeros are real coordinates, not dropped parts: `AllZero` + `subStair_zero_tail`
  say the zeros of a coordinate list form a **terminal block**, so a coordinate
  list is positive prefix ++ zero padding;
* the padding cannot be discarded: `witness_padding_carries_length` proves
  `addStair [1] ≠ addStair [1,0]` (`[2]` vs `[4,1]`). Dropping the trailing zero
  loses the length `k` that `addStair` consumes, so the two subtypes are the only
  correct specification.

## Two honest technical remarks

1. **`subStair_nonneg` carries no content.** `0 <= x` for `x : Nat` is
   `Nat.zero_le x`, true for *every* list, positive or not, gap or not. The
   frozen file's `subStair_nonneg` uses `Pos`/`Gap` in its proof but needs
   neither; `nonneg_is_vacuous : ∀ (l : List Nat) (x : Nat), x ∈ l → 0 ≤ x`
   records this, machine-checked, `[no axioms]`. Nonnegativity is not a lemma
   about partitions.
2. **The order law does not need `head_bound`.** `subStair_weakDec` is proved
   from `b + 2 ≤ a` alone, by `omega`, which handles truncating `Nat` subtraction
   by case split. So the non-truncation bound `2*rest.length+1 ≤ a` (needed by
   `addStair_subStair`) is not needed for the order half: even where `Nat`
   subtraction truncates, the staircase image stays weakly decreasing. Nothing
   in the proof is vacuous: `witness_gap_hypothesis_needed` shows `[1,3]` is
   positive with `¬ WeakDec (subStair [1,3])` (`[0,2]`), so `Gap` is doing real
   work, and `witness_weakDec_41` checks the conclusion on `[4,1] ↦ [1,0]`.

## What is NOT proved (do not read more into this)

* **Nothing here touches `A_n`, `phi`, `psi`, `T`, `B_n`, or the Mathathon
  objective.** The staircase bridge is only the second half of the reduction
  `D_n ↔ coordinate lists`; the residue-to-staircase step is still the hard part
  (`Main/DECISIONS.md` D-5, `Main/RESULTS.md`).
* The `Nat.Partition` bridge is still not started, and `lakefile.toml` is
  untouched: `RogersRamanujan/Lean/` is still outside the `Mathathon` hierarchy.
* **Toolchain mismatch unchanged.** `lean --version` here is 4.33.1;
  `lean-toolchain` pins `v4.35.0`. These theorems are therefore kernel-checked on
  4.33.1 only, exactly the caveat already recorded in `Lean/README.md`. Nothing
  in the file is version-specific in any way I can see, but I did not run 4.35.0.
* `WeakDec`, `AllZero`, `StairBridge` are mine, not frozen API. `StairBridge` is
  a hand-rolled `Equiv` because core `Init` has no `Equiv` (it lives in
  Std/Mathlib, which D-4 forbids).

## Proposed changes for Main (I edited nothing outside this folder)

1. Merge `StaircaseOrder.lean`'s body into `RogersRamanujan/Lean/Staircase.lean`
   immediately before `end RR127`, deleting the `import StaircaseBase` line. The
   splice is verified to compile as one file: `StaircaseMerged.lean`, exit 0,
   sha256 `0f383a62a676fe01eb14c441e12264d5a900d9b461875c12c2636c1121e15f47`.
   Then `lean RogersRamanujan/Lean/Staircase.lean` remains the single
   verification command with no `.olean` and no copy of a source file.
2. In `Lean/README.md`: change the dependency-table row "`subStair` is weakly
   decreasing" from `computational only (checker)` to `proved (subStair_weakDec)`,
   add the new rows, and change the sentence "Lean currently proves
   nonnegativity but not the order" in `Counterexamples/REGISTRY.md` (standing
   objections) — that objection is now stale, and the nonnegativity it refers to
   was never content.
3. `PROGRESS.md` currently says "6 staircase theorems kernel-checked"; after the
   merge it is 16 new + 6 old, and RESULT wording "the staircase reduction is
   kernel-checked" can be strengthened to "the staircase *equivalence* is
   kernel-checked (both directions, correct subtypes)".
4. Re-run on the pinned toolchain `v4.35.0` before quoting any of this in a
   submission.
