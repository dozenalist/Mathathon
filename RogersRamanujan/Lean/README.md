# Lean (L) -- RR127

## Build target (added in cycle 2 by Main)

`RogersRamanujan/Lean/` was outside the `Mathathon` hierarchy, so the default
build validated nothing of it. Cycle 2 adds a named target:

* `lakefile.toml` gains `[[lean_lib]] name = "RogersRamanujan"`,
  `globs = ["RogersRamanujan.Lean.*"]`;
* `RogersRamanujan.lean` (repository root) is the aggregator importing
  `RogersRamanujan.Lean.Staircase`.

```sh
lake build RogersRamanujan        # the intended command; see status below
```

**Status of `lake build`: NOT VERIFIED on the SAIR VM.** There is no `.lake/`
package checkout in this container, so Lake would first clone Mathlib v4.35.0 and
its eight dependencies; that is outside this block's budget and the VM has
already failed to elaborate `import Mathlib` once (6.4 GB of oleans against 15 GB
of RAM). The configuration is written and is expected to work wherever the
repository's pinned dependencies are present. This is recorded as an unverified
integration, not as a passing build.

## Verification that was actually run

Two commands, both executed here:

```sh
# 1. the module, standalone, against the local executable (Lean 4.33.1)
lean RogersRamanujan/Lean/Staircase.lean
#    exit 0, ~14 s; six #print axioms lines as recorded below.

# 2. the aggregator, which also proves the module path resolves
lean -o .scratch/olean/RogersRamanujan/Lean/Staircase.olean \
     RogersRamanujan/Lean/Staircase.lean
LEAN_PATH="$LEAN_PATH:$PWD/.scratch/olean" lean RogersRamanujan.lean
#    exit 0  <- the name `RogersRamanujan.Lean.Staircase` is the right module name
```

Independently, the supervisor compiled the same `Staircase.lean`
(SHA256 `C7ACBCD74866958596ACC458A7231939EBE01969A0723179BFDAAF263CBEB280`) with
the **pinned** Lean 4.35.0 (`eb6cafb7290e8bd5f2937522d8d804f58f02bafc`, exit 0)
and reported identical axiom sets. So the toolchain question is settled in favour
of the pin; the local 4.33.1 runs agree.

| theorem | axioms |
| --- | --- |
| `RR127.subStair_addStair` | `[propext]` |
| `RR127.head_bound` | `[propext, Quot.sound]` |
| `RR127.addStair_subStair` | `[propext, Quot.sound]` |
| `RR127.sum_addStair` | `[propext, Quot.sound]` |
| `RR127.weight_subStair` | `[propext, Quot.sound]` |
| `RR127.subStair_nonneg` | `[propext, Quot.sound]` |

All inside the event's allowed set; no `sorry`, no `admit`, no `sorryAx`, no
custom axiom, no `native_decide`, no `Classical.choice`.

## Cycle 2: the order statement is now proved (this IS a staircase equivalence)

`Lean/StaircaseOrder.lean` (integrated by Main from cycle-2 worker m2) supplies
what cycle 1 recorded as missing:

| theorem | statement |
| --- | --- |
| `RR127.subStair_weakDec` | `Pos l -> Gap l -> WeakDec (subStair l)` — **the order half** |
| `RR127.addStair_pos` | `Pos (addStair l)`, no hypothesis |
| `RR127.addStair_gap` | `WeakDec l -> Gap (addStair l)` — surjectivity onto coordinates |
| `RR127.addStairMap_subStairMap` | `addStairMap ∘ subStairMap = id` on `StairGap` |
| `RR127.subStairMap_addStairMap` | `subStairMap ∘ addStairMap = id` on `StairCoord` |
| `RR127.stairBridge` | the pair packaged (Init has no `Equiv`) |
| `RR127.subStairMap_facts` | length retained, `sum = n - k*k` |
| `RR127.allZero_of_weakDec_zero`, `subStair_zero_tail` | the zeros of a coordinate list are a terminal block, so a coordinate is "positive part ++ padding", and the padding must be kept because `addStair` needs the length |

Witnesses that the statement is not vacuous: `subStair [4,1] = [1,0]`;
`¬ WeakDec (subStair [1,3])`, so the `Gap` hypothesis is needed; and
`addStair [1] ≠ addStair [1,0]`, so padding carries the length.

`StairGap = {l // Pos l ∧ Gap l}` (length retained, positivity, gaps) and
`StairCoord = {m // WeakDec m}` (length retained, weakly decreasing `Nat` list,
trailing zeros allowed). So `StairGap ≃ StairCoord` is a genuine equivalence of
the two objects the contract names.

**Main's independent verification of this module.** Compiled here, exit 0,
axioms `[propext, Quot.sound]` or none for all 22 declarations, no `sorryAx`;
plus a separate non-vacuity file importing it and discharging by `rfl` that the
map computes (`subStairMap ⟨[7,3,1], _⟩ = ⟨[2,0,0], _⟩`), that both subtype round
trips fire at concrete elements, and that the order statement holds where claimed
while failing without `Gap`. The kernel also evaluates `subStair [7,3,1] = [2,0,0]`,
`addStair [5,3,3] = [10,6,4]`, `subStair (addStair [4,0,0]) = [4,0,0]`.

**Toolchain label, precisely.** This module is **LEAN_VERIFIED on Lean 4.33.1**
(the VM's executable). It has **not** been compiled on the pinned 4.35.0; the
cycle-1 base module was, independently, by the supervisor. Since `StaircaseOrder`
is `Init`-only and uses only `omega`/`simp`, a 4.35.0 run is expected to agree,
but it is not claimed. Under the event rules this makes the *pair* of modules
Lean-conditional on the pin until someone runs the pinned compiler.

Two integration fixes applied by Main: the module now imports
`RogersRamanujan.Lean.Staircase` rather than a copy, and `def StairGap`/
`def StairCoord` became `abbrev`, because with `def` the subtypes are opaque to
importers (`⟨⟩` notation and `rfl`-level checks then fail from outside the file).

## Superseded: the cycle-1 scope caveat

Cycle 1 advertised the six declarations as a staircase bridge; the supervisor's
review correctly narrowed that. Two specific problems:

1. ~~**Weak-decreasingness is missing.**~~ **Fixed in cycle 2:**
   `subStair_weakDec`. This was the one addition needed to turn the six lemmas
   into a genuine equivalence, and it is now kernel-checked.
2. **`subStair_nonneg` carries no content.** For `Nat`-valued coordinates
   `0 <= x` is automatic, so it cannot establish absence of truncation. The
   substantive non-truncation evidence is `head_bound` (which forces
   `lambda_1 >= 2(k-1)+1`) together with `addStair_subStair` (which needs exactly
   that bound to apply `Nat.sub_add_cancel`). Keep the lemma, but do not cite it
   as truncation evidence.

## Dependency table

| Obligation | Why it matters | Status |
| --- | --- | --- |
| `WeakDec (subStair l)` | the other half of "mu is a partition" | **DONE** (`subStair_weakDec`) |
| subtype-level bridge | packages the two inverse laws as a genuine equivalence, length retained | **DONE** (`StairBridge`, both round trips) |
| `T` and `B_n` (= smallest part >= length) | bridges to BZ82/BP06 notation | not started |
| `Nat.Partition` bridge | the repo pin is a `Multiset` without consecutive indices | not started |
| BZ82 `phi`/`psi` | would let the kernel replace RR-C009's finite test | not started |
| `lake build RogersRamanujan` | proves the target actually builds with the pin | **not verified here** (no `.lake` checkout) |
