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

## Honest scope: this is NOT yet a staircase equivalence

Cycle 1 advertised the six declarations as a staircase bridge; the supervisor's
review correctly narrowed that. Two specific problems:

1. **Weak-decreasingness is missing.** `subStair` producing a nonnegative list of
   the right length and weight does not make it a *partition*; the order
   statement (`WeakDec (subStair l)`) is still only checked computationally
   (Computation results, `staircase_and_T.ok`), not in Lean. This is the one
   addition that would turn the six lemmas into a genuine equivalence.
2. **`subStair_nonneg` carries no content.** For `Nat`-valued coordinates
   `0 <= x` is automatic, so it cannot establish absence of truncation. The
   substantive non-truncation evidence is `head_bound` (which forces
   `lambda_1 >= 2(k-1)+1`) together with `addStair_subStair` (which needs exactly
   that bound to apply `Nat.sub_add_cancel`). Keep the lemma, but do not cite it
   as truncation evidence.

## Dependency table

| Obligation | Why it matters | Status |
| --- | --- | --- |
| `WeakDec (subStair l)` | the other half of "mu is a partition" | **open** (computational only) |
| subtype-level `Equiv` | packages the two inverse laws as a genuine equivalence of the two families, length retained | open; needs the row above |
| `T` and `B_n` (= smallest part >= length) | bridges to BZ82/BP06 notation | not started |
| `Nat.Partition` bridge | the repo pin is a `Multiset` without consecutive indices | not started |
| BZ82 `phi`/`psi` | would let the kernel replace RR-C009's finite test | not started |
| `lake build RogersRamanujan` | proves the target actually builds with the pin | **not verified here** (no `.lake` checkout) |
